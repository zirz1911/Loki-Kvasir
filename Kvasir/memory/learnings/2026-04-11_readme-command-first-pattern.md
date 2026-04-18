---
name: README command-first pattern
description: README ที่ดีคือ command-first — copy-paste ได้เลย ไม่ใช่ identity document
type: feedback
---

README เป็น "how to use" document ไม่ใช่ "what we believe" document

**Why:** เมื่อ rewrite README ของ Loki-Kvasir ตาม style ของ loki-skills-cli พบว่า README เดิมมี philosophy, principles, และ narrative ยาว แต่ user จริงๆ ต้องการ: install command, skill list, done

**How to apply:**
- README = commands ก่อน, skills table, agent table — จบ
- Identity และ philosophy อยู่ใน `CLAUDE.md` และ `memory/resonance/` แล้ว ไม่ต้องซ้ำ
- Skill descriptions: pull จาก `SKILL.md` frontmatter โดยตรง ไม่เดา
- ถ้าข้อมูลนั้นอยู่ใน source อื่นแล้ว README ไม่ต้องมี
