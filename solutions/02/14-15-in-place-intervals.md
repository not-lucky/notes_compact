# Solution: In-Place and Intervals

## Problem 1: Rotate Image
You are given an `n x n` 2D matrix representing an image, rotate the image by 90 degrees (clockwise). You have to rotate the image in-place.

### Python Implementation
```python
def rotate(matrix: list[list[int]]) -> None:
    """
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    n = len(matrix)
    # Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse rows
    for row in matrix:
        row.reverse()
```

---

## Problem 2: Merge Intervals
Given an array of intervals where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

### Python Implementation
```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if not intervals: return []
    intervals.sort()
    res = [intervals[0]]
    for i in range(1, len(intervals)):
        if intervals[i][0] <= res[-1][1]:
            res[-1][1] = max(res[-1][1], intervals[i][1])
        else:
            res.append(intervals[i])
    return res
```

---

## Problem 3: Next Permutation
Implement next permutation, which rearranges numbers into the lexicographically next greater permutation of numbers.

### Python Implementation
```python
def next_permutation(nums: list[int]) -> None:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    n = len(nums)
    i = n - 2
    while i >= 0 and nums[i] >= nums[i+1]:
        i -= 1

    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]

    # Reverse suffix
    l, r = i + 1, n - 1
    while l < r:
        nums[l], nums[r] = nums[r], nums[l]
        l += 1
        r -= 1
```
