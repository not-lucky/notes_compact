# Longest Increasing Subsequence Solutions

## Problem: Longest Increasing Subsequence
Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

### Constraints
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4

### Examples
- Input: [10, 9, 2, 5, 3, 7, 101, 18] -> Output: 4 ([2, 3, 7, 18])
- Input: [0, 1, 0, 3, 2, 3] -> Output: 4 ([0, 1, 2, 3])

### Implementation

```python
import bisect

def length_of_lis(nums: list[int]) -> int:
    """
    Finds the length of LIS using binary search (patience sorting).
    Time complexity: O(n log n)
    Space complexity: O(n)
    """
    if not nums:
        return 0

    tails = []
    for num in nums:
        idx = bisect.bisect_left(tails, num)
        if idx == len(tails):
            tails.append(num)
        else:
            tails[idx] = num
    return len(tails)

def length_of_lis_dp(nums: list[int]) -> int:
    """
    Classic O(n^2) DP approach.
    Time complexity: O(n^2)
    Space complexity: O(n)
    """
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

## Problem: Russian Doll Envelopes
You are given a 2D array of integers `envelopes` where `envelopes[i] = [wi, hi]` represents the width and the height of an envelope. One envelope can fit into another if and only if both the width and height of one envelope are greater than the other envelope's width and height. Return the maximum number of envelopes you can Russian doll (i.e., put one inside another).

### Implementation

```python
import bisect

def max_envelopes(envelopes: list[list[int]]) -> int:
    """
    Finds maximum Russian doll envelopes using sorting + LIS.
    Time complexity: O(n log n)
    Space complexity: O(n)
    """
    # Sort by width ascending, then by height descending
    # Descending height ensures we don't pick two envelopes with the same width
    envelopes.sort(key=lambda x: (x[0], -x[1]))

    heights = [e[1] for e in envelopes]
    tails = []
    for h in heights:
        idx = bisect.bisect_left(tails, h)
        if idx == len(tails):
            tails.append(h)
        else:
            tails[idx] = h
    return len(tails)
```
