# Solution: Histogram Problems Practice Problems

## Problem 1: Largest Rectangle in Histogram
### Problem Statement
Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.

### Constraints
- `1 <= heights.length <= 10^5`
- `0 <= heights[i] <= 10^4`

### Example
Input: `heights = [2,1,5,6,2,3]`
Output: `10`

### Python Implementation
```python
def largestRectangleArea(heights: list[int]) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    stack = [] # indices
    max_area = 0
    heights.append(0) # sentinel

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    heights.pop() # remove sentinel
    return max_area
```

---

## Problem 2: Maximal Rectangle
### Problem Statement
Given a `rows x cols` binary `matrix` filled with `0`'s and `1`'s, find the largest rectangle containing only `1`'s and return its area.

### Constraints
- `rows == matrix.length`
- `cols == matrix[i].length`
- `1 <= row, cols <= 200`
- `matrix[i][j]` is `'0'` or `'1'`.

### Example
Input: `matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]`
Output: `6`

### Python Implementation
```python
def maximalRectangle(matrix: list[list[str]]) -> int:
    """
    Time Complexity: O(rows * cols)
    Space Complexity: O(cols)
    """
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix[0])
    heights = [0] * n
    max_area = 0

    def get_max_area(heights):
        stack = []
        res = 0
        h_copy = heights + [0]
        for i, h in enumerate(h_copy):
            while stack and h_copy[stack[-1]] >= h:
                height = h_copy[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                res = max(res, height * width)
            stack.append(i)
        return res

    for row in matrix:
        for i in range(n):
            if row[i] == '1':
                heights[i] += 1
            else:
                heights[i] = 0
        max_area = max(max_area, get_max_area(heights))

    return max_area
```

---

## Problem 3: Trapping Rain Water
### Problem Statement
Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

### Constraints
- `n == height.length`
- `1 <= n <= 2 * 10^4`
- `0 <= height[i] <= 10^5`

### Example
Input: `height = [0,1,0,2,1,0,1,3,2,1,2,1]`
Output: `6`

### Python Implementation
```python
def trap(height: list[int]) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not height:
        return 0

    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    res = 0

    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            res += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            res += right_max - height[right]

    return res
```

---

## Problem 4: Container With Most Water
### Problem Statement
You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i`th line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

### Constraints
- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`

### Example
Input: `height = [1,8,6,2,5,4,8,3,7]`
Output: `49`

### Python Implementation
```python
def maxArea(height: list[int]) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    left, right = 0, len(height) - 1
    max_area = 0

    while left < right:
        curr_area = min(height[left], height[right]) * (right - left)
        max_area = max(max_area, curr_area)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_area
```
