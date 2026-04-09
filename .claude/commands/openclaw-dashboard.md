# /openclaw-dashboard — Openclaw Status Dashboard

Check the live status of active Openclaw instances from this session.

Usage: `/openclaw-dashboard`

## Active Fleet

| Session | Alias | Bot | IP | Version |
|---------|-------|-----|----|---------|
| `claude30` | — | `@conclaw30bot` | local (root) | 2026.2.9 |
| `claude29` | — | `@conclaw29bot` | 192.168.1.34 | 2026.2.19-2 |
| `claude28` | **Claude202** | `@openpaji_bot` | new machine | 2026.2.6-3 |

**Lokkji's Telegram chatId**: `8190607091`

## Task

### Step 1: Run dashboard script

```bash
bash /home/paji/Loki-Kvasir/.claude/openclaw-dashboard.sh
```

Show the output to Lokkji.

### Step 2: If any instance is down

- **tmux session missing** → instance not started
- **Telegram: error** → check bot token in openclaw config
- **Gateway: error** → gateway may have crashed, check `openclaw-gateway` process
- **pairing required** → run `openclaw devices list` then `openclaw devices approve <id>`

### Step 3: Quick health per instance

```bash
tmux send-keys -t <session> C-u && sleep 0.3 && \
tmux send-keys -t <session> "openclaw health 2>&1" && \
sleep 0.5 && tmux send-keys -t <session> C-m
sleep 35 && tmux capture-pane -t <session> -p | tail -20
```

## Sending to a Specific Instance

```bash
# claude30 (v2026.2.9)
tmux send-keys -t claude30 C-u && sleep 0.3 && \
tmux send-keys -t claude30 "openclaw agent --session-id agent:main:main --message \"<msg>\" --json" && \
sleep 0.5 && tmux send-keys -t claude30 C-m

# claude29 (v2026.2.19-2)
tmux send-keys -t claude29 C-u && sleep 0.3 && \
tmux send-keys -t claude29 "openclaw agent --agent main --message \"<msg>\" --json" && \
sleep 0.5 && tmux send-keys -t claude29 C-m

# claude28 / Claude202 (v2026.2.6-3)
tmux send-keys -t claude28 C-u && sleep 0.3 && \
tmux send-keys -t claude28 "openclaw agent --agent main --message \"<msg>\" --json" && \
sleep 0.5 && tmux send-keys -t claude28 C-m
```

## Notes

- `--session-id agent:main:main` for v2026.2.9, `--agent main` for v2026.2.19-2 and v2026.2.6-3
- claude28 = Claude202 (new machine, @openpaji_bot) — agents: coder-man, thor, loki, hermes, tyr, ymir
- old claude28 (192.168.1.229) removed — machine offline
