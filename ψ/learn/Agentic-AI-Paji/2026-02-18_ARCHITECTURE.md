# Agentic-AI-Paji — Architecture

**Date**: 2026-02-18
**Repo**: https://github.com/ContentsUS/Agentic-AI-Paji
**Owner**: Lokkji (ContentsUS)

---

## System Summary

Cost-optimized multi-agent AI system. Routes tasks to the cheapest appropriate model.

**Key result**: $0.75 → $0.02 per 10 tasks (**97.2% cost reduction**)

---

## Three-Phase Pipeline

```
User Request
    ↓
[Phase 1: GATEKEEPER]     → Filter context, reduce tokens 50–90%
    ↓
[Phase 2: ROUTER]         → Classify complexity
  ├─ SIMPLE  (40%) → Junior Developer (Gemini Flash / Local LLM) = $0.0021
  ├─ MODERATE(30%) → Junior + Claude Review                      = $0.0231
  └─ COMPLEX (30%) → Claude Sonnet (filtered context)            = $0.0231
    ↓
[Phase 3: FEEDBACK LOOP]  → Auto-test → fix → retry (max 3x) → escalate
```

---

## Core Components

| File | Phase | Role |
|------|-------|------|
| `gatekeeper.py` | 1 | Context filter — 69% token savings |
| `task_router.py` | 2.1 | Complexity classifier (SIMPLE/MODERATE/COMPLEX) |
| `junior_developer.py` | 2.2 | Cheap model executor (Gemini Flash or Local LLM) |
| `agent_coordinator.py` | 2.3 | Workflow orchestrator |
| `feedback_loop.py` | 3 | Self-healing: test → fix → retry |
| `test_executor.py` | 3.1 | Multi-framework test runner |

---

## Infrastructure (Docker)

| Service | Port | Role |
|---------|------|------|
| llama (Qwen 2.5-7B) | 8088 | Local LLM — FREE |
| embeddings (BAAI/bge-m3) | 8081 | Semantic search |
| qdrant | 6333 | Vector database |
| rag-api (FastAPI) | 8090 | RAG search API |
| mongo | internal | Document store |
| n8n | 5678 | Workflow automation |
| comfyui | host | Image generation |

---

## Norse Agent System (within Claude Code)

| Agent | Role | Model | Cost |
|-------|------|-------|------|
| **Thor ⚡** | Code generation | Qwen 32B (local) | FREE |
| **Loki 🔮** | Search & patterns | Qwen 7B GPU | FREE |
| **Heimdall 🌈** | Research & docs | Qwen 7B | FREE |
| **Tyr ⚔️** | Complex coding | Claude Sonnet | $$ |
| **Ymir 🏔️** | Production-grade | Claude Opus 4.6 | $$$$ |
| **Odin 👁️** | Main orchestrator | Sonnet/Opus | varies |

**Strategy**: Use local agents (Thor/Loki/Heimdall) for 90% of tasks → effectively FREE

---

## Sub-Projects

- `rag-api/` — FastAPI RAG with hybrid BM25 + vector search
- `mcp-local-llm/` — MCP server wrapper for local Qwen LLM
- `litellm-proxy/` — Single proxy for Claude + Gemini + Local (port 4000)
- `backend/` — TypeScript/Node.js REST API
- `time-tracker/` — Time tracking agent + Next.js dashboard
- `gemgen_workflows/` — 12 Gemlogin browser automation workflows
- `knowledge-base/` — Obsidian vault with project knowledge

---

## Key Integrations

- **Claude Code**: 9 custom slash commands (nnn, gogogo, jjj, ggg, lll, ccc, rrr, www, ttt)
- **LiteLLM**: Routes `claude-sonnet-4-5` → local Qwen (transparent cost swap)
- **MCP**: Local LLM tools available inside Claude Code sessions
