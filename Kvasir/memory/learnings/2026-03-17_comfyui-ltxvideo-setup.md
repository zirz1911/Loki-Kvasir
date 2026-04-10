# ComfyUI + LTXVideo Setup on Low VRAM

**Date**: 2026-03-17
**Source**: ComfyUI setup session — LTX-2.3 22B on RTX 3070 Ti 8GB

## Critical Setup Steps

### 1. Fix permissions first
```bash
sudo chown -R paji:paji /home/paji/Project/ComfyUI/models/
```
Do this BEFORE downloading any models. ComfyUI install as root leaves all subfolders root-owned.

### 2. LTXVideo folder mapping (symlinks required)
ComfyUI-LTXVideo nodes hardcode specific folders:
```bash
# Main model → checkpoints/ (NOT diffusion_models/)
ln -sf models/diffusion_models/ltx-2.3-22b-dev-fp8.safetensors \
  models/checkpoints/ltx-2.3-22b-dev-fp8.safetensors

# Spatial upscaler → latent_upscale_models/ (NOT upscale_models/)
ln -sf models/upscale_models/ltx-2.3-spatial-upscaler-x2-1.0.safetensors \
  models/latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.0.safetensors
```

### 3. start.sh for 8GB VRAM
```bash
python main.py --listen 0.0.0.0 --port 8188 --lowvram
```

### 4. VAE Decode for low VRAM
Use `LTXVSpatioTemporalTiledVAEDecode` instead of `VAEDecodeTiled`:
- `spatial_tiles`: 2
- `temporal_tile_length`: 8
- `working_device`: cpu
- `working_dtype`: float16

### 5. Clear stuck queue
```bash
curl -X POST localhost:8188/queue -H "Content-Type: application/json" -d '{"clear":true}'
curl -X POST localhost:8188/interrupt
```

## Expected Performance (8GB VRAM)
- Text encoding: ~1-2 min (11GB model on CPU)
- Denoising: slow, depends on steps/resolution
- VAE decode: tiled on CPU, manageable

## Model Locations
| File | Folder |
|------|--------|
| ltx-2.3-22b-dev-fp8.safetensors | checkpoints/ (symlink) + diffusion_models/ (real) |
| ltx-2.3-spatial-upscaler | latent_upscale_models/ (symlink) + upscale_models/ (real) |
| gemma_3_12B_it_fp4_mixed | text_encoders/ |
| ltx-2.3-22b-distilled-lora-384 | loras/ |
