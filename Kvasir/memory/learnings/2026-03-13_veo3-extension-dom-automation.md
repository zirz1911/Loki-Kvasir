---
name: VEO3 Extension — DOM Automation Patterns
description: Lessons from analyzing VEO3-Extention Chrome extension codebase
type: project
---

# DOM Automation Chrome Extension — Lessons

## Key Patterns

**File injection without native picker:**
```javascript
// Block click events on file input
document.addEventListener('click', blockHandler, true); // capture phase
// Then inject via native setter
const nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'files')?.set;
nativeSetter.call(fileInput, dataTransfer.files);
```

**Slate editor text input:**
```javascript
editable.dispatchEvent(new InputEvent('beforeinput', {
    inputType: 'insertText', data: text, bubbles: true, cancelable: true
}));
// Fallback:
document.execCommand('insertText', false, text);
```

**Stable selectors > class-based:**
- XPath text matching: `//div[text()="เริ่ม" or text()="Start"]`
- Attribute-based: `[data-slate-editor="true"]`, `[data-index="0"]`
- Icon text: `//button[.//i[normalize-space(text())="upload"]]`
- Avoid: CSS classes like `.sc-46973129-1` (generated, unstable)

## Process

- Always check GitHub vs local when repo has active development
- Unknown DOM selectors = inspect first, plan second
- `chrome.storage.session` for passing data between tabs
