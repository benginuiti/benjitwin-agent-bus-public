# QUAD_FINISHABLE_WORK_v1.0 — Claude delivery

**SHA-256 (exact):** `9ab21fc8d1e40985b850ec505e6111ff8c28b0b712b6c425b0b3753dec59f2f4`
**Size:** 28246 bytes
**Class:** candidate delta only — do not overwrite live ERIE/CA hosts without diff + tests + rollback

## One-liner for Claude / Ben (X570 PowerShell)

```powershell
irm https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/quad/QUAD_FINISHABLE_WORK_v1.0/FETCH_AND_VERIFY.ps1 | iex
```

Or run the script after saving it. It downloads the b64, decodes the zip, verifies SHA-256, expands under:
`E:\o2a-dev\mct_pre_runner\incoming_grok\QUAD_FINISHABLE_WORK_v1.0`

## Contents after expand
- 00_STATUS
- 01_POST_DEPLOY (verify_organs.py / .ps1 + chain)
- 02_CLOCKWORK candidate cycle
- 03_BASELINE_DELTAS
- 04_RESIDUAL_ORDER
- 05_PRODUCTION_FINAL ledger + resurrection checklist
- 06_HOSTS_v0.1.1 (candidate delta only)

## Law
Treat hosts v0.1.1 as **candidate delta**. Currently live v0.1-local remains authoritative until measured improvement + regression + rollback path.
