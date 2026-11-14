"""Bounded source binder for DKD v2 dossiers (stdlib only, keyless public APIs, CC0 metadata).

Binds authored dossier items to real catalog records; it never edits authored text.
  textbooks  -> Open Library search (CC0 catalog metadata): first_publish_year, edition_count, work key
  works      -> OpenAlex (CC0): id, DOI, publication_year, cited_by_count; books fall back to Open Library
  people     -> Wikidata (CC0): QID, birth/death, doctoral advisor (P184), doctoral student (P185),
                student of (P1066), student (P802)
  lineage    -> a dossier teacher->student link is VERIFIED when Wikidata records it in either direction
  genealogy  -> advisor/student edges around bound people, expanded breadth-first within the budget.
                This is the sourced academic family tree ("who taught the people who wrote the papers").

Bounds: --max-requests per run (default 40), at most 1 request per --interval seconds (default 1.1), responses cached
in harvest_cache/ and never refetched within 30 days, 429/5xx back off, and a run stops at its budget.
Writes only bindings.sqlite and harvest_cache/. Reads knowledge.sqlite read-only.

usage: python bind_sources.py [--max-requests N] [--only textbooks|works|people|lineage|genealogy] [--status]
"""
import argparse, datetime, difflib, hashlib, json, re, sqlite3, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KDB = ROOT / "knowledge.sqlite"
BDB = ROOT / "bindings.sqlite"
CACHE = ROOT / "harvest_cache"
UA = "WAi-HKC-binder/0.2 (bounded local research cache; low rate)"
TTL_DAYS = 30
LICENSE = {"openlibrary": "Open Library catalog metadata (CC0)", "openalex": "OpenAlex (CC0)", "wikidata": "Wikidata (CC0)"}
LINEAGE_PROPS = {"P184": ("student", "advisor"), "P185": ("advisor", "student"), "P1066": ("student", "advisor"), "P802": ("advisor", "student")}

DDL = """
CREATE TABLE IF NOT EXISTS http_cache(url_sha TEXT PRIMARY KEY, url TEXT, provider TEXT, http_status INT, fetched_utc TEXT, body_sha TEXT, path TEXT);
CREATE TABLE IF NOT EXISTS source_binding(target_type TEXT, target_key TEXT, provider TEXT, query TEXT, status TEXT,
  match_id TEXT, match_label TEXT, match_year INT, score REAL, detail TEXT, license TEXT, checked_utc TEXT,
  PRIMARY KEY(target_type, target_key, provider));
CREATE TABLE IF NOT EXISTS person_qid(person_key TEXT PRIMARY KEY, name TEXT, qid TEXT, label TEXT, description TEXT,
  birth INT, death INT, status TEXT, checked_utc TEXT);
CREATE INDEX IF NOT EXISTS ix_pq_qid ON person_qid(qid);
CREATE TABLE IF NOT EXISTS entity_claims(qid TEXT PRIMARY KEY, label TEXT, description TEXT, birth INT, death INT,
  is_human INT, claims TEXT, fetched_utc TEXT);
CREATE TABLE IF NOT EXISTS genealogy(advisor_qid TEXT, student_qid TEXT, advisor_label TEXT, student_label TEXT, property TEXT,
  PRIMARY KEY(advisor_qid, student_qid, property));
CREATE INDEX IF NOT EXISTS ix_gen_s ON genealogy(student_qid);
CREATE TABLE IF NOT EXISTS lineage_check(teacher_key TEXT, student_key TEXT, status TEXT, detail TEXT, checked_utc TEXT,
  PRIMARY KEY(teacher_key, student_key));
CREATE TABLE IF NOT EXISTS textbook_editions(work_key TEXT, edition_key TEXT, title TEXT, publish_date TEXT, year INT,
  publishers TEXT, edition_name TEXT, isbn TEXT, PRIMARY KEY(work_key, edition_key));
CREATE TABLE IF NOT EXISTS editions_done(work_key TEXT PRIMARY KEY, n INT, fetched_utc TEXT);
CREATE TABLE IF NOT EXISTS expand_queue(qid TEXT PRIMARY KEY, depth INT, done INT DEFAULT 0);
CREATE TABLE IF NOT EXISTS binder_runs(seq INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT, receipt TEXT);
"""


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\(.*?\)|[:;].*$", " ", s) if len(s) > 40 else s  # long titles: compare main title
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def sim(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def surname(n):
    parts = re.sub(r"[^\w\s-]", " ", unicodedata.normalize("NFKD", n or "").encode("ascii", "ignore").decode()).split()
    return parts[-1].lower() if parts else ""


def years(text):
    return [int(y) for y in re.findall(r"(?<!\d)(\d{3,4})(?!\d)", str(text or ""))]


class Budget(Exception):
    pass


class Http:
    def __init__(self, b, max_requests, interval):
        self.b, self.left, self.interval, self.last, self.made, self.cached = b, max_requests, interval, 0.0, 0, 0

    def get(self, provider, url):
        key = hashlib.sha256(url.encode()).hexdigest()
        r = self.b.execute("SELECT http_status,fetched_utc,path FROM http_cache WHERE url_sha=?", (key,)).fetchone()
        if r and r[2] and Path(r[2]).exists():
            age = datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(r[1])
            if age.days < TTL_DAYS and r[0] == 200:
                self.cached += 1
                return json.loads(Path(r[2]).read_text(encoding="utf8"))
        if self.left <= 0:
            raise Budget()
        wait = self.interval - (time.monotonic() - self.last)
        if wait > 0:
            time.sleep(wait)
        self.left -= 1; self.made += 1; self.last = time.monotonic()
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        status, body = 0, None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    status, body = resp.status, resp.read()
                break
            except urllib.error.HTTPError as e:
                status = e.code
                if e.code in (429, 500, 502, 503, 504) and attempt < 2:
                    time.sleep(5 * (attempt + 1)); continue
                break
            except (urllib.error.URLError, TimeoutError, OSError):
                status = -1
                if attempt < 2:
                    time.sleep(3); continue
        path = None
        if body is not None and status == 200:
            d = CACHE / provider
            d.mkdir(parents=True, exist_ok=True)
            path = d / (key + ".json")
            path.write_bytes(body)
        self.b.execute("INSERT OR REPLACE INTO http_cache VALUES(?,?,?,?,?,?,?)",
                       (key, url, provider, status, utc(), hashlib.sha256(body or b"").hexdigest(), str(path) if path else None))
        self.b.commit()
        if status != 200:
            return None
        return json.loads(body)


def bind(b, ttype, tkey, provider, query, status, mid=None, label=None, year=None, score=None, detail=None):
    b.execute("INSERT OR REPLACE INTO source_binding VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (ttype, tkey, provider, query, status, mid, label, year, score,
               json.dumps(detail or {}, ensure_ascii=False), LICENSE.get(provider), utc()))
    b.commit()


def openlibrary(http, title, authors, want_year):
    q = {"title": title, "limit": "5", "fields": "key,title,author_name,first_publish_year,edition_count"}
    if authors:
        q["author"] = surname(authors[0])
    data = http.get("openlibrary", "https://openlibrary.org/search.json?" + urllib.parse.urlencode(q))
    if data is None:
        return "ERROR", None
    best = None
    for doc in data.get("docs", []):
        s = sim(title, doc.get("title", ""))
        au = {surname(a) for a in doc.get("author_name", []) or []}
        if authors and not ({surname(a) for a in authors} & au):
            s -= 0.25
        if not best or s > best[0]:
            best = (s, doc)
    if not best or best[0] < 0.8:
        return "NOT_FOUND", None
    doc = best[1]
    fy = doc.get("first_publish_year")
    # A catalog whose earliest edition is LATER than the authored first edition is a catalog gap, not a conflict.
    st = "MATCHED" if (not want_year or not fy or int(fy) >= int(want_year) - 3) else "YEAR_CONFLICT"
    return st, {"id": doc.get("key"), "label": doc.get("title"), "year": fy, "score": round(best[0], 3),
                "detail": {"authors": doc.get("author_name"), "edition_count": doc.get("edition_count"), "authored_year": want_year}}


def openalex(http, title, authors, want_year):
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"search": title[:200], "per-page": "5", "select": "id,doi,display_name,publication_year,cited_by_count,authorships,type"})
    data = http.get("openalex", url)
    if data is None:
        return "ERROR", None
    best = None
    for w in data.get("results", []):
        s = sim(title, w.get("display_name", ""))
        names = {surname(a.get("author", {}).get("display_name", "")) for a in w.get("authorships", []) or []}
        if authors and names and not ({surname(a) for a in authors} & names):
            s -= 0.25
        if want_year and w.get("publication_year") and abs(w["publication_year"] - int(want_year)) > 3:
            s -= 0.1
        if not best or s > best[0]:
            best = (s, w)
    if not best or best[0] < 0.82:
        return "NOT_FOUND", None
    w = best[1]
    yr = w.get("publication_year")
    st = "MATCHED" if (not want_year or not yr or yr >= int(want_year) - 3) else "YEAR_CONFLICT"
    return st, {"id": w.get("id"), "label": w.get("display_name"), "year": yr, "score": round(best[0], 3),
                "detail": {"doi": w.get("doi"), "cited_by_count": w.get("cited_by_count"), "type": w.get("type"), "authored_year": want_year}}


def claim_ids(claims, prop):
    out = []
    for s in claims.get(prop, []) or []:
        v = s.get("mainsnak", {}).get("datavalue", {}).get("value")
        if isinstance(v, dict) and v.get("id"):
            out.append(v["id"])
    return out


def claim_year(claims, prop):
    for s in claims.get(prop, []) or []:
        t = s.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("time")
        if t:
            m = re.match(r"([+-]\d+)-", t)
            if m:
                return int(m.group(1))
    return None


def fetch_entities(http, b, qids):
    qids = [q for q in dict.fromkeys(qids) if q and not b.execute("SELECT 1 FROM entity_claims WHERE qid=?", (q,)).fetchone()]
    for i in range(0, len(qids), 40):
        chunk = qids[i:i + 40]
        data = http.get("wikidata", "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
            {"action": "wbgetentities", "ids": "|".join(chunk), "props": "labels|descriptions|claims",
             "languages": "en", "format": "json"}))
        if not data:
            continue
        for q, e in (data.get("entities") or {}).items():
            cl = e.get("claims", {}) or {}
            keep = {p: claim_ids(cl, p) for p in ("P31", "P106", *LINEAGE_PROPS)}
            b.execute("INSERT OR REPLACE INTO entity_claims VALUES(?,?,?,?,?,?,?,?)",
                      (q, e.get("labels", {}).get("en", {}).get("value"), e.get("descriptions", {}).get("en", {}).get("value"),
                       claim_year(cl, "P569"), claim_year(cl, "P570"), int("Q5" in keep["P31"]),
                       json.dumps(keep), utc()))
        b.commit()


def record_genealogy(b, qid, ancestors_only=False):
    r = b.execute("SELECT claims,label FROM entity_claims WHERE qid=?", (qid,)).fetchone()
    if not r:
        return []
    claims, label = json.loads(r[0]), r[1]
    related = []
    for prop, (me, other) in LINEAGE_PROPS.items():
        for o in claims.get(prop, []):
            adv, stu = (o, qid) if me == "student" else (qid, o)
            b.execute("INSERT OR IGNORE INTO genealogy VALUES(?,?,?,?,?)", (adv, stu, None, None, prop))
            if not (ancestors_only and adv != o):  # beyond depth 1 climb only toward advisors
                related.append(o)
    b.commit()
    return related


def bind_person(http, b, key, name, life):
    data = http.get("wikidata", "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "wbsearchentities", "search": name[:100], "language": "en", "type": "item", "limit": "7", "format": "json"}))
    if data is None:
        return "ERROR"
    cands = [s["id"] for s in data.get("search", [])]
    if not cands:
        b.execute("INSERT OR REPLACE INTO person_qid VALUES(?,?,?,?,?,?,?,?,?)", (key, name, None, None, None, None, None, "NOT_FOUND", utc()))
        bind(b, "person", key, "wikidata", name, "NOT_FOUND"); return "NOT_FOUND"
    fetch_entities(http, b, cands)
    want = years(life)
    scored = []
    for q in cands:
        r = b.execute("SELECT label,description,birth,death,is_human FROM entity_claims WHERE qid=?", (q,)).fetchone()
        if not r or not r[4]:
            continue
        s = sim(name, r[0] or "")
        if want and r[2]:
            s += 0.5 if any(abs(r[2] - y) <= 2 for y in want) else -0.6
        scored.append((s, q, r))
    scored.sort(reverse=True)
    if not scored or scored[0][0] < 0.75:
        st = "NOT_FOUND"
    elif len(scored) > 1 and scored[1][0] >= scored[0][0] - 0.05 and not want:
        st = "AMBIGUOUS"
    else:
        st = "MATCHED"
    if st == "NOT_FOUND":
        b.execute("INSERT OR REPLACE INTO person_qid VALUES(?,?,?,?,?,?,?,?,?)", (key, name, None, None, None, None, None, st, utc()))
        bind(b, "person", key, "wikidata", name, st); return st
    s, q, r = scored[0]
    b.execute("INSERT OR REPLACE INTO person_qid VALUES(?,?,?,?,?,?,?,?,?)", (key, name, q, r[0], r[1], r[2], r[3], st, utc()))
    bind(b, "person", key, "wikidata", name, st, q, r[0], r[2], round(s, 3),
         {"description": r[1], "birth": r[2], "death": r[3], "candidates": [x[1] for x in scored[:4]]})
    if st == "MATCHED":
        for o in record_genealogy(b, q):
            b.execute("INSERT OR IGNORE INTO expand_queue VALUES(?,?,0)", (o, 1))
        b.commit()
    return st


def check_lineage(b, tkey, skey):
    t = b.execute("SELECT qid FROM person_qid WHERE person_key=? AND status='MATCHED'", (tkey,)).fetchone()
    s = b.execute("SELECT qid FROM person_qid WHERE person_key=? AND status='MATCHED'", (skey,)).fetchone()
    if not (t and s):
        return None
    hit = b.execute("SELECT property FROM genealogy WHERE advisor_qid=? AND student_qid=?", (t[0], s[0])).fetchall()
    st = "VERIFIED" if hit else "NOT_IN_WIKIDATA"
    b.execute("INSERT OR REPLACE INTO lineage_check VALUES(?,?,?,?,?)",
              (tkey, skey, st, json.dumps({"teacher_qid": t[0], "student_qid": s[0], "props": [h[0] for h in hit]}), utc()))
    b.commit()
    return st


def label_genealogy(http, b, limit=200):
    missing = [r[0] for r in b.execute("""SELECT q FROM (SELECT advisor_qid q FROM genealogy WHERE advisor_label IS NULL
                                          UNION SELECT student_qid FROM genealogy WHERE student_label IS NULL) LIMIT ?""", (limit,))]
    fetch_entities(http, b, missing)
    b.execute("""UPDATE genealogy SET advisor_label=(SELECT label FROM entity_claims WHERE qid=advisor_qid) WHERE advisor_label IS NULL""")
    b.execute("""UPDATE genealogy SET student_label=(SELECT label FROM entity_claims WHERE qid=student_qid) WHERE student_label IS NULL""")
    b.commit()


def fetch_editions(http, b, work_key):
    """Edition history of a matched Open Library work (dates, publishers, edition names)."""
    data = http.get("openlibrary", f"https://openlibrary.org{work_key}/editions.json?limit=100")
    if data is None:
        return 0
    n = 0
    for e in data.get("entries", []):
        pd = e.get("publish_date") or ""
        ys = years(pd)
        b.execute("INSERT OR IGNORE INTO textbook_editions VALUES(?,?,?,?,?,?,?,?)",
                  (work_key, e.get("key"), e.get("title"), pd, ys[0] if ys else None, "; ".join(e.get("publishers", []) or []),
                   e.get("edition_name"), ((e.get("isbn_13") or []) + (e.get("isbn_10") or []) or [None])[0]))
        n += 1
    b.execute("INSERT OR REPLACE INTO editions_done VALUES(?,?,?)", (work_key, n, utc()))
    b.commit()
    return n


def run(max_requests=40, interval=1.1, only=None, max_depth=5):
    CACHE.mkdir(exist_ok=True)
    b = sqlite3.connect(str(BDB)); b.execute("PRAGMA journal_mode=WAL"); b.executescript(DDL)
    k = sqlite3.connect("file:" + KDB.as_posix() + "?mode=ro", uri=True)
    http = Http(b, max_requests, interval)
    done = {"textbooks": 0, "works": 0, "people": 0, "lineage": 0, "genealogy": 0}
    conf = "CASE confidence WHEN 'high' THEN 0 WHEN 'medium' THEN 1 ELSE 2 END"
    bound = lambda tt, key: b.execute("SELECT 1 FROM source_binding WHERE target_type=? AND target_key=? AND status!='ERROR'", (tt, key)).fetchone()
    try:
        try:
            k.execute("SELECT 1 FROM dk_textbook LIMIT 1")
        except sqlite3.OperationalError:
            return {"outcome": "NO_DOSSIER_TABLES"}
        # Round-robin across target kinds so every kind advances every cycle.
        lanes = []
        if only in (None, "people"):
            lanes.append(("people", iter(k.execute(f"""SELECT person_id, name, life FROM dk_person GROUP BY person_id
                                                     ORDER BY MIN({conf}), person_id""").fetchall())))
        if only in (None, "textbooks"):
            lanes.append(("textbooks", iter(k.execute(f"""SELECT work_id, title, authors, first_ed_year FROM dk_textbook
                                                        GROUP BY work_id ORDER BY MIN({conf}), work_id""").fetchall())))
        if only in (None, "works"):
            lanes.append(("works", iter(k.execute(f"""SELECT work_id, title, authors, year, kind FROM dk_work
                                                    GROUP BY work_id ORDER BY MIN({conf}), work_id""").fetchall())))
        # Budget phases: 60% catalog lanes, 20% edition histories, 20% genealogy expansion (unused budget rolls forward).
        total = http.left
        http.left = int(total * 0.6) or total
        reserve = total - http.left
        active = list(lanes)
        try:
          while active:
            for lane in list(active):
                name, it = lane
                row = None
                for r in it:
                    tt = {"people": "person", "textbooks": "textbook", "works": "work"}[name]
                    if not bound(tt, r[0]):
                        row = r; break
                if row is None:
                    active.remove(lane); continue
                if name == "people":
                    bind_person(http, b, row[0], row[1], row[2])
                elif name == "textbooks":
                    authors = [a.strip() for a in (row[2] or "").split(";") if a.strip()]
                    st, m = openlibrary(http, row[1], authors, row[3])
                    bind(b, "textbook", row[0], "openlibrary", row[1], st, *(m and (m["id"], m["label"], m["year"], m["score"], m["detail"]) or ()))
                else:
                    authors = [a.strip() for a in (row[2] or "").split(";") if a.strip()]
                    if row[4] == "book":
                        st, m = openlibrary(http, row[1], authors, row[3]); prov = "openlibrary"
                    else:
                        st, m = openalex(http, row[1], authors, row[3]); prov = "openalex"
                    bind(b, "work", row[0], prov, row[1], st, *(m and (m["id"], m["label"], m["year"], m["score"], m["detail"]) or ()))
                done[name] += 1
        except Budget:
            pass
        http.left += reserve
        reserve = http.left // 2
        http.left -= reserve
        # Lineage checks are free (local joins) once both people are bound.
        if only in (None, "lineage", "people"):
            for t, s in k.execute("SELECT DISTINCT teacher_id, student_id FROM dk_lineage").fetchall():
                if check_lineage(b, t, s):
                    done["lineage"] += 1
        # Edition histories for matched textbooks (sourced "history of the textbook").
        if only in (None, "textbooks"):
          try:
            for (wk,) in b.execute("""SELECT match_id FROM source_binding WHERE target_type='textbook' AND provider='openlibrary'
                                      AND status IN ('MATCHED','YEAR_CONFLICT') AND match_id NOT IN (SELECT work_key FROM editions_done)
                                      LIMIT 20""").fetchall():
                fetch_editions(http, b, wk)
                done["editions"] = done.get("editions", 0) + 1
          except Budget:
            pass
        http.left += reserve
        # Genealogy expansion: breadth-first over advisor/student QIDs.
        if only in (None, "genealogy"):
            batch = b.execute("SELECT qid, depth FROM expand_queue WHERE done=0 AND depth<=? ORDER BY depth, qid LIMIT 120", (max_depth,)).fetchall()
            fetch_entities(http, b, [q for q, _ in batch])  # 40 entities per request
            for q, d in batch:
                if not b.execute("SELECT 1 FROM entity_claims WHERE qid=?", (q,)).fetchone():
                    continue
                for o in record_genealogy(b, q, ancestors_only=d >= 1):
                    b.execute("INSERT OR IGNORE INTO expand_queue VALUES(?,?,0)", (o, d + 1))
                b.execute("UPDATE expand_queue SET done=1 WHERE qid=?", (q,)); b.commit()
                done["genealogy"] += 1
            label_genealogy(http, b)
        outcome = "PASS"
    except Budget:
        outcome = "BUDGET_REACHED"
    finally:
        k.close()
    receipt = {"schema": "wai.hkc.binder_receipt/1", "at": utc(), "outcome": outcome, "requests_made": http.made,
               "cache_hits": http.cached, "advanced": done,
               "bindings": dict(b.execute("SELECT target_type||':'||status, COUNT(*) FROM source_binding GROUP BY 1")),
               "lineage": dict(b.execute("SELECT status, COUNT(*) FROM lineage_check GROUP BY 1")),
               "genealogy_edges": b.execute("SELECT COUNT(*) FROM genealogy").fetchone()[0],
               "textbook_editions": b.execute("SELECT COUNT(*) FROM textbook_editions").fetchone()[0],
               "network": "keyless public APIs, bounded", "edits_authored_text": False}
    b.execute("INSERT INTO binder_runs(at, receipt) VALUES(?,?)", (receipt["at"], json.dumps(receipt)))
    b.commit(); b.close()
    receipt["new_bindings"] = sum(v for key, v in done.items() if key != "lineage")  # lineage re-checks are local, not progress
    return receipt


def cycle(max_requests=30):
    """Entry point for cycle_runner.py; failures are reported, never raised."""
    try:
        r = run(max_requests=max_requests)
        return {"outcome": r["outcome"] if r["outcome"] != "BUDGET_REACHED" else "PASS", "new": r.get("new_bindings", 0), "receipt": r}
    except Exception as e:
        return {"outcome": "BLOCKED:" + type(e).__name__, "new": 0, "error": str(e)[:200]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--max-requests", type=int, default=40)
    ap.add_argument("--interval", type=float, default=1.1)
    ap.add_argument("--only", choices=["textbooks", "works", "people", "lineage", "genealogy"])
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    if a.status:
        b = sqlite3.connect(str(BDB)); b.executescript(DDL)
        print(json.dumps({"bindings": dict(b.execute("SELECT target_type||':'||status, COUNT(*) FROM source_binding GROUP BY 1")),
                          "lineage": dict(b.execute("SELECT status, COUNT(*) FROM lineage_check GROUP BY 1")),
                          "genealogy_edges": b.execute("SELECT COUNT(*) FROM genealogy").fetchone()[0],
                          "requests_total": b.execute("SELECT COUNT(*) FROM http_cache").fetchone()[0]}, sort_keys=True))
    else:
        print(json.dumps(run(a.max_requests, a.interval, a.only), sort_keys=True))
