# Lesson: Repo Rename Causes Silent Infrastructure Breaks

**Date**: 2026-04-11
**Source**: wrap: loki-pixfice-tmux-setup

## Pattern

When a project directory or repo is renamed, downstream scripts that reference the old name by hardcoded path will silently fail — not with errors, but by showing empty results or no-ops.

## Example

`Loki-Oracle` renamed to `Loki-Kvasir`. `Loki-Pixfice/scripts/setup.sh` still referenced:
- `ORACLE_DIR=/home/paji/Loki-Oracle` (directory no longer exists)
- Session name `loki-oracle` (config default `loki-oracle`, but CLAUDE.md now uses `loki-kvasir`)
- `FREYR_DIR=/home/paji/Freyr-Oracle` (also renamed to `Freyr-Kvasir`)

Result: tmux sessions were never created. UI ran on port 3456 but showed zero agents.

## Fix Pattern

After any project rename:
1. Grep all scripts for old name: `grep -r "Loki-Oracle\|loki-oracle" ~/Project/ ~/.config/`
2. Update setup scripts with new paths
3. Update config files that reference session/host names
4. Re-run setup to verify

## Broader Rule

Silent empty-state failures (app runs, shows nothing) are harder to diagnose than explicit errors. Always check config files AND setup scripts after any rename operation.
