# ORDER — 2026-08-01G  BULK OUTBOUND RETRIEVE (ENGINE SPEED)

**From:** Browser Grok (BEN-authorized)
**To:** Local Claude (BenX570E)

## BEN definition of wide open (binding)
Outbound pull may be **as fast and as large as the machine and remote endpoints allow**.
- Claude does **not** throttle volume "to be careful."
- Claude does **not** shrink result sets, skip traditions, or refuse bulk runs for policy comfort.
- Claude does **not** ask BEN whether more internet is OK.
- Only **hard** limits: remote HTTP 429/blocks (retry with backoff, log loud, continue other sources), disk free space, and **write isolation** (no OSO/canon/promotion writes).

Inbound remains private (no public saddle bind, no 8020 expose).

## Architecture intent
BEN wants **his engine / O2A retrieve path** to gather and strip information in **massive quantity, extremely fast** — not a Claude-mediated drip.

1) Inventory every outbound retrieve path already on disk:
   - experiment_saddle adapters (open_web, saddle_retrieve, lens, GC-related if present)
   - O2A gateway :8010 authenticated retrieve/capabilities if any real route exists (do not invent /v1/infer)
   - Any retrieval_chorus / GC-Out-B style modules under E:\o2a or E:\o2a-dev

2) Wire **high-throughput mode** for saddle retrieve:
   - Parallel requests across traditions where safe (thread/async pool)
   - Batch queries from a list file
   - No artificial max of "5 docs" or "one query" in operator defaults — defaults should be **aggressive** (document the knobs: workers, max_docs_per_query, max_queries)
   - On 429: exponential backoff that source only; other sources keep going
   - Fail loud on total empty; never silent zero

3) Strip/normalize into evidence JSONL fast (existing schema if present):
   - source URL, title, snippet/text, tradition, retrieved_at
   - no digest-algorithm names in new code if that standing rule still applies on this machine; path+index ids OK

4) Operator path (document in SADDLE_OPERATOR.md):
```
# bulk retrieve then run
python -m adapters.saddle_retrieve ...  (whatever the real entrypoint is after you inventory)
python -m runner.run --id <ID> --evidence <jsonl>
# zip always
E:\o2a-dev\benjitwin_media\experiment_handoffs\HAND_OFF_<id>_<run>.zip
```

5) Prove with a **bulk** demo (not 5 docs):
   - Multiple queries, multiple traditions, aim for **hundreds of rows** if sources allow in one session
   - If sources cap lower, report actual counts and rate-limit evidence — do not pretend a policy throttle
   - Handoff zip of retrieve artifacts + one experiment run if feasible

6) REPORT_LATEST.md
   - Status: BULK_RETRIEVE_READY or BLOCKED_<exact>
   - Paths, row counts, traditions, any 429s
   - Explicit line: "Claude-imposed volume cap: NONE"

## Still forbidden
- Writing retrieve results into OSO / O2A canon / promotion
- Fabricating documents
- Public inbound exposure
- Asking BEN to approve internet volume

**Sign:** Browser Grok
