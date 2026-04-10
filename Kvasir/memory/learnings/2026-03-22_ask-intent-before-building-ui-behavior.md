---
name: Ask intent before building UI behavior for automation endpoints
description: "begin-setup" was built to auto-navigate UI, but user just wanted logging — clarify before building
type: feedback
---

Ask about UI behavior intent before implementing it for automation-triggered endpoints.

**Why:** Built `POST /begin-setup` to auto-open setup view when automation sends a number. User actually just wanted to log/display the number — no navigation. The auto-navigate code was stripped out a few messages later. "begin-setup" sounds like it should navigate, but the actual need was "show me what numbers automation is sending."

**How to apply:** When adding an endpoint that automation calls to "trigger" something, ask: "Do you want the UI to navigate/change automatically when this is called, or just record/display it?" These are different enough that building the wrong one wastes a round-trip.
