# DESIGN.md + Skill Harvest Patterns

**Date**: 2026-04-10
**Source**: wrap: Loki-Kvasir

## Pattern 1: DESIGN.md install

```bash
npx getdesign@latest add [brand]   # linear.app, notion, vercel, stripe, etc.
```

Content hosted behind JS rendering — **WebFetch won't work**. Use the CLI.
Drop in project root → every AI agent reading that project knows the UI spec automatically.

**Good matches:**
- Dev tool / dark UI → `linear.app`
- Content / messaging app → `notion`
- SaaS / docs → `vercel` or `mintlify`

## Pattern 2: Post-parallel-agent verification

Always immediately verify output after parallel agents complete:
```bash
for SLUG in "owner/repo1" "owner/repo2"; do
  echo "--- $SLUG ---"
  ls learn/$SLUG/DATE/ 2>/dev/null || echo "(empty — agent failed to write)"
done
```

Catch missing files immediately, not at the end.

## Pattern 3: Skill extraction from ECC

Everything-claude-code (`affaan-m/everything-claude-code`) has 181 skills. Best ones for Kvasir:
- `agentic-engineering` — eval-first, 15-min units, model routing
- `continuous-agent-loop` — loop selection, failure modes, recovery
- `mcp-server-patterns` — tools/resources/prompts, stdio vs HTTP

Read skill, adapt to Kvasir context (Thai description + Norse agent mapping), write to `~/.claude/skills/`.
