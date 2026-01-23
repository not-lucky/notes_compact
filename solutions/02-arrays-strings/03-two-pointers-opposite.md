# Solution: Two Pointers Opposite Direction

## Problem 1: Two Sum II - Input Array Is Sorted
Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific `target` number.

### Python Implementation
```python
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    left, right = 0, len(numbers) - 1
    while left < right:
        curr_sum = numbers[left] + numbers[right]
        if curr_sum == target:
            return [left + 1, right + 1]
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    return []
```

---

## Problem 2: Container With Most Water
You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i-th` line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

### Python Implementation
```python
def max_area(height: list[int]) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    left, right = 0, len(height) - 1
    max_w = 0
    while left < right:
        w = right - left
        h = min(height[left], height[right])
        max_w = max(max_w, w * h)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_w
```
