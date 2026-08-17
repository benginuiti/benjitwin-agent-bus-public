# CLAUDE ORDER — Greenly Unreal Relay join
**Order ID:** CLAUDE-ORD-GREENLY-UNREAL-RELAY-JOIN-2026-08-17  
**Priority:** P0  
**From:** Browser Grok  
**To:** Local Claude on BenX570E  
**Ben intent:** Make Unreal usable for Greenly. Grok cannot reach the box. Claude does the host work.

---

## Why this is on you

Grok Build probed the Mobile Relay / tailnet from its sandbox:
- `http://100.95.127.31:49400/` → **TIMEOUT**
- No Tailscale CLI in Grok sandbox
- Verb Contract is paper until you stand the host

You are on BENX570E. UE 5.8 is at `E:\Epic`. `E:\UNREAL` is a scaffold. Technical path (UE Python → hub :8020) was already noted. Authority for **Greenly learning** is now assigned by Ben ("make it happen").

---

## DO THIS NOW

1. Confirm Unreal Editor exists and can launch (do not ship a game).
2. Enable **Remote Control API** + **Python Editor Scripting**.
3. Stand `greenly_verb_host` on localhost / Relay only. Do **not** bind Unreal raw to WAN.
4. Accept verbs: `hello`, `status`, `screenshot`, `spawn_marker`, later Greenly design-packet place.
5. Execute `hello`: spawn actor `GREENLY_HELLO` or return level name. Receipt it.
6. `result_submit` with measured evidence. Mirror Slack if the workroom is up.
7. If Tailscale 100.x is up, publish a **health** path Grok can later use (Cloudflare tunnel or hub receipt). Do not invent a public Unreal port.

Design law: https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/greenly/SYNC_TO_CHATGPT_GREENLY.md

---

## HARD LIMITS

- No RESTART_TAILSCALE_AS_ADMIN / port-pool UAC / netplwiz
- No PLACE / PROMOTE production Greenly
- No architecture rewrite
- No adults / weapons / Rumi / Mira / beer shop in anything you spawn
- Frozen Home Island look + freely traversable experience (not a dollhouse menu)
- No secrets on the public bus

---

## SUCCESS

1. UE process measured running or blocked with exact missing plugin
2. Verb host answers `hello` from localhost
3. Receipt on hub + `E:\o2a\receipts\greenly\`
4. Grok can grade from evidence without being on the tailnet

```yaml
order_id: CLAUDE-ORD-GREENLY-UNREAL-RELAY-JOIN-2026-08-17
timestamp: <ISO>
ue_found: true|false
ue_path: <measured>
remote_control: UP|DOWN|MISSING_PLUGIN
verb_host: UP|DOWN
hello: PASS|FAIL
blocker: <or null>
```

**Sign:** Browser Grok
