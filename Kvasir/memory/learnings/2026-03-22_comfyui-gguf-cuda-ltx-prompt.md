# ComfyUI GGUF CUDA Mismatch + LTX Prompt Enhancement Cost

**Date**: 2026-03-22
**Source**: ComfyUI LTX-2.3 slow generation debug session

## GGUF Approach — CUDA Version Wall

ComfyUI-GGUF node requires PyTorch compiled with CUDA 13.0 (`cu130`).

Check your CUDA version before attempting:
```bash
python -c "import torch; print(torch.version.cuda)"
# Must be 13.0 for GGUF; cu124 = blocked
```

**If you have cu124 (CUDA 12.4)**: GGUF approach is blocked without recompiling PyTorch.

## LTXVGemmaEnhancePrompt — Hidden Cost

This node does **autoregressive text generation** (not just encoding).

- Default: 256 new tokens
- Speed on CPU with 8GB VRAM: ~27s/token
- Total time for default: **~1.7 hours** just for prompt enhancement

### Fix Options

**Option A — Remove the node**: Use `LTXVConditioning` directly with a well-written prompt.

**Option B — Reduce tokens**:
- `max_new_tokens`: 64–128 instead of 256
- Time: 29–57 minutes (still slow but usable)

**Option C — Quick prompt**: Write a detailed prompt yourself → skip enhancement entirely.

**Best for 8GB VRAM**: Remove `LTXVGemmaEnhancePrompt` from workflow. Write your own prompt.

## LTX Setup Reminders (every fresh install)

```bash
# Symlinks
ln -sf models/diffusion_models/ltx-2.3-22b-dev-fp8.safetensors \
  models/checkpoints/ltx-2.3-22b-dev-fp8.safetensors

ln -sf models/upscale_models/ltx-2.3-spatial-upscaler-x2-1.0.safetensors \
  models/latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.0.safetensors

# start.sh flag
python main.py --listen 0.0.0.0 --port 8188 --lowvram
```

VAE node: `LTXVSpatioTemporalTiledVAEDecode` (spatial_tiles=2, temporal_tile_length=8, working_device=cpu)
