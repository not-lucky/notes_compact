# Kadane's Algorithm

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Kadane's algorithm finds the maximum subarray sum in O(n) time using a simple but powerful insight: at each position, either extend the current subarray or start fresh. This space-optimized dynamic programming solution is a cornerstone of algorithmic problem-solving.

## Building Intuition

**Why does "extend or restart" give the optimal answer?**

The key insight is **local optimality leads to global optimality**. At each position, we make the locally optimal choice:

1. **The Core Decision**: At position i, the maximum subarray ending at i either:
   - Includes the previous maximum subarray (extend): `prev_max + arr[i]`
   - Starts fresh at i (restart): `arr[i]`
   - We take whichever is larger: `max(arr[i], prev_max + arr[i])`

2. **Why This Works**: If the previous maximum subarray has a positive sum, extending it can only help (positive + anything increases the anything). If it has a negative sum, extending it hurts—we're better off starting fresh.

3. **Simpler Form**: `current_max = max(arr[i], current_max + arr[i])` simplifies to: "If current_max is negative, reset to arr[i]; otherwise, add arr[i] to it."

**Mental Model**: Imagine you're collecting coins (positive) and paying tolls (negative) as you walk. At each step, ask: "Is my accumulated wealth helping or hurting me?" If you're in debt (negative sum), declare bankruptcy and start over. If you have savings (positive sum), keep going.

**Visual Trace**:
```
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

Position 0: current = max(-2, -2) = -2, global = -2
Position 1: current = max(1, -2+1=-1) = 1, global = 1
           (Starting fresh at 1 is better than extending!)
Position 2: current = max(-3, 1-3=-2) = -2, global = 1
Position 3: current = max(4, -2+4=2) = 4, global = 4
           (Starting fresh at 4 is better!)
Position 4: current = max(-1, 4-1=3) = 3, global = 4
Position 5: current = max(2, 3+2=5) = 5, global = 5
Position 6: current = max(1, 5+1=6) = 6, global = 6 ← Maximum!
Position 7: current = max(-5, 6-5=1) = 1, global = 6
Position 8: current = max(4, 1+4=5) = 5, global = 6

Answer: 6 (subarray [4, -1, 2, 1])
```

## When NOT to Use Kadane's Algorithm

Kadane's solves a specific problem:

1. **Non-Contiguous Subsequence**: Kadane's finds contiguous subarrays. For subsequences (non-adjacent elements), use DP with different state.

2. **Product Instead of Sum**: For maximum product, track both max AND min (negative × negative = positive). See Max Product Subarray variation.

3. **Must Include Specific Elements**: If certain elements must be included, Kadane's greedy approach may skip them. Need constrained DP.

4. **Length Constraints**: If subarray must be at least length k or at most length m, standard Kadane's doesn't handle this directly. Need sliding window + Kadane's hybrid.

5. **Multiple Disjoint Subarrays**: "Find 2 non-overlapping subarrays with maximum sum" needs a different approach (left-max and right-max arrays).

6. **All Elements Are Negative**: Kadane's still works (returns the least negative), but clarify with interviewer: "Is empty subarray allowed?" If yes, answer is 0.

**Red Flags:**
- "Subsequence" (not subarray) → Different DP
- "Product" (not sum) → Track min and max
- "Exactly k elements" → Sliding window or constrained DP
- "Two disjoint subarrays" → Left/right max arrays

---

## Interview Context

Kadane's algorithm solves the Maximum Subarray problem in O(n) time. This is a classic interview problem because:

- It tests dynamic programming intuition
- Has many variations (product, circular, 2D)
- Simple but easy to get wrong
- Foundation for more complex DP problems

Maximum Subarray is a top-10 most asked interview question at FANG+.

---

## The Problem

Given an array of integers, find the contiguous subarray with the largest sum.

```
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

Maximum subarray: [4, -1, 2, 1] with sum = 6
```

---

## Core Insight

At each position, we have two choices:
1. **Extend** the current subarray (include this element)
2. **Start fresh** from this element

We extend if the current sum + element > element alone.

```
current_sum = max(arr[i], current_sum + arr[i])

If current_sum > 0: extending helps
If current_sum < 0: start fresh (negative sum only hurts)
```

---

## Template: Maximum Subarray Sum

```python
def max_subarray(arr: list[int]) -> int:
    """
    Find the maximum sum of any contiguous subarray.

    Time: O(n)
    Space: O(1)

    Example:
    [-2, 1, -3, 4, -1, 2, 1, -5, 4] → 6
    """
    if not arr:
        return 0

    current_sum = arr[0]
    max_sum = arr[0]

    for i in range(1, len(arr)):
        # Extend current subarray OR start new one
        current_sum = max(arr[i], current_sum + arr[i])
        max_sum = max(max_sum, current_sum)

    return max_sum
```

### Visual Trace

```
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

i=0: current=-2, max=-2
i=1: current=max(1, -2+1)=1, max=1
i=2: current=max(-3, 1-3)=-2, max=1
i=3: current=max(4, -2+4)=4, max=4
i=4: current=max(-1, 4-1)=3, max=4
i=5: current=max(2, 3+2)=5, max=5
i=6: current=max(1, 5+1)=6, max=6  ← answer!
i=7: current=max(-5, 6-5)=1, max=6
i=8: current=max(4, 1+4)=5, max=6

Return 6
```

---

## Template: Maximum Subarray with Indices

```python
def max_subarray_with_indices(arr: list[int]) -> tuple[int, int, int]:
    """
    Return (max_sum, start_index, end_index).

    Time: O(n)
    Space: O(1)
    """
    if not arr:
        return (0, -1, -1)

    current_sum = arr[0]
    max_sum = arr[0]
    start = end = 0
    temp_start = 0

    for i in range(1, len(arr)):
        if arr[i] > current_sum + arr[i]:
            # Start fresh
            current_sum = arr[i]
            temp_start = i
        else:
            # Extend
            current_sum = current_sum + arr[i]

        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i

    return (max_sum, start, end)
```

---

## Variation: Maximum Product Subarray

```python
def max_product(arr: list[int]) -> int:
    """
    Find the maximum product of any contiguous subarray.

    Key insight: Track both max and min because
    negative × negative = positive.

    Time: O(n)
    Space: O(1)

    Example:
    [2, 3, -2, 4] → 6 (subarray [2, 3])
    [-2, 0, -1] → 0 (subarray [0])
    """
    if not arr:
        return 0

    max_prod = min_prod = result = arr[0]

    for i in range(1, len(arr)):
        num = arr[i]

        # Swap if current number is negative
        if num < 0:
            max_prod, min_prod = min_prod, max_prod

        max_prod = max(num, max_prod * num)
        min_prod = min(num, min_prod * num)

        result = max(result, max_prod)

    return result
```

### Why Track Min?

```
arr = [2, -3, -4]

i=0: max=2, min=2, result=2
i=1: num=-3 is negative, swap → max=2, min=2
     max=max(-3, 2×-3)=-3
     min=min(-3, 2×-3)=-6
     result=2
i=2: num=-4 is negative, swap → max=-6, min=-3
     max=max(-4, -6×-4)=24  ← answer!
     min=min(-4, -3×-4)=-4
     result=24

Tracking min allowed us to find 2 × -3 × -4 = 24
```

---

## Variation: Maximum Circular Subarray

```python
def max_circular_subarray(arr: list[int]) -> int:
    """
    Maximum subarray sum in a circular array.

    Key insight: Answer is either:
    1. Normal max subarray (middle portion)
    2. Total - min subarray (wrapping around)

    Time: O(n)
    Space: O(1)

    Example:
    [5, -3, 5] → 10 (wrap: 5 + 5)
    [3, -1, 2, -1] → 4 (wrap: 3 + -1 + 2)
    """
    total = sum(arr)

    # Case 1: Max subarray (normal Kadane)
    max_kadane = kadane_max(arr)

    # Case 2: Max wrap = total - min subarray
    min_kadane = kadane_min(arr)
    max_wrap = total - min_kadane

    # Edge case: all negative (min_kadane = total)
    if max_wrap == 0:
        return max_kadane

    return max(max_kadane, max_wrap)


def kadane_max(arr: list[int]) -> int:
    """Standard Kadane for maximum."""
    current = result = arr[0]
    for i in range(1, len(arr)):
        current = max(arr[i], current + arr[i])
        result = max(result, current)
    return result


def kadane_min(arr: list[int]) -> int:
    """Modified Kadane for minimum."""
    current = result = arr[0]
    for i in range(1, len(arr)):
        current = min(arr[i], current + arr[i])
        result = min(result, current)
    return result
```

### Visual: Why This Works

```
Circular array: [5, -3, 5]

Normal: max contiguous = 5

Circular wrap:
[5, -3, 5] → take [5] + [5] = 10
            ↑       ↑
          end     start

This is equivalent to:
total - (middle portion we DON'T take)
= (5 + -3 + 5) - (-3)
= 7 - (-3)
= 10
```

---

## Variation: Maximum Sum with No Adjacent Elements

```python
def max_sum_no_adjacent(arr: list[int]) -> int:
    """
    Maximum sum where no two elements are adjacent.
    (House Robber problem)

    Time: O(n)
    Space: O(1)

    Example:
    [2, 7, 9, 3, 1] → 12 (2 + 9 + 1)
    [1, 2, 3, 1] → 4 (1 + 3)
    """
    if not arr:
        return 0
    if len(arr) == 1:
        return max(0, arr[0])

    # prev2 = max sum ending 2 positions back
    # prev1 = max sum ending 1 position back
    prev2, prev1 = 0, max(0, arr[0])

    for i in range(1, len(arr)):
        current = max(prev1, prev2 + arr[i])
        prev2, prev1 = prev1, current

    return prev1
```

---

## Variation: Maximum Sum Rectangle (2D)

```python
def max_sum_rectangle(matrix: list[list[int]]) -> int:
    """
    Find rectangle with maximum sum in 2D matrix.

    Time: O(cols² × rows) - for each column pair, run Kadane
    Space: O(rows)

    Uses: For each pair of left/right columns,
          compress to 1D array and apply Kadane.
    """
    if not matrix or not matrix[0]:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    max_sum = float('-inf')

    # Try all pairs of left and right columns
    for left in range(cols):
        # temp[i] = sum of row i from column left to right
        temp = [0] * rows

        for right in range(left, cols):
            # Add current column to running sums
            for i in range(rows):
                temp[i] += matrix[i][right]

            # Apply Kadane on this 1D array
            current_max = kadane_max(temp)
            max_sum = max(max_sum, current_max)

    return max_sum
```

---

## Edge Cases

```python
# All negative
[-3, -1, -2] → -1 (must take at least one element)

# Single element
[5] → 5
[-5] → -5

# All positive
[1, 2, 3, 4] → 10 (entire array)

# Contains zero
[1, 0, 2] → 3 (for sum) or 0 (for product if including 0)

# Empty array
[] → 0 or error (clarify with interviewer)
```

---

## DP Perspective

Kadane's algorithm is a space-optimized DP:

```
dp[i] = maximum subarray sum ending at index i

dp[i] = max(arr[i], dp[i-1] + arr[i])

answer = max(dp[0], dp[1], ..., dp[n-1])

Space optimization: only need dp[i-1] → single variable
```

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Maximum Subarray | Medium | Basic Kadane |
| 2 | Maximum Product Subarray | Medium | Track min/max |
| 3 | Maximum Sum Circular Subarray | Medium | Total - min |
| 4 | House Robber | Medium | No adjacent |
| 5 | House Robber II | Medium | Circular + no adjacent |
| 6 | Best Time to Buy and Sell Stock | Easy | Kadane variation |
| 7 | Maximum Sum Rectangle (2D) | Hard | 2D compression |
| 8 | Maximum Subarray Sum with One Deletion | Medium | Track with/without deletion |

---

## Key Takeaways

1. **At each position**: extend or start fresh
2. **Track running sum** and reset when it becomes negative
3. **For products**: track both max and min (negatives flip)
4. **For circular**: max(normal, total - min)
5. **Space-optimized DP**: only need previous state

---

## Next: [09-string-basics.md](./09-string-basics.md)

Learn string fundamentals and manipulation techniques.
