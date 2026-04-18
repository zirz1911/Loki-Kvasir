---
name: Claude Code hook payload format
description: UserPromptSubmit hook ส่ง hook_event_name + prompt โดยตรง ไม่ใช่ event field และไม่ต้องอ่าน transcript
type: project
---

## Claude Code Hook Payload (UserPromptSubmit)

```json
{
  "session_id": "...",
  "transcript_path": "/home/.../session.jsonl",
  "cwd": "/home/paji/Loki-Kvasir",
  "permission_mode": "bypassPermissions",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "user's actual message here"
}
```

**Key fields:**
- `hook_event_name` — ไม่ใช่ `event` — ชื่อ event จริงๆ
- `prompt` — user message โดยตรง (ใน UserPromptSubmit เท่านั้น)
- `transcript_path` — path ไปยัง session .jsonl ถ้าต้องการ full history

**ไม่ต้อง**: อ่าน transcript, parse Python repr strings, assume field names จาก feed_hook.py

## Project vs Global Settings hooks

ทั้ง `~/.claude/settings.json` และ `.claude/settings.local.json` fire พร้อมกัน — ถ้าเพิ่ม hook เดียวกันในทั้งสอง จะ duplicate เพิ่ม project-specific hooks ใน `settings.local.json` เท่านั้น

## Debug Method

เมื่อ hook ไม่ทำงานตามคาด: สร้าง capture script ชั่วคราวที่ write stdin ไป `/tmp/` แล้วดู actual payload ก่อน assume ใดๆ

```python
# /tmp/stdin_capture.py
import sys, json
raw = sys.stdin.read()
with open("/tmp/captured.json", "w") as f:
    f.write(raw)
```
