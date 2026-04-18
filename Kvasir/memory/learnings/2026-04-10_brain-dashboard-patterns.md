---
name: Brain dashboard visualization patterns
description: D3 force-directed graph สำหรับ knowledge brain + routing decisions สำหรับ standalone tools
type: project
---

## Pattern 1: ถามก่อนว่า canonical home คืออะไร

ก่อน deploy หรือ route artifact ใหม่ → ถามตัวเองก่อนว่า "ของชิ้นนี้ควรอยู่ที่ไหน?"

**Why:** ถ้าไม่ถาม จะ add/revert cycle เหมือนที่เกิดกับ `index.html` redirect — 3 commits แทนที่จะเป็น 1

**How to apply:** Dashboard / visualization / standalone tool → ควรอยู่ใน repo ของตัวเอง ไม่ใช่ embedded ใน repo ที่มัน visualize

## Pattern 2: Viewer ไม่ควรอยู่ใน exhibit

`brain-dashboard.html` อยู่ใน `Kvasir/` → แต่ scan `Kvasir/**/*.md` → นับตัวเองหรือ exclude ตัวเองผิดๆ

**Why:** Observer-in-the-exhibit pattern ทำให้ข้อมูลไม่ถูกต้องและ architecture แปลก

**How to apply:** Visualization → แยก repo → ชี้ `DATA_SOURCE` มาที่ source repo ข้างนอก

## Pattern 3: Mobile viewport ไม่ใช่ afterthought

2 sessions ติดกัน (Kvasir-Install, brain-dashboard) ที่ลืม mobile viewport

**Why:** D3 force graph บนมือถือโดยไม่มี viewport meta = unusable

**How to apply:** ทุก HTML project ที่ build สำหรับ browser → add `<meta name="viewport" content="width=device-width, initial-scale=1">` และ mobile CSS ในรอบเดียวกับ desktop build

## Pattern 4: D3 force graph สำหรับ knowledge visualization

```html
<!-- Exo-Paji style: dark bg, cyan/purple/orange, orbital nodes -->
<!-- Stats bar: total files, sessions, learnings, code studies -->
<!-- Interactive: drag, zoom, hover tooltip with title + type -->
<!-- Color by node type: learnings=cyan, sessions=purple, code=orange -->
```

**Why:** Force-directed graph เหมาะกับ knowledge network ที่ไม่มี hierarchy ตายตัว — nodes cluster ตาม semantic proximity
