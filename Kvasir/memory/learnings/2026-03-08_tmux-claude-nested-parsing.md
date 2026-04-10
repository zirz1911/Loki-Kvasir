# Lessons: tmux Capture Parsing + Nested Claude Sessions

**Date**: 2026-03-08
**Source**: loki-pixfice-ui-overhaul session

---

## Nested Claude Sessions

Claude Code sets the `CLAUDECODE` env var. Launching `claude` inside a Claude Code session fails with:
> "Claude Code cannot be launched inside another Claude Code session."

**Fix**: `unset CLAUDECODE && claude --dangerously-skip-permissions`

Add this to any tmux setup script that launches Claude agents.

---

## tmux Capture Parsing

### Always Trim Bottom 15%

```ts
const allLines = raw.split('\n');
const cutoff = Math.floor(allLines.length * 0.85);
const content = allLines.slice(0, cutoff).join('\n');
```

Bottom 15% contains: tmux statusline, Claude Code footer (`⏵⏵ bypass permissions`), token counts.

### seenPrompt Pattern

Only parse content **after the first `❯` prompt**. Skips: startup banners, shell commands, ASCII art.

```ts
let seenPrompt = false;
for (const line of lines) {
  if (line.trim().startsWith('❯')) { seenPrompt = true; /* handle */ continue; }
  if (!seenPrompt) continue;
  // ... parse turns
}
```

### `●` Is Ambiguous in Claude Code Output

- `● ToolName(args)` = tool call → classify as `tool`
- `● regular text` = assistant response → classify as `assistant` (strip the `●`)

Pattern to distinguish:
```ts
const isToolCall = /^●\s+\w+\s*\(/.test(trimmed)  // ● Write(path)
  || /^[◆✔✗⎿▶]/.test(trimmed);
```

### Strip `●` from Assistant Text

```ts
if (role === 'assistant') text = text.replace(/^●\s+/, '');
```
