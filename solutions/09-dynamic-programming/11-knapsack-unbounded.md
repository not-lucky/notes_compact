# Unbounded Knapsack Solutions

## Problem: Unbounded Knapsack
Given weights and values of `n` items with unlimited supply, put these items in a knapsack of capacity `W` to get the maximum total value in the knapsack.

### Constraints
- 1 <= n <= 1000
- 1 <= W <= 1000

### Implementation

```python
def unbounded_knapsack(weights: list[int], values: list[int], W: int) -> int:
    """
    Unbounded Knapsack using space-optimized 1D DP.
    Time complexity: O(n * W)
    Space complexity: O(W)
    """
    n = len(weights)
    dp = [0] * (W + 1)

    for i in range(n):
        # Iterate forward to allow multiple use of the same item
        for w in range(weights[i], W + 1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[W]
```

## Problem: Rod Cutting
Given a rod of length `n` inches and an array of prices that includes prices of all pieces of size smaller than `n`. Determine the maximum value obtainable by cutting up the rod and selling the pieces.

### Implementation

```python
def rod_cutting(prices: list[int], n: int) -> int:
    """
    Finds maximum value from cutting a rod of length n.
    prices[i] is the price of a rod of length i+1.
    Time complexity: O(n^2)
    Space complexity: O(n)
    """
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        for j in range(1, i + 1):
            dp[i] = max(dp[i], prices[j-1] + dp[i-j])

    return dp[n]
```

## Problem: Integer Break
Given an integer `n`, break it into the sum of `k` positive integers, where `k >= 2`, and maximize the product of those integers.

### Implementation

```python
def integer_break(n: int) -> int:
    """
    Maximizes product of integers summing to n.
    Time complexity: O(n^2)
    Space complexity: O(n)
    """
    if n <= 3:
        return n - 1

    dp = [0] * (n + 1)
    dp[2] = 2
    dp[3] = 3

    for i in range(4, n + 1):
        for j in range(2, i // 2 + 1):
            dp[i] = max(dp[i], dp[j] * dp[i-j])

    return dp[n]
```
