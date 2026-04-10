---
name: Add placeholder hint for profile_id input to prevent S/5 typo
description: Admin panel profile_id field has no format hint — S typed as 5 caused silent webhook failure
type: feedback
---

Add a placeholder or format hint to profile_id input fields in admin panels that accept opaque string identifiers.

**Why:** User typed `RFCY60256MV` (digit 5) instead of `RFCY602S6MV` (letter S) when adding cards via admin panel. Webhook fired but GemLogin silently rejected unknown profile — automation didn't run. No error shown anywhere. Diagnosed only by reading config.json manually.

**How to apply:** Whenever there's an input for an opaque external ID (profile_id, device_id, workflow_id), add `placeholder="e.g. RFCY602S6MV"` using an existing known-good value. Also consider noting case-sensitivity. Apply to admin.html profile_id and id inputs.
