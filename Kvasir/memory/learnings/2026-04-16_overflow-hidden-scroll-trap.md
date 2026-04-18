---
name: overflow-hidden scroll trap
description: CSS overflow:hidden at ancestor silently kills descendant scroll with no visual indicator
type: feedback
---

`overflow: hidden` ที่ ancestor ตัดความสามารถ scroll ของ descendant ทั้งหมด โดยไม่มี visual indicator ให้รู้

**Why:** Fleet ไม่ scroll เพราะ Shell.tsx main content div มี `overflow: "hidden"` ซึ่งเป็น default ที่ copy มาจาก mobile layout เดิม Overview scroll ได้เพราะมี internal scroll container ของตัวเอง

**How to apply:** เมื่อ scroll ไม่ทำงานใน component — ก่อนอื่น grep `overflow.*hidden` ใน parent chain ทั้งหมดก่อน debug ที่ component ตัวเอง ถ้าต้องการ clip overflow บน axis เดียว ใช้ `overflowX: hidden` + `overflowY: auto` แทน `overflow: hidden` เสมอ
