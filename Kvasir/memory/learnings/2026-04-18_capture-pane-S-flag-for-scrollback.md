---
name: tmux capture-pane needs -S flag for scrollback history
description: capture-pane without -S only returns the current visible area; -S -N is required to include N lines of scrollback history
type: feedback
---

`tmux capture-pane -p -e -t target` returns ONLY the current visible terminal area (~20-40 rows depending on pane height). To include scrollback history, you MUST add `-S -N` (e.g., `-S -500` for 500 lines of history).

**Why:** In Loki-Pixfice's pty.ts, `startCaptureLoop` was calling capture-pane without `-S`. The server.ts `capture()` function correctly uses `-S -${lines}`, but it's only called via the `/ws` endpoint — not `/ws/pty`. The CapturePane frontend connects to `/ws/pty` and sends `capture-subscribe`, which goes to pty.ts. So the correct flag was never being used for the actual terminal display.

**How to apply:** Any time terminal scrollback history is needed via `tmux capture-pane`, always check for the `-S -N` flag. Default (no `-S`) = visible area only = ~20-40 rows. Also: when debugging "only N lines showing", check WHICH code path is actually running — there may be multiple capture implementations in the same project serving different endpoints.
