# Kadane's Algorithm

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Kadane's algorithm finds the maximum subarray sum in a tight bound of $\Theta(n)$ time using a simple but powerful insight: at each position, either extend the current subarray or start fresh. This space-optimized dynamic programming solution is a cornerstone of algorithmic problem-solving, operating in strict $\Theta(1)$ auxiliary space.

## Building Intuition

**Why does "extend or restart" give the optimal answer?**

The key insight is **local optimality leads to global optimality**. At each position, we make the locally optimal choice:

1. **The Core Decision**: At position `i`, the maximum subarray ending at `i` either:
   - Includes the previous maximum subarray (extend): `prev_max + arr[i]`
   - Starts fresh at `i` (restart): `arr[i]`
   - We take whichever is larger: `max(arr[i], prev_max + arr[i])`

2. **Why This Works**: If the previous maximum subarray has a positive sum, extending it can only help (positive + anything increases the anything). If it has a negative sum, extending it hurts—we're better off starting fresh.

3. **Simpler Form**: `current_max = max(arr[i], current_max + arr[i])` simplifies to: "If `current_max` is negative, reset to `arr[i]`; otherwise, add `arr[i]` to it."

**Mental Model**: Imagine you're walking down a road collecting coins (positive) and paying tolls (negative). Your pockets hold your current accumulated wealth (your current subarray). At each step, ask: "Is the accumulated wealth in my pockets helping me or hurting me?" If you're in debt (a negative sum), you are better off emptying your pockets, declaring bankruptcy, and starting over with the current coin or toll. If you have savings (a positive sum), keep going and add the current coin or toll to your pockets.

**Visual Trace**:

```text
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
4. **Length Constraints**: If subarray must be at least length `k` or at most length `m`, standard Kadane's doesn't handle this directly. Need sliding window + Kadane's hybrid.
5. **Multiple Disjoint Subarrays**: "Find 2 non-overlapping subarrays with maximum sum" needs a different approach (left-max and right-max arrays).
6. **All Elements Are Negative**: Kadane's still works (returns the least negative), but clarify with interviewer: "Is empty subarray allowed?" If yes, answer is `0`.

**Red Flags:**

- "Subsequence" (not subarray) → Different DP
- "Product" (not sum) → Track min and max
- "Exactly `k` elements" → Sliding window or constrained DP
- "Two disjoint subarrays" → Left/right max arrays

---

## Interview Context & Complexity Precision

Kadane's algorithm solves the Maximum Subarray problem in $\Theta(n)$ time. This is a classic interview problem because:

- It tests dynamic programming intuition.
- Has many variations (product, circular, 2D).
- Simple but easy to get wrong.
- Foundation for more complex DP problems.

**Python Specifics**:
- **Dynamic Arrays**: Python lists are dynamic arrays. While appending to them is amortized $\Theta(1)$, building a subarray item-by-item during Kadane's would require memory reallocation and cost $O(n)$ space. By only tracking sums (or indices), we maintain strict $\Theta(1)$ space.
- **String/List Concatenation**: If the problem asked to return the subarray as a string, avoid string concatenation (`+=`) in a loop, as it results in $O(n^2)$ time due to memory churn. Use `.join()` or track indices instead.
- **Hash Maps**: If a variation requires tracking seen sums (like in prefix sum approaches to subarray problems), remember that Python dictionary insertions/lookups are amortized $\Theta(1)$ but worst-case $O(n)$ due to hash collisions.
- **Recursive Call Stack**: None of these standard iterative versions utilize recursion, so there is no hidden $\Theta(n)$ space complexity on the call stack, guaranteeing an exact $\Theta(1)$ space footprint.

---

## Template: Maximum Subarray Sum

### Problem: Maximum Subarray
**Problem Statement:** Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

**Why it works:**
At each index `i`, we decide whether to include the previous subarray or start a new one.
1. `current_sum_at_i = max(nums[i], current_sum_at_i-1 + nums[i])`.
2. If `current_sum_at_i-1` is positive, adding it to `nums[i]` will always result in a larger sum than `nums[i]` alone.
3. If it's negative, it only drags down the potential sum, so we're better off starting fresh with `nums[i]`.
This greedy approach ensures we find the global maximum in a single pass.

```python
def max_subarray(arr: list[int]) -> int:
    """
    Find the maximum sum of any contiguous subarray.

    Time Complexity: $\Theta(n)$ - tight bound, single pass.
    Space Complexity: $\Theta(1)$ - tight bound, strictly uses scalar variables.

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

---

## Template: Maximum Subarray with Indices

If you need the actual subarray, track the indices. *Do not append elements to a new list during the loop or use string concatenation (`+=`), as that wastes memory and can degrade performance.* Python lists are dynamic arrays, so simply track the bounds and slice the array at the end (`arr[start:end+1]`) to get the subarray in $\Theta(k)$ time (where $k$ is the length of the subarray).

```python
def max_subarray_with_indices(arr: list[int]) -> tuple[int, int, int]:
    """
    Return (max_sum, start_index, end_index).

    Time Complexity: $\Theta(n)$
    Space Complexity: $\Theta(1)$
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

### Problem: Maximum Product Subarray
**Problem Statement:** Given an integer array `nums`, find a contiguous non-empty subarray within the array that has the largest product, and return the product.

**Why it works:**
Unlike sums, the product can flip sign when multiplying by a negative number.
1. A very small negative number (large absolute value) can become a very large positive number when multiplied by another negative.
2. Therefore, we track both the `max_prod` and `min_prod` ending at each position.
3. When we encounter a negative number, `max_prod` and `min_prod` effectively swap roles before the multiplication.

```python
def max_product(arr: list[int]) -> int:
    """
    Find the maximum product of any contiguous subarray.

    Key insight: Track both max and min because
    negative × negative = positive.

    Time Complexity: $\Theta(n)$ - tight bound.
    Space Complexity: $\Theta(1)$ - strict auxiliary space, no call stack.

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

```text
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

### Problem: Maximum Sum Circular Subarray
**Problem Statement:** Given a circular integer array `nums` of length `n`, return the maximum possible sum of a non-empty subarray of `nums`.

**Why it works:**
A circular subarray can either be "normal" (middle of the array) or "wrapped" (includes both ends).
1. The "normal" case is solved using standard Kadane's.
2. The "wrapped" case is the `TotalSum - MinimumSubarraySum` (the part we exclude).
3. We calculate both and take the maximum.
Special handling is required if all numbers are negative (where `TotalSum == MinSubarraySum`).

```python
def max_circular_subarray(arr: list[int]) -> int:
    """
    Maximum subarray sum in a circular array.

    Key insight: Answer is either:
    1. Normal max subarray (middle portion)
    2. Total - min subarray (wrapping around)

    Time Complexity: $\Theta(n)$
    Space Complexity: $\Theta(1)$
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

```text
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

### Problem: House Robber
**Problem Statement:** You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. The only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night. Find the maximum money you can rob.

**Why it works:**
At each house `i`, we have two choices:
1. Rob the current house: `Total = house[i] + max_sum_up_to_house_i-2`.
2. Don't rob current house: `Total = max_sum_up_to_house_i-1`.
This is a DP problem where we only need the last two states (`prev1` and `prev2`) to calculate the current maximum, similar to the space-optimized Kadane's.

**Mental Model:** Imagine having to clear items from a conveyor belt, but taking one item triggers a temporary alarm preventing you from taking the immediate next item. You have to evaluate if the current item is worth more than the adjacent one you'd have to skip.

```python
def max_sum_no_adjacent(arr: list[int]) -> int:
    """
    Maximum sum where no two elements are adjacent.
    (House Robber problem)

    Time Complexity: $\Theta(n)$
    Space Complexity: $\Theta(1)$ - DP optimized to two variables.
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

### Problem: Max Sum of Rectangle in a 2D Matrix
**Problem Statement:** Given a 2D matrix, find the maximum sum of a rectangle within it.

**Why it works:**
We can convert this 2D problem into 1D Kadane's.
1. We pick a pair of columns `(L, R)`.
2. We "compress" all columns between `L` and `R` into a single 1D array where each element is the sum of a row between these columns.
3. We run Kadane's on this 1D array to find the best set of rows for this column pair.
4. By iterating over all column pairs ($\Theta(\text{cols}^2)$), we find the global maximum rectangle.

```python
def max_sum_rectangle(matrix: list[list[int]]) -> int:
    """
    Find rectangle with maximum sum in 2D matrix.

    Time Complexity: $\Theta(\text{cols}^2 \times \text{rows})$ - for each column pair, run Kadane
    Space Complexity: $\Theta(\text{rows})$ - temp array to store row sums. No recursion used.

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
            max_sum = max(max_sum, float(current_max))

    return int(max_sum) if max_sum != float('-inf') else 0
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

```text
dp[i] = maximum subarray sum ending at index i

dp[i] = max(arr[i], dp[i-1] + arr[i])

answer = max(dp[0], dp[1], ..., dp[n-1])

Space optimization: only need dp[i-1] → single variable
```

---

## Practice Problems

| #   | Problem                                | Difficulty | Key Variation               |
| --- | -------------------------------------- | ---------- | --------------------------- |
| 1   | Maximum Subarray                       | Medium     | Basic Kadane                |
| 2   | Maximum Product Subarray               | Medium     | Track min/max               |
| 3   | Maximum Sum Circular Subarray          | Medium     | Total - min                 |
| 4   | House Robber                           | Medium     | No adjacent                 |
| 5   | House Robber II                        | Medium     | Circular + no adjacent      |
| 6   | Best Time to Buy and Sell Stock        | Easy       | Kadane variation            |
| 7   | Maximum Sum Rectangle (2D)             | Hard       | 2D compression              |
| 8   | Maximum Subarray Sum with One Deletion | Medium     | Track with/without deletion |

---

## Key Takeaways

1. **At each position**: extend or start fresh.
2. **Track running sum** and reset when it becomes negative.
3. **For products**: track both max and min (negatives flip).
4. **For circular**: `max(normal, total - min)`.
5. **Space-optimized DP**: only need previous state.
6. **Time/Space**: Always $\Theta(n)$ time and $\Theta(1)$ space for the standard 1D form.

---

## Next: [09-string-basics.md](./09-string-basics.md)

Learn string fundamentals and manipulation techniques.
