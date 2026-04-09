# /openclaw — Send Message to Openclaw Agent

Control any Openclaw agent from this session via tmux bridge.

Usage: `/openclaw <message>`
Usage: `/openclaw <session> <message>` (target specific instance)

Example: `/openclaw สวัสดี`
Example: `/openclaw ส่งข้อความ Telegram ไปหา Lokkji ว่า build สำเร็จแล้ว`
Example: `/openclaw claude29 สวัสดีจาก session หลัก`

## Architecture

```
[Loki Kvasir - this session]
       ↓ tmux send-keys
[claude28 / claude29 / claude30]
       ↓ openclaw agent CLI
[Gateway ws://127.0.0.1:18789 → agent:main:main]
```

## Fleet Config

| Session | Alias | Bot | IP | Version | Flag |
|---------|-------|-----|----|---------|------|
| `claude30` | — | `@conclaw30bot` | local (root) | 2026.2.9 | `--session-id agent:main:main` |
| `claude29` | — | `@conclaw29bot` | 192.168.1.34 | 2026.2.19-2 | `--agent main` |
| `claude28` | **Claude202** | `@openpaji_bot` | new machine | 2026.2.6-3 | `--agent <name>` |

**Lokkji's Telegram chatId**: `8190607091`
**Default session**: `claude30`

## CLI Flags by Version

- **v2026.2.9** (claude30): `openclaw agent --session-id agent:main:main --message "..." --json`
- **v2026.2.19-2** (claude28, claude29): `openclaw agent --agent main --message "..." --json`

## Task

### Step 1: Parse Arguments

If first word matches a tmux session name (`claude28`, `claude29`, `claude30`) → use that as target, rest as message.
Otherwise → default to `claude30`, full `$ARGUMENTS` as message.

If empty → ask: "จะส่งอะไรไปหา Openclaw agent?"

### Step 2: Check session is alive

```bash
tmux list-sessions 2>&1
```

Verify target session exists. If not → stop and warn, show available sessions.

### Step 3: Send via tmux → target session

Clear input first, then send with correct flag for version:

**claude30** (v2026.2.9):
```bash
tmux send-keys -t claude30 C-u && sleep 0.3 && tmux send-keys -t claude30 "openclaw agent --session-id agent:main:main --message \"<message>\" --json 2>&1" && sleep 0.5 && tmux send-keys -t claude30 C-m
```

**claude28 / claude29** (v2026.2.19-2):
```bash
tmux send-keys -t <session> C-u && sleep 0.3 && tmux send-keys -t <session> "openclaw agent --agent main --message \"<message>\" --json 2>&1" && sleep 0.5 && tmux send-keys -t <session> C-m
```

### Step 4: Wait and capture response

```bash
sleep 5 && tmux capture-pane -t <session> -p | tail -40
```

If still running → wait another 15s and capture again.
If approval prompt → approve with `1` + C-m then wait again.

### Step 5: Display result

```
Openclaw → <session> (<bot>)
"<message sent>"

Response:
<agent reply>
```

## Notes

- openclaw NOT installed in this session — must route through target tmux session
- v2026.2.19-2 broke `--session-id` → use `--agent main` instead
- First run after idle may be slow (30-60s)
- Gateway is shared at `ws://127.0.0.1:18789` across all instances
