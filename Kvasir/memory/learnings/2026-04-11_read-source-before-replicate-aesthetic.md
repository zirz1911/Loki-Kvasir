---
name: Read source before replicating aesthetic
description: ชื่อ font/style ไม่เชื่อถือได้ — ต้องอ่าน CSS/source จริงก่อน replicate
type: feedback
---

ถ้าต้องการ replicate aesthetic ของ project อื่น ให้ **อ่าน source จริงก่อนเสมอ** อย่าเดาจากชื่อหรือ description

**Why:** Claude-Skill-Learn ใช้ฟอนต์ "Exo 2" (geometric sans-serif) แล้วเรียกตัวเองว่า "Exo-Paji style" — แต่ Exo-Paji จริงใช้ `Silkscreen` (pixel terminal font) + terminal green palette ไม่ใช่ cyan/purple/orange การเดาจากชื่อทำให้ผิดทั้งหมด โดยไม่รู้ตัว

**How to apply:** ก่อน implement "X style" — ค้นหา X project บน filesystem (`find /home/paji -name "*.css" -path "*X*"`) แล้วอ่าน CSS จริง เฉพาะ fonts, colors, effects ที่กำหนดไว้ใน `:root` หรือ `@theme`
