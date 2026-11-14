# Deep Knowledge Dossier v2 (DKD v2): schema

Schema id: `wai.hkc.dossier_set/2` (set) and `wai.hkc.dossier/2` (one vertical).
It replaces the 12-field `vertical_enrichment` v1 as the main per-vertical knowledge object. It keeps every v1 field, so v1 cards stay readable,
and adds the layers a field expert carries: the textbook canon and its history, theory, application practice, the pedagogy path
from first course to research frontier, teacher->student lineage, landmark works and a dated timeline.

## Evidence contract (unchanged from v1)
- Model-authored content is `HYPOTHESIS` until bound to sources and reviewed. `mastery_claim` is always false.
- Every textbook, work, person and lineage link has `confidence` (`high`|`medium`|`low`). The binder (`bind_sources.py`)
  works through `high` first and records `source_binding` rows. It never edits authored text.
- Do not invent citations. Leave out any work you cannot name with real authors and a real approximate year.
- Original wording only. Do not reproduce third-party text.

## Set envelope
```json
{"schema":"wai.hkc.dossier_set/2","set_id":"DKD_V2_STM","family":"SCIENCE AND MATHEMATICS EXPANSION",
 "authored_utc":"2026-11-14","authorship":"MODEL_AUTHORED ...","evidence_state":"HYPOTHESIS",
 "review_required":"...","mastery_claim":false,"dossiers":{"MAX-STM-08":{...}}}
```

## Dossier (keys marked * are required; the rest are strongly expected)
| key | type | meaning |
|---|---|---|
| title* | str | vertical title, exactly as in the registry |
| summary* | str | 3-6 sentence definition at textbook level: what the field studies and why it matters |
| keywords* | [str] | 6-15 search terms, including aliases and abbreviations |
| aliases | [str] | other names, including non-English names where they are standard |
| prereqs* | [id] | Compendium vertical ids learned first (same family or any registry id) |
| identifiers | {scheme:[code]} | classification codes to verify: `msc2020`, `acm_ccs`, `jel`, `pacs`, `lcc`, `ddc`, `mesh`, `cip`, `wikidata_label` |
| first_principles*, facts*, mechanisms*, logic*, equations*, methods*, applications*, falsifiers*, failures*, simulations* | [str] | v1 fields (kept) |
| diagram* | str | one diagram spec in words |
| theory* | obj | `core_concepts:[{term,definition}]`, `laws_axioms:[str]`, `key_results:[{name,statement,by,year}]`, `formalisms:[str]`, `schools_debates:[str]` |
| application_knowledge* | obj | `domains:[str]`, `practitioner_workflows:[str]`, `tools_software:[str]`, `standards:[str]`, `worked_example:{problem,approach,result}` |
| textbook_canon* | [obj] | `{title,authors:[str],first_ed_year:int,latest_known_ed:str,level,role,notes,confidence}`; level is one of `intro`,`undergrad`,`grad`,`reference`,`monograph`,`practitioner`,`popular`,`historical` |
| textbook_history* | [obj] | `{era,shift}`: how the teaching texts changed over time (which book displaced which, and why) |
| pedagogy* | obj | `learning_path:[{stage,topics:[str],typical_texts:[str]}]`, with stages in order from `secondary`/`lower_undergrad`/`upper_undergrad`/`masters`/`phd`/`research`/`practitioner`; also `misconceptions:[str]`, `mastery_signals:[str]`, `classic_exercises:[str]` |
| lineage* | obj | `teaching_chains:[{chain:[name,...],institution_era,transmitted,confidence}]` (teacher first); `schools:[{name,place,era,founders:[str],signature}]` |
| key_people* | [obj] | `{name,life:str,era,contribution,confidence}` |
| landmark_works* | [obj] | `{year:int,authors:[str],title,venue,kind,why,confidence}`; kind is one of `paper`,`book`,`report`,`standard`,`thesis`,`lecture_notes`,`software`,`dataset` |
| frontier* | obj | `open_problems:[str]`, `active_directions:[str]`, `venues:[str]` (journals/conferences where the frontier is published) |
| history_timeline* | [obj] | `{year:str,event}` in chronological order |
| cross_links | [obj] | `{to:id,relation}`; relation is one of `uses`,`applies_to`,`generalizes`,`specializes`,`analogy`,`historical_root`,`tooling_for` |
| uncertainty_notes | [str] | where the field disagrees with itself or the author is unsure |
| sources_to_bind* | [str] | citations to locate (not copies) |

## Depth targets per dossier
5+ textbooks across at least 3 levels, 3+ textbook-history eras, 4+ learning-path stages, 2+ teaching chains (where the field has
an academic genealogy), 5+ key people, 6+ landmark works, 8+ timeline events, 6+ core concepts, 3+ key results, and 3+ open problems.
Practice-led fields (sales, live events, sustainment) replace academic chains with apprenticeship and institutional lineages, such as
schools, firms, guilds, standards bodies and handbooks.

## Machine surfaces built by `ingest_dossier_v2.py`
- `assets` row kind `vertical_dossier` (id `dossier:vertical:<ID>:v2`), FTS-indexed, linked `enriches` -> vertical.
- Entity assets, deduplicated across all dossiers: `person:<slug>`, `work:<slug>` (textbooks and landmark works), `school:<slug>`.
- Edges: `canonical_text_for`, `landmark_for`, `key_person_for`, `taught` (teacher->student, from lineage chains), `authored`,
  `prerequisite_of`, `cross_link:<relation>`, `school_of`.
- Normalized tables (all keyed by `original_id`): `dk_textbook`, `dk_work`, `dk_person`, `dk_lineage`, `dk_timeline`,
  `dk_concept`, `dk_result`, `dk_path`, `dk_identifier`, `dk_open_problem`, plus FTS5 `dk_search` across all dossier text.
- `machine_card_cache` is rebuilt with v2 coverage, scored over 22 fields (v1 had 12).
- Export: `exports/dossiers_v2.jsonl`, one canonical dossier per line with its SHA-256.
