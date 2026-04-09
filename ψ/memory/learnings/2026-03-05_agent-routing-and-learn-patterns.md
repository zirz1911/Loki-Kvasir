# Lesson: Agent Routing + /learn Patterns on Windows
**Date**: 2026-03-05 | **Source**: rrr: Loki-Kvasir

## Core Lessons

### 1. Explore agents = read-only, general-purpose = read+write
Explore agents cannot write files — they return output to main context only.
Use general-purpose agents whenever the task requires creating/editing files.
Use Explore agents when you want output returned to the conversation (not saved).

**Pattern**:
- `/learn` with save → general-purpose agent
- Quick codebase questions → Explore agent

### 2. ψ character in bash on Windows
UTF-8 paths with ψ break in bash variable expansion on Windows (Git Bash/MSYS2).
**Always hardcode the full path** — never assign ψ to a shell variable.
```bash
# BROKEN
PSI_DIR="D:/Loki-Kvasir/Loki-Kvasir/ψ/learn"
mkdir -p "$PSI_DIR/foo"  # encoding corruption

# WORKS
mkdir -p "D:/Loki-Kvasir/Loki-Kvasir/ψ/learn/foo"
```

### 3. ghq not installed — use manual D:/ghq/ convention
/learn skill assumes ghq for repo management and origin/ symlinks.
Without ghq, clone to `D:/ghq/[owner]/[repo]` manually.
Symlinks from ψ/learn → D:/ghq work if created manually.

### 4. System prompts as living documentation
gemgen pattern: 500+ line system prompts serve as both AI instructions AND block type reference documentation. AI reads it, humans read it, both get value. Apply to any AI-first project.

### 5. Stack evolution reveals intent
Reading a user's repos chronologically shows growth arc, not just current state.
2022 JS → 2024 Angular → 2025-Q4 Python AI → 2026 Rust+TypeScript+Kvasir = systems thinker emerging.
Always scan the full repo list and timeline before diving into any single repo.

## Tags
agent-routing, learn-skill, windows-bash, utf8, ghq, system-prompts, repo-archaeology
