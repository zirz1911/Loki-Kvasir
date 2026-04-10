# Local LLM as Code Generator — Review Workflow Lessons

**Date**: 2026-02-22
**Source**: RateLimiter generation + test session via MCP local-llm tools

---

## 1. defaultdict(float) ≠ "uninitialized timestamp"

**Problem**: Using `defaultdict(float)` for timestamps initializes to `0.0` (Unix epoch, Jan 1 1970).
Any elapsed-time calculation on first access yields ~1.7 billion seconds, filling token buckets immediately.

**Fix options**:
```python
# Option A: check for 0.0
if self.last_refill_time[key] == 0.0:
    self.last_refill_time[key] = now  # init without refilling

# Option B: use None sentinel
self.last_refill_time: dict[str, float | None] = {}
if self.last_refill_time.get(key) is None:
    self.last_refill_time[key] = now
```

---

## 2. Local LLM tests need behavioral contract, not just code

When asking local LLM to generate tests, it assumes behavior from reading the code.
If the code has non-obvious initialization behavior (e.g., clock starts on first call, not constructor),
the generated tests will be wrong.

**Fix**: Include docstring or usage example in the prompt:
```python
# Bad prompt:
"Write pytest tests for this class: [code]"

# Good prompt:
"Write pytest tests. Note: first allow() call always returns False (initializes clock).
Tokens only accumulate after first call. [code]"
```

---

## 3. compare_models is for short-medium prompts only

qwen2.5-coder:32b (19GB) is slow for complex tasks.
Running both models in parallel means total time = max(7b_time, 32b_time).
For production use, complex prompts timeout before 32b responds.

**Rule of thumb**: use compare_models for prompts that 7b answers in <10s.
For anything longer, query each model separately or use 7b only.

---

## 4. Local LLM workflow pattern that works

```
query_local_llm → generate code
    ↓ review: find obvious bugs
fix in editor
    ↓
query_local_llm → generate tests (with behavioral context)
    ↓ run tests
fix remaining bugs revealed by tests
    ↓
commit + push
```

This catches two categories of bugs:
- **Logic bugs**: caught by human review (missing token deduction)
- **Contract bugs**: caught by tests (epoch initialization)

**Tags**: `local-llm`, `testing`, `rate-limiter`, `defaultdict`, `workflow`
