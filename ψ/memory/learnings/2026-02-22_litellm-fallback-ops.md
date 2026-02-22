# LiteLLM Fallback — Ops Lessons

**Date**: 2026-02-22
**Source**: Fallback test session (Ollama kill → Anthropic auto-fallback)

---

## 1. LiteLLM proxy must be restarted after config changes

LiteLLM loads config at startup only — no hot-reload.
If fallback entries are added to YAML after proxy is already running, they are silently ignored.

**Workflow**:
```powershell
# 1. Edit config
notepad ~\.claude\litellm_config.yaml
# 2. Kill old proxy
Stop-Process -Id <pid> -Force
# 3. Restart
powershell -ExecutionPolicy Bypass -File ~\.claude\start-litellm.ps1
```

---

## 2. ANTHROPIC_API_KEY must be in proxy process environment

`api_key: os.environ/ANTHROPIC_API_KEY` in config reads from the **proxy's** environment.
If the key isn't set when the proxy starts, fallback fails with `Available Model Group Fallbacks=None`.

**Fix in start-litellm.ps1**:
```powershell
$env:ANTHROPIC_API_KEY = (Get-Content '~\.claude\api_key' -Raw).Trim()
```

---

## 3. Ollama on Windows has a watchdog tray app

`ollama app.exe` (system tray) monitors and auto-restarts `ollama.exe` when killed.
Killing only the server process is ineffective — it restarts within seconds.

**To fully stop Ollama**:
```powershell
# kill-ollama.ps1
$procs = Get-Process | Where-Object { $_.Path -like '*Ollama*' -or $_.Name -like '*ollama*' }
$procs | Stop-Process -Force
```

**To restart**:
```powershell
Start-Process 'C:\Users\pajipan\AppData\Local\Programs\Ollama\ollama app.exe'
```

---

## 4. Verified fallback behavior (2026-02-22)

```
Ollama DOWN → LiteLLM tries ollama/qwen2.5-coder:7b → ConnectionRefused
           → auto-fallback → claude-haiku-4-5-20251001 (real Anthropic)
           → response: {"type":"message","model":"claude-haiku-4-5-20251001",...}
```

Response from fallback includes `service_tier: standard` and `cache_creation_input_tokens`
— proof it went to real Anthropic API, not local.

**Tags**: `litellm`, `fallback`, `ollama`, `windows`, `ops`
