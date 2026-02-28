# 0/1 Knapsack

> **Prerequisites:** [07-2d-dp-basics](./07-2d-dp-basics.md)

## Overview

The 0/1 Knapsack problem is the undisputed king of Dynamic Programming optimization problems. If you understand 0/1 Knapsack deeply, a massive chunk of DP interview questions will suddenly look like trivial variations of the exact same code.

**The Setup:**
Imagine you are a thief in a jewelry store. You have a knapsack (backpack) that can hold a maximum weight $W$. There are $n$ items in the store, each with a specific `weight` and a `value`. Your goal is to maximize the total value of the items you put in your knapsack without exceeding its weight capacity.

**The "0/1" Constraint:**
For every single item, you face a binary choice:
- **0 (Exclude):** You leave the item behind.
- **1 (Include):** You put the entire item in your knapsack.

You *cannot* take a fraction of an item (like taking half a gold bar), and you *cannot* take an item multiple times.

---

## Building Intuition

**Why is 0/1 Knapsack solved with DP?**

A brute-force approach would try every possible combination of items. For $n$ items, there are $2^n$ possible subsets. This exponential time complexity $O(2^n)$ is far too slow for even small values of $n$.

However, the problem exhibits the two hallmarks of DP:

1. **Optimal Substructure:** The best way to pack a knapsack of capacity $W$ using $n$ items relies on the best way to pack smaller capacities using fewer items. If we decide to include the $n$-th item, the remaining problem is finding the optimal way to pack the remaining capacity $W - \text{weight}[n]$ using the first $n-1$ items.
2. **Overlapping Subproblems:** Different combinations of items might leave us with the exact same remaining capacity and the same set of items left to consider. DP prevents us from recalculating these identical states.

**Mental Model:**
Process the items one by one. For the current item, ask yourself: *"If I have $w$ capacity available right now, does adding this item give me a better total value than if I just completely ignored it and stuck with whatever optimal combination I already found for the previous items using this exact same capacity $w$?"*

---

## Formal Recurrence

Let $dp[i][w]$ be the maximum value we can achieve using a subset of the **first $i$ items** (from index 0 to $i-1$), given a maximum capacity constraint of $w$.

For the item at index $i-1$ (which has weight $wt[i-1]$ and value $val[i-1]$), we have two choices:

1.  **Exclude the item:** The maximum value is simply whatever we could achieve using the previous $i-1$ items with the exact same capacity $w$.
    $$dp[i][w] = dp[i-1][w]$$

2.  **Include the item:** We can only do this if the item actually fits ($wt[i-1] \leq w$). If it does, we gain its value ($val[i-1]$), but we consume its weight. We must add this value to the maximum value we could have achieved with the *remaining* capacity ($w - wt[i-1]$) using the previous $i-1$ items.
    $$dp[i][w] = dp[i-1][w - wt[i-1]] + val[i-1]$$

**The Transition:**
We want to maximize our value, so we take the better of the two choices:
$$
dp[i][w] =
\begin{cases}
dp[i-1][w] & \text{if } wt[i-1] > w \text{ (too heavy)} \\
\max(dp[i-1][w], dp[i-1][w - wt[i-1]] + val[i-1]) & \text{if } wt[i-1] \leq w \text{ (fits)}
\end{cases}
$$

**Base Cases:**
- $dp[0][w] = 0$ for all $w \in [0, W]$ (0 items available means 0 value).
- $dp[i][0] = 0$ for all $i \in [0, n]$ (0 capacity means we can't take any items, so 0 value).

---

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

This approach recursively explores both choices (include/exclude) and caches the results to avoid redundant work. It evaluates the state space on-demand, which can be faster if the capacity $W$ is very large but few intermediate capacities are actually reachable.

```python
from functools import cache

def knapsack_memo(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Top-Down DP (Memoization)
    Time: O(n * capacity)
    Space: O(n * capacity) for the memoization cache and call stack.
    """
    n = len(weights)

    @cache
    def dfs(i: int, w: int) -> int:
        # Base case: no items left to consider, or knapsack is full
        if i == n or w == 0:
            return 0

        # Choice 1: Exclude item i
        res = dfs(i + 1, w)

        # Choice 2: Include item i (if it fits in the remaining capacity w)
        if weights[i] <= w:
            res = max(res, values[i] + dfs(i + 1, w - weights[i]))

        return res

    # Start with item index 0 and the full initial capacity
    return dfs(0, capacity)
```

### 2. Bottom-Up 2D (Tabulation)

This iterative approach builds the solution systematically from smaller subproblems up to the target capacity. It directly maps to the formal recurrence relation.

```python
def knapsack_2d(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Bottom-Up DP (Tabulation)
    Time: O(n * capacity)
    Space: O(n * capacity)
    """
    n = len(weights)
    # dp[i][w] = max value using the first i items with a capacity of w.
    # We use dimensions (n + 1) x (capacity + 1) to naturally handle the base cases (0 items/0 capacity).
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wt = weights[i - 1]
        val = values[i - 1]

        for w in range(capacity + 1):
            # Base choice: Always consider excluding the item
            dp[i][w] = dp[i - 1][w]

            # If the item fits, consider including it and take the max
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
| **0** (0, 0) | `0` | `0` | `0` | `0` | `0` |
| **1** (1, 15) | `0` | `15` | `15` | `15` | `15` |
| **2** (3, 20) | `0` | `15` | `15` | `20` | `35` |
| **3** (4, 30) | `0` | `15` | `15` | `20` | `35` |

**Trace at `dp[2][4]` (evaluating Item 2 with weight 3, value 20 at capacity 4):**
- **Exclude Item 2:** Look directly above $\rightarrow dp[1][4] = 15$.
- **Include Item 2:** Look above, but shifted left by weight $3$ $\rightarrow dp[1][4-3] + 20 \rightarrow 15 + 20 = 35$.
- $\max(15, 35) = 35$.

### 3. Space-Optimized 1D (Best Practice)

In the 2D visualization above, notice that to compute the values for row `i`, we *only* ever look at the values from row `i-1`. We don't need the rows `i-2`, `i-3`, etc.

We can squash the $O(n \times W)$ matrix down into a single $1D$ array of size $W+1$ that simply represents the "current" capacity values. As we iterate through each item, we update this array in-place.

```python
def knapsack_1d(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Space-Optimized Bottom-Up DP (1D Tabulation)
    Time: O(n * capacity)
    Space: O(capacity)
    """
    n = len(weights)
    dp = [0] * (capacity + 1)

    for i in range(n):
        wt = weights[i]
        val = values[i]

        # CRITICAL: We MUST iterate backwards through the capacities!
        # We stop at `wt` because if w < wt, the item doesn't fit anyway,
        # so dp[w] would just remain unchanged.
        for w in range(capacity, wt - 1, -1):
            dp[w] = max(dp[w], dp[w - wt] + val)

    return dp[capacity]
```

#### Why Iterate Backwards in 1D DP?

This is the most common pitfall in 1D Knapsack implementations.

When updating `dp[w]` for the current item $i$, we need to read `dp[w - wt]`. According to our 2D recurrence, this read *must* come from the previous item's state ($i-1$).

Because `w - wt < w`, the index we read from is always to the **left** of the index we are writing to.

**If we iterate Left-to-Right (FORWARD):**
Imagine an item with weight $2$, value $10$.
1.  `w=2`: `dp[2] = max(dp[2], dp[0] + 10) = 10`. (We included the item).
2.  `w=4`: `dp[4] = max(dp[4], dp[2] + 10) = max(0, 10 + 10) = 20`.

Wait! We just used `dp[2]` to calculate `dp[4]`. But `dp[2]` was *already updated* in this same loop to include the item. By reading it again, we effectively put the item in the knapsack twice! **Iterating forward solves the Unbounded Knapsack problem, where you have infinite copies of each item.**

**If we iterate Right-to-Left (BACKWARD):**
1.  `w=4`: `dp[4] = max(dp[4], dp[2] + 10) = 10`. (Reads the `dp[2]` from the *previous* item iteration).
2.  `w=2`: `dp[2] = max(dp[2], dp[0] + 10) = 10`. (Reads the `dp[0]` from the *previous* item iteration).

Iterating backward guarantees that when we evaluate `dp[w]`, the cells to its left have not yet been touched by the current item. They safely represent the state from $i-1$.

---

## Related Patterns

Many popular DP problems don't explicitly mention "items" or "capacity," but they reduce exactly to 0/1 Knapsack once you translate the terminology.

### 1. Subset Sum

**Problem:** Given an array of positive integers, can you find a subset that sums exactly to a specific `target`?

**Translation to Knapsack:**
*   **Items:** The numbers in the array.
*   **Weight:** The value of the number itself.
*   **Capacity:** The `target` sum.
*   **Value:** Boolean (`True` if the sum is achievable, `False` otherwise).

Instead of `max()`, we use logical `OR`.

```python
def can_partition(nums: list[int], target: int) -> bool:
    dp = [False] * (target + 1)
    dp[0] = True  # A sum of 0 is always possible (empty subset)

    for num in nums:
        # Backward iteration! Stop at `num` because we can't form sums smaller than `num` using `num`.
        for t in range(target, num - 1, -1):
            # We can make sum `t` if we could ALREADY make it without `num` (dp[t]),
            # OR if we could make `t - num` previously.
            dp[t] = dp[t] or dp[t - num]

    return dp[target]
```

### 2. Partition Equal Subset Sum (LeetCode 416)

**Problem:** Can we partition an array into two subsets such that the sum of elements in both subsets is equal?

**Insight:** If the total sum of the array is $S$, we need to find a subset that sums exactly to $S / 2$.
1.  If $S$ is odd, it's impossible to split into two integers. Return `False`.
2.  If $S$ is even, this is literally just the **Subset Sum** problem where `target = S // 2`.

Call `can_partition(nums, sum(nums) // 2)`.

### 3. Target Sum (LeetCode 494)

**Problem:** Given an array of integers, assign a `+` or `-` sign to each number to achieve a specific `target` sum. Return the number of valid ways to do this.

**Insight (The Math Trick):**
Let $P$ be the subset of numbers assigned a `+` sign.
Let $N$ be the subset of numbers assigned a `-` sign.

We know two things:
1.  Sum($P$) - Sum($N$) = $target$ (This is the goal of the problem)
2.  Sum($P$) + Sum($N$) = Sum(all $nums$) (Every number must be assigned exactly one sign)

If we add the two equations together:
$2 \times \text{Sum}(P) = target + \text{Sum(all } nums)$
$\text{Sum}(P) = \frac{target + \text{Sum(all } nums)}{2}$

This is a massive breakthrough! We have eliminated the `-` signs completely. The problem simply becomes: **Find the number of subsets that sum exactly to $P$.**

This is 0/1 Knapsack where `capacity = P`. Because we want the *number of ways*, we use addition instead of `max()`.

```python
def find_target_sum_ways(nums: list[int], target: int) -> int:
    total_sum = sum(nums)

    # If the required sum P isn't an integer, or total_sum is too small, it's impossible
    if total_sum < abs(target) or (total_sum + target) % 2 != 0:
        return 0

    p = (total_sum + target) // 2
    dp = [0] * (p + 1)
    dp[0] = 1  # 1 way to make a sum of 0 (choose no elements)

    for num in nums:
        for t in range(p, num - 1, -1):
            # The number of ways to form target `t` increases by the number
            # of ways we could form `t - num` before considering `num`.
            dp[t] += dp[t - num]

    return dp[p]
```

### 4. Last Stone Weight II (LeetCode 1049)

**Problem:** You have a set of stones with weights. You smash two stones together; the smaller is destroyed, and the larger is reduced by the weight of the smaller. What is the smallest possible weight of the final stone left?

**Insight:** When you smash stone $A$ and stone $B$, the result is $A - B$. If you smash that result with stone $C$, you get $(A - B) - C = A - B - C$.
Notice that every stone's weight is either added or subtracted from the total. The final stone's weight is exactly equal to the difference between two subsets of stones: Sum($P$) - Sum($N$).

To minimize the final difference, we want the two subsets to be as close to equal as possible. Specifically, we want to find a subset $P$ whose sum is as large as possible without exceeding half the total sum of all stones ($\lfloor \text{Sum} / 2 \rfloor$).

This is exactly 0/1 Knapsack:
*   **Items / Weights / Values:** The stones themselves.
*   **Capacity:** `sum(stones) // 2`.
*   **Goal:** Maximize the value (sum) packed into this capacity.

Once we find the max possible sum for subset $P$ (`dp[capacity]`), the sum of the other subset is $N = \text{total\_sum} - P$. The final stone weight is $N - P = \text{total\_sum} - 2 \times P$.

---

## When NOT to Use 0/1 Knapsack

1.  **Unlimited Item Usage (Unbounded Knapsack):** If you can pick an item an infinite number of times (e.g., Coin Change), you use the forward-iteration 1D DP approach instead.
2.  **Fractional Items (Fractional Knapsack):** If you can take 50% of an item for 50% of its value (e.g., stealing gold dust instead of gold bars), DP is overkill. Use a **Greedy** algorithm: sort items by their value-to-weight ratio and greedily take the highest ratios first. Greedy is $O(n \log n)$, which is much faster.
3.  **Massive Capacity ($W > 10^7$):** The DP approach takes $O(n \times W)$ time and $O(W)$ space. If $W$ is $10^9$, your $O(W)$ array will exceed memory limits, and the loop will Time Limit Exceed (TLE).
    *   If $n$ is small (e.g., $n \leq 40$), use a "Meet in the Middle" approach ($O(2^{n/2})$).
    *   Otherwise, branch and bound / recursive backtracking might be required.
4.  **Complex Interdependencies:** If the value of Item B depends on whether you picked Item A (e.g., set bonuses), the standard independent state transitions of 0/1 Knapsack break down.

---

## Complexity Summary

| Approach | Time | Space | Notes |
| :--- | :--- | :--- | :--- |
| Memoization (Top-Down) | $O(n \times W)$ | $O(n \times W)$ | Good if capacity space is sparse. Risk of `RecursionError` in Python for very large $n$. |
| Tabulation (2D) | $O(n \times W)$ | $O(n \times W)$ | Easiest to conceptualize and debug. |
| **Tabulation (1D)** | $O(n \times W)$ | $O(W)$ | **Best practice.** Optimized space. Expected in interviews. |

*Note: $W$ is the capacity. These algorithms run in **pseudo-polynomial** time. $O(n \times W)$ is polynomial relative to the numeric value of $W$, but exponential relative to the number of bits needed to represent the value $W$ in binary. If $W$ is a billion, the algorithm is slow, even though a billion is only a 30-bit number.*