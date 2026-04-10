# Lesson: Claude Code settings.local.json is NOT Auto-Ignored

**Date**: 2026-02-20
**Source**: rrr: gitignore-settings-local

## Pattern

Unlike many frameworks (Next.js `.env.local`, etc.), Claude Code does NOT auto-generate a `.gitignore` for `settings.local.json`. If you `git init` a Claude Code project, `settings.local.json` will be tracked and pushed to GitHub by default.

## What settings.local.json contains

- `permissions.allow` — machine-specific tool permissions
- `hooks` — local file paths to hook scripts
- `enabledMcpjsonServers` — MCP server config
- `statusLine.command` — local script path

None of these are secrets, but all are machine-specific. They don't belong in a shared repo.

## Solution

Always add to `.gitignore` when starting a Claude Code project:

```gitignore
# Local machine settings
.claude/settings.local.json
.claude/todos.json
```

## What TO track

- `.claude/statusline.py` — reusable script, worth sharing
- `.claude/subagent_tracker.py` — reusable hook script
- `.claude/agents/*.md` — agent definitions (reusable)
- `.claude/commands/*.md` — custom commands (reusable)

## Recovery Pattern

If already tracked and pushed:
```bash
git rm --cached .claude/settings.local.json
# then add to .gitignore and commit
```

File stays on disk, stops appearing in future commits.
