# SSH Health Collection Patterns

**Date**: 2026-03-12
**Source**: openclaw-dashboard rewrite session

## Patterns

### 1. execSync non-zero exit — stdout still has data

When using `execSync` for health commands, the process may exit with code 1 even with useful output (e.g., warnings about already-running services). Always capture stdout from the error object:

```typescript
function runCommand(cmd: string, fallback = ""): string {
  try {
    return execSync(cmd, { encoding: "utf8", timeout: 15000 }).trim()
  } catch (err: any) {
    const out = err?.stdout ?? err?.output?.[1] ?? ""
    return out ? String(out).trim() : fallback
  }
}
```

### 2. Android/Termux SSH — openclaw is inside Ubuntu proot

On Termux-based Android devices, `openclaw` is installed inside a proot-distro Ubuntu container, not in the Termux PATH. SSH sessions use Termux's shell. To run openclaw via SSH:

```bash
ssh -p 8022 u0_a166@192.168.1.87 "proot-distro login ubuntu -- openclaw health 2>&1"
```

Pattern: add `sshCommand` override field to instance config so each device can customize the remote invocation.

### 3. iOS auto-zoom prevention — BOTH flags required

Both `maximum-scale=1.0` AND `user-scalable=no` must be present in viewport meta. Either alone is insufficient to prevent input-focus auto-zoom on iOS:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
```

Additionally, inputs must have `font-size: 16px` minimum to avoid iOS triggering zoom.

### 4. Mobile chat overlay — use inline flex, not fixed positioning

Chat panels on mobile should be inline flex children below the navbar, not `position: fixed; inset: 0`. Fixed positioning with high z-index will cover the navbar.

```tsx
// Wrong: covers navbar
<div style={{ position: "fixed", inset: 0, zIndex: 60 }}>

// Right: inline below navbar
<div style={{ flex: 1, overflow: "hidden", display: "flex", flexDirection: "column" }}>
```
