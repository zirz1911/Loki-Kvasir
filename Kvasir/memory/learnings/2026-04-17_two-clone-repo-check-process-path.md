---
name: two-clone-repo-check-process-path
description: เมื่อ pm2/process run จาก path ที่ต่างกับ repo ที่ edit — ตรวจ process path ก่อนเสมอ
type: feedback
---

เมื่อมีสอง clone ของ repo บนเครื่องเดียว (เช่น `~/ghq/...` กับ `~/Project/...`) pm2 หรือ process ที่ running อาจชี้ไปที่ clone ที่ต่างกับที่กำลัง edit ทำให้ edit แล้ว deploy แต่ไม่เห็นผล

**Why:** ใน session นี้ edit `/home/paji/ghq/github.com/zirz1911/Loki-Pixfice/src/server.ts` ทั้งหมดก่อนจะพบว่า pm2 run จาก `/home/paji/Project/Loki-Pixfice/` — ตรวจเห็นจาก error log ที่แสดง path จริง เสียเวลา 1 รอบ deploy

**How to apply:** ก่อน edit code สำหรับ process ที่ running ให้ตรวจก่อน:
```bash
pm2 show <process-name>          # ดู script path
pm2 logs <name> --err --lines 5  # ดู stack trace มี path จริง
```
ถ้ามีสอง clone ให้ทำ marker ชัด (เช่น `README: THIS IS PRODUCTION`) หรือใช้ symlink
