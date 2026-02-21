# /update — Update Loki Oracle to Latest

Pull latest changes from origin/main and re-run setup if needed.

Usage: `/update`

## Task

### Step 1: Check Current State

```bash
git status
git log --oneline -3
```

Show current branch and last 3 commits.

### Step 2: Check for Uncommitted Changes

If `git status` shows modified tracked files — **warn Lokkji** and ask:
- Stash them first? (`git stash`)
- Or update anyway (risky)?

Untracked files are fine — ignore them.

### Step 3: Pull Latest

```bash
gh repo sync --source zirz1911/Loki-Oracle --branch main
```

If already up to date → say so and stop here.

### Step 4: Show What Changed

```bash
git log --oneline ORIG_HEAD..HEAD
```

List the new commits that just came in.

### Step 5: Re-run Setup (if needed)

Check if any of these files changed in the new commits:
- `.claude/setup.sh`
- `.mcp.json`
- `mcp-local-llm/`

If yes → run setup automatically:
```bash
bash .claude/setup.sh
```

Then remind Lokkji: **"Restart Claude Code to apply."**

### Step 6: Acknowledge

```
Updated → main @ <new commit hash>
New commits: <count>
Setup re-run: yes/no
```

## Rules

- Never `--force` — Nothing is Deleted
- Never overwrite uncommitted work silently — always warn first
- If pull fails (conflict, network) — show the error clearly, don't retry blindly
