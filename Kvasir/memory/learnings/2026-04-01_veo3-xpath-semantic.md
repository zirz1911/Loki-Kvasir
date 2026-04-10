---
name: VEO3 XPath — ใช้ semantic text ไม่ใช่ generated class
description: XPath ที่เสถียรใน labs.google ต้องจับที่ visible/aria text ไม่ใช่ CSS-in-JS class names
type: project
---

ใน labs.google UI ทุก class name เป็น generated (เช่น `sc-84e494b2-2 ckCGSv`) — เปลี่ยนได้ทุก deploy

**XPath ที่ใช้งานได้ (2026-04-01):**
```
ปุ่ม +:      //button[.//span[text()='สร้าง' or text()='Create']]
ปุ่ม Upload: //div[contains(text(),'อัปโหลดรูปภาพ') or contains(text(),'Upload')]
ปุ่ม เริ่ม:  //div[@aria-haspopup='dialog' and (text()='เริ่ม' or text()='Start')]
```

**Why:** class names เปลี่ยนทุก deploy แต่ user-visible text และ aria attributes เสถียรกว่า

**How to apply:** ทุกครั้งที่เขียน XPath ใหม่สำหรับ labs.google ให้ target `text()`, `aria-label`, `aria-haspopup` ก่อน อย่า target `class` หรือ `data-*` ที่ดูเหมือน generated
