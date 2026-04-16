# /reflect — ปิดวงจร learnings → CLAUDE.md ใช้เมื่อพูดว่า reflect, learning loop, promote learnings, review learnings

ปิดวงจร: learnings → CLAUDE.md

## เมื่อไหร่ใช้
- หลังสะสม learnings ≥ 10 session
- ก่อน `/wrap` แบบ deep
- เมื่อรู้สึกว่า CLAUDE.md ล้าสมัย

## สิ่งที่ต้องทำ

### Step 1: นับ learnings ที่สะสมอยู่
```bash
ls -t Kvasir/memory/learnings/*.md | head -20
ls Kvasir/memory/learnings/*.md | wc -l
```

### Step 2: อ่าน learnings ล่าสุด (2 สัปดาห์)
```bash
find Kvasir/memory/learnings -name "*.md" -newer Kvasir/memory/learnings/$(ls -t Kvasir/memory/learnings/*.md | tail -1 | xargs basename) | sort
```

หรือใช้ date filter:
```bash
find Kvasir/memory/learnings -name "*.md" -mtime -14 | sort
```

### Step 3: จัด learnings เป็น 3 กลุ่ม

สำหรับแต่ละ learning ถามตัวเอง:

| คำถาม | น้ำหนัก |
|-------|---------|
| เป็น pattern ซ้ำๆ หรือ one-time? | สูง |
| future-Kvasir จะได้ใช้ทันทีมั้ย? | สูง |
| เคยทำผิดเพราะไม่รู้สิ่งนี้มั้ย? | กลาง |
| ไม่ obvious จาก docs/code? | กลาง |

**promote** → ควรเข้า CLAUDE.md
**keep** → เก็บใน learnings/ (ยังไม่ถึงเวลา)
**archive** → จริงแต่ ephemeral มากเกินไป

### Step 4: promote เข้า CLAUDE.md

เปิด `CLAUDE.md` และเพิ่มใน section ที่เหมาะสม:
- **Golden Rules** — ถ้าเป็น DO/DON'T ที่ชัดเจน
- **Brain Structure** — ถ้าเกี่ยวกับ file/directory patterns
- **Norse Agent System** — ถ้าเกี่ยวกับ delegation/routing
- **ท้ายสุด** — สร้าง section ใหม่ถ้าไม่ fit ที่ไหน

Format ใน CLAUDE.md:
```markdown
## Patterns Learned

- **[ชื่อ pattern]** — [อธิบาย 1 บรรทัด]. เพราะ: [เหตุผล]
```

### Step 5: บันทึกว่า reflect แล้ว

```bash
echo "$(date +%Y-%m-%d): reflected on $(ls Kvasir/memory/learnings/*.md | wc -l) learnings" \
  >> Kvasir/memory/logs/reflect.log
```

## Output ที่คาดหวัง

สรุปสั้นๆ:
- จำนวน learnings ที่ review
- กี่อันที่ promote เข้า CLAUDE.md
- CLAUDE.md sections ที่เปลี่ยน
- learnings ที่ archive (ถ้ามี)

## ตัวอย่าง Promote

Learning:
> rename-causes-silent-infrastructure-break — เมื่อ rename file ใน Kvasir ต้องตรวจว่า running process / hook ยังอ้างถึง path เดิมอยู่มั้ย

→ Promote เข้า Golden Rules:
```
- Never rename .claude/ scripts without checking running hooks reference them
```
