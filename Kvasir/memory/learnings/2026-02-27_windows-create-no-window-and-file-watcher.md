# Windows: CREATE_NO_WINDOW + File Watcher Pattern

**Date**: 2026-02-27
**Source**: Kvasir Voice Tray debugging session

---

## Pattern 1: CREATE_NO_WINDOW in Rust (Windows)

When spawning a subprocess on Windows that should have NO visible window, use `CREATE_NO_WINDOW` via `CommandExt` trait — NOT `SW_HIDE` or `windowsHide`.

```rust
#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;

const CREATE_NO_WINDOW: u32 = 0x08000000;

Command::new("powershell")
    .args(["-NoProfile", "-NonInteractive", "-Command", &script])
    .creation_flags(CREATE_NO_WINDOW)
    .spawn()
```

**Why not SW_HIDE?** `SW_HIDE` sets `wShowWindow` in STARTUPINFO — for console apps, this is unreliable. `CREATE_NO_WINDOW` is the `dwCreationFlags` path — it tells Windows not to create a console at all.

**Context**: Fixed Kvasir Voice Tray (`tray.rs`) — PowerShell TTS was spawning a visible window on every voice playback.

---

## Pattern 2: File Watcher as Hook Replacement

Instead of using shell-based hooks (which spawn visible subprocesses on Windows), watch an existing log/event file directly.

**Applied to**: Claude Code session watcher in Kvasir Voice Tray

```rust
// Watch ~/.claude/projects/**/*.jsonl
// When file changes, tail-read new lines
// Detect: type == "assistant" && stop_reason == "end_turn"
// → Queue voice notification
```

**Why better than hooks:**
- No subprocess spawn → no window flash
- No shell wrapping → no PowerShell/cmd overhead
- Simpler configuration — nothing to break
- Works even if hooks are disabled/removed

**Detection signal in Claude Code .jsonl:**
```json
{"type": "assistant", "message": {"stop_reason": "end_turn", ...}}
```

---

## Pattern 3: Windows Path for python3

On Windows, `python3` in hook commands may resolve to the Microsoft Store stub which fails silently. Always use the full path:

```
C:/Users/<user>/AppData/Local/Python/bin/python3.exe
```

Find it with: `powershell.exe -Command "where.exe python3"`

---

## Pattern 4: Platform-aware Tray Popup Position (Tauri)

```rust
let window_height = 490.0_f64;

#[cfg(target_os = "macos")]
let y_pos = (y + 30.0) as i32;    // macOS: menu bar at TOP, show below
#[cfg(not(target_os = "macos"))]
let y_pos = (y - window_height) as i32;  // Windows/Linux: taskbar at BOTTOM, show above

let x_pos = ((x - 200.0) as i32).max(0);  // clamp to screen left edge
```
