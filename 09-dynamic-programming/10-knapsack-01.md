# 0/1 Knapsack

> **Prerequisites:** [07-2d-dp-basics](./07-2d-dp-basics.md)

## Overview

0/1 Knapsack is a fundamental optimization problem where you select items (each usable at most once) to maximize value while staying within a weight capacity.

## Building Intuition

**Why is 0/1 Knapsack solved with DP?**

1. **Exponential Choices, Polynomial States**: With n items, there are 2^n possible subsets. But the answer only depends on (current item index, remaining capacity)—just n × W states.

2. **The Include/Exclude Decision**: For each item, we have two choices:
   - **Exclude item i**: Best value is same as with items 0..i-1 and same capacity.
   - **Include item i**: Best value is value[i] + best value for remaining capacity (capacity - weight[i]) using items 0..i-1.

   We take the max. This captures all 2^n possibilities efficiently.

3. **Why Backward Iteration (1D DP)**: In the space-optimized version, we iterate capacity backward. Why? If we go forward, dp[w - weight[i]] has already been updated in this iteration—we'd be using the same item twice! Backward ensures we use values from the "previous item" row.

4. **Pseudo-Polynomial Complexity**: O(n × W) looks polynomial, but W is a VALUE (number of possible weights), not the INPUT SIZE (log W bits). If W = 10^9, this is infeasible.

5. **Mental Model**: Imagine packing a backpack before a hike. You consider items one by one. For each item, you ask: "If I take this, is the value gained worth the capacity I lose?" You can only decide based on what you COULD fit before considering this item.

## Interview Context

0/1 Knapsack is a foundational pattern because:

1. **Classic optimization**: Maximum value with constraints
2. **Include/exclude decision**: Binary choice at each step
3. **Many variations**: Subset sum, partition, target sum
4. **Space optimization**: 2D → 1D reduction

---

## When NOT to Use 0/1 Knapsack

1. **Unlimited Item Usage**: If items can be reused, use Unbounded Knapsack (forward iteration, not backward).

2. **Very Large Capacity**: If W = 10^9, O(n × W) is infeasible. Consider:
   - Meeting in the middle (O(2^(n/2)) for small n)
   - Approximation algorithms
   - Greedy if items are divisible (fractional knapsack)

3. **Greedy Works (Fractional Knapsack)**: If you can take fractions of items, sort by value/weight ratio and take greedily. DP is unnecessary.

4. **Multiple Knapsacks**: For bin packing or multiple knapsack problems, standard 0/1 DP doesn't apply directly. Use more complex formulations.

5. **Non-Additive Objectives**: If total value isn't the sum of individual values (e.g., discounts for combinations), the standard recurrence breaks.

**Recognize 0/1 Knapsack Pattern When:**

- Each item has weight and value
- Capacity constraint
- Each item used at most once
- Maximize/minimize sum
- Reduction: Subset Sum, Partition, Target Sum

---

## Problem Statement

Given weights and values of n items, find maximum value that fits in capacity W.
Each item can be used at most once (0/1 = take or don't take).

```
Input:
  weights = [1, 3, 4, 5]
  values = [1, 4, 5, 7]
  capacity = 7

Output: 9
Explanation: Take items with weights 3 and 4 (values 4 + 5 = 9)
```

---

## Solution

```python
def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    """
    0/1 Knapsack - maximum value within capacity.

    State: dp[i][w] = max value using items 0..i-1 with capacity w
    Recurrence:
        If weight[i-1] > w: dp[i][w] = dp[i-1][w]
        Else: dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight[i-1]] + value[i-1])

    Time: O(n × W)
    Space: O(W)
    """
    n = len(weights)
    dp = [0] * (capacity + 1)

    for i in range(n):
        # Iterate backwards to avoid using same item twice
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]
```

### 2D Version (Clearer)

```python
def knapsack_2d(weights: list[int], values: list[int], capacity: int) -> int:
    """
    2D DP version for clarity.

    Time: O(n × W)
    Space: O(n × W)
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]  # Don't take item

            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )

    return dp[n][capacity]
```

---

## Why Iterate Backwards?

```
Forward iteration (WRONG for 0/1):
weights = [2], values = [3], capacity = 4

w=2: dp[2] = max(dp[2], dp[0] + 3) = 3
w=3: dp[3] = max(dp[3], dp[1] + 3) = 3
w=4: dp[4] = max(dp[4], dp[2] + 3) = 6  ← Uses item TWICE!

Backward iteration (CORRECT):
w=4: dp[4] = max(dp[4], dp[2] + 3) = 3
w=3: dp[3] = max(dp[3], dp[1] + 3) = 3
w=2: dp[2] = max(dp[2], dp[0] + 3) = 3  ✓ Each item used once
```

---

## Related: Subset Sum

```python
def can_partition(nums: list[int], target: int) -> bool:
    """
    Can we select subset that sums to target?

    Time: O(n × target)
    Space: O(target)
    """
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for t in range(target, num - 1, -1):
            dp[t] = dp[t] or dp[t - num]

    return dp[target]
```

---

## Related: Partition Equal Subset Sum

```python
def can_partition_equal(nums: list[int]) -> bool:
    """
    Can partition into two subsets with equal sum?

    Time: O(n × sum/2)
    Space: O(sum/2)
    """
    total = sum(nums)

    if total % 2 != 0:
        return False

    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for t in range(target, num - 1, -1):
            dp[t] = dp[t] or dp[t - num]

    return dp[target]
```

---

## Related: Target Sum

```python
def find_target_sum_ways(nums: list[int], target: int) -> int:
    """
    Count ways to assign +/- to nums to get target.

    Transform: Let P = positive subset, N = negative subset
    P - N = target
    P + N = sum(nums)
    2P = target + sum(nums)
    P = (target + sum(nums)) / 2

    So count subsets summing to P.

    Time: O(n × P)
    Space: O(P)
    """
    total = sum(nums)

    if (total + target) % 2 != 0 or total + target < 0:
        return 0

    p = (total + target) // 2
    dp = [0] * (p + 1)
    dp[0] = 1

    for num in nums:
        for t in range(p, num - 1, -1):
            dp[t] += dp[t - num]

    return dp[p]
```

---

## Related: Count Subsets with Sum

```python
def count_subsets_with_sum(nums: list[int], target: int) -> int:
    """
    Count subsets that sum to target.

    Time: O(n × target)
    Space: O(target)
    """
    dp = [0] * (target + 1)
    dp[0] = 1  # Empty subset

    for num in nums:
        for t in range(target, num - 1, -1):
            dp[t] += dp[t - num]

    return dp[target]
```

---

## Related: Last Stone Weight II

```python
def last_stone_weight_ii(stones: list[int]) -> int:
    """
    Minimize remaining stone weight after optimal smashing.

    Key insight: Partition into two groups, minimize difference.
    Same as: find subset sum closest to total/2.

    Time: O(n × sum/2)
    Space: O(sum/2)
    """
    total = sum(stones)
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for stone in stones:
        for t in range(target, stone - 1, -1):
            dp[t] = dp[t] or dp[t - stone]

    # Find largest achievable sum <= target
    for t in range(target, -1, -1):
        if dp[t]:
            return total - 2 * t

    return 0
```

---

## Reconstructing the Solution

```python
def knapsack_with_items(weights: list[int], values: list[int],
                        capacity: int) -> tuple[int, list[int]]:
    """
    Return max value and indices of items taken.
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w],
                               dp[i - 1][w - weights[i - 1]] + values[i - 1])

    # Backtrack
    items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            items.append(i - 1)
            w -= weights[i - 1]

    return dp[n][capacity], items[::-1]
```

---

## Edge Cases

```python
# 1. Empty items
weights, values = [], []
capacity = 10
# Return 0

# 2. Zero capacity
weights = [1, 2, 3]
values = [10, 20, 30]
capacity = 0
# Return 0

# 3. All items fit
weights = [1, 1, 1]
values = [10, 20, 30]
capacity = 10
# Return 60 (take all)

# 4. Single item
weights = [5]
values = [10]
capacity = 5
# Return 10
```

---

## Common Mistakes

```python
# WRONG: Forward iteration for 0/1 knapsack
for num in nums:
    for t in range(num, target + 1):  # Forward!
        dp[t] = dp[t] or dp[t - num]  # Uses same item multiple times!

# CORRECT: Backward iteration
for t in range(target, num - 1, -1):  # Backward!


# WRONG: Wrong loop bounds
for w in range(capacity, weights[i], -1):  # Misses weights[i]

# CORRECT:
for w in range(capacity, weights[i] - 1, -1):  # Include weights[i]
```

---

## Complexity

| Problem         | Time          | Space     |
| --------------- | ------------- | --------- |
| 0/1 Knapsack    | O(n × W)      | O(W)      |
| Subset Sum      | O(n × target) | O(target) |
| Partition Equal | O(n × sum/2)  | O(sum/2)  |
| Target Sum      | O(n × P)      | O(P)      |

Note: These are **pseudo-polynomial** time (polynomial in numeric value, not input size).

---

## Interview Tips

1. **Identify knapsack pattern**: Include/exclude decision with capacity
2. **Transform the problem**: Target Sum → Subset Sum
3. **Know iteration direction**: Backward for 0/1, forward for unbounded
4. **Handle edge cases**: Empty, zero capacity, overflow
5. **Mention complexity**: Pseudo-polynomial, not truly polynomial

---

## Practice Problems

| #   | Problem                    | Difficulty | Variant            |
| --- | -------------------------- | ---------- | ------------------ |
| 1   | 0/1 Knapsack               | Medium     | Classic            |
| 2   | Partition Equal Subset Sum | Medium     | Boolean subset     |
| 3   | Target Sum                 | Medium     | Count with +/-     |
| 4   | Last Stone Weight II       | Medium     | Min partition diff |
| 5   | Ones and Zeroes            | Medium     | 2D knapsack        |

---

## Key Takeaways

1. **Binary choice**: Take or don't take each item
2. **Backward iteration**: Ensures each item used once
3. **Transform problems**: Many reduce to subset sum
4. **Space optimization**: 1D array sufficient
5. **Pseudo-polynomial**: Depends on capacity value

---

## Next: [11-knapsack-unbounded.md](./11-knapsack-unbounded.md)

Learn unbounded knapsack where items can be used multiple times.
