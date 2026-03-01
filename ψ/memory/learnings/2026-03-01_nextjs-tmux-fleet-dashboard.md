# Next.js Fleet Dashboard + tmux Health Parsing

**Date**: 2026-03-01
**Source**: openclaw-dashboard build session
**Tags**: nextjs, tmux, fleet-monitoring, dashboard, openclaw

---

## Pattern: tmux-based health detection in Next.js API routes

When building a dashboard that polls local tmux sessions, use `execSync` with explicit timeouts to prevent hangs:

```typescript
function hasTmuxSession(session: string): boolean {
  try {
    execSync(`tmux has-session -t "${session}"`, { timeout: 3000 })
    return true
  } catch {
    return false
  }
}

function captureTmuxPane(session: string): string {
  try {
    return execSync(`tmux capture-pane -t "${session}" -p 2>/dev/null | tail -20`, {
      encoding: "utf8",
      timeout: 5000,
    }).trim()
  } catch {
    return ""
  }
}
```

Key: always wrap in try/catch — tmux returns non-zero exit code when session doesn't exist.

---

## Pattern: Openclaw health output parsing

These regex patterns match Openclaw's `health` command output. Translated from the shell script at `.claude/openclaw-dashboard.sh`:

```typescript
// Telegram status
if (/Telegram:\s*ok/i.test(output)) return "ok"
if (/Telegram:/i.test(output)) return "error"
return "unknown"

// Gateway status
if (/Gateway.*ok|gateway.*online/i.test(output)) return "ok"
if (/error|Error|fail|1008|reject/i.test(output)) return "error"
return "unknown"

// Agent status
if (/Heartbeat interval|agent:main/i.test(output)) return "active"
if (/Running|Musing/i.test(output)) return "running"
return "idle"
```

---

## Pattern: Next.js dynamic API route for server-side shell commands

Mark the route as dynamic to prevent static generation:

```typescript
// app/api/fleet/route.ts
export const dynamic = "force-dynamic"

export async function GET() {
  const fleet = collectFleetStatus()  // runs execSync
  return NextResponse.json(fleet)
}
```

Without `force-dynamic`, Next.js may try to pre-render the route at build time and fail.

---

## Pattern: Auto-refresh with countdown in React

```typescript
const REFRESH_INTERVAL = 30_000

useEffect(() => {
  fetchFleet()
  const timer = setInterval(fetchFleet, REFRESH_INTERVAL)
  return () => clearInterval(timer)
}, [fetchFleet])

// Countdown resets when lastRefresh changes
useEffect(() => {
  const tick = setInterval(() => {
    setCountdown((c) => (c > 0 ? c - 1 : 0))
  }, 1000)
  return () => clearInterval(tick)
}, [lastRefresh])
```

---

## Known limitation: synchronous collector

`collectFleetStatus()` calls tmux commands serially. For >5 instances or SSH-based instances, convert to async:

```typescript
export async function collectFleetStatus(): Promise<InstanceStatus[]> {
  return Promise.all(INSTANCES.map(getInstanceStatusAsync))
}
```

---

## Repo

- **GitHub**: https://github.com/zirz1911/openclaw-dashboard
- **Local**: `/Users/paji/Desktop/Paji/openclaw-dashboard/`
- **Stack**: Next.js 15 (App Router), TypeScript, Tailwind CSS
