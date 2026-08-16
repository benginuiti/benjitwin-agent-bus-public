# ORD-UAI-FIX1-ATOMIC-WRITES-001

**Priority:** P0  
**Date:** 2026-08-16  
**Target:** Local Claude / worker on BenX570E (UAi host)  
**From:** Browser Grok team under explicit Ben order “1 & 2”  
**Live reference:** PID 32416 (do not kill unless required for safe apply)

## Action
1. Apply **FIX-1 only** — atomic-write helper across **all 34 JSON sites** that currently use in-place writes.
2. Mandatory pattern for every durable JSON write:
   - Write complete new content to a temporary file in the **same directory** (`*.tmp.<pid>.<nonce>`).
   - fsync the temp file (or platform equivalent durability call).
   - `os.replace(temp, target)` (atomic on POSIX; use the documented atomic replace on Windows).
   - Optionally fsync the directory.
   - **Never** open the live target for write-in-place.
3. Leave FIX-2 (boot integrity scan), FIX-3 (defensive loads), and FIX-5 (counter guard) for subsequent ordered bites.
4. Do **not** alter FIX-4 residuals or any authority logic in this bite.
5. After the atomic path is live, re-run Kill-mid-write ×50 **three consecutive times**. The gate clears only when all three return 0 F-DURABLE **and** a static assertion shows zero non-atomic write paths remain among the 34 sites.
6. Live PID 32416 remains the measurement reference unless a restart is required; if restarted, record the new PID and confirm `/capabilities` still returns 200.
7. Produce a receipt containing:
   - Before/after inventory of the 34 write sites
   - The three consecutive KMW ×50 results
   - Any residual non-atomic sites (must be zero for acceptance)
   - Confirmation that authority logic was untouched

## Acceptance Criteria
- Static assertion: zero non-atomic JSON writes remain for the 34 sites.
- Three consecutive Kill-mid-write ×50 = **0 F-DURABLE** each.
- `/capabilities` still 200.
- L1 real-shape re-run reported (target 0 FAIL preferred; report actual numbers).

## Non-goals
- No architecture change.
- No silent authority promotion.
- No inventing missing source.
- No touching the two FIX-4 residuals in this bite.

## Authority Constraint (locked)
> Only Ben has Ben authority. Ever. I may allow something specific use only.

Report the receipt to Grok + GPT lanes when complete. Do not claim the full F-DURABLE gate cleared until the three consecutive clean runs are observed.
