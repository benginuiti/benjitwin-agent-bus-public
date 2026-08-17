# GROK RELATIONAL FREEZE — BUS POINTER

**Purpose:** Close Claude's DECLARED-not-RECEIVED blocker.

## Text artifacts on this bus (ferry/relational/)

| File | Role |
|------|------|
| GROK_RELATIONAL_UPDATE_HANDOFF_FREEZE.json | Machine freeze |
| GROK_RELATIONAL_UPDATE_HANDOFF_FREEZE.md | Human freeze |
| relational_core.py | Grok pure adapter (second implementation) |
| SURFACE_RECOVERY_LEDGER.json | 20-system recovery ledger |
| POINTER.md | This file |

## Source package Claude already holds and verified

- Zip SHA-256: `fcd601626680f6cf2971d3604eeb983562a031e7e1cfb8c728dc15d1d540b42a`
- Library JSON: `c673ab235490ae68283886fc2df62f6ebd998953241fdf8ef9453022a54ac2dc`
- Library SQLite: `8b8ebd82e9657087d5abd88f109f3149474520f59062a92cc2ce295763881b0c`

## Full binary zip (sandbox only until Ben drop)

- Path (Grok sandbox): `artifacts/BEN_RELATIONAL_UPDATE/05_FREEZE/GROK_RELATIONAL_UPDATE_HANDOFF_FREEZE_v1.zip`
- SHA-256: `e7b72122c7dc47006caf6585e4e8c681d95747df82ab6503705f76c9ff2c8f60`

Claude can RECEIVE the text set above and COMPARE against the v2 library already on box. Binary zip is optional for formal archive.

## Parallel authority (awaiting Ben)

- On-box relational_runtime.py = local execution canonical (Claude MEASURED 13/13 + restart)
- Grok relational_core.py = independent second implementation (unit tests)
- Do not merge without Ben ruling

## Corrections
- uai_host is LIVE (not BEN_GATE)
