# Monotonic Queue / Sliding Window Maximum

## Practice Problems

### 1. Sliding Window Maximum
**Difficulty:** Hard
**Key Technique:** Monotonic decreasing deque of indices

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Time: O(n)
    Space: O(k)
    """
    q = deque()
    res = []
    for i, n in enumerate(nums):
        # Expiry
        if q and q[0] <= i - k:
            q.popleft()
        # Monotonicity
        while q and nums[q[-1]] < n:
            q.pop()
        q.append(i)
        # Record
        if i >= k - 1:
            res.append(nums[q[0]])
    return res
```

### 2. Shortest Subarray with Sum at Least K
**Difficulty:** Hard
**Key Technique:** Monotonic increasing deque of prefix sums

```python
from collections import deque

def shortest_subarray(nums: list[int], k: int) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    n = len(nums)
    pref = [0] * (n + 1)
    for i in range(n): pref[i+1] = pref[i] + nums[i]

    res = n + 1
    q = deque()
    for i, p in enumerate(pref):
        # Result update
        while q and p - pref[q[0]] >= k:
            res = min(res, i - q.popleft())
        # Monotonicity
        while q and pref[q[-1]] >= p:
            q.pop()
        q.append(i)

    return res if res <= n else -1
```

### 3. Jump Game VI
**Difficulty:** Medium
**Key Technique:** DP + Monotonic deque for range maximum

```python
from collections import deque

def max_result(nums: list[int], k: int) -> int:
    """
    Time: O(n)
    Space: O(k)
    """
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    q = deque([0]) # indices of max dp values

    for i in range(1, n):
        # Expiry
        if q[0] < i - k:
            q.popleft()
        dp[i] = nums[i] + dp[q[0]]
        # Monotonicity
        while q and dp[q[-1]] <= dp[i]:
            q.pop()
        q.append(i)

    return dp[-1]
```

### 4. Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit
**Difficulty:** Medium
**Key Technique:** Two monotonic deques (max and min)

```python
from collections import deque

def longest_subarray(nums: list[int], limit: int) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    max_q = deque()
    min_q = deque()
    l = 0
    res = 0
    for r, n in enumerate(nums):
        while max_q and nums[max_q[-1]] < n: max_q.pop()
        while min_q and nums[min_q[-1]] > n: min_q.pop()
        max_q.append(r)
        min_q.append(r)

        while nums[max_q[0]] - nums[min_q[0]] > limit:
            l += 1
            if max_q[0] < l: max_q.popleft()
            if min_q[0] < l: min_q.popleft()
        res = max(res, r - l + 1)
    return res
```
