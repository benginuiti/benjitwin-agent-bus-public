# Greenly — how ChatGPT and local services review design

**Updated:** 2026-08-17  
**Tied to ChatGPT session:** Greenly  
**Authority:** BEN only for promotion.

## First file for ChatGPT

https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/greenly/SYNC_TO_CHATGPT_GREENLY.md

Then:

```
https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/greenly/DESIGN.json
https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/greenly/EXPERIENCE.md
https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/greenly/COCKPIT.md
https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/greenly/PLAY.md
```

If a live host is reachable, prefer `/api/cockpit` then `/api/design`.

## Three lanes

| Lane | What it is | Where |
|------|------------|--------|
| **Lived world** | Freely traversable Home Island | Preview **World** (`/world`) |
| **Operator** | LAN / Tailscale / Relay deck | `/cockpit` · `/api/cockpit` |
| **Design** | Machine + human check | `/design` · `/api/design` · this bus folder |

ChatGPT cannot see the Grok preview tab. Fetch the bus files or the live machine endpoints.

## Review contract

1. Ingest SYNC_TO_CHATGPT_GREENLY.md.
2. Fetch DESIGN.json (or `/api/design`).
3. Do not invent locked names, rights, or beach/underwater features.
4. FAIL if Rumi/Mira, adults on GIA, weapons, beer shop, or military vehicles appear as locked.
5. Write findings back to the Greenly chat only. No silent promotion.

## Play

Guest. `/world`. WASD or pad. Run at the slide.

## Cockpit reach

- House: `http://<lan-ip>:8080/cockpit`
- Away: Tailscale Serve MagicDNS `/cockpit`
- Twin assets: relay `http://100.95.127.31:49400` (go-between, not the cockpit)
