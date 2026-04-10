# Local LLM on macOS — Setup Guide

**Date**: 2026-02-25
**Source**: Norse Agent System + MCP Server setup for macOS

---

## Overview

This document describes the macOS version of the Local LLM setup, complementing the existing Windows configuration.

**Differences from Windows**:
- macOS: bash scripts, UTF-8 by default, no encoding issues
- Windows: PowerShell scripts, cp874 encoding problems, requires `PYTHONIOENCODING=utf-8`

---

## Setup Summary

### 1. Prerequisites

- **Ollama**: Already installed (v0.17.0)
- **Models**: qwen2.5-coder:7b (4.7 GB) installed
- **Python**: Python 3.13+ with pip
- **Claude Code**: Latest version

### 2. File Structure

```
~/.claude/
├── litellm_config_macos.yaml       # LiteLLM configuration
├── start-litellm-macos.sh          # Bash launcher (vs .ps1 on Windows)
└── mcp-local-llm-macos/
    ├── server.py                   # MCP server (same logic as Windows)
    ├── install.sh                  # Bash installer (vs .ps1 on Windows)
    └── README.md                   # Documentation
```

### 3. Key Components

#### LiteLLM Config (`litellm_config_macos.yaml`)

Maps Ollama models to Claude API names:
- `claude-haiku-3-5-20241022` → `ollama/qwen2.5-coder:7b`
- `claude-sonnet-3-5-20241022` → `ollama/qwen2.5-coder:32b`
- Fallback: `claude-haiku-real`, `claude-sonnet-real` (real API)

#### Bash Launcher (`start-litellm-macos.sh`)

Starts LiteLLM proxy on port 4000. No encoding issues on macOS (UTF-8 default).

#### MCP Server (`server.py`)

Provides three tools for Claude Code:
- `query_thor` — Code generation (qwen2.5-coder:7b)
- `query_loki` — Pattern search (qwen2.5-coder:7b)
- `query_heimdall` — Research (qwen2.5-coder:7b)

#### Install Script (`install.sh`)

One-shot installer that:
1. Checks Python and Ollama
2. Installs dependencies (mcp, httpx, litellm)
3. Pulls Ollama models
4. Registers MCP server with Claude Code

---

## Installation

### Quick Install

```bash
cd ~/.claude/mcp-local-llm-macos
./install.sh
```

### Manual Install

```bash
# Install Python dependencies
pip3 install mcp httpx litellm

# Pull Ollama models
ollama pull qwen2.5-coder:7b   # Required (4.7 GB)
ollama pull qwen2.5-coder:32b  # Optional (19 GB)

# Register MCP server
claude mcp add norse-local-llm \
    -e FAST_MODEL=qwen2.5-coder:7b \
    -e POWER_MODEL=qwen2.5-coder:32b \
    -e OLLAMA_BASE=http://localhost:11434 \
    -- python3 ~/.claude/mcp-local-llm-macos/server.py

# Restart Claude Code
```

---

## Usage

### 1. Start Ollama (if not running)

```bash
ollama serve
```

### 2. Use MCP Tools in Claude Code

After restart, tools are available:

```python
# Example: Generate code with Thor
query_thor(prompt="Write a function to check if a number is prime")

# Example: Search patterns with Loki
query_loki(prompt="Find all error handling patterns in this codebase")

# Example: Research with Heimdall
query_heimdall(prompt="Explain the architecture of this project")
```

### 3. Optional: Start LiteLLM Proxy

```bash
~/.claude/start-litellm-macos.sh
```

Test:
```bash
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-haiku-3-5-20241022",
    "messages": [{"role": "user", "content": "Say OK"}]
  }'
```

---

## Differences from Windows

| Aspect | Windows | macOS |
|--------|---------|-------|
| **Scripts** | PowerShell (.ps1) | Bash (.sh) |
| **Encoding** | cp874 → requires UTF-8 env vars | UTF-8 by default |
| **Launcher** | `start-litellm.ps1` | `start-litellm-macos.sh` |
| **Execution** | `powershell -File` | Direct `.sh` execution |
| **Directory** | `~/.claude/mcp-local-llm/` | `~/.claude/mcp-local-llm-macos/` |

---

## Norse Agent System Integration

The MCP server provides the backend for Norse agents:

| Agent | Model | Use Case | Cost |
|-------|-------|----------|------|
| **Thor ⚡** | qwen2.5-coder:7b | Code gen, tests, boilerplate | FREE |
| **Loki 🔮** | qwen2.5-coder:7b | Pattern search, file analysis | FREE |
| **Heimdall 🌈** | qwen2.5-coder:7b | Research, documentation | FREE |
| **Tyr ⚔️** | qwen2.5-coder:32b | Complex features, architecture | FREE |
| **Ymir 🏔️** | Claude Opus | Critical production code | PAID |
| **Odin 👁️** | Claude Sonnet | Orchestration | PAID |

**Strategy**: Local models (qwen2.5-coder) handle ~90% of tasks for free. Escalate to Claude API only when needed.

---

## Performance Notes

### qwen2.5-coder:7b
- **Speed**: ~50 tokens/sec (M1/M2 Mac)
- **Quality**: Good for most coding tasks
- **Size**: 4.7 GB

### qwen2.5-coder:32b
- **Speed**: ~15 tokens/sec (M1/M2 Mac)
- **Quality**: Better, especially for complex logic
- **Size**: 19 GB
- **Note**: May timeout on very long prompts (>2000 tokens)

---

## Troubleshooting

### MCP Server Not Showing Up

1. Check registration:
   ```bash
   cat ~/.claude/.claude.json
   ```

2. Check logs:
   ```bash
   tail -f ~/.claude/debug/mcp-*.log
   ```

3. Restart Claude Code

### Ollama Connection Issues

1. Check if Ollama is running:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. Start Ollama:
   ```bash
   ollama serve
   ```

### Model Not Found

Pull the model:
```bash
ollama pull qwen2.5-coder:7b
```

---

## Next Steps

- [ ] Test all three MCP tools (thor, loki, heimdall)
- [ ] Test LiteLLM proxy fallback (kill Ollama → should fallback to Claude API)
- [ ] Add qwen2.5-coder:32b for Tyr agent (optional)
- [ ] Create unified documentation linking Windows and macOS setups

---

**Tags**: `macos`, `ollama`, `mcp`, `litellm`, `norse-agents`, `local-llm`, `claude-code`
