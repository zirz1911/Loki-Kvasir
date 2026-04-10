# Minimal Correct Change

**Date**: 2026-02-18
**Context**: README update — adding Norse Agent System and Installed Skills sections
**Confidence**: High

## Key Learning

When given an underspecified edit instruction ("update README"), the right move is:
1. Read the file as-is
2. Compare against the authoritative source (CLAUDE.md, code, etc.)
3. Add only what's missing
4. Stop at done

The temptation is to "improve while you're there" — clean up phrasing, restructure sections, add new ideas. Resist this. Scope creep in documentation is just as real as in feature development. The user said "update," not "rewrite."

## The Pattern

```
receive instruction → read current state → find delta → fill delta → stop
```

Not:

```
receive instruction → read current state → improve everything you see → stop (never)
```

## Why This Matters

Every unnecessary change is:
- A new diff to review
- A potential introduction of drift from the user's mental model
- Noise in git history

The **Nothing is Deleted** principle protects history. The **minimal correct change** principle protects clarity. Together they create a codebase that grows intentionally, not randomly.

This also applies to responses, conversations, and suggestions: say exactly what needs to be said, then stop.

## Tags

`documentation`, `discipline`, `scope`, `minimal-change`, `editing`
