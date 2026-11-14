# DKD v2 operations (X550)

Run everything from `D:\WAi-Human-Knowledge-Compendium` with `P:\RAi Root\Runtime\python312\python\python.exe -X utf8`.

| task | command |
|---|---|
| add or revise a family | write parts to `enrichment\dossiers\parts\<CODE>_<n>.json`, then `python enrichment\dossiers\merge_parts.py CODE`, then `python ingest_ready.py CODE` |
| rebuild projections only | `python ingest_dossier_v2.py --refresh` |
| binder progress | `python bind_sources.py --status` |
| manual binder burst | `python bind_sources.py --max-requests 60 [--only people\|textbooks\|works\|genealogy]` |
| corpus stats | `python dossier_lookup.py stats` |
| thinnest dossiers / unfilled verticals | `python dossier_lookup.py gaps [FAMILY]` |
| one dossier / one section | `python dossier_lookup.py dossier MAX-STM-08 [--section textbook_canon]` |
| textbooks, edition history | `python dossier_lookup.py textbooks MAX-STM-08`, `python dossier_lookup.py history MAX-STM-08` |
| who taught whom | `python dossier_lookup.py lineage "Hilbert" --depth 4` |
| learning order | `python dossier_lookup.py path MAX-AIR-10` |
| full-text search | `python dossier_lookup.py search "spectral theorem" [--section result]` |

Revisions are append-only: re-ingesting a changed dossier adds a new `:v2:<sha12>` asset that `supersedes` the old one. An unchanged dossier is a no-op.
Every ingest takes CYCLE.lock and makes an online backup in `backups\`.
The 5-minute cycle runs the binder (60 requests) and refreshes projections when it makes progress.
