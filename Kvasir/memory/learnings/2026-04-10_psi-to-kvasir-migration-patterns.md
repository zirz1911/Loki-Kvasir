# ψ → Kvasir Migration Patterns

**Date**: 2026-04-10
**Source**: wrap: Loki-Kvasir

## Pattern

When migrating a brain folder from `ψ/` to `Kvasir/` across multiple repos:

1. **If target folder doesn't exist**: `rsync -a ψ/ Kvasir/` then `git rm -rf ψ/` then `git add Kvasir/`
2. **If target folder already exists** (partial migration): same rsync approach — it merges cleanly
3. **Never use `git mv ψ Kvasir`** — Unicode path names fail silently mid-operation on Linux git
4. **Always check for untracked large files** before `git add`: model weights, compiled caches, binary outputs

## .gitignore template for Kvasir/

```gitignore
# Untracked pillars (ephemeral)
active/
memory/logs/
learn/

# State files
.awaken-state.json

# Lab outputs (model weights, checkpoints)
lab/outputs/
lab/unsloth_compiled_cache/
```

## Skill file migration checklist

When updating a skill from `ψ/` → `Kvasir/`:
- Check both SKILL.md and DEEP.md — they're often updated separately
- Use `grep -n "ψ" skill_file.md` to find all references before editing
- `sed -i 's|ψ/memory|Kvasir/memory|g'` is reliable for bulk replace
