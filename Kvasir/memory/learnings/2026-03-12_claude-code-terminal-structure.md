# Claude Code Terminal Structure — For Busy Detection

**Date**: 2026-03-12
**Context**: Loki-Pixfice poll-based busy detection in useSessions.ts

## Terminal Layout (24-line pane)

When Claude Code is thinking/working, the visible terminal looks like:

```
[conversation content / tool output]
● ToolName(args...)         ← tool call header
  ⎿  Running…               ← tool running indicator
[blank]
✽ Actioning… (5s · ↓ 123 tokens · thinking)   ← spinner (varies)
  ⎿  Tip: ...               ← tip text (optional)
[blank]
─────────────────────── ▪▪▪ ─   ← separator
❯                               ← prompt (always visible!)
────────────────────────────────  ← separator
  ᚹ Name │ project │ model │ ctx  ← status bar
  ⏵⏵ bypass permissions on...    ← bypass line
```

**Status bar always takes ~4-5 lines at bottom.**
Spinner appears ~6-10 lines from bottom.

## Reliable Detection Patterns

### Strong signals (prefer these):
- `● \w+\(` — tool call in progress (most reliable)
- `\b(Read|Edit|Write|Bash|Grep|Glob|Agent)\b` — specific tool names
- `⎿  Running…` — tool currently executing

### Fragile (avoid relying on alone):
- Spinner chars: `✽✸✶✻✢` — Claude rotates many Unicode star chars
- Thinking words: Spelunking/Billowing/Actioning/Drizzling/etc — not stable

### Better text pattern:
```typescript
/\(\d+s [·↓]/.test(bottom15)  // matches duration format: "(5s ·" or "(1m ↓"
```
This matches the duration indicator that appears with any thinking word.

## Key Facts
- `❯` prompt is ALWAYS visible even when busy → `hasPrompt` must not override `hasBusySign`
- Use `bottom15` (not bottom5) to clear the status bar
- `bottom5` only captures: bypass line, status bar, two separators, `❯` — never catches the spinner
