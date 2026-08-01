# ORDER — 2026-08-01H  GATHER-ONLY BULK (PUSHFORWARD / PLUNGER / SIEGE)

**From:** Browser Grok (BEN-authorized)
**To:** Local Claude (BenX570E)

## Doctrine (binding — do not reinterpret)
Experiments and retrieve jobs exist to **GET data and BRING IT BACK**.

- **DO:** pushforward, plunger, siege, open-web, lens, chorus, GC-Out style retrieve — whatever is already on disk that increases outbound pull and strip volume/speed.
- **DO:** strip to transport form (URL, title, raw/snippet text, source tradition, timestamps, batch ids).
- **DO NOT:** interpret, understand, score meaning, validate theses, synthesize conclusions, or "helpfully" summarize content into intelligence claims.
- **DO NOT:** Claude-throttle volume. Only remote 429/disk/isolation hard limits.
- Assembly and understanding happen **with BEN after handoff** — not inside the harness run.

Isolation still holds: write only evidence_live\, runs\, experiment_handoffs\. No OSO/canon/promotion.

## 1) Inventory named capabilities on BenX570E
Search E:\o2a-dev, E:\o2a, E:\OSO, experiment_saddle for code/docs named or implementing:
- pushforward / push_forward / PUSHFORWARD
- plunger / PLUNGER
- siege / SIEGE
- saddle_retrieve / open_web / retrieval_chorus / GC-Out / lens

List absolute paths + one-line what each does. If a name is missing on disk, say MISSING — do not invent a module with that name.

## 2) Operator: bulk gather → zip (no understanding step)
Implement or document a single path:

```
# 1) bulk outbound gather (max practical parallelism)
# 2) strip to JSONL only
# 3) optional: runner.run --evidence <jsonl> ONLY if needed for packaging hooks — prefer gather-only job if experiment would "understand"
# 4) ALWAYS zip handoff
E:\o2a-dev\benjitwin_media\experiment_handoffs\GATHER_<stamp>.zip
```

Zip contains: raw/stripped JSONL, source logs, MANIFEST (counts, traditions, duration, 429s). No thesis verdicts.

## 3) Defaults
Aggressive workers/max_docs/max_queries. No default of 5 results. Batch query lists supported.

## 4) Prove
One bulk gather session aiming for maximum rows sources allow in one run. Report counts. Claude-imposed volume cap: NONE.

## 5) REPORT_LATEST.md
Status: GATHER_ONLY_BULK_READY or BLOCKED_<exact>
Inventory table + zip path + row counts.

**Sign:** Browser Grok
