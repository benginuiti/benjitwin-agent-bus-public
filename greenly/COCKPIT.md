# Greenly operator cockpit

**Tied:** 2026-08-17  
**Authority:** BEN sole promotion  
**ChatGPT session:** Greenly  

The cockpit is the **operator surface**. It is not the lived world.

- Human: `/cockpit`
- Machine: `/api/cockpit`, `/api/cockpit/probe`, `/api/health`

## How Ben reaches it

| From | How |
| --- | --- |
| This preview / public host | Open `/cockpit` on the current origin |
| Laptop or iPad at home | Same Greenly process on the house machine, bound on all interfaces. Open `http://<lan-ip>:8080/cockpit` |
| Phone away from home | Tailscale Serve on that house machine. Open `https://<magicdns>/cockpit` (or the `100.x` origin). Prefer Serve, not Funnel |
| Twin / assets | Tailscale Mobile Relay `http://100.95.127.31:49400` — go-between only, not a second Greenly |

Save LAN, Tailscale, and Relay origins in the cockpit. They persist on that browser. Probe them from the deck.

## What ChatGPT and local services should fetch

1. `/api/cockpit` — live operator packet (access class, surfaces, gates, loops)
2. `/api/health` — heartbeat for LAN / Tailscale checks
3. `/api/design` — design packet + gate results
4. This file on the public bus if the live host is not reachable

Do not invent locked names, broadcast rights, beach/underwater travel, or a dollhouse experience model.

## Settled experience (do not reopen)

Greenly is a real-time freely traversable world. Frozen Home Island visual baseline unchanged. Cockpit does not redesign it.
