# Unbounded Knapsack

> **Prerequisites:** [10-knapsack-01](./10-knapsack-01.md)

## Overview

Unbounded Knapsack allows each item to be used multiple times (unlike 0/1 where each is used at most once).

## Formal Recurrence

Let $dp[w]$ be the maximum value we can achieve with a total weight limit of $w$.

Since we have an unlimited supply of items, for a given capacity $w$, we can try adding *any* item $i$. If we pick item $i$, the value is $val[i]$ plus the best value we can get with the *remaining* capacity $w - wt[i]$.

$$
dp[w] = \max_{i \text{ where } wt[i] \leq w} (dp[w], dp[w - wt[i]] + val[i])
$$

**Base Case:**
- $dp[0] = 0$ (0 value with 0 capacity)

Alternatively, expressed as a 2D relation $dp[i][w]$ (using first $i$ items, capacity $w$):
$$
dp[i][w] = \max(dp[i-1][w], dp[i][w - wt[i]] + val[i])
$$
*Notice the second term uses $dp[i]$ instead of $dp[i-1]$, reflecting that we can pick item $i$ again.*

## Building Intuition

**Why does forward iteration allow reuse?**

1. **The Key Difference**: In 0/1 knapsack, backward iteration ensures `dp[w - wt[i]]` reflects the state "before considering item $i$." Forward iteration means `dp[w - wt[i]]` may already include item $i$—allowing reuse.
2. **Why This Works**: For unbounded, we WANT to reuse items. When computing `dp[10]` with a coin of 3, if `dp[7]` already optimally used that coin twice, great! We can use it a third time by doing `dp[7] + val`.
3. **Iteration Order Matters**:
   - Backward (0/1): Uses previous-row values $\rightarrow$ item appears at most once $\rightarrow$ CORRECT for 0/1.
   - Forward (Unbounded): Uses current-row values $\rightarrow$ item can appear multiple times $\rightarrow$ CORRECT for unbounded.
4. **Combinations vs Permutations (Order Matters for Counting)**:
   - Items outer, capacity inner $\rightarrow$ combinations (coin 1+2 is same as 2+1, counted once).
   - Capacity outer, items inner $\rightarrow$ permutations (1+2 and 2+1 counted separately).
5. **Mental Model**: Imagine a vending machine with infinite stock. When filling capacity $W$, you can pick any item that fits and immediately consider the same item again for the remaining capacity.

## When NOT to Use Unbounded Knapsack

1. **Limited Item Quantities**: If each item has a specific maximum count (e.g., "you have three 5¢ coins"), use Bounded Knapsack or split into multiple "virtual" items (0/1 Knapsack).
2. **Single Use Required**: If items can only be used once, use 0/1 Knapsack (backward iteration).
3. **Very Large Capacity**: If $W = 10^9$, $O(n \times W)$ is infeasible. If item values are proportional to weights, use Greedy.
4. **Order-Dependent Sequence Construction**: If the sequence of items matters (not just combinations), like finding the longest valid parentheses sequence, this is a different problem class.
5. **Negative Values**: Unbounded with negative values and weights can lead to infinite loops. Ensure all weights are positive.

---

## Problem Statement

Given weights and values of $n$ items with unlimited supply, find maximum value that fits in capacity $W$.

```
Input:
  weights = [1, 3, 4, 5]
  values = [10, 40, 50, 70]
  capacity = 8

Output: 110
Explanation:
- Two weight-4 items: 2 * 50 = 100
- weight-3 + weight-5 = 40 + 70 = 110 ✓
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
                max_val = max(max_val, values[i] + dfs(w - weights[i]))

        memo[w] = max_val
        return max_val

    return dfs(capacity)
```

### 2. Space-Optimized 1D (Best Practice)

Notice we don't even need a 2D table. We just iterate capacities forward.

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

For pure optimization (max/min), the loop order doesn't matter.

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

*Notice at row 1, cap 4: `dp[4] = max(dp_prev[4], dp[4-2] + 15) = dp[2] + 15 = 15 + 15 = 30` (Used item 1 twice!)*

---

## Related Patterns

### Coin Change (Min Coins)
Target amount, unlimited coins. Objective: Min count.
```python
def coin_change(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins: # Outer or inner loop works for MIN/MAX
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

### Coin Change II (Count Ways - Combinations)
Target amount, unlimited coins. Objective: Count combinations.
**CRITICAL**: Items MUST be the outer loop to prevent duplicate counting of permutations (like `1+2` and `2+1`).
```python
def change(amount: int, coins: list[int]) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1 # 1 way to make 0

    for coin in coins:  # Coin MUST be outer loop for combinations
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]

    return dp[amount]
```

### Combination Sum IV (Count Ways - Permutations)
Target amount, unlimited items. Objective: Count permutations (`1+2` $\neq$ `2+1`).
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
Find min perfect squares summing to $n$.
Items are implicitly squares `1, 4, 9, 16...`. Capacity is $n$.
```python
def num_squares(n: int) -> int:
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1): # Capacity
        j = 1
        while j * j <= i:     # Items
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1

    return dp[n]
```

---

## 0/1 vs Unbounded Recap

| Aspect | 0/1 Knapsack | Unbounded Knapsack |
| :--- | :--- | :--- |
| **Item usage** | At most once | Unlimited |
| **1D Iteration** | Backward | Forward |
| **Count Ways** | Combinations only | Combinations (Item outer) OR Permutations (Cap outer) |
| **Common Problem** | Subset Sum | Coin Change |

*If you accidentally iterate Unbounded backward, you solve 0/1. If you accidentally iterate 0/1 forward, you solve Unbounded.*