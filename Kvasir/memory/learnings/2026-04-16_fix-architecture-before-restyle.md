---
name: Fix architecture before restyling UI
description: Applying visual polish on top of broken foundation forces multiple redo cycles — fix the underlying bug first, then style once
type: feedback
---

ถ้า UI มี visual bugs ให้ถามก่อนว่า bugs มาจาก **architecture** หรือ **styling** — อย่า restyle บน foundation ที่ยังแตก

**Why:** วันนี้ restyle TerminalModal เป็น Paji-Exo 2 รอบ และกลับไปใช้สไตล์เดิม 1 รอบ เพราะ "visual bugs" จริงๆ มาจาก xterm.js rendering แตก ไม่ใช่ CSS ผิด พอเปลี่ยนไปใช้ CapturePane (architecture ถูกต้อง) แล้ว restyle ครั้งเดียวก็ clean ทันที

**How to apply:**
1. ถ้า user บอกว่า terminal หน้าตาบั๊ก → debug rendering pipeline ก่อน
2. แยก "data pipeline broken" ออกจาก "styling wrong"
3. Fix foundation → test → style → done (ครั้งเดียว)
