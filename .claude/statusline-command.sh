#!/usr/bin/env bash
# Loki Oracle — Status Line (Windows-compatible, no jq needed)
input=$(cat)
python3 - "$input" <<'PYEOF'
import sys, json, time
sys.stdout.reconfigure(encoding="utf-8")

try:
    data = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
except:
    data = {}

# Extract fields
cwd     = data.get("cwd") or data.get("workspace", {}).get("current_dir", "")
model   = data.get("model", {}).get("display_name", "") if isinstance(data.get("model"), dict) else str(data.get("model", ""))
used    = data.get("context_window", {}).get("used_percentage")
vim_mode= data.get("vim", {}).get("mode", "")

# ANSI colors
RST="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
CYN="\033[36m"; GLD="\033[33m"; GRN="\033[32m"
YLW="\033[33m"; RED="\033[31m"; MAG="\033[35m"; BLU="\033[34m"

# Rune (cycles per second)
RUNES = "ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊᛏᛒᛖᛗᛚᛜᛞᛟ"
rune = RUNES[int(time.time()) % len(RUNES)]

# Shorten cwd
parts = cwd.replace("\\", "/").rstrip("/").split("/")
short = "/".join(parts[-2:]) if len(parts) >= 2 else (parts[-1] if parts else "")

# Context bar
if used is not None:
    u = int(float(used))
    bar = "█" * (u // 10) + "░" * (10 - u // 10)
    col = RED if u >= 80 else (YLW if u >= 50 else GRN)
    ctx = f"{col}{bar} {u}%{RST}"
else:
    ctx = f"{DIM}ctx: —{RST}"

# Vim mode
vim = f" {GRN}[INSERT]{RST}" if vim_mode == "INSERT" else (f" {GLD}[NORMAL]{RST}" if vim_mode else "")

# Output
print(f"{GLD}{rune}{RST} {BOLD}{CYN}Loki{RST} {DIM}|{RST} {MAG}{short}{RST} {DIM}|{RST} {BLU}{model}{RST} {DIM}|{RST} {ctx}{vim}")
PYEOF
