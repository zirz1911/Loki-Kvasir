#!/usr/bin/env python3
"""
MCP Server — Norse Local LLM
ให้ Claude Code (Odin) เรียกใช้ Ollama models เป็น tool โดยตรง

Tools:
  query_thor      → qwen2.5-coder:32b  (code generation)
  query_loki      → qwen2.5-coder:7b   (search & patterns)
  query_heimdall  → qwen2.5:7b         (research & docs)

Endpoint: Ollama OpenAI-compatible API (localhost:11434)
"""

import json
import sys
import os
import requests

OLLAMA_BASE = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_URL = f"{OLLAMA_BASE}/v1/chat/completions"

MODELS = {
    "thor":     "qwen2.5-coder:32b",
    "loki":     "qwen2.5-coder:7b",
    "heimdall": "qwen2.5:7b",
}


def query_ollama(agent: str, prompt: str, system: str = None, max_tokens: int = 1000) -> str:
    model = MODELS[agent]
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": model, "messages": messages, "max_tokens": max_tokens, "stream": False},
            timeout=300,
        )
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error calling Ollama ({model}): {str(e)}"


def handle_list_tools():
    return {
        "tools": [
            {
                "name": "query_thor",
                "description": "Thor ⚡ — Code generation via qwen2.5-coder:32b (FREE, local). Use for: writing functions, generating tests, boilerplate, refactoring, algorithms. Faster and free vs Claude API.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Code task or question"},
                        "system": {"type": "string", "description": "Optional system prompt"},
                        "max_tokens": {"type": "number", "description": "Max tokens (default 1000)"},
                    },
                    "required": ["prompt"],
                },
            },
            {
                "name": "query_loki",
                "description": "Loki 🔮 — Pattern search via qwen2.5-coder:7b (FREE, local). Use for: analyzing code patterns, understanding file structures, quick code questions, pattern matching.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Search or pattern question"},
                        "system": {"type": "string", "description": "Optional system prompt"},
                        "max_tokens": {"type": "number", "description": "Max tokens (default 1000)"},
                    },
                    "required": ["prompt"],
                },
            },
            {
                "name": "query_heimdall",
                "description": "Heimdall 🌈 — Research via qwen2.5:7b (FREE, local). Use for: explaining concepts, summarizing docs, research questions, understanding how things work.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Research question or topic"},
                        "system": {"type": "string", "description": "Optional system prompt"},
                        "max_tokens": {"type": "number", "description": "Max tokens (default 1000)"},
                    },
                    "required": ["prompt"],
                },
            },
        ]
    }


def handle_call_tool(tool_name: str, arguments: dict) -> dict:
    agent_map = {"query_thor": "thor", "query_loki": "loki", "query_heimdall": "heimdall"}
    agent_icons = {"thor": "⚡ Thor", "loki": "🔮 Loki", "heimdall": "🌈 Heimdall"}

    if tool_name not in agent_map:
        return {"content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}]}

    agent = agent_map[tool_name]
    prompt = arguments.get("prompt", "")
    system = arguments.get("system")
    max_tokens = arguments.get("max_tokens", 1000)

    result = query_ollama(agent, prompt, system, max_tokens)
    icon = agent_icons[agent]
    model = MODELS[agent]

    return {
        "content": [
            {
                "type": "text",
                "text": f"{icon} [{model}]:\n\n{result}",
            }
        ]
    }


def main():
    """MCP Server — JSON-RPC loop via stdin/stdout"""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")

            if method == "initialize":
                result = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "norse-local-llm", "version": "1.0.0"},
                }
            elif method == "tools/list":
                result = handle_list_tools()
            elif method == "tools/call":
                result = handle_call_tool(params.get("name"), params.get("arguments", {}))
            else:
                result = {"error": f"Unknown method: {method}"}

            print(json.dumps({"jsonrpc": "2.0", "id": request_id, "result": result}), flush=True)

        except Exception as e:
            error_resp = {
                "jsonrpc": "2.0",
                "id": request.get("id") if "request" in locals() else None,
                "error": {"code": -32603, "message": str(e)},
            }
            print(json.dumps(error_resp), flush=True)


if __name__ == "__main__":
    main()
