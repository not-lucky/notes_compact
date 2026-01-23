# Knapsack Solutions

## Problem: 0/1 Knapsack
Given weights and values of `n` items, put these items in a knapsack of capacity `W` to get the maximum total value in the knapsack.

### Constraints
- 1 <= n <= 1000
- 1 <= W <= 1000

### Implementation

```python
def knapsack_01(weights: list[int], values: list[int], W: int) -> int:
    """
    Standard 0/1 Knapsack using space-optimized 1D DP.
    Time complexity: O(n * W)
    Space complexity: O(W)
    """
    n = len(weights)
    dp = [0] * (W + 1)

    for i in range(n):
        # Iterate backwards to ensure each item is used at most once
        for w in range(W, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[W]
```

## Problem: Partition Equal Subset Sum
Given a non-empty array `nums` containing only positive integers, find if the array can be partitioned into two subsets such that the sum of elements in both subsets is equal.

### Implementation

```python
def can_partition(nums: list[int]) -> bool:
    """
    Checks if array can be partitioned into two equal sum subsets.
    Reduces to a 0/1 Knapsack (Subset Sum) problem.
    Time complexity: O(n * sum/2)
    Space complexity: O(sum/2)
    """
    total_sum = sum(nums)
    if total_sum % 2 != 0:
        return False

    target = total_sum // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for t in range(target, num - 1, -1):
            dp[t] = dp[t] or dp[t - num]

    return dp[target]
```

## Problem: Target Sum
You are given an integer array `nums` and an integer `target`. You want to build an expression out of nums by adding one of the symbols '+' and '-' before each integer in nums and then concatenate all the integers. Return the number of different expressions that you can build, which evaluates to `target`.

### Implementation

```python
def find_target_sum_ways(nums: list[int], target: int) -> int:
    """
    Finds number of ways to reach target using + or -.
    Sum(P) - Sum(N) = target
    Sum(P) + Sum(N) = Total
    2 * Sum(P) = target + Total
    Sum(P) = (target + Total) / 2
    Time complexity: O(n * Sum(P))
    Space complexity: O(Sum(P))
    """
    total = sum(nums)
    if abs(target) > total or (target + total) % 2 != 0:
        return 0

    subset_sum = (target + total) // 2
    dp = [0] * (subset_sum + 1)
    dp[0] = 1

    for num in nums:
        for t in range(subset_sum, num - 1, -1):
            dp[t] += dp[t - num]

    return dp[subset_sum]
```
