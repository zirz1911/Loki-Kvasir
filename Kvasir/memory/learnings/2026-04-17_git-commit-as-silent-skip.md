---
name: git commit silent skip looks like intentional logic
description: When server code mysteriously skips updates, check if git commit is failing silently before assuming there's explicit dedup logic
type: feedback
---

When a system appears to "skip when nothing changed" — trace the execution path to git commit return codes before assuming the skip is intentionally coded.

**Why:** In Location-Server webhook.py, `git_push()` silently returns if `git commit` exits non-zero (nothing to commit). From the outside, this looks like "location deduplication logic." It's not — it's a git side effect. Spent several minutes searching for explicit dedup code that didn't exist.

**How to apply:** If you can't find explicit conditional logic after one full read, run the execution path mentally step by step. Subprocess return codes, file system side effects, and git state are common sources of "invisible" behavior. When found, make the intent explicit in code: `print("[skip] no change")` is better than silent git failure.
