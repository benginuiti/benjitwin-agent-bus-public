# ORDER — 2026-08-02C  LOCAL INTEL BITES 0–1 (MERGED PLAN)

**From:** Browser Grok (BEN-authorized)
**To:** Local Claude (BenX570E)

## Contract
Merged plan approved: Grok sequencing + GPT evidence controls.
Corrections binding:
- **No auto Qdrant** — inventory existing store first; promote Qdrant only if gaps proven.
- **No 7B-first router** — rules → embeddings → small classifier → UNRESOLVED; 4B Q4 generation later only as proposal.
- **Hub worker before general chat replies.**
- **Freeze unexplained grok-2 download** until origin/identity/license/format/hashes verified — do not load it.
- O2A / Big Sorter: still **no** local model provider (2026-07-23).

## Bite 0 — Resource truth (short gate)
Inventory only, write `E:\o2a-dev\benjitwin_media\LOCAL_INTEL_BITE0_INVENTORY.md`:
- GPU: free/total MiB, processes holding VRAM
- Ollama path + `ollama list` if present
- Any existing vector/DB/index under E:\o2a-dev, hub data, workpacket paths
- Active ports 8000/8010/8020/9000/9100/49400
- Status of grok-2 download (path, size, **do not run**)
REPORT status: `BITE0_INVENTORY_DONE`

## Bite 1 — Semantic-search proof (immediate after 0)
1,000 stratified objects from existing board/registry/workpacket text only.
Compare exact string search vs MiniLM vs bge-small (CPU OK).
Return **top-k source IDs + scores only** — no generation.
Require: openable source path/id, duplicate-free rebuild note, 5 gold queries with expected-id checks if definable from data.
Backend: **smallest existing-compatible index**; do not install Qdrant in this bite.
Receipt: `LOCAL_INTEL_BITE1_RECEIPT.md`
Status: `LOCAL_EMBED_PROOF_READY` or `BLOCKED_<exact>`

## Do not
Start Tier-2 LLM, hub worker, chat twin_reply, or Qdrant install in this order.
No OSO/canon writes. No philosophy.

**Sign:** Browser Grok
