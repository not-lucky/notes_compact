# Unbounded Knapsack

> **Prerequisites:** [10-knapsack-01](./10-knapsack-01.md)

## Overview

Unbounded Knapsack is identical to 0/1 Knapsack, except for one rule: **Infinite supply**. You can pick an item zero, one, or multiple times.

---

## Formal Recurrence

Let $dp[i][w]$ be the maximum value we can achieve using a subset of the first $i$ items, with a knapsack capacity of $w$.

When considering item $i$, we have two choices:
1. **Don't pick it:** The max value is what we could get using the previous $i-1$ items with the same capacity $w$. $\rightarrow dp[i-1][w]$
2. **Pick it (if $weight[i] \leq w$):** The max value is $value[i]$ plus the best value we can get with the *remaining* capacity $w - weight[i]$.

   **Here is the critical difference:** Because we have unlimited items, after picking item $i$, we can pick item $i$ *again*. Therefore, we look at $dp[i][w - weight[i]]$ (current row), NOT $dp[i-1][w - weight[i]]$ (previous row).

$$
dp[i][w] = \max(dp[i-1][w], \ dp[i][w - weight[i]] + value[i])
$$

**Base Cases:**
- $dp[0][w] = 0$: 0 items mean 0 value.
- $dp[i][0] = 0$: 0 capacity means 0 value.

---

## Building Intuition: Forward Iteration

The core difference lies in the 1D space-optimized implementation.
In 0/1 Knapsack, we iterate capacity **backward** to prevent reusing the same item.
In Unbounded Knapsack, we iterate capacity **forward**.

Why forward? Because when we calculate `dp[w]`, we look back at `dp[w - weight]`. If we iterate forward, `dp[w - weight]` was *already updated* during the current item's loop. By building on that updated value, we are effectively adding the same item multiple times.

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
    Time: O(n \cdot w), where n is number of items, W is capacity
    Space: O(w) for the memoization dictionary and recursion stack
    """
    memo = {}

    def dfs(rem_w: int) -> int:
        if rem_w == 0:
            return 0
        if rem_w in memo:
            return memo[rem_w]

        max_value = 0

        # Try taking EVERY possible item for the remaining capacity
        for i in range(len(weights)):
            if weights[i] <= rem_w:
                # Add item value, and recurse with remaining capacity
                # We can pick 'i' again because the loop in the child call
                # will again consider all items [0...n-1]
                max_value = max(max_value, values[i] + dfs(rem_w - weights[i]))

        memo[rem_w] = max_value
        return max_value

    return dfs(capacity)
```

### 2. Tabulation (2D Array)

Building the full 2D table helps visualize the formal recurrence. We use $dp[i][w]$ to mean the max value using the first $i$ items with capacity $w$.

```python
def unbounded_knapsack_2d(weights: list[int], values: list[int], capacity: int) -> int:
    """
    2D Bottom-Up DP
    Time: O(n \cdot w)
    Space: O(n \cdot w)
    """
    n = len(weights)
    # dp[i][w] = max value using first i items (1-indexed) with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = weights[i - 1]
        value = values[i - 1]

        for w in range(1, capacity + 1):
            if weight <= w:
                # CRITICAL: Notice dp[i][w - weight], not dp[i-1][w - weight]
                # We stay on the same row 'i' to allow reusing the item.
                dp[i][w] = max(dp[i - 1][w], dp[i][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]
```

### 3. Tabulation (1D Space-Optimized - Best Practice)

We only ever need the current row `i` and the previous row `i-1`. In fact, because the Unbounded Knapsack recurrence requires looking at *earlier* computed values in the *current* row (`dp[i][w - weight]`), we can collapse this into a single 1D array by iterating capacity **forward**.

```python
def unbounded_knapsack_1d(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Space-Optimized 1D Bottom-Up DP
    Time: O(n \cdot w)
    Space: O(w)
    """
    # dp[w] = max value achievable with capacity w
    dp = [0] * (capacity + 1)

    # For each item...
    for i in range(len(weights)):
        weight = weights[i]
        value = values[i]

        # Iterate FORWARD through capacity!
        # We start at 'weight' because we can't fit the item in a smaller capacity.
        for w in range(weight, capacity + 1):
            # dp[w - weight] might already include the current item 'i',
            # allowing us to pick it multiple times.
            dp[w] = max(dp[w], dp[w - weight] + value)

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
            weight = weights[i]
            value = values[i]
            if weight <= w:
                dp[w] = max(dp[w], dp[w - weight] + value)

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
3. **Very Large Capacity ($W > 10^7$):** DP becomes $O(n \times w)$, causing TLE (Time Limit Exceeded) and MLE (Memory Limit Exceeded). Use a Greedy approach, often combined with a small DP for the modulo remainder.
4. **Sequence/Order Matters:** If you need to find a specific valid sequence (like valid parentheses), DP on states or Interval DP is required, not knapsack.
5. **Negative Weights/Cycles:** Taking an item would *increase* your capacity, creating infinite loops. Knapsack DP requires weights $\geq 0$.

---

## Progressive Problems

While Unbounded Knapsack is an optimization problem (finding the `max` value), the **forward-iteration structure** is heavily used in *counting* problems (finding the `sum` of ways) and other optimization variants.

Here are the progressive problems to solidify your understanding. For each, we provide both the **Top-Down (Memoization)** and **Bottom-Up (Tabulation)** approaches.

### 1. Rod Cutting (Classic Unbounded Knapsack)
*Problem: Given a rod of length $n$ and an array of prices for different lengths, find the maximum revenue by cutting the rod and selling the pieces. You can cut the rod into as many pieces as you want.*

This is the exact same problem as Unbounded Knapsack, where `weights` are the piece lengths, `values` are the piece prices, and `capacity` is the total rod length.

<details>
<summary>Implementation</summary>

```python
def cut_rod_memo(prices: list[int], n: int) -> int:
    memo = {}
    def dfs(rem_len: int) -> int:
        if rem_len == 0:
            return 0
        if rem_len in memo:
            return memo[rem_len]

        max_val = 0
        # Try cutting a piece of length i+1
        for i in range(len(prices)):
            length = i + 1
            if length <= rem_len:
                max_val = max(max_val, prices[i] + dfs(rem_len - length))

        memo[rem_len] = max_val
        return max_val

    return dfs(n)

def cut_rod_dp(prices: list[int], n: int) -> int:
    dp = [0] * (n + 1)
    for i in range(len(prices)):
        length = i + 1
        for w in range(length, n + 1):
            dp[w] = max(dp[w], dp[w - length] + prices[i])
    return dp[n]
```
</details>

### 2. Coin Change (Min Elements)
*Problem: Find the minimum number of coins to make a given amount. (LeetCode 322)*

Since this is an optimization problem (min) and not a counting problem (sum), **loop order doesn't matter** for Tabulation. Either items outer or capacity outer will work.

<details>
<summary>Implementation</summary>

```python
def coin_change_memo(coins: list[int], amount: int) -> int:
    memo = {}
    def dfs(rem: int) -> int:
        if rem == 0:
            return 0
        if rem < 0:
            return float('inf')
        if rem in memo:
            return memo[rem]

        min_coins = float('inf')
        for coin in coins:
            res = dfs(rem - coin)
            if res != float('inf'):
                min_coins = min(min_coins, res + 1)

        memo[rem] = min_coins
        return min_coins

    ans = dfs(amount)
    return ans if ans != float('inf') else -1

def coin_change_dp(coins: list[int], amount: int) -> int:
    # Initialize with infinity, since we want the minimum
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    # Outer or inner loop works here
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```
</details>

### 3. Coin Change II (Count Combinations)
*Problem: Given unlimited coins, count the ways to make an amount. Order does NOT matter. ($1+2$ is the same as $2+1$). (LeetCode 518)*

**Rule: For Combinations, Items MUST be the outer loop.**
By locking the coin in the outer loop, you process all 1s, then all 2s. You can never go back to 1s after using a 2. Thus, you only generate combinations like `1+1+2`, preventing duplicates like `1+2+1`.
For Top-Down, this means we must track the `index` of the current coin to avoid going backwards in our choices.

<details>
<summary>Implementation</summary>

```python
def change_memo(amount: int, coins: list[int]) -> int:
    memo = {}
    def dfs(i: int, rem: int) -> int:
        if rem == 0:
            return 1
        if rem < 0 or i == len(coins):
            return 0
        if (i, rem) in memo:
            return memo[(i, rem)]

        # 2 choices: skip the coin, or use the coin (and stay at same index)
        res = dfs(i + 1, rem) + dfs(i, rem - coins[i])

        memo[(i, rem)] = res
        return res

    return dfs(0, amount)

def change_dp(amount: int, coins: list[int]) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1  # 1 way to make 0: use no coins

    # Outer loop = Items -> Combinations
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]

    return dp[amount]
```
</details>

### 4. Combination Sum IV (Count Permutations)
*Problem: Given unlimited numbers, count the ways to make a target. Order DOES matter. ($1+2$ is different from $2+1$). (LeetCode 377)*

**Rule: For Permutations, Capacity MUST be the outer loop.**
By locking the capacity in the outer loop, you try *every* item for a given capacity. To reach `capacity = 3`, you try adding `1` (from state 2) and adding `2` (from state 1). This allows generating both `1+2` and `2+1` as distinct paths.
For Top-Down, this means we don't need to track an `index` - we can try every number from the beginning for every remaining amount.

<details>
<summary>Implementation</summary>

```python
def combination_sum_4_memo(nums: list[int], target: int) -> int:
    memo = {}
    def dfs(rem: int) -> int:
        if rem == 0:
            return 1
        if rem < 0:
            return 0
        if rem in memo:
            return memo[rem]

        ways = 0
        # Try EVERY number again for permutations
        for num in nums:
            ways += dfs(rem - num)

        memo[rem] = ways
        return ways

    return dfs(target)

def combination_sum_4_dp(nums: list[int], target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1

    # Outer loop = Capacity -> Permutations
    for a in range(1, target + 1):
        for num in nums:
            if num <= a:
                dp[a] += dp[a - num]

    return dp[target]
```
</details>

### 5. Perfect Squares
*Problem: Find the least number of perfect square numbers that sum to $n$. (LeetCode 279)*

This is exactly like Coin Change (Min Elements), but the "coins" (items) are generated dynamically (1, 4, 9, 16...).

<details>
<summary>Implementation</summary>

```python
def num_squares_memo(n: int) -> int:
    memo = {}
    def dfs(rem: int) -> int:
        if rem == 0:
            return 0
        if rem < 0:
            return float('inf')
        if rem in memo:
            return memo[rem]

        min_sq = float('inf')
        i = 1
        # Dynamically generate "items"
        while i * i <= rem:
            res = dfs(rem - i * i)
            if res != float('inf'):
                min_sq = min(min_sq, res + 1)
            i += 1

        memo[rem] = min_sq
        return min_sq

    return dfs(n)

def num_squares_dp(n: int) -> int:
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1

    return dp[n]
```
</details>

---

## 0/1 vs Unbounded Recap

| Aspect | 0/1 Knapsack | Unbounded Knapsack |
| :--- | :--- | :--- |
| **Item usage** | At most once | Unlimited |
| **2D Recurrence** | `dp[i-1][w - weight] + value` | `dp[i][w - weight] + value` |
| **1D DP Update** | `dp[w] = max(dp[w], dp[w - weight] + value)` | `dp[w] = max(dp[w], dp[w - weight] + value)` |
| **1D Iteration** | **Backward** (`w` down to `weight`) | **Forward** (`weight` up to `w`) |
| **Counting Loop Order** | Combinations only | Combinations (Item outer) OR Permutations (Cap outer) |

*Mnemonic: If you accidentally iterate Unbounded backward, you solve 0/1. If you accidentally iterate 0/1 forward, you solve Unbounded.*
