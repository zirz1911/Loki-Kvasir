---
name: Browser automation — dialog state & React click patterns
description: Lessons from building multi-step UI automation for a React app (Google Flow)
type: feedback
---

# Browser Automation — Dialog State & React Click Patterns

When automating multi-step flows in React SPAs:

**Why:** Each dialog has its own lifecycle. Closing one dialog to "confirm" selection destroys the upload button needed for the next upload. Re-open the trigger (e.g. `+` button) for each upload that requires its own dialog session.

**Re-click trigger for multiple uploads:**
If an upload dialog closes after selecting one file, click the trigger button again before the next upload. Don't try to keep one dialog open for multiple uploads — the UI wasn't designed for it.

**robustClick > humanClick for React:**
Raw `MouseEvent` dispatch often misses React fiber event handlers. `robustClick` walks `__reactProps$` up the DOM tree and calls `onClick` directly — use it for any button that doesn't respond to standard dispatch.

**XPath with icon text is more stable than hashed class names:**
`//button[.//i[normalize-space(text())="add_2"]]` survives CSS-in-JS rebuilds. Class names like `sc-46973129-1` will change. Prefer icon text, aria attributes, and role selectors.

**Storage as pipeline bridge:**
Use `chrome.storage.local` to pass artifacts between pipeline stages (e.g. generated image → video upload). Don't try to read DOM state from a previous step — store it explicitly when it's available.

**Get the full manual click sequence first:**
Every back button, every clear button, every modal dismiss — ask the user to describe the complete manual flow before writing automation. Missing one step = one more fix cycle.

**How to apply:** Apply these patterns to any browser extension or Playwright/Puppeteer automation involving multi-step dialogs in React apps.
