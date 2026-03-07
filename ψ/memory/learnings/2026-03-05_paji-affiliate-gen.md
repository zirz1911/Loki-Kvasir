# Learnings: Paji-Affiliate-Gen Build

**Date**: 2026-03-05
**Source**: Session building Paji-Affiliate-Gen desktop app

---

## 1. Windows subprocess: binary missing = exception, not exit code

On Windows, `subprocess.run(["missing_binary", ...])` raises `FileNotFoundError` — it does NOT return `returncode != 0`. Always wrap availability checks in try/except:

```python
# WRONG — crashes on Windows if binary missing
result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
if result.returncode != 0:
    warn()

# CORRECT
try:
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    if result.returncode != 0:
        raise FileNotFoundError
except FileNotFoundError:
    warn()
```

## 2. GUI app launch: use pythonw / background

- `python main.py` blocks the terminal — bad for GUI apps
- `start pythonw main.py` (Windows) launches detached with no console window
- `pythonw` is the right tool for CTk/tkinter apps distributed to users

## 3. New project scaffolding checklist

When creating a new Python project:
- `git init` + initial commit
- `.gitignore` (especially `__pycache__/`, `*.pyc`, `.env`, config files with secrets)
- Store API keys outside the repo (e.g., `~/.paji-affiliate/config.json`) — already done here ✅
- Add README with run instructions

## 4. TTS pipeline architecture

Gemini TTS flow that works:
1. `POST https://texttospeech.googleapis.com/v1beta1/text:synthesize?key={key}`
2. Response: `{"audioContent": "<base64 MP3>"}`
3. Decode base64 → write `.mp3`
4. `ffprobe` to get audio duration
5. Random clip selection until `total_clips_duration >= audio_duration`
6. `ffmpeg concat` → `ffmpeg merge audio`
