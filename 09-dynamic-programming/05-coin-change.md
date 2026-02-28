# Coin Change & Unbounded Knapsack

> **Prerequisites:** [1D DP Basics](./03-1d-dp-basics.md)

## Overview

Coin Change is the canonical **unbounded knapsack** problem. In this pattern, you are given a target amount and a set of item sizes (coin denominations). Unlike the standard 0/1 Knapsack where each item can be used at most once, here you have an **unlimited supply** of each item.

Your goal is typically to find either:
1. The **minimum number of coins** to reach the target amount.
2. The **total number of combinations** (or permutations) to reach the target amount.

## Problem 1: Minimum Coins (Coin Change)

Given an array of integer `coins` and a target `amount`, return the **fewest number of coins** needed to make up that amount. If it cannot be made, return `-1`.

### Why Greedy Fails

A greedy approach (always picking the largest possible coin first) feels natural because it works for canonical currency systems (like US coins: 1, 5, 10, 25). However, it fails for arbitrary denominations.

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

**Rule of Thumb:** You *must* use Dynamic Programming (or BFS) when coin denominations are arbitrary.

### State and Recurrence

To find the minimum coins for `amount`, we must check all possible "last coins" we could have added. If we know the optimal solution for `amount - coin`, we just add 1 to it.

- **State:** `dp[i]` represents the minimum number of coins needed to make the amount `i`.
- **Recurrence:** `dp[i] = min(dp[i], dp[i - coin] + 1)` for each `coin` in `coins`.
- **Base Case:** `dp[0] = 0` (It takes 0 coins to make an amount of 0). Initialize all other states to infinity (`inf`), representing unreachable amounts.

### Visual Walkthrough

`coins = [1, 2, 5]`, `amount = 5`

| i (amount) | 0 | 1 | 2 | 3 | 4 | 5 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `dp[i]` | 0 | 1 | 1 | 2 | 2 | 1 |

*Tracing `dp[5]`*:
To make `5`, we evaluate the states before adding each possible coin:
- Using coin `1`: Look at `dp[5 - 1]`. `dp[4] + 1 = 2 + 1 = 3`.
- Using coin `2`: Look at `dp[5 - 2]`. `dp[3] + 1 = 2 + 1 = 3`.
- Using coin `5`: Look at `dp[5 - 5]`. `dp[0] + 1 = 0 + 1 = 1`.
- `dp[5] = min(3, 3, 1) = 1`.

### Bottom-Up DP (Tabulation)

```python
def coin_change(coins: list[int], amount: int) -> int:
    """
    Finds the minimum number of coins to make the given amount.

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
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return int(dp[amount]) if dp[amount] != float('inf') else -1
```

> **Optimization Note:** For finding the *minimum* coins, you can safely swap the nested loops. Putting `coins` in the outer loop allows you to eliminate the `if i - coin >= 0` check by starting the inner loop directly at `coin`. While loop order doesn't affect the final answer for *minimums*, we will see in Problem 2 that loop order is **critical** when *counting combinations*.

### Alternative: BFS Approach (Shortest Path)

Finding the minimum number of coins to reach exactly `amount` is mathematically equivalent to finding the shortest path in an unweighted graph where nodes are amounts and edges are coins. Breadth-First Search (BFS) explores level-by-level, ensuring the first time we reach the target, it's via the shortest path.

```python
from collections import deque

def coin_change_bfs(coins: list[int], amount: int) -> int:
    """
    BFS approach - finds minimum coins naturally level-by-level.

    Time: O(amount * len(coins)) in the worst case
    Space: O(amount) for the queue and visited set
    """
    if amount == 0:
        return 0

    queue = deque([(0, 0)])  # (current_amount, num_coins_used)
    visited = {0}            # Track visited amounts to avoid cycles/redundant work

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

This problem is infamous for a very specific implementation detail: **the order of your nested loops entirely changes the answer.**

### State and Recurrence

- **State:** `dp[i]` represents the number of ways to make the amount `i`.
- **Recurrence:** `dp[i] += dp[i - coin]`. To find the total ways to make amount `i`, we sum the ways to make `i - coin` for all possible coins.
- **Base Case:** `dp[0] = 1`. There is exactly 1 way to make the amount 0 (by selecting no coins). If initialized to 0, all subsequent additions would remain 0.

### The Loop Order Mystery: Combinations vs Permutations

If we want to count the number of ways to make `3` using `[1, 2]`, what is the answer?
- If we count **combinations** (order doesn't matter), the ways are `{1, 1, 1}` and `{1, 2}`. The answer is **2**.
- If we count **permutations** (order matters), the ways are `(1, 1, 1)`, `(1, 2)`, and `(2, 1)`. The answer is **3**.

How do we control which one our DP calculates? **By the order of the loops.**

#### 1. Combinations (Coins Outer Loop)
To calculate *combinations*, we iterate through `coins` in the outer loop and `amounts` in the inner loop.

```python
def change_combinations(amount: int, coins: list[int]) -> int:
    """
    Counts combinations (order doesn't matter).
    e.g., {1, 2} and {2, 1} are counted once as {1, 2}.
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    # Outer loop: Coins
    for coin in coins:
        # Inner loop: Amounts
        # Notice we can start the loop at 'coin' rather than 1
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]
```

**Why this works:** By putting `coins` on the outside, we say: "Let's find all the ways to make every amount using *only* the first coin. Then, let's go back and add the ways to make every amount using the second coin, building on what we did before."
Because we fully process coin `1` before even looking at coin `2`, we can **never** have a sequence like `(2, 1)`. The coin `1` was added, and then the coin `2` was added on top of it. This enforces an artificial order (sorted by coin), effectively counting combinations.

This is actually a space-optimized 2D DP. In 2D, the state is `dp[coin_idx][amount]`. By dropping the `coin_idx` dimension, we must process the outer loop identically to the 2D version.

#### 2. Permutations (Amount Outer Loop)
To calculate *permutations* (often called Combination Sum IV), we iterate through `amounts` in the outer loop and `coins` in the inner loop.

```python
def change_permutations(amount: int, coins: list[int]) -> int:
    """
    Counts permutations (order matters).
    e.g., (1, 2) and (2, 1) are counted as distinct sequences.
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    # Outer loop: Amounts
    for i in range(1, amount + 1):
        # Inner loop: Coins
        for coin in coins:
            # We must check bounds since we iterate over all coins
            if i - coin >= 0:
                dp[i] += dp[i - coin]

    return dp[amount]
```

**Why this works:** By putting `amount` on the outside, we say: "To solve for amount `i`, what happens if my *very last* step is adding coin 1? What if my very last step is adding coin 2?"
For amount `3`, it asks:
- "If I add a 1 as the last step, how many ways were there to make 2?" (Includes paths ending in 1)
- "If I add a 2 as the last step, how many ways were there to make 1?" (Includes paths ending in 2)
Because any coin can be added at any step to build up to the current amount, different orderings are counted separately.

### Summary of Loop Order

| Aspect | Combinations (Coin Change II) | Permutations (Combination Sum IV) |
| :--- | :--- | :--- |
| **Loop Order** | `coins` outer, `amount` inner | `amount` outer, `coins` inner |
| **Duplicates** | `{1, 2}` is identical to `{2, 1}` | `(1, 2)` and `(2, 1)` are distinct |
| **Mental Model** | Process one coin entirely, then the next | Build target step-by-step using any coin |

---

## Restoring the Path (Finding Which Coins Were Used)

Sometimes finding the minimum number of coins isn't enough; you also need to know *which* coins were used. We can achieve this by storing a `last_coin` array that tracks the decision that led to the optimal state.

```python
def coin_change_with_path(coins: list[int], amount: int) -> tuple[int, list[int]]:
    """
    Returns (min_coins, list_of_coins_used).

    Time: O(amount * len(coins))
    Space: O(amount) for DP arrays
    """
    dp = [float('inf')] * (amount + 1)
    last_coin = [-1] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0 and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                last_coin[i] = coin  # Track which coin got us here optimally

    if dp[amount] == float('inf'):
        return -1, []

    # Reconstruct path by walking backwards from amount to 0
    coins_used = []
    curr = amount
    while curr > 0:
        used = last_coin[curr]
        coins_used.append(used)
        curr -= used

    return int(dp[amount]), coins_used
```

---

## Related Pattern: Generating "Coins" Dynamically

Some problems are just Coin Change in disguise, where the "coins" aren't given to you in an array, but are generated dynamically based on the target.

### Perfect Squares

Find the minimum number of perfect square numbers (`1, 4, 9, 16, ...`) that sum to `n`.
*This is exactly Coin Change where the "coins" are perfect squares up to `n`.*

```python
def num_squares(n: int) -> int:
    """
    Finds the minimum number of perfect squares that sum to n.

    Time: O(n * sqrt(n))
    Space: O(n)
    """
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        # Generate our "coins" (perfect squares) on the fly
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1

    return int(dp[n])
```

---

## Common Pitfalls and Edge Cases

### 1. Initializing the DP Array Incorrectly
For "Minimum Coins" variations, initializing the DP array with `0` is a fatal mistake because `min(0, dp[i - coin] + 1)` will always prefer `0`.
```python
# WRONG (for min problems)
dp = [0] * (amount + 1)

# CORRECT (for min problems)
dp = [float('inf')] * (amount + 1)
dp[0] = 0
```
Conversely, for "Counting Ways", you must initialize with `0`, but explicitly set `dp[0] = 1`.

### 2. Inner Loop Optimization
Notice in the Combinations code, the inner loop starts at `coin`:
```python
for i in range(coin, amount + 1):
```
This is a clean optimization. We don't need to check `if i - coin >= 0` because the loop bounds guarantee it. Any amount strictly less than `coin` obviously cannot be made using `coin`.

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
| [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | Min Coins | Initialize with `inf` |
| [Coin Change II](https://leetcode.com/problems/coin-change-ii/) | Medium | Combinations | `coins` in the outer loop |
| [Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/) | Medium | Permutations | `amount` in the outer loop |
| [Perfect Squares](https://leetcode.com/problems/perfect-squares/) | Medium | Min Coins | "Coins" are perfect squares generated on the fly |

---

## Key Takeaways

1. **Unbounded Knapsack:** Items (coins) can be reused infinitely. DP iterates forwards rather than backwards (unlike 0/1 knapsack).
2. **The Loop Order Rule:**
   - `coins` outer, `amounts` inner = **Combinations** (order doesn't matter).
   - `amounts` outer, `coins` inner = **Permutations** (order matters).
3. **Initialization Matters:** Use `infinity` for minimum finding problems and `0` for counting problems.
4. **Base Cases:** Making an amount of `0` requires `0` coins (Min Coins) and has `1` way to do it (Count Ways).
