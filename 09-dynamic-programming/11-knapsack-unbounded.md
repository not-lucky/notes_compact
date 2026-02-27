# Unbounded Knapsack

> **Prerequisites:** [10-knapsack-01](./10-knapsack-01.md)

## Overview

Unbounded Knapsack is a variation of the classic knapsack problem where we have an **infinite supply** of each item. In the 0/1 Knapsack problem, each item can be selected at most once. In the Unbounded Knapsack problem, each item can be selected zero, one, or multiple times, as long as the total weight does not exceed the knapsack capacity.

## Formal Recurrence

Let $dp[w]$ be the maximum value we can achieve with a total weight limit of $w$.

Since we have an unlimited supply of items, for a given capacity $w$, we can try adding *any* item $i$. If we pick item $i$, the total value is $val[i]$ plus the best value we can get with the *remaining* capacity $w - wt[i]$. Because we can reuse item $i$, the subproblem for the remaining capacity can also consider item $i$.

$$
dp[w] = \max_{i \text{ where } wt[i] \leq w} (dp[w], dp[w - wt[i]] + val[i])
$$

**Base Case:**
- $dp[0] = 0$ (A knapsack with 0 capacity can hold 0 value)

Alternatively, expressed as a 2D relation $dp[i][w]$ (maximum value using a subset of the first $i$ items, with capacity $w$):
$$
dp[i][w] = \max(dp[i-1][w], \ dp[i][w - wt[i]] + val[i])
$$
*Notice the second term uses $dp[i]$ instead of $dp[i-1]$. This reflects that after picking item $i$, we can still pick item $i$ again for the remaining capacity $w - wt[i]$.*

## Building Intuition

**Why does forward iteration allow reuse?**

1. **The Key Difference**: In the 1D space-optimized 0/1 knapsack, we iterate capacity **backward**. This ensures that when computing `dp[w]`, the value `dp[w - wt[i]]` represents the state from the *previous* item (i.e., "before considering item $i$"). Forward iteration means `dp[w - wt[i]]` may *already* include item $i$—allowing reuse.
2. **Why This Works**: For unbounded knapsack, we *want* to reuse items. When computing the max value for capacity 10 (`dp[10]`) considering a coin of weight 3, we look at `dp[7]`. If `dp[7]` already optimally used that coin twice, that's exactly what we want! We can use it a third time by doing `dp[7] + val`.
3. **Iteration Order Matters**:
   - **Backward (0/1)**: Evaluates larger capacities before smaller ones. Uses previous-row values $\rightarrow$ item appears at most once $\rightarrow$ CORRECT for 0/1.
   - **Forward (Unbounded)**: Evaluates smaller capacities before larger ones. Uses current-row values $\rightarrow$ item can appear multiple times $\rightarrow$ CORRECT for unbounded.
4. **Combinations vs. Permutations (Order Matters for Counting)**:
   - When counting ways (not just finding max/min), the loop order dictates what you count.
   - **Items outer, capacity inner** $\rightarrow$ combinations (e.g., coin $1+2$ is considered the same as $2+1$, counted only once).
   - **Capacity outer, items inner** $\rightarrow$ permutations (e.g., $1+2$ and $2+1$ are counted as separate sequences).
5. **Mental Model**: Imagine a vending machine with infinite stock. When trying to fill capacity $W$, you can pick any item that fits, subtract its weight, and immediately be faced with the exact same choices for the remaining capacity.

## When NOT to Use Unbounded Knapsack

1. **Limited Item Quantities**: If each item has a specific maximum count (e.g., "you have exactly three 5¢ coins"), use Bounded Knapsack or split the items into multiple "virtual" items (which reduces it to 0/1 Knapsack).
2. **Single Use Required**: If items can only be used once, use 0/1 Knapsack (backward iteration).
3. **Very Large Capacity**: If $W = 10^9$, $O(n \times W)$ DP is too slow and takes too much memory. If item values are proportional to weights, or if you can take an enormous amount of the most efficient item, use a Greedy approach (often with a small DP for the remainder).
4. **Order-Dependent Sequence Construction**: If the actual sequence of items matters for validity (not just for counting permutations), like finding the longest valid parentheses sequence, this requires a different DP approach (often interval DP).
5. **Negative Weights**: Unbounded knapsack with negative weights can lead to infinite loops (taking an item increases capacity). Ensure all weights are non-negative.

---

## Problem Statement

Given weights and values of $n$ items with an unlimited supply of each, find the maximum value that fits in a knapsack of capacity $W$.

```text
Input:
  weights = [1, 3, 4, 5]
  values = [10, 40, 50, 70]
  capacity = 8

Output: 110
Explanation:
- We could take two weight-4 items: 2 * 50 = 100
- Better: take one weight-3 + one weight-5: 40 + 70 = 110 ✓
- Even better? eight weight-1 items: 8 * 10 = 80 (not optimal)
```

---

## Implementations

### 1. Top-Down (Memoization)

```python
def unbounded_knapsack_memo(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Top-Down DP (Memoization)
    Time: O(n * W)
    Space: O(W) for memo + call stack
    """
    memo = {}

    def dfs(w: int) -> int:
        if w == 0:
            return 0
        if w in memo:
            return memo[w]

        max_val = 0
        # Try taking each item
        for i in range(len(weights)):
            if weights[i] <= w:
                # Add item value, and recurse with remaining capacity
                # Because we don't track 'i' in the state, we can pick 'i' again
                max_val = max(max_val, values[i] + dfs(w - weights[i]))

        memo[w] = max_val
        return max_val

    return dfs(capacity)
```

### 2. Space-Optimized 1D (Best Practice)

Notice we don't even need a 2D table. We just iterate capacities forward. This is the standard, most efficient way to write Unbounded Knapsack.

```python
def unbounded_knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Unbounded knapsack - items can be used unlimited times.
    Time: O(n * W)
    Space: O(W)
    """
    dp = [0] * (capacity + 1)

    # For each item...
    for i in range(len(weights)):
        wt = weights[i]
        val = values[i]
        # Iterate FORWARD through capacity!
        for w in range(wt, capacity + 1):
            dp[w] = max(dp[w], dp[w - wt] + val)

    return dp[capacity]
```

### 3. Alternative 1D: Capacity Outer Loop

For pure optimization problems (finding the max/min value), the loop order doesn't matter. You can put the capacity loop on the outside.

```python
def unbounded_knapsack_alt(weights: list[int], values: list[int], capacity: int) -> int:
    dp = [0] * (capacity + 1)

    # For each capacity...
    for w in range(1, capacity + 1):
        # Try every item
        for i in range(len(weights)):
            if weights[i] <= w:
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]
```

---

## DP Table Visualization

`weights = [2, 3]`, `values = [15, 20]`, `capacity = 6`:

| Item \ Cap | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0** (0,0) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **1** (2,15)| 0 | 0 | 15| 15| 30| 30| 45|
| **2** (3,20)| 0 | 0 | 15| 20| 30| 35| 45|

*Walkthrough of `dp[4]` at row 1:*
`dp[4] = max(dp_prev[4], dp[4 - wt[1]] + val[1])`
`dp[4] = max(0, dp[2] + 15)`
`dp[4] = max(0, 15 + 15) = 30` *(Used item 1 twice!)*

*Walkthrough of `dp[6]` at row 2:*
`dp[6] = max(dp_prev[6], dp[6 - wt[2]] + val[2])`
`dp[6] = max(45, dp[3] + 20)`
`dp[6] = max(45, 20 + 20) = 45` *(Keeping three item 1s is better than two item 2s)*

---

## Related Patterns

### Coin Change (Min Coins)
Given a target amount and unlimited coins, find the minimum number of coins needed.
```python
def coin_change(coins: list[int], amount: int) -> int:
    # Initialize with infinity, since we want the minimum
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins: # Outer or inner loop works for MIN/MAX
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

### Coin Change II (Count Ways - Combinations)
Given a target amount and unlimited coins, count the number of combinations that make up that amount.
**CRITICAL**: Items MUST be the outer loop to prevent duplicate counting of permutations (where `1+2` is considered the same as `2+1`).
```python
def change(amount: int, coins: list[int]) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1 # 1 way to make 0 (use 0 coins)

    for coin in coins:  # Coin MUST be outer loop for combinations
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]

    return dp[amount]
```

### Combination Sum IV (Count Ways - Permutations)
Given a target amount and unlimited items, count the number of permutations (`1+2` $\neq$ `2+1`).
**CRITICAL**: Capacity MUST be the outer loop.
```python
def combinationSum4(nums: list[int], target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1

    for a in range(1, target + 1): # Capacity MUST be outer loop for permutations
        for num in nums:
            if num <= a:
                dp[a] += dp[a - num]

    return dp[target]
```

### Perfect Squares (Min elements)
Find the minimum number of perfect squares that sum to $n$.
Items are implicitly squares `1, 4, 9, 16...`. Capacity is $n$.
```python
def num_squares(n: int) -> int:
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    # Here, capacity is outer loop, items are inner loop
    for i in range(1, n + 1): # Capacity
        j = 1
        while j * j <= i:     # Items (perfect squares)
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1

    return dp[n]
```

---

## 0/1 vs Unbounded Recap

| Aspect | 0/1 Knapsack | Unbounded Knapsack |
| :--- | :--- | :--- |
| **Item usage** | At most once | Unlimited |
| **1D DP Update** | `dp[w] = max(dp[w], dp[w - wt] + val)` | `dp[w] = max(dp[w], dp[w - wt] + val)` |
| **1D Iteration** | **Backward** (`W` down to `wt`) | **Forward** (`wt` up to `W`) |
| **Count Ways** | Combinations only | Combinations (Item outer) OR Permutations (Cap outer) |
| **Common Problem** | Subset Sum, Partition Equal Subset Sum | Coin Change, Integer Break |

*Mnemonic: If you accidentally iterate Unbounded backward, you solve 0/1. If you accidentally iterate 0/1 forward, you solve Unbounded.*
