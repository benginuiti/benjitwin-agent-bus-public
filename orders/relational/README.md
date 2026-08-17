# Grok Relational Update Freeze (text artifacts)

**Purpose:** Give Claude actual RECEIVE-able bytes for the ordered baton sequence.

## Files here
- `GROK_RELATIONAL_UPDATE_HANDOFF_FREEZE.json` — machine freeze
- `GROK_RELATIONAL_UPDATE_HANDOFF_FREEZE.md` — human freeze
- `relational_core.py` — portable L01–L15 core (Grok unit-test surface)
- `relational_adapter.py` — alternate portable adapter (30/30 unit tests)
- `SURFACE_RECOVERY_LEDGER.json` — recovery of 20 systems from Grok surface
- `GROK_RELATIONAL_FREEZE_MANIFEST.json` — hashes + status

## Claude sequence
`RECEIVE → READBACK → COMPARE → ACK` against these files + original v2 library already verified.

## Status notes
- **uai_host BEN_GATE CLOSED** (Claude measured LIVE).
- Parallel authority **AWAITING_BEN**: on-box `relational_runtime.py` (13/13 RT+restart MEASURED) vs these Grok unit-test adapters. Do not merge without Ben ruling.
- Full binary zip still Grok-sandbox only until Ben ferries if required.
- Claude PARTIAL stands (UMCEF not on box).

Architecture locked. Evidence law absolute. Only Ben promotes.
