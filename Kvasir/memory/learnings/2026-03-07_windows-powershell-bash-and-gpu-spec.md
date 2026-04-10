# Windows PowerShell in Bash + GPU Spec Patterns

**Date**: 2026-03-07
**Source**: rrr: Loki-Kvasir

## Pattern 1: PowerShell via bash — variable interpolation conflict

When running PowerShell from bash on Windows, bash strips `$` from variable names inside `-Command` strings.

**Bad** (bash eats the `$`):
```bash
powershell -Command "
  $cpu = Get-CimInstance Win32_Processor
  Write-Host $cpu.Name   # $cpu becomes empty
"
```

**Good** (separate one-liner calls):
```bash
powershell -Command "Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores | Format-List"
```

Or escape with backtick — but simpler to just break into separate calls.

## Pattern 2: WMI VRAM is inaccurate — always use nvidia-smi

`Win32_VideoController.AdapterRAM` reported ~4GB for an RTX 4050 Laptop (actual: 6GB).

**Always verify NVIDIA VRAM with**:
```bash
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
```

## Pattern 3: ML Training capability by VRAM

| VRAM | What you can do |
|------|----------------|
| <4GB | Inference only, very small models (1B 4bit) |
| 4-6GB | QLoRA fine-tuning 1B-7B with 4bit |
| 8-12GB | LoRA fine-tuning 7B-13B |
| 16GB+ | Full fine-tuning 7B, LoRA 30B+ |

RTX 4050 Laptop (6GB): QLoRA 7B is the sweet spot. Use Unsloth for 2x speed + lower VRAM.
