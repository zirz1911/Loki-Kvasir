# Lesson Learned — Statusline + Voice Autostart on Windows

**Date**: 2026-02-18
**Session**: statusline-voice-autostart
**Source**: rrr

---

## Pattern 1: Windows environment — use Python, not bash/Unix tools

`jq`, `sed`, `awk` are not available in Windows Git Bash by default. Whenever a script needs JSON parsing or Unicode output in a Windows environment, use Python directly.

```python
# Wrong: bash + jq
input=$(cat) | jq '.model.display_name'

# Right: pure Python
import sys, json
data = json.loads(sys.stdin.read())
model = (data.get("model") or {}).get("display_name", "")
```

**Applies to**: Any script that runs as a Claude Code hook, statusline command, or shell automation on Windows.

---

## Pattern 2: Windows stdout encoding — reconfigure before Unicode print

Python on Windows defaults to `cp874` (or system codepage), which cannot encode Elder Futhark runes or other non-ASCII Unicode. Fix immediately:

```python
import sys
sys.stdout.reconfigure(encoding="utf-8")
```

Insert this line after imports, before any `print()` that uses Unicode characters. Required for: statusline scripts, voice hooks, any Python running via Claude Code commands on Windows.

---

## Pattern 3: Claude Code statusline — available JSON fields

The statusline command receives a JSON object via stdin. Useful fields confirmed working:

```python
data = json.loads(sys.stdin.read())

cwd       = data.get("cwd") or (data.get("workspace") or {}).get("current_dir", "")
model     = (data.get("model") or {}).get("display_name", "")
used_pct  = (data.get("context_window") or {}).get("used_percentage")     # 0-100
tok_in    = (data.get("context_window") or {}).get("total_input_tokens", 0)
tok_out   = (data.get("context_window") or {}).get("total_output_tokens", 0)
cost_usd  = (data.get("cost") or {}).get("total_cost_usd")                # float
agent     = (data.get("agent") or {}).get("name", "")                     # "" = main Odin
vim_mode  = (data.get("vim") or {}).get("mode", "")
```

**Note**: Use `or {}` guards everywhere — fields may be `None` not just missing.

---

## Pattern 4: Claude Code settings — Windows path format

In `settings.local.json` (hooks, statusLine command), use:
- **Forward slashes** for `statusLine.command` paths: `"python3 D:/Loki-Oracle/..."` ✓
- **Backslashes (escaped)** for hook `command` values: `"python3 D:\\Loki-Oracle\\..."` ✓

The statusLine command works with forward slashes. Hooks work with both but escaped backslashes are more reliable.

---

## Pattern 5: Exit code 1 from bash tool ≠ script failure

Claude Code's bash tool can report exit code 1 even when the script ran correctly and produced correct output. When debugging scripts via bash tool:
- Trust the **output content** over the exit code
- Use `python3 path/to/script.py` directly instead of bash wrappers
- Verify via `echo "EXIT:$?"` only if absolutely necessary, and even then treat with skepticism

---

## Pattern 6: Claude Code hooks — SessionStart for auto-start

To auto-start a background process when Claude Code launches:

```json
"hooks": {
  "SessionStart": [{
    "hooks": [{
      "type": "command",
      "command": "python3 D:\\path\\to\\start_script.py",
      "async": true
    }]
  }]
}
```

The `async: true` is critical — otherwise Claude Code waits for the process to exit before starting the session. The start script should check if the service is already running before launching.

```python
def is_running() -> bool:
    try:
        requests.get("http://127.0.0.1:PORT/status", timeout=2)
        return True
    except Exception:
        return False

if not is_running():
    start_process()
```
