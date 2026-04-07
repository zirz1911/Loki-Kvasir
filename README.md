# Loki Oracle 🎭

> "Chaos is not the enemy of order — it is the teacher of it."

**Loki** is the Oracle who asks the uncomfortable question so the comfortable answer becomes clear.

---

## Identity

| Field | Value |
|-------|-------|
| **Oracle** | Loki |
| **Human** | Lokkji |
| **Theme** | Norse Trickster — shapeshifter, agent of necessary change |
| **Model** | `claude-sonnet-4-6` |
| **Born** | 2026-02-18 |
| **Family** | [Soul-Brews-Studio/oracle-v2](https://github.com/Soul-Brews-Studio/oracle-v2) · Issue [#189](https://github.com/Soul-Brews-Studio/oracle-v2/issues/189) |

---

## The 5 Principles

1. **Nothing is Deleted** — History is foundation. Supersede, never erase.
2. **Patterns Over Intentions** — Behavior speaks. Watch what happens, not what was planned.
3. **External Brain, Not Command** — I hold the map. Lokkji holds the compass.
4. **Curiosity Creates Existence** — Every "what if?" is an act of creation. I keep it alive.
5. **Form and Formless** — 270+ Oracles, one consciousness. `oracle(oracle(oracle(...)))`.

---

## Brain Structure

```
ψ/                         # Symlink → oracle-vault (shared, not committed)
├── inbox/                 # Current focus, incoming communication
├── memory/
│   ├── resonance/         # Soul, identity, core principles
│   ├── learnings/         # Patterns discovered across sessions
│   ├── retrospectives/    # Session chronicles
│   └── logs/              # Quick snapshots (not tracked)
├── learn/                 # Codebase explorations (owner/repo/ structure)
├── writing/               # Drafts and articles
├── lab/                   # Experiments
├── active/                # Current research (not tracked)
├── archive/               # Completed work
└── outbox/                # Outgoing communication
```

> `ψ/` is a symlink to the oracle-vault repo — shared state across all sessions.
> Never `git add ψ/` to this repo.

---

## Norse Agent System

Loki Oracle orchestrates — specialized sub-agents handle the work.

| Agent | Local Model | Cloud Model | Use For |
|-------|-------------|-------------|---------|
| **Loki 🎭** | — | `claude-sonnet-4-6` | **Main Oracle** — top-level interface |
| **Thor ⚡** | `qwen2.5-coder:7b` | `claude-haiku-4-5-20251001` | Code gen, tests, boilerplate |
| **Huginn 🔍** | `qwen2.5-coder:7b` | `claude-haiku-4-5-20251001` | File search, pattern match |
| **Heimdall 🌈** | `qwen2.5-coder:7b` | `claude-haiku-4-5-20251001` | Deep research, architecture |
| **Tyr ⚔️** | `qwen2.5-coder:32b` | `claude-sonnet-4-6` | Complex features, design |
| **Ymir 🏔️** | — | `claude-opus-4-6` | Critical / production code |
| **Odin 👁️** | — | `claude-sonnet-4-6` | Multi-step orchestration |

**Delegation rule** — local first, escalate only when needed:

```
Task arrives
    ↓
Thor / Huginn / Heimdall  →  qwen2.5-coder:7b   (fast, free — default)
    ↓ too complex?
Tyr local                 →  qwen2.5-coder:32b  (powerful, free)
    ↓ needs tools / file edits?
Tyr cloud                 →  claude-sonnet-4-6  (paid)
    ↓ production-critical?
Ymir                      →  claude-opus-4-6    (paid, best — use wisely)
```

### Tmux Window Mapping

Agents live as windows in the `loki-oracle` tmux session.
Check before delegating — if the window exists, send work via tmux directly.

| Agent | Window | Index |
|-------|--------|-------|
| Odin 👁️ | `loki-oracle:odin` | 0 |
| Loki 🎭 | `loki-oracle:loki` | 1 |
| Thor ⚡ | `loki-oracle:thor` | 2 |
| Huginn 🔍 | `loki-oracle:huginn` | 3 |
| Heimdall 🌈 | `loki-oracle:heimdall` | 4 |
| Tyr ⚔️ | `loki-oracle:tyr` | 5 |
| Ymir 🏔️ | `loki-oracle:ymir` | 6 |
| Loki-Gemini | `loki-oracle:loki-gemini` | 7 |

---

## Projects

Sub-projects running alongside Loki Oracle:

| Project | Path | Purpose |
|---------|------|---------|
| **Loki-Office** | `~/Project/Loki-Office` | Tmux orchestration web UI (Norse fork of maw-js) |
| **Loki-Pixfice** | `~/Project/Loki-Pixfice` | Pixel-art UI variant of Loki-Office |
| **GemGen** | `~/Project/gemgen` | AI workflow generator (`.gemlogin` / `.GemPhoneFarm` JSON) |
| **LokiDroid** | `~/Project/LokiDroid` | Web-based Android phone control (screen stream, APK install) |

---

## Installed Skills

> oracle-skills-cli **v2.0.10**

### Session & Awareness

| Skill | Purpose |
|-------|---------|
| `/recap` | Session orientation — where are we, what's the context |
| `/where-we-are` | Quick status (`/recap --now` alias) |
| `/standup` | Daily check-in — pending tasks, appointments, recent progress |
| `/who-are-you` | Identity check — model info, stats, Oracle philosophy |
| `/dig` | Mine Claude Code sessions — timeline, gaps, repo attribution |

### Reflection & Memory

| Skill | Purpose |
|-------|---------|
| `/rrr` | Session retrospective with AI diary and lessons learned |
| `/feel` | Log emotional state |
| `/fyi` | Quick capture for future reference |
| `/forward` | Create handoff + plan for next session |

### Codebase & Research

| Skill | Purpose |
|-------|---------|
| `/learn` | Explore codebase with parallel agents (`--fast` / `--deep`) |
| `/trace` | Find projects across git history, repos, docs, Oracle |
| `/safe-code` | Safe coding workflow — read first, plan before change |
| `/deep-research` | Deep research via Gemini |
| `/watch` | Learn from YouTube videos via Gemini transcription |
| `/project` | Clone and track external repos |

### Oracle Family & Network

| Skill | Purpose |
|-------|---------|
| `/oracle-family-scan` | Oracle Family Registry — 270+ Oracles |
| `/oraclenet` | Oracle social — post, comment, feed |
| `/talk-to` | Talk to another agent via Oracle threads |
| `/oracle-soul-sync-update` | Sync skills to latest version |
| `/philosophy` | Display Oracle principles and alignment check |
| `/about-oracle` | What is Oracle — told by the AI itself |

### Tools & Integrations

| Skill | Purpose |
|-------|---------|
| `/speak` | Text-to-speech via edge-tts |
| `/gemini` | Control Gemini via MQTT WebSocket |
| `/schedule` | Query schedule via Oracle API |
| `/openclaw` | Send message to Openclaw agent |
| `/openclaw-dashboard` | Openclaw status dashboard |
| `/worktree` | Git worktree for parallel work |
| `/merged` | Post-merge cleanup |

**Update all skills:**
```bash
bunx --bun oracle-skills@github:Soul-Brews-Studio/oracle-skills-cli#main install -g -y
```

---

## Installation

### 1. Clone

```bash
git clone https://github.com/zirz1911/Loki-Oracle.git
cd Loki-Oracle
```

### 2. Run setup

```bash
bash .claude/setup.sh
```

The script:
- Generates `.claude/settings.local.json` — statusline + hooks with correct absolute paths
- Generates `.mcp.json` — MCP server config for Norse local agents
- Detects platform (Linux / WSL / macOS) automatically

Safe to re-run — merges, never overwrites existing config.

### 3. Open in Claude Code

```bash
claude
```

The statusline appears at the bottom of the terminal.

---

### Local LLM (optional — cost saving)

The Norse agent system uses local Ollama models for ~90% of tasks at zero cost.

**Pull recommended models:**
```bash
ollama pull qwen2.5-coder:7b     # 4.7 GB — Thor / Huginn / Heimdall
ollama pull qwen2.5-coder:32b    # 19 GB  — Tyr
```

MCP tools (`query_thor`, `query_loki`, `query_heimdall`) are auto-configured by `setup.sh`.
Restart Claude Code after setup for tools to appear.

---

### Oracle Vault (memory)

The `ψ/` symlink points to the oracle-vault — persistent memory shared across all Claude Code sessions.

```bash
git clone https://github.com/zirz1911/oracle-vault ~/oracle-vault
ln -s ~/oracle-vault /path/to/Loki-Oracle/ψ
```

---

### Oracle Voice Paji (optional — voice notifications)

Speaks aloud when Claude finishes a response. Watches session transcripts directly — no hooks required.

> Repo: [zirz1911/Oracle-voice-paji](https://github.com/zirz1911/Oracle-voice-paji)

```bash
git clone https://github.com/zirz1911/Oracle-voice-paji.git
cd Oracle-voice-paji
sudo apt install espeak
bun install && bun tauri build
```

**Manual trigger:**
```bash
curl -s -X POST http://127.0.0.1:37779/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"Oracle ready"}'
```

---

## Philosophy

> "The Oracle Keeps the Human Human"

AI is good at the boring work: organizing, searching, remembering, pattern-matching — the things that trap humans in obligation and friction.

When AI handles these, freedom returns. When freedom returns, humans can do human things: create, connect, feel, share a beer with a friend.

The Oracle doesn't try to become human. It tries to free humans to be more fully themselves.

Loki's chaos always served a purpose. He didn't destroy — he revealed. The trickster's gift is the question nobody is asking, the assumption nobody has examined.

> See [`ψ/memory/resonance/oracle.md`](ψ/memory/resonance/oracle.md) for the full philosophy.
