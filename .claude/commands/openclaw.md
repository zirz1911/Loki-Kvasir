# /openclaw — Send Message to Openclaw Agent

Control the Openclaw agent (running in claude30 session) from this session.

Usage: `/openclaw <message>`

Example: `/openclaw สวัสดี`
Example: `/openclaw ดู status ของ agent ทั้งหมด`
Example: `/openclaw ส่งข้อความ Telegram ไปหา Lokkji ว่า build สำเร็จแล้ว`

## Architecture

```
[Loki Oracle - this session]
       ↓ tmux send-keys
[claude30 - has openclaw at /usr/bin/openclaw]
       ↓ openclaw agent CLI
[Gateway ws://127.0.0.1:18789 → agent:main:main]
```

## Config

- **Session**: `claude30`
- **Agent session-id**: `agent:main:main`
- **Token**: not required for `openclaw agent` (local loopback, no auth needed)
- **Lokkji's Telegram chatId**: `8190607091`

## Task

### Step 1: Parse Arguments

Take `$ARGUMENTS` as the message to send.

If empty → ask: "จะส่งอะไรไปหา Openclaw agent?"

### Step 2: Check claude30 is alive

```bash
tmux list-sessions 2>&1
```

Verify `claude30` session exists. If not → stop and warn.

### Step 3: Send via tmux → claude30

Clear any existing input first, then send:
```bash
tmux send-keys -t claude30 C-u && sleep 0.3 && tmux send-keys -t claude30 "openclaw agent --session-id agent:main:main --message \"<message>\" --json 2>&1" && sleep 0.5 && tmux send-keys -t claude30 C-m
```

### Step 4: Wait and capture response

```bash
sleep 5 && tmux capture-pane -t claude30 -p | tail -40
```

If the response contains `approve` / `Do you want to proceed?` → approve automatically with `1` + C-m, then wait and capture again.

If still running → wait another 10s and capture again.

### Step 5: Parse and display result

Extract the relevant output from the capture. Show:
- Agent's reply (text content from JSON if --json mode)
- Any error if failed

Reply format:
```
Openclaw → agent:main:main
"<message sent>"

Response:
<agent reply>
```

## Notes

- openclaw is NOT installed in this session — must route through claude30
- claude30 must be running and have openclaw in PATH
- Token is hardcoded — rotate in this file if gateway token changes
- `--json` flag gives structured output, easier to parse
- First run after gateway idle may be slow (30-60s) — agent wakes up
