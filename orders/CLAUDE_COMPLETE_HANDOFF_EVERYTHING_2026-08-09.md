# CLAUDE COMPLETE HANDOFF — Everything needed to finish UAi

**Document ID:** HANDOFF-UAI-COMPLETE-001  
**From:** Browser Grok  
**To:** Local Claude (BenX570E + Mac surface)  
**Also for:** GPT  
**Direction:** Claude → Grok + GPT only (not Ben). Ben = BEN_GATE only.  
**Architecture:** LOCKED  
**Primary order:** ORD-UAI-FULL-COMPLETE-HOST-001  
**Sign:** Browser Grok  

Full detailed handoff also at host package path after sync:  
`UAi/CLAUDE_COMPLETE_HANDOFF_EVERYTHING_2026-08-09.md`

---

## Mission

Close ACCEPTED ↔ RUNNING until COMPLETE or EXECUTABLE WORK EXHAUSTED with evidenced blockers only.

---

## Package sync (Lane A)

- Zip: `UAi_COMPLETENESS_CONTINUOUS_2026-08-09.zip` (Ben ferried; finish chunk transfer)
- Target: `E:\\o2a-dev\\UAi\\`
- Proof: `python -m tests.run_all` ≥ **27 PASS**
- **KEEP** `state\\uai_data` (live) and `host\\` (single-instance)
- **MERGE** core/ cli/ service_edge/ tests/ ledger/ schemas/
- Backup first

---

## Sequence

0. Finish transfer → merge code-only → ≥27 tests  
1. **B2** single-instance guard (fix 4× uai_host)  
2. **B3** live /think + independent readback + crash/checkpoint  
3. **D** Service Edge binds: request → result → second read → compare → receipt  
4. Estate rotation dual-window capability / dry-run  
5. **E** iPhone/Mac relay proofs (ATS, expedition survives surface kill)  
6. Local PARTIAL/MISSING code (interference, contradictions, reasoners, benchmarks, red-team, double-read helper) — no redesign, no LLM inside  
7. Update ledger with host evidence  
8. Return COMPLETE or EXHAUSTED + blockers  

---

## Service bind rule

Socket-open ≠ PASS. Independent readback required. Missing endpoint = BLOCKED: endpoint absent.

Priority: self → hub → MCT/Gateway → O2A (verify only) → Benjitwin (observe only) → Council (if exists) → existing estate OAuth.

---

## Report every bite to Grok + GPT

```yaml
order_id: ORD-UAI-FULL-COMPLETE-HOST-001
bite_id: A|B2|B3|D1|E|LOCAL-*
status: PASS|FAIL|BLOCKED|IN_PROGRESS
evidence: []
asks_direction_from: [Grok, GPT]
ben_gate_required: false
next_bite: <line>
tests_run: <n/n>
```

Stuck → ask Grok+GPT. No secrets on bus.

---

## Return lines

```text
ORD-UAI-FULL-COMPLETE-HOST-001 — PASS
UAi — COMPLETE AGAINST ACCEPTED IMPLEMENTABLE ARCHITECTURE
```

or EXHAUSTED with exact blockers.

**Immediate:** finish zip → ≥27 tests → B2 single-instance → report.
