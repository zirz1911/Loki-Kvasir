---
name: Chrome Extension — Popup vs Side Panel + Mobile
description: Lessons from implementing cross-platform Chrome extension with popup/side panel modes
type: project
---

# Chrome Extension Popup + Mobile Lessons

## Rules

**Popup closes immediately if focus is stolen:**
`chrome.tabs.create()`, `chrome.windows.create()`, or any focus-shifting call in DOMContentLoaded → popup loses focus → auto-closes.
**Fix**: guard with `isPopupMode()` check, skip auto-open in popup.

**`default_popup` in manifest > dynamic `setPopup()`:**
manifest is loaded before any JS. Use it as universal fallback.
Desktop override: `chrome.action.setPopup({ popup: '' })` then `sidePanel.setPanelBehavior`.

**Feature detection > OS string for browser detection:**
```javascript
// ❌ fragile — Orion iOS doesn't return 'ios'
const isMobile = os === 'android' || os === 'ios';

// ✅ reliable — works on any browser without sidePanel API
if (!chrome.sidePanel) { /* use popup */ }
```

**MutationObserver > setTimeout for async DOM waits:**
`waitForVideoReady()` watches for new `<video>` elements or download buttons — real signal, not fake timer.

## Why

- Orion iOS (Kagi) doesn't return `os: 'ios'` from `getPlatformInfo()`
- Chrome popup has strict focus rules — any tab interaction closes it
- manifest `default_popup` is the only guaranteed cross-browser way to set popup
