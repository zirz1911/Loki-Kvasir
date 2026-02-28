# Lesson: Claude Code Settings Hierarchy

**Date**: 2026-02-28
**Source**: statusline debug session

---

## Priority Order (High → Low)

```
Enterprise/managed settings
    ↓
settings.local.json  (project-local, NOT tracked in git — highest project-level)
    ↓
settings.json        (project, tracked in git)
    ↓
~/.claude/settings.json  (user-level — lowest)
```

## Practical Impact

When `settings.local.json` defines `statusLine`, `hooks`, or `permissions`, the user-level `~/.claude/settings.json` equivalents are **completely overridden** — not merged for some keys (e.g., statusLine is winner-takes-all).

## Rule

**Before adding/modifying any Claude Code config, always check:**
1. Does `settings.local.json` exist in the project?
2. Does it already define the key you're about to set?
3. If yes → modify THAT file, not the user-level one.

## Where MCP Config Lives

Project-level MCP servers are NOT in settings files — they live in:
```
C:/Users/<user>/.claude.json → projects["<project-path>"].mcpServers
```

This is Claude Code's main data store. Edit with Python/jq, not by hand.
