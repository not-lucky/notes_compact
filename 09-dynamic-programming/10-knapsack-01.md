# 0/1 Knapsack

> **Prerequisites:** [07-2d-dp-basics](./07-2d-dp-basics.md)

## Overview

0/1 Knapsack is a fundamental optimization problem where you select items (each usable at most once) to maximize value while staying within a weight capacity.

## Formal Recurrence

Let $dp[i][w]$ be the maximum value we can achieve using a subset of the first $i$ items with a total weight limit of $w$.

For item $i$ (with weight $wt[i]$ and value $val[i]$), we have two choices:
1. **Exclude it:** The max value is what we could get with the first $i-1$ items.
   $dp[i][w] = dp[i-1][w]$
2. **Include it:** If $wt[i] \leq w$, we gain $val[i]$ but use $wt[i]$ capacity. We add this to the best we could do with the remaining capacity using the first $i-1$ items.
   $dp[i][w] = dp[i-1][w - wt[i]] + val[i]$

Combining these:
$$
dp[i][w] =
\begin{cases}
dp[i-1][w] & \text{if } wt[i] > w \\
\max(dp[i-1][w], dp[i-1][w - wt[i]] + val[i]) & \text{if } wt[i] \leq w
\end{cases}
$$

**Base Cases:**
- $dp[0][w] = 0$ for all $w$ (0 value with 0 items)
- $dp[i][0] = 0$ for all $i$ (0 value with 0 capacity)

## Building Intuition

**Why is 0/1 Knapsack solved with DP?**

1. **Exponential Choices, Polynomial States**: With $n$ items, there are $2^n$ possible subsets. But the answer only depends on (current item index, remaining capacity)—just $n \times W$ states.

2. **The Include/Exclude Decision**: At each step we make a binary choice. By taking the `max()` of both valid choices, we explore all $2^n$ possibilities efficiently without redundant work.

3. **Pseudo-Polynomial Complexity**: $O(n \times W)$ looks polynomial, but $W$ is a VALUE (number of possible weights), not the INPUT SIZE (which takes $\log W$ bits to represent). If $W = 10^9$, this approach is infeasible.

4. **Mental Model**: Imagine packing a backpack before a hike. You consider items one by one. For each item, you ask: "If I take this, is the value gained worth the capacity I lose?" You decide based on the optimal packing of the *remaining* capacity using *previously considered* items.

## When NOT to Use 0/1 Knapsack

1. **Unlimited Item Usage**: If items can be reused, use Unbounded Knapsack.
   *Example: Coin Change (you have unlimited 1¢, 5¢, 10¢ coins).*
2. **Very Large Capacity**: If $W = 10^9$, $O(n \times W)$ will TLE (Time Limit Exceeded) and MLE (Memory Limit Exceeded). Consider:
   - Meeting in the middle ($O(2^{n/2})$ for small $n$, e.g., $n \leq 40$)
   - Branch and Bound (A* Search)
3. **Fractions Allowed (Fractional Knapsack)**: If you can take 50% of an item for 50% of its value, use a Greedy approach. Sort items by value/weight ratio and take as much of the highest ratio items as possible. DP is overkill and slower.
4. **Non-Additive Objectives**: If items have synergies (e.g., "Item A and B together give +10 bonus value"), the standard subproblem structure breaks down because choices are no longer independent.

## Problem Statement

Given weights and values of $n$ items, find maximum value that fits in capacity $W$. Each item can be used at most once (0/1 = take or don't take).

```
Input:
  weights = [1, 3, 4, 5]
  values = [1, 4, 5, 7]
  capacity = 7

Output: 9
Explanation: Take items with weights 3 and 4 (values 4 + 5 = 9)
```

## Implementations

### 1. Top-Down (Memoization)

Good for sparse capacities where not all states are visited.

```python
def knapsack_memo(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Top-Down DP (Memoization)
    Time: O(n * W)
    Space: O(n * W) for memoization table + O(n) call stack
    """
    memo = {}

    def dfs(i: int, w: int) -> int:
        # Base case: no items left or no capacity left
        if i < 0 or w == 0:
            return 0

        if (i, w) in memo:
            return memo[(i, w)]

        # Choice 1: Exclude item i
        res = dfs(i - 1, w)

        # Choice 2: Include item i (if it fits)
        if weights[i] <= w:
            res = max(res, values[i] + dfs(i - 1, w - weights[i]))

        memo[(i, w)] = res
        return res

    return dfs(len(weights) - 1, capacity)
```

### 2. Bottom-Up 2D (Tabulation)

Clearest mapping to the recurrence relation.

```python
def knapsack_2d(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Bottom-Up DP (Tabulation)
    Time: O(n * W)
    Space: O(n * W)
    """
    n = len(weights)
    # dp[i][w] = max value using first i items with capacity w
    # Size is (n+1) x (capacity+1) to handle base cases (0 items, 0 capacity)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wt = weights[i - 1]
        val = values[i - 1]

        for w in range(capacity + 1):
            # Default: don't take the item
            dp[i][w] = dp[i - 1][w]

            # If it fits, see if taking it is better
            if wt <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - wt] + val
                )

    return dp[n][capacity]
```

### 3. Space-Optimized 1D (Best Practice)

Notice in the 2D version, `dp[i][w]` only depends on the *previous row* `dp[i-1]`. We can optimize space from $O(n \times W)$ to $O(W)$ by keeping only one row.

```python
def knapsack_1d(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Space-Optimized Bottom-Up DP
    Time: O(n * W)
    Space: O(W)
    """
    n = len(weights)
    dp = [0] * (capacity + 1)

    for i in range(n):
        wt = weights[i]
        val = values[i]

        # CRITICAL: Iterate backwards!
        for w in range(capacity, wt - 1, -1):
            dp[w] = max(dp[w], dp[w - wt] + val)

    return dp[capacity]
```

## Why Iterate Backwards in 1D DP?

When compressing from 2D to 1D, we drop the item index `i`.
`dp[w]` represents the current row `i` being built, while trying to read values from the previous row `i-1`.

The recurrence is: `new_dp[w] = max(old_dp[w], old_dp[w - wt] + val)`

Because `w - wt < w`, the value we need to read (`w - wt`) is always to the *left* of the current capacity `w`.

**If we iterate forward (Left to Right):**
```
Item weight = 2, value = 3
w=2: dp[2] = max(dp[2], dp[0] + 3) = 3  (Uses the item once)
w=4: dp[4] = max(dp[4], dp[2] + 3) = 6  (Uses dp[2] which ALREADY includes the item!)
```
Forward iteration effectively allows an item to be selected multiple times. This solves the *Unbounded* Knapsack problem.

**If we iterate backward (Right to Left):**
```
Item weight = 2, value = 3
w=4: dp[4] = max(dp[4], dp[2] + 3) = 3  (Reads dp[2] from the PREVIOUS item iteration)
w=2: dp[2] = max(dp[2], dp[0] + 3) = 3  (Reads dp[0] from the PREVIOUS item iteration)
```
Backward iteration guarantees that when evaluating `dp[w]`, all values to its left (`dp[w - wt]`) have *not yet been updated* in the current loop. Therefore, they still hold the values from the previous item (`i-1`), perfectly matching the 2D recurrence.

---

## DP Table Visualization

For `weights = [1, 3, 4]`, `values = [15, 20, 30]`, `capacity = 4`:

| Item (wt, val) \ Cap | 0 | 1 | 2 | 3 | 4 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0** (0, 0) | 0 | 0 | 0 | 0 | 0 |
| **1** (1, 15) | 0 | 15 | 15 | 15 | 15 |
| **2** (3, 20) | 0 | 15 | 15 | 20 | 35 |
| **3** (4, 30) | 0 | 15 | 15 | 20 | 35 |

*At `dp[2][4]`: max(exclude item 2 `dp[1][4]=15`, include item 2 `dp[1][4-3] + 20 = dp[1][1] + 20 = 15 + 20 = 35`)*

---

## Related Patterns

Many problems are 0/1 Knapsack in disguise. The trick is identifying the "capacity" and "items".

### Subset Sum (Can we sum to target?)
Items = numbers, Capacity = target, Value = N/A (boolean state).
```python
def can_partition(nums: list[int], target: int) -> bool:
    dp = [False] * (target + 1)
    dp[0] = True  # Base case: sum of 0 is always possible with empty subset

    for num in nums:
        for t in range(target, num - 1, -1): # Backward!
            dp[t] = dp[t] or dp[t - num]

    return dp[target]
```

### Partition Equal Subset Sum
Target is exactly `sum(nums) / 2`. Reduces directly to Subset Sum.

### Target Sum (Assign +/- to sum to target)
Let $P$ be subset of positive numbers, $N$ be negative.
$P - N = target$ and $P + N = \sum nums$
$\Rightarrow 2P = target + \sum nums \Rightarrow P = (target + \sum nums) / 2$
Reduces to finding count of subsets that sum to $P$.

```python
def find_target_sum_ways(nums: list[int], target: int) -> int:
    total = sum(nums)
    if (total + target) % 2 != 0 or total < abs(target): return 0

    p = (total + target) // 2
    dp = [0] * (p + 1)
    dp[0] = 1 # 1 way to make sum 0

    for num in nums:
        for t in range(p, num - 1, -1):
            dp[t] += dp[t - num]

    return dp[p]
```

### Last Stone Weight II (Minimize difference between two partitions)
Find a subset sum closest to $\lfloor \text{total} / 2 \rfloor$. The remaining stones form the other subset.

---

## Complexity Recap

| Approach | Time | Space | Notes |
| :--- | :--- | :--- | :--- |
| Top-Down Memoization | $O(n \times W)$ | $O(n \times W)$ | Best when capacity space is sparse |
| Bottom-Up 2D | $O(n \times W)$ | $O(n \times W)$ | Easiest to debug |
| Bottom-Up 1D | $O(n \times W)$ | $O(W)$ | Standard interview answer |

*Note: These are **pseudo-polynomial** time (polynomial relative to the numeric value of W, but exponential relative to the number of bits needed to represent W).*