# Learning: Statusline Usage Fix — Keychain + SSL

**Date**: 2026-03-07
**Source**: Bug fix session, statusline not showing usage quota

## Root Causes

### 1. Background subprocess script didn't have Keychain fallback
`_refresh_usage_bg()` embeds Python code as a string. The main script's `_get_token()` had Keychain support (added 2026-03-01), but the embedded string was never updated — it only tried the credentials file. On macOS where Claude Code stores credentials in Keychain, the background fetch always failed silently.

**Fix**: Replicate the full Keychain fallback logic inside the embedded script.

### 2. Python 3.14 on macOS has no root CA bundle
`ssl.create_default_context()` looks for `/Library/Frameworks/Python.framework/Versions/3.14/etc/openssl/cert.pem` which doesn't exist. Result: `CERTIFICATE_VERIFY_FAILED` on any HTTPS call.

**Fix**: Use `certifi.where()` as the CA file:
```python
try:
    import certifi
    ctx = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    ctx = ssl.create_default_context()
```

## Patterns to Watch

- **Embedded script strings drift** — when you fix logic in the outer script, always check if the same logic exists in any `subprocess.Popen([sys.executable, "-c", script])` embedded strings
- **Silent background failures** — `except Exception: pass` in background processes means debugging requires manual isolation; consider writing a failure marker file
- **certifi is always available** if you're in a modern Python environment; prefer it over bare `ssl.create_default_context()` on macOS

## Diagnosis Steps for "usage not showing"

1. Check cache: `ls -la /tmp/claude_usage_cache.json`
2. If missing, run embedded script logic manually in Python REPL
3. Check credentials: `security find-generic-password -s "Claude Code-credentials" -w`
4. Check SSL: `python3 -c "import ssl, urllib.request; urllib.request.urlopen('https://api.anthropic.com')"`
5. If SSL fails → add certifi
