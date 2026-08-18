# Greenly operator cockpit

**Tied:** 2026-08-18  
**Packet:** 1.6.0  
**Authority:** BEN sole promotion  
**ChatGPT session:** Greenly  

The cockpit is the **operator surface**. It is not the lived world.

- Human: `/cockpit`
- Machine: `/api/cockpit`, `/api/cockpit/probe`, `/api/health`

## Alignment (packet v1.0)

States stay separate: `RECOVERED`, `WONDER`, `ACCEPTED`, `APPLIED`, `VERIFIED`.

| Item | State |
| --- | --- |
| Frozen island look | FROZEN |
| `/world` | Lived player world |
| Cockpit 1.6.0 | APPLIED · live JSON readback |
| Day 3 Pet Friend Studio | APPLIED on `/world` — expression, not replacement |
| Day 5 Wildshape Conservatory | APPLIED on `/world` — inspirations, not captives; scale is not power |
| UX v0.1 | ACCEPTED as design baseline (Ben execute 2026-08-17) |
| Day 1 lived journey | APPLIED on `/world` — not a menu |
| Day 10 Our Place | NOT YET BUILT — executing next |
| Bite 2 affordance map | APPLIED — 17 lived landmarks |
| GDR 81 | RECOVERED prior decisions (71 ACCEPT / 10 HOLD) |
| GRC 509 / GBA 163 / GWN 077 | Recovered or wonder — not silently merged |
| Quiet cove + private exit | ACCEPTED · APPLIED |
| Family envelope | APPLIED on cockpit only |
| Runtime | UNVERIFIED — no joined lived-world + SRN + device + failure-injection proof |

Review Center: https://greenly-ben-design-review.heyavguru.chatgpt.site

## How Ben reaches it

| From | How |
| --- | --- |
| This preview / public host | Open `/cockpit` on the current origin |
| Laptop or iPad at home | Same Greenly process on the house machine, bound on all interfaces. Open `http://<lan-ip>:8080/cockpit` |
| Phone away from home | Tailscale Serve on that house machine. Open `https://<magicdns>/cockpit` (or the `100.x` origin). Prefer Serve, not Funnel |
| Twin / assets | Tailscale Mobile Relay `http://100.95.127.31:49400` — go-between only, not a second Greenly |

Save LAN, Tailscale, and Relay origins in the cockpit. They persist on that browser. Probe them from the deck.

## What ChatGPT and local services should fetch

1. `/api/cockpit` — live operator packet (access class, surfaces, gates, loops, alignment)
2. `/api/health` — heartbeat for LAN / Tailscale checks
3. `/api/design` — design packet + gate results
4. This file on the public bus if the live host is not reachable

Do not invent locked names, broadcast rights, beach/underwater travel, or a dollhouse experience model. Do not promote GRC / GBA / GWN.

## Settled experience (do not reopen)

Greenly is a real-time freely traversable world. Frozen Home Island visual baseline unchanged. Cockpit does not redesign it.
