"""WAi-HKC dossier lookup: fast, read-only machine queries over Deep Knowledge Dossiers v2. JSON out.

  stats                          dossier corpus counts and binding progress
  dossier <ID> [--section S]     full current dossier (or one top-level section)
  textbooks <ID|terms>           textbook canon, by vertical id or full-text over titles/authors
  history <ID>                   textbook-history eras plus the dated field timeline
  path <ID>                      ordered learning path: transitive prerequisites (topological), then this dossier's stages
  lineage <name> [--depth N]     teacher/student graph around a person (dossier chains + Wikidata advisor links if bound)
  person <name>                  every vertical a person appears in, with their role there
  works <ID|terms>               landmark works
  frontier [<ID>|<FAMILY>]       open problems, active directions and venues
  search "<terms>" [--section S] FTS5 over all dossier text; sections include textbook, lineage, result, concept, timeline
  concept "<term>"               definitions of a term across all fields
  gaps [<FAMILY>]                thinnest dossiers first (harvest targets)
  bench                          local latency benchmark
Every row carries confidence and bound_status, so consumers can separate authored hypotheses from source-bound items.
"""
import argparse, json, re, sqlite3, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / "knowledge.sqlite"
BINDINGS_DB = ROOT / "bindings.sqlite"


def ro():
    c = sqlite3.connect("file:" + DB.as_posix() + "?mode=ro", uri=True)
    c.execute("PRAGMA query_only=ON")
    if BINDINGS_DB.exists():
        try:
            c.execute("ATTACH DATABASE ? AS b", ("file:" + BINDINGS_DB.as_posix() + "?mode=ro",))
        except sqlite3.OperationalError:
            pass
    return c


def rows(c, sql, args=()):
    cur = c.execute(sql, args)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def is_id(v):
    return bool(re.match(r"^[A-Z]{2,4}(-[A-Z0-9_]+)+$", v or ""))


def fts_q(text):
    terms = re.findall(r"\w+", text, re.UNICODE)[:16]
    if not terms:
        raise SystemExit("NO_TERMS")
    return " ".join('"' + t + '"' for t in terms)


def has_b(c):
    return bool(c.execute("SELECT 1 FROM pragma_database_list WHERE name='b'").fetchone())


def stats(c):
    q = lambda s: c.execute(s).fetchone()[0]
    out = {"dossiers": q("SELECT COUNT(*) FROM dk_current"), "mean_depth": q("SELECT ROUND(AVG(depth),4) FROM dk_current"),
           "by_family": rows(c, """SELECT m.family, COUNT(*) n, ROUND(AVG(d.depth),3) depth FROM dk_current d
                                  JOIN machine_card_cache m USING(original_id) GROUP BY m.family ORDER BY m.family"""),
           "textbooks": q("SELECT COUNT(*) FROM dk_textbook"), "distinct_textbooks": q("SELECT COUNT(DISTINCT work_id) FROM dk_textbook"),
           "works": q("SELECT COUNT(*) FROM dk_work"), "people": q("SELECT COUNT(DISTINCT person_id) FROM dk_person"),
           "lineage_links": q("SELECT COUNT(*) FROM dk_lineage"), "timeline_events": q("SELECT COUNT(*) FROM dk_timeline"),
           "concepts": q("SELECT COUNT(*) FROM dk_concept"), "open_problems": q("SELECT COUNT(*) FROM dk_open_problem WHERE kind='open_problems'"),
           "bound": {"textbooks": q("SELECT COUNT(*) FROM dk_textbook WHERE bound_status='MATCHED'"),
                     "works": q("SELECT COUNT(*) FROM dk_work WHERE bound_status='MATCHED'"),
                     "people": q("SELECT COUNT(DISTINCT person_id) FROM dk_person WHERE bound_status='MATCHED'"),
                     "lineage_verified": q("SELECT COUNT(*) FROM dk_lineage WHERE bound_status='VERIFIED'")},
           "vertical_total": q("SELECT COUNT(*) FROM machine_card_cache")}
    if has_b(c):
        out["binder"] = {"requests": q("SELECT COUNT(*) FROM b.http_cache"),
                         "bindings": dict(c.execute("SELECT status,COUNT(*) FROM b.source_binding GROUP BY status")),
                         "wikidata_advisor_edges": q("SELECT COUNT(*) FROM b.genealogy")}
    return out


def dossier(c, oid, section=None):
    r = c.execute("SELECT a.payload FROM dk_current d JOIN assets a ON a.id=d.dossier_id WHERE d.original_id=?", (oid,)).fetchone()
    if not r:
        return {"state": "NOT_FOUND", "original_id": oid}
    p = json.loads(r[0])
    d = p["dossier"]
    meta = {"original_id": oid, "set_id": p["set_id"], "sha256": p["sha256"], "depth": p["depth"], "evidence_state": "HYPOTHESIS"}
    return meta | ({section: d.get(section)} if section else {"dossier": d})


def textbooks(c, v):
    if is_id(v):
        return rows(c, "SELECT * FROM dk_textbook WHERE original_id=? ORDER BY ord", (v,))
    return rows(c, """SELECT t.* FROM dk_search s JOIN dk_textbook t ON t.original_id=s.original_id
                      WHERE dk_search MATCH ? AND s.section='textbook' AND (t.title LIKE ? OR t.authors LIKE ?)
                      GROUP BY t.work_id, t.original_id LIMIT 60""", (fts_q(v), f"%{v.split()[0]}%", f"%{v.split()[-1]}%"))


def history(c, oid):
    eds = []
    if has_b(c):
        eds = rows(c, """SELECT t.title textbook, t.first_ed_year authored_first_ed, e.year, e.publish_date, e.edition_name, e.publishers
                         FROM dk_textbook t JOIN b.source_binding sb ON sb.target_type='textbook' AND sb.target_key=t.work_id
                         JOIN b.textbook_editions e ON e.work_key=sb.match_id WHERE t.original_id=? ORDER BY t.ord, e.year""", (oid,))
    return {"sourced_editions": eds,"textbook_eras": rows(c, "SELECT ord,era,shift FROM dk_textbook_era WHERE original_id=? ORDER BY ord", (oid,)),
            "timeline": rows(c, "SELECT year,year_num,event FROM dk_timeline WHERE original_id=? ORDER BY COALESCE(year_num,99999),ord", (oid,)),
            "textbooks_by_year": rows(c, "SELECT first_ed_year,title,authors,level FROM dk_textbook WHERE original_id=? ORDER BY first_ed_year", (oid,))}


def path(c, oid, limit=60):
    # Transitive prerequisites from one edge scan, then Kahn's topological sort (ties by id); O(V+E).
    allpre = {}
    for src, dst in c.execute("SELECT src, dst FROM edges WHERE relation='prerequisite_of' AND src LIKE 'curriculum:vertical:%'"):
        allpre.setdefault(dst.rsplit(":", 1)[1], set()).add(src.rsplit(":", 1)[1])
    seen, frontier = {oid}, [oid]
    while frontier and len(seen) < limit:
        nxt = []
        for x in frontier:
            for p in allpre.get(x, ()):
                if p not in seen:
                    seen.add(p); nxt.append(p)
        frontier = nxt
    pre = {n: allpre.get(n, set()) & seen for n in seen}
    kids = {}
    for n, ps in pre.items():
        for p in ps:
            kids.setdefault(p, []).append(n)
    indeg = {n: len(ps) for n, ps in pre.items()}
    import heapq
    ready = [n for n in seen if indeg[n] == 0]; heapq.heapify(ready)
    order = []
    while ready:
        n = heapq.heappop(ready); order.append(n)
        for m in kids.get(n, ()):
            indeg[m] -= 1
            if indeg[m] == 0:
                heapq.heappush(ready, m)
    order += sorted(n for n in seen if n not in set(order))  # cycles, if any, appended rather than dropped
    ph = ",".join("?" * len(order))
    titles = dict(c.execute(f"SELECT original_id,title FROM machine_card_cache WHERE original_id IN ({ph})", order))
    has = {r[0] for r in c.execute(f"SELECT original_id FROM dk_current WHERE original_id IN ({ph})", order)}
    return {"target": oid, "prerequisite_order": [{"id": n, "title": titles.get(n), "has_dossier": n in has} for n in order],
            "stages": rows(c, "SELECT ord,stage,topics,typical_texts FROM dk_path WHERE original_id=? ORDER BY ord", (oid,))}


def lineage(c, name, depth=3):
    seed = "person:" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    cand = [r[0] for r in c.execute("SELECT DISTINCT person_id FROM dk_person WHERE name LIKE ? UNION "
                                    "SELECT DISTINCT teacher_id FROM dk_lineage WHERE teacher LIKE ? UNION "
                                    "SELECT DISTINCT student_id FROM dk_lineage WHERE student LIKE ?",
                                    (f"%{name}%",) * 3)]
    seeds = [seed] if seed in cand or not cand else cand[:5]
    edges, seen, frontier = [], set(seeds), list(seeds)
    for _ in range(max(1, min(depth, 6))):
        nxt = []
        for pid in frontier:
            for r in rows(c, """SELECT teacher_id,student_id,teacher,student,institution_era,confidence,bound_status,original_id
                                FROM dk_lineage WHERE teacher_id=? OR student_id=?""", (pid, pid)):
                edges.append(r | {"source": "dossier"})
                for x in (r["teacher_id"], r["student_id"]):
                    if x not in seen:
                        seen.add(x); nxt.append(x)
            if has_b(c):
                for r in rows(c, """SELECT g.advisor_qid,g.student_qid,g.advisor_label,g.student_label,g.property
                                    FROM b.genealogy g JOIN b.person_qid p ON (p.qid=g.advisor_qid OR p.qid=g.student_qid)
                                    WHERE p.person_key=?""", (pid,)):
                    edges.append(r | {"source": "wikidata", "bound_status": "SOURCE_CATALOGUED"})
        frontier = nxt
    uniq = {json.dumps(e, sort_keys=True) for e in edges}
    return {"seeds": seeds, "edges": [json.loads(u) for u in sorted(uniq)][:400]}


def person(c, name):
    return rows(c, """SELECT p.original_id, m.title vertical, p.name, p.life, p.contribution, p.confidence, p.bound_status, p.bound_ref
                      FROM dk_person p JOIN machine_card_cache m USING(original_id) WHERE p.name LIKE ? ORDER BY p.original_id LIMIT 100""",
                (f"%{name}%",))


def works(c, v):
    if is_id(v):
        return rows(c, "SELECT * FROM dk_work WHERE original_id=? ORDER BY year", (v,))
    return rows(c, """SELECT w.* FROM dk_search s JOIN dk_work w ON w.original_id=s.original_id
                      WHERE dk_search MATCH ? AND s.section='work' GROUP BY w.work_id ORDER BY w.year LIMIT 60""", (fts_q(v),))


def frontier(c, v=None):
    sql = "SELECT f.original_id, m.title, f.kind, f.text FROM dk_open_problem f JOIN machine_card_cache m USING(original_id)"
    if v and is_id(v):
        return rows(c, sql + " WHERE f.original_id=?", (v,))
    if v:
        return rows(c, sql + " WHERE m.family=? ORDER BY f.original_id", (v.upper(),))
    return rows(c, sql + " WHERE f.kind='open_problems' ORDER BY f.original_id LIMIT 400")


def search(c, text, section=None, limit=30):
    sql = """SELECT s.original_id, m.title, s.section, snippet(dk_search, 2, '[', ']', ' ... ', 18) snippet,
                    bm25(dk_search) score FROM dk_search s JOIN machine_card_cache m USING(original_id) WHERE dk_search MATCH ?"""
    args = [fts_q(text)]
    if section:
        sql += " AND s.section=?"; args.append(section)
    sql += " ORDER BY score LIMIT ?"; args.append(limit)
    return rows(c, sql, args)


def concept(c, term):
    return rows(c, """SELECT k.original_id, m.title field, k.term, k.definition FROM dk_concept k JOIN machine_card_cache m USING(original_id)
                      WHERE k.term LIKE ? ORDER BY length(k.term), k.original_id LIMIT 50""", (f"%{term}%",))


def gaps(c, fam=None):
    sql = """SELECT m.original_id, m.title, m.family, COALESCE(d.depth,0) depth, d.original_id IS NOT NULL has_dossier
             FROM machine_card_cache m LEFT JOIN dk_current d USING(original_id)"""
    args = ()
    if fam:
        sql += " WHERE m.family=?"; args = (fam.upper(),)
    return rows(c, sql + " ORDER BY depth, m.original_id LIMIT 800", args)


def bench(c):
    some = [r[0] for r in c.execute("SELECT original_id FROM dk_current LIMIT 20")] or ["MAX-SWL-01"]
    res = {}
    for name, fn, n in [("dossier_ms", lambda i: dossier(c, some[i % len(some)]), 500),
                        ("textbooks_ms", lambda i: textbooks(c, some[i % len(some)]), 500),
                        ("search_ms", lambda i: search(c, ("theorem", "textbook history", "advisor student", "open problem")[i % 4]), 200),
                        ("path_ms", lambda i: path(c, some[i % len(some)]), 100),
                        ("lineage_ms", lambda i: lineage(c, ("Hilbert", "Klein", "Hinton", "Prandtl")[i % 4]), 100)]:
        t = time.perf_counter()
        for i in range(n):
            fn(i)
        res[name] = round((time.perf_counter() - t) * 1000 / n, 4)
    res["scope"] = "LOCAL_SINGLE_PROCESS_NOT_NETWORK_BENCHMARK"
    return res


OPS = ["stats", "dossier", "textbooks", "history", "path", "lineage", "person", "works", "frontier", "search", "concept", "gaps", "bench"]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("op", choices=OPS)
    p.add_argument("value", nargs="?")
    p.add_argument("--section")
    p.add_argument("--depth", type=int, default=3)
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--jsonl", action="store_true")
    a = p.parse_args(argv)
    if a.value and len(a.value) > 300:
        raise SystemExit("VALUE_TOO_LONG")
    need = {"dossier", "textbooks", "history", "path", "lineage", "person", "works", "search", "concept"}
    if a.op in need and not a.value:
        raise SystemExit(a.op.upper() + "_NEEDS_VALUE")
    v = a.value.upper() if a.value and is_id(a.value.upper()) and a.op not in ("search", "concept", "person", "lineage") else a.value
    t0 = time.perf_counter()
    c = ro()
    try:
        fn = {"stats": lambda: stats(c), "dossier": lambda: dossier(c, v, a.section), "textbooks": lambda: textbooks(c, v),
              "history": lambda: history(c, v), "path": lambda: path(c, v), "lineage": lambda: lineage(c, v, a.depth),
              "person": lambda: person(c, v), "works": lambda: works(c, v), "frontier": lambda: frontier(c, v),
              "search": lambda: search(c, v, a.section, max(1, min(a.limit, 200))), "concept": lambda: concept(c, v),
              "gaps": lambda: gaps(c, v), "bench": lambda: bench(c)}[a.op]
        result = fn()
    finally:
        c.close()
    if a.jsonl and isinstance(result, list):
        for r in result:
            print(json.dumps(r, ensure_ascii=False))
        return 0
    print(json.dumps({"op": a.op, "elapsed_ms": round((time.perf_counter() - t0) * 1000, 3), "result": result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
