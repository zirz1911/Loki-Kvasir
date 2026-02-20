#!/usr/bin/env bash
# Loki Oracle — Machine Setup
# Creates .claude/settings.local.json AND .mcp.json with correct absolute paths.
# Safe to run multiple times — merges with existing config.
#
# Usage:
#   bash .claude/setup.sh

set -euo pipefail

# Detect repo root from this script's location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Detect environment: WSL or native
IS_WSL=false
if grep -qi microsoft /proc/version 2>/dev/null; then
    IS_WSL=true
fi

# Determine Ollama host
if $IS_WSL; then
    # WSL: Ollama runs on Windows — need Windows host IP
    # Try nameserver from resolv.conf (WSL2 default gateway = Windows host)
    WIN_HOST=$(grep nameserver /etc/resolv.conf 2>/dev/null | awk '{print $2}' | head -1)
    if [[ -z "$WIN_HOST" ]]; then
        WIN_HOST="localhost"
    fi
    OLLAMA_HOST="http://${WIN_HOST}:11434"
    ENV_LABEL="WSL → Windows host ($WIN_HOST)"
else
    OLLAMA_HOST="http://localhost:11434"
    ENV_LABEL="Windows/Linux native"
fi

echo "🔧 Loki Oracle — Setup"
echo "   Repo:        $REPO_ROOT"
echo "   Environment: $ENV_LABEL"
echo "   Ollama:      $OLLAMA_HOST"
echo ""

# ── 1. settings.local.json ──────────────────────────────────────────────────

SETTINGS_OUT="$REPO_ROOT/.claude/settings.local.json"

python3 - <<PYEOF
import json, os

repo = "$REPO_ROOT"
output = "$SETTINGS_OUT"
repo_fwd = repo.replace("\\\\", "/")

statusline_cmd = f"python3 {repo_fwd}/.claude/statusline.py"
tracker_cmd    = f"python3 {repo_fwd}/.claude/subagent_tracker.py"

existing = {}
if os.path.exists(output):
    try:
        with open(output, "r", encoding="utf-8") as f:
            existing = json.load(f)
        print(f"  settings.local.json — merging with existing...")
    except Exception as e:
        print(f"  Warning: could not parse existing settings.local.json ({e}) — overwriting")

new_config = {
    "statusLine": {
        "type": "command",
        "command": statusline_cmd
    },
    "hooks": {
        "PreToolUse": [
            {
                "matcher": "Task|mcp__norse-local-llm__query_thor|mcp__norse-local-llm__query_loki|mcp__norse-local-llm__query_heimdall",
                "hooks": [{"type": "command", "command": tracker_cmd}]
            }
        ],
        "PostToolUse": [
            {
                "matcher": "Task|mcp__norse-local-llm__query_thor|mcp__norse-local-llm__query_loki|mcp__norse-local-llm__query_heimdall",
                "hooks": [{"type": "command", "command": tracker_cmd}]
            }
        ]
    }
}

merged = {**existing, **new_config}

with open(output, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"  ✓ statusLine → {statusline_cmd}")
print(f"  ✓ hooks      → {tracker_cmd}")
PYEOF

# ── 2. .mcp.json ────────────────────────────────────────────────────────────

MCP_OUT="$REPO_ROOT/.mcp.json"

python3 - <<PYEOF
import json, os

repo = "$REPO_ROOT"
output = "$MCP_OUT"
ollama_host = "$OLLAMA_HOST"
repo_fwd = repo.replace("\\\\", "/")

server_path = f"{repo_fwd}/mcp-local-llm/server.py"

mcp_config = {
    "mcpServers": {
        "norse-local-llm": {
            "type": "stdio",
            "command": "python3",
            "args": [server_path],
            "env": {
                "OLLAMA_HOST": ollama_host
            }
        }
    }
}

with open(output, "w", encoding="utf-8") as f:
    json.dump(mcp_config, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"  ✓ MCP server → {server_path}")
print(f"  ✓ OLLAMA_HOST → {ollama_host}")
PYEOF

echo ""
echo "  Restart Claude Code to apply."
