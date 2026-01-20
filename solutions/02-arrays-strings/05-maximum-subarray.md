# Maximum Subarray (Kadane's Algorithm)

## Problem Statement

Given an integer array `nums`, find the subarray with the largest sum and return its sum.

A subarray is a contiguous part of an array.

**Example:**
```
Input: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6
Explanation: Subarray [4, -1, 2, 1] has the largest sum = 6.
```

## Building Intuition

### Why This Works

Kadane's algorithm is based on a simple observation: at each position, you have exactly two choices. Either extend the current subarray by including this element, or start a fresh subarray beginning at this element. The decision is easy: if the previous subarray sum is negative, it can only hurt you, so start fresh. If it is positive (or zero), it can only help (or not hurt), so extend.

Mathematically, `current_sum = max(num, current_sum + num)`. If `current_sum` before adding `num` is negative, then `num > current_sum + num`, so we start fresh. Otherwise, we extend.

The global maximum is tracked separately because the best subarray might end somewhere in the middle of the array, not at the end. After processing each element, we check if we have a new global best.

### How to Discover This

When asked for the "best contiguous subsequence," consider: what is the best answer ending at each position? This is a form of dynamic programming where `dp[i]` = "best subarray sum ending exactly at index `i`".

The recurrence `dp[i] = max(nums[i], dp[i-1] + nums[i])` follows naturally: either the best subarray ending at `i` includes previous elements (extend), or it is just `nums[i]` itself (start fresh). Kadane's is just this DP with space optimized from O(n) to O(1).

### Pattern Recognition

This is **Kadane's Algorithm**, a special case of the **Optimal Substructure** DP pattern. It appears in:
- Maximum subarray sum (this problem)
- Maximum product subarray (track both max and min due to sign flipping)
- Best time to buy and sell stock (equivalent formulation)
- Circular array variants (combine with min subarray)
- Any problem asking for optimal contiguous segment

## When NOT to Use

- **When the subarray has size constraints**: If you need exactly `k` elements or at least `k` elements, Kadane's needs modification or a sliding window approach.
- **When you need the actual subarray, not just the sum**: Kadane's can be extended to track indices, but the basic version only returns the value.
- **When there are additional constraints on elements**: If only certain elements can be included (e.g., no two adjacent), you need a different DP formulation.
- **When the problem involves products instead of sums**: Maximum product subarray requires tracking both max and min products because negatives can flip signs.

## Approach

### Kadane's Algorithm
The key insight: At each position, we decide whether to:
1. **Extend** the previous subarray by including current element
2. **Start fresh** from current element (if previous sum is negative)

We keep track of:
- `current_sum`: Best sum ending at current position
- `max_sum`: Best sum seen so far

**Decision rule:** `current_sum = max(num, current_sum + num)`

```
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

i=0: num=-2, current=max(-2, -2)=-2, max=-2
i=1: num=1,  current=max(1, -2+1=-1)=1, max=1
i=2: num=-3, current=max(-3, 1-3=-2)=-2, max=1
i=3: num=4,  current=max(4, -2+4=2)=4, max=4
i=4: num=-1, current=max(-1, 4-1=3)=3, max=4
i=5: num=2,  current=max(2, 3+2=5)=5, max=5
i=6: num=1,  current=max(1, 5+1=6)=6, max=6
i=7: num=-5, current=max(-5, 6-5=1)=1, max=6
i=8: num=4,  current=max(4, 1+4=5)=5, max=6

Result: 6
```

## Implementation

```python
def max_subarray(nums: list[int]) -> int:
    """
    Find maximum subarray sum using Kadane's algorithm.

    Time: O(n) - single pass
    Space: O(1) - only tracking two variables
    """
    current_sum = nums[0]
    max_sum = nums[0]

    for num in nums[1:]:
        # Either extend previous subarray or start fresh
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)

    return max_sum


def max_subarray_with_indices(nums: list[int]) -> tuple[int, int, int]:
    """
    Return (max_sum, start_index, end_index).
    """
    current_sum = nums[0]
    max_sum = nums[0]

    start = 0
    temp_start = 0
    end = 0

    for i in range(1, len(nums)):
        if nums[i] > current_sum + nums[i]:
            current_sum = nums[i]
            temp_start = i
        else:
            current_sum = current_sum + nums[i]

        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i

    return max_sum, start, end


def max_subarray_dp(nums: list[int]) -> int:
    """
    DP formulation (same as Kadane's, explicit DP array).

    dp[i] = maximum sum of subarray ending at index i
    dp[i] = max(nums[i], dp[i-1] + nums[i])
    """
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]

    for i in range(1, n):
        dp[i] = max(nums[i], dp[i-1] + nums[i])

    return max(dp)
```

## Complexity Analysis

| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n) | Single pass through array |
| Space | O(1) | Only two variables |

## Edge Cases

1. **All negative**: `[-3, -2, -1]` → Return -1 (largest single element)
2. **Single element**: `[5]` → Return 5
3. **All positive**: Sum of entire array
4. **Mix of positive/negative**: Kadane's handles this
5. **Zeros in array**: Treated as any other element
6. **Large values**: Watch for integer overflow in other languages

## Common Mistakes

1. **Initializing max_sum to 0**: Wrong for all-negative arrays
2. **Not handling single element**: Edge case
3. **Off-by-one in loop**: Start from index 1, not 0
4. **Returning current_sum instead of max_sum**: Track global maximum

## Variations

### Maximum Circular Subarray
```python
def max_subarray_circular(nums: list[int]) -> int:
    """
    Array is circular - can wrap around.

    Answer is either:
    1. Normal max subarray (no wrap)
    2. Total sum - min subarray (wrap case)

    Edge case: All negative → can't use wrap case
    """
    total = sum(nums)
    max_sum = max_subarray(nums)

    # Find min subarray (to exclude from wrap)
    current_min = nums[0]
    min_sum = nums[0]
    for num in nums[1:]:
        current_min = min(num, current_min + num)
        min_sum = min(min_sum, current_min)

    # If all negative, wrap case gives total - min_sum = 0
    # which is wrong, so only use max_sum
    if min_sum == total:
        return max_sum

    return max(max_sum, total - min_sum)
```

### Maximum Product Subarray
```python
def max_product(nums: list[int]) -> int:
    """
    Track both max and min (negatives can flip).
    """
    max_prod = min_prod = result = nums[0]

    for num in nums[1:]:
        candidates = (num, max_prod * num, min_prod * num)
        max_prod = max(candidates)
        min_prod = min(candidates)
        result = max(result, max_prod)

    return result
```

### Minimum Subarray Sum
```python
def min_subarray(nums: list[int]) -> int:
    """Same as max, but track minimum."""
    current = min_sum = nums[0]

    for num in nums[1:]:
        current = min(num, current + num)
        min_sum = min(min_sum, current)

    return min_sum
```

## Divide and Conquer Approach

```python
def max_subarray_divide_conquer(nums: list[int]) -> int:
    """
    Divide and conquer approach.

    Time: O(n log n)
    Space: O(log n) recursion stack
    """
    def helper(left: int, right: int) -> int:
        if left == right:
            return nums[left]

        mid = (left + right) // 2

        # Max sum crossing the midpoint
        left_sum = float('-inf')
        curr = 0
        for i in range(mid, left - 1, -1):
            curr += nums[i]
            left_sum = max(left_sum, curr)

        right_sum = float('-inf')
        curr = 0
        for i in range(mid + 1, right + 1):
            curr += nums[i]
            right_sum = max(right_sum, curr)

        cross_sum = left_sum + right_sum

        return max(
            helper(left, mid),      # Left half
            helper(mid + 1, right), # Right half
            cross_sum               # Crossing middle
        )

    return helper(0, len(nums) - 1)
```

## Related Problems

- **Maximum Product Subarray** - Product instead of sum
- **Maximum Sum Circular Subarray** - Circular array
- **Best Time to Buy and Sell Stock** - Same concept, different framing
- **Shortest Subarray with Sum at Least K** - Deque approach
- **Maximum Subarray Sum with One Deletion** - DP variant
