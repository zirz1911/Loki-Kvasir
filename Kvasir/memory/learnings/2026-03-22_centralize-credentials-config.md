---
name: Centralize webhook credentials as named constants
description: Moving token/device_id/workflow_id to top-level constants prevents scattered hardcoding
type: feedback
---

Extract all webhook credentials into named constants at the top of the script — never inline them at call sites.

**Why:** User needed to swap `device_id` + `workflow_id` then immediately revert. Because everything was centralized (`TOKEN`, `DEVICE_ID`, `WF_OTP`, `WF_SWAP`), both the change and the revert were 2-line edits. If they were scattered across 4+ fetch calls, each would need individual edits with risk of missing one.

**How to apply:** Any time there are 2+ fetch calls using the same credentials, extract to constants before writing the second call. Don't wait until the third.
