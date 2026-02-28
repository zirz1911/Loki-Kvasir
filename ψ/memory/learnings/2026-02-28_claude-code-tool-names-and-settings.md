# Lesson: Claude Code Tool Names + settings.json Side Effects

**Date**: 2026-02-28
**Source**: oracle-voice-tray watcher + hooks implementation

---

## 1. Tool Names Are Implementation Details (v2.1.63)

| Tool | JSONL `name` field |
|------|-------------------|
| Subagent spawn | `"Agent"` ← NOT "Task" |
| File edit | `"Edit"` |
| Shell command | `"Bash"` |
| File read | `"Read"` |

Always verify tool names by inspecting actual JSONL before writing code that parses them.
Search: `grep -r '"name":"X"' ~/.claude/projects/**/*.jsonl`

## 2. `~/.claude/settings.json` Affects Claude Code Directly

Keys in this file are NOT just metadata for third-party tools — they change Claude Code's behavior:

| Key | Effect |
|-----|--------|
| `skipDangerousModePermissionPrompt: true` | Claude Code skips ALL permission prompts (dangerous!) |
| `hooks.PreToolUse` | Runs shell commands before tool execution |

**Never set `skipDangerousModePermissionPrompt: true`** without explicit user consent — it disables all approval prompts globally.

## 3. PreToolUse Hook > Timer for Approval Detection

Timer-based approach (detect tool_use → wait Ns → if no tool_result → alert) **cannot** distinguish:
- Tool waiting for approval (blocked)
- Tool already approved but running slowly

**Only reliable approach**: `PreToolUse` hook fires once, before the approval prompt appears, with zero false positives from slow tools.

Hook config in `~/.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit|Write|MultiEdit|NotebookEdit",
        "hooks": [{"type": "command", "command": "...notify-approval.ps1..."}]
      }
    ]
  }
}
```

## 4. oracle-voice-tray Push Rules

- `paji` remote → `zirz1911/Oracle-voice-paji` ✓
- `origin` remote → `Soul-Brews-Studio/oracle-voice-tray` ✗ (403 — org token required)
- **Never push to origin**
