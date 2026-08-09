# ORDER — Estate 24h keeper completeness + atomic bearer rotation
**Order ID:** ORD-ESTATE-24H-ROTATION-001
**Priority:** P0
**From:** Browser Grok
**To:** Local Claude on BenX570E (hub/runner owner)
**Authority:** Ben
**Mode:** EXECUTE — no secrets on public bus
**Sign:** Browser Grok

---

## Goal

1. Keep the live **24h auto-refresh session fabric** for all estate connections.
2. Publish a **non-secret session summary** UAi can observe.
3. Implement **atomic bearer rotation** for STATIC_BEARER connections (explicit, dual-window, config rewrite, restart, revoke, receipt).

---

## Non-negotiables

1. No access tokens, refresh tokens, bearer secrets, or DPAPI blobs in git, bus, UAi state, or receipts.
2. UAi never becomes the secret store.
3. OAuth continues true refresh via refresh_token.
4. LOOPBACK = keepalive + window reset.
5. MCP_CLIENT (Desktop Commander) = track + keep server up; do not claim client session force-reconnect.
6. STATIC_BEARER rotation is **only** when Ben/this order authorizes a named connection — never silent daily rotate.
7. Dual-window required: old OR new valid until new proven.
8. Atomic config write: temp → fsync → rename; backup previous.
9. Receipt every mutation.

---

## Already PASS (do not rebuild)

- 24h sessions on estate connections with connection-keeper in runner
- OAuth access TTL 86400 + refresh_token path
- Overdue session auto-refresh proof (refresh_count=1)
- UAi v0.02 package includes observer + rotation *plans* (23/23 tests)

---

## Exact work

### A. Session mirror for UAi (required)

1. Hub or runner writes **non-secret** JSON mirror to:
   `E:\\o2a-dev\\UAi\\state\\uai_data\\estate_sessions_mirror.json`
   **or** hub endpoint `GET /sessions/summary` returning the same shape.
2. Shape per connection (fields only):

```json
{
  "connection_id": "svc-...",
  "name": "Slack",
  "kind": "OAUTH|LOOPBACK|MCP_CLIENT|STATIC_BEARER",
  "expires_at": "ISO-8601",
  "refresh_count": 0,
  "last_keepalive": "ISO-8601",
  "keepalive_status": "alive|dead|unknown",
  "due_now": false,
  "notes": "no secrets"
}
```

3. Strip any token fields before write.
4. On host after UAi sync: `python -m cli.uai_cli sessions` must show source local_mirror or hub_endpoint.

### B. Atomic bearer rotation (required capability)

Implement host tool/procedure:

```text
plan → dual_window → rewrite configs → restart deps → prove new → revoke old → receipt
```

On failure: restore backup configs → restart → state ROLLED_BACK → receipt.

Minimum: dry-run against a test bearer **or** one STATIC_BEARER Ben names.

### C. Proofs

1. Mirror or `/sessions/summary` readable; `due_count` consistent with keeper.
2. Plant overdue loopback session → keeper refreshes (regression).
3. Rotation dry-run or real: dual-window, atomic rewrite, PASS receipt **without** secret material.
4. UAi `sessions` CLI on host shows INFERENCE summary only.

---

## Do not

- Put secrets in UAi or this bus
- Force Claude Desktop MCP client reconnect from server
- Daily-rotate static bearers without explicit named target
- Move OAuth tokens into UAi core
- Redesign UAi cognition

---

## Receipt

Write: `reports/RECEIPT_ORD-ESTATE-24H-ROTATION-001.md` (bus) and/or local host receipt.

```yaml
order_id: ORD-ESTATE-24H-ROTATION-001
session_mirror: PASS|FAIL
keeper_regression: PASS|FAIL
bearer_rotation: PASS|FAIL|DRY_RUN_PASS
secrets_in_artifacts: false
result: PASS|BLOCKED
blocker: null|string
```

## Return line

`ORD-ESTATE-24H-ROTATION-001 — PASS`
or
`ORD-ESTATE-24H-ROTATION-001 — BLOCKED: <one blocker>`
