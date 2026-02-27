# 0/1 Knapsack

> **Prerequisites:** [07-2d-dp-basics](./07-2d-dp-basics.md)

## Overview

0/1 Knapsack is a fundamental optimization problem. You are given a set of items, each with a weight and a value. You need to determine the maximum value you can pack into a knapsack of a given capacity.

The "0/1" part means you have a binary choice for each item: you either include it completely (1) or exclude it completely (0). You cannot take fractions of an item, and you cannot take multiple copies of the same item.

## Formal Recurrence

Let $dp[i][w]$ be the maximum value we can achieve using a subset of the first $i$ items, given a total weight limit of $w$.

For the $i$-th item (1-indexed), which has weight $wt[i-1]$ and value $val[i-1]$, we have two choices:

1.  **Exclude it:** The maximum value is what we could get with the first $i-1$ items with the same capacity $w$.
    $$dp[i][w] = dp[i-1][w]$$
2.  **Include it:** If $wt[i-1] \leq w$, we gain $val[i-1]$ but use $wt[i-1]$ capacity. We add this to the best we could do with the remaining capacity $w - wt[i-1]$ using the first $i-1$ items.
    $$dp[i][w] = dp[i-1][w - wt[i-1]] + val[i-1]$$

Combining these choices, we want the maximum of both:
$$
dp[i][w] =
\begin{cases}
dp[i-1][w] & \text{if } wt[i-1] > w \\
\max(dp[i-1][w], dp[i-1][w - wt[i-1]] + val[i-1]) & \text{if } wt[i-1] \leq w
\end{cases}
$$

**Base Cases:**
*   $dp[0][w] = 0$ for all $w \in [0, W]$ (0 value with 0 items)
*   $dp[i][0] = 0$ for all $i \in [0, n]$ (0 value with 0 capacity)

## Building Intuition

**Why is 0/1 Knapsack solved with DP?**

1.  **Exponential Choices, Polynomial States**: With $n$ items, there are $2^n$ possible subsets. However, the optimal answer only depends on two factors: (current item index, remaining capacity). This gives us just $n \times W$ unique states to evaluate.
2.  **Optimal Substructure**: The optimal solution to the problem containing $n$ items and capacity $W$ contains optimal solutions to subproblems (e.g., $n-1$ items with capacity $W$, or $n-1$ items with capacity $W - wt[n]$).
3.  **Overlapping Subproblems**: Different combinations of items might leave us with the same remaining capacity at the same item index. DP prevents recalculating these.

**Mental Model:**
Imagine packing a backpack. You go through your items one by one. For each item, you ask: "If I take this, is the value gained worth the capacity I lose?" You make this decision based on the optimal packing of the *remaining* capacity using *previously considered* items.

## When NOT to Use 0/1 Knapsack

1.  **Unlimited Item Usage**: If items can be reused multiple times, use **Unbounded Knapsack**. (e.g., Coin Change - you have unlimited 1¢, 5¢, 10¢ coins).
2.  **Very Large Capacity**: If $W$ is very large (e.g., $10^9$), an $O(n \times W)$ DP approach will result in Time Limit Exceeded (TLE) and Memory Limit Exceeded (MLE). Consider:
    *   Meeting in the middle ($O(2^{n/2})$ for small $n \leq 40$)
    *   Branch and Bound
3.  **Fractions Allowed (Fractional Knapsack)**: If you can take fractions of items (e.g., gold dust), use a **Greedy** approach. Sort items by value-to-weight ratio and take as much as possible from the highest ratio items. DP is overkill and slower.
4.  **Non-Additive Objectives**: If items have complex synergies (e.g., "Item A and B together give a bonus"), the standard subproblem structure breaks down because choices are no longer independent.

## Implementations

### Problem Statement

Given `weights` and `values` of $n$ items, find the maximum value that fits in `capacity` $W$. Each item can be used at most once.

```python
# Example
weights = [1, 3, 4, 5]
values = [1, 4, 5, 7]
capacity = 7

# Output: 9
# Explanation: Take items with weights 3 and 4 (values 4 + 5 = 9).
```

### 1. Top-Down (Memoization)

This approach recursively solves the problem and caches the results. It's often easier to write and can be faster if the capacity space is sparse (i.e., not all states are visited).

```python
from functools import cache

def knapsack_memo(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Top-Down DP (Memoization)
    Time: O(n * W)
    Space: O(n * W) for memo table + call stack
    """
    n = len(weights)

    @cache
    def dfs(i: int, w: int) -> int:
        # Base case: no items left or no capacity left
        if i == n or w == 0:
            return 0

        # Choice 1: Exclude item i
        res = dfs(i + 1, w)

        # Choice 2: Include item i (if it fits)
        if weights[i] <= w:
            res = max(res, values[i] + dfs(i + 1, w - weights[i]))

        return res

    return dfs(0, capacity)
```

### 2. Bottom-Up 2D (Tabulation)

This approach builds a 2D table iteratively. It provides the clearest mapping to the formal recurrence relation.

```python
def knapsack_2d(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Bottom-Up DP (Tabulation)
    Time: O(n * W)
    Space: O(n * W)
    """
    n = len(weights)
    # dp[i][w] = max value using first i items with capacity w
    # Size is (n+1) x (capacity+1) to handle base cases
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wt = weights[i - 1]
        val = values[i - 1]

        for w in range(capacity + 1):
            # Exclude the item
            dp[i][w] = dp[i - 1][w]

            # Include the item if it fits
            if wt <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - wt] + val
                )

    return dp[n][capacity]
```

### DP Table Visualization (2D)

For `weights = [1, 3, 4]`, `values = [15, 20, 30]`, `capacity = 4`:

| Item `i` (wt, val) \ Cap `w` | 0 | 1 | 2 | 3 | 4 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0** (0, 0) | 0 | 0 | 0 | 0 | 0 |
| **1** (1, 15) | 0 | 15 | 15 | 15 | 15 |
| **2** (3, 20) | 0 | 15 | 15 | 20 | 35 |
| **3** (4, 30) | 0 | 15 | 15 | 20 | 35 |

*At `dp[2][4]`: `max(exclude item 2 (dp[1][4] -> 15), include item 2 (dp[1][4-3] + 20 -> 15 + 20 = 35)) = 35`*

### 3. Space-Optimized 1D (Best Practice)

Notice in the 2D version, computing `dp[i][w]` only requires values from the *previous row* `dp[i-1]`. We don't need the entire $n \times W$ table at once. We can optimize the space from $O(n \times W)$ down to $O(W)$ by keeping only a single 1D array representing the "current" row.

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

#### Why Iterate Backwards in 1D DP?

When compressing from 2D to 1D, `dp[w]` represents the state we are calculating for item $i$, but we need it to read values calculated for item $i-1$.

The recurrence is: `new_dp[w] = max(old_dp[w], old_dp[w - wt] + val)`

Because `w - wt < w`, the value we need to read (`w - wt`) is always to the *left* of the current capacity `w`.

**If we iterate forward (Left to Right):**
```
Item weight = 2, value = 3
w=2: dp[2] = max(dp[2], dp[0] + 3) = 3  (Uses the item once)
w=4: dp[4] = max(dp[4], dp[2] + 3) = 6  (Uses dp[2] which ALREADY includes the item!)
```
Forward iteration effectively allows an item to be selected multiple times, because `dp[w - wt]` has already been updated with the current item's choice. This solves the **Unbounded Knapsack** problem, not 0/1 Knapsack.

**If we iterate backward (Right to Left):**
```
Item weight = 2, value = 3
w=4: dp[4] = max(dp[4], dp[2] + 3) = 3  (Reads dp[2] from the PREVIOUS item iteration)
w=2: dp[2] = max(dp[2], dp[0] + 3) = 3  (Reads dp[0] from the PREVIOUS item iteration)
```
Backward iteration guarantees that when evaluating `dp[w]`, all values to its left (`dp[w - wt]`) have *not yet been updated* in the current outer loop iteration. Therefore, they correctly reflect the state from the previous item ($i-1$).

---

## Related Patterns

Many DP problems are 0/1 Knapsack in disguise. The key is identifying the "items," the "capacity," and what constitutes the "value."

### 1. Subset Sum (Can we partition to a target?)
*   **Items:** Numbers in the array.
*   **Capacity:** Target sum.
*   **Value:** Boolean (True/False if sum is possible).

```python
def can_partition(nums: list[int], target: int) -> bool:
    dp = [False] * (target + 1)
    dp[0] = True  # Sum of 0 is always possible (empty subset)

    for num in nums:
        # Backward iteration!
        for t in range(target, num - 1, -1):
            # It's possible if we already could make `t`, or if we could make `t - num`
            dp[t] = dp[t] or dp[t - num]

    return dp[target]
```

### 2. Partition Equal Subset Sum
Can we partition an array into two subsets such that the sum of elements in both subsets is equal?
*   This is identical to Subset Sum where the `target` is exactly `sum(nums) / 2`.
*   If `sum(nums)` is odd, it's impossible. Otherwise, call `can_partition(nums, sum(nums) // 2)`.

### 3. Target Sum (Assign +/- to sum to target)
Given an array of integers, you want to assign a `+` or `-` sign to each to achieve a specific target.
Let $P$ be the sum of numbers assigned positive signs, and $N$ be the sum of numbers assigned negative signs.
1.  $P - N = target$
2.  $P + N = \sum nums$

Adding the two equations:
$2P = target + \sum nums$
$P = \frac{target + \sum nums}{2}$

This reduces the problem to finding the *number of subsets* that sum to exactly $P$.

```python
def find_target_sum_ways(nums: list[int], target: int) -> int:
    total_sum = sum(nums)

    # Check if a valid positive sum P exists
    if total_sum < abs(target) or (total_sum + target) % 2 != 0:
        return 0

    p = (total_sum + target) // 2
    dp = [0] * (p + 1)
    dp[0] = 1  # 1 way to make sum 0 (choose nothing)

    for num in nums:
        for t in range(p, num - 1, -1):
            # The number of ways to make t is increased by the number of ways to make t - num
            dp[t] += dp[t - num]

    return dp[p]
```

### 4. Last Stone Weight II
You have a set of stones. You smash two stones together, and their difference remains. What is the smallest possible weight of the final stone?
*   Smashing stones $x$ and $y$ leaves $x - y$. Smashing $(x - y)$ with $z$ leaves $(x - y) - z = x - y - z$.
*   Ultimately, the remaining stone is the difference between two subsets of stones.
*   We want to minimize this difference, which means we want to find a subset whose sum is as close to $\lfloor \text{sum(stones)} / 2 \rfloor$ as possible.
*   This is 0/1 Knapsack where `capacity = sum(stones) // 2`, `weights = stones`, and `values = stones`.

```python
def lastStoneWeightII(stones: list[int]) -> int:
    total_sum = sum(stones)
    capacity = total_sum // 2

    dp = [0] * (capacity + 1)

    for stone in stones:
        for w in range(capacity, stone - 1, -1):
            dp[w] = max(dp[w], dp[w - stone] + stone)

    # dp[capacity] holds the max subset sum <= total_sum // 2
    # The other subset sum will be total_sum - dp[capacity]
    # The difference is the final stone weight
    return (total_sum - dp[capacity]) - dp[capacity]
```

---

## Complexity Recap

| Approach | Time | Space | Notes |
| :--- | :--- | :--- | :--- |
| Top-Down Memoization | $O(n \times W)$ | $O(n \times W)$ | Good when capacity space is sparse. Uses recursion stack. |
| Bottom-Up 2D | $O(n \times W)$ | $O(n \times W)$ | Easiest to debug and conceptualize. |
| Bottom-Up 1D | $O(n \times W)$ | $O(W)$ | **Best practice.** Optimized space. Standard interview answer. |

*Note: These algorithms run in **pseudo-polynomial** time. $O(n \times W)$ is polynomial relative to the numeric value of $W$, but exponential relative to the number of bits needed to represent the value $W$ in binary.*