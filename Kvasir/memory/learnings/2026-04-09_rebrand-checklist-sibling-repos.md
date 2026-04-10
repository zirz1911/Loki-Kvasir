---
name: Rebrand checklist — scan sibling repos
description: เมื่อ rebrand identity หลัก ต้อง scan sibling repos ด้วย ไม่ใช่แค่ repo ปัจจุบัน
type: feedback
---

เมื่อ rebrand identity (เช่น Oracle→Kvasir) อย่าลืม check repos อื่นที่ branch มาจาก identity เดิม

**Why:** Loki-Oracle → Loki-Kvasir rebrand เสร็จแล้ว แต่ Loki-Gemini ซึ่งสร้างมาจาก Loki-Oracle ยังอ้างตัวเองว่า "Oracle" อยู่ — ทำให้ต้องมา cleanup แยกอีก session

**How to apply:**
1. ก่อน rebrand ให้ run: `find /home/paji -maxdepth 2 -name "GEMINI.md" -o -name "CLAUDE.md" | xargs grep -l "<old-name>"`
2. Track ทุก repo ที่พบก่อน commit rebrand หลัก
3. `.gemini/commands/` ควรถูก `git add` ตั้งแต่วันเกิด repo — เป็น behavior config ที่หายได้ถ้าไม่ track
