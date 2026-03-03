# Rate Limiter

> **Prerequisites:** Understanding of queues, sliding window concept, and basic distributed systems

## Quick Reference (Interview Cheat Sheet)

```
Token Bucket     → Allows bursts, O(1)/O(1), use for API gateways
Leaky Bucket     → Smooths output, O(1)/O(1), use for streaming/traffic shaping
Fixed Window     → Simplest, O(1)/O(1), boundary problem (2x burst)
Sliding Log      → Exact, O(1)*/O(n), use for low-volume accuracy-critical
Sliding Counter  → Approximate, O(1)/O(1), use for high-volume APIs

Key question: "How many requests in the last N seconds?"
Key trade-off: Accuracy vs Memory vs Complexity
Distributed: Redis + Lua scripts for atomicity
HTTP: 429 status, X-RateLimit-*, Retry-After headers
```

## Building Intuition

### Why Rate Limiting? Protecting Your System

Rate limiting is about **protecting resources from being overwhelmed**. Think of it like a bouncer at a club:

> **"You can only let in 100 people per hour. After that, everyone waits in line."**

Without rate limiting:

- A single user can consume all server resources
- Denial of service attacks succeed easily
- Expensive operations drain your budget (API calls, database queries)
- Downstream services get overwhelmed

### The Core Problem: Counting Events Over Time

Every rate limiter answers one question:

> **"How many requests have occurred in the last N seconds?"**

The challenge is doing this efficiently:

```
Naive approach: Store every timestamp, count those within window
Problem: O(n) per request, unbounded memory

Smart approach: Use data structures that give O(1) operations
```

### The Five Algorithms: Mental Models

**1. Token Bucket** - "The Arcade Token Dispenser"

```
Imagine an arcade that gives you 10 tokens per hour, max 10 at a time.
- Tokens accumulate while you're away (up to max)
- Each game costs 1 token
- No tokens? Wait or leave

Key insight: Allows BURSTS (if you saved tokens)
Real-world: AWS API Gateway, Stripe API (allows short bursts of requests)
```

**2. Leaky Bucket** - "The Water Tank with a Hole"

```
Water (requests) pours in at any rate.
Water leaks out at a fixed rate through a hole at the bottom.
If tank overflows, excess water is rejected.

Key insight: SMOOTHS output (constant rate out, regardless of input pattern)
Difference from Token Bucket: Token Bucket controls ADMISSION (do you have tokens?),
Leaky Bucket controls OUTPUT RATE (requests drain at a fixed pace).
Real-world: Network traffic shaping (NGINX limit_req), video streaming bitrate
```

**3. Fixed Window** - "The Hourly Counter"

```
Count resets every hour on the hour.
"100 requests per hour" = counter resets at :00

Key insight: SIMPLE but has boundary problem
(200 requests in 2 seconds: 100 at 12:59:59, 100 at 13:00:00)
Real-world: GitHub API (5000 requests/hour, resets on the hour)
```

**Why the boundary problem matters:**

```
Limit: 100 requests per minute

Timeline:
  12:00:00 ─────────────────── 12:01:00 ─────────────────── 12:02:00
                    |← 100 reqs →|← 100 reqs →|
                   12:00:50      12:01:00     12:01:10

A user sends 100 requests at 12:00:50 (end of window 1)
and 100 more at 12:01:10 (start of window 2).
Both windows pass: each has exactly 100.

But in a 20-second span, 200 requests went through — 2x the intended limit!
This is why "fixed window" can allow double the rate at boundaries.
```

**4. Sliding Window Log** - "The Receipt Box"

```
Keep every timestamp (receipt) in a box.
To check limit: count receipts from last N seconds.
Remove old receipts as you go.

Key insight: ACCURATE but memory-intensive
Real-world: Financial transaction monitoring, audit-heavy compliance APIs
```

**5. Sliding Window Counter** - "The Smart Estimator"

```
Keep counts for current and previous window.
Estimate current window using weighted average.

Key insight: MEMORY-EFFICIENT approximation
Real-world: Cloudflare rate limiting, high-volume public APIs (millions of users)
```

### Visual Comparison: Same Scenario, Different Results

Limit: 4 requests per 10 seconds

```
Time:     0s   2s   4s   6s   8s   10s  12s  14s  16s
Requests: R    R    R    R    R    R    R    -    R

Token Bucket (4 tokens, refill 0.4/sec):
R✓   R✓   R✓   R✓   R✓   R✓   R✓   -    R✓
tokens: 3.0  2.8  2.6  2.4  2.2  2.0  1.8       2.4
(refill outpaces consumption at 1 req/2s — never runs out)

Leaky Bucket (4 capacity, leak 0.4/sec):
R✓   R✓   R✓   R✓   R✓   R✓   R✓   -    R✓
water: 1.0  1.2  1.4  1.6  1.8  2.0  2.2       1.6
(leak rate keeps up with arrivals — bucket never fills)

Fixed Window (resets at 0s, 10s, 20s):
R✓   R✓   R✓   R✓   R✗   R✓   R✓   -    R✓
(window [0,10): 5 requests, 5th rejected; window [10,20): 3 requests, all pass)

Sliding Window Log (exact sliding 10s window):
R✓   R✓   R✓   R✓   R✗   R✓   R✓   -    R✓
(at t=8: 4 requests in [0,8], limit hit; at t=10: t=0 expires, count=3)
```

> **Key insight:** Token Bucket and Leaky Bucket both allow all requests here because
> the arrival rate (1 req/2s = 0.5/s) is close to the refill/leak rate (0.4/s).
> They only reject when requests arrive in a burst that exceeds capacity.
> Fixed Window and Sliding Window Log both reject at t=8 because
> 5 requests in one window exceeds the limit of 4.

### Token Bucket vs Leaky Bucket: The Key Difference

These two are frequently confused. The critical distinction:

```
Token Bucket:
  - Controls ADMISSION: "Do you have enough tokens to enter?"
  - Allows BURSTS: If tokens have accumulated, many requests pass at once
  - Output rate varies: can be bursty up to capacity, then rate-limited
  - Think: prepaid phone minutes — use them whenever, but they accumulate

Leaky Bucket:
  - Controls OUTPUT RATE: "Requests drain at a fixed pace"
  - SMOOTHS traffic: output is always at a constant rate
  - Input can be bursty (just fills the bucket), output is steady
  - Think: funnel — pour water in fast, it drips out slowly

Same scenario, different behavior:
  10 requests arrive simultaneously, limit = 5/sec, capacity = 5

  Token Bucket: All 5 pass immediately (burst), remaining 5 rejected
  Leaky Bucket: All 5 accepted into queue, processed at 1/sec over 5 seconds
```

## Interview Context

Rate limiting is a fundamental system design topic that also appears in coding interviews. It tests:

- Algorithm design for time-based constraints
- Trade-offs between accuracy and memory
- Understanding of distributed systems (for follow-ups)
- Real-world API design knowledge

Common interview questions: "Implement a rate limiter" or "Design an API rate limiting system."

---

## Rate Limiting Algorithms

| Algorithm              | Pros                  | Cons             | Use Case         |
| ---------------------- | --------------------- | ---------------- | ---------------- |
| Token Bucket           | Allows bursts, smooth | Complex          | API gateways     |
| Leaky Bucket           | Smooth output         | No bursts        | Streaming        |
| Fixed Window           | Simple                | Boundary spike   | Basic limiting   |
| Sliding Window Log     | Accurate              | Memory intensive | Low-volume APIs  |
| Sliding Window Counter | Memory efficient      | Approximate      | High-volume APIs |

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

    def __init__(self, capacity: int, refill_rate: float) -> None:
        """
        Args:
            capacity: Maximum tokens in bucket
            refill_rate: Tokens added per second
        """
        self.capacity: int = capacity
        self.refill_rate: float = refill_rate
        self.tokens: float = float(capacity)
        self.last_refill: float = time.monotonic()

    def _refill(self) -> None:
        """Add tokens based on time elapsed."""
        now = time.monotonic()
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
print(f"After 2s: {limiter.allow_request()}")  # True (got ~2 tokens back)
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

    Time: O(1) amortized (cleanup is distributed across requests)
    Space: O(limit) in worst case — at most 'limit' timestamps stored
    """

    def __init__(self, limit: int, window_seconds: float) -> None:
        """
        Args:
            limit: Maximum requests per window
            window_seconds: Window size in seconds
        """
        self.limit: int = limit
        self.window: float = window_seconds
        self.requests: deque[float] = deque()  # Timestamps of requests

    def allow_request(self) -> bool:
        """
        Check if request is allowed.

        Returns:
            True if allowed, False if rate limited
        """
        now = time.monotonic()
        cutoff = now - self.window

        # Remove expired timestamps — O(1) amortized because each
        # timestamp is added once and removed once across its lifetime
        while self.requests and self.requests[0] <= cutoff:
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

    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit: int = limit
        self.window: int = window_seconds
        self.current_window: int = 0
        self.counter: int = 0

    def _get_window(self) -> int:
        """Get current window ID."""
        return int(time.monotonic() // self.window)

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

    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit: int = limit
        self.window: int = window_seconds
        self.prev_window: int = 0
        self.prev_count: int = 0
        self.curr_window: int = 0
        self.curr_count: int = 0

    def allow_request(self) -> bool:
        now = time.monotonic()
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
        prev_weight = 1.0 - elapsed_ratio

        # Weighted estimate of requests in the sliding window.
        # We compare the raw float against the limit — no rounding needed.
        # This avoids both over-rejection (from rounding up) and
        # under-rejection (from rounding down).
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

### Visualization

```
Bucket capacity: 3, Leak rate: 1/sec

Time 0: [○○○] water = 0
        Request → [█○○] water = 1
        Request → [██○] water = 2
        Request → [███] water = 3
        Request → REJECTED (bucket full)

Time 1:          [██○] water = 2 (leaked 1)
        Request → [███] water = 3

Time 2:          [██○] water = 2 (leaked 1)
        Request → [███] water = 3
```

### Implementation

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

    def __init__(self, capacity: int, leak_rate: float) -> None:
        """
        Args:
            capacity: Maximum queue size
            leak_rate: Requests processed per second
        """
        self.capacity: int = capacity
        self.leak_rate: float = leak_rate
        self.water: float = 0.0  # Current queue size
        self.last_leak: float = time.monotonic()

    def _leak(self) -> None:
        """Remove processed requests from bucket."""
        now = time.monotonic()
        elapsed = now - self.last_leak
        leaked = elapsed * self.leak_rate
        self.water = max(0.0, self.water - leaked)
        self.last_leak = now

    def allow_request(self) -> bool:
        self._leak()

        if self.water < self.capacity:
            self.water += 1
            return True

        return False


# Test
limiter = LeakyBucket(capacity=3, leak_rate=1)  # 3 capacity, 1/sec leak

for i in range(3):
    print(f"Request {i+1}: {limiter.allow_request()}")  # All True

print(f"Request 4: {limiter.allow_request()}")  # False (bucket full)

time.sleep(2)
print(f"After 2s: {limiter.allow_request()}")  # True (leaked ~2)
```

---

## Practical Pattern: Rate Limiter as a Decorator

In real codebases, rate limiting is often applied as a decorator or middleware.
This pattern shows up frequently in interviews when discussing API design.

```python
import functools
import time
from typing import Any, Callable


class RateLimitExceeded(Exception):
    """Raised when a rate limit is exceeded."""

    def __init__(self, retry_after: float) -> None:
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after:.1f}s")


def rate_limit(
    max_calls: int, period: float
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator that rate-limits a function using the token bucket algorithm.

    Args:
        max_calls: Maximum calls allowed per period
        period: Time period in seconds

    Usage:
        @rate_limit(max_calls=5, period=60)
        def call_external_api(query: str) -> dict:
            ...
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # Token bucket state — closed over by the wrapper
        tokens = float(max_calls)
        last_refill = time.monotonic()
        refill_rate = max_calls / period

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal tokens, last_refill

            # Refill tokens
            now = time.monotonic()
            elapsed = now - last_refill
            tokens = min(max_calls, tokens + elapsed * refill_rate)
            last_refill = now

            if tokens >= 1:
                tokens -= 1
                return func(*args, **kwargs)

            # Calculate when next token will be available
            wait_time = (1 - tokens) / refill_rate
            raise RateLimitExceeded(retry_after=wait_time)

        return wrapper

    return decorator


# Usage example
@rate_limit(max_calls=3, period=10)
def send_notification(user_id: str, message: str) -> str:
    return f"Sent '{message}' to {user_id}"


# Test
for i in range(4):
    try:
        result = send_notification("user123", f"msg_{i}")
        print(f"Call {i+1}: {result}")
    except RateLimitExceeded as e:
        print(f"Call {i+1}: {e}")
```

---

## Real-World: HTTP Rate Limit Headers

Production rate limiters communicate status through HTTP headers. Knowing these
shows interviewers you understand how rate limiting works end-to-end.

```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100            ← Max requests allowed per window
X-RateLimit-Remaining: 0          ← Requests left in current window
X-RateLimit-Reset: 1672531260     ← Unix timestamp when window resets
Retry-After: 30                   ← Seconds to wait before retrying
```

**Why this matters in interviews:**

- Clients can self-throttle using `Retry-After` (reduces wasted requests)
- `X-RateLimit-Remaining` lets clients pace themselves proactively
- The `429` status code is specifically designated for rate limiting (RFC 6585)
- Some APIs also include `X-RateLimit-Policy` to describe the limit tier

**Examples in the wild:**

| Service        | Limit Header Style             | Limit                 |
| -------------- | ------------------------------ | --------------------- |
| GitHub API     | `X-RateLimit-*`                | 5000 req/hour (auth)  |
| Stripe API     | `RateLimit-*` + `Retry-After`  | 100 req/sec (live)    |
| Twitter/X API  | `x-rate-limit-*`               | Varies by endpoint    |
| Cloudflare     | Returns `429` + `Retry-After`  | Configurable per zone |

---

## Distributed Rate Limiting

For distributed systems, rate limiting needs coordination:

### Redis-Based Implementation

```python
import time
import uuid

import redis


class DistributedRateLimiter:
    """
    Distributed rate limiter using Redis sorted sets.

    Uses a Lua script for true atomicity. A Redis pipeline alone is NOT
    atomic — it batches commands but another client can interleave between
    them. Lua scripts execute atomically on the Redis server.
    """

    # Lua script ensures all operations execute atomically on the Redis server.
    # KEYS[1] = rate limit key (e.g., "ratelimit:user123")
    # ARGV[1] = window_start (oldest allowed timestamp)
    # ARGV[2] = now (current timestamp, used as score)
    # ARGV[3] = limit (max requests per window)
    # ARGV[4] = window_seconds (TTL for the key)
    # ARGV[5] = unique request ID (member — must be unique per request)
    LUA_SCRIPT = """
    redis.call('ZREMRANGEBYSCORE', KEYS[1], 0, ARGV[1])
    local count = redis.call('ZCARD', KEYS[1])
    if count < tonumber(ARGV[3]) then
        redis.call('ZADD', KEYS[1], ARGV[2], ARGV[5])
        redis.call('EXPIRE', KEYS[1], tonumber(ARGV[4]))
        return 1
    end
    return 0
    """

    def __init__(
        self,
        redis_client: redis.Redis,  # type: ignore[type-arg]
        key_prefix: str,
        limit: int,
        window_seconds: int,
    ) -> None:
        self.redis: redis.Redis = redis_client  # type: ignore[type-arg]
        self.prefix: str = key_prefix
        self.limit: int = limit
        self.window: int = window_seconds
        self._script = self.redis.register_script(self.LUA_SCRIPT)

    def allow_request(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        key = f"{self.prefix}:{user_id}"
        now = time.time()
        window_start = now - self.window
        # Unique member prevents two same-timestamp requests from colliding
        # in the sorted set (sorted sets have unique members).
        request_id = f"{now}:{uuid.uuid4()}"

        result = self._script(
            keys=[key],
            args=[window_start, now, self.limit, self.window, request_id],
        )
        return bool(result)


# Usage with Redis
# r = redis.Redis()
# limiter = DistributedRateLimiter(r, "ratelimit", 100, 60)
# limiter.allow_request("user123")
```

> **Why Lua instead of pipeline?** A Redis pipeline sends commands in a batch
> but does NOT guarantee atomicity — another client's commands can execute between
> yours. A Lua script runs entirely on the Redis server as a single atomic operation,
> preventing race conditions where two requests both read count < limit and both add.

> **Why unique member IDs?** Redis sorted sets require unique members. If two requests
> arrive at the exact same `time.time()` value and you use the timestamp as the member,
> the second ZADD silently overwrites the first — effectively losing a request from the
> count. Using `uuid4()` ensures every request gets its own entry.

---

## Complexity Analysis

| Algorithm              | Time   | Space    | Accuracy                 | Burst Handling           |
| ---------------------- | ------ | -------- | ------------------------ | ------------------------ |
| Token Bucket           | O(1)   | O(1)     | Exact for burst control  | Allows bursts up to cap  |
| Leaky Bucket           | O(1)   | O(1)     | Exact for rate smoothing | Smooths bursts to fixed  |
| Fixed Window           | O(1)   | O(1)     | Boundary issues (2x)     | No burst control         |
| Sliding Window Log     | O(1)\* | O(limit) | Exact                    | Hard limit per window    |
| Sliding Window Counter | O(1)   | O(1)     | Approximate              | Approximated at boundary |

\*Amortized O(1), cleanup is O(n) but distributed over requests

### Complexity Derivation: Why Sliding Window Counter is O(1)

The sliding window counter is clever because it avoids storing individual timestamps:

```
Data stored: Just 4 values!
- prev_window_id: int
- prev_count: int
- curr_window_id: int
- curr_count: int

Space: O(1) regardless of request volume!

Per-request operations:
1. Get current time             → O(1)
2. Calculate window ID          → O(1) division
3. Update window if changed     → O(1) assignment
4. Calculate weighted estimate  → O(1) arithmetic
5. Increment counter if allowed → O(1)
Total: O(1)
```

**Why the estimate works:**

```
If we're 30% into the current window:
- 70% of requests from previous window are "in scope"
- 100% of current window requests are "in scope"

Estimate = prev_count * 0.70 + curr_count * 1.0

This is approximate but very close to true sliding window!
```

## When NOT to Use Rate Limiting

Rate limiting isn't always the answer. Here's when to skip it or use alternatives.

### When Rate Limiting is Overkill

```
DON'T add rate limiting when:

1. Internal service-to-service calls
   Problem: You control both ends, add latency for no benefit
   Better: Use circuit breakers, backpressure

2. Batch/offline processing
   Problem: No real-time constraints
   Better: Queue-based throttling, job scheduling

3. Low-traffic endpoints
   Problem: Overhead exceeds benefit
   Better: Simple validation, maybe no protection

4. Write-once-read-many data
   Problem: Writes are rare, reads are cacheable
   Better: Caching, CDN
```

### When You Need Something Else

**Problem: Protecting against slow clients**

```
Rate limiting says: "You can only send 100 requests/minute"
But what if each request takes 30 seconds to process?

Better: Connection limits, request timeouts, thread pool sizing
```

**Problem: Protecting expensive operations**

```
Rate limiting treats all requests equally.
But GET /users is cheap, POST /analyze-video is expensive.

Better: Operation-based limits (10 videos/day) or cost-based tokens
```

**Problem: Fair sharing among users**

```
Rate limiting per user, but some users share IP.
Or: enterprise customers need higher limits.

Better: Tiered limits, quotas, or reservation systems
```

### Algorithm Selection Pitfalls

```
Token Bucket when you need smooth output
   → Use Leaky Bucket instead

Fixed Window when accuracy matters
   → Use Sliding Window instead

Sliding Window Log for high-volume APIs
   → Memory explodes; use Counter instead

Any single algorithm for distributed systems
   → Need coordination (Redis, consensus)
```

### The Distributed Rate Limiting Challenge

```
Single server: Easy - all state is local
Multiple servers: Hard - state must be shared

Options:
1. Sticky sessions (route user to same server)
   + Simple
   - Uneven load, single point of failure

2. Centralized store (Redis)
   + Accurate
   - Redis becomes bottleneck, adds latency

3. Approximate/probabilistic
   + Fast, scalable
   - Not exact, can over/under limit

Real systems often use hybrid:
- Local rate limiting (fast, approximate)
- Periodic sync with central store (accurate over time)
```

### When to Use Each Algorithm

| Scenario                | Best Algorithm         | Why                              |
| ----------------------- | ---------------------- | -------------------------------- |
| API gateway             | Token Bucket           | Allows bursts for bursty clients |
| Video streaming         | Leaky Bucket           | Smooth, constant bitrate needed  |
| Simple API              | Fixed Window           | Easy to implement and explain    |
| Financial transactions  | Sliding Window Log     | Accuracy critical, low volume    |
| High-traffic public API | Sliding Window Counter | Memory-efficient, good accuracy  |

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
    └── No → Accuracy vs simplicity?
        ├── Simple is fine → Fixed Window Counter
        │                     - Easiest to implement
        │                     - Boundary problem (up to 2x burst)
        │
        └── Need accuracy → How much memory?
            ├── Minimal → Sliding Window Counter
            │             - Approximate but efficient
            │
            └── More OK → Sliding Window Log
                          - Exact but stores all timestamps
```

---

## Edge Cases

1. **Time going backwards**: Use `time.monotonic()` instead of `time.time()` — monotonic clocks never go backwards, even during NTP adjustments or daylight saving changes. Exception: distributed systems where you need wall-clock time for cross-server coordination (use `time.time()` with Redis, since all servers must agree on "now").
2. **Very high request rate**: Cleanup overhead in log-based approaches — consider amortizing cleanup or switching to counter-based approaches.
3. **Distributed systems**: Need truly atomic operations (Redis Lua scripts, not just pipelines). Race conditions are the #1 source of rate limiter bugs in production.
4. **Per-user vs global**: Different keys for different limits. Global limits protect the system; per-user limits ensure fairness.
5. **Different limits per endpoint**: `GET /users` (cheap) vs `POST /analyze-video` (expensive) should have different limits. Consider cost-based token deduction.
6. **Floating point precision**: Weighted estimates can suffer from floating point errors at boundary values. Compare the raw float against the limit (`estimated < limit`) rather than rounding — this avoids subtle off-by-one rejections from rounding schemes.
7. **Cold start**: When a rate limiter restarts, all state is lost. Consider persisting state to Redis or accepting a brief window of no limiting after restart.

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

| #   | Problem                              | Difficulty | Key Concept                    |
| --- | ------------------------------------ | ---------- | ------------------------------ |
| 1   | Design Hit Counter (LC 362)          | Medium     | Sliding window basics          |
| 2   | Logger Rate Limiter (LC 359)         | Easy       | Simple timestamp tracking      |
| 3   | Design Rate Limiter (system design)  | Medium     | Full system design question    |
| 4   | API Rate Limiter                     | Medium     | Token bucket implementation    |
| 5   | Sliding Window Maximum (LC 239)      | Hard       | Related sliding window concept |

---

## Coding Exercises (Progressive)

### Exercise 1: Simple Counter Rate Limiter (Easy)

**Problem:** Implement a rate limiter that allows at most `limit` calls to `allow_request()`
within any contiguous `window_seconds` period. Use a simple list of timestamps.

Focus on correctness, not efficiency.

```python
import time


class SimpleRateLimiter:
    """
    Simplest possible rate limiter using a list of timestamps.

    This is the brute-force approach: store every request timestamp,
    filter out expired ones on each check.

    Time: O(n) per request (scanning the list)
    Space: O(n) where n = number of requests in window
    """

    def __init__(self, limit: int, window_seconds: float) -> None:
        self.limit: int = limit
        self.window: float = window_seconds
        self.timestamps: list[float] = []

    def allow_request(self) -> bool:
        """Return True if request is allowed, False otherwise."""
        now = time.monotonic()
        cutoff = now - self.window

        # Remove expired timestamps
        self.timestamps = [t for t in self.timestamps if t > cutoff]

        if len(self.timestamps) < self.limit:
            self.timestamps.append(now)
            return True

        return False


# ── Tests ──
def test_simple_rate_limiter() -> None:
    limiter = SimpleRateLimiter(limit=3, window_seconds=1.0)

    # 3 requests should all pass
    assert limiter.allow_request() is True   # 1st
    assert limiter.allow_request() is True   # 2nd
    assert limiter.allow_request() is True   # 3rd

    # 4th request should fail (limit = 3)
    assert limiter.allow_request() is False

    # Wait for window to expire, then it should pass again
    time.sleep(1.1)
    assert limiter.allow_request() is True

    print("All tests passed!")


test_simple_rate_limiter()
```

**Key takeaway:** This works but is O(n) per request. The `deque`-based
SlidingWindowLog (Pattern 2) improves this to amortized O(1) by using
`popleft()` instead of rebuilding the list.

---

### Exercise 2: Sliding Window Counter with Testable Clock (Medium)

**Problem:** Implement a SlidingWindowCounter where you can inject a custom clock
function. This makes it testable without `time.sleep()` — critical for reliable
unit tests and interview demonstrations.

```python
import time
from typing import Callable


class TestableWindowCounter:
    """
    Sliding Window Counter with injectable clock for testing.

    In interviews, injecting a clock function shows understanding of:
    - Dependency injection for testability
    - Avoiding time.sleep() in tests (flaky, slow)
    - Separation of concerns

    Time: O(1)
    Space: O(1)
    """

    def __init__(
        self,
        limit: int,
        window_seconds: int,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.limit: int = limit
        self.window: int = window_seconds
        self.clock: Callable[[], float] = clock
        self.prev_count: int = 0
        self.curr_count: int = 0
        self.curr_window: int = 0

    def allow_request(self) -> bool:
        now = self.clock()
        window_id = int(now // self.window)

        if window_id != self.curr_window:
            if window_id == self.curr_window + 1:
                self.prev_count = self.curr_count
            else:
                self.prev_count = 0
            self.curr_window = window_id
            self.curr_count = 0

        window_start = window_id * self.window
        elapsed_ratio = (now - window_start) / self.window
        prev_weight = 1.0 - elapsed_ratio

        estimated = self.prev_count * prev_weight + self.curr_count

        if estimated < self.limit:
            self.curr_count += 1
            return True
        return False


# ── Tests using a fake clock (no time.sleep!) ──
def test_testable_window_counter() -> None:
    fake_time = 0.0

    def fake_clock() -> float:
        return fake_time

    limiter = TestableWindowCounter(limit=5, window_seconds=10, clock=fake_clock)

    # Fill up within first window
    for _ in range(5):
        assert limiter.allow_request() is True
    assert limiter.allow_request() is False  # 6th request rejected

    # Move to next window (10s later) — previous count carries over partially
    fake_time = 15.0  # 50% into second window (window_id=1, window_start=10)
    # Estimated = prev_count * prev_weight + curr_count
    #           = 5 * 0.5 + 0 = 2.5
    assert limiter.allow_request() is True   # 2.5 < 5, allowed; curr_count becomes 1

    # Estimated = 5 * 0.5 + 1 = 3.5
    assert limiter.allow_request() is True   # 3.5 < 5, allowed; curr_count becomes 2
    # Estimated = 5 * 0.5 + 2 = 4.5
    assert limiter.allow_request() is True   # 4.5 < 5, allowed; curr_count becomes 3
    # Estimated = 5 * 0.5 + 3 = 5.5
    assert limiter.allow_request() is False  # 5.5 >= 5, rejected

    # Move far ahead — previous window should be fully expired
    fake_time = 100.0
    for _ in range(5):
        assert limiter.allow_request() is True
    assert limiter.allow_request() is False

    print("All tests passed!")


test_testable_window_counter()
```

**Key takeaway:** Injecting a clock function eliminates `time.sleep()` from tests,
making them fast, deterministic, and non-flaky. This is a technique interviewers
love to see.

---

### Exercise 3: Per-User Rate Limiter with Multiple Tiers (Medium-Hard)

**Problem:** Build a rate limiter that supports different rate limits for different
user tiers (free, pro, enterprise). Each user gets their own independent limit.

```python
import time
from collections import deque
from dataclasses import dataclass
from enum import Enum


class Tier(Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


@dataclass(frozen=True)
class RateLimit:
    """Immutable rate limit configuration."""
    requests: int
    window_seconds: float


# Default tier configurations
TIER_LIMITS: dict[Tier, RateLimit] = {
    Tier.FREE:       RateLimit(requests=10,   window_seconds=60),
    Tier.PRO:        RateLimit(requests=100,  window_seconds=60),
    Tier.ENTERPRISE: RateLimit(requests=1000, window_seconds=60),
}


class PerUserRateLimiter:
    """
    Per-user rate limiter with tiered limits.

    Each user gets their own sliding window log, sized according
    to their tier. Unknown users default to FREE tier.

    Time: O(1) amortized per request
    Space: O(users * max_limit) worst case
    """

    def __init__(
        self,
        tier_limits: dict[Tier, RateLimit] | None = None,
    ) -> None:
        self.tier_limits: dict[Tier, RateLimit] = tier_limits or TIER_LIMITS
        # user_id -> deque of timestamps
        self._user_logs: dict[str, deque[float]] = {}
        # user_id -> tier
        self._user_tiers: dict[str, Tier] = {}

    def register_user(self, user_id: str, tier: Tier) -> None:
        """Register or update a user's tier."""
        self._user_tiers[user_id] = tier

    def allow_request(self, user_id: str) -> bool:
        """Check if a request from user_id is allowed."""
        tier = self._user_tiers.get(user_id, Tier.FREE)
        limit_config = self.tier_limits[tier]

        now = time.monotonic()
        cutoff = now - limit_config.window_seconds

        # Get or create the user's request log
        if user_id not in self._user_logs:
            self._user_logs[user_id] = deque()

        log = self._user_logs[user_id]

        # Remove expired timestamps
        while log and log[0] <= cutoff:
            log.popleft()

        if len(log) < limit_config.requests:
            log.append(now)
            return True

        return False

    def get_remaining(self, user_id: str) -> int:
        """Return how many requests the user has left in current window."""
        tier = self._user_tiers.get(user_id, Tier.FREE)
        limit_config = self.tier_limits[tier]

        now = time.monotonic()
        cutoff = now - limit_config.window_seconds

        log = self._user_logs.get(user_id, deque())

        # Count only non-expired entries
        active = sum(1 for t in log if t > cutoff)
        return max(0, limit_config.requests - active)


# ── Tests ──
def test_per_user_rate_limiter() -> None:
    limiter = PerUserRateLimiter(tier_limits={
        Tier.FREE: RateLimit(requests=2, window_seconds=1.0),
        Tier.PRO:  RateLimit(requests=5, window_seconds=1.0),
    })

    # Free user (default tier)
    assert limiter.allow_request("alice") is True
    assert limiter.allow_request("alice") is True
    assert limiter.allow_request("alice") is False  # Free limit = 2

    # Pro user
    limiter.register_user("bob", Tier.PRO)
    for _ in range(5):
        assert limiter.allow_request("bob") is True
    assert limiter.allow_request("bob") is False  # Pro limit = 5

    # Users are independent — charlie (free) is unaffected by alice/bob
    assert limiter.allow_request("charlie") is True
    assert limiter.allow_request("charlie") is True
    assert limiter.allow_request("charlie") is False

    # Check remaining
    assert limiter.get_remaining("alice") == 0
    assert limiter.get_remaining("bob") == 0

    # Wait for window to expire
    time.sleep(1.1)
    assert limiter.allow_request("alice") is True
    assert limiter.get_remaining("alice") == 1  # Used 1 of 2

    print("All tests passed!")


test_per_user_rate_limiter()
```

**Key takeaway:** In production systems, rate limits are almost never one-size-fits-all.
This exercise demonstrates per-user isolation, tier-based configuration, and
the sliding window log pattern — all common FANG interview discussion points.

---

### Exercise 4: Multi-Key Rate Limiter (Hard)

**Problem:** Build a rate limiter that enforces **multiple simultaneous limits** per
user — for example, 10 requests per second AND 100 requests per minute AND 1000
requests per hour. A request is only allowed if ALL limits pass. This is how
production APIs (e.g., Discord, Twitter) actually work.

```python
import time
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Limit:
    """A single rate limit rule."""
    max_requests: int
    window_seconds: float


class MultiKeyRateLimiter:
    """
    Enforces multiple rate limits simultaneously.

    A request is allowed only if it passes ALL configured limits.
    Uses sliding window log per limit per user.

    Example: 10/sec AND 100/min AND 1000/hour

    Time: O(L) per request where L = number of limits
    Space: O(users * L * max_limit) worst case
    """

    def __init__(self, limits: list[Limit]) -> None:
        if not limits:
            raise ValueError("At least one limit must be provided")
        self.limits: list[Limit] = limits
        # user_id -> list of deques (one per limit)
        self._logs: dict[str, list[deque[float]]] = {}

    def _get_user_logs(self, user_id: str) -> list[deque[float]]:
        """Get or create per-limit logs for a user."""
        if user_id not in self._logs:
            self._logs[user_id] = [deque() for _ in self.limits]
        return self._logs[user_id]

    def allow_request(self, user_id: str) -> bool:
        """
        Check if request passes ALL limits.

        Important: We check all limits BEFORE adding the timestamp to any.
        This prevents partial state corruption if a later limit rejects.
        """
        now = time.monotonic()
        logs = self._get_user_logs(user_id)

        # Phase 1: Clean up expired entries and check all limits
        for i, limit in enumerate(self.limits):
            log = logs[i]
            cutoff = now - limit.window_seconds

            while log and log[0] <= cutoff:
                log.popleft()

            if len(log) >= limit.max_requests:
                return False  # At least one limit exceeded

        # Phase 2: All limits passed — record the request in all logs
        for log in logs:
            log.append(now)

        return True

    def get_status(self, user_id: str) -> list[dict[str, int | float]]:
        """Return remaining capacity for each limit (for HTTP headers)."""
        now = time.monotonic()
        logs = self._get_user_logs(user_id)
        status = []

        for i, limit in enumerate(self.limits):
            log = logs[i]
            cutoff = now - limit.window_seconds
            active = sum(1 for t in log if t > cutoff)
            remaining = max(0, limit.max_requests - active)
            status.append({
                "window_seconds": limit.window_seconds,
                "limit": limit.max_requests,
                "remaining": remaining,
            })

        return status


# ── Tests ──
def test_multi_key_rate_limiter() -> None:
    limiter = MultiKeyRateLimiter(limits=[
        Limit(max_requests=3, window_seconds=1.0),   # 3 per second
        Limit(max_requests=5, window_seconds=10.0),   # 5 per 10 seconds
    ])

    # First 3 requests pass both limits
    for i in range(3):
        assert limiter.allow_request("alice") is True, f"Request {i+1} failed"

    # 4th request fails the per-second limit (3/sec)
    assert limiter.allow_request("alice") is False

    # Wait for per-second window to expire
    time.sleep(1.1)

    # 5th and 6th requests: per-second limit resets, but per-10s limit is at 3
    assert limiter.allow_request("alice") is True   # 4th in 10s window
    assert limiter.allow_request("alice") is True   # 5th in 10s window
    assert limiter.allow_request("alice") is False  # 6th hits 10s limit (5/10s)

    # Check status
    status = limiter.get_status("alice")
    print(f"Per-second: {status[0]['remaining']}/{status[0]['limit']}")
    print(f"Per-10-sec: {status[1]['remaining']}/{status[1]['limit']}")

    # Different user is unaffected
    assert limiter.allow_request("bob") is True

    print("All tests passed!")


test_multi_key_rate_limiter()
```

**Key takeaway:** Real-world APIs enforce multiple overlapping limits. The critical
implementation detail is the **two-phase check-then-write**: check all limits first,
only then record the request. This prevents partial state corruption where one log
records a request but a later limit rejects it.

---

## Related Sections

- [Data Structure Choices](./01-data-structure-choices.md) - Queue and counter structures
- [LRU Cache](./02-lru-cache.md) - Similar time-based eviction concepts
