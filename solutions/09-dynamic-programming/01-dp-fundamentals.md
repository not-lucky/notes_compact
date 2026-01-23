# DP Fundamentals Solutions

## Problem: Fibonacci Number
The Fibonacci numbers, commonly denoted F(n) form a sequence, called the Fibonacci sequence, such that each number is the sum of the two preceding ones, starting from 0 and 1.

### Constraints
- 0 <= n <= 30

### Examples
- Input: n = 2 -> Output: 1
- Input: n = 4 -> Output: 3

### Implementation

```python
def fib_memo(n: int, memo: dict = None) -> int:
    """
    Top-down DP with memoization.
    Time complexity: O(n)
    Space complexity: O(n)
    """
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

def fib_tab(n: int) -> int:
    """
    Bottom-up DP with tabulation.
    Time complexity: O(n)
    Space complexity: O(n)
    """
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

def fib_optimized(n: int) -> int:
    """
    Space optimized DP.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1
```

## Problem: Climbing Stairs
You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

### Constraints
- 1 <= n <= 45

### Examples
- Input: n = 2 -> Output: 2
- Input: n = 3 -> Output: 3

### Implementation

```python
def climb_stairs(n: int) -> int:
    """
    Climbing stairs using space-optimized DP.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1
```
