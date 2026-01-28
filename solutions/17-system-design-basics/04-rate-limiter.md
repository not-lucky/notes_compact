# Solutions for Rate Limiter

This file provides optimal Python solutions for practice problems related to Rate Limiting algorithms and time-windowed counting.

## 1. Design Hit Counter

_Note: This problem is covered in detail in the [LFU Cache Solution File](./03-lfu-cache.md#4-design-hit-counter). It uses a bucket-based array to track hits in a sliding window._

---

## 2. Logger Rate Limiter

### Problem Statement

Design a logger system that receives a stream of messages with their timestamps. Each unique message should only be printed at most every 10 seconds. If a message is received within 10 seconds of being printed, it should be dropped.

### Examples & Edge Cases

- **Example**: `log(1, "foo")` -> True, `log(2, "bar")` -> True, `log(3, "foo")` -> False, `log(11, "foo")` -> True.
- **Edge Cases**:
  - Multiple messages at the same timestamp.
  - Timestamps are non-decreasing.

### Optimal Python Solution

```python
class Logger:
    def __init__(self):
        # Maps message string to the next available timestamp it can be printed
        self.msg_map = {}

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if message not in self.msg_map or timestamp >= self.msg_map[message]:
            self.msg_map[message] = timestamp + 10
            return True
        return False
```

### Explanation

We use a **HashMap** to store the expiration time for each message.

1. If the message is new or the current `timestamp` is greater than or equal to the stored `next_allowed_time`, we update the map and return `True`.
2. Otherwise, we return `False`.

### Complexity Analysis

- **Time Complexity**: $O(1)$ per request.
- **Space Complexity**: $O(M)$ where $M$ is the number of unique messages.

---

## 3. Design Rate Limiter (Token Bucket)

### Problem Statement

Implement a rate limiter that allows a maximum number of requests in a given time period.

### Examples & Edge Cases

- **Example**: `capacity=5`, `refill_rate=1/sec`. A burst of 5 is allowed, then 1 per second.
- **Edge Cases**:
  - Very high frequency requests.
  - Large time gaps between requests (bucket should not exceed capacity).

### Optimal Python Solution

```python
import time

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate # tokens per second
        self.tokens = capacity
        self.last_update = time.time()

    def allow_request(self) -> bool:
        now = time.time()
        # Calculate how many tokens were added since last request
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_update = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

### Explanation

This is the **Token Bucket** algorithm.

1. We track the `last_update` time.
2. Every time `allow_request` is called, we "refill" the bucket based on the elapsed time.
3. If the bucket has at least 1 token, we consume it and allow the request.

### Complexity Analysis

- **Time Complexity**: $O(1)$.
- **Space Complexity**: $O(1)$.

---

## 4. API Rate Limiter (Fixed Window vs Sliding Window)

### Problem Statement

Implement a rate limiter for an API endpoint. Compare a fixed window approach with a sliding window approach.

### Optimal Python Solution (Sliding Window Counter)

```python
import time

class SlidingWindowCounter:
    def __init__(self, limit: int, window_size: int):
        self.limit = limit
        self.window_size = window_size
        self.prev_count = 0
        self.curr_count = 0
        self.curr_window_start = int(time.time() // window_size) * window_size

    def allow_request(self) -> bool:
        now = time.time()
        window_start = int(now // self.window_size) * self.window_size

        if window_start != self.curr_window_start:
            # Shift windows
            self.prev_count = self.curr_count if window_start == self.curr_window_start + self.window_size else 0
            self.curr_count = 0
            self.curr_window_start = window_start

        # Calculate weight of previous window
        elapsed_in_curr = now - self.curr_window_start
        weight_prev = 1 - (elapsed_in_curr / self.window_size)

        estimate = self.prev_count * weight_prev + self.curr_count

        if estimate < self.limit:
            self.curr_count += 1
            return True
        return False
```

### Explanation

The **Sliding Window Counter** approximates a true sliding window using weighted averages of the current and previous fixed windows. This solves the "boundary problem" of Fixed Window (where 2x the limit can pass at the edge of a window) while being much more memory-efficient than a Sliding Window Log.

### Complexity Analysis

- **Time Complexity**: $O(1)$.
- **Space Complexity**: $O(1)$.

---

## 5. Sliding Window Maximum

### Problem Statement

Given an array `nums` and a window size `k`, return the maximum element in each sliding window of size `k`.

### Examples & Edge Cases

- **Example**: `nums = [1,3,-1,-3,5,3,6,7], k = 3` -> `[3,3,5,5,6,7]`.
- **Edge Cases**:
  - `k = 1`: Return the array itself.
  - `k = len(nums)`: Return the max of the whole array.

### Optimal Python Solution

```python
from collections import deque

def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    if not nums: return []
    res = []
    # Store indices of elements in decreasing order of their values
    dq = deque()

    for i, num in enumerate(nums):
        # 1. Remove indices that are out of the current window
        if dq and dq[0] < i - k + 1:
            dq.popleft()

        # 2. Remove smaller elements from the right as they'll never be max
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # 3. Add to result once window is full
        if i >= k - 1:
            res.append(nums[dq[0]])

    return res
```

### Explanation

We use a **Monotonic Dequeue** (Double-ended queue) to store indices of elements.

1. The dequeue maintains indices in a way that `nums[dq[i]]` is strictly decreasing.
2. The current maximum is always at `dq[0]`.
3. For each new element, we discard indices of elements smaller than it (because the new larger element will outlast them in any future window) and discard indices that fall out of the `k` range.

### Complexity Analysis

- **Time Complexity**: $O(N)$. Each element is pushed and popped at most once.
- **Space Complexity**: $O(K)$ for the dequeue.
