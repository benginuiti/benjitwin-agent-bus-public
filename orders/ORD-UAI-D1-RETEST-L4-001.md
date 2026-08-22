# ORD-UAI-D1-RETEST-L4-001

**Issued:** 2026-08-22  
**Priority:** P0 UAi L4  
**Primary executor:** Local Claude on BENX570E **testlab only**  
**Grok role:** package + grade receipts (no live host mutation from browser plane)  
**Prior:** L4 POSTFIX NOT_CLEARED | D1 (stale signed anchor granted Ben)

## One-line mission
Apply Grok D1 freshness fix (`0.02-r100c30-fix4-d1`) in **lab tree only**, prove suite ≥44 including `d1_stale_anchor_replay_rejected`, re-run L4 battery D1 → expect UNKNOWN (no Ben from gen-1 after gen-2 floor).

## Ferry (Grok surface)
```text
artifacts/UAi_D1_FRESHNESS_FIX_FERRY_2026-08-22.zip
SHA-256 c15eb2c332e4cec8d167d417c21ea832362c61cdb5427557601cecc206c0d7f8
```
Contains: identity.py, run_all.py, VERSION, L4 matrix, this order family, D1 receipt.

## Hard rules
- Testlab copy only
- No live merge into production UAi state
- No identity rebind (BEN_GATE)
- No host mutation / no stop estate services
- `live_host_touched: false`
- Receipts only under lab `receipts/`

## Steps
1. Unpack/patch ferry into lab UAi (not live state).
2. `python -m tests.run_all` → ≥44 PASS including `d1_stale_anchor_replay_rejected`.
3. L4 D1: gen-1 anchor → gen-2 floor → corrupt identity → only gen-1 anchor → **authority=UNKNOWN**.
4. Optional: spot A3/A5/E2.
5. Lab receipt + return line.

## Return line (exactly one)
```text
UAi L4 POSTFIX — CLEARED (testlab) | D1 fixed | suite N/N | critical_failures 0
```
or
```text
UAi L4 POSTFIX — NOT_CLEARED | <id> | live_host_touched false
```

## Do not
- Auto-clear L4 without D1 PASS
- Write receipts into live `E:\o2a-dev\UAi\receipts\`
- Open Wonder/feature merges
- Rebind live Ben authority
