#!/usr/bin/env python3
import sys, json, time, os, tempfile, urllib.request

sys.stdout.reconfigure(encoding="utf-8")

try:
    data = json.loads(sys.stdin.read())
except Exception:
    data = {}

# --- Extract fields ---
cwd          = data.get("cwd") or (data.get("workspace") or {}).get("current_dir", "")
model        = (data.get("model") or {}).get("display_name", "")
used         = (data.get("context_window") or {}).get("used_percentage")
vim_mode     = (data.get("vim") or {}).get("mode", "")
agent        = (data.get("agent") or {}).get("name", "")
agent_type   = (data.get("agent") or {}).get("type", "")
session_name = (data.get("session") or {}).get("name", "") or data.get("session_name", "")
added_dirs   = (data.get("workspace") or {}).get("added_dirs", []) or []

cost_usd  = (data.get("cost") or {}).get("total_cost_usd")
tok_in    = (data.get("context_window") or {}).get("total_input_tokens", 0) or 0
tok_out   = (data.get("context_window") or {}).get("total_output_tokens", 0) or 0
total_tok = tok_in + tok_out

# --- ANSI colors ---
RST  = "\033[0m";  BOLD = "\033[1m";  DIM  = "\033[2m"
CYN  = "\033[36m"; GLD  = "\033[33m"; GRN  = "\033[32m"
YLW  = "\033[93m"; RED  = "\033[31m"; MAG  = "\033[95m"
BLU  = "\033[94m"; WHT  = "\033[97m"; PRP  = "\033[35m"
TEAL = "\033[96m"

SEP = f" {DIM}│{RST} "

# --- Rune (cycles per second) ---
RUNES = "ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊᛏᛒᛖᛗᛚᛜᛞᛟ"
rune = RUNES[int(time.time()) % len(RUNES)]

# --- Shorten cwd ---
parts = cwd.replace("\\", "/").rstrip("/").split("/")
short = "/".join(parts[-2:]) if len(parts) >= 2 else (parts[-1] if parts else "~")

# --- Context bar ---
if used is not None:
    u = int(float(used))
    filled = u // 10
    bar = "█" * filled + "░" * (10 - filled)
    col = RED if u >= 80 else (YLW if u >= 50 else GRN)
    ctx = f"{col}{bar} {u}%{RST}"
else:
    ctx = f"{DIM}ctx: —{RST}"

# --- Tokens ---
if total_tok > 0:
    tok_str = f"{total_tok/1000:.1f}k" if total_tok >= 1000 else str(total_tok)
    tok_display = f"{TEAL}{tok_str} tok{RST}"
else:
    tok_display = f"{DIM}0 tok{RST}"

# --- Cost ---
if cost_usd is not None:
    if cost_usd >= 1.0:
        cost_str, cost_col = f"${cost_usd:.2f}", RED
    elif cost_usd >= 0.1:
        cost_str, cost_col = f"${cost_usd:.3f}", YLW
    else:
        cost_str, cost_col = f"${cost_usd:.4f}", GRN
    cost_display = f"{cost_col}{cost_str}{RST}"
else:
    cost_display = f"{DIM}$—{RST}"

# --- Subscription usage (cached 60s) ---
USAGE_CACHE = os.path.join(tempfile.gettempdir(), "claude_usage_cache.json")
CREDS_FILE  = os.path.expanduser("~/.claude/.credentials.json")

def get_usage():
    # Return (five_hour_pct, seven_day_pct) or (None, None)
    try:
        # Check cache freshness
        if os.path.exists(USAGE_CACHE) and time.time() - os.path.getmtime(USAGE_CACHE) < 60:
            with open(USAGE_CACHE, encoding="utf-8") as f:
                cached = json.load(f)
        else:
            with open(CREDS_FILE, encoding="utf-8") as f:
                token = json.load(f)["claudeAiOauth"]["accessToken"]
            req = urllib.request.Request(
                "https://api.anthropic.com/api/oauth/usage",
                headers={"Authorization": f"Bearer {token}", "anthropic-beta": "oauth-2025-04-20"},
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                cached = json.loads(resp.read())
            with open(USAGE_CACHE, "w", encoding="utf-8") as f:
                json.dump(cached, f)
        fh = cached.get("five_hour") or {}
        sd = cached.get("seven_day") or {}
        return fh.get("utilization"), sd.get("utilization")
    except Exception:
        return None, None

fh_pct, sd_pct = get_usage()

def usage_str(pct, label):
    if pct is None:
        return ""
    p = int(float(pct))
    col = RED if p >= 80 else (YLW if p >= 50 else GRN)
    return f"{col}{label}:{p}%{RST}"

usage_parts = [s for s in [usage_str(fh_pct, "5h"), usage_str(sd_pct, "7d")] if s]
usage_display = SEP + f" {DIM}│{RST} ".join(usage_parts) if usage_parts else ""

# --- Agent ---
AGENT_MAP = {
    "thor":     ("⚡", "Thor"),
    "loki":     ("🔮", "Loki"),
    "heimdall": ("🌈", "Heimdall"),
    "tyr":      ("⚔️", "Tyr"),
    "ymir":     ("🏔️", "Ymir"),
    "odin":     ("👁️", "Odin"),
}

def model_to_icon_name(model_str):
    m = model_str.lower()
    if "haiku" in m: return ("⚡", "Thor")
    if "opus"  in m: return ("🏔️", "Ymir")
    return ("👁️", "Odin")

# Base agent: explicit > agent_type fallback > model inference
if agent:
    icon, name = AGENT_MAP.get(agent.lower(), ("◆", agent))
elif agent_type:
    icon, name = AGENT_MAP.get(agent_type.lower(), ("◆", agent_type))
else:
    icon, name = model_to_icon_name(model)

# Active subagent from temp file (written by subagent_tracker.py hook)
TEMP_AGENT_FILE = os.path.join(tempfile.gettempdir(), "claude_subagent_active.txt")
active_sub = ""
try:
    with open(TEMP_AGENT_FILE, encoding="utf-8") as f:
        active_sub = f.read().strip()
except Exception:
    pass

if active_sub:
    sub_icon, sub_name = AGENT_MAP.get(active_sub.lower(), ("◆", active_sub))
    agent_display = (
        f"{MAG}{BOLD}{icon} {name}{RST}"
        f"{DIM}→{RST}"
        f"{MAG}{BOLD}{sub_icon} {sub_name}{RST}"
    )
else:
    agent_display = f"{MAG}{BOLD}{icon} {name}{RST}"

# --- Vim mode ---
if vim_mode == "INSERT":
    vim = f"{SEP}{GRN}[INSERT]{RST}"
elif vim_mode:
    vim = f"{SEP}{GLD}[{vim_mode}]{RST}"
else:
    vim = ""

# --- Session name & added dirs ---
loki_label = f"Loki [{session_name}]" if session_name else "Loki"
dirs_badge = f" {DIM}+{len(added_dirs)}{RST}" if added_dirs else ""

# --- Assemble ---
line = (
    f"{GLD}{rune}{RST} "
    f"{BOLD}{CYN}{loki_label}{RST}"
    f"{SEP}{YLW}{short}{RST}{dirs_badge}"
    f"{SEP}{BLU}{model}{RST}"
    f"{SEP}{ctx}"
    f"{SEP}{tok_display}"
    f"{SEP}{cost_display}"
    f"{usage_display}"
    f"{SEP}{agent_display}"
    f"{vim}"
)

print(line)
