# Static HTML + Canvas Animation + Vercel

**Date**: 2026-03-07
**Source**: rrr: Mins-gang

---

## Pattern 1: Vanilla Canvas Particle Animation

Self-contained background animation — no libraries, no dependencies.

```javascript
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
const PARTICLE_COUNT = 80;
const CONNECTION_DIST = 160;
const SCAN_SPEED = 0.4;

// Init
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

const particles = Array.from({ length: PARTICLE_COUNT }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.6,
    vy: (Math.random() - 0.5) * 0.6,
    r: Math.random() * 2 + 1,
}));

let scanY = 0;
let scanDir = 1;

function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw grid
    // Draw particles
    // Draw connection lines (distance < CONNECTION_DIST)
    // Draw scan beam (horizontal gradient line)
    // Move scan: scanY += SCAN_SPEED * scanDir; if out of bounds, flip scanDir

    requestAnimationFrame(loop);
}
loop();
```

Key details:
- `position: fixed; inset: 0; z-index: 0; pointer-events: none` on canvas
- All content wrapped in elements with `position: relative; z-index: 1`
- Resize handler keeps canvas = viewport size

---

## Pattern 2: Static HTML on Vercel

Zero config needed beyond `vercel.json`:

```json
{
  "cleanUrls": true,
  "trailingSlash": false
}
```

No framework, no build step, no `package.json`. Just push and it deploys.

---

## Pattern 3: Context Compaction Recovery

When a long session hits context limits and gets summarized:
1. Do NOT trust the summary as ground truth for code state
2. Run `git diff` — the diff IS the ground truth
3. Run `git status` — confirms what's staged/unstaged
4. Only then continue work

The summary is prose; the diff is math.
