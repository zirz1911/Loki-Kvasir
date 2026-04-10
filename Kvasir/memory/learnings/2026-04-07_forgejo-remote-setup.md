# Forgejo Remote Setup — Dual Remote Pattern

**Date**: 2026-04-07
**Source**: Session — forgejo-setup

## Patterns Discovered

### Add Forgejo as Second Remote
```bash
git remote add forgejo https://<forgejo-url>/<user>/<repo>.git
git push forgejo main
```

### Credential Store (non-TTY safe)
```bash
# Store token once, never type again
git config credential.helper store
printf "https://<user>:<token>@<forgejo-host>\n" >> ~/.git-credentials
```

### Dual Remote Push
```bash
# Push to both GitHub and Forgejo
git push origin main && git push forgejo main
```

### Set Upstream Tracking
```bash
git push -u forgejo main  # tracks forgejo/main in git status
```

## Context
- Forgejo = self-hosted Git (Gitea fork) for company internal use
- Pattern: `origin` = GitHub (public), `forgejo` = company (internal)
- Token-in-URL is anti-pattern — always use credential store
- Non-TTY environments (tmux, CI) can't do interactive password prompts
