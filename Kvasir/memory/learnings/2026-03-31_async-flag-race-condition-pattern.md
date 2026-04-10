---
name: Async flag race condition — set before the event, not in response to it
type: learning
date: 2026-03-31
project: VEO3-Extention
tags: [async, race-condition, chrome-extension, storage, concurrency]
---

# Lesson: Flags that gate concurrent behavior must be set before the triggering event

## Pattern

When multiple async listeners respond to the same event, and one of them sets a flag that the others check — the flag must be set **before** the event fires, not **in** the event handler.

## What happened

`sidepanelHandlingUpload` flag was set inside the `videoReady` message handler (sidepanel.js). `runTaskJob` in background.js also listened for `videoReady`. Both woke up simultaneously. background.js did `chrome.storage.local.get(['sidepanelHandlingUpload'])` — the get resolved before sidepanel's `set()` committed. Flag was `undefined`. background.js proceeded to upload without logo.

## Fix

Set `sidepanelHandlingUpload: true` at **Run All button click time** — before any flow begins, long before `videoReady` fires. Flag is guaranteed to be in storage by the time any concurrent listener checks it.

## Rule

> If a flag gates concurrent behavior triggered by event E, set the flag before E is possible — never inside the handler for E.

## Also learned

- `chrome.runtime.lastError` (connection failed) ≠ content script `{ error: ... }` response — distinguish before deciding to retry
- Chrome MV3 blocks `blob:` in `script-src` — FFmpeg.wasm blob Worker creation requires patching the library to use direct `chrome-extension://` URLs instead
