---
pattern: Global Claude settings silently override project config for anything not explicitly set locally
concepts: [settings, statusline, configuration, global-vs-local, claude-code]
source: "wrap: Loki-Kvasir — gpu-removal-agent-cleanup"
date: 2026-04-16
---

# Global Settings Shadow Project Config

## The Pattern

Claude Code loads both `~/.claude/settings.json` (global) and `.claude/settings.local.json` (project). When the global sets something (like `statusLine`) and the project doesn't, the global wins — silently.

Freyr-Kvasir was showing `🦉 Athena` on its statusline because the global `~/.claude/settings.json` had `statusLine` hardcoded with Athena's name. Freyr had no local override, so it inherited Athena.

## The Fix

Always add an explicit `statusLine` (or any config the project needs to own) to `.claude/settings.local.json`. Don't rely on absence meaning "use default."

## Where to Check

When something behaves wrong and you can't find the cause in project config:
1. `cat ~/.claude/settings.json` — check global settings
2. `cat ~/.claude/settings.local.json` — check global local overrides
3. Look for statusLine, hooks, permissions in both layers

## Applies To

- `statusLine` — identity display
- `hooks` — same hook can fire twice if added to both global + project (duplicate = both fire)
- `permissions.allow` — global + project both contribute (additive, not override)
