# Rate Limiter

> **Prerequisites:** Understanding of queues and sliding window concept

## Interview Context

Rate limiting is a fundamental system design topic that also appears in coding interviews. It tests:

- Algorithm design for time-based constraints
- Trade-offs between accuracy and memory
- Understanding of distributed systems (for follow-ups)
- Real-world API design knowledge

Common interview questions: "Implement a rate limiter" or "Design an API rate limiting system."

---

## Rate Limiting Algorithms

| Algorithm | Pros | Cons | Use Case |
|-----------|------|------|----------|
| Token Bucket | Allows bursts, smooth | Complex | API gateways |
| Leaky Bucket | Smooth output | No bursts | Streaming |
| Fixed Window | Simple | Boundary spike | Basic limiting |
| Sliding Window Log | Accurate | Memory intensive | Low-volume APIs |
| Sliding Window Counter | Memory efficient | Approximate | High-volume APIs |

---

## Pattern 1: Token Bucket

Tokens are added at a fixed rate. Each request consumes a token. If no tokens, request is rejected.

### Visualization

```
Bucket capacity: 5 tokens
Refill rate: 1 token/second

Time 0: [●●●●●] 5 tokens
        Request → [●●●●○] 4 tokens
        Request → [●●●○○] 3 tokens
Time 1:          [●●●●○] 4 tokens (1 added)
        Request → [●●●○○] 3 tokens
        Request → [●●○○○] 2 tokens
        Request → [●○○○○] 1 token
        Request → [○○○○○] 0 tokens
        Request → REJECTED (no tokens)
Time 2:          [●○○○○] 1 token (1 added)
```

### Implementation

```python
import time

class TokenBucket:
    """
    Token Bucket rate limiter.

    Allows bursts up to bucket capacity.

    Time: O(1) per request
    Space: O(1)
    """

    def __init__(self, capacity: int, refill_rate: float):
        """
        Args:
            capacity: Maximum tokens in bucket
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def _refill(self) -> None:
        """Add tokens based on time elapsed."""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

    def allow_request(self, tokens: int = 1) -> bool:
        """
        Check if request is allowed and consume tokens.

        Returns:
            True if request is allowed, False if rate limited
        """
        self._refill()

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


# Test
limiter = TokenBucket(capacity=5, refill_rate=1)  # 5 tokens, 1/sec refill

# Burst of 5 requests should pass
for i in range(5):
    print(f"Request {i+1}: {limiter.allow_request()}")  # All True

# 6th request should fail
print(f"Request 6: {limiter.allow_request()}")  # False

# Wait and try again
time.sleep(2)
print(f"After 2s: {limiter.allow_request()}")  # True (got 2 tokens back)
```

---

## Pattern 2: Sliding Window Log

Store timestamp of each request. Count requests in the sliding window.

### Visualization

```
Window: 60 seconds, Limit: 3 requests

Timestamps: [10, 25, 45]  (3 requests in last 60s)

At time 70:
  Remove old: [25, 45]  (10 is > 60s ago)
  Count: 2
  New request → allowed, add 70: [25, 45, 70]

At time 71:
  Count: 3 (all within 60s)
  New request → REJECTED
```

### Implementation

```python
from collections import deque
import time

class SlidingWindowLog:
    """
    Sliding Window Log rate limiter.

    Stores timestamp of each request.
    Most accurate but memory-intensive.

    Time: O(1) amortized (cleanup is distributed)
    Space: O(limit) in worst case
    """

    def __init__(self, limit: int, window_seconds: float):
        """
        Args:
            limit: Maximum requests per window
            window_seconds: Window size in seconds
        """
        self.limit = limit
        self.window = window_seconds
        self.requests = deque()  # Timestamps of requests

    def allow_request(self) -> bool:
        """
        Check if request is allowed.

        Returns:
            True if allowed, False if rate limited
        """
        now = time.time()
        cutoff = now - self.window

        # Remove expired timestamps
        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()

        if len(self.requests) < self.limit:
            self.requests.append(now)
            return True

        return False


# Test
limiter = SlidingWindowLog(limit=3, window_seconds=10)

print(limiter.allow_request())  # True
print(limiter.allow_request())  # True
print(limiter.allow_request())  # True
print(limiter.allow_request())  # False (limit reached)

time.sleep(11)  # Wait for window to pass
print(limiter.allow_request())  # True
```

---

## Pattern 3: Fixed Window Counter

Divide time into fixed windows (e.g., 1-minute buckets). Count requests per window.

### Visualization

```
Window size: 1 minute, Limit: 100

12:00:00 - 12:00:59 → Window 1, counter = 0
12:01:00 - 12:01:59 → Window 2, counter = 0

Requests at 12:00:30: counter[1] = 50
Requests at 12:00:45: counter[1] = 100
Request at 12:00:50: REJECTED (counter[1] >= 100)

12:01:00: counter[2] = 0 (new window)
Request at 12:01:00: counter[2] = 1 (allowed)
```

### Implementation

```python
import time

class FixedWindowCounter:
    """
    Fixed Window Counter rate limiter.

    Simple but has boundary problem:
    - 100 requests at 12:00:59
    - 100 requests at 12:01:00
    - Both pass, but 200 requests in 2 seconds!

    Time: O(1)
    Space: O(1)
    """

    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.current_window = 0
        self.counter = 0

    def _get_window(self) -> int:
        """Get current window ID."""
        return int(time.time() // self.window)

    def allow_request(self) -> bool:
        window = self._get_window()

        if window != self.current_window:
            # New window, reset counter
            self.current_window = window
            self.counter = 0

        if self.counter < self.limit:
            self.counter += 1
            return True

        return False


# Test
limiter = FixedWindowCounter(limit=5, window_seconds=10)

for i in range(5):
    print(f"Request {i+1}: {limiter.allow_request()}")  # All True

print(f"Request 6: {limiter.allow_request()}")  # False
```

---

## Pattern 4: Sliding Window Counter

Combines fixed windows with weighted averaging to fix the boundary problem.

### Algorithm

```
Estimate = (previous_window_count * overlap_ratio) + current_window_count

Example:
- Window: 1 minute, Limit: 100
- Previous window (12:00-12:01): 80 requests
- Current window (12:01-12:02): 20 requests
- Current time: 12:01:15 (25% into current window)

Overlap with previous = 75%
Estimate = 80 * 0.75 + 20 = 80

If estimate >= 100, reject
```

### Implementation

```python
import time

class SlidingWindowCounter:
    """
    Sliding Window Counter rate limiter.

    Memory-efficient approximation of sliding window.
    More accurate than fixed window at boundary.

    Time: O(1)
    Space: O(1)
    """

    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.prev_window = 0
        self.prev_count = 0
        self.curr_window = 0
        self.curr_count = 0

    def allow_request(self) -> bool:
        now = time.time()
        curr_window = int(now // self.window)

        # Update windows
        if curr_window != self.curr_window:
            if curr_window == self.curr_window + 1:
                # Move to next window
                self.prev_window = self.curr_window
                self.prev_count = self.curr_count
            else:
                # Skipped windows, reset previous
                self.prev_window = curr_window - 1
                self.prev_count = 0

            self.curr_window = curr_window
            self.curr_count = 0

        # Calculate weighted count
        window_start = curr_window * self.window
        elapsed_ratio = (now - window_start) / self.window
        prev_weight = 1 - elapsed_ratio

        estimated_count = self.prev_count * prev_weight + self.curr_count

        if estimated_count < self.limit:
            self.curr_count += 1
            return True

        return False


# Test
limiter = SlidingWindowCounter(limit=10, window_seconds=60)

for i in range(10):
    print(f"Request {i+1}: {limiter.allow_request()}")

print(f"Request 11: {limiter.allow_request()}")  # Likely False
```

---

## Pattern 5: Leaky Bucket

Requests enter a bucket and "leak" out at a fixed rate. If bucket is full, reject.

```python
import time

class LeakyBucket:
    """
    Leaky Bucket rate limiter.

    Smooths out bursts - requests are processed at fixed rate.
    Often used for packet shaping.

    Time: O(1)
    Space: O(1)
    """

    def __init__(self, capacity: int, leak_rate: float):
        """
        Args:
            capacity: Maximum queue size
            leak_rate: Requests processed per second
        """
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.water = 0.0  # Current queue size
        self.last_leak = time.time()

    def _leak(self) -> None:
        """Remove processed requests from bucket."""
        now = time.time()
        elapsed = now - self.last_leak
        leaked = elapsed * self.leak_rate
        self.water = max(0, self.water - leaked)
        self.last_leak = now

    def allow_request(self) -> bool:
        self._leak()

        if self.water < self.capacity:
            self.water += 1
            return True

        return False
```

---

## Distributed Rate Limiting

For distributed systems, rate limiting needs coordination:

### Redis-Based Implementation

```python
import redis
import time

class DistributedRateLimiter:
    """
    Distributed rate limiter using Redis.

    Uses atomic operations for consistency.
    """

    def __init__(self, redis_client: redis.Redis, key_prefix: str,
                 limit: int, window_seconds: int):
        self.redis = redis_client
        self.prefix = key_prefix
        self.limit = limit
        self.window = window_seconds

    def allow_request(self, user_id: str) -> bool:
        key = f"{self.prefix}:{user_id}"
        now = int(time.time())
        window_start = now - self.window

        pipe = self.redis.pipeline()

        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start)

        # Count current entries
        pipe.zcard(key)

        # Add current request
        pipe.zadd(key, {str(now): now})

        # Set TTL
        pipe.expire(key, self.window)

        results = pipe.execute()
        current_count = results[1]

        return current_count < self.limit


# Usage with Redis
# r = redis.Redis()
# limiter = DistributedRateLimiter(r, "ratelimit", 100, 60)
# limiter.allow_request("user123")
```

---

## Complexity Analysis

| Algorithm | Time | Space | Accuracy |
|-----------|------|-------|----------|
| Token Bucket | O(1) | O(1) | Exact for burst control |
| Leaky Bucket | O(1) | O(1) | Exact for rate smoothing |
| Fixed Window | O(1) | O(1) | Boundary issues |
| Sliding Window Log | O(1)* | O(limit) | Exact |
| Sliding Window Counter | O(1) | O(1) | Approximate |

*Amortized O(1), cleanup is O(n) but distributed over requests

---

## Algorithm Selection Guide

```
Need to allow bursts?
├── Yes → Token Bucket
│         - Good for API rate limiting
│         - Allows burst up to capacity
│
└── No → Need smooth output?
    ├── Yes → Leaky Bucket
    │         - Good for streaming, packet shaping
    │
    └── No → How much memory?
        ├── Minimal → Sliding Window Counter
        │             - Approximate but efficient
        │
        └── More OK → Sliding Window Log
                      - Exact but stores all timestamps
```

---

## Edge Cases

1. **Time going backwards**: Handle clock skew (use monotonic time)
2. **Very high request rate**: Cleanup overhead in log-based approaches
3. **Distributed systems**: Need atomic operations (Redis, etc.)
4. **Per-user vs global**: Different keys for different limits
5. **Different limits**: Premium users get higher limits

---

## Interview Tips

1. **Clarify requirements**: "Is this per-user or global? What's the window size?"
2. **Start simple**: Fixed window, then explain improvements
3. **Mention trade-offs**: Accuracy vs memory vs complexity
4. **Discuss distribution**: How to scale to multiple servers
5. **Know real systems**: "Redis can do this with sorted sets"

### Common Follow-ups

```
Q: How would you handle rate limiting across multiple servers?
A: Use a centralized store like Redis with atomic operations,
   or use consistent hashing to route users to specific rate limiters.

Q: What if the rate limiter itself becomes a bottleneck?
A: Shard by user ID, use local caching with periodic sync,
   or use probabilistic rate limiting.

Q: How do you handle different rate limits for different users?
A: Store limits in a config service, look up per request,
   or use tiers with predetermined limits.
```

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Design Hit Counter | Medium | Sliding window basics |
| 2 | Logger Rate Limiter | Easy | Simple timestamp tracking |
| 3 | Design Rate Limiter | Medium | System design question |
| 4 | API Rate Limiter | Medium | Token bucket implementation |
| 5 | Sliding Window Maximum | Hard | Related sliding window concept |

---

## Related Sections

- [Data Structure Choices](./01-data-structure-choices.md) - Queue and counter structures
- [LRU Cache](./02-lru-cache.md) - Similar time-based eviction concepts
