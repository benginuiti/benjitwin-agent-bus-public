# ORDER — 2026-08-02B  BENJITWIN LOCAL INTEL TIER 1

**From:** Browser Grok (BEN-authorized)
**To:** Local Claude (BenX570E)

## Scope
Local intelligence for **Benjitwin only** (hub/registry/work board).  
**Do not** add Ollama or any local model into O2A or Big Sorter (2026-07-23 ruling stands).

## P0 still
If relay/poller down: restore per 2026-08-02A first (token from BEN for relay).

## Tier 1 — embeddings (execute)
1) Install embedding model offline-capable: prefer `BAAI/bge-small-en-v1.5` or `all-MiniLM-L6-v2` via sentence-transformers **or** Ollama pull **only if** kept in a Benjitwin-only path (document path; never wire into o2a_mcp write surface).
2) Build index over existing local text only:
   - hub work items / board export if available
   - workpacket identity fields if readable without loading full 29MB into RAM at once (batch)
   - registry entity names/summaries if present on disk
3) CLI or small service on **loopback only**: `query → top-k doc ids + scores` — no generation.
4) Prove: 3 sample queries return ranked existing ids; write receipt to benjitwin_media\LOCAL_INTEL_TIER1_RECEIPT.md
5) REPORT status: `LOCAL_EMBED_READY` or `BLOCKED_<exact>`

## Do not
- Open-ended chat model in this bite
- Assert facts not in retrieved rows
- Canon/OSO writes
- GPU required for Tier 1 (CPU OK)

Tier 2 (Qwen2.5-7B route capabilities) only after Tier 1 green + explicit BEN go.

**Sign:** Browser Grok
