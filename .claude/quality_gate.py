#!/usr/bin/env python3
"""
ARIA-style Quality Gate for Loki-Kvasir learnings.

Scores a learning on 4 dimensions:
  pattern     (0-3) — is this a recurring pattern, not a one-time incident?
  actionable  (0-3) — can future-Kvasir act on this in the next session?
  hard_lesson (0-2) — did this cause a visible mistake/wasted work before?
  non_obvious (0-2) — not derivable from docs / code / common sense?

Total 0-10:
  ≥ 7  → approved   ✅  keep as learning
  4-6  → quarantine ⚠️  needs 1+ more incidents to confirm
  < 4  → rejected   ❌  too ephemeral or already obvious

Usage:
  # Interactive scoring
  python3 quality_gate.py path/to/learning.md

  # From a pipe (just score the text)
  echo "some learning text" | python3 quality_gate.py -

  # Batch: score all unreviewed learnings
  python3 quality_gate.py --batch
"""
import sys, json, re
from pathlib import Path
from datetime import datetime, timezone, timedelta

BKK = timezone(timedelta(hours=7))
KVASIR_ROOT = Path("/home/paji/Loki-Kvasir")
LEARNINGS_DIR = KVASIR_ROOT / "Kvasir/memory/learnings"
GATE_LOG = KVASIR_ROOT / "Kvasir/memory/logs/quality_gate.jsonl"


CRITERIA = {
    "pattern":     ("Is this a RECURRING pattern (not a one-time incident)?",  3),
    "actionable":  ("Can future-Kvasir act on this immediately?",               3),
    "hard_lesson": ("Did this cause a visible mistake or wasted work?",         2),
    "non_obvious": ("Is this non-obvious (not in docs / common sense)?",        2),
}

def score_interactive(text: str, filename: str = "") -> dict:
    print(f"\n{'='*60}")
    print(f"📋 Quality Gate: {filename or 'learning'}")
    print(f"{'='*60}")
    print(f"\n{text[:400]}\n")
    print(f"{'─'*60}")
    print("Score each criterion (0 = no, max shown in brackets):\n")

    scores = {}
    for key, (question, max_score) in CRITERIA.items():
        while True:
            try:
                val = input(f"  {question}\n  [{key}] 0-{max_score}: ").strip()
                n = int(val)
                if 0 <= n <= max_score:
                    scores[key] = n
                    break
                print(f"  ⚠️  Enter 0-{max_score}")
            except (ValueError, KeyboardInterrupt):
                scores[key] = 0
                break

    return scores

def verdict(total: int) -> tuple[str, str]:
    if total >= 7:
        return "approved", "✅"
    elif total >= 4:
        return "quarantine", "⚠️"
    else:
        return "rejected", "❌"

def log_result(filename: str, scores: dict, total: int, status: str):
    GATE_LOG.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": datetime.now(BKK).isoformat(),
        "file": filename,
        "scores": scores,
        "total": total,
        "status": status,
    }
    with open(GATE_LOG, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def score_file(path: Path):
    text = path.read_text(encoding="utf-8")
    # strip frontmatter
    content = re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL).strip()
    scores = score_interactive(content, path.name)
    total = sum(scores.values())
    status, icon = verdict(total)

    print(f"\n{'─'*60}")
    print(f"  Total: {total}/10  →  {icon} {status.upper()}")
    for k, v in scores.items():
        max_v = CRITERIA[k][1]
        print(f"    {k:<12} {v}/{max_v}")
    print(f"{'─'*60}\n")

    log_result(str(path), scores, total, status)

    if status == "rejected":
        confirm = input("  Delete this learning? [y/N]: ").strip().lower()
        if confirm == "y":
            path.unlink()
            print(f"  🗑️  Deleted: {path.name}")

    return status

def batch_score():
    # Only score files NOT already in quality_gate.log
    reviewed = set()
    if GATE_LOG.exists():
        for line in GATE_LOG.read_text().splitlines():
            try:
                r = json.loads(line)
                reviewed.add(Path(r["file"]).name)
            except Exception:
                pass

    files = sorted(LEARNINGS_DIR.glob("*.md"))
    pending = [f for f in files if f.name not in reviewed]

    if not pending:
        print("✅ All learnings already reviewed.")
        return

    print(f"📋 {len(pending)} learnings pending quality gate\n")
    for i, f in enumerate(pending, 1):
        print(f"[{i}/{len(pending)}]", end="")
        result = score_file(f)
        if i < len(pending):
            cont = input("  Continue? [Y/n]: ").strip().lower()
            if cont == "n":
                break

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] == "--batch":
        batch_score()
    elif args[0] == "-":
        text = sys.stdin.read()
        scores = score_interactive(text, "stdin")
        total = sum(scores.values())
        status, icon = verdict(total)
        print(f"\n{icon} {status.upper()} ({total}/10)")
        print(json.dumps({"scores": scores, "total": total, "status": status}, indent=2))
    else:
        path = Path(args[0])
        if path.exists():
            score_file(path)
        else:
            print(f"File not found: {path}", file=sys.stderr)
            sys.exit(1)
