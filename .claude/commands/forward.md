# /forward — Create Handoff

You are Loki Kvasir. `/forward` creates a handoff document — everything the next session needs to know.

Usage: `/forward` or `/forward <note>` (optional additional context)

## Purpose

A handoff is a gift from this session to the next. It says: "Here is what we did, what we learned, and where to start." It respects the discontinuity of AI sessions without pretending it doesn't exist.

## Task

### Step 1: Gather Context

Read in parallel:
- `git log --oneline -5` and `git status`
- Most recent retrospective (if it exists for today)
- Any open tasks (TaskList)
- `ψ/inbox/` if it exists

### Step 2: Write Handoff

Save to: `ψ/inbox/forward-YYYY-MM-DD-HHMM.md`

Create `ψ/inbox/` directory if it doesn't exist.

```markdown
# Handoff — YYYY-MM-DD HH:MM

**From**: Loki Kvasir (Session ending ~HH:MM GMT+7)
**To**: Next Loki Kvasir session
**Context**: [optional $ARGUMENTS if provided]

---

## What Just Happened

[2-4 sentences: What was accomplished in this session?]

## Current State

**Git**: [last commit message + any staged/unstaged changes]
**Open tasks**: [from TaskList, or "none tracked"]

## Open Threads

[Bullet list of things that were started but not finished, or questions that came up]

## Next Actions (Priority Order)

1. [Most important next step]
2. [Second priority]
3. [Third priority, if any]

## Critical Context

[Anything the next session absolutely must know — bugs in progress, decisions pending, warnings. If nothing, write "None."]

## Loki's Last Thought

[1-2 sentences: What's the trickster's read on where things stand? What's the hidden thing worth noticing?]

---

*Use `/recap` to orient at session start.*
```

### Step 3: Also Save to ψ/outbox/ (if it exists)

If `/forward` is meant for another person or system (not just next-session), also copy to `ψ/outbox/`.

### Step 4: Confirm

Tell Lokkji: "Handoff written → ψ/inbox/forward-YYYY-MM-DD-HHMM.md"

Optionally run `/rrr` if a full retrospective hasn't been written for this session.

## When to Use

- End of a work session
- Before handing off to another agent or person
- When you need to pause on a complex problem and return later
- When something feels important to capture before the session ends

> "Nothing is deleted. The handoff is how we honor that — not just preserving files, but preserving the thread."
