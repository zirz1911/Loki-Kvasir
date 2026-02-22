# Local LLM on Windows — Lessons from LiteLLM + MCP Setup

**Date**: 2026-02-22
**Source**: LiteLLM proxy + Ollama MCP server installation session

---

## 1. Windows encoding kills LiteLLM in two places

**Problem**: Python uses cp874 (Thai codepage) as default terminal encoding on this machine.
This causes crashes in TWO places when running LiteLLM:
- Reading YAML config → `UnicodeDecodeError` if file has Thai/Unicode characters
- Printing startup banner → `UnicodeEncodeError` (banner has emoji/box-drawing chars)

**Fix**:
- Keep YAML config ASCII-only (no Thai comments)
- Set `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1` before launching LiteLLM
- Must be done via PowerShell script (`$env:PYTHONIOENCODING = 'utf-8'`) — bash can't set Windows env vars reliably

---

## 2. Claude Code MCP registration: `claude mcp add`, not settings.json

**Problem**: Claude Code `settings.json` schema does NOT have `mcpServers` key (unlike Claude Desktop).
Creating `mcp.json` + `enabledMcpjsonServers` in settings.json works for project-scoped `.mcp.json` files but NOT for direct stdio server registration.

**Fix**: Use the CLI:
```powershell
claude mcp add server-name -e KEY=val -- python path/to/server.py
```
This writes to `.claude.json` in the project directory. Requires Claude Code restart to activate.

---

## 3. LiteLLM background process on Windows requires PS1 launcher

**Problem**: Running LiteLLM in background from bash-on-Windows is unreliable:
- `cmd /B` doesn't inherit env vars properly
- `Start-Process` without env setup fails
- Inline `& exe &` uses PowerShell syntax not bash syntax

**Fix**: Create a `.ps1` launcher script that sets env vars and runs the exe directly:
```powershell
$env:PYTHONIOENCODING = 'utf-8'
& 'path\to\litellm.exe' --config config.yaml --port 4000
```
Then run: `powershell -ExecutionPolicy Bypass -File launcher.ps1 &`

---

## 4. MCP server descriptions should use dynamic variables

Hardcoded model names in MCP tool descriptions become stale when env vars change.
Use f-strings so descriptions auto-reflect the configured model:
```python
# Bad
description="Query qwen2.5-coder:7b..."
# Good
description=f"Query {FAST_MODEL}..."
```

---

## 5. compare_models: only works for short-medium prompts

qwen2.5-coder:32b (19GB) takes 60-120s+ for complex prompts.
Running both models in parallel means total timeout = max(7b_time, 32b_time).
For production use: either increase timeout or separate tool calls for 32b.

**Tags**: `windows`, `litellm`, `mcp`, `ollama`, `encoding`, `claude-code`
