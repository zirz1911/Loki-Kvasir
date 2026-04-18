---
date: 2026-04-18
tags: [manim, thai-font, video-generation, cairo, pango]
source: "wrap: Loki-Kvasir"
---

# Manim Thai Font Check Before Writing Thai Text

## Pattern

Before using Thai (or any non-Latin) text in a Manim script, verify fonts are installed:

```bash
fc-list | grep -i thai
```

If empty → fonts missing. Manim uses Cairo/Pango for text rendering. Missing fonts produce silent failures — boxes, empty strings, or rendering errors that only appear at render time.

## Fix Options

**Option A: Install Thai fonts**
```bash
sudo apt-get install fonts-thai-tlwg fonts-noto
```

**Option B: Switch to English** (faster, no system changes needed)
- Replace all Thai strings with English equivalents
- Change TTS voice: `"th-TH-NiwatNeural"` → `"en-US-GuyNeural"`

## Why This Matters

Discovered after Tyr wrote a 782-line Manim script with Thai text throughout. Full render completed but output had broken text. Required 14 Edit calls + full re-render cycle to fix. A single font check before writing the script would have saved 30+ minutes.

## Also Apply To

- Any Manim script using CJK, Arabic, Devanagari, or other non-Latin scripts
- General rule: check font availability before committing to a text renderer that doesn't fail loudly
