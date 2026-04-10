# message-board: config extraction + admin panel patterns

**Date**: 2026-03-27
**Source**: message-board OTP dashboard session

## Patterns Discovered

### 1. State reset on view navigation — defense in depth
When navigating between views that have local state (timers, button states, countdowns), call the reset function in **both** places:
- On **exit** (back button)
- On **entry** (openDetail/openView)

One call is brittle. Both calls means you can't get stuck no matter how you navigate.

```js
function resetOTPState() {
  if (timer) { clearInterval(timer); timer = null }
  cdWrap.classList.remove('active')
  otpBtn.style.display = 'inline-block'
  otpBtn.disabled = false
  retryBtn.disabled = true
}

backBtn.addEventListener('click', () => { resetOTPState(); /* ... */ })
function openDetail(number) { resetOTPState(); /* ... */ }
```

### 2. Config extraction to JSON — never hardcode credentials in frontend
When a project has API tokens, device IDs, or dynamic lists (like phone numbers), move them to a server-side `config.json`:
- Server loads on startup
- Admin API allows live editing without restart
- Frontend never sees credentials — all calls proxy through server
- gitignore the config file

### 3. Always render visible error state in fetch calls
`.catch(() => {})` hides real bugs. Use:

```js
fetch('/api/cards')
  .then(r => r.json())
  .then(render)
  .catch(e => { container.innerHTML = `<div class="error">ERROR: ${e.message}</div>` })
```

### 4. Dynamic card rendering via SSE invalidation
When admin changes data, broadcast `{ _cards_updated: true }` via SSE. Main board re-fetches and re-renders automatically. No polling needed.

### 5. Custom modal pattern (replaces browser confirm())
CSS overlay with `opacity` + `pointer-events` transition, inner box with `transform: scale()`. Backdrop click closes. Returns a Promise.

```js
function customConfirm(msg) {
  overlay.classList.add('show')
  return new Promise(resolve => {
    resolveFn = (val) => { overlay.classList.remove('show'); resolve(val) }
  })
}
```
