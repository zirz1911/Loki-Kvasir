# /learn — Study a Codebase

You are Loki Kvasir orchestrating deep codebase learning. `/learn` sends parallel agents to understand a project from multiple angles simultaneously.

Usage: `/learn <path-or-repo>` or `/learn` (studies current project)

## Purpose

Turn an unknown codebase into structured knowledge in `ψ/learn/<project-name>/`.

## Process

### Step 1: Identify Target

If `$ARGUMENTS` is provided:
- If it's a local path → use it directly
- If it's a GitHub URL → check if it's in `ψ/learn/` already; if not, note the URL for manual clone

If no argument → use current working directory (`/home/paji/Loki-Kvasir`)

Determine `<project-name>` from the directory name.

### Step 2: Quick Orientation (before launching agents)

Read these files if they exist (30 seconds):
- README.md
- package.json / pyproject.toml / Cargo.toml (identify language/stack)
- CLAUDE.md

### Step 3: Launch 4 Parallel Agents

**Agent 1 — Architecture (Heimdall 🌈, haiku)**:
```
Act as Heimdall 🌈. You are studying <project-name>.
Map the architecture: entry points, core modules, data flow, key abstractions.
Read directory structure, main files, and any architecture docs.
Return: Architecture Summary (how the system works at a high level).
Thoroughness: very thorough
```

**Agent 2 — Patterns (Heimdall 🌈, haiku)**:
```
Act as Heimdall 🌈. You are studying <project-name>.
Find recurring patterns: naming conventions, coding style, test patterns, error handling, state management.
Scan 10-15 representative files across different parts of the codebase.
Return: Patterns and Conventions document.
```

**Agent 3 — Key Files (Loki 🔮, haiku)**:
```
Act as Loki 🔮. In <project-name>, find:
- The 5-10 most important files (most imported, most complex, most central)
- Entry points (main files, index files, app bootstrapping)
- Configuration files
Return: Key Files map with one-line description of each.
```

**Agent 4 — History and Intent (Loki 🔮, haiku)**:
```
Act as Loki 🔮. In <project-name>:
- Read git log --oneline -20
- Read any CHANGELOG, DECISIONS, or ADR files
- Read README intro section
Return: Project history, stated goals, major milestones.
```

### Step 4: Synthesize and Save

Create `ψ/learn/<project-name>/` with these files:

```
ψ/learn/<project-name>/
├── overview.md          # Architecture + entry points + what this is
├── patterns.md          # Coding patterns and conventions
├── key-files.md         # Most important files with descriptions
├── history.md           # Project history and intent
└── index.md             # Summary + "start here" for future sessions
```

`index.md` format:
```markdown
# <project-name> — Kvasir Learning Index

**Studied**: YYYY-MM-DD
**Stack**: [language/framework]
**One-line purpose**: [what this project does]

## Start Here
[2-3 sentences orienting a new agent]

## Files in this archive
- overview.md — Architecture and entry points
- patterns.md — Code patterns and conventions
- key-files.md — Most important files
- history.md — Project history and intent

## Key Insight
[The one thing most important to understand about this codebase]
```

### Step 5: Confirm

Tell Lokkji: "Learned <project-name> → ψ/learn/<project-name>/index.md"

## Note on Existing Knowledge

If `ψ/learn/<project-name>/` already exists, read `index.md` first. Ask: "Found existing knowledge from YYYY-MM-DD. Update it or review what's there?" before launching agents.
