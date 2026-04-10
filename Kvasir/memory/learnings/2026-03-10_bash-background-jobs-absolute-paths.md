# Bash Background Jobs — Always Use Absolute Paths

**Discovered**: 2026-03-10
**Context**: wget parallel downloads ใน ComfyUI install

## Pattern

Background jobs (`&`) ใน bash **ไม่ inherit cwd ของ parent เสมอ** โดยเฉพาะเมื่อใช้ร่วมกับ `cd` ก่อนหน้า

```bash
# ❌ FAILS — relative path ไม่ทำงานใน background job
cd /some/dir && wget -O file.txt http://... &

# ✅ WORKS — absolute path ปลอดภัยเสมอ
wget -O /some/dir/file.txt http://... &
```

## Rule

เมื่อ run parallel downloads หรือ background processes ที่ต้องการ write ไฟล์ — ใช้ absolute path เสมอ

## Related

- symlink write permission: ก่อน symlink folder ที่จะเขียน ทำ `touch /path/test && rm /path/test` ก่อน
