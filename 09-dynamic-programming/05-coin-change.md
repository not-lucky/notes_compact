# Coin Change & Unbounded Knapsack

> **Prerequisites:** [1D DP Basics](./03-1d-dp-basics.md)

## Overview

Coin Change introduces the **unbounded knapsack** pattern: you have an **unlimited supply** of each item (coin).

Goals are usually to find:
1. The **minimum coins** to reach a target amount.
2. The **number of combinations** to reach a target amount.

## Problem 1: Minimum Coins

Given integer `coins` and a target `amount`, return the **fewest coins** needed. Return `-1` if impossible.

### Why Greedy Fails
Greedy works for standard currency (e.g. US coins) but fails for arbitrary denominations. For `coins=[1, 3, 4]` and `amount=6`, greedy picks `4, 1, 1` (3 coins), but optimal is `3, 3` (2 coins).

### State and Recurrence

To find the minimum coins for `amount`, we must check all possible "last coins" we could have added. If we know the optimal solution for `amount - coin`, we just add 1 to it.

- **State:** `dp(i)` represents the minimum number of coins needed to make the amount `i`.
- **Recurrence:** `dp(i) = min(dp(i - coin) + 1)` for each `coin` in `coins`.
- **Base Case:** `dp(0) = 0` (It takes 0 coins to make an amount of 0). If `i < 0`, it's an invalid path, return infinity.

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

### Top-Down DP (Memoization)

The most intuitive way to solve this is to think recursively. From the target `amount`, we branch out by subtracting each `coin`. We memoize the results to avoid redundant calculations.

```python
def coin_change_memo(coins: list[int], amount: int) -> int:
    """
    Top-down DP (Memoization) for minimum coins.
    
    Time: O(amount * len(coins))
    Space: O(amount) for recursion stack and memo dictionary
    """
    memo = {}

    def dfs(rem_amount: int) -> int:
        # Base cases
        if rem_amount == 0:
            return 0
        if rem_amount < 0:
            return float('inf')
        
        # Check memo
        if rem_amount in memo:
            return memo[rem_amount]
            
        # Recursive step: try all coins
        min_coins = float('inf')
        for coin in coins:
            res = dfs(rem_amount - coin)
            if res != float('inf'):
                min_coins = min(min_coins, res + 1)
                
        # Store and return
        memo[rem_amount] = min_coins
        return memo[rem_amount]

    ans = dfs(amount)
    return ans if ans != float('inf') else -1
```

### Bottom-Up DP (Tabulation)

Converting the top-down approach to bottom-up involves filling an array from `0` to `amount`.

```python
def coin_change(coins: list[int], amount: int) -> int:
    """
    Bottom-up DP (Tabulation) for minimum coins.

    Time: O(amount * len(coins))
    Space: O(amount)
    """
    # Initialize DP array with float('inf')
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed to make amount 0

    # For every amount from 1 to target
    for i in range(1, amount + 1):
        for coin in coins:
            # If the coin can be used for this amount
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
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

- **State:** `dp(i)` represents the number of ways to make the amount `i`.
- **Recurrence:** `dp(i) = sum(dp(i - coin))` for valid coins.
- **Base Case:** `dp(0) = 1`. There is exactly 1 way to make the amount 0 (by selecting no coins). If initialized to 0, all subsequent additions would remain 0.

### Combinations vs Permutations (Loop Order)

To make `3` using `[1, 2]`:
*   **Combinations** (order doesn't matter): `{1, 1, 1}`, `{1, 2}` $\rightarrow$ **2 ways**.
*   **Permutations** (order matters): `(1, 1, 1)`, `(1, 2)`, `(2, 1)` $\rightarrow$ **3 ways**.

How we nest loops determines which one we compute.

### 1. Combinations (Coin Change II)

To count combinations, **process one coin completely before the next**.

#### Top-Down DP (Memoization)

In top-down, we must track which coin we are currently considering to prevent looking "backward" at previous coins, which would create permutations.

```python
def change_combinations_memo(amount: int, coins: list[int]) -> int:
    """
    Top-down DP for Combinations.
    We track `coin_idx` to only use current and subsequent coins.
    """
    memo = {}
    
    def dfs(rem_amount: int, coin_idx: int) -> int:
        if rem_amount == 0:
            return 1
        if rem_amount < 0 or coin_idx == len(coins):
            return 0
            
        if (rem_amount, coin_idx) in memo:
            return memo[(rem_amount, coin_idx)]
            
        # Option 1: Use the current coin (stay at same coin_idx)
        # Option 2: Skip the current coin (move to coin_idx + 1)
        ways = dfs(rem_amount - coins[coin_idx], coin_idx) + \
               dfs(rem_amount, coin_idx + 1)
               
        memo[(rem_amount, coin_idx)] = ways
        return ways
        
    return dfs(amount, 0)
```

#### Bottom-Up DP (Tabulation)

In bottom-up, this translates to iterating through `coins` in the outer loop and `amounts` in the inner loop.

```python
def change_combinations(amount: int, coins: list[int]) -> int:
    """
    Bottom-up DP for Combinations (order doesn't matter).
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

### 2. Permutations (Combination Sum IV)

To count permutations, **build the amount step-by-step using any coin**.

#### Top-Down DP (Memoization)

In top-down, at every step we can choose *any* coin. We don't restrict `coin_idx`.

```python
def change_permutations_memo(amount: int, coins: list[int]) -> int:
    """
    Top-down DP for Permutations.
    At each step, we can pick any coin.
    """
    memo = {}
    
    def dfs(rem_amount: int) -> int:
        if rem_amount == 0:
            return 1
        if rem_amount < 0:
            return 0
            
        if rem_amount in memo:
            return memo[rem_amount]
            
        ways = 0
        for coin in coins:
            ways += dfs(rem_amount - coin)
            
        memo[rem_amount] = ways
        return ways
        
    return dfs(amount)
```

#### Bottom-Up DP (Tabulation)

In bottom-up, this translates to iterating through `amounts` in the outer loop and `coins` in the inner loop.

```python
def change_permutations(amount: int, coins: list[int]) -> int:
    """
    Bottom-up DP for Permutations (order matters).
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
| **Top-Down State** | `dfs(amount, coin_idx)` | `dfs(amount)` |
| **Tabulation Loops** | `coins` outer, `amount` inner | `amount` outer, `coins` inner |
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

    return dp[amount], coins_used
```

---

## Related Pattern: Generating "Coins" Dynamically

Some problems are just Coin Change in disguise, where the "coins" aren't given to you in an array, but are generated dynamically based on the target.

### Perfect Squares

Find the minimum number of perfect square numbers (`1, 4, 9, 16, ...`) that sum to `n`.
*This is exactly Coin Change where the "coins" are perfect squares up to `n`.*

#### Top-Down DP (Memoization)

```python
import math

def num_squares_memo(n: int) -> int:
    """
    Top-down DP for Perfect Squares.
    """
    memo = {}
    
    def dfs(rem: int) -> int:
        if rem == 0:
            return 0
        if rem < 0:
            return float('inf')
            
        if rem in memo:
            return memo[rem]
            
        min_sq = float('inf')
        # Try all perfect squares up to rem
        limit = int(math.sqrt(rem))
        for i in range(1, limit + 1):
            square = i * i
            res = dfs(rem - square)
            if res != float('inf'):
                min_sq = min(min_sq, res + 1)
                
        memo[rem] = min_sq
        return min_sq
        
    return dfs(n)
```

#### Bottom-Up DP (Tabulation)

```python
def num_squares(n: int) -> int:
    """
    Bottom-up DP for Perfect Squares.

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

    return dp[n]
```

---

## Common Pitfalls and Edge Cases

### 1. Initializing the DP Array Incorrectly
For "Minimum Coins" variations, initializing the DP array with `0` is a fatal mistake because `min(0, dp[i - coin] + 1)` will always prefer `0`.
```python
# WRONG (for min problems)
dp = [0] * (amount + 1)

# CORRECT (for min problems - using float('inf'))
dp = [float('inf')] * (amount + 1)
dp[0] = 0
```
Conversely, for "Counting Ways", you must initialize with `0`, but explicitly set `dp[0] = 1`.

### 2. Inner Loop Optimization
Notice in the Combinations bottom-up code, the inner loop starts at `coin`:
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

## Progressive Problems

| Problem | Difficulty | Variant | Key Insight |
| :--- | :--- | :--- | :--- |
| [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | Min Coins | Initialize with `inf`, top-down dfs(rem) |
| [Coin Change II](https://leetcode.com/problems/coin-change-ii/) | Medium | Combinations | `coins` outer loop / `dfs(rem, coin_idx)` |
| [Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/) | Medium | Permutations | `amount` outer loop / `dfs(rem)` |
| [Perfect Squares](https://leetcode.com/problems/perfect-squares/) | Medium | Min Coins | "Coins" are perfect squares generated on the fly |

---

## Key Takeaways

1. **Unbounded Knapsack:** Items (coins) can be reused infinitely.
2. **Top-Down vs Bottom-Up:** Top-down uses recursion and memoization. Bottom-up iterates iteratively. Both are important to understand.
3. **The Combinations vs Permutations Rule:**
   - **Combinations:** Top-down `dfs(rem_amount, coin_idx)`. Bottom-up: `coins` outer loop. Order doesn't matter.
   - **Permutations:** Top-down `dfs(rem_amount)`. Bottom-up: `amounts` outer loop. Order matters.
4. **Initialization Matters:** Use `infinity` (`float('inf')`) for minimum finding problems and `0` for counting problems.
5. **Base Cases:** Making an amount of `0` requires `0` coins (Min Coins) and has `1` way to do it (Count Ways).
