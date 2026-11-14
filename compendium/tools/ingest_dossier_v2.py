"""Ingest Deep Knowledge Dossier v2 sets into the WAi Human Knowledge Compendium (stdlib only).

usage:
  python ingest_dossier_v2.py [set.json ...]   ingest given sets (default: enrichment/dossiers/*.json)
  python ingest_dossier_v2.py --refresh        rebuild derived tables/cards/exports only (cheap; cycle-safe)

Storage model
- Source of truth stays append-only in `assets`/`edges`: each dossier revision is an immutable asset
  `dossier:vertical:<ID>:v2:<sha12>`, linked `enriches` -> the vertical and `supersedes` -> its previous revision.
- `dk_current` points each vertical at its current revision.
- Everything else is a derived projection rebuilt from current revisions: dk_* tables, the dk_search FTS5 index,
  machine_card_cache v2 blocks and exports/dossiers_v2.jsonl. Rebuilding is deterministic and idempotent.
- Entities (person:, work:, school:) are deduplicated across all dossiers by normalized slug; first sighting wins
  the immutable asset, later variants stay visible in the dk_* rows.
- Source-binding results from bindings.sqlite (bind_sources.py) are attached read-only and projected onto
  dk_* rows (bound_status) and card counts. Authored text is never edited by binding.
Takes CYCLE.lock (unless the caller already holds it), makes an online backup before writing, and runs in one transaction.
"""
import datetime, glob, hashlib, json, re, sqlite3, sys, time, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compendium as k  # noqa: E402

DOSSIER_DIR = HERE / "enrichment" / "dossiers"
EXPORTS = HERE / "exports"
BINDINGS_DB = HERE / "bindings.sqlite"
SOURCE_RIGHTS = {"text": "Original wording authored for WAi-HKC; no third-party text reproduced.",
                 "references": "Citations are pointers to locate, not copies; record rights before importing any source text.",
                 "disclosure": "PRIVATE_LOCAL"}
V2_FIELDS = ["summary", "first_principles", "facts", "mechanisms", "logic", "equations", "methods", "applications",
             "falsifiers", "failures", "simulations", "theory.core_concepts", "theory.key_results",
             "application_knowledge.worked_example", "textbook_canon", "textbook_history", "pedagogy.learning_path",
             "lineage", "key_people", "landmark_works", "frontier.open_problems", "history_timeline"]

DDL = """
CREATE TABLE IF NOT EXISTS dk_current(original_id TEXT PRIMARY KEY, dossier_id TEXT NOT NULL, set_id TEXT NOT NULL,
  sha256 TEXT NOT NULL, depth REAL NOT NULL, ingested_utc TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS ix_edges_rel_dst ON edges(relation, dst);
CREATE INDEX IF NOT EXISTS ix_edges_dst ON edges(dst);
"""
DERIVED = """
DROP TABLE IF EXISTS dk_textbook; DROP TABLE IF EXISTS dk_work; DROP TABLE IF EXISTS dk_person;
DROP TABLE IF EXISTS dk_lineage; DROP TABLE IF EXISTS dk_school; DROP TABLE IF EXISTS dk_timeline;
DROP TABLE IF EXISTS dk_concept; DROP TABLE IF EXISTS dk_result; DROP TABLE IF EXISTS dk_path;
DROP TABLE IF EXISTS dk_identifier; DROP TABLE IF EXISTS dk_open_problem; DROP TABLE IF EXISTS dk_textbook_era;
DROP TABLE IF EXISTS dk_link; DROP TABLE IF EXISTS dk_search;
CREATE TABLE dk_textbook(original_id TEXT, ord INT, work_id TEXT, title TEXT, authors TEXT, first_ed_year INT,
  latest_known_ed TEXT, level TEXT, role TEXT, notes TEXT, confidence TEXT, bound_status TEXT, bound_ref TEXT);
CREATE TABLE dk_work(original_id TEXT, ord INT, work_id TEXT, year INT, authors TEXT, title TEXT, venue TEXT,
  kind TEXT, why TEXT, confidence TEXT, bound_status TEXT, bound_ref TEXT);
CREATE TABLE dk_person(original_id TEXT, ord INT, person_id TEXT, name TEXT, life TEXT, era TEXT,
  contribution TEXT, confidence TEXT, bound_status TEXT, bound_ref TEXT);
CREATE TABLE dk_lineage(original_id TEXT, chain_no INT, pos INT, teacher_id TEXT, student_id TEXT, teacher TEXT,
  student TEXT, institution_era TEXT, transmitted TEXT, confidence TEXT, bound_status TEXT);
CREATE TABLE dk_school(original_id TEXT, school_id TEXT, name TEXT, place TEXT, era TEXT, founders TEXT, signature TEXT);
CREATE TABLE dk_timeline(original_id TEXT, ord INT, year TEXT, year_num INT, event TEXT);
CREATE TABLE dk_textbook_era(original_id TEXT, ord INT, era TEXT, shift TEXT);
CREATE TABLE dk_concept(original_id TEXT, term TEXT, definition TEXT);
CREATE TABLE dk_result(original_id TEXT, name TEXT, statement TEXT, by_ TEXT, year TEXT);
CREATE TABLE dk_path(original_id TEXT, ord INT, stage TEXT, topics TEXT, typical_texts TEXT);
CREATE TABLE dk_identifier(original_id TEXT, scheme TEXT, code TEXT);
CREATE TABLE dk_open_problem(original_id TEXT, kind TEXT, text TEXT);
CREATE TABLE dk_link(src TEXT, dst TEXT, relation TEXT);
CREATE VIRTUAL TABLE dk_search USING fts5(original_id UNINDEXED, section UNINDEXED, text, tokenize='unicode61 remove_diacritics 2');
CREATE INDEX ix_dk_tb ON dk_textbook(original_id, level); CREATE INDEX ix_dk_tb_w ON dk_textbook(work_id);
CREATE INDEX ix_dk_work ON dk_work(original_id, year); CREATE INDEX ix_dk_work_w ON dk_work(work_id);
CREATE INDEX ix_dk_person ON dk_person(person_id); CREATE INDEX ix_dk_person_o ON dk_person(original_id);
CREATE INDEX ix_dk_lin_t ON dk_lineage(teacher_id); CREATE INDEX ix_dk_lin_s ON dk_lineage(student_id);
CREATE INDEX ix_dk_tl ON dk_timeline(original_id, year_num); CREATE INDEX ix_dk_id ON dk_identifier(scheme, code);
CREATE INDEX ix_dk_link ON dk_link(src); CREATE INDEX ix_dk_link_d ON dk_link(dst);
"""


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def slug(s, n=60):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:n] or "x"


def person_id(name):
    return "person:" + slug(name)


def work_id(title, authors):
    first = slug((authors or ["anon"])[0].split()[-1] if authors else "anon", 24)
    return "work:" + slug(title, 70) + "--" + first


def lock():
    f = (HERE / "CYCLE.lock").open("a+b")
    for _ in range(180):
        try:
            f.seek(0)
            if sys.platform == "win32":
                import msvcrt
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return f
        except OSError:
            time.sleep(1)
    raise RuntimeError("CYCLE_LOCK_BUSY")


def get(d, path):
    for p in path.split("."):
        d = d.get(p) if isinstance(d, dict) else None
    return d


def depth(d):
    def filled(f):
        v = get(d, f)
        if f == "lineage":
            return bool((v or {}).get("teaching_chains") or (v or {}).get("schools"))
        return bool(v) and (not isinstance(v, list) or len(v) >= 1)
    return round(sum(filled(f) for f in V2_FIELDS) / len(V2_FIELDS), 4)


def year_num(y):
    m = re.search(r"-?\d{1,4}", str(y or ""))
    if not m:
        return None
    v = int(m.group())
    return -v if re.search(r"BCE|BC\b", str(y)) and v > 0 else v


def ensure_entity(c, eid, kind, title, summary, payload, tags, stats):
    if c.execute("SELECT 1 FROM assets WHERE id=?", (eid,)).fetchone():
        return
    rec = k.rec(eid, kind, title[:300], summary[:500] or title[:300], "estate://WAi-HKC/dossiers/v2", tags,
                state="HYPOTHESIS", disclosure="PRIVATE_LOCAL", license_id="WAI_AUTHORED_ORIGINAL", payload=payload)
    stats[k.insert(c, rec)] += 1


def ingest_sets(c, paths, stats):
    vertical_ok = {r[0] for r in c.execute("SELECT id FROM assets WHERE kind='knowledge_vertical'")}
    for path in paths:
        data = json.loads(Path(path).read_text(encoding="utf8"))
        assert data.get("schema") == "wai.hkc.dossier_set/2", "SET_SCHEMA:" + str(path)
        for oid, d in sorted(data["dossiers"].items()):
            cur = "curriculum:vertical:" + oid
            if cur not in vertical_ok:
                stats["SKIPPED_UNKNOWN_VERTICAL"] += 1
                continue
            body = dict(d, schema="wai.hkc.dossier/2", original_id=oid, source_rights=SOURCE_RIGHTS)
            sha = k.digest(body)
            did = f"dossier:vertical:{oid}:v2:{sha[:12]}"
            prev = c.execute("SELECT dossier_id, sha256 FROM dk_current WHERE original_id=?", (oid,)).fetchone()
            if prev and prev[1] == sha:
                stats["UNCHANGED"] += 1
                continue
            dep = depth(d)
            tags = ["dossier", "dkd_v2", oid.lower()] + [t for t in d.get("keywords", [])[:15] if isinstance(t, str)]
            rec = k.rec(did, "vertical_dossier", "Dossier v2: " + d.get("title", oid), d.get("summary", "")[:2000],
                        "file:///" + Path(path).resolve().as_posix().replace(" ", "%20"), tags,
                        state="HYPOTHESIS", disclosure="PRIVATE_LOCAL", license_id="WAI_AUTHORED_ORIGINAL",
                        payload={"set_id": data["set_id"], "sha256": sha, "depth": dep, "authorship": data.get("authorship"),
                                 "authored_utc": data.get("authored_utc"), "review_required": True,
                                 "mastery_claim": False, "dossier": body})
            stats[k.insert(c, rec)] += 1
            for dst in (cur, "estate:vertical:" + oid):
                if c.execute("SELECT 1 FROM assets WHERE id=?", (dst,)).fetchone():
                    c.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)", (did, dst, "enriches", "MODEL_AUTHORED_HYPOTHESIS"))
            if prev:
                c.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)", (did, prev[0], "supersedes", "REVISION"))
            c.execute("INSERT OR REPLACE INTO dk_current VALUES(?,?,?,?,?,?)", (oid, did, data["set_id"], sha, dep, utc()))
            # Entities and typed edges (append-only, deduplicated).
            for t in d.get("textbook_canon", []):
                wid = work_id(t.get("title", ""), t.get("authors"))
                ensure_entity(c, wid, "work_entity", t.get("title", ""), "; ".join(t.get("authors", [])),
                              {"title": t.get("title"), "authors": t.get("authors"), "year": t.get("first_ed_year"),
                               "kind": "book"}, ["work", "textbook"], stats)
                c.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)", (wid, cur, "canonical_text_for", "MODEL_AUTHORED_HYPOTHESIS"))
                for a in t.get("authors", []):
                    pid = person_id(a)
                    ensure_entity(c, pid, "person_entity", a, a, {"name": a}, ["person"], stats)
                    c.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)", (pid, wid, "authored", "MODEL_AUTHORED_HYPOTHESIS"))
            for w in d.get("landmark_works", []):
                wid = work_id(w.get("title", ""), w.get("authors"))
                ensure_entity(c, wid, "work_entity", w.get("title", ""), "; ".join(w.get("authors", [])),
                              {"title": w.get("title"), "authors": w.get("authors"), "year": w.get("year"),
                               "kind": w.get("kind")}, ["work", str(w.get("kind"))], stats)
                c.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)", (wid, cur, "landmark_for", "MODEL_AUTHORED_HYPOTHESIS"))
                for a in w.get("authors", []):
                    pid = person_id(a)
                    ensure_entity(c, pid, "person_entity", a, a, {"name": a}, ["person"], stats)
                    c.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)", (pid, wid, "authored", "MODEL_AUTHORED_HYPOTHESIS"))
            for p in d.get("key_people", []):
                pid = person_id(p.get("name", ""))
                ensure_entity(c, pid, "person_entity", p.get("name", ""), p.get("name", ""), {"name": p.get("name")}, ["person"], stats)
                c.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)", (pid, cur, "key_person_for", "MODEL_AUTHORED_HYPOTHESIS"))
            for ch in d.get("lineage", {}).get("teaching_chains", []):
                names = [n for n in ch.get("chain", []) if isinstance(n, str) and n.strip()]
                for n in names:
                    ensure_entity(c, person_id(n), "person_entity", n, n, {"name": n}, ["person"], stats)
                for a, b in zip(names, names[1:]):
                    c.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)", (person_id(a), person_id(b), "taught", "MODEL_AUTHORED_HYPOTHESIS"))
            for s in d.get("lineage", {}).get("schools", []):
                sid = "school:" + slug(s.get("name", ""))
                ensure_entity(c, sid, "school_entity", s.get("name", ""), s.get("signature", "") or s.get("name", ""),
                              {"name": s.get("name"), "place": s.get("place"), "era": s.get("era")}, ["school"], stats)
                c.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)", (sid, cur, "school_of", "MODEL_AUTHORED_HYPOTHESIS"))
            for p in d.get("prereqs", []):
                src = "curriculum:vertical:" + p
                if src in vertical_ok and p != oid:
                    c.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)", (src, cur, "prerequisite_of", "DOSSIER_V2_MODEL_AUTHORED_HYPOTHESIS"))
            for x in d.get("cross_links", []):
                dst = "curriculum:vertical:" + str(x.get("to"))
                if dst in vertical_ok and x.get("to") != oid:
                    c.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)", (cur, dst, "cross_link:" + slug(x.get("relation", "related"), 24), "MODEL_AUTHORED_HYPOTHESIS"))


def binding_map(c):
    """Best binding per (target_type, target_key) from bindings.sqlite, if present."""
    if not BINDINGS_DB.exists():
        return {}
    try:
        c.execute("ATTACH DATABASE ? AS b", (str(BINDINGS_DB),))  # plain path: this connection is not URI-enabled
    except sqlite3.OperationalError:
        return {}
    try:
        rows = c.execute("""SELECT target_type,target_key,status,provider,match_id FROM b.source_binding
                            ORDER BY CASE status WHEN 'MATCHED' THEN 0 WHEN 'VERIFIED' THEN 0 WHEN 'AMBIGUOUS' THEN 1 ELSE 2 END""").fetchall()
        lin = {(r[0], r[1]): r[2] for r in c.execute("SELECT teacher_key,student_key,status FROM b.lineage_check")}
    except sqlite3.OperationalError:
        rows, lin = [], {}
    m = {}
    for tt, key, st, prov, mid in rows:
        m.setdefault((tt, key), (st, f"{prov}:{mid}" if mid else prov))
    m["__lineage__"] = lin
    return m


def run_script(c, script):
    """Execute DDL statement by statement (executescript would COMMIT the open transaction)."""
    for stmt in script.split(";"):
        if stmt.strip():
            c.execute(stmt)


def rebuild(c, bm):
    run_script(c, DERIVED)
    bm = dict(bm)
    lin = bm.pop("__lineage__", {})
    rows = c.execute("""SELECT d.original_id, a.payload FROM dk_current d JOIN assets a ON a.id=d.dossier_id
                        ORDER BY d.original_id""").fetchall()
    export = []
    for oid, payload in rows:
        d = json.loads(payload)["dossier"]
        S = lambda sec, txt: c.execute("INSERT INTO dk_search VALUES(?,?,?)", (oid, sec, txt)) if txt else None
        S("title", d.get("title", "")); S("summary", d.get("summary", ""))
        S("keywords", " ".join(d.get("keywords", []) + d.get("aliases", [])))
        for f in ("first_principles", "facts", "mechanisms", "logic", "equations", "methods", "applications",
                  "falsifiers", "failures", "simulations", "uncertainty_notes"):
            S(f, "\n".join(d.get(f, []) or []))
        th, ak, pe, li, fr = (d.get(x, {}) or {} for x in ("theory", "application_knowledge", "pedagogy", "lineage", "frontier"))
        for cc in th.get("core_concepts", []):
            c.execute("INSERT INTO dk_concept VALUES(?,?,?)", (oid, cc.get("term"), cc.get("definition")))
            S("concept", f"{cc.get('term')}: {cc.get('definition')}")
        for r in th.get("key_results", []):
            c.execute("INSERT INTO dk_result VALUES(?,?,?,?,?)", (oid, r.get("name"), r.get("statement"), r.get("by"), str(r.get("year", ""))))
            S("result", f"{r.get('name')} ({r.get('by')}, {r.get('year')}): {r.get('statement')}")
        S("theory", "\n".join((th.get("laws_axioms") or []) + (th.get("formalisms") or []) + (th.get("schools_debates") or [])))
        we = ak.get("worked_example") or {}
        S("application", "\n".join((ak.get("domains") or []) + (ak.get("practitioner_workflows") or []) +
                                   (ak.get("tools_software") or []) + (ak.get("standards") or []) +
                                   [" ".join(str(v) for v in we.values()) if isinstance(we, dict) else str(we)]))
        for i, t in enumerate(d.get("textbook_canon", [])):
            wid = work_id(t.get("title", ""), t.get("authors"))
            st, ref = bm.get(("textbook", wid), ("UNBOUND", None))
            c.execute("INSERT INTO dk_textbook VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (oid, i, wid, t.get("title"), "; ".join(t.get("authors", [])), t.get("first_ed_year"),
                       t.get("latest_known_ed"), t.get("level"), t.get("role"), t.get("notes"), t.get("confidence"), st, ref))
            S("textbook", f"{t.get('title')} by {', '.join(t.get('authors', []))} ({t.get('first_ed_year')}; {t.get('level')}): {t.get('role')} {t.get('notes') or ''}")
        for i, e in enumerate(d.get("textbook_history", [])):
            c.execute("INSERT INTO dk_textbook_era VALUES(?,?,?,?)", (oid, i, e.get("era"), e.get("shift")))
            S("textbook_history", f"{e.get('era')}: {e.get('shift')}")
        for i, w in enumerate(d.get("landmark_works", [])):
            wid = work_id(w.get("title", ""), w.get("authors"))
            st, ref = bm.get(("work", wid), ("UNBOUND", None))
            c.execute("INSERT INTO dk_work VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                      (oid, i, wid, w.get("year"), "; ".join(w.get("authors", [])), w.get("title"), w.get("venue"),
                       w.get("kind"), w.get("why"), w.get("confidence"), st, ref))
            S("work", f"{w.get('year')} {', '.join(w.get('authors', []))}: {w.get('title')} ({w.get('venue')}) - {w.get('why')}")
        for i, p in enumerate(d.get("key_people", [])):
            pid = person_id(p.get("name", ""))
            st, ref = bm.get(("person", pid), ("UNBOUND", None))
            c.execute("INSERT INTO dk_person VALUES(?,?,?,?,?,?,?,?,?,?)",
                      (oid, i, pid, p.get("name"), p.get("life"), p.get("era"), p.get("contribution"), p.get("confidence"), st, ref))
            S("person", f"{p.get('name')} ({p.get('life')}): {p.get('contribution')}")
        for n, ch in enumerate(li.get("teaching_chains", [])):
            names = [x for x in ch.get("chain", []) if isinstance(x, str) and x.strip()]
            for pos, (a, b) in enumerate(zip(names, names[1:])):
                st = lin.get((person_id(a), person_id(b)), "UNCHECKED")
                c.execute("INSERT INTO dk_lineage VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                          (oid, n, pos, person_id(a), person_id(b), a, b, ch.get("institution_era"), ch.get("transmitted"),
                           ch.get("confidence"), st))
            S("lineage", " -> ".join(names) + f" [{ch.get('institution_era')}] {ch.get('transmitted') or ''}")
        for s in li.get("schools", []):
            c.execute("INSERT INTO dk_school VALUES(?,?,?,?,?,?,?)", (oid, "school:" + slug(s.get("name", "")), s.get("name"),
                      s.get("place"), s.get("era"), "; ".join(s.get("founders", []) or []), s.get("signature")))
            S("school", f"{s.get('name')} ({s.get('place')}, {s.get('era')}): {s.get('signature')}")
        for i, st in enumerate(pe.get("learning_path", [])):
            c.execute("INSERT INTO dk_path VALUES(?,?,?,?,?)", (oid, i, st.get("stage"), json.dumps(st.get("topics", []), ensure_ascii=False),
                      json.dumps(st.get("typical_texts", []), ensure_ascii=False)))
            S("pedagogy", f"{st.get('stage')}: {', '.join(st.get('topics', []))}")
        S("pedagogy", "\n".join((pe.get("misconceptions") or []) + (pe.get("mastery_signals") or []) + (pe.get("classic_exercises") or [])))
        for i, e in enumerate(d.get("history_timeline", [])):
            c.execute("INSERT INTO dk_timeline VALUES(?,?,?,?,?)", (oid, i, str(e.get("year")), year_num(e.get("year")), e.get("event")))
            S("timeline", f"{e.get('year')}: {e.get('event')}")
        for scheme, codes in (d.get("identifiers") or {}).items():
            for code in (codes if isinstance(codes, list) else [codes]):
                c.execute("INSERT INTO dk_identifier VALUES(?,?,?)", (oid, scheme, str(code)))
        for kind in ("open_problems", "active_directions", "venues"):
            for t in fr.get(kind, []) or []:
                c.execute("INSERT INTO dk_open_problem VALUES(?,?,?)", (oid, kind, t))
            S("frontier_" + kind, "\n".join(fr.get(kind, []) or []))
        for p in d.get("prereqs", []):
            c.execute("INSERT INTO dk_link VALUES(?,?,?)", (p, oid, "prerequisite_of"))
        for x in d.get("cross_links", []):
            c.execute("INSERT INTO dk_link VALUES(?,?,?)", (oid, x.get("to"), x.get("relation")))
        export.append(d | {"original_id": oid})
    return export


def refresh_cards(c):
    """Attach a compact v2 block to each card; coverage = max(v1 coverage, v2 depth)."""
    n = 0
    for oid, did, sha, dep in c.execute("SELECT original_id,dossier_id,sha256,depth FROM dk_current").fetchall():
        r = c.execute("SELECT card,coverage FROM machine_card_cache WHERE original_id=?", (oid,)).fetchone()
        if not r:
            continue
        card = json.loads(r[0])
        q = lambda sql: c.execute(sql, (oid,)).fetchone()[0]
        card["dossier_v2"] = {
            "id": did, "sha256": sha, "depth": dep, "evidence_state": "HYPOTHESIS", "review_required": True,
            "counts": {"textbooks": q("SELECT COUNT(*) FROM dk_textbook WHERE original_id=?"),
                       "works": q("SELECT COUNT(*) FROM dk_work WHERE original_id=?"),
                       "people": q("SELECT COUNT(*) FROM dk_person WHERE original_id=?"),
                       "lineage_links": q("SELECT COUNT(*) FROM dk_lineage WHERE original_id=?"),
                       "timeline": q("SELECT COUNT(*) FROM dk_timeline WHERE original_id=?"),
                       "concepts": q("SELECT COUNT(*) FROM dk_concept WHERE original_id=?")},
            "bound": {"textbooks": q("SELECT COUNT(*) FROM dk_textbook WHERE original_id=? AND bound_status='MATCHED'"),
                      "works": q("SELECT COUNT(*) FROM dk_work WHERE original_id=? AND bound_status='MATCHED'"),
                      "people": q("SELECT COUNT(*) FROM dk_person WHERE original_id=? AND bound_status='MATCHED'"),
                      "lineage_verified": q("SELECT COUNT(*) FROM dk_lineage WHERE original_id=? AND bound_status='VERIFIED'")},
            "top_textbooks": [dict(zip(["title", "authors", "year", "level"], x)) for x in c.execute(
                "SELECT title,authors,first_ed_year,level FROM dk_textbook WHERE original_id=? ORDER BY ord LIMIT 5", (oid,))],
            "ops": [f"dossier_lookup.py dossier {oid}", f"dossier_lookup.py textbooks {oid}", f"dossier_lookup.py path {oid}"]}
        card["coverage"] = max(float(r[1]), dep)
        card["gaps_v2"] = [f for f in V2_FIELDS if not (get(json.loads(c.execute(
            "SELECT payload FROM assets WHERE id=?", (did,)).fetchone()[0])["dossier"], f))]
        text = k.canonical(card)
        c.execute("UPDATE machine_card_cache SET card=?, card_sha256=?, enriched=1, coverage=?, built_utc=? WHERE original_id=?",
                  (text, hashlib.sha256(text.encode()).hexdigest(), card["coverage"], utc(), oid))
        n += 1
    return n


def write_export(export):
    EXPORTS.mkdir(exist_ok=True)
    tmp = EXPORTS / "dossiers_v2.jsonl.tmp"
    with tmp.open("w", encoding="utf8") as f:
        for d in export:
            line = k.canonical(d)
            f.write(json.dumps({"sha256": hashlib.sha256(line.encode()).hexdigest(), "dossier": d}, ensure_ascii=False, sort_keys=True) + "\n")
    tmp.replace(EXPORTS / "dossiers_v2.jsonl")


def run(paths=None, refresh_only=False, locked=False):
    lk = None if locked else lock()
    try:
        c = k.connect(); c.execute("PRAGMA busy_timeout=20000"); k.bootstrap(c); c.executescript(DDL)
        stats = {"ADDED": 0, "EXISTING": 0, "UNCHANGED": 0, "SKIPPED_UNKNOWN_VERTICAL": 0}
        backup = None
        before = c.execute("SELECT COUNT(*) FROM assets").fetchone()[0]
        if not refresh_only:
            paths = paths or sorted(glob.glob(str(DOSSIER_DIR / "*.json")))
            ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            (HERE / "backups").mkdir(exist_ok=True)
            backup = HERE / "backups" / f"knowledge.pre_dossier_v2.{ts}.sqlite"
            b = sqlite3.connect(str(backup)); c.backup(b); b.close()
        bm = binding_map(c)  # ATTACH must happen outside a transaction
        c.execute("BEGIN IMMEDIATE")
        try:
            if not refresh_only:
                ingest_sets(c, paths, stats)
            export = rebuild(c, bm)
            cards = refresh_cards(c)
            c.commit()
        except Exception:
            c.rollback(); raise
        try:
            c.execute("DETACH DATABASE b")
        except sqlite3.OperationalError:
            pass
        write_export(export)
        count = c.execute("SELECT COUNT(*) FROM assets").fetchone()[0]
        fts = c.execute("SELECT COUNT(*) FROM asset_search").fetchone()[0]
        integrity = c.execute("PRAGMA quick_check").fetchone()[0]
        assert count == fts and integrity == "ok", ("INTEGRITY", count, fts, integrity)
        q = lambda s: c.execute(s).fetchone()[0]
        receipt = {"schema": "wai.hkc.dossier_v2_receipt/1", "time_utc": utc(), "mode": "refresh" if refresh_only else "ingest",
                   "sets": [str(p) for p in (paths or [])], "backup": str(backup) if backup else None,
                   "assets_before": before, "assets_after": count, "fts": fts, "db_integrity": integrity, **stats,
                   "dossiers_current": q("SELECT COUNT(*) FROM dk_current"),
                   "mean_depth": q("SELECT ROUND(AVG(depth),4) FROM dk_current"),
                   "textbooks": q("SELECT COUNT(*) FROM dk_textbook"), "works": q("SELECT COUNT(*) FROM dk_work"),
                   "people_mentions": q("SELECT COUNT(*) FROM dk_person"), "lineage_links": q("SELECT COUNT(*) FROM dk_lineage"),
                   "timeline_events": q("SELECT COUNT(*) FROM dk_timeline"), "concepts": q("SELECT COUNT(*) FROM dk_concept"),
                   "entities": dict(c.execute("SELECT kind,COUNT(*) FROM assets WHERE kind IN ('person_entity','work_entity','school_entity') GROUP BY kind")),
                   "bound": {"textbooks": q("SELECT COUNT(*) FROM dk_textbook WHERE bound_status='MATCHED'"),
                             "works": q("SELECT COUNT(*) FROM dk_work WHERE bound_status='MATCHED'"),
                             "people": q("SELECT COUNT(DISTINCT person_id) FROM dk_person WHERE bound_status='MATCHED'"),
                             "lineage_verified": q("SELECT COUNT(*) FROM dk_lineage WHERE bound_status='VERIFIED'")},
                   "cards_refreshed": cards,
                   "what_is_proven": "records stored, hashed, linked, indexed; projections rebuilt from current revisions",
                   "not_proven": ["factual accuracy of model-authored dossiers beyond bound items", "vertical mastery", "native RAi admission"]}
        if not refresh_only:
            (HERE / "DOSSIER_V2_RECEIPT.json").write_text(json.dumps(receipt, indent=2), encoding="utf8")
        c.close()
        return receipt
    finally:
        if lk:
            lk.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    r = run(refresh_only=True) if args[:1] == ["--refresh"] else run([a for a in args] or None)
    print(json.dumps(r, sort_keys=True))
