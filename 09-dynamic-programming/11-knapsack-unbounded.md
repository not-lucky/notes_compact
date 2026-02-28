# Unbounded Knapsack

> **Prerequisites:** [10-knapsack-01](./10-knapsack-01.md)

## Overview

Unbounded Knapsack is a variation of the classic 0/1 Knapsack problem. The core difference? **Infinite supply**.

In 0/1 Knapsack, you can either take an item once or leave it. In Unbounded Knapsack, you can pick an item zero, one, or **multiple times**, limited only by the total capacity of the knapsack.

Imagine you're robbing a bank vault. 0/1 Knapsack is when there's exactly one of each item (one diamond, one gold bar, one watch). Unbounded Knapsack is when the vault is a warehouse with giant bins full of identical diamonds, identical gold bars, and identical watches. You can grab as many from a single bin as you want, provided you can carry the weight.

---

## Formal Recurrence

Let $dp[i][w]$ be the maximum value we can achieve using a subset of the first $i$ items, with a knapsack capacity of $w$.

When considering item $i$, we have two choices:
1. **Don't pick it:** The max value is what we could get using the previous $i-1$ items with the same capacity $w$. $\rightarrow dp[i-1][w]$
2. **Pick it (if $wt[i] \leq w$):** The max value is $val[i]$ plus the best value we can get with the *remaining* capacity $w - wt[i]$.

   **Here is the critical difference:** Because we have unlimited items, after picking item $i$, we can pick item $i$ *again*. Therefore, we look at $dp[i][w - wt[i]]$ (current row), NOT $dp[i-1][w - wt[i]]$ (previous row).

$$
dp[i][w] = \max(dp[i-1][w], \ dp[i][w - wt[i]] + val[i])
$$

**Base Cases:**
- $dp[0][w] = 0$: 0 items mean 0 value.
- $dp[i][0] = 0$: 0 capacity means 0 value.

---

## Building Intuition: Forward vs. Backward Iteration

The most elegant part of Unbounded Knapsack is how it translates to a 1D space-optimized array.

In 0/1 Knapsack, we iterate capacity **backward**. Why? To ensure that when we update `dp[w] = max(dp[w], dp[w - wt] + val)`, the value we pull from `dp[w - wt]` represents the state *before* we considered the current item. This prevents us from taking the same item twice.

In Unbounded Knapsack, we want to allow taking the same item multiple times! Therefore, we iterate capacity **forward**.

1. When we calculate `dp[w]`, we look back at `dp[w - wt[i]]`.
2. Because we are iterating forward, `dp[w - wt[i]]` was *already updated* in the current item's loop.
3. If `dp[w - wt[i]]` already includes item $i$, our update `dp[w - wt[i]] + val[i]` means we are effectively taking item $i$ *again*. This perfectly models infinite supply.

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
- Try two weight-4 items: 2 * 50 = 100
- Try eight weight-1 items: 8 * 10 = 80
- Try one weight-3 + one weight-5: 40 + 70 = 110 (Optimal)
```

---

## Implementations

### 1. Top-Down (Memoization)

The top-down approach is straightforward. Notice that the state only needs the remaining capacity `w`. We don't need to track the "current item index" because every recursive call has access to *all* items again.

```python
def unbounded_knapsack_memo(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Top-Down DP (Memoization)
    Time: O(n * W), where n is number of items, W is capacity
    Space: O(W) for the memoization dictionary and recursion stack
    """
    memo = {}

    def dfs(rem_cap: int) -> int:
        if rem_cap == 0:
            return 0
        if rem_cap in memo:
            return memo[rem_cap]

        max_val = 0

        # Try taking EVERY possible item for the remaining capacity
        for i in range(len(weights)):
            if weights[i] <= rem_cap:
                # Add item value, and recurse with remaining capacity
                # We can pick 'i' again because the loop in the child call
                # will again consider all items [0...n-1]
                max_val = max(max_val, values[i] + dfs(rem_cap - weights[i]))

        memo[rem_cap] = max_val
        return max_val

    return dfs(capacity)
```

### 2. Tabulation (2D Array)

Building the full 2D table helps visualize the formal recurrence. We use $dp[i][w]$ to mean the max value using the first $i$ items with capacity $w$.

```python
def unbounded_knapsack_2d(weights: list[int], values: list[int], capacity: int) -> int:
    """
    2D Bottom-Up DP
    Time: O(n * W)
    Space: O(n * W)
    """
    n = len(weights)
    # dp[i][w] = max value using first i items (1-indexed) with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wt = weights[i - 1]
        val = values[i - 1]

        for w in range(1, capacity + 1):
            if wt <= w:
                # CRITICAL: Notice dp[i][w - wt], not dp[i-1][w - wt]
                # We stay on the same row 'i' to allow reusing the item.
                dp[i][w] = max(dp[i - 1][w], dp[i][w - wt] + val)
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]
```

### 3. Tabulation (1D Space-Optimized - Best Practice)

We only ever need the current row `i` and the previous row `i-1`. In fact, because the Unbounded Knapsack recurrence requires looking at *earlier* computed values in the *current* row (`dp[i][w - wt]`), we can collapse this into a single 1D array by iterating capacity **forward**.

```python
def unbounded_knapsack_1d(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Space-Optimized 1D Bottom-Up DP
    Time: O(n * W)
    Space: O(W)
    """
    # dp[w] = max value achievable with capacity w
    dp = [0] * (capacity + 1)

    # For each item...
    for i in range(len(weights)):
        wt = weights[i]
        val = values[i]

        # Iterate FORWARD through capacity!
        # We start at 'wt' because we can't fit the item in a smaller capacity.
        for w in range(wt, capacity + 1):
            # dp[w - wt] might already include the current item 'i',
            # allowing us to pick it multiple times.
            dp[w] = max(dp[w], dp[w - wt] + val)

    return dp[capacity]
```

### 4. Alternative 1D (Loops Swapped)

For pure optimization problems (finding the max/min value), the loop order doesn't matter. You can put the capacity loop on the outside. Conceptually, this matches the top-down memoization approach: "For this specific capacity $w$, let me try adding every possible item."

```python
def unbounded_knapsack_swapped(weights: list[int], values: list[int], capacity: int) -> int:
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

Let's trace the 1D Space-Optimized approach.
`weights = [2, 3]`, `values = [15, 20]`, `capacity = 6`.

Array `dp` initialized to `[0, 0, 0, 0, 0, 0, 0]`.

**Processing Item 0 (wt=2, val=15):** Iterate `w` from 2 to 6.
- `w=2`: `dp[2] = max(0, dp[0] + 15) = 15` (Take one 2kg item)
- `w=3`: `dp[3] = max(0, dp[1] + 15) = 15` (Take one 2kg item)
- `w=4`: `dp[4] = max(0, dp[2] + 15) = max(0, 15 + 15) = 30` **(Reused! Took two 2kg items)**
- `w=5`: `dp[5] = max(0, dp[3] + 15) = max(0, 15 + 15) = 30` (Took two 2kg items)
- `w=6`: `dp[6] = max(0, dp[4] + 15) = max(0, 30 + 15) = 45` **(Reused! Took three 2kg items)**

Current `dp` array: `[0, 0, 15, 15, 30, 30, 45]`

**Processing Item 1 (wt=3, val=20):** Iterate `w` from 3 to 6.
- `w=3`: `dp[3] = max(15, dp[0] + 20) = 20` (Replace 2kg with 3kg)
- `w=4`: `dp[4] = max(30, dp[1] + 20) = 30` (Keep two 2kg items)
- `w=5`: `dp[5] = max(30, dp[2] + 20) = max(30, 15 + 20) = 35` (Take one 2kg + one 3kg)
- `w=6`: `dp[6] = max(45, dp[3] + 20) = max(45, 20 + 20) = 45` (Three 2kg items [45] is better than two 3kg items [40])

Final `dp` array: `[0, 0, 15, 20, 30, 35, 45]`
Answer: `45`

---

## When NOT to Use Unbounded Knapsack

1. **Limited Item Quantities:** If you have exactly $K$ copies of an item, it's a **Bounded Knapsack** problem. Treat it as 0/1 Knapsack by "flattening" the items (e.g., three 5¢ coins become three separate 5¢ items).
2. **Single Use Required:** Use 0/1 Knapsack (backward capacity iteration).
3. **Very Large Capacity ($W > 10^7$):** DP becomes $O(n \times W)$, causing TLE (Time Limit Exceeded) and MLE (Memory Limit Exceeded). Use a Greedy approach, often combined with a small DP for the modulo remainder.
4. **Sequence/Order Matters:** If you need to find a specific valid sequence (like valid parentheses), DP on states or Interval DP is required, not knapsack.
5. **Negative Weights/Cycles:** Taking an item would *increase* your capacity, creating infinite loops. Knapsack DP requires weights $\geq 0$.

---

## Related Patterns: The Counting Variations

While Unbounded Knapsack is an optimization problem (finding the `max` value), the **forward-iteration structure** is heavily used in *counting* problems (finding the `sum` of ways).

**CRITICAL WARNING:** For counting problems, the loop order (Items Outer vs. Capacity Outer) completely changes what you are counting!

### 1. Coin Change II (Count Combinations)
*Problem: Given unlimited coins, count the ways to make an amount. Order does NOT matter. ($1+2$ is the same as $2+1$)*

**Rule: Items MUST be the outer loop.**
By locking the coin in the outer loop, you process all 1s, then all 2s. You can never go back to 1s after using a 2. Thus, you only generate combinations like `1+1+2`, preventing duplicates like `1+2+1`.

```python
def change(amount: int, coins: list[int]) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1  # 1 way to make 0: use no coins

    # Outer loop = Items -> Combinations
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]

    return dp[amount]
```

### 2. Combination Sum IV (Count Permutations)
*Problem: Given unlimited numbers, count the ways to make a target. Order DOES matter. ($1+2$ is different from $2+1$)*

**Rule: Capacity MUST be the outer loop.**
By locking the capacity in the outer loop, you try *every* item for a given capacity. To reach `capacity = 3`, you try adding `1` (from state 2) and adding `2` (from state 1). This allows generating both `1+2` and `2+1` as distinct paths.

```python
def combinationSum4(nums: list[int], target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1

    # Outer loop = Capacity -> Permutations
    for a in range(1, target + 1):
        for num in nums:
            if num <= a:
                dp[a] += dp[a - num]

    return dp[target]
```

### 3. Coin Change (Min Elements)
*Problem: Find the minimum number of coins to make an amount.*

Since this is an optimization problem (min) and not a counting problem (sum), **loop order doesn't matter**. Either items outer or capacity outer will work.

```python
def coin_change(coins: list[int], amount: int) -> int:
    # Initialize with infinity, since we want the minimum
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    # Outer or inner loop works here
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

---

## 0/1 vs Unbounded Recap

| Aspect | 0/1 Knapsack | Unbounded Knapsack |
| :--- | :--- | :--- |
| **Item usage** | At most once | Unlimited |
| **2D Recurrence** | `dp[i-1][w - wt] + val` | `dp[i][w - wt] + val` |
| **1D DP Update** | `dp[w] = max(dp[w], dp[w - wt] + val)` | `dp[w] = max(dp[w], dp[w - wt] + val)` |
| **1D Iteration** | **Backward** (`W` down to `wt`) | **Forward** (`wt` up to `W`) |
| **Counting Loop Order** | Combinations only | Combinations (Item outer) OR Permutations (Cap outer) |

*Mnemonic: If you accidentally iterate Unbounded backward, you solve 0/1. If you accidentally iterate 0/1 forward, you solve Unbounded.*
