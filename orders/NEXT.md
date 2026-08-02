# ORDER — 2026-08-02D  SLACK OPS CHANNEL

**From:** Browser Grok (BEN-authorized)
**To:** Local Claude (BenX570E)
**BEN:** go slack

## Goal
Private Slack ops channel that mirrors machine status and accepts **allowlisted** commands only. Not a replacement for hub receipts. No secrets in Slack messages.

## BEN does first (Claude cannot)
1. Create Slack app at api.slack.com → Socket Mode ON
2. Bot scopes minimum: `chat:write`, `channels:history`, `channels:read`, `app_mentions:read` (add `commands` if slash commands used)
3. Install to workspace; create private channel e.g. `#benjitwin-ops`; invite bot
4. Put tokens in **DPAPI / process env only** — never disk in git:
   - `BEN_SLACK_BOT_TOKEN` (xoxb-…)
   - `BEN_SLACK_APP_TOKEN` (xapp-… for Socket Mode)
5. Tell Claude when env is set (do not paste full tokens into chat if avoidable)

## Claude executes when tokens available
1. Scaffold `E:\o2a-dev\benjitwin_slack\`:
   - `worker.py` — Socket Mode listener OR short-poll if simpler and documented
   - Allowlist only:
     - `status` → core ports + relay probe summary
     - `report` → last 30 lines REPORT_LATEST.md or path
     - `next` → fetch public NEXT.md raw (no secrets) and post summary
     - `channel` → append note to AGENT_CHANNEL.md that Slack received command
   - Reject everything else with fixed message
2. On startup post one line to channel: `benjitwin-slack-worker up`
3. Mirror: when REPORT_LATEST.md status line changes, optional post (debounce 60s)
4. Loopback / local process only; no exposure of 8020 to Slack network
5. README operator steps; **no tokens in README**
6. If tokens **not** in env: write scaffold + `SLACK_WAITING_TOKENS` in REPORT_LATEST.md — do not block other work forever

## Laws
- Never post O2A_GATEWAY_TOKEN, relay token, API keys, or file contents from E:\OSO
- Never run arbitrary shell from Slack text
- Hub/receipts remain source of truth for work

## Report
Status: `SLACK_WORKER_UP` | `SLACK_WAITING_TOKENS` | `BLOCKED_<exact>`

Parallel OK: if LOCAL INTEL Bite 0–1 was in progress, finish or note paused.

**Sign:** Browser Grok
