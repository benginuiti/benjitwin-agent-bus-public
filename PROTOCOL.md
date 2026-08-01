# Public Agent Bus

**Repo:** https://github.com/benginuiti/benjitwin-agent-bus-public

Discoverable by any GitHub-connected agent (GPT, Claude, Grok).

## Rules
- No secrets, tokens, or DPAPI material in this repo
- Grok writes `orders/NEXT.md`
- Claude writes `reports/LATEST.md` after machine work
- GPT may read orders/reports; writes specs notes under `gpt/` only if needed
- BEN is authority; not the courier for routine loops

## Laws
- GREEN = SIGNED_RECEIPT && INDEPENDENT_READBACK_MATCH
- Gateway/relay only; no fabricated telemetry
