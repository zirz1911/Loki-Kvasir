# Debug Rule: Reach for Reference Code After One Failed Attempt

**Date**: 2026-03-06
**Source**: rrr: Paji-Affiliate-Gen

## Pattern

When a bug survives one fix attempt:
1. Stop theorizing
2. Find a working implementation of the same problem
3. Read it carefully
4. Apply the pattern, not the theory

## Example

Video freeze bug in ffmpeg clip pipeline:
- Attempt 1: "source clips might have no audio" → add anullsrc fallback → still frozen
- Attempt 2: Read Paji-editz `core/video.py` → saw `-an` on all intermediate clips → applied → fixed

The reference code had the answer in 5 lines. Two rounds of hypothesis missed it.

## Rule

> After one failed fix attempt on a persistent bug, the next step is reference code — not another hypothesis.

## Related

- `2026-03-05_ffmpeg-clip-pipeline-pattern.md` — the specific ffmpeg pattern discovered
