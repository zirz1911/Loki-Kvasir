# /openclaw-dashboard — Openclaw Status Dashboard

Check the live status of all 3 Openclaw instances from this session.

Usage: `/openclaw-dashboard`

## Instances

| Session | Bot | User | Token |
|---------|-----|------|-------|
| `claude30` | `@conclaw30bot` | root | gateway auth token (local) |
| `claude28` | `@conclaw28bot` | paji | `b636eca573bad0e5c3be4ce5ba539c443b5a1f4dc7129329` |
| `claude29` | `@conclaw29bot` | paji | copied from root config |

**Shared Gateway**: `ws://127.0.0.1:18789` (pid 10346, openclaw-gateway)
**Lokkji's Telegram chatId**: `8190607091`

## Task

### Step 1: Run dashboard script

```bash
bash /home/paji/Loki-Oracle/.claude/openclaw-dashboard.sh
```

Show the output to Lokkji.

### Step 2: If any instance is down

- **tmux session missing** → instance not started
- **Telegram: error** → check bot token in openclaw config
- **Gateway: error** → gateway may have crashed, check `openclaw-gateway` process

### Step 3: Quick health per instance

To check a single instance manually:
```bash
tmux send-keys -t <session> C-u && sleep 0.3 && tmux send-keys -t <session> "openclaw health 2>&1" && sleep 0.5 && tmux send-keys -t <session> C-m
sleep 30 && tmux capture-pane -t <session> -p | tail -20
```

## Sending to a Specific Instance

Each bot is independent. To target a specific instance:
```bash
# via claude28
tmux send-keys -t claude28 C-u && sleep 0.3 && \
tmux send-keys -t claude28 "openclaw agent --session-id agent:main:main --message \"<msg>\" --json" && \
sleep 0.5 && tmux send-keys -t claude28 C-m

# via claude29 (same pattern)
# via claude30 (same pattern)
```

## Notes

- All 3 instances connect to the same gateway (`ws://127.0.0.1:18789`)
- Each has its own Telegram bot and agent session
- Dashboard polls all 3 simultaneously for efficiency
- Health checks take ~30s each (openclaw startup time)
