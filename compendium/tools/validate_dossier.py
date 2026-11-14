"""Validate a DKD v2 dossier set (stdlib only).

usage: python validate_dossier.py <set.json> [registry.json]
Exit 0 when the set passes. Prints the errors, depth warnings and a per-dossier depth score.
"""
import json, sys

LEVELS = {"intro", "undergrad", "grad", "reference", "monograph", "practitioner", "popular", "historical"}
KINDS = {"paper", "book", "report", "standard", "thesis", "lecture_notes", "software", "dataset",
         "artwork", "film", "recording", "patent"}
CONF = {"high", "medium", "low"}
LISTS = ["keywords", "prereqs", "first_principles", "facts", "mechanisms", "logic", "equations", "methods",
         "applications", "falsifiers", "failures", "simulations", "sources_to_bind"]
OBJS = ["theory", "application_knowledge", "pedagogy", "lineage", "frontier"]
ARRS = ["textbook_canon", "textbook_history", "key_people", "landmark_works", "history_timeline"]
TARGET = {"textbook_canon": 5, "textbook_history": 3, "key_people": 5, "landmark_works": 6, "history_timeline": 8}


def depth(d):
    """Simple depth score 0..1 over the 22 v2 fields."""
    th, pe, li, fr = d.get("theory", {}), d.get("pedagogy", {}), d.get("lineage", {}), d.get("frontier", {})
    checks = [len(d.get(k, [])) >= 2 for k in ("first_principles", "facts", "mechanisms", "logic", "equations",
                                                "methods", "applications", "falsifiers", "failures", "simulations")]
    checks += [bool(d.get("summary")),
               len(th.get("core_concepts", [])) >= 6, len(th.get("key_results", [])) >= 3,
               bool(d.get("application_knowledge", {}).get("worked_example")),
               len(d.get("textbook_canon", [])) >= 5, len(d.get("textbook_history", [])) >= 3,
               len(pe.get("learning_path", [])) >= 4,
               len(li.get("teaching_chains", [])) + len(li.get("schools", [])) >= 2,
               len(d.get("key_people", [])) >= 5, len(d.get("landmark_works", [])) >= 6,
               len(fr.get("open_problems", [])) >= 3, len(d.get("history_timeline", [])) >= 8]
    return round(sum(checks) / len(checks), 3)


def validate(s, registry=None):
    err, warn = [], []
    if s.get("schema") != "wai.hkc.dossier_set/2":
        err.append("SET_SCHEMA")
    for k in ("set_id", "family", "authorship", "dossiers"):
        if not s.get(k):
            err.append("SET_MISSING:" + k)
    scores = {}
    for oid, d in (s.get("dossiers") or {}).items():
        p = oid + ":"
        if registry is not None and oid not in registry:
            err.append(p + "UNKNOWN_ID")
        if registry and oid in registry and registry[oid]["title"] != d.get("title"):
            warn.append(p + "TITLE_MISMATCH")
        if not isinstance(d.get("summary"), str) or len(d.get("summary", "")) < 80:
            err.append(p + "SUMMARY")
        for k in LISTS:
            v = d.get(k)
            if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
                err.append(p + "LIST:" + k)
        if not isinstance(d.get("diagram"), str):
            err.append(p + "DIAGRAM")
        for k in OBJS:
            if not isinstance(d.get(k), dict):
                err.append(p + "OBJ:" + k)
        for k in ARRS:
            if not isinstance(d.get(k), list):
                err.append(p + "ARR:" + k)
            elif len(d[k]) < TARGET[k]:
                warn.append(f"{p}THIN:{k}={len(d[k])}")
        for t in d.get("textbook_canon", []):
            if not (t.get("title") and isinstance(t.get("authors"), list) and t.get("authors")):
                err.append(p + "TEXTBOOK_SHAPE:" + str(t.get("title")))
            if t.get("level") not in LEVELS:
                err.append(p + "TEXTBOOK_LEVEL:" + str(t.get("level")))
            if t.get("confidence") not in CONF:
                err.append(p + "TEXTBOOK_CONF:" + str(t.get("title")))
            if not isinstance(t.get("first_ed_year"), int):
                err.append(p + "TEXTBOOK_YEAR:" + str(t.get("title")))
        for w in d.get("landmark_works", []):
            if not (w.get("title") and isinstance(w.get("authors"), list) and isinstance(w.get("year"), int)):
                err.append(p + "WORK_SHAPE:" + str(w.get("title")))
            if w.get("kind") not in KINDS:
                err.append(p + "WORK_KIND:" + str(w.get("kind")))
            if w.get("confidence") not in CONF:
                err.append(p + "WORK_CONF:" + str(w.get("title")))
        for q in d.get("key_people", []):
            if not q.get("name") or q.get("confidence") not in CONF:
                err.append(p + "PERSON:" + str(q.get("name")))
        for ch in d.get("lineage", {}).get("teaching_chains", []):
            if not isinstance(ch.get("chain"), list) or len(ch["chain"]) < 2 or ch.get("confidence") not in CONF:
                err.append(p + "CHAIN")
        for e in d.get("history_timeline", []):
            if not (isinstance(e.get("year"), str) and e.get("event")):
                err.append(p + "TIMELINE")
        for x in d.get("prereqs", []) + [c.get("to") for c in d.get("cross_links", [])]:
            if x == oid:
                err.append(p + "SELF_LINK")
            elif registry is not None and x not in registry:
                warn.append(p + "LINK_OUTSIDE_REGISTRY:" + str(x))
        scores[oid] = depth(d)
    return err, warn, scores


if __name__ == "__main__":
    s = json.load(open(sys.argv[1], encoding="utf8"))
    reg = json.load(open(sys.argv[2], encoding="utf8")) if len(sys.argv) > 2 else None
    e, w, sc = validate(s, reg)
    print(json.dumps({"errors": e[:60], "n_errors": len(e), "warnings": w[:60], "n_warnings": len(w),
                      "dossiers": len(sc), "mean_depth": round(sum(sc.values()) / max(1, len(sc)), 3),
                      "depth": sc}, indent=1))
    sys.exit(1 if e else 0)
