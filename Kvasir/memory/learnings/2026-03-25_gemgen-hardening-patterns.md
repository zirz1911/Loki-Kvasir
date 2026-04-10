---
name: gemgen-hardening-patterns
description: Security hardening, JSON reliability, and UX patterns from GemGen production review
type: project
---

## GemGen Production Hardening Patterns

**Context**: Full production review of GemGen (Python HTTP server → Claude API → workflow JSON)

### Reliability
- `max_tokens=16000` for complex structured JSON output — 8000 truncates long workflows mid-JSON
- `temperature=0.2` for structured output (JSON, code); `temperature=0.7` only for creative text
- Retry logic (3 attempts) is safety net — fix root cause (token limit) first, add retry second
- Retry order matters: diagnose → fix → then add defensive retry

### Security (Python HTTP server)
- `MAX_BODY_SIZE = 1_000_000` — guard against Content-Length DoS before reading body
- Validate `Content-Length` header exists before `rfile.read(content_length)`
- Use `Path(__file__).parent` for CWD-independent static file serving
- `_send_json()` helper centralizes response format, prevents inconsistency
- Never leak internal error details in 500 responses — log to server, return generic message
- `ThreadingHTTPServer` is drop-in for non-blocking concurrent Python HTTP

### Deployment Context
- Always ask how server is accessed before hardening network bindings
- `0.0.0.0` = correct for Tailscale / LAN access; `127.0.0.1` = only for localhost-only deploy
- "More secure" network binding is architecture-dependent, not universal

### UX
- Progress bar + elapsed timer = makes AI generation feel responsive (hides latency)
- Token cost in success notification = builds trust, shows users real API cost
- `duration` from server-side timing is more accurate than client-side fetch timing

**Why**: Applied during first production review of GemGen after months of use.
**How to apply**: Use these patterns as checklist for any new Python HTTP server serving AI-generated content.
