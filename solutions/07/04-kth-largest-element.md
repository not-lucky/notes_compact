# Kth Largest Element

## Practice Problems

### 1. Kth Largest Element in an Array (Heap)
**Difficulty:** Medium
**Concept:** Min heap of size k

```python
import heapq
from typing import List

def find_kth_largest_heap(nums: List[int], k: int) -> int:
    """
    Find kth largest element using a min heap.

    >>> find_kth_largest_heap([3,2,1,5,6,4], 2)
    5
    >>> find_kth_largest_heap([3,2,3,1,2,4,5,5,6], 4)
    4

    Time: O(n log k)
    Space: O(k)
    """
    return heapq.nlargest(k, nums)[-1]
```

### 2. Kth Largest Element (QuickSelect)
**Difficulty:** Medium
**Concept:** QuickSelect (O(n) average)

```python
import random

def find_kth_largest_quickselect(nums: List[int], k: int) -> int:
    """
    Find kth largest element using QuickSelect.

    >>> find_kth_largest_quickselect([3,2,1,5,6,4], 2)
    5
    >>> find_kth_largest_quickselect([3,2,3,1,2,4,5,5,6], 4)
    4

    Time: O(n) average, O(n^2) worst
    Space: O(1)
    """
    target = len(nums) - k
    left, right = 0, len(nums) - 1

    while left <= right:
        pivot_idx = random.randint(left, right)
        pivot = nums[pivot_idx]
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        store = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[i], nums[store] = nums[store], nums[i]
                store += 1

        nums[store], nums[right] = nums[right], nums[store]

        if store == target:
            return nums[store]
        elif store < target:
            left = store + 1
        else:
            right = store - 1
    return -1
```
