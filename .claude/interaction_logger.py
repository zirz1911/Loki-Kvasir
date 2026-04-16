#!/usr/bin/env python3
"""
ARIA-style Interaction Logger for Loki-Kvasir

Hook payload format (actual Claude Code):
  {
    "session_id": "...",
    "transcript_path": "...",
    "cwd": "/home/paji/Loki-Kvasir",
    "hook_event_name": "UserPromptSubmit",
    "prompt": "user's actual message"   ← only in UserPromptSubmit
  }

Output: Kvasir/memory/logs/interactions/YYYY-MM-DD.jsonl
"""
import sys, json, os
from datetime import datetime, timezone, timedelta
from pathlib import Path

BKK = timezone(timedelta(hours=7))
LOGS_DIR = Path("/home/paji/Loki-Kvasir/Kvasir/memory/logs/interactions")

try:
    data = json.loads(sys.stdin.read())
except Exception:
    data = {}

event = data.get("hook_event_name", sys.argv[1] if len(sys.argv) > 1 else "")
if event not in ("UserPromptSubmit", "Stop"):
    sys.exit(0)

cwd = data.get("cwd", "")
project = os.path.basename(cwd.rstrip("/")) if cwd else "loki-kvasir"
session = data.get("session_id", "")[:8]
now = datetime.now(BKK)

if event == "UserPromptSubmit":
    prompt = data.get("prompt", "")
    record = {
        "ts": now.isoformat(),
        "event": "prompt",
        "project": project,
        "session": session,
        "prompt": prompt[:300],
        "prompt_len": len(prompt),
    }
elif event == "Stop":
    record = {
        "ts": now.isoformat(),
        "event": "stop",
        "project": project,
        "session": session,
        "reason": data.get("stop_reason", ""),
    }

LOGS_DIR.mkdir(parents=True, exist_ok=True)
today = now.strftime("%Y-%m-%d")
with open(LOGS_DIR / f"{today}.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")
