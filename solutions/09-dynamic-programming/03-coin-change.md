# Coin Change

## Problem Statement

Given an array of coin denominations and a target amount, find the fewest number of coins needed to make up that amount.

If it's impossible to make the amount, return -1.

You have an infinite supply of each coin denomination.

**Example:**
```
Input: coins = [1, 2, 5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1

Input: coins = [2], amount = 3
Output: -1

Input: coins = [1], amount = 0
Output: 0
```

## Building Intuition

### Why This Works

The insight is to think about the **last coin** you use. To make amount X, the last coin must be one of your denominations - say, coin C. That means before adding C, you had amount X-C, which you made optimally with some number of coins. So `dp[X] = dp[X-C] + 1`. Since you don't know which coin is best for the last position, try all of them and take the minimum.

This is **Unbounded Knapsack**: you can use each coin infinitely many times, and you're minimizing the count (not maximizing value). The DP array builds from amount 0 upward, ensuring that when you compute dp[X], all values dp[X-coin] are already known (since X-coin < X for positive coins).

The key to understanding why greedy fails: with coins [1, 3, 4] and amount 6, greedy picks 4+1+1 (3 coins), but optimal is 3+3 (2 coins). DP exhaustively considers all paths, guaranteeing optimality.

### How to Discover This

When you see "minimum number of..." with unlimited supply, think Unbounded Knapsack. The recurrence template is: `dp[amount] = min(dp[amount - coin] + 1)` for all coins. The "+1" represents using one coin; the recursive call solves the remaining amount optimally. Initialize dp[0] = 0 (zero coins to make zero amount) and everything else to infinity.

### Pattern Recognition

This is the **Unbounded Knapsack / Coin Change** pattern. Recognize it when:
- You have a set of items that can be reused infinitely
- You want to reach a target sum/value
- You're optimizing (min/max) or counting ways

## When NOT to Use

- **When each coin can only be used once**: That's 0/1 Knapsack, requiring a different DP approach (iterate coins outer, amount inner, in reverse).
- **When the amount is extremely large**: O(amount x coins) might be too slow. Consider BFS or meet-in-the-middle techniques.
- **When coins have associated costs different from "1 per coin"**: You'd minimize total cost, not count.
- **When order matters in the combination**: Coin Change counts combinations (1+2 = 2+1), not permutations. For permutations, iterate amounts before coins.

## Approach

### Key Insight
This is an **Unbounded Knapsack** problem. For each amount, try using each coin and find the minimum.

`dp[amount] = min(dp[amount - coin] + 1)` for all valid coins

### Build from Bottom
Start from amount 0 and build up to target.

## Implementation

```python
def coin_change(coins: list[int], amount: int) -> int:
    """
    Find minimum coins using bottom-up DP.

    Time: O(amount × len(coins))
    Space: O(amount)
    """
    # dp[i] = minimum coins to make amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_memo(coins: list[int], amount: int) -> int:
    """
    Top-down with memoization.

    Time: O(amount × len(coins))
    Space: O(amount)
    """
    memo = {}

    def helper(remaining: int) -> int:
        if remaining == 0:
            return 0
        if remaining < 0:
            return float('inf')
        if remaining in memo:
            return memo[remaining]

        min_coins = float('inf')
        for coin in coins:
            result = helper(remaining - coin)
            min_coins = min(min_coins, result + 1)

        memo[remaining] = min_coins
        return min_coins

    result = helper(amount)
    return result if result != float('inf') else -1


def coin_change_bfs(coins: list[int], amount: int) -> int:
    """
    BFS approach: find shortest path to amount.

    Time: O(amount × len(coins))
    Space: O(amount)
    """
    if amount == 0:
        return 0

    from collections import deque

    visited = {0}
    queue = deque([0])
    level = 0

    while queue:
        level += 1
        for _ in range(len(queue)):
            current = queue.popleft()
            for coin in coins:
                next_amount = current + coin
                if next_amount == amount:
                    return level
                if next_amount < amount and next_amount not in visited:
                    visited.add(next_amount)
                    queue.append(next_amount)

    return -1
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Bottom-up DP | O(A × C) | O(A) | A = amount, C = coins |
| Memoization | O(A × C) | O(A) | Same complexity |
| BFS | O(A × C) | O(A) | May be faster in practice |

## Visual Walkthrough

```
coins = [1, 2, 5], amount = 11

dp array evolution:

Initial: dp = [0, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞]
                0  1  2  3  4  5  6  7  8  9  10 11

i=1: dp[1] = min(dp[0]+1) = 1           [0,1,∞,∞,∞,∞,∞,∞,∞,∞,∞,∞]
i=2: dp[2] = min(dp[1]+1, dp[0]+1) = 1  [0,1,1,∞,∞,∞,∞,∞,∞,∞,∞,∞]
i=3: dp[3] = min(dp[2]+1, dp[1]+1) = 2  [0,1,1,2,∞,∞,∞,∞,∞,∞,∞,∞]
i=4: dp[4] = min(dp[3]+1, dp[2]+1) = 2  [0,1,1,2,2,∞,∞,∞,∞,∞,∞,∞]
i=5: dp[5] = min(dp[4]+1, dp[3]+1, dp[0]+1) = 1  [0,1,1,2,2,1,∞,∞,∞,∞,∞,∞]
...
i=11: dp[11] = 3 (5+5+1)

Result: 3
```

## Edge Cases

1. **Amount = 0**: Return 0 (need 0 coins)
2. **Single coin equals amount**: Return 1
3. **Impossible**: `coins=[2]`, amount=3 → -1
4. **Single coin = 1**: Always possible, return amount
5. **Large amount**: Algorithm handles efficiently
6. **Empty coins**: Return -1 if amount > 0

## Common Mistakes

1. **Forgetting base case dp[0] = 0**: Essential for building solution
2. **Not checking for infinity**: May return wrong answer
3. **Off-by-one in loops**: Should go to amount + 1
4. **Using greedy**: Greedy doesn't always work (e.g., [1,3,4], amount=6)

## Why Greedy Fails

```
coins = [1, 3, 4], amount = 6

Greedy: 4 + 1 + 1 = 3 coins
Optimal: 3 + 3 = 2 coins

Greedy picks largest first but misses better combinations.
```

## Variations

### Coin Change II (Number of Ways)
```python
def coin_change_ii(coins: list[int], amount: int) -> int:
    """
    Count NUMBER of ways to make amount.
    Order doesn't matter (1+2 = 2+1).

    Time: O(amount × coins)
    Space: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    # Process coin by coin (not amount by amount)
    # This ensures we count combinations, not permutations
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]
```

### Combination Sum IV (Permutations)
```python
def combination_sum_iv(nums: list[int], target: int) -> int:
    """
    Count ways where order MATTERS (1+2 ≠ 2+1).

    Time: O(target × nums)
    Space: O(target)
    """
    dp = [0] * (target + 1)
    dp[0] = 1

    # Process amount by amount (not coin by coin)
    for i in range(1, target + 1):
        for num in nums:
            if num <= i:
                dp[i] += dp[i - num]

    return dp[target]
```

### Perfect Squares
```python
def num_squares(n: int) -> int:
    """
    Minimum perfect squares that sum to n.
    Same as coin change with coins = [1, 4, 9, 16, ...]

    Time: O(n × sqrt(n))
    Space: O(n)
    """
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j*j] + 1)
            j += 1

    return dp[n]
```

### Word Break (Similar Pattern)
```python
def word_break(s: str, word_dict: list[str]) -> bool:
    """
    Can string s be segmented into dictionary words?
    Similar to coin change with words as coins.

    Time: O(n² × m) where m is avg word length
    Space: O(n)
    """
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True

    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[len(s)]
```

## Related Problems

- **Coin Change II** - Count combinations
- **Combination Sum IV** - Count permutations
- **Perfect Squares** - Squares as coins
- **Word Break** - Words as coins
- **Minimum Cost For Tickets** - Variant with costs
- **Integer Break** - Similar optimization pattern
