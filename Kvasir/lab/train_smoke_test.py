#!/usr/bin/env python3
"""
QLoRA Fine-tuning: Qwen2.5-7B on CodeAlpaca-20k
Using Unsloth for memory-efficient training

Usage:
    source ~/hfvenv/bin/activate
    python3 train_qwen_code.py

Output:
    ./outputs/qwen2.5-7b-code/  — LoRA adapter weights
"""

from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig
import torch

# ── Config ────────────────────────────────────────────────────────────────────
MODEL_NAME   = "unsloth/Qwen2.5-Coder-3B-Instruct"
OUTPUT_DIR   = "./outputs/qwen2.5-3b-code"
MAX_SEQ_LEN  = 2048     # 3B fits comfortably in 8GB VRAM
LORA_RANK    = 8
BATCH_SIZE   = 1
GRAD_ACCUM   = 8        # effective batch = 8
EPOCHS       = 1        # 1 epoch for quick test, increase for production
LR           = 2e-4
WARMUP_RATIO = 0.05
MAX_STEPS    = 100       # -1 = full epoch, set e.g. 100 for quick smoke test

# ── Load model ────────────────────────────────────────────────────────────────
print("Loading model...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name      = MODEL_NAME,
    max_seq_length  = MAX_SEQ_LEN,
    load_in_4bit    = True,     # QLoRA 4-bit quantization
    dtype           = None,     # auto-detect (bfloat16 on Ampere+)
)

# ── Attach LoRA adapter ───────────────────────────────────────────────────────
model = FastLanguageModel.get_peft_model(
    model,
    r                   = LORA_RANK,
    target_modules      = ["q_proj", "k_proj", "v_proj", "o_proj",
                           "gate_proj", "up_proj", "down_proj"],
    lora_alpha          = LORA_RANK * 2,
    lora_dropout        = 0,
    bias                = "none",
    use_gradient_checkpointing = "unsloth",
    random_state        = 42,
)

# ── Dataset ───────────────────────────────────────────────────────────────────
print("Loading dataset...")
dataset = load_dataset("sahil2801/CodeAlpaca-20k", split="train")
print(f"Dataset size: {len(dataset)} samples")

# Format to chat template
def format_example(example):
    instruction = example["instruction"]
    input_text  = example.get("input", "").strip()
    output      = example["output"]

    if input_text:
        user_msg = f"{instruction}\n\n{input_text}"
    else:
        user_msg = instruction

    messages = [
        {"role": "user",      "content": user_msg},
        {"role": "assistant", "content": output},
    ]
    return {"text": tokenizer.apply_chat_template(messages, tokenize=False)}

dataset = dataset.map(format_example, remove_columns=dataset.column_names)
print(f"Sample:\n{dataset[0]['text'][:300]}\n...")

# ── Train ─────────────────────────────────────────────────────────────────────
print("Starting training...")
trainer = SFTTrainer(
    model      = model,
    tokenizer  = tokenizer,
    train_dataset = dataset,
    args = SFTConfig(
        output_dir              = OUTPUT_DIR,
        num_train_epochs        = EPOCHS,
        max_steps               = MAX_STEPS,
        per_device_train_batch_size = BATCH_SIZE,
        gradient_accumulation_steps = GRAD_ACCUM,
        learning_rate           = LR,
        warmup_ratio            = WARMUP_RATIO,
        lr_scheduler_type       = "cosine",
        optim                   = "adamw_8bit",
        fp16                    = not torch.cuda.is_bf16_supported(),
        bf16                    = torch.cuda.is_bf16_supported(),
        logging_steps           = 10,
        save_steps              = 200,
        save_total_limit        = 2,
        max_seq_length          = MAX_SEQ_LEN,
        dataset_text_field      = "text",
        report_to               = "none",
    ),
)

trainer.train()

# ── Save ──────────────────────────────────────────────────────────────────────
print(f"Saving LoRA adapter to {OUTPUT_DIR}...")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print("Done!")
print(f"\nTo run inference: load adapter from {OUTPUT_DIR}")
