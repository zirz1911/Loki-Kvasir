# gh repo sync vs git pull

**Date**: 2026-02-21
**Context**: Tried to use `gh repo sync` in the /update skill as a "gh-flavored" pull

## The Mistake

`gh repo sync` is designed to sync a **fork** from its **upstream parent** — not for pulling remote changes into a local working copy.

## What Works

```bash
# Pull latest into local repo (with gh auth)
git pull --rebase origin main

# gh repo sync is for:
gh repo sync owner/fork --source owner/upstream --branch main
```

## Rule

When Lokkji says "use gh" for pulling updates — `git pull --rebase` is still the right tool. gh doesn't replace git pull for local repos.

## Related Lesson

Skills that prescribe shell commands must be mentally traced or tested before committing. Wrong commands in skill files persist longer than wrong commands in chat.
