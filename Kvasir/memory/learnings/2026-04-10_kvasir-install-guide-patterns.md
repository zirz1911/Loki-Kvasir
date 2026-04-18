---
name: Kvasir-Install guide patterns
description: สร้าง install guide ที่เป็น Claude Code prompt + slide website + GitHub Pages
type: project
---

## Pattern 1: Issue as Claude Code prompt

แทนที่จะเขียน documentation ยาว — เขียน Issue เป็น prompt ที่ copy-paste เข้า Claude Code ได้เลย

**Why:** ผู้ใช้ใหม่ไม่ต้องอ่านทีละขั้นและรันเอง — Claude Code ทำให้ทั้งหมด

**How to apply:**
- ขั้นตอน terminal ปกติ → code blocks ธรรมดา
- ขั้นตอนที่ต้องการ AI → ระบุชัดเป็น "Claude Code Prompt" section

## Pattern 2: Slide website สำหรับ multi-step guide

สร้าง single HTML file เป็น slide presentation — ดีกว่า long-form doc เพราะ:
- แต่ละ slide = 1 ขั้นตอน = ไม่ท่วม
- Platform tabs แยก Linux/macOS/Windows ในหน้าเดียว
- Copy button บน code block ทุก block

**Why:** ผู้ใช้ใหม่ต้องการ focus — ไม่ใช่ wall of text

## Pattern 3: Zoom > detail panel สำหรับ slides

ปุ่ม zoom in/out เหมาะกับ slide format มากกว่า side panel

**Why:** Side panel สร้าง cognitive split — อ่าน slide หรืออ่าน panel? Zoom แก้ปัญหา accessibility โดยไม่ทำลาย focus

## Pattern 4: GitHub Pages จาก index.html ที่ root

```bash
gh api repos/[owner]/[repo]/pages -X POST \
  --field 'source[branch]=main' \
  --field 'source[path]=/'
```

Deploy ทันทีหลัง push — ไม่ต้องการ CI/CD
