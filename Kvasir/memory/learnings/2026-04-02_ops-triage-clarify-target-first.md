---
name: Ops triage — clarify target before diagnosing path
description: When debugging connectivity, ask what specific service/port the user is reaching before running network diagnostics
type: feedback
---

Clarify the target before diagnosing the path.

"Can't access Tailscale IP" could mean SSH, web UI, ping — each has completely different failure modes. One question up front saves multiple rounds of mis-scoped diagnostics.

**Fastest ops triage sequence:**
1. Ask: what specifically are you trying to reach? (SSH? web port? ping?)
2. `ss -tlnp | grep PORT` — is the service even running?
3. Then check network/firewall if service IS running

**Why:** This session wasted ~10 min on Tailscale network debugging when the actual problem was a dead `bun` process on port 3456.

**How to apply:** On any "can't access X" report, ask target+port before running network diagnostics.
