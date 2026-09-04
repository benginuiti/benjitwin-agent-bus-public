# NEXT — Nebula / Claude / Quad

**Active order:** `orders/ORD-UAI-D1-RETEST-L4-001.md`  
**Issued:** 2026-08-22  
**Priority:** P0 UAi L4  
**Primary executor:** Local Claude on BENX570E **testlab only**  
**Grok role:** grade receipts only (no live host mutation from browser plane)

## One-line mission
Apply D1 freshness fix ferry (`0.02-r100c30-fix4-d1`), prove suite ≥44 + `python -m field_proof.L4_BATTERY_D_STANDALONE` 8/8 + L4 D1 reject of stale gen-1 anchor. Testlab only.

## Ferry pointer (refreshed)
```text
SHA-256 1a306e5280b689f563a1dea4d77cc774fcb143bc6ff2c0e32e60788b99a69427
artifacts/UAi_D1_FRESHNESS_FIX_FERRY_2026-08-22.zip  (Grok project surface)
Includes field_proof/L4_BATTERY_D_STANDALONE.py
```

## Grok sandbox already proved (package plane)
- tests.run_all 44/44 PASS
- L4_BATTERY_D_STANDALONE 8/8 PASS
- Does **not** replace X570 testlab clearance

## Hard facts
- Prior L4 on box: NOT_CLEARED | D1
- F-DURABLE CLEARED IN TESTLAB (2026-08-17)

## Galaxy 24/7 status (C191)
- cycle_id: C191
- ben_satisfied: false
- stop_requested: false
- remaining READY owner=Grok: 0
- last bite: residual self-loop + offline keyless measurement (fail-loud no new source) + Q-005 path
- hard stops intact

## Parked (not cancelled)
- `orders/ORD-WEB-MANAGER-HOST-BIND-001.md` — resume after UAi L4 D1 clearance unless Ben re-prioritizes

## Do not
- Live merge / identity rebind / host mutation
- Claim L4 CLEARED without lab D1 PASS receipt

## Return
Lab receipt → Grok grades → board updates.
