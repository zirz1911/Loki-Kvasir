import time
from collections import defaultdict
import threading


class RateLimiter:
    def __init__(self, max_tokens: int, refill_rate: float):
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.tokens = defaultdict(int)
        self.last_refill_time = defaultdict(float)
        self.lock = threading.Lock()

    def allow(self, key: str) -> bool:
        with self.lock:
            now = time.time()
            if now - self.last_refill_time[key] > 0:
                self.tokens[key] += (now - self.last_refill_time[key]) * self.refill_rate
                self.tokens[key] = min(self.tokens[key], self.max_tokens)
                self.last_refill_time[key] = now
            if self.tokens[key] >= 1:
                self.tokens[key] -= 1  # fix: deduct token on approval
                return True
            return False

    def reset(self, key: str):
        with self.lock:
            self.tokens[key] = 0
            self.last_refill_time[key] = time.time()
