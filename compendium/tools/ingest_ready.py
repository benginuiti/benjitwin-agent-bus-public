"""Validate named DKD v2 sets and ingest every clean one in a single run (one backup, one transaction).

usage: python ingest_ready.py CODE [CODE ...]     e.g. GMR ARA BLS
Sets with validator errors are reported and skipped, never ingested.
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate_dossier as v  # noqa: E402
import ingest_dossier_v2 as ing  # noqa: E402

D = HERE / "enrichment" / "dossiers"
reg = json.loads((D / "registry.json").read_text(encoding="utf8"))
ok, report = [], {}
for code in sys.argv[1:]:
    p = D / f"DKD_V2_{code}.json"
    if not p.exists():
        report[code] = "MISSING"; continue
    s = json.loads(p.read_text(encoding="utf8"))
    e, w, sc = v.validate(s, reg)
    report[code] = {"dossiers": len(sc), "errors": len(e), "first_errors": e[:5],
                    "mean_depth": round(sum(sc.values()) / max(1, len(sc)), 3)}
    if not e:
        ok.append(str(p))
r = ing.run(ok) if ok else None
print(json.dumps({"validated": report, "ingested": ok,
                  "receipt": {k: r[k] for k in ("ADDED", "UNCHANGED", "assets_after", "fts", "db_integrity", "dossiers_current",
                                                "mean_depth", "textbooks", "works", "lineage_links", "bound")} if r else None}))
