# /tmux-send — Send Message to Tmux Session

Send a message to any tmux session from the current session.

Usage: `/tmux-send <session> <message>`

Example: `/tmux-send claude30 สวัสดี`
Example: `/tmux-send 0 ls -la`
Example: `/tmux-send work git status`

## Task

### Step 1: Parse Arguments

Take `$ARGUMENTS` and split:
- First word = **session name**
- Rest = **message**

If no session → ask: "ส่งไปที่ session ไหน?"
If no message → ask: "จะส่งข้อความอะไร?"

### Step 2: Check Session Exists

Run:
```bash
tmux list-sessions 2>&1
```

Verify the target session exists. If not — show available sessions and stop.

### Step 3: Send

Clear any existing input first, then send:
```bash
tmux send-keys -t <session> C-u && sleep 0.3 && tmux send-keys -t <session> "<message>" && sleep 0.5 && tmux send-keys -t <session> C-m
```

### Step 4: Capture Output

Wait 1 second then capture the pane to confirm delivery:
```bash
sleep 1 && tmux capture-pane -t <session> -p | tail -20
```

### Step 5: Acknowledge

Reply with:
```
Sent → [session]: "[message]"
```

Then show the last few lines of the session output so Lokkji can see the response.

## Notes

- Uses `C-m` (Ctrl+M = carriage return) instead of literal `Enter` — more reliable
- 0.5s delay between text and send prevents race conditions
- Works with any tmux session: numbered (`0`, `1`) or named (`claude30`, `work`)
