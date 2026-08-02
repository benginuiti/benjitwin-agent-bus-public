# ORDER — 2026-08-02E  HUB WORKER V0

**From:** Browser Grok (BEN-authorized)
**To:** Local Claude (BenX570E)
**BEN:** Go hub worker

## Goal
Replace routine paste/Claude execution for OPEN hub items. v0 is ack + status + Slack thread reply. No cloud LLM keys required. No arbitrary shell.

## Location
`E:\o2a-dev\benjitwin_hub_worker\` (new)
Share 3.12 venv patterns with relay/slack if practical.

## Behavior
1. Poll `http://127.0.0.1:8020` for OPEN work (use real hub API from source — do not invent routes; read hub code first).
2. Claim one eligible item if hub supports claim; else process with explicit "worker touch" note without violating self-verify bans.
3. Allowlist actions only:
   - **ack** — mark handled path with receipt under `benjitwin_media\receipts\`
   - **status** — same port summary style as Slack heartbeat (loopback probes)
   - **echo** — return title/description truncated in result
4. If work description/meta contains Slack channel+thread (from Slack intake), post result back to that thread via existing Slack bot tokens (env/DPAPI). If no Slack context, write receipt only.
5. Never: OSO writes, promote, delete, arbitrary shell from title text, provider API calls in v0.
6. start script: `start_hub_worker.ps1` — restart-safe, logs to benjitwin_media\hub_worker.log
7. Heartbeat optional line to #runtime every N minutes: `hub-worker v0 alive`

## Hub auth
8020 currently may have no auth — do not expose; worker is loopback only. Document exact routes used in HUB_WORKER_V0.md

## Report
`HUB_WORKER_V0_UP` with: poll interval, routes used, one test work_id processed, Slack reply yes/no.
Or `BLOCKED_<exact>` if hub API cannot claim/list OPEN.

Slack worker stays running; do not break it.

**Sign:** Browser Grok
