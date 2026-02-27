# Coin Change

> **Prerequisites:** [1D DP Basics](./03-1d-dp-basics.md)

## Overview

Coin Change is the canonical **unbounded knapsack** problem. In this pattern, you need to find either the **minimum number of coins** or the **total number of combinations** to reach a target amount using an unlimited supply of given coin denominations.

## Building Intuition

**Why does Coin Change work with DP?**

1. **Optimal Substructure**: If the optimal way to make an amount of `11` uses a coin of value `5`, then the remaining amount `6` must also be made optimally. Using a suboptimal solution for `6` would make the overall solution for `11` suboptimal.
2. **Overlapping Subproblems**: To make `11`, we might try subtracting a `1` or a `5`. The subproblem for `10` (after subtracting `1`) will eventually need to evaluate the amount `5`, and the subproblem for `6` (after subtracting `5`) will also need to evaluate `5`. We repeatedly solve for the same remaining amounts.
3. **The Unbounded Nature**: Unlike the standard 0/1 Knapsack problem where items can only be used once, Coin Change allows using the same coin multiple times. This changes the traversal direction: we iterate forward through the amounts so that updated values can immediately be reused.
4. **Mental Model**: Think of building a staircase. To reach step `N`, you can hop from any step that is exactly one coin-value behind. The minimum hops to reach `N` is `1 + minimum hops to the best valid previous step`.

## Why Greedy Fails

A greedy approach (always picking the largest possible coin first) does not always yield the minimum number of coins for arbitrary denominations.

```text
coins = [1, 3, 4], amount = 6

Greedy approach:
- Pick 4 (remaining: 2)
- Pick 1 (remaining: 1)
- Pick 1 (remaining: 0)
Total coins: 3 (4 + 1 + 1)

Optimal DP approach:
- Pick 3 (remaining: 3)
- Pick 3 (remaining: 0)
Total coins: 2 (3 + 3)
```

**Rule of Thumb:** Greedy works for canonical systems (like standard US currency: 1, 5, 10, 25), but you *must* use DP when coin denominations are arbitrary.

---

## When to Use the Coin Change Pattern

**Recognize the pattern when:**
- You have an unlimited use of items (unbounded knapsack).
- You are trying to reach an exact target sum or amount.
- You need to minimize a count OR find the number of possible combinations.
- All values involved are non-negative.

**Do NOT use this pattern when:**
- Items can only be used once (**0/1 Knapsack**).
- Finding permutations where order matters, e.g., `{1, 2}` is different from `{2, 1}` (this requires a different loop order).
- The amount is massive (e.g., $10^9$) and memory is limited. This might require math or matrix exponentiation.

---

## Problem 1: Minimum Coins (Coin Change)

Given an array of integer `coins` and a target `amount`, return the fewest number of coins needed to make up that amount. If it cannot be made, return `-1`.

### State and Recurrence

- **State:** `dp[i]` represents the minimum number of coins needed to make the amount `i`.
- **Recurrence:** `dp[i] = min(dp[i], dp[i - coin] + 1)` for each `coin` in `coins`.
- **Base Case:** `dp[0] = 0` (It takes 0 coins to make an amount of 0). All other states are initialized to infinity (`inf`), representing unreachable amounts.

### Visual Walkthrough

`coins = [1, 2, 5]`, `amount = 5`

| i (amount) | 0 | 1 | 2 | 3 | 4 | 5 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `dp[i]` | 0 | 1 | 1 | 2 | 2 | 1 |

*Explanation for `dp[5]`*:
- From coin `1`: `dp[5 - 1] + 1` = `dp[4] + 1` = $2 + 1 = 3$
- From coin `2`: `dp[5 - 2] + 1` = `dp[3] + 1` = $2 + 1 = 3$
- From coin `5`: `dp[5 - 5] + 1` = `dp[0] + 1` = $0 + 1 = 1$
- `dp[5] = min(3, 3, 1) = 1`

### Bottom-Up DP (Tabulation)

```python
def coin_change(coins: list[int], amount: int) -> int:
    """
    Minimum coins to make amount.

    Time: O(amount * len(coins))
    Space: O(amount)
    """
    # Initialize DP array with infinity
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed to make amount 0

    # For every amount from 1 to target
    for i in range(1, amount + 1):
        for coin in coins:
            # If the coin can be used for this amount
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

### Top-Down DP (Memoization)

```python
def coin_change_memo(coins: list[int], amount: int) -> int:
    """
    Memoized recursive solution for min coins.
    """
    memo = {}

    def dp(remaining: int) -> int:
        if remaining == 0:
            return 0
        if remaining < 0:
            return float('inf')
        if remaining in memo:
            return memo[remaining]

        min_coins = float('inf')
        for coin in coins:
            result = dp(remaining - coin)
            if result != float('inf'):
                min_coins = min(min_coins, result + 1)

        memo[remaining] = min_coins
        return min_coins

    ans = dp(amount)
    return ans if ans != float('inf') else -1
```

### BFS Approach (Shortest Path)

Finding the minimum number of coins is equivalent to finding the shortest path in an unweighted graph, making Breadth-First Search (BFS) a highly effective approach.

```python
from collections import deque

def coin_change_bfs(coins: list[int], amount: int) -> int:
    """
    BFS approach - finds minimum coins naturally level-by-level.
    """
    if amount == 0:
        return 0

    queue = deque([(0, 0)])  # (current_amount, num_coins_used)
    visited = {0}            # Keep track of visited amounts to avoid cycles

    while queue:
        curr_amt, num_coins = queue.popleft()

        for coin in coins:
            next_amt = curr_amt + coin

            if next_amt == amount:
                return num_coins + 1

            # Only add to queue if we haven't seen this exact sum before
            # and it doesn't exceed the target amount
            if next_amt < amount and next_amt not in visited:
                visited.add(next_amt)
                queue.append((next_amt, num_coins + 1))

    return -1
```

---

## Problem 2: Number of Ways (Coin Change II)

Given `coins` and an `amount`, return the **number of combinations** that make up that amount.

### State and Recurrence

- **State:** `dp[i]` represents the number of ways to make the amount `i`.
- **Recurrence:** `dp[i] = dp[i] + dp[i - coin]` for each `coin`.
- **Base Case:** `dp[0] = 1`. There is exactly 1 way to make the amount 0 (by selecting no coins). If initialized to 0, all subsequent additions would remain 0.

### Loop Ordering Is Critical

To count **combinations** (where `{1, 2}` and `{2, 1}` are considered the same), you must iterate through the `coins` in the outer loop and the `amounts` in the inner loop.

This ensures a coin is fully processed across all amounts before the next coin is considered, preventing the same set of coins from being counted in different orders.

### Visual Walkthrough

`coins = [1, 2]`, `amount = 3`

| i (amount) | 0 | 1 | 2 | 3 |
| :--- | :--- | :--- | :--- | :--- |
| Initial `dp` | 1 | 0 | 0 | 0 |
| After coin `1` | 1 | 1 | 1 | 1 |
| After coin `2` | 1 | 1 | 2 | 2 |

*Explanation*:
- **Initial:** `dp[0] = 1`, all others 0.
- **Coin `1` pass:**
  - `dp[1] += dp[0]` $\rightarrow 1$
  - `dp[2] += dp[1]` $\rightarrow 1$
  - `dp[3] += dp[2]` $\rightarrow 1$
  *(At this point, ways to make 3: `{1, 1, 1}`)*
- **Coin `2` pass:**
  - `dp[2] += dp[0]` $\rightarrow 1 + 1 = 2$ ways (`{1,1}`, `{2}`)
  - `dp[3] += dp[1]` $\rightarrow 1 + 1 = 2$ ways (`{1,1,1}`, `{1,2}`)

### Bottom-Up DP (Combinations)

```python
def change(amount: int, coins: list[int]) -> int:
    """
    Count combinations (order doesn't matter).
    Key: Coins outer loop, amounts inner loop.

    Time: O(amount * len(coins))
    Space: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1  # 1 way to make amount 0

    # Process one coin entirely before moving to the next
    for coin in coins:
        # We start checking from `coin` because any amount less than `coin`
        # obviously can't be made using this coin.
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]
```

### Permutations vs. Combinations

What happens if you swap the loop order? You calculate **permutations**, where order matters. `{1, 2}` and `{2, 1}` are counted as distinct paths.

```python
def num_ways_permutations(amount: int, coins: list[int]) -> int:
    """
    Count permutations (order matters).
    Key: Amount outer loop, coins inner loop.
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] += dp[i - coin]

    return dp[amount]
```

| Aspect | Combinations (Coin Change II) | Permutations (Combination Sum IV) |
| :--- | :--- | :--- |
| **Loop Order** | `coins` outer, `amount` inner | `amount` outer, `coins` inner |
| **Duplicates** | `{1, 2}` same as `{2, 1}` | `{1, 2}` and `{2, 1}` are distinct |

---

## Restoring the Path (Finding Which Coins Were Used)

Often, finding the minimum coins isn't enough; you also need to know *which* coins were used. We can achieve this by storing a `parent` or `last_coin` array.

```python
def coin_change_with_path(coins: list[int], amount: int) -> tuple[int, list[int]]:
    """
    Return (min_coins, list_of_coins_used).
    """
    dp = [float('inf')] * (amount + 1)
    last_coin = [-1] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                last_coin[i] = coin  # Track which coin got us here optimally

    if dp[amount] == float('inf'):
        return -1, []

    # Reconstruct path backwards from amount to 0
    coins_used = []
    curr = amount
    while curr > 0:
        used = last_coin[curr]
        coins_used.append(used)
        curr -= used

    return dp[amount], coins_used
```

---

## Related Problems

### Perfect Squares

Find the minimum number of perfect square numbers (`1, 4, 9, 16, ...`) that sum to `n`.
*This is exactly Coin Change where the "coins" are dynamically generated perfect squares up to `n`.*

```python
def num_squares(n: int) -> int:
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1

    return dp[n]
```

---

## Common Pitfalls and Edge Cases

### 1. Initializing the DP Array Incorrectly
For the "Minimum Coins" variation, initializing the DP array with `0` is a fatal mistake because the `min()` function will always prefer `0` over any actual count.
```python
# WRONG
dp = [0] * (amount + 1)

# CORRECT
dp = [float('inf')] * (amount + 1)
dp[0] = 0
```

### 2. Edge Cases to Handle
- **`amount == 0`**: Should return `0` (or `1` for combinations). DP arrays automatically handle this via the base case.
- **Impossible amounts**: Be sure to return `-1` or `0` depending on the problem constraints when the final DP state is unreachable.
- **Large amount, tiny coins**: Be aware of potential Time Limit Exceeded (TLE) if `amount` is huge and constraints allow for optimized mathematical approaches.

---

## Complexity Analysis

| Problem Variant | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| **Minimum Coins (DP)** | $O(A \times C)$ | $O(A)$ |
| **Minimum Coins (BFS)**| $O(A \times C)$ | $O(A)$ |
| **Number of Ways** | $O(A \times C)$ | $O(A)$ |
| **Perfect Squares** | $O(A \sqrt{A})$ | $O(A)$ |

*Where $A$ is the `amount` and $C$ is the number of `coins`.*

---

## Practice Problems

| Problem | Difficulty | Variant | Key Insight |
| :--- | :--- | :--- | :--- |
| [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | Min Coins | Use `inf` initialization |
| [Coin Change II](https://leetcode.com/problems/coin-change-ii/) | Medium | Combinations | Coins in the outer loop |
| [Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/) | Medium | Permutations | Amount in the outer loop |
| [Perfect Squares](https://leetcode.com/problems/perfect-squares/) | Medium | Min Coins | "Coins" are perfect squares |

---

## Key Takeaways

1. **Unbounded Knapsack:** Items (coins) can be reused infinitely. DP iterates forwards rather than backwards.
2. **Combinations vs. Permutations:** Loop ordering determines whether you are counting unique combinations of coins or order-dependent permutations.
3. **Initialization Matters:** Use `infinity` for minimum finding problems and `0` for counting problems.
4. **Base Cases:** Making an amount of `0` requires `0` coins (Min Coins) and has `1` way to do it (Count Ways).

---

## Next Steps

Now that you've mastered unbounded knapsack and standard linear sequences, it's time to tackle subsequences.

**Next:** [Longest Increasing Subsequence](./06-longest-increasing-subsequence.md)