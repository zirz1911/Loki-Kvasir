# Agentic-AI-Paji — Quick Reference

**Date**: 2026-02-18

---

## What It Is

Lokkji's personal AI infrastructure. Multi-agent system that routes tasks intelligently to save 97% on AI API costs while maintaining quality.

**Philosophy**: ใช้ Claude เฉพาะตอนจำเป็นจริงๆ — ที่เหลือใช้ Gemini Flash หรือ Local LLM (free)

---

## Slash Commands ใน Claude Code

| Command | หน้าที่ |
|---------|---------|
| `/nnn` | วางแผน feature ใหม่ (ใช้ Gemini 2.5 Pro) |
| `/gogogo` | รัน plan step-by-step |
| `/jjj` | route task ไปหา agent ที่ถูกที่สุด |
| `/ggg` | filter context ก่อนส่ง Claude (ประหยัด 50–90%) |
| `/lll` | ดู project status: issues, PRs, commits |
| `/ccc` | save session context + compact |
| `/rrr` | retrospective (AI Diary) |
| `/www` | check/restart MCP worker |
| `/ttt` | ส่ง message ไป tmux session อื่น |

---

## How to Run

```bash
# Setup
pip install google-generativeai requests
export GEMINI_API_KEY="..."
export LOCAL_LLM_URL="http://localhost:8088/v1/chat/completions"

# Test pipeline
python3 test_gatekeeper.py
python3 test_task_router.py
python3 test_phase3.py

# Full Docker stack
docker-compose up -d

# Speed check
python benchmark_speed.py
```

---

## Performance

| Metric | Result |
|--------|--------|
| Cost reduction | **97.2%** |
| Test accuracy | 100% (29/29) |
| Router accuracy | 100% (20/20) |
| Junior success rate | 80%+ |
| Self-healing rate | 33% (no Claude needed) |
| LLM speed (GPU) | 80–100 tokens/s |

---

## Cost Breakdown

```
1,000 tasks/month:
Claude-only:     $75.00
+ Gatekeeper:    $23.25  (69% saved)
+ Router:        $15.00  (80% saved)
+ Self-healing:   $2.10  (97% saved)
```

---

## Current Status (Jan 2026)

- Phase 1–3 pipeline: **complete**
- 9 Claude Code skills: **deployed**
- Time Tracker sub-project: **in progress**
- Fine-tuning pipeline: **working**
- RAG API: **running on Docker**
- Gemlogin workflows: **12 validated**

---

## Key Files to Know First

```
CLAUDE.md            → How Lokkji wants Claude to behave in this repo
README.md            → Full system overview
QUICK_START.md       → Setup guide
agent_coordinator.py → Main entry point
task_router.py       → Complexity classifier
gatekeeper.py        → Token reducer
.claude/skills/      → All 9 custom commands
```
