# Lesson: Windows Filesystem Traversal in Claude Code

**Date**: 2026-02-18
**Source**: rrr: worldmap-project-exploration

## Pattern

On Windows with Claude Code bash shell, direct Unix-style filesystem commands fail silently on non-primary drives:

```bash
ls "D:/Paji AI/WorldMap/"     # FAILS — exit code 1
mkdir -p "D:/..."              # FAILS — exit code 1
cat "D:/..."                   # FAILS — exit code 1
```

## Solution

Always use PowerShell for D:\ (and other non-C:) filesystem operations:

```bash
# List directory
powershell.exe -Command "Get-ChildItem 'D:\Path\To\Dir' | Select-Object Name"

# List recursively with timestamps
powershell.exe -Command "Get-ChildItem 'D:\Path' -Recurse | Select-Object FullName, LastWriteTime | Sort-Object LastWriteTime -Descending"

# Create directory
powershell.exe -Command "New-Item -ItemType Directory -Force 'D:\Path\To\Dir'"

# Read file (small)
powershell.exe -Command "Get-Content 'D:\Path\file.txt'"

# Check if exists
powershell.exe -Command "Test-Path 'D:\Path\file.txt'"
```

## Why

The bash shell in Claude Code on Windows operates from a specific working directory (e.g., `D:\Loki-Oracle\Loki-Oracle`). It cannot traverse to other paths using Unix conventions because the MSYS/Git Bash layer doesn't map Windows drive letters the same way.

## Also Applies To

- `git` commands on files in other directories — use `-C path` flag or run via PowerShell
- File writes to other drives — always use `Write` tool with absolute Windows paths (they work fine)

## Note on Read/Write tools

The Claude Code `Read` and `Write` tools handle absolute Windows paths correctly (e.g., `D:\Paji AI\WorldMap\package.json`). Only the `Bash` tool has the traversal issue.
