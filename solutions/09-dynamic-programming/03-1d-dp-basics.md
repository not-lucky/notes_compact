# 1D DP Basics Solutions

## Problem: Min Cost Climbing Stairs
You are given an integer array `cost` where `cost[i]` is the cost of `i-th` step on a staircase. Once you pay the cost, you can either climb one or two steps. You can either start from the step with index 0, or the step with index 1. Return the minimum cost to reach the top of the floor.

### Constraints
- 2 <= cost.length <= 1000
- 0 <= cost[i] <= 999

### Examples
- Input: cost = [10, 15, 20] -> Output: 15
- Input: cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1] -> Output: 6

### Implementation

```python
def min_cost_climbing_stairs(cost: list[int]) -> int:
    """
    Minimum cost to reach the top.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    n = len(cost)
    # Can start at index 0 or 1
    prev2, prev1 = cost[0], cost[1]

    for i in range(2, n):
        curr = cost[i] + min(prev1, prev2)
        prev2, prev1 = prev1, curr

    # To reach the floor above the last step, we can come from either of the last two steps
    return min(prev1, prev2)
```

## Problem: Maximum Subarray (Kadane's Algorithm)
Given an integer array `nums`, find the subarray with the largest sum, and return its sum.

### Constraints
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

### Examples
- Input: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4] -> Output: 6 (Subarray: [4, -1, 2, 1])
- Input: nums = [5, 4, -1, 7, 8] -> Output: 23

### Implementation

```python
def max_subarray(nums: list[int]) -> int:
    """
    Finds maximum subarray sum using Kadane's algorithm.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    if not nums:
        return 0

    max_sum = curr_sum = nums[0]
    for i in range(1, len(nums)):
        curr_sum = max(nums[i], curr_sum + nums[i])
        max_sum = max(max_sum, curr_sum)
    return max_sum
```

## Problem: Decode Ways
A message containing letters from A-Z can be encoded into numbers using the mapping: 'A' -> "1", 'B' -> "2", ..., 'Z' -> "26". To decode an encoded message, all the digits must be grouped then mapped back into letters. Given a string `s` containing only digits, return the number of ways to decode it.

### Constraints
- 1 <= s.length <= 100
- `s` contains only digits and may contain leading zero(s).

### Examples
- Input: s = "12" -> Output: 2 ("AB" or "L")
- Input: s = "226" -> Output: 3 ("BZ", "VF", or "BBF")

### Implementation

```python
def num_decodings(s: str) -> int:
    """
    Counts decoding ways using space-optimized 1D DP.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    if not s or s[0] == '0':
        return 0

    n = len(s)
    # prev2: dp[i-2], prev1: dp[i-1]
    prev2, prev1 = 1, 1

    for i in range(2, n + 1):
        curr = 0
        # Check single digit
        if s[i-1] != '0':
            curr += prev1

        # Check two digits
        two_digit = int(s[i-2:i])
        if 10 <= two_digit <= 26:
            curr += prev2

        prev2, prev1 = prev1, curr

    return prev1
```
