# ORD-WEB-MANAGER-HOST-BIND-001
**Issued:** 2026-08-19T21:00:00Z  
**Issuer:** Grok (Browser) — under Ben Law  
**Priority:** P0 — HOST  
**Status:** READY  
**Targets:** Local Claude · Quad (ERIE + Coding Agent) · Nebula Build Team Loop · Galaxy 24/7 residual

---

## 1. Mission

Bind **Ben Web Manager v0.1** on BENX570E as the single-writer control plane for hard primary paths and temporary use banks.

Reference package (Grok surface): `artifacts/BEN_WEB_MANAGER_v0.1/`  
Ferry order: `GROK_FERRY_ORDER.md`  
Ben Law: `BEN_LAW.md`  
Host decision: `HOST_BINDING_DECISION_2026-08-19.md`

## 2. Authority boundaries (non-negotiable)

- Ben = sole architecture / naming / acceptance / promotion authority.
- Web Manager alone allocates, changes, publishes, drains, retires governed paths.
- OSO performs authorized host mutation; callers never choose port/PID/path.
- O2A remains evidence authority.
- CLOCKWORK = scheduler/watchdog only (reconcile consumer).
- MCT = display only (read `/v0/status` `/v0/flow` `/v0/requests` `/v0/receipts`).
- No public Cloudflare/Funnel exposure without separate Ben authorization.
- Fail closed on both AWAITING_BEN decisions (failed-primary hard-path reuse; emergency early temp interrupt).

## 3. Live census facts (already recovered)

| Field | Value |
|-------|-------|
| Computer | BENX570E |
| Observed | 2026-08-19T20:55:13.8294131Z |
| TCP listeners | 71 |
| UDP endpoints | 87 |
| Processes | 65 |
| IPv4 TCP dynamic | 10000–65534 |
| Excluded | 5357, 9011, 27339, 50000–50059 |
| Tailscale | installed=true |

### Historical primaries observed LIVE

| Thing | Port | Addr | PID |
|-------|-----:|------|----:|
| O2A MCP | 8000 | 127.0.0.1 | 26812 |
| O2A Gateway | 8010 | 127.0.0.1 | 26716 |
| Benjitwin | 8020 | 127.0.0.1 | 29176 |
| MCT | 9000 | 127.0.0.1 | 29792 |
| MCT Gateway | 9100 | 127.0.0.1 | 29776 |
| Mobile Relay | 49400 | 0.0.0.0 | 32708 |
| UAi | 49500 | 100.95.127.31 | 3856 |
| ERIE | 49600 | 127.0.0.1 | 23456 |
| Coding Agent | 49700 | 127.0.0.1 | 10872 |
| LOCAL Executor | 49820 | 127.0.0.1 | 9024 |

### Quarantine / do-not-adopt

| Port | Note |
|-----:|------|
| 49750 | CLOCKWORK historical — **MISSING** from live LISTEN |
| 49800 | Unknown adjacent to LOCAL |
| 49610 | Unknown adjacent to ERIE |
| 8055 | Unknown |
| 8899 | Transfer helper candidate — not auto-adopted |
| 9201 | Unknown |

## 4. Port decision (Grok)

| Role | Bind |
|------|------|
| **Web Manager** | **`127.0.0.1:8830`** |
| Alternate | `127.0.0.1:8200` |
| Rejected | 49900 (dev default) |

Nine banks already seeded locally (SERVICE, AGENT, CODER, CODE_GENERATOR, GRAPHICS_GENERATOR, OTHER_GENERATOR, CLIENT_SESSION, PREVIEW_REVIEW, TUNNEL_HTTPS). 24/24 unit tests green.

## 5. Work breakdown by participant

### Local Claude (HOST EXECUTE — primary)

1. Place `BEN_WEB_MANAGER_v0.1` package on BENX570E (or recover from ferry).
2. Generate token; start:
   ```powershell
   $env:BEN_WEB_MANAGER_TOKEN = "<generated-secret>"
   py -m ben_web_manager --db .\web_manager.sqlite3 seed
   py -m ben_web_manager --db .\web_manager.sqlite3 serve --host 127.0.0.1 --port 8830 --token $env:BEN_WEB_MANAGER_TOKEN
   ```
3. Independent round-trip:
   - `GET http://127.0.0.1:8830/health` → 200 minimal
   - Authenticated `GET /v0/status` with `X-Web-Manager-Token`
4. Register live primaries (§3 table) via:
   - `POST /v0/requests` (thing_id, thing_type, bank_name, idempotency_key)
   - `POST /v0/instances/{id}/bind` (PID + start_time + exe fingerprint)
   - `POST /v0/instances/{id}/verify` with **OSO-observed** admission gates only (no caller-supplied booleans)
5. Do **not** move existing service ports. Record them as hard primaries.
6. Leave CLOCKWORK 49750 unregistered until observed listening.
7. Run mandatory host tests from `tests/ACCEPTANCE_MATRIX.md` (host section).
8. Write receipt to project receipts path and report back.

### Coding Agent (Quad — ENGINEERING)

- Implement or harden Windows runtime observer adapters if missing:
  - Listener/PID/start/fingerprint observer
  - Independent client round-trip probe
  - Generation-aware OSO start/drain/stop adapter
- Reject stale generation at mutation boundary.
- No redesign of Web Manager core.

### ERIE (Quad — RESEARCH / NEED)

- Surface any Need for missing identity on quarantined ports (49800, 49610, 8055, 8899, 9201).
- Do not invent identities. Emit Need packets only.

### Nebula Build Team Loop

- Accept this order as LARGE-lane host work under Nebula primary.
- Tick must not mark HOST_VERIFIED from source presence alone.
- Fan-out: Claude executes; ERIE/CA support; Grok grades receipts.

### Galaxy 24/7 residual

- Nebula supersedes Galaxy as primary continuous loop.
- Galaxy residual board may track this as continuity item only — do not dual-execute.

### Browser Grok (this lane)

- Already: ferry custody, census analysis, port candidate, bank seed, 24/24 local tests.
- Next: grade host receipts when Claude returns them. No host start from this surface.

## 6. Acceptance (HOST_VERIFIED only when all true)

- [ ] Process listening on `127.0.0.1:8830`
- [ ] `/health` 200
- [ ] Authenticated `/v0/status` returns nine banks + receipt integrity ok
- [ ] Live primaries registered without port moves
- [ ] Quarantined ports not auto-adopted
- [ ] At least one independent client round-trip receipt
- [ ] MCT can read status/flow without mutation rights
- [ ] No Tailscale Serve / public exposure added unless Ben ordered

## 7. Return format

Claude returns one packet containing:

1. Start command used + token handling note (no raw token in public bus)
2. `/health` + `/v0/status` captures
3. Registration receipts for each primary
4. Host test results (pass/fail per item)
5. Remaining blockers tagged `HOST` | `EVIDENCE` | `AWAITING_BEN`

## 8. Stop conditions

- Architecture change requested → stop, escalate to Ben
- Destructive action needed → stop
- Paid credential required → stop
- LIVE public exposure → Ben only
- No remaining executable host work → report DONE or BLOCKED honestly

---

**Order ID:** ORD-WEB-MANAGER-HOST-BIND-001  
**Grok classification after issue:** READY_FOR_HOST  
**Do not claim completion from open port or HTTP 200 alone.**
