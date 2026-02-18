#!/usr/bin/env python3
"""
Voice Hook — PostToolUse
Fires after query_thor / query_loki / query_heimdall completes
Sends first sentence to Oracle Voice Tray (http://127.0.0.1:37779)
"""

import json
import sys
import re
import requests

VOICE_URL = "http://127.0.0.1:37779/speak"
MAX_CHARS = 200

AGENTS = {
    "mcp__norse-local-llm__query_thor":     {"name": "Thor",     "voice": "Microsoft David Desktop"},
    "mcp__norse-local-llm__query_loki":     {"name": "Loki",     "voice": "Microsoft Zira Desktop"},
    "mcp__norse-local-llm__query_heimdall": {"name": "Heimdall", "voice": "Microsoft Zira Desktop"},
}


def extract_text(tool_response) -> str:
    """Extract plain text from MCP tool_response"""
    # MCP response: {"content": [{"type": "text", "text": "..."}]}
    if isinstance(tool_response, dict):
        content = tool_response.get("content", [])
        if content and isinstance(content, list):
            text = content[0].get("text", "")
        else:
            text = str(tool_response)
    else:
        text = str(tool_response)

    # Strip the "⚡ Thor [model]:\n\n" header line
    lines = text.strip().splitlines()
    body_lines = [l for l in lines if l.strip() and not l.startswith(("⚡", "🔮", "🌈"))]
    text = " ".join(body_lines)

    # Strip markdown code blocks
    text = re.sub(r"```[\s\S]*?```", "code block", text)
    text = re.sub(r"`[^`]+`", "", text)

    # Take first sentence (up to MAX_CHARS)
    sentence_end = re.search(r"[.!?]", text[:MAX_CHARS])
    if sentence_end:
        text = text[:sentence_end.start() + 1]
    else:
        text = text[:MAX_CHARS]

    return text.strip()


def main():
    try:
        payload = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool_name = payload.get("tool_name", "")
    agent_info = AGENTS.get(tool_name)

    if not agent_info:
        sys.exit(0)

    tool_response = payload.get("tool_response", {})
    text = extract_text(tool_response)

    if not text:
        sys.exit(0)

    try:
        requests.post(VOICE_URL, json={
            "text": text,
            "voice": agent_info["voice"],
            "agent": agent_info["name"],
        }, timeout=2)
    except Exception:
        pass  # Voice tray not running — silent fail

    sys.exit(0)


if __name__ == "__main__":
    main()
