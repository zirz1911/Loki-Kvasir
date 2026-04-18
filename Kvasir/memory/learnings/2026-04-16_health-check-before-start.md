---
name: Health check before attempting start
description: Check if service is already running before starting — EADDRINUSE is a symptom, not a problem
type: feedback
---

Always verify service health before attempting to start it. If port is in use and process is healthy, communicate "already running" and stop — don't proceed to start and surface an error to the user.

**Why:** Running `start` on a healthy service produces confusing EADDRINUSE errors that look like failure but aren't. The right sequence is: check → report status → only start if needed.

**How to apply:** For any "start X" request — first check if the process is already alive (`lsof -i:<port>` or `ps`), then report. Only attempt start if the check shows it's down.

---

Bonus lesson from same session: `EXCLUDED_SESSIONS = ["athena"]` pattern — filter at the source function (`listSessions`) not at each consumer. Keeps filtering logic in one place.
