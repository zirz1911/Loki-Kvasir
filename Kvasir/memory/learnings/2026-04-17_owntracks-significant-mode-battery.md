---
name: OwnTracks "Significant" mode stops sending when stationary
description: OwnTracks iOS in Significant mode uses iOS CLLocationManager significant-change API — doesn't fire when phone is stationary, regardless of battery changes
type: feedback
---

When OwnTracks battery isn't updating on dashboard, check if the phone has been stationary — not whether the server code is correct.

**Why:** OwnTracks iOS "Significant" monitoring mode uses Apple's CLLocationManager significant-change API. This API only fires when the device moves ~500m+ (cell tower handoff). Stationary phone = zero OwnTracks pings = stale battery on dashboard. This is expected iOS behavior, not a bug.

**How to apply:** Before investigating server-side battery tracking code, run `git log` on the location repo — if last commit is >30 minutes ago and device should be stationary, suspect OwnTracks mode. Fix: change OwnTracks monitoring mode from "Significant" to "Move" or enable periodic ping. The server-side battery deduplication fix handles battery-only updates correctly once OwnTracks actually sends them.
