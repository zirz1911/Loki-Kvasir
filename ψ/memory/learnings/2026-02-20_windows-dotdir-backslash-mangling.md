# Lesson: Windows Dot-Dir Backslash Mangling in Hook Commands

**Date**: 2026-02-20
**Source**: rrr: statusline-subagent-tracking

## Pattern

In Claude Code hook `command` fields (and likely CMD invocations generally), backslash paths through dot-prefixed directories get mangled:

```json
"command": "python3 D:\\Loki-Kvasir\\Loki-Kvasir\\.claude\\subagent_tracker.py"
```

The `\\.claude\\` part causes path corruption. Result:
```
D:\Loki-Kvasir\Loki-Kvasir\Loki-KvasirLoki-Kvasir.claudesubagent_tracker.py
```
All components after the dot-dir get concatenated without separators → file not found error.

## Solution

**Always use forward slashes when path contains a dot-prefixed directory:**

```json
"command": "python3 D:/Loki-Kvasir/Loki-Kvasir/.claude/subagent_tracker.py"
```

Python and Windows both accept forward slashes. No shell interpretation strips them.

## Affected Directories

Any dot-prefixed directory in a backslash path:
- `.claude\` — Claude Code config
- `.git\` — Git internals
- `.next\` — Next.js build
- `.env` — environment files (if in subpath)

## Also Applies To

The `statusLine.command` in settings.local.json already uses forward slashes correctly:
```json
"command": "python3 D:/Loki-Kvasir/Loki-Kvasir/.claude/statusline.py"
```
Follow this pattern for all hook commands involving dot-prefixed paths.

---

## Lesson 2: Hook Async vs Sync Timing

Also learned in this session:

- `"async": true` → hook spawns in background, runs PARALLEL to tool → too late for PreToolUse signals
- No `async` flag (or `"async": false`) → hook runs BEFORE tool continues → correct for timing-sensitive signals

**Rule**: Use synchronous hooks for signals that must precede or follow tool execution precisely. Use async only for fire-and-forget (logging, speech, notifications).
