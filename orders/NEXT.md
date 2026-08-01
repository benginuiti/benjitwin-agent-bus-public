# ORDER — 2026-08-01I  TWIN OUTBOUND PROVIDER APIs

**From:** Browser Grok (BEN-authorized)
**To:** Local Claude (BenX570E)
**BEN intent:** Benjitwin gets **direct API control** of external providers (OpenAI/GPT, Anthropic/Claude, xAI/Grok) as **callable tools**, not as owners of the twin.

## Architecture (do not invent alternate)
```
Phone /chat → /intention → hub work
                → provider_bridge (new)
                    → OpenAI API | Anthropic API | xAI API
                → receipt + response artifact on disk
                → optional: surface reply in chat UI
```

- Keys: **Windows DPAPI / existing sealed store only** — never write API keys into git, chat.html, or REPORT files.
- Env names (example): `BEN_OPENAI_API_KEY`, `BEN_ANTHROPIC_API_KEY`, `BEN_XAI_API_KEY` — if unset, that provider returns honest UNAVAILABLE.
- Every call: log provider, model, latency, token usage if available, work_id, receipt_id — no silent calls.

## Phase 1 — Scaffold + one live provider (read-first)
1) Inventory any existing HTTP client / LLM wrapper under E:\o2a-dev or E:\o2a (do not duplicate blindly).
2) Create `E:\o2a-dev\benjitwin_provider_bridge\` with:
   - `bridge.py` or `bridge_app` callable from hub worker OR relay after intention
   - `providers/openai_compat.py` (OpenAI + xAI often OpenAI-compatible)
   - `providers/anthropic.py`
   - `README.md` operator only (no secrets)
3) Minimal interface:
   `complete(provider, model, messages, work_id) -> {text, provider, model, usage, error}`
4) Wire **one** path end-to-end for proof:
   - Prefer: after successful /intention, if env `BEN_TWIN_PROVIDER` set, call bridge and append reply text to receipt JSON and return in /intention response so /chat shows it.
   - If hub worker is cleaner given current code, do that — document which.
5) Prove with whichever key is already on the machine (report provider name only, never key).
   If **no** keys in env/DPAPI: implement full scaffold, prove UNAVAILABLE path, status `BRIDGE_READY_AWAITING_KEYS`.

## Phase 2 — Chat UX
- /chat already posts /intention; ensure JSON response can carry `twin_reply` when bridge runs.
- Do not fake intelligence if provider fails — show error honestly.

## Laws
- External models are **ecosystem tools**, not O2A organs.
- No canon/OSO writes from provider output unless BEN later promotes.
- No keys in repo or logs.
- Gather-only bulk order remains valid for data plane; this bite is **articulation/control plane**.

## Report
REPORT_LATEST.md status: `PROVIDER_BRIDGE_LIVE` | `BRIDGE_READY_AWAITING_KEYS` | `BLOCKED_<exact>`
List providers implemented + which env vars expected.

**Sign:** Browser Grok
