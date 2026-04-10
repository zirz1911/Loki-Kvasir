# Chrome Extension Web Automation Patterns

**Date**: 2026-03-13
**Source**: VEO3-Extension — Google Labs Flow automation

---

## Key Patterns

### 1. Block native file input dialog
```javascript
// Capture phase intercepts BEFORE browser activates file picker
document.addEventListener('click', (e) => {
    if (e.target.type === 'file') {
        e.preventDefault();
        e.stopImmediatePropagation();
    }
}, true); // <-- capture: true is critical
```

### 2. Inject file into React/Radix input
```javascript
const nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'files')?.set;
if (nativeSetter) nativeSetter.call(fileInput, dataTransfer.files);
fileInput.dispatchEvent(new Event('change', { bubbles: true }));
```

### 3. Insert text into Slate editor
```javascript
editable.focus();
editable.dispatchEvent(new InputEvent('beforeinput', {
    bubbles: true, cancelable: true,
    inputType: 'insertText', data: text
}));
```

### 4. Open Radix UI dropdowns
```javascript
// .click() alone doesn't work — need full pointer sequence
['pointerdown','mousedown','pointerup','mouseup','click'].forEach(type => {
    el.dispatchEvent(new MouseEvent(type, { bubbles: true, cancelable: true, view: window, button: 0, buttons: 1, composed: true }));
});
```

### 5. Detect upload completion (media library)
```javascript
// Watch for img src change rather than counting DOM nodes (virtualized lists lie)
const srcBefore = document.querySelector('[data-index="0"] img')?.src;
// poll until src changes → new item at top
```

### 6. MutationObserver caveat
Always block pre-existing elements AND watch for new ones:
```javascript
document.querySelectorAll('input[type="file"]').forEach(block); // existing
const obs = new MutationObserver(() => document.querySelectorAll('input[type="file"]').forEach(block));
obs.observe(document.body, { childList: true, subtree: true });
```
