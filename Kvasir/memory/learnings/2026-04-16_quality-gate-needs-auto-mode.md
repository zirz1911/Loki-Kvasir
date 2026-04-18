---
name: Quality gate auto-score mode
description: Interactive batch scoring สำหรับ 84 files นั้น impractical — ต้องมี --auto flag
type: feedback
---

`quality_gate.py --batch` ถูก design ให้ interactive (พิมพ์คะแนนทีละตัว) ซึ่ง impractical มากสำหรับ 84 files จริงๆ ถ้าไม่มี agent ช่วย ระบบนี้จะไม่เคยถูกรันเลย

**Why:** Session นี้ต้องให้ Tyr agent score แทนทั้งหมด เพราะ human batch scoring 84 files = ชั่วโมง การออกแบบที่ดีกว่าคือ `--auto` flag ที่ให้ Claude score โดยตรง

**How to apply:** เพิ่ม `--auto` flag ใน `quality_gate.py` — อ่านแต่ละไฟล์, ส่งเนื้อหาให้ Claude judge ตาม 4 criteria, write JSON result โดยอัตโนมัติ ไม่ต้อง interactive prompt
