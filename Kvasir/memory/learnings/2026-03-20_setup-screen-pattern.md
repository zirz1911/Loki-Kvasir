---
name: Setup screen UX pattern — honest animation + real signal
description: How to build a setup loading screen that syncs with real execution time
type: project
---

## Pattern: Honest Setup Screen

When building a "loading" screen that waits for a real async operation:

1. **Animate steps at realistic intervals** — measure actual execution time, spread steps proportionally. Fake UX that's 10x faster than reality breaks trust.
2. **Hold the final step open-ended** — the last step spins indefinitely until the real signal arrives. Never fake-complete something that hasn't actually completed.
3. **Fire the real operation immediately** — don't wait for animations. Fire the webhook on screen entry, animations play in parallel.
4. **Use a separate SSE event type** — `_setup: true` keeps setup signals separate from message history. Clean channels.

**Why:** User said "real execution is 1m 12s" after seeing the 10s fake timer. Mismatched UX erodes trust even if functional.

**How to apply:** Any setup/onboarding screen that waits for a real backend operation. Spread N steps across ~80% of expected duration, leave last step as open hold.
