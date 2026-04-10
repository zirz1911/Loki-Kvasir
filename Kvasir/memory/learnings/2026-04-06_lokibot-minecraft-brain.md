# LokiBot — Minecraft Bot with Claude Brain

**Date**: 2026-04-06
**Source**: Session rrr

## Patterns Discovered

### mineflayer Bot Setup (offline mode)
```javascript
const bot = mineflayer.createBot({
  host: 'localhost', port: 25565,
  username: 'LokiBot', auth: 'offline',
  version: '1.21.11'
})
// Requires: online-mode=false in server.properties
// Requires: enforce-secure-profile=false (or client won't see unsigned chat)
```

### Pathfinder Creative Mode Fix
```javascript
const move = new Movements(bot)
move.canDig = false
move.allowFreeMotion = true
move.canFly = true           // ← CRITICAL for creative mode
bot.pathfinder.setMovements(move)
```

### Claude Brain Pattern
- Collect perception (pos, nearby players, recent chat, last action)
- Call `claude-haiku-4-5` with `temperature: 1.0`
- Track `botHistory[]` — last 20 messages bot said
- Include in prompt: "DO NOT REPEAT: [botHistory]"
- Parse JSON response → execute action

### Prevent Bot Repetition
- `temperature: 1.0` + history tracking
- Explicitly list recent messages in prompt and forbid repetition
- Tell Claude to vary action types (not always chat)

### House Builder
- Use `/fill` commands via `bot.chat()`
- Minimum 400ms delay between commands (< 100ms causes server lag)
- 16+ fill commands for a basic 9×5×9 house

## Project Location
`/home/paji/Project/LokiBot/`
- `bot.js` — main bot with command handler + house builder
- `brain.js` — Claude brain perception→think→action loop
