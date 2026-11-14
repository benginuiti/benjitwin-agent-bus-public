# WAi Human Knowledge Compendium: DKD v2 tooling (code only)

This folder holds code and schema only. Compendium data (knowledge.sqlite, dossiers, vertical ids/scopes) stays private on the
X550 instance at `D:\WAi-Human-Knowledge-Compendium` and is never pushed here.

| file | role |
|---|---|
| `schema/DKD_V2_SCHEMA.md` | Deep Knowledge Dossier v2: textbook canon and its history, theory, application, pedagogy path, teacher->student lineage, landmark works, frontier, timeline |
| `tools/validate_dossier.py` | shape check plus a 0..1 depth score per dossier |
| `tools/ingest_dossier_v2.py` | append-only revisions, entity resolution (person/work/school), typed edges, normalized `dk_*` tables, `dk_search` FTS5, card refresh, JSONL export |
| `tools/dossier_lookup.py` | read-only machine queries (dossier, textbooks, history, path, lineage, person, works, frontier, search, concept, gaps, bench) at about 1 ms |
| `tools/bind_sources.py` | bounded keyless binder: Open Library (textbooks and edition histories), OpenAlex (papers), Wikidata (people, doctoral-advisor genealogy, lineage verification) |

Evidence contract: authored dossiers are `HYPOTHESIS`. Binding adds `source_binding` rows (CC0 catalog metadata) and never edits authored text.
`mastery_claim` is always false.
