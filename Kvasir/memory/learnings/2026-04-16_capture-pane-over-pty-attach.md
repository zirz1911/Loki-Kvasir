---
name: tmux capture-pane > PTY attach for web terminal viewers
description: For browser-based tmux viewers, capture-pane approach eliminates all VT100/escape sequence issues that plague xterm.js + PTY attach
type: project
---

`tmux capture-pane -p -e -t TARGET` ดีกว่า PTY attach + xterm.js สำหรับ web terminal viewer เพราะ:

1. **ไม่มี VT100 cursor positioning codes** — capture-pane output เป็น plain ANSI color/style text เท่านั้น
2. **ไม่มี tmux status bar sequences** — ไม่ต้องสู้กับ `\ek...\e\\` title sequences หรือ status bar artifacts
3. **Thai input ทำงาน** ผ่าน `tmux send-keys -t TARGET -l TEXT` (literal flag)
4. **Bundle เล็กกว่า** — ไม่ต้องใช้ xterm.js (~290KB gzipped)

**Why:** พยายาม debug tmux escape sequences ใน xterm.js หลายรอบ (`status off`, `set-titles off`, `sh -c` wrapper) แต่ทุก fix สร้าง bug ใหม่ root cause คือ xterm.js ออกแบบมาสำหรับ full PTY stream ไม่ใช่ grouped tmux sessions

**How to apply:** เวลาสร้าง web terminal viewer ที่ดู tmux sessions:
- Server: `Bun.spawnSync(["tmux", "capture-pane", "-p", "-e", "-t", target])` poll ทุก 250ms
- Client: ANSI → HTML parser + `<div>` render (ไม่ต้องใช้ xterm.js)
- Input: `Bun.spawnSync(["tmux", "send-keys", "-t", target, "-l", text])` สำหรับ literal text
