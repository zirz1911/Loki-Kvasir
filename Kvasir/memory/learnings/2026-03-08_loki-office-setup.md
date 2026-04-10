# Loki-Office Setup Patterns

**Date**: 2026-03-08
**Source**: Loki-Office fork + Norse theming session

---

## Project Location

- **Repo**: https://github.com/zirz1911/Loki-Office
- **Local**: `/home/paji/Project/Loki-Office/`
- **Stack**: Bun + Hono (backend) + React 19 + Tailwind 4 + Three.js (frontend)
- **Port**: `:3456` → `/office`

## Setup Command

```bash
bash /home/paji/Project/Loki-Office/scripts/setup.sh
```

Creates:
- `loki-kvasir` session: windows `odin thor loki heimdall tyr ymir`
- `loki-office` session: server on `:3456`

## Pattern: Convention-Based Theming

`ROOM_COLORS` in `constants.ts` is keyed by **tmux session name**. Name your session correctly → UI theme applies automatically.

```
loki-kvasir → Asgard (gold)
midgard     → Midgard (green)
jotunheim   → Jotunheim (blue)
...
```

Same for agents: window named `thor` → ⚡ blue. No config needed.

## Pattern: Fork by Copy

When you want a clean-history fork:
```bash
cp -r source/ destination/
rm -rf destination/.git
cd destination && git init && git add . && git commit -m "init"
```

Cleaner than `gh repo fork` — new repo owns its own story from commit 0.

## bun PATH Issue on Fresh Machines

`bun run build:office` fails with `bunx: command not found` if bun isn't in shell PATH.

**Fix**: Source profile first, or call full path:
```bash
/home/paji/.bun/bin/bunx vite build
```

The `ecosystem.config.cjs` already uses full path for the interpreter — that pattern is correct for production.
