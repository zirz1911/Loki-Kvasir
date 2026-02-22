import time
import threading
import pytest
from rate_limiter import RateLimiter


def test_new_key_starts_empty():
    rl = RateLimiter(max_tokens=2, refill_rate=1)
    assert rl.allow("user1") is False


def test_tokens_refill_over_time():
    rl = RateLimiter(max_tokens=2, refill_rate=2)
    assert rl.allow("user1") is False  # first call: init clock, 0 tokens
    time.sleep(0.6)  # ~1.2 tokens refilled
    assert rl.allow("user1") is True
    assert rl.allow("user1") is False  # second draw empty


def test_reset_clears_tokens():
    rl = RateLimiter(max_tokens=2, refill_rate=2)
    time.sleep(1)
    rl.allow("user1")   # drain
    rl.allow("user1")
    rl.reset("user1")
    assert rl.allow("user1") is False  # empty after reset


def test_keys_are_independent():
    rl = RateLimiter(max_tokens=2, refill_rate=2)
    assert rl.allow("a") is False  # init clock for a
    assert rl.allow("b") is False  # init clock for b
    time.sleep(0.6)
    assert rl.allow("a") is True
    assert rl.allow("b") is True  # b unaffected by a


def test_thread_safety():
    rl = RateLimiter(max_tokens=3, refill_rate=0)  # no refill
    time.sleep(0.1)
    # prime 3 tokens manually via time gap — use high refill for setup
    rl2 = RateLimiter(max_tokens=3, refill_rate=100)
    time.sleep(0.05)  # fills to 3

    results = []
    lock = threading.Lock()

    def try_allow():
        r = rl2.allow("shared")
        with lock:
            results.append(r)

    threads = [threading.Thread(target=try_allow) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert sum(results) <= 3  # never exceeds max_tokens
