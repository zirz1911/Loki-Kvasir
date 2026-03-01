# macOS Claude Code — Keychain credentials + Python SSL

**Date**: 2026-03-01
**Source**: statusline usage quota debug session

## Pattern: Claude Code OAuth on macOS

Modern Claude Code (2.1.x+) on macOS stores OAuth credentials in **macOS Keychain**, NOT as a file.

- ❌ `~/.claude/.credentials.json` — only exists on Linux or older versions
- ✅ macOS Keychain: `"Claude Code-credentials"` service

### How to read:

```python
import subprocess, json

result = subprocess.run(
    ["security", "find-generic-password", "-s", "Claude Code-credentials", "-w"],
    capture_output=True, text=True
)
if result.returncode == 0:
    token = json.loads(result.stdout.strip())["claudeAiOauth"]["accessToken"]
```

### Cross-platform helper:

```python
def get_claude_token():
    creds_file = os.path.expanduser("~/.claude/.credentials.json")
    if os.path.exists(creds_file):
        with open(creds_file) as f:
            return json.load(f)["claudeAiOauth"]["accessToken"]
    # macOS Keychain fallback
    import subprocess
    r = subprocess.run(
        ["security", "find-generic-password", "-s", "Claude Code-credentials", "-w"],
        capture_output=True, text=True
    )
    if r.returncode == 0:
        return json.loads(r.stdout.strip())["claudeAiOauth"]["accessToken"]
    raise FileNotFoundError("No Claude credentials found")
```

---

## Pattern: Python 3.14 SSL on macOS

Python 3.14 installed via python.org installer on macOS does NOT have CA bundle configured by default. Must run `/Applications/Python 3.14/Install Certificates.command` OR use explicit SSL context.

### Fix:

```python
import ssl, os

ctx = ssl.create_default_context()
try:
    import certifi
    ctx.load_verify_locations(certifi.where())
except ImportError:
    if os.path.exists("/etc/ssl/cert.pem"):
        ctx.load_verify_locations("/etc/ssl/cert.pem")

# Then pass context= to urlopen
urllib.request.urlopen(req, timeout=3, context=ctx)
```

### Why this happens:
Python.org macOS installer does not auto-install certificates. The `Install Certificates.command` script must be run manually. Most people forget this step.

---

## Tags
`macos`, `claude-code`, `oauth`, `keychain`, `python-ssl`, `statusline`
