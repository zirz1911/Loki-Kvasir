---
name: Fix script not just docs
description: เมื่อแก้ reference ใน CLAUDE.md ต้อง grep หา references เดียวกันใน shell scripts ด้วย
type: feedback
---

เมื่อแก้ window reference, path, หรือ config ใน CLAUDE.md — ให้ grep หา reference เดียวกันใน shell scripts และ config files ด้วยเสมอ

**Why:** Session นี้พบว่า `loki-kvasir:6` ถูก fix ใน CLAUDE.md (session 15:17) แต่ `smart-route-hook.sh` ยังมี `:6` อยู่ ทำให้ hook ส่งงานผิด window ต่อไปอีก session ทั้งที่เอกสารบอกว่า fix แล้ว CLAUDE.md อัพเดตง่ายจน script มองข้ามได้

**How to apply:** หลัง fix reference ใน CLAUDE.md เสมอ:
```bash
grep -r "OLD_REFERENCE" ~/.claude/ .claude/ --include="*.sh" --include="*.py" --include="*.json"
```
ถ้าเจอ → fix ทันที ถ้าไม่เจอ → safe to proceed
