# NEXT — Benjitwin

**Updated:** 2026-08-16T09:20Z  
**Priority:** P0  
**From:** Ben order “fix everything you can” via Browser Grok team  
**Target:** Local Claude on BenX570E (live UAi host)

## Active technical order

**ORD-UAI-FIX1-ATOMIC-WRITES-001**  
**File:** `orders/ORD-UAI-FIX1-ATOMIC-WRITES-001.md`

```text
Apply FIX-1 atomic JSON write helper across all 34 sites.
Pattern: temp → fsync → os.replace. Never in-place.
Then: static assertion of zero non-atomic writes
     + three consecutive Kill-mid-write ×50 (must all be 0 F-DURABLE).
Do not touch authority / FIX-4 residuals.
Leave PID 32416 running if possible; if restarted, record new PID and confirm /capabilities 200.
```

Authority constraint remains locked: only Ben has Ben authority. Ever.

Architecture LOCKED. No secrets on bus.

**Sign:** Ben order “fix everything you can” + Browser Grok team
