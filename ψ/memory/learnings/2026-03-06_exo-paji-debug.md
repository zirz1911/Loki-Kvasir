# Lesson: Exo-Paji Startup & Model Loading Debugging

**Date**: 2026-03-06
**Source**: rrr: exo-paji-debug

## Patterns Discovered

### uv run in Rust workspace = cargo recompile every time
- `uv run <script>` detects workspace members and triggers `cargo rustc` even when `.so` already built
- Fix: call `.venv/bin/<script>` directly — bypasses uv entirely, instant start

### Pre-flight for exo
```bash
pkill -f ".venv/bin/exo"   # clear stale processes
pkill ollama                # free Metal GPU memory
# check free RAM > 500MB before loading models
./start-exo-safe.sh
```

### Silent subprocess hang = memory or IPC, not code
- If `LoadModel` logs `Fast synch flag: 0` then goes silent for minutes → runner subprocess hung
- Most likely cause: RAM < 200MB free, causing mlx_lm imports to thrash
- Secondary cause: Ollama holding Metal GPU memory, blocking MLX allocation

### mlx_lm import cost
- Clean (no other ML process): ~10s
- Under memory pressure: can hang indefinitely (no timeout in runner_supervisor)

### Ollama login item
- Ollama installs as macOS login item — respawns after every reboot silently
- Always kill before running exo on same machine
