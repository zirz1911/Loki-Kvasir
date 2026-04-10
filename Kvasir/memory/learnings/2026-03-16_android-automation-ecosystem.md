# Android Automation Ecosystem — Abstraction Levels

**Date**: 2026-03-16
**Source**: /learn sprint — escrcpy, droidrun, gemgen

## Pattern

Android automation exists on a spectrum of abstraction levels:

| Level | Tool | Interface | Use Case |
|-------|------|-----------|----------|
| Raw ADB | Escrcpy | UI + Scrcpy binary | Human mirror/control |
| LLM CodeAct | DroidRun | Python agent + Portal APK | AI task execution |
| Workflow Graph | GemGen / AutoGLM | JSON blocks/edges | Repeatable automation |
| Visual Macro | DroidRun Macro mode | Record → replay | No-code sequences |

**Key insight**: Each level up trades precision/control for accessibility. CodeAct can reason through unexpected UI states; macros can't.

## DroidRun Portal APK Pattern

Install Portal APK on Android device → exposes accessibility tree via ADB → LLM sees structured UI elements → generates click/type/swipe actions → executes via ADB commands.

This is the clean abstraction: device becomes an API endpoint.

## /learn Agent Tool Access (Critical)

**Problem**: Haiku agents used in /learn cannot write files — they only have read tools.
**Fix**: Use `thor` subagent_type for /learn agents (thor has Read + Write + Edit).
**Impact**: Without this, /learn produces content that gets lost when context window compresses.

## Chrome Extension Mobile State

- `chrome.storage.session` → Chrome 102+ only, silent failure on older mobile
- `chrome.storage.local` → universal, use as default
- Background service worker survives popup close → use as message relay for running jobs
