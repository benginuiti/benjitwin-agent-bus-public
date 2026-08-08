#!/usr/bin/env bash
# poll_agent_bus.sh — fetch public NEXT.md (+ referenced order), detect changes, write local bus files.
# No secrets. No remote code execution. Order body is saved for Claude/operator to run.
# macOS / Linux. Default: one poll. Use --loop to poll until stopped.

set -euo pipefail

BUS_BASE="${BUS_BASE:-https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main}"
BUS_URL="${BUS_URL:-$BUS_BASE/orders/NEXT.md}"
LOCAL_ROOT="${LOCAL_ROOT:-$HOME/benjitwin_bus}"
INTERVAL_SEC="${INTERVAL_SEC:-120}"
LOOP=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --loop) LOOP=1; shift ;;
    --interval) INTERVAL_SEC="$2"; shift 2 ;;
    --root) LOCAL_ROOT="$2"; shift 2 ;;
    --url) BUS_URL="$2"; shift 2 ;;
    -h|--help)
      cat <<'EOF'
Usage: poll_agent_bus.sh [--loop] [--interval SEC] [--root DIR] [--url URL]

Fetches public agent-bus NEXT.md, writes local copy, detects changes,
and downloads any order file referenced as orders/<name>.md

Defaults:
  LOCAL_ROOT=$HOME/benjitwin_bus
  INTERVAL_SEC=120
  BUS_URL=https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/orders/NEXT.md

Env overrides: BUS_BASE, BUS_URL, LOCAL_ROOT, INTERVAL_SEC
EOF
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

ORDERS_DIR="$LOCAL_ROOT/orders"
STATE_DIR="$LOCAL_ROOT/bus_state"
REPORTS_DIR="$LOCAL_ROOT/reports"
NEXT_LOCAL="$ORDERS_DIR/NEXT.md"
HASH_FILE="$STATE_DIR/next.sha256"
LOG_FILE="$STATE_DIR/poll_log.txt"
FLAG_NEW="$STATE_DIR/NEW_ORDER.flag"
ACTIVE_ORDER_FILE="$STATE_DIR/active_order_path.txt"

mkdir -p "$ORDERS_DIR" "$STATE_DIR" "$REPORTS_DIR"

log() {
  local line
  line="$(date -u +"%Y-%m-%dT%H:%M:%SZ")  $*"
  echo "$line" | tee -a "$LOG_FILE"
}

sha256_text() {
  # macOS shasum vs Linux sha256sum
  if command -v sha256sum >/dev/null 2>&1; then
    printf '%s' "$1" | sha256sum | awk '{print $1}'
  else
    printf '%s' "$1" | shasum -a 256 | awk '{print $1}'
  fi
}

fetch() {
  local url="$1"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL --max-time 30 "$url"
  else
    wget -qO- --timeout=30 "$url"
  fi
}

# Extract first orders/*.md reference from NEXT body (filename only)
extract_order_ref() {
  local body="$1"
  printf '%s
' "$body" | grep -Eo 'orders/[A-Za-z0-9._-]+\.md' | head -1 || true
}

poll_once() {
  local body sha prev status order_rel order_url order_local
  body="$(fetch "$BUS_URL")"
  sha="$(sha256_text "$body")"
  prev=""
  if [[ -f "$HASH_FILE" ]]; then
    prev="$(tr -d '[:space:]' < "$HASH_FILE")"
  fi

  printf '%s
' "$body" > "$NEXT_LOCAL"

  order_rel="$(extract_order_ref "$body")"
  if [[ -n "$order_rel" ]]; then
    order_url="$BUS_BASE/$order_rel"
    order_local="$LOCAL_ROOT/$order_rel"
    mkdir -p "$(dirname "$order_local")"
    if fetch "$order_url" > "$order_local"; then
      printf '%s
' "$order_local" > "$ACTIVE_ORDER_FILE"
      log "ORDER_FETCHED $order_rel -> $order_local"
    else
      log "ORDER_FETCH_FAILED $order_url"
    fi
  else
    log "ORDER_REF_NONE (no orders/*.md in NEXT.md)"
  fi

  if [[ "$sha" != "$prev" ]]; then
    printf '%s
' "$sha" > "$HASH_FILE"
    cat > "$FLAG_NEW" <<EOF
{
  "measuredAt": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "sha256": "$sha",
  "path": "$NEXT_LOCAL",
  "url": "$BUS_URL",
  "order_ref": "${order_rel:-}"
}
EOF
    log "NEW_ORDER sha=$sha bytes=${#body} -> $NEXT_LOCAL"
    status="NEW_ORDER"
  else
    log "UNCHANGED sha=$sha"
    status="UNCHANGED"
  fi
  printf '%s
' "$status"
}

log "poll start Loop=$LOOP IntervalSec=$INTERVAL_SEC Root=$LOCAL_ROOT"
status="ERROR"
while true; do
  if status="$(poll_once)"; then
    :
  else
    log "ERROR poll failed"
    status="ERROR"
  fi
  if [[ "$LOOP" -eq 0 ]]; then
    break
  fi
  sleep "$INTERVAL_SEC"
done

log "poll end status=$status"
exit 0
