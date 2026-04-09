#!/usr/bin/env bash
# Loki Kvasir — Machine Setup
# Creates .claude/settings.local.json AND .mcp.json with correct absolute paths.
# Safe to run multiple times — merges with existing config.
#
# Usage:
#   bash .claude/setup.sh              # auto-detect everything
#   bash .claude/setup.sh --no-voice   # skip voice tray hooks

set -euo pipefail

NO_VOICE=false
for arg in "$@"; do
  [[ "$arg" == "--no-voice" ]] && NO_VOICE=true
done

# Detect repo root from this script's location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Detect platform
IS_WSL=false
IS_WINDOWS=false
IS_LINUX=false

if grep -qi microsoft /proc/version 2>/dev/null; then
    IS_WSL=true
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    IS_WINDOWS=true
else
    IS_LINUX=true
fi

# Voice tray only works on Windows (native or Git Bash)
# WSL can ping the tray if it's running on Windows host, but can't start it
VOICE_AVAILABLE=false
if $IS_WINDOWS; then
    VOICE_AVAILABLE=true
fi

if $NO_VOICE; then
    VOICE_AVAILABLE=false
fi

# Determine Ollama host
if $IS_WSL; then
    WIN_HOST=$(grep nameserver /etc/resolv.conf 2>/dev/null | awk '{print $2}' | head -1)
    [[ -z "$WIN_HOST" ]] && WIN_HOST="localhost"
    OLLAMA_HOST="http://${WIN_HOST}:11434"
    ENV_LABEL="WSL → Windows host ($WIN_HOST)"
else
    OLLAMA_HOST="http://localhost:11434"
    ENV_LABEL="Windows/Linux native"
fi

echo "🔧 Loki Kvasir — Setup"
echo "   Repo:        $REPO_ROOT"
echo "   Environment: $ENV_LABEL"
echo "   Ollama:      $OLLAMA_HOST"
echo "   Voice Tray:  $($VOICE_AVAILABLE && echo 'enabled' || echo 'skipped (Windows only)')"
echo ""

# ── 1. Python deps ───────────────────────────────────────────────────────────

echo "📦 Python dependencies..."
python3 -m pip install --quiet requests 2>/dev/null && echo "  ✓ requests" || echo "  ⚠ pip install requests failed — voice features may not work"
echo ""

# ── 2. settings.local.json ──────────────────────────────────────────────────

echo "⚙️  settings.local.json..."

SETTINGS_OUT="$REPO_ROOT/.claude/settings.local.json"

python3 - <<PYEOF
import json, os, sys

repo        = "$REPO_ROOT"
output      = "$SETTINGS_OUT"
voice_avail = "$VOICE_AVAILABLE" == "true"
repo_fwd    = repo.replace("\\\\", "/")

statusline_cmd  = f"python3 {repo_fwd}/.claude/statusline.py"
tracker_cmd     = f"python3 {repo_fwd}/.claude/subagent_tracker.py"
voice_hook_cmd  = f"python3 {repo_fwd}/mcp-local-llm/voice_hook.py"
voice_start_cmd = f"python3 {repo_fwd}/mcp-local-llm/start_voice_tray.py"

NORSE_MATCHER = "Task|mcp__norse-local-llm__query_thor|mcp__norse-local-llm__query_loki|mcp__norse-local-llm__query_heimdall"
VOICE_MATCHER = "mcp__norse-local-llm__query_thor|mcp__norse-local-llm__query_loki|mcp__norse-local-llm__query_heimdall"

existing = {}
if os.path.exists(output):
    try:
        with open(output, "r", encoding="utf-8") as f:
            existing = json.load(f)
        print(f"  merging with existing settings.local.json...")
    except Exception as e:
        print(f"  Warning: could not parse existing ({e}) — overwriting")

# PostToolUse hooks: always tracker, voice if available
post_norse_hooks = [{"type": "command", "command": tracker_cmd}]
if voice_avail:
    post_norse_hooks.insert(0, {"type": "command", "command": voice_hook_cmd, "async": True})

hooks = {
    "PreToolUse": [
        {
            "matcher": NORSE_MATCHER,
            "hooks": [{"type": "command", "command": tracker_cmd}]
        }
    ],
    "PostToolUse": [
        {
            "matcher": VOICE_MATCHER if voice_avail else NORSE_MATCHER,
            "hooks": post_norse_hooks
        },
        {
            "matcher": "Task",
            "hooks": [{"type": "command", "command": tracker_cmd}]
        }
    ]
}

if voice_avail:
    hooks["SessionStart"] = [
        {
            "hooks": [
                {"type": "command", "command": voice_start_cmd, "async": True}
            ]
        }
    ]

new_config = {
    "statusLine": {"type": "command", "command": statusline_cmd},
    "hooks": hooks
}

merged = {**existing, **new_config}

with open(output, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"  ✓ statusLine    → {statusline_cmd}")
print(f"  ✓ tracker hooks → {tracker_cmd}")
if voice_avail:
    print(f"  ✓ voice hook    → {voice_hook_cmd}")
    print(f"  ✓ voice start   → {voice_start_cmd} (SessionStart)")
else:
    print(f"  — voice tray    skipped")
PYEOF

echo ""

# ── 3. .mcp.json ─────────────────────────────────────────────────────────────

echo "🔌 .mcp.json (Norse MCP server)..."

MCP_OUT="$REPO_ROOT/.mcp.json"

python3 - <<PYEOF
import json, os

repo        = "$REPO_ROOT"
output      = "$MCP_OUT"
ollama_host = "$OLLAMA_HOST"
repo_fwd    = repo.replace("\\\\", "/")

mcp_config = {
    "mcpServers": {
        "norse-local-llm": {
            "type": "stdio",
            "command": "python3",
            "args": [f"{repo_fwd}/mcp-local-llm/server.py"],
            "env": {"OLLAMA_HOST": ollama_host}
        }
    }
}

with open(output, "w", encoding="utf-8") as f:
    json.dump(mcp_config, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"  ✓ norse-local-llm → {repo_fwd}/mcp-local-llm/server.py")
print(f"  ✓ OLLAMA_HOST     → {ollama_host}")
PYEOF

echo ""

# ── 4. Voice tray reminder (Windows only) ───────────────────────────────────

if $VOICE_AVAILABLE; then
    echo "🔊 Voice Tray check..."
    if curl -s --max-time 2 http://127.0.0.1:37779/status > /dev/null 2>&1; then
        echo "  ✓ kvasir-voice-tray already running"
    else
        echo "  ⚠ kvasir-voice-tray not running"
        echo "    → Start manually: cd D:\\kvasir-voice-tray && npm run tauri dev"
        echo "    → Or let SessionStart hook auto-launch it when Claude Code starts"
    fi
    echo ""
fi

echo "✅ Setup complete. Restart Claude Code to apply."
