"""
04-rate-limiter.py

Implementations of various Rate Limiting algorithms.
"""

import time
from collections import deque

# 1. Token Bucket
class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_refill = time.time()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def allow_request(self, tokens: int = 1) -> bool:
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

# 2. Sliding Window Log
class SlidingWindowLog:
    def __init__(self, limit: int, window_seconds: float):
        self.limit = limit
        self.window = window_seconds
        self.requests = deque()

    def allow_request(self) -> bool:
        now = time.time()
        cutoff = now - self.window
        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()

        if len(self.requests) < self.limit:
            self.requests.append(now)
            return True
        return False

# 3. Fixed Window Counter
class FixedWindowCounter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.current_window = 0
        self.counter = 0

    def allow_request(self) -> bool:
        window = int(time.time() // self.window)
        if window != self.current_window:
            self.current_window = window
            self.counter = 0

        if self.counter < self.limit:
            self.counter += 1
            return True
        return False

# 4. Sliding Window Counter (Approximation)
class SlidingWindowCounter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.prev_count = 0
        self.curr_count = 0
        self.curr_window = 0

    def allow_request(self) -> bool:
        now = time.time()
        curr_window = int(now // self.window)

        if curr_window != self.curr_window:
            if curr_window == self.curr_window + 1:
                self.prev_count = self.curr_count
            else:
                self.prev_count = 0
            self.curr_window = curr_window
            self.curr_count = 0

        elapsed_in_window = now % self.window
        overlap_ratio = 1 - (elapsed_in_window / self.window)
        estimated_count = self.prev_count * overlap_ratio + self.curr_count

        if estimated_count < self.limit:
            self.curr_count += 1
            return True
        return False

# 5. Leaky Bucket
class LeakyBucket:
    def __init__(self, capacity: int, leak_rate: float):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.water = 0.0
        self.last_leak = time.time()

    def _leak(self):
        now = time.time()
        elapsed = now - self.last_leak
        self.water = max(0.0, self.water - elapsed * self.leak_rate)
        self.last_leak = now

    def allow_request(self) -> bool:
        self._leak()
        if self.water < self.capacity:
            self.water += 1.0
            return True
        return False
