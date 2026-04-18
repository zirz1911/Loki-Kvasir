---
name: pm2-crash-loop-eaddrinuse
description: pm2 restart loop + EADDRINUSE — fix pattern และ root cause
type: feedback
---

pm2 restart count 50+ รอบ + `EADDRINUSE` ใน error log = crash loop ที่แก้ไม่หายด้วย `pm2 restart`

**Why:** เมื่อ pm2 restart process ใหม่มาก่อนที่ process เก่าจะ release port เสมอ ทำให้ EADDRINUSE → crash → restart วนไปเรื่อยๆ

**How to apply:** Fix ที่ถูกต้องคือ:
1. `pm2 stop <name>` — หยุดก่อน
2. `kill $(lsof -ti :<port>)` — clear port
3. `pm2 start <name>` — start clean

อย่า `pm2 restart` เพียงอย่างเดียวถ้า restart count สูงมากและมี EADDRINUSE ใน logs — มันจะไม่แก้ปัญหา
