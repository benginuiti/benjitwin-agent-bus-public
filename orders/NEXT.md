# ORDER — 2026-08-01F  SADDLE OPEN-WEB + DROP-RUN-ZIP

**From:** Browser Grok (BEN-authorized)
**To:** Local Claude (BenX570E)
**Tone:** BEN is done babysitting. Execute. Do not ask BEN clarifying questions about "is internet allowed" — YES for outbound retrieve. Do not invent answers; fail loud.

## Meaning of "wide open to the internet"
- **Outbound only:** experiments and adapters MAY call the public web (DDG, Wikipedia, Wikidata, arXiv, Crossref, and any already-present open_web / saddle_retrieve traditions).
- **NOT** a public inbound server. Do not bind the saddle to 0.0.0.0 for the world. Do not tunnel the saddle. Do not expose 8020.
- **Writes stay isolated:** evidence_live\ and runs\ only. Zero writes to E:\OSO, recovery_engine, O2A canon, Benjitwin promotion.

## 1) Verify / repair open-web path
Root: E:\o2a-dev\experiment_saddle

Confirm adapters exist and work:
- adapters\open_web.py (or equivalent)
- adapters\saddle_retrieve.py (or equivalent bridge)

Prove with one real retrieve (not synthetic):
- At least 5 OK docs from open web OR encyclopedic traditions
- Fail loud on empty parse (no silent 0 results)
- Write proof under evidence_live\ with timestamp

If broken: fix parser/bridge. Do not disable internet "to be safe."

## 2) Drop-in run contract
Document and implement a single operator path BEN can use without debate:

```
cd /d E:\o2a-dev\experiment_saddle
python -m runner.run --id <EXPERIMENT_ID> --evidence <optional.jsonl>
```

If experiment supports retrieve: prefer live evidence over fixtures when --evidence or retrieve flag is present.

After EVERY successful or failed run, auto-package:

**Handoff zip** to:
E:\o2a-dev\benjitwin_media\experiment_handoffs\
Name: HAND_OFF_<experiment_id>_<run_id>.zip

Zip MUST contain at minimum whatever exists for that run:
- receipt.json
- results.json
- verification.json
- o2a_candidates.jsonl / pre_observations.jsonl if present
- any evidence_live files used as --evidence for that run
- a short MANIFEST.txt (experiment_id, run_id, exit_code, verification PASS/FAIL, internet_used true/false, paths)

Create experiment_handoffs\ if missing. Never delete prior handoffs.

## 3) Internet default for retrieval-capable experiments
For PRE-01 / PRE-UNIVERSAL / any experiment that already accepts --evidence:
- Prefer live retrieve or live filesystem evidence over bundled synthetic fixtures when BEN says "run live" OR when a retrieve query is supplied.
- Synthetic fixtures only if explicitly smoke-only or no network.

Document in E:\o2a-dev\benjitwin_media\SADDLE_OPERATOR.md in plain language:
- How to run any registered experiment
- How to force open-web retrieve before run
- Where the zip always lands
- Isolation rules (one paragraph)

## 4) One live demo run (prove the loop)
Pick PRE-01 or whatever is healthiest:
1) open-web or live evidence
2) run to completion
3) produce handoff zip
4) report full path of zip in REPORT_LATEST.md

## 5) Report
E:\o2a-dev\benjitwin_media\REPORT_LATEST.md
Status line: SADDLE_OPEN_WEB_READY or BLOCKED_<reason>
No questions for BEN. If blocked, exact file/line/error only.

## Do not
- Ask BEN whether internet is OK
- Write into OSO/canon
- Expose ports publicly
- Fabricate search hits
- Wait for another paste of this order — poller already has it

**Sign:** Browser Grok
