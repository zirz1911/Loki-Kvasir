---
name: Live-fill input pattern for static code guides
description: เทคนิคใส่ input field ใน static HTML guide ให้ผู้ใช้กรอก value แล้ว code blocks อัพเดท live
type: project
---

## Pattern: Live-fill input ใน static guide

แทนที่จะให้ผู้ใช้ copy code แล้วแก้ placeholder เอง → ใส่ input field → code blocks อัพเดทอัตโนมัติ

**Technique:**
1. ใส่ `<span id="kv-{platform}">placeholder</span>` รอบค่า placeholder ใน `<pre>` block แต่ละแท็บ
2. Input field เรียก `updateApiKey(val)` ผ่าน `oninput`
3. JS: `document.getElementById('kv-bash').textContent = key` × จำนวน platforms
4. `copyCode()` ที่ใช้ `pre.innerText` จะ pick up ค่า updated โดยอัตโนมัติ — ไม่ต้องแก้ copy logic

**Badge pattern:** `✓ SET` badge (hidden by default, `.visible` class เมื่อมีค่า) → confirmation ที่ไม่ intrusive

**Progressive disclosure:** ถ้าไม่กรอก → placeholder ยังอยู่ → slide ทำงานปกติ. ถ้ากรอก → live update

**Why:** ลด friction จาก "instructions" → "executable" — ผู้ใช้ copy command ที่ใช้งานได้เลยโดยไม่ต้องแก้

**How to apply:** ทุก HTML guide ที่มี placeholder value ที่ user-specific (API key, username, domain, project name) → ใส่ input field + span IDs แทน static placeholder
