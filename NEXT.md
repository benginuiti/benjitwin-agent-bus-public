# NEXT — Nebula / Claude / Quad

**Active order:** `orders/ORD-UAI-D1-RETEST-L4-001.md`  
**Issued:** 2026-08-22  
**Priority:** P0 UAi L4  
**Primary executor:** Local Claude on BENX570E **testlab only**  
**Grok role:** grade receipts only (no live host mutation from browser plane)

## One-line mission
Apply D1 freshness fix ferry (`0.02-r100c30-fix4-d1`), prove suite ≥44 + L4 D1 reject of stale gen-1 anchor after gen-2 floor. Testlab only.

## Ferry pointer
```text
SHA-256 c15eb2c332e4cec8d167d417c21ea832362c61cdb5427557601cecc206c0d7f8
artifacts/UAi_D1_FRESHNESS_FIX_FERRY_2026-08-22.zip  (Grok project surface)
```

## Hard facts
- Prior L4: NOT_CLEARED | D1 (stale signed anchor → Ben)
- F-DURABLE still CLEARED IN TESTLAB (2026-08-17)
- Live host digest was unchanged on prior L4 run

## Parked (not cancelled)
- `orders/ORD-WEB-MANAGER-HOST-BIND-001.md` — resume after UAi L4 D1 clearance unless Ben re-prioritizes

## Do not
- Live merge / identity rebind / host mutation
- Claim L4 CLEARED without D1 PASS receipt
- Claim HOST_VERIFIED from source presence alone

## Return
Lab receipt → Grok grades → board updates.
