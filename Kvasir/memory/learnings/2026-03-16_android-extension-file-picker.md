---
name: Android Extension File Picker + Mobile Tab Behavior
description: File picker blocked on Android via JS .click(); label-for fix and lazy tab opening
type: feedback
---

## Android blocks indirect `input.click()`

On Android (Quetta, Chrome, Orion), `input.click()` called from a JavaScript event handler is treated as an indirect user gesture and blocked. The file picker never opens — no error, no feedback.

**Fix:** Replace the `<div>` wrapper with `<label for="inputId">`. The browser opens the file picker natively when the label is tapped — no JS required.

```html
<!-- Before (broken on Android) -->
<div id="uploadArea">
  <input type="file" id="fileInput" hidden>
</div>

<!-- After (works everywhere) -->
<label id="uploadArea" for="fileInput">
  <input type="file" id="fileInput" style="display:none">
</label>
```

**Also required:**
- Any buttons inside the label must have `type="button"` explicitly (default is `type="submit"` in form context)
- The button's click handler needs `e.preventDefault()` to stop the label from also triggering the file picker

## Don't auto-open tabs on extension load

On mobile browsers (Quetta/Android), extensions opening tabs on startup causes crashes or unexpected behavior.

**Rule:** Never call `chrome.tabs.create()` in `DOMContentLoaded` or on extension load. Only open tabs lazily when a specific user action requires it.

**Why:** Desktop Chrome handles eager tab creation gracefully. Mobile browsers may not have a stable tab context ready when the extension UI first opens.
