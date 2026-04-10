---
name: ui-delegation-checklist
description: When delegating UI feature ports to sub-agents, always include explicit integration checklist
type: feedback
---

When delegating UI port or feature implementation to a sub-agent (Tyr/Ymir), explicitly require:

1. CSS imported (e.g. `@xterm/xterm/css/xterm.css` for xterm.js)
2. New component wired into App.tsx with a named route
3. Nav item added to StatusBar (both desktop and mobile hamburger)
4. `bun run build:office` passes

**Why:** Tyr built a working XTerminal and WorktreeView but missed all three integration points. Build passed but UI was broken — black terminal, unreachable route, missing nav item. Required a second commit to fix what should have been in the first.

**How to apply:** Add this checklist as explicit requirements at the end of every Tyr/Ymir prompt for UI work:
```
After implementing, verify:
- All CSS imports are present
- New views are routed in App.tsx
- Nav items exist in StatusBar for new routes
- bun run build:office passes with no errors
```
