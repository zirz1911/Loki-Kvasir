---
name: After rename — check running state not just written state
description: Directory rename แก้ files/scripts แต่ process/session ใน RAM ยังใช้ชื่อเก่า
type: feedback
---

หลัง rename directory ให้ audit สิ่งที่ **กำลังรัน** ไม่ใช่แค่ไฟล์ที่เขียนไว้

**Why:** Athena-Oracle → Athena-Kvasir: scripts/configs อัปเดตหมด แต่ bun server ที่ยังรันอยู่ถูก spawn จาก `/home/paji/Athena-Oracle/office` ตั้งแต่ Apr06 (10 วันก่อน) — พอพยายาม restart จึง "No such file or directory" เพราะ path เก่าหายไปแล้ว

**How to apply:** หลัง rename ทุกครั้งให้รัน:
1. `ps aux | grep OLD-NAME` — ดู process ที่ยังรัน
2. `tmux list-sessions` — ดู session ที่ต้อง recreate
3. `lsof -i :PORT` — verify port ถูก bind จาก path ใหม่
4. `systemctl --user list-units | grep name` — ดู services
