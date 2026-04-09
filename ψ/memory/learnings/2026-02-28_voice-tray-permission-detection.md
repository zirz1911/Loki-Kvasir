# Lesson: Voice Tray Permission Alert Detection

**Date**: 2026-02-28
**Source**: kvasir-voice-tray watcher iteration

---

## Core Insight

`stop_reason: tool_use` ใน Claude Code JSONL ไม่ใช่ signal ของ "ต้องขอ permission" — มันยิงสำหรับ **ทุก tool ทุกตัว** ไม่ว่าจะ auto-approved หรือไม่

## Correct Detection Pattern

```
tool_use → start 3s timer
    ├── tool_result มาภายใน 3s → auto-approved → cancel timer
    └── ครบ 3s ไม่มี tool_result → user needs to approve → alert
```

**ต้อง gate ด้วย permission mode:**
- `skipDangerousModePermissionPrompt: true` ใน `~/.claude/settings.json` → ปิด alert ทั้งหมด
- mode อื่น → ใช้ timer

## JSONL Fields

| Field | Location | Meaning |
|-------|----------|---------|
| `stop_reason: "end_turn"` | `message.stop_reason` | Claude หยุดทำงาน |
| `stop_reason: "tool_use"` | `message.stop_reason` | Claude กำลังใช้ tool |
| `name: "Task"` | `message.content[].name` | Spawn subagent |
| `input.description` | `message.content[].input.description` | ชื่องานของ subagent |
| `tool_result` | user message content | Tool executed (approved/denied) |

## Permission Mode Storage

| Mode | Settings field | In settings.json? |
|------|---------------|-------------------|
| Dangerously skip | `skipDangerousModePermissionPrompt: true` | ✅ |
| Accept edits on | (in-memory session state) | ❌ ไม่เขียนไฟล์ |
| Normal | (default, no field) | N/A |

## Soul-Brews-Studio Org

repos ใน `Soul-Brews-Studio` org ต้องใช้ org token แยก
`zirz1911` personal account ไม่มีสิทธิ์ push — ต้องให้ Lokkji push เอง
