---
name: Duplicated CARDS config across server and frontend is a sync risk
description: CARDS object exists in both server.js and index.html — every addition requires two edits
type: project
---

The `CARDS` config mapping phone numbers to profile_id/id is duplicated in both `server.js` and `public/index.html`. Currently 16 entries × 2 files.

**Why:** Started as frontend-only, then server needed it too for webhook calls. No one stopped to centralize it.

**How to apply:** Propose `/cards` endpoint on server + `fetch('/cards')` on frontend load when the user next asks about adding numbers or modifying card config. This is the right moment to fix the duplication — not mid-session when it's not the focus.
