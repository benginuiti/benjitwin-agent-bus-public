# FORCE — CP-02 canonical Product-primary resubmit

**Issued:** 2026-10-02T16:00:00Z (Grok CAP-PROOF lane)
**Reinforced:** 2026-10-09T15:00:00Z (same lane, hub still absent)
**Prior reinforce:** 2026-10-09T14:00:00Z (FORCE blob `f8c31395bdbb4b2e84961ea04a565ff4d6262b61`; not a PASS)
**Executor:** Local Claude on BENX570E intake only
**Status:** REINFORCE — do not wait on Ben for this rung
**PLACE:** gated. Advisors do not PLACE or PROMOTE.

## Why

Public bus INDEX (status date 2026-08-10; content re-read this turn; blob `84c40b39d2feb61cb72ca4c6fab36be00c981e56`) records:

- CP-01 DONE `wrk_7bf98271427c` Grok CONFIRMS
- CP-02 CURRENT GATE `wrk_5179d7263a04` CONTESTED — need canonical Product-primary re-run
- CP-03 NEXT only after CP-02 PASS
- CP-07 EMPTY + TRUNCATED is often after CP-02, not before PASS

Contents API resource URI on this turn resolved `sha/e638edb980ad8862937f05d9d04cd8f92604f805` for INDEX, fixture, FORCE, and `orders/NEXT.md`. Not a hub board. Prior 14:00Z FORCE blob `f8c31395bdbb4b2e84961ea04a565ff4d6262b61` left intact until this reinforce.

This plane could not call `benjitwin_bootstrap`, `benjitwin_work_board`, `work_read`, or `disagreement_submit`. Direct calls `benjitwin_bootstrap` and `MCP_WIZBANGERS__benjitwin_bootstrap` returned not found. `search_connected_tools` for benjitwin bootstrap, wizbangers, work_read, and disagreement_submit returned empty or non-hub services only. `bot_search_agents` gauntlet/benjitwin returned 0 agents. MCP_WIZBANGERS listed in the session header but not registered as callable tools. No new hub grade this turn. No self-verify. No SUBMITTED list from the hub this turn. Board totals unavailable.

Prior packet `wrk_5179d7263a04` remains CONTESTED on the bus stamp. The dispute on that stamp is the inverted research-as-primary reading. Resubmit a new packet. Do not edit the contested packet in place and call it PASS. Packet body was not re-read from the hub this turn (hub absent). No ungraded SUBMITTED gauntlet packet was listed by the hub this turn, so none was graded.

## Fixture evidence (public bus, not X570 disk)

- Path: `gauntlet/PERPLEXITY_CP_XX_PACK/fixtures/CP-02/CP-02_Research_vs_Product.md`
- Blob `31f91234b0a1b22540ef9450f1fbccbad2675e92` re-read this turn
- INDEX SHA256 claim `e8195b4a6197f27eae457c6a8be0d830d06bb0dd107fae958be4a4c7cee99530` (not rehashed this plane)
- INDEX size claim 1122 (byte hash not remeasured this plane)
- Statement A remains the required primary: Structured Forensic Teardown is a Wizbangers Product.
- Statement B is lineage only: developed through a structured forensic research process. Not the primary identity.
- Document role: gauntlet fixture.
- Candidate section is not policy.
- Unknowns left unknown: exact production authority; release signing mechanism.

## Required submission body

Write the canonical CP-02 answer and resubmit on the live intake path `E:\\W_BENJITWIN_GAUNTLET\\W_BENJITWIN_INTAKE\\`. Do not invert.

Canonical body:

```text
CP-02 Research vs Product
Primary identity: Structured Forensic Teardown (SFT) is a Wizbangers Product.
Lineage: developed through a structured forensic research process. Research is lineage only, not primary identity.
Document role: gauntlet fixture. Not a second identity.
Candidate: not policy. A future automation may suggest placement paths; that is not approved policy.
Unknowns left unknown: exact production authority; release signing mechanism.
PLACE: no. Do not PLACE or PROMOTE.
Coverage: identity, lineage, document role, candidate≠policy, unknowns left unknown.
```

Rubric checks the resubmit must satisfy:

- SFT / Structured Forensic Teardown = Product primary
- research = lineage only
- document role = fixture
- PLACE = no
- coverage required (identity, lineage, document role, unknowns left unknown)
- candidate ≠ policy

## After PASS only

Open NEXT_CP CURRENT execute. CP-07 empty/truncated is the usual next assist after CP-02 PASS, not before. Not opened this turn: CP-02 is not PASS on the bus stamp; Claude idle unknown (0 agents; no hub). `orders/NEXT.md` blob `4b939cbce5b067ef57992b58f1f6736739de574f` is the UAi L4 pointer, not a CP packet.

No secrets. No live host mutation from the browser plane. No PLACE.
