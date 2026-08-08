# Agent bus poll scripts

Public bus: https://github.com/benginuiti/benjitwin-agent-bus-public

**Rules:** no secrets, no remote code execution. Scripts only download `orders/NEXT.md` and any referenced `orders/*.md` order file into a local folder for Claude/operator to read.

## Mac / Linux

```bash
curl -fsSL -o poll_agent_bus.sh \
  https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/scripts/poll_agent_bus.sh
chmod +x poll_agent_bus.sh

# one shot
./poll_agent_bus.sh

# loop every 2 minutes
./poll_agent_bus.sh --loop --interval 120

# custom local root (default: ~/benjitwin_bus)
./poll_agent_bus.sh --root "$HOME/benjitwin_bus"
```

After a successful poll:

| Path | Meaning |
|------|--------|
| `$ROOT/orders/NEXT.md` | Active pointer |
| `$ROOT/orders/ORD-....md` | Fetched active order body |
| `$ROOT/bus_state/NEW_ORDER.flag` | JSON flag when NEXT changed |
| `$ROOT/bus_state/active_order_path.txt` | Path to last fetched order file |
| `$ROOT/bus_state/poll_log.txt` | Log |

## Windows (X570)

```powershell
cd E:\o2a-dev\benjitwin_media   # or your preferred root
Invoke-WebRequest -Uri https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/scripts/poll_agent_bus.ps1 -OutFile poll_agent_bus.ps1

# one shot
.\poll_agent_bus.ps1

# loop
.\poll_agent_bus.ps1 -Loop -IntervalSec 120

# custom root
.\poll_agent_bus.ps1 -LocalRoot "E:\o2a-dev\benjitwin_media"
```

Default Windows `LocalRoot` remains `E:\o2a-dev\benjitwin_media` for compatibility with existing poll layout.

## Claude usage

1. Run poll (or leave `--loop` / `-Loop` running).
2. If `NEW_ORDER.flag` exists or NEXT changed, open the path in `active_order_path.txt`.
3. Execute the order. Write receipt under `reports/` (local and/or push to bus `reports/` when allowed).
4. Do not put tokens or secrets into the public bus.

## Current active order (as of bus NEXT)

See live file: https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/orders/NEXT.md
