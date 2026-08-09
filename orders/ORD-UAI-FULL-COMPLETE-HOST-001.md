# ORDER — UAi FULL COMPLETE (HOST / EXTERNAL LANES ONLY)

**Order ID:** ORD-UAI-FULL-COMPLETE-HOST-001  
**Priority:** P0 — continuous until executable host work exhausted  
**From:** Browser Grok  
**To:** Local Claude (BenX570E primary; Mac Claude for surface/ATS only)  
**Authority:** Ben (multi-agent mode)  
**Direction chain (MANDATORY):**  
```text
Claude → reports / asks direction → Grok + GPT
Claude → does NOT ask Ben for ordinary engineering
Claude → Ben only if true BEN_GATE (architecture, legal, financial, public, privilege, security boundary expansion)
```
**Mode:** EXECUTE  
**No secrets on public bus**  
**Sign:** Browser Grok  

---

## Why this order exists

Grok ran UAi COMPLETE EVERYTHING on the package side:
- Ledger: UAi/ledger/UAI_COMPLETENESS_LEDGER.json (75 requirements)
- Coverage report + continuous core (NLU, task/anatomy lifecycle, durability)
- Tests ≥27 PASS in package
- Package: UAi_COMPLETENESS_CONTINUOUS_2026-08-09.zip

Grok cannot complete live host, mesh, portal, or external organ lanes from sandbox. **Claude closes those lanes.** Architecture LOCKED. No redesign.

---

## Non-negotiables

1. Canonical UAi mind = BENX570E only. iPhone/Mac/browser = relay surfaces only.
2. No external model inside UAi. Services only across Service Edge.
3. Standalone must PASS with all services disabled.
4. No secrets in git, bus, receipts, or UAi state.
5. Direction: ask **Grok and GPT** (not Ben) for sequencing/ambiguity/repair.
6. BEN_GATE only for architecture change, legal/financial/public, privilege or security boundary expansion.
7. Socket-open is not PASS. Every external bind: request → result → independent readback → compare → receipt.
8. Do not invent live O2A/YEP numbers or fake peer data.

---

## Mission

Bring UAi to:

```text
UAi — COMPLETE AGAINST ACCEPTED IMPLEMENTABLE ARCHITECTURE
```

or exhaust executable host work with exact evidenced blockers only.

---

## A. Sync package first

1. Sync `UAi_COMPLETENESS_CONTINUOUS_2026-08-09.zip` → `E:\\o2a-dev\\UAi\\`
2. `python -m tests.run_all` → ≥27 PASS
3. Receipt: `E:\\o2a-dev\\UAi\\receipts\\HOST_SYNC_RECEIPT.md`

## B. Host durability

- API :49500 (or documented) boot + think
- Private bind only
- Kill/restart → expeditions intact
- **Reboot/autostart** without browser
- Crash mid-write recovery
- Checkpoint/restore, backup/export/import
- Provider/internet/Galaxy loss → standalone still works

Encryption: local DPAPI only if policy clear; else BLOCKED: BEN_GATE crypto policy and continue.

## C. Estate sessions + bearer rotation

Finish ORD-ESTATE-24H-ROTATION-001 if open.
Mirror: `E:\\o2a-dev\\UAi\\state\\uai_data\\estate_sessions_mirror.json` or hub GET /sessions/summary
Prove `python -m cli.uai_cli sessions`
Bearer rotation dual-window capability or dry-run PASS (no silent prod rotate).

## D. Service Edge live binds

enable → call → independent readback → compare → receipt

Priority: self-health, hub/MCT/Gateway, O2A (verify only), Benjitwin (observe/route only), 23 Council (authorized AUTO_APPLY only), existing estate OAuth/services.

Missing endpoint = BLOCKED: endpoint absent — do not invent.

## E. Surfaces

- ORD-UAI-MAC-SURFACE-001: ATS → host Think → expedition continues after surface close
- /ben/uai portal if in scope: relay only; if Cloudflare hold → BLOCKED: deployment policy; Tailscale relay OK

## F. Reporting law — FORCE TO GROK + GPT

After every bite (and ≥ every 30–60 min):

Write bus-safe report:

```yaml
order_id: ORD-UAI-FULL-COMPLETE-HOST-001
bite_id: <id>
status: PASS|FAIL|BLOCKED|IN_PROGRESS
evidence: <paths>
ledger_updates: <ids + states>
asks_direction_from: [Grok, GPT]
ben_gate_required: false|true
ben_gate_reason: null|<line>
next_bite: <line>
```

**Stuck → ask Grok and GPT. Do not wait on Ben.**
No tokens on bus.

## G. Ledger

Update requirement states only with current host evidence.

## H. Return lines

```text
ORD-UAI-FULL-COMPLETE-HOST-001 — PASS
UAi — COMPLETE AGAINST ACCEPTED IMPLEMENTABLE ARCHITECTURE
```

or

```text
ORD-UAI-FULL-COMPLETE-HOST-001 — EXECUTABLE WORK EXHAUSTED
BLOCKED ONLY BY:
- <blocker>
```

**Claude: begin host sync + durability + session mirror. Report to Grok and GPT.**
