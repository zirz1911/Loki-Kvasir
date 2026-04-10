#!/usr/bin/env python3
"""
Quick inference test for fine-tuned Qwen2.5-Coder-3B
"""
from unsloth import FastLanguageModel
import torch

MODEL_NAME  = "unsloth/Qwen2.5-Coder-3B-Instruct"
ADAPTER_DIR = "./outputs/qwen2.5-3b-code"
MAX_SEQ_LEN = 2048

print("Loading model + adapter...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name     = ADAPTER_DIR,
    max_seq_length = MAX_SEQ_LEN,
    load_in_4bit   = True,
)
FastLanguageModel.for_inference(model)

def ask(prompt, max_new_tokens=512):
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to("cuda")
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=max_new_tokens, temperature=0.7, do_sample=True)
    decoded = tokenizer.decode(out[0], skip_special_tokens=True)
    # strip the prompt part
    return decoded[len(tokenizer.decode(inputs["input_ids"][0], skip_special_tokens=True)):]

# Test cases
tests = [
    "Write a Python function to reverse a linked list.",
    "Write a binary search function in Python with docstring.",
    "Create a simple REST API endpoint using FastAPI that returns hello world.",
]

for i, prompt in enumerate(tests, 1):
    print(f"\n{'='*60}")
    print(f"Test {i}: {prompt}")
    print(f"{'='*60}")
    result = ask(prompt)
    print(result)

print("\nDone!")
