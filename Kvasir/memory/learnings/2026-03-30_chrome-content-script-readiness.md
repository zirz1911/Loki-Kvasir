---
name: Chrome content script readiness — ping before message
description: How to reliably send messages to content scripts in background tabs that may have been discarded
type: project
---

Never use a fixed delay (setTimeout) before sending messages to a Chrome extension content script.

**Why:** Chrome memory saver can discard background tabs. When the tab is switched to active, it reloads — the content script must re-initialize. A 500ms hardcoded delay works when the tab is warm, fails silently when the tab was discarded (which can take 5-30 seconds to restore).

**How to apply:**

1. Add a `ping` handler in content.js:
```javascript
if (request.action === 'ping') { sendResponse({ pong: true }); return; }
```

2. In background.js, wait for tab load completion:
```javascript
function bgWaitForTabComplete(tabId, timeoutMs = 30000) {
    return new Promise(resolve => {
        chrome.tabs.get(tabId, tab => {
            if (tab?.status === 'complete') { resolve(); return; }
            const l = (id, info) => { if (id === tabId && info.status === 'complete') { chrome.tabs.onUpdated.removeListener(l); resolve(); } };
            chrome.tabs.onUpdated.addListener(l);
            setTimeout(() => { chrome.tabs.onUpdated.removeListener(l); resolve(); }, timeoutMs);
        });
    });
}
```

3. Then retry-ping until content script responds:
```javascript
async function bgWaitForContentScript(tabId, retries = 20, delayMs = 1500) {
    for (let i = 0; i < retries; i++) {
        const ok = await new Promise(r => chrome.tabs.sendMessage(tabId, { action: 'ping' }, res => r(!chrome.runtime.lastError && res?.pong === true)));
        if (ok) return;
        await new Promise(r => setTimeout(r, delayMs));
    }
    throw new Error('Content script not responding');
}
```

**Why:** `bgWaitForTabComplete` catches the reload, `bgWaitForContentScript` catches the content script init time. Together they handle the full discard-and-restore cycle.
