# Openclaw Agent CLI — Confirmed Working Command

**Date**: 2026-02-21
**Context**: สำรวจ Openclaw บนเครื่อง claude30, ทดสอบจนได้คำสั่งที่ใช้งานได้จริง

## Working Command

```bash
openclaw agent \
  --session-id agent:main:main \
  --message "ข้อความ" \
  --json
```

## Gateway Info

- URL: `ws://127.0.0.1:18789`
- Token: **ไม่จำเป็น** สำหรับ local loopback connections
- Agent session-id: `agent:main:main`
- Telegram: `@conclaw30bot`
- Version: `2026.2.9`

## ข้อผิดพลาดที่เคยเกิด

- `--token` — ไม่ใช่ option ของ `openclaw agent` (ใช้ใน `openclaw acp` เท่านั้น)
- `--session` — ไม่ถูกต้อง, ต้องใช้ `--session-id`
- `--url` — ไม่ใช่ option ของ `openclaw agent`

## สองโหมดหลัก

| Command | Mode | ใช้เมื่อ |
|---|---|---|
| `openclaw agent --message "..."` | One-shot | Script/automation |
| `openclaw acp client` | Interactive REPL | คุยกับ agent โดยตรง |

## Architecture ใน Loki Kvasir

- openclaw ติดตั้งเฉพาะ claude30 session (root environment)
- session หลัก (paji/WSL) route ผ่าน tmux-send → claude30
- Skill: `.claude/commands/openclaw.md`
