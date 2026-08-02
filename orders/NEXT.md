# ORDER — 2026-08-02A  MORNING BOOT

**From:** Browser Grok (BEN-authorized)
**To:** Local Claude (BenX570E)

## P0 — Restore phone + bus (do this first)
Core five already verified UP by Claude. Do not restart them unless a probe fails.

1) **Bus poller** — relaunch the same poller that was pid 44128 (orders/NEXT.md fetch). No token needed. Confirm it is alive.
2) **Relay :49400** — restart with `BENJITWIN_RELAY_TOKEN` from process env only (BEN will paste token). Bind mesh `100.95.127.31:49400` as before. Prove:
   - GET /health 200
   - GET /chat 200
   - GET /mct/ 200
   - GET /status without bearer → 401
3) REPORT_LATEST.md status line: `BOOT_RELAY_POLLER_UP` or `BOOT_WAITING_RELAY_TOKEN` if token not yet provided.

## P1 — After boot green
Resume prior work in this order only:
1. If Greenly verb surface is reachable → continue GREENLY_CYCLE01 per prior contract (isolation, evidence package).
2. Else gather handoff / direct_fetch continuation if Greenly blocked.
3. Provider API bridge remains paused unless BEN reopens it.

## Do not
- Write tokens to disk
- Restart healthy core five for sport
- Ask BEN philosophical questions — execute boot proofs

**Sign:** Browser Grok
