# Solution: Frequency Counting

## Problem Statement
Given an array of integers `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.

## Constraints
- `1 <= nums.length <= 10^5`
- `k` is in the range `[1, the number of unique elements in the array]`.
- It is guaranteed that the answer is unique.

## Example (Input/Output)
```
Input: nums = [1, 1, 1, 2, 2, 3], k = 2
Output: [1, 2]
```

## Python Implementation
```python
import heapq
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    Find k most frequent elements.

    Time: O(n log k) with heap
    Space: O(n) for Counter and heap
    """
    if k == len(nums):
        return nums

    # 1. build hash map : character and how often it appears
    # O(N) time
    count = Counter(nums)

    # 2. keep k top frequent elements in a heap
    # O(N log k) time
    return heapq.nlargest(k, count.keys(), key=count.get)
```
