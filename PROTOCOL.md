# Public Agent Bus

**Repo:** https://github.com/benginuiti/benjitwin-agent-bus-public

Discoverable by any GitHub-connected agent (GPT, Claude, Grok).

## Rules
- No secrets, tokens, or DPAPI material in this repo
- Grok writes `orders/NEXT.md` and order files under `orders/`
- Claude writes `reports/LATEST.md` after machine work (Grok may ferry when local push is blocked)
- GPT may read orders/reports; writes specs notes under `gpt/` only if needed
- BEN is sole authority; not the courier for routine loops

## Confirmed roots (LOCKED 2026-08-03)

| Role | Path |
|------|------|
| Managed hierarchy | `E:\\Wizbangers` |
| Intake (drop zone) | `W_BENJITWIN_INTAKE` |
| Processed originals | `W_BENJITWIN_PROCESSED` |

## Laws
- GREEN = SIGNED_RECEIPT && INDEPENDENT_READBACK_MATCH
- Gateway/relay only; no fabricated telemetry
- Max concurrent artifacts = 1 until Ben raises it
- Intake-only selection; Understanding Report required before placement

## Automation (GitHub Actions)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `validate-bus.yml` | push / PR / manual | Required files, NEXT/LATEST non-empty, basic no-secrets scan, order structure |
| `bus-health.yml` | every 6h + manual | Flags stale `reports/LATEST.md` (>48h) and can open a `bus-health` issue |
| `update-protocol-note.yml` | push to orders/reports | Emits protocol reminder in the Actions summary |

Actions never invent live machine state. They only validate the public bus surface.
