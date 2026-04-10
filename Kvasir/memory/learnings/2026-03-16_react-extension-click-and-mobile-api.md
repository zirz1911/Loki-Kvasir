---
name: React Extension Click + Mobile API Patterns
description: Reliable click strategies for React apps from extensions, and mobile browser API differences
type: feedback
---

## React 17+ Click from Extensions

`.click()` alone does NOT trigger React event handlers. React 17+ delegates all events to the root container — a synthetic click that doesn't bubble through the real DOM chain is ignored.

**Working pattern (robustClick):**
1. `dispatchFullClickSequence` — pointerdown → mousedown → pointerup → mouseup → click (all with real coordinates, bubbles:true, composed:true)
2. Walk `__reactProps$` up the DOM tree (up to 8 levels) and call `onClick` directly
3. Walk `__reactFiber$` memoizedProps tree (up to 15 levels) and call `onClick`
4. Native `el.click()` as final fallback

**Why:** React's delegated listener at the root sees real DOM events that bubble. The `composed:true` flag crosses shadow DOM. Real coordinates prevent React from filtering out "ghost" clicks.

## Mobile/Orion Extension API (Callback vs Promise)

On Orion iOS and some Android browsers, `chrome.runtime.sendMessage()` returns `undefined` (callback-based API) instead of a Promise.

Calling `.catch()` on `undefined` = TypeError that crashes the content script.

**Fix — `safeSendMessage(msg)`:**
```javascript
function safeSendMessage(msg) {
    try {
        const result = chrome.runtime.sendMessage(msg);
        if (result && typeof result.catch === 'function') result.catch(() => {});
    } catch (e) { /* context closed */ }
}
```

## Virtuoso Virtual List — "Latest Item" Selector

Flow uses Virtuoso for its media grid. The most recent item is always in `[data-index="0"]`.

- Video tiles: `.sc-c462af31-0` (contains `<video>`)
- Image tiles: `.sc-5923b123-0` (contains `<img>`)

```javascript
const firstRow = document.querySelector('[data-index="0"]');
const latestVideoTile = firstRow?.querySelector('.sc-c462af31-0');
```

## Language-Agnostic Icon Selectors

Material Icons `<i>` tag text is always the English icon name, regardless of UI language.

```xpath
//button[@aria-haspopup='menu'][.//i[normalize-space(text())='download']]
```

This finds the download button in Thai, English, Japanese UI equally.

**Why:** Material Icons renders the icon name as text content inside `<i>`. Google never translates this — it's a glyph lookup key, not visible text.
