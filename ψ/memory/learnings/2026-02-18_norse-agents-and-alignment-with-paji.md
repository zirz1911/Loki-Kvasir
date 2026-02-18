# Norse Agents — Alignment with Existing Infrastructure

**Date**: 2026-02-18
**Context**: Building Norse Agent System after studying Paji repo
**Confidence**: High

## Key Learning

When building for a human who already has a mature AI system (Paji), don't reinvent — extend. Lokkji's Paji repo already has a fully developed Norse Agent philosophy with clear model mapping (local free → Gemini Flash → Claude). Loki Oracle's agent files should align with that mental model exactly.

The model mapping that works:
- **Haiku** for Thor/Loki/Heimdall — fast, cheap, handles 90% of requests. These are the workhorses.
- **Sonnet** for Tyr — when strategic thinking is needed but not production-critical
- **Opus** for Ymir — production-critical only. The rarity is the feature.

## The Pattern

Agent files in `.claude/agents/` use YAML frontmatter:

```markdown
---
name: agent-name
description: When to use this agent (used by Claude to auto-select)
tools: Read, Write, Edit, Bash, Grep, Glob
model: haiku | sonnet | opus
---
```

The `description` field is critical — it's what Claude uses to decide when to route to this agent automatically. Write it as "Use for: [specific scenarios]".

## Why This Matters

The Paji repo's 97% cost reduction comes from one discipline: **never use an expensive model when a cheap one will do**. Building Norse agents with the right model defaults enforces this discipline structurally — you can't accidentally use Opus for a file search if Loki (haiku) is the defined agent for that task.

The naming `loki-explorer.md` (not `loki.md`) matters: avoids collision with Loki Oracle's own identity while preserving the Norse mythology mapping that Lokkji already uses in Paji.

## Tags

`norse-agents`, `cost-optimization`, `claude-code-agents`, `haiku-first`, `model-selection`
