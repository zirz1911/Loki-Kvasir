# Lesson Learned — Local LLM + Voice Integration

**Date**: 2026-02-18
**Source**: rrr: Loki-Kvasir session

---

## 1. Read the room's docs before proposing external solutions

Lokkji เขียน `CLAUDE_CODE_WITH_LOCAL_LLM.md` ไว้แล้ว — อธิบายชัดว่า MCP Server คือวิธีที่ดีที่สุด, LiteLLM proxy ไม่แนะนำ ถ้าไม่ตรวจ Paji repo จะเสียเวลา propose approach ผิด

**Tags**: `paji-repo`, `mcp`, `research-first`

---

## 2. Rust `#[cfg(target_os)]` สำหรับ cross-platform code

```rust
#[cfg(target_os = "macos")]
pub fn speak_text(...) { Command::new("say")... }

#[cfg(target_os = "windows")]
pub fn speak_text(...) { Command::new("powershell")... }
```

Compile-time selection — ไม่มี runtime overhead ไม่มี if/else ไม่มี Option ใช้กับ TTS, filesystem paths, platform APIs

**Tags**: `rust`, `cross-platform`, `cfg`

---

## 3. Local LLM timeout baseline

- 32B model บน consumer hardware: ตั้ง timeout ≥ 300s
- 7B model: 60s พอ
- 120s default ไม่พอสำหรับ 32B + long prompt

**Tags**: `ollama`, `timeout`, `local-llm`, `thor`

---

## 4. Windows TTS via SAPI ผ่าน PowerShell

```powershell
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.Rate = 0  # -10 to +10, 0 = normal
$s.SelectVoice('Microsoft Zira Desktop')
$s.Speak('Hello')
```

Rate conversion จาก macOS wpm: `windows_rate = ((wpm - 220) / 30).clamp(-10, 10)`
Voices ที่มักมี: `Microsoft David Desktop`, `Microsoft Zira Desktop`

**Tags**: `windows`, `tts`, `sapi`, `powershell`

---

## 5. MCP Server ใน Claude Code ใช้ `.mcp.json` ไม่ใช่ `settings.json`

- `.mcp.json` ที่ project root = project-scoped MCP server
- `settings.local.json` + `enabledMcpjsonServers: ["name"]` = auto-approve
- `settings.json` (user-level) ไม่รองรับ `mcpServers` field โดยตรง

**Tags**: `claude-code`, `mcp`, `settings`
