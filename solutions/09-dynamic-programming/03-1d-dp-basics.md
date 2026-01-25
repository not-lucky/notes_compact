# Solutions: 1D DP Basics

## 1. Climbing Stairs
**Problem:** Count ways to reach the $n$-th step if you can take 1 or 2 steps at a time.

### Optimal Python Solution
```python
def climb_stairs(n: int) -> int:
    # State: dp[i] = ways to reach step i
    # Recurrence: dp[i] = dp[i-1] + dp[i-2]
    # Space optimization: Only need last two values
    if n <= 2:
        return n

    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr

    return prev1
```

### Complexity Analysis
- **Time:** $O(n)$ - Single pass through steps.
- **Space:** $O(1)$ - Only storing the last two results.

---

## 2. Min Cost Climbing Stairs
**Problem:** Find the minimum cost to reach the top of the floor. You can start from step 0 or step 1.

### Optimal Python Solution
```python
def min_cost_climbing_stairs(cost: list[int]) -> int:
    # State: dp[i] = min cost to reach step i
    # Recurrence: dp[i] = cost[i] + min(dp[i-1], dp[i-2])
    n = len(cost)
    prev2, prev1 = cost[0], cost[1]

    for i in range(2, n):
        curr = cost[i] + min(prev1, prev2)
        prev2, prev1 = prev1, curr

    return min(prev1, prev2)
```

### Complexity Analysis
- **Time:** $O(n)$ - Single pass.
- **Space:** $O(1)$ - Constant space.

---

## 3. House Robber
**Problem:** Maximize sum of non-adjacent elements in an array.

### Optimal Python Solution
```python
def rob(nums: list[int]) -> int:
    # State: dp[i] = max money from houses 0..i
    # Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    if not nums: return 0
    if len(nums) == 1: return nums[0]

    prev2, prev1 = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        curr = max(prev1, prev2 + nums[i])
        prev2, prev1 = prev1, curr

    return prev1
```

### Complexity Analysis
- **Time:** $O(n)$
- **Space:** $O(1)$

---

## 4. House Robber II
**Problem:** House Robber on a circular array (first and last are neighbors).

### Optimal Python Solution
```python
def rob_circular(nums: list[int]) -> int:
    if len(nums) == 1: return nums[0]

    def rob_linear(arr):
        p2, p1 = 0, 0
        for x in arr:
            p2, p1 = p1, max(p1, p2 + x)
        return p1

    # Case 1: Rob 0..n-2, Case 2: Rob 1..n-1
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

### Complexity Analysis
- **Time:** $O(n)$ - Two linear passes.
- **Space:** $O(1)$ (ignoring slice overhead, which can be avoided with indices).

---

## 5. Maximum Subarray (Kadane's)
**Problem:** Find contiguous subarray with the largest sum.

### Optimal Python Solution
```python
def max_subarray(nums: list[int]) -> int:
    # State: dp[i] = max sum ending at i
    # Recurrence: dp[i] = max(nums[i], dp[i-1] + nums[i])
    max_sum = curr_sum = nums[0]
    for i in range(1, len(nums)):
        curr_sum = max(nums[i], curr_sum + nums[i])
        max_sum = max(max_sum, curr_sum)
    return max_sum
```

### Complexity Analysis
- **Time:** $O(n)$
- **Space:** $O(1)$

---

## 6. Decode Ways
**Problem:** Count ways to decode a string of digits to letters (1='A', ..., 26='Z').

### Optimal Python Solution
```python
def num_decodings(s: str) -> int:
    if not s or s[0] == '0': return 0

    n = len(s)
    prev2, prev1 = 1, 1 # dp[0], dp[1]

    for i in range(2, n + 1):
        curr = 0
        # Check 1-digit
        if s[i-1] != '0':
            curr += prev1
        # Check 2-digits
        two_digit = int(s[i-2:i])
        if 10 <= two_digit <= 26:
            curr += prev2
        prev2, prev1 = prev1, curr

    return prev1
```

### Complexity Analysis
- **Time:** $O(n)$
- **Space:** $O(1)$

---

## 7. Perfect Squares
**Problem:** Minimum perfect squares that sum to $n$.

### Optimal Python Solution
```python
def num_squares(n: int) -> int:
    # State: dp[i] = min squares for sum i
    # Recurrence: dp[i] = min(dp[i - j*j] + 1) for all j*j <= i
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j*j] + 1)
            j += 1
    return dp[n]
```

### Complexity Analysis
- **Time:** $O(n\sqrt{n})$ - Outer loop $n$, inner loop $\sqrt{n}$.
- **Space:** $O(n)$ - To store results for all sums up to $n$.

---

## 8. Jump Game
**Problem:** Can you reach the last index starting from the first?

### Optimal Python Solution
```python
def can_jump(nums: list[int]) -> bool:
    # Greedy is O(n), DP is also O(n) with reachability
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
    return True
```

### Complexity Analysis
- **Time:** $O(n)$
- **Space:** $O(1)$
