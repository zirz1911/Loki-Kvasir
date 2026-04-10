#!/usr/bin/env python3
"""
Hard inference tests for fine-tuned Qwen2.5-Coder-3B
"""
from unsloth import FastLanguageModel
import torch

ADAPTER_DIR = "./outputs/qwen2.5-3b-code"
MAX_SEQ_LEN = 2048

print("Loading model...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name     = ADAPTER_DIR,
    max_seq_length = MAX_SEQ_LEN,
    load_in_4bit   = True,
)
FastLanguageModel.for_inference(model)

def ask(prompt, max_new_tokens=800):
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to("cuda")
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=max_new_tokens, temperature=0.7, do_sample=True)
    decoded = tokenizer.decode(out[0], skip_special_tokens=True)
    return decoded[len(tokenizer.decode(inputs["input_ids"][0], skip_special_tokens=True)):]

tests = [
    ("LRU Cache",
     "Implement an LRU Cache class in Python with get and put methods. Use O(1) time complexity for both."),

    ("Async rate limiter",
     "Write an async Python function that rate-limits API calls to max 10 requests per second using asyncio."),

    ("Decorator with args",
     "Write a Python decorator factory `@retry(max_attempts=3, delay=1.0)` that retries a function on exception."),

    ("SQL injection safe",
     "Write a Python function that safely queries a SQLite database for users by username. Avoid SQL injection."),

    ("Tree traversal",
     "Write Python functions for preorder, inorder, and postorder traversal of a binary tree — both recursive and iterative."),
]

for i, (title, prompt) in enumerate(tests, 1):
    print(f"\n{'='*60}")
    print(f"Test {i}: {title}")
    print(f"Prompt: {prompt}")
    print(f"{'='*60}")
    result = ask(prompt)
    print(result)

print("\nAll done!")
