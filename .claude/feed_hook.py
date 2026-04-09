#!/usr/bin/env python3
"""
Kvasir Feed Hook — writes Claude Code events to feed.log
Format: TIMESTAMP | ORACLE | HOST | EVENT | PROJECT | SESSION_ID » MESSAGE
"""
import sys, json, os, socket
from datetime import datetime, timezone, timedelta

FEED_LOG = "/tmp/loki-feed.log"
BKK = timezone(timedelta(hours=7))

try:
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}
except Exception:
    data = {}

# Determine kvasir name: ORACLE_NAME env > tmux window name > "loki"
def _tmux_window_name():
    try:
        import subprocess
        pane = os.environ.get("TMUX_PANE", "")
        if pane:
            r = subprocess.run(["tmux", "display-message", "-p", "-t", pane, "#{window_name}"],
                               capture_output=True, text=True, timeout=1)
            name = r.stdout.strip()
            if name:
                return name
    except Exception:
        pass
    return None

kvasir = os.environ.get("ORACLE_NAME") or _tmux_window_name() or "loki"
host = socket.gethostname()

# Extract from hook data
event_type = data.get("event", "")
session_id = data.get("session_id", "")
project = ""
cwd = data.get("cwd", "")
if cwd:
    project = os.path.basename(cwd.rstrip("/"))

# Build message from tool use data if present
message = ""
tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})
tool_response = data.get("tool_response", {})

if event_type == "PreToolUse" and tool_name:
    # Summarize tool input briefly
    if tool_name == "Bash":
        cmd = (tool_input.get("command", "") or "")[:80]
        message = f"{tool_name}: {cmd}"
    elif tool_name in ("Read", "Write", "Edit"):
        fp = tool_input.get("file_path", "")
        if fp:
            message = f"{tool_name}: {os.path.basename(fp)}"
        else:
            message = tool_name
    elif tool_name in ("Grep", "Glob"):
        pat = tool_input.get("pattern", "")
        message = f"{tool_name}: {pat[:60]}" if pat else tool_name
    elif tool_name == "Agent":
        desc = tool_input.get("description", "")
        message = f"{tool_name}: {desc[:60]}" if desc else tool_name
    else:
        message = tool_name

elif event_type == "PostToolUse" and tool_name:
    is_err = bool(data.get("tool_response", {}).get("is_error"))
    message = f"{tool_name} {'✗' if is_err else '✓'}"
    if is_err:
        event_type = "PostToolUseFailure"

elif event_type == "UserPromptSubmit":
    prompt = data.get("prompt", "")
    message = prompt[:100] if prompt else ""

elif event_type == "Stop":
    message = data.get("stop_reason", "")

elif event_type == "Notification":
    message = data.get("message", "")[:100]

# Map hook event names to feed event types
EVENT_MAP = {
    "PreToolUse": "PreToolUse",
    "PostToolUse": "PostToolUse",
    "PostToolUseFailure": "PostToolUseFailure",
    "UserPromptSubmit": "UserPromptSubmit",
    "Stop": "Stop",
    "Notification": "Notification",
}
feed_event = EVENT_MAP.get(event_type, event_type)
if not feed_event:
    sys.exit(0)

timestamp = datetime.now(BKK).strftime("%Y-%m-%d %H:%M:%S")
line = f"{timestamp} | {kvasir} | {host} | {feed_event} | {project} | {session_id} » {message}\n"

try:
    with open(FEED_LOG, "a", encoding="utf-8") as f:
        f.write(line)
except Exception:
    pass
