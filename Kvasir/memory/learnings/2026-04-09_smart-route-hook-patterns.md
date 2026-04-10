---
date: 2026-04-09
tags: [smart-route, hooks, token-saving, tmux, gemini]
source: "wrap: Loki-Kvasir"
---

# Smart Route Hook Patterns

## Pattern: UserPromptSubmit hook for auto-routing

`additionalContext` injected via `UserPromptSubmit` hook is the right mechanism for "always-on" behavior without touching CLAUDE.md. The hook runs at system level — I have the routing map before responding.

```json
{
  "type": "command",
  "command": "/path/to/hook.sh",
  "statusMessage": "routing..."
}
```

The script outputs JSON with `hookSpecificOutput.additionalContext`.

## Pattern: Gemini CLI shell mode trap

When Gemini CLI pane is in shell mode (`! prefix`), tmux `send-keys` sends text as shell command, not Gemini prompt. Always Escape first:

```bash
tmux send-keys -t SESSION:WINDOW Escape
sleep 0.5
tmux send-keys -t SESSION:WINDOW "your message" Enter
```

## Pattern: Verify tmux targets before hardcoding

Always run `tmux ls` before writing session:window references into skills or hooks. Sessions don't auto-rename when repos do.

```bash
tmux ls  # check session names
tmux list-windows -t SESSION -F '#{window_index}:#{window_name}'  # check windows
```

## Cost model for hook injection

~50 tokens overhead per message for routing hint. Cost-positive when it successfully routes even 1 in 20 messages to a free agent (Gemini saves ~500+ tokens per substantial message).
