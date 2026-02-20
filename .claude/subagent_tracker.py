#!/usr/bin/env python3
"""
Subagent Tracker — PreToolUse + PostToolUse hook
Writes active subagent name to temp file so statusline.py can show it.

PreToolUse  → writes agent name to temp file
PostToolUse → clears temp file (detects by presence of tool_response key)
"""
import sys, json, os, tempfile

TEMP_AGENT_FILE = os.path.join(tempfile.gettempdir(), "claude_subagent_active.txt")

# MCP Norse tool → agent name
MCP_AGENTS = {
    "mcp__norse-local-llm__query_thor":     "Thor",
    "mcp__norse-local-llm__query_loki":     "Loki",
    "mcp__norse-local-llm__query_heimdall": "Heimdall",
}

# subagent_type → agent name
SUBTYPE_AGENTS = {
    "Explore":         "Heimdall",
    "Plan":            "Tyr",
    "general-purpose": "Thor",
    "Bash":            "Thor",
}

# model keyword → agent name
MODEL_AGENTS = [
    ("haiku", "Thor"),
    ("opus",  "Ymir"),
    ("sonnet", "Tyr"),  # spawned sonnet = Tyr (not Odin)
]


def detect_agent(tool_name, tool_input):
    if tool_name in MCP_AGENTS:
        return MCP_AGENTS[tool_name]
    if tool_name == "Task":
        model = str(tool_input.get("model", "")).lower()
        subtype = tool_input.get("subagent_type", "")
        for keyword, name in MODEL_AGENTS:
            if keyword in model:
                return name
        return SUBTYPE_AGENTS.get(subtype, "Thor")
    return None


def main():
    try:
        payload = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool_name  = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}
    is_post    = "tool_response" in payload  # PostToolUse has tool_response; PreToolUse doesn't

    agent = detect_agent(tool_name, tool_input)
    if not agent:
        sys.exit(0)

    if is_post:
        # Clear active subagent after tool completes
        try:
            os.remove(TEMP_AGENT_FILE)
        except Exception:
            pass
    else:
        # Write active subagent before tool runs
        try:
            with open(TEMP_AGENT_FILE, "w", encoding="utf-8") as f:
                f.write(agent)
        except Exception:
            pass

    sys.exit(0)


if __name__ == "__main__":
    main()
