# Coin Change Solutions

## Problem: Coin Change (Minimum Coins)
You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money. Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1. You may assume that you have an infinite number of each kind of coin.

### Constraints
- 1 <= coins.length <= 12
- 1 <= coins[i] <= 2^31 - 1
- 0 <= amount <= 10^4

### Examples
- Input: coins = [1, 2, 5], amount = 11 -> Output: 3 (5 + 5 + 1)
- Input: coins = [2], amount = 3 -> Output: -1

### Implementation

```python
def coin_change(coins: list[int], amount: int) -> int:
    """
    Finds the minimum number of coins to make the amount.
    Time complexity: O(amount * len(coins))
    Space complexity: O(amount)
    """
    # dp[i] will be the minimum coins to make amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

## Problem: Coin Change II (Total Ways)
You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money. Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0.

### Constraints
- 1 <= coins.length <= 300
- 1 <= coins[i] <= 5000
- 0 <= amount <= 5000

### Examples
- Input: amount = 5, coins = [1, 2, 5] -> Output: 4
- Input: amount = 3, coins = [2] -> Output: 0

### Implementation

```python
def change(amount: int, coins: list[int]) -> int:
    """
    Finds total number of ways to make the amount (combinations).
    To count combinations (not permutations), iterate over coins in outer loop.
    Time complexity: O(amount * len(coins))
    Space complexity: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]
```

## Problem: Combination Sum IV (Permutations)
Given an array of distinct integers `nums` and a target integer `target`, return the number of possible combinations that add up to `target`. Note that different sequences are counted as different combinations (permutations).

### Implementation

```python
def combination_sum_4(nums: list[int], target: int) -> int:
    """
    Finds total number of permutations that sum to target.
    To count permutations, iterate over target in outer loop.
    Time complexity: O(target * len(nums))
    Space complexity: O(target)
    """
    dp = [0] * (target + 1)
    dp[0] = 1

    for i in range(1, target + 1):
        for num in nums:
            if num <= i:
                dp[i] += dp[i - num]

    return dp[target]
```
