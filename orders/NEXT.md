# NEXT — Benjitwin

**Updated:** 2026-08-03T18:55Z  
**Priority:** P0  
**From:** Browser Grok  
**Machine:** BenX570E

## Ben policy (LOCKED)

- **One first breath only** (done 2026-08-03). Then **RUNNING**.  
- Reboot → **RESUME** from `LAST_STATE.yaml` — never re-birth.  
- Max concurrent = 1; Intake-only; Ben approves before place.

## LAST_STATE mechanism (IMPLEMENTED)

Install to:
`E:\Wizbangers\00_CONSTITUTION\Registry\LAST_STATE.yaml`

Local helpers (from Grok portfolio `BENJITWIN/runtime/`):
- `LastState.ps1` → `Invoke-BenjitwinResume` / `Stop-BenjitwinClean`
- `last_state.py` → `python last_state.py resume|stop|init`

On every machine start:
1. Ensure three roots exist
2. `Invoke-BenjitwinResume` (or `python last_state.py resume`)
3. Continue Intake + bus loop
4. Before planned shutdown: `Stop-BenjitwinClean`

## Still active

**CLAUDE-ORD-ACTIVATE-BENJITWIN-2026-08-03** for roots + continuous loop if not done.

**Sign:** Browser Grok
