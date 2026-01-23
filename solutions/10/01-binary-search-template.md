# Binary Search

## Practice Problems

### 1. Binary Search
**Difficulty:** Easy
**Concept:** Standard template

```python
from typing import List

def search(nums: List[int], target: int) -> int:
    """
    Standard binary search.
    Time: O(log n)
    Space: O(1)
    """
    l, r = 0, len(nums) - 1
    while l <= r:
        m = l + (r - l) // 2
        if nums[m] == target:
            return m
        elif nums[m] < target:
            l = m + 1
        else:
            r = m - 1
    return -1
```

### 2. Search a 2D Matrix
**Difficulty:** Medium
**Concept:** 2D mapping to 1D

```python
def search_matrix(matrix: List[List[int]], target: int) -> bool:
    """
    Binary search on a sorted matrix.
    Time: O(log(m * n))
    Space: O(1)
    """
    if not matrix: return False
    rows, cols = len(matrix), len(matrix[0])
    l, r = 0, rows * cols - 1
    while l <= r:
        m = l + (r - l) // 2
        # Map 1D index to 2D
        row, col = m // cols, m % cols
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] < target:
            l = m + 1
        else:
            r = m - 1
    return False
```

### 3. Find Minimum in Rotated Sorted Array
**Difficulty:** Medium
**Concept:** Modified binary search

```python
def find_min(nums: List[int]) -> int:
    """
    Finds pivot in rotated sorted array.
    Time: O(log n)
    Space: O(1)
    """
    l, r = 0, len(nums) - 1
    while l < r:
        m = l + (r - l) // 2
        if nums[m] > nums[r]:
            l = m + 1
        else:
            r = m
    return nums[l]
```

### 4. Search in Rotated Sorted Array
**Difficulty:** Medium
**Concept:** Two-case logic

```python
def search_rotated(nums: List[int], target: int) -> int:
    """
    Search in rotated sorted array.
    Time: O(log n)
    Space: O(1)
    """
    l, r = 0, len(nums) - 1
    while l <= r:
        m = l + (r - l) // 2
        if nums[m] == target: return m

        # Left side sorted
        if nums[l] <= nums[m]:
            if nums[l] <= target < nums[m]:
                r = m - 1
            else:
                l = m + 1
        # Right side sorted
        else:
            if nums[m] < target <= nums[r]:
                l = m + 1
            else:
                r = m - 1
    return -1
```

### 5. Find First and Last Position of Element
**Difficulty:** Medium
**Concept:** Boundary finding

```python
def search_range(nums: List[int], target: int) -> List[int]:
    """
    Finds first and last occurrences of target.
    Time: O(log n)
    Space: O(1)
    """
    def find_bound(is_first):
        l, r = 0, len(nums) - 1
        bound = -1
        while l <= r:
            m = l + (r - l) // 2
            if nums[m] == target:
                bound = m
                if is_first: r = m - 1
                else: l = m + 1
            elif nums[m] < target:
                l = m + 1
            else:
                r = m - 1
        return bound

    return [find_bound(True), find_bound(False)]
```

### 6. Koko Eating Bananas
**Difficulty:** Medium
**Concept:** Binary search on answer space

```python
import math

def min_eating_speed(piles: List[int], h: int) -> int:
    """
    Binary search for minimum k such that all bananas eaten within h hours.
    Time: O(n log(max_p))
    Space: O(1)
    """
    l, r = 1, max(piles)
    res = r

    while l <= r:
        k = l + (r - l) // 2
        hours = 0
        for p in piles:
            hours += math.ceil(p / k)

        if hours <= h:
            res = k
            r = k - 1
        else:
            l = k + 1
    return res
```
