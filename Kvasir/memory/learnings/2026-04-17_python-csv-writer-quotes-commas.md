---
name: python-csv-writer-quotes-commas
description: Python csv.writer auto-quotes fields ที่มี commas — อย่า split(",") แบบ naive
type: feedback
---

Python `csv.writer` จะ quote field อัตโนมัติถ้า field มี commas เช่น address ที่มาจาก reverse geocoding: `"บ้านโนนสมบูร, บ้านธาตุ, อำเภอเพ็ญ, จังหวัดอุดรธานี, ประเทศไทย"` การ `line.split(",")` แบบ naive จะ parse ผิดทั้งหมด

**Why:** CSV จาก Paji-Location subscriber มี address field ที่ถูก quote — ทำให้ lat/lon parse ถูก แต่ address, timestamp, battery, accuracy, device ทั้งหมดอ่านผิด จนกว่าจะเห็น raw file

**How to apply:** เมื่อ parse CSV จากแหล่งภายนอก (โดยเฉพาะ Python-generated) ให้:
1. ดู raw file ก่อนเสมอ (`cat file.csv`)
2. ใช้ proper quoted-field parser หรือ library

```typescript
function parseCSVRow(line: string): string[] {
  const result: string[] = [];
  let current = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') { current += '"'; i++; }
      else { inQuotes = !inQuotes; }
    } else if (ch === "," && !inQuotes) {
      result.push(current); current = "";
    } else { current += ch; }
  }
  result.push(current);
  return result;
}
```
