# QLoRA VRAM Requirements by Model Size

**Discovered**: 2026-03-07
**Context**: Qwen2.5-7B failed OOM 3 times on RTX 3070 Ti (8GB VRAM)

## The Problem

Qwen2.5-7B has a 152k-token vocabulary. Even with 4-bit quantization, the cross-entropy loss computation creates logits tensors of shape `(batch * seq_len * vocab_size)`:

- seq_len=2048, batch=2: ~2.4GB for logits alone → OOM
- seq_len=1024, batch=1: ~600MB → OOM during backward pass
- seq_len=512, batch=1: ~300MB → OOM in CE loss chunking

The model weights themselves fit (~3.5GB quantized) but activation memory + optimizer states + CE logits push total VRAM over 8GB.

## Hardware → Model Decision Tree

| VRAM | Max Model (QLoRA 4-bit) | Notes |
|------|------------------------|-------|
| 6GB  | 3B                     | Tight; use seq_len ≤ 1024 |
| 8GB  | 3B (comfortable)       | seq_len 2048 fine |
| 12GB | 7B                     | seq_len 2048 fine |
| 16GB | 13B                    | seq_len 2048 fine |
| 24GB | 13B (full fine-tune) / 30B QLoRA | |
| 40GB+ | 70B QLoRA             | A100 territory |

## Fix for 8GB GPUs

Use `unsloth/Qwen2.5-Coder-3B-Instruct` instead of 7B:
- VRAM usage: ~2.8GB (vs 7.7GB for 7B)
- Speed: ~6s/step (vs theoretical ~20s/step for 7B)
- Quality: sufficient for instruction-following code tasks

## Always Set

```bash
PYTORCH_ALLOC_CONF=expandable_segments:True python3 train.py
```

Reduces memory fragmentation at zero cost.
