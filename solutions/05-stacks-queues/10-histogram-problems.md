# Histogram Problems - Practice Solutions

This file provides optimal Python solutions and explanations for the practice problems listed in the Histogram Problems notes.

## 1. Largest Rectangle in Histogram
**Problem Statement**: Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.

### Examples & Edge Cases
- **Example 1**: `heights = [2,1,5,6,2,3]` -> `10` (height 5 and width 2)
- **Edge Case**: All bars have the same height.
- **Edge Case**: Strictly increasing or decreasing heights.
- **Edge Case**: Empty array or single element.

### Optimal Python Solution
```python
def largestRectangleArea(heights: list[int]) -> int:
    # Use a stack to maintain indices of bars in monotonic increasing order
    stack = [-1] # Initialize with -1 to simplify width calculation
    max_area = 0
    # Append a 0 sentinel to the end to ensure we process all remaining bars
    heights.append(0)

    for i, h in enumerate(heights):
        # When we find a bar shorter than the top of the stack
        while heights[stack[-1]] > h:
            # The bar at the top of stack is the 'height' of a potential rectangle
            height = heights[stack.pop()]
            # The current index 'i' is the right boundary (exclusive)
            # The new stack top index is the left boundary (exclusive)
            width = i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    # Clean up sentinel for consistency
    heights.pop()
    return max_area
```

### Explanation
We use a Monotonic Increasing Stack. For each bar, we want to find the first bar on its left and right that is shorter than it.
1. When we encounter a bar `h` shorter than the top of the stack, it means the bar at `stack[-1]` has found its **right boundary** (the current index `i`).
2. Its **left boundary** is the index now at the top of the stack after the pop.
3. The width is `(right_index - left_index - 1)`.
This approach ensures we check every bar as the "minimum height" of a rectangle exactly once.

### Complexity Analysis
- **Time Complexity**: O(n), where n is the number of bars. Each bar index is pushed and popped exactly once.
- **Space Complexity**: O(n), for the stack in the worst case (e.g., strictly increasing heights).

---

## 2. Maximal Rectangle
**Problem Statement**: Given a `rows x cols` binary `matrix` filled with `0`'s and `1`'s, find the largest rectangle containing only `1`'s and return its area.

### Optimal Python Solution
```python
def maximalRectangle(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]: return 0

    cols = len(matrix[0])
    heights = [0] * cols
    max_area = 0

    for row in matrix:
        # Update current histogram heights for the current row
        for j in range(cols):
            if row[j] == '1':
                heights[j] += 1
            else:
                heights[j] = 0

        # Calculate largest rectangle for the current histogram
        max_area = max(max_area, self.largestRectangleArea(heights))

    return max_area

def largestRectangleArea(heights):
    stack = [-1]
    max_area = 0
    # Create copy to avoid modifying original or use pop() later
    copy = heights + [0]
    for i, h in enumerate(copy):
        while copy[stack[-1]] > h:
            height = copy[stack.pop()]
            width = i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area
```

### Explanation
This problem is a 2D extension of "Largest Rectangle in Histogram". We process the matrix row by row. For each row, we treat it as the base of a histogram. The height of the bar at column `j` is the number of consecutive `1`s ending at the current row. We then solve the 1D problem for each row.

---

## 3. Trapping Rain Water
**Problem Statement**: Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

### Optimal Python Solution (Monotonic Stack)
```python
def trap(height: list[int]) -> int:
    stack = [] # Monotonic decreasing stack of indices
    water = 0

    for i, h in enumerate(height):
        # When we find a bar taller than the top, we might trap water
        while stack and height[stack[-1]] < h:
            bottom_idx = stack.pop()
            if not stack: break # No left wall

            left_idx = stack[-1]
            distance = i - left_idx - 1
            # Trapped water height is limited by the shorter of the two walls
            bounded_height = min(height[left_idx], h) - height[bottom_idx]
            water += distance * bounded_height
        stack.append(i)

    return water
```

### Explanation
We use a monotonic decreasing stack. When we find a taller bar than the current top, it acts as a "right wall". The element we pop is the "bottom" of a pool. The new stack top is the "left wall". We calculate water level-by-level horizontally.

---

## 4. Container With Most Water
**Problem Statement**: Find two lines that together with the x-axis form a container, such that the container contains the most water.

### Optimal Python Solution
```python
def maxArea(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    max_area = 0

    while left < right:
        # Area = width * min(h_left, h_right)
        area = (right - left) * min(height[left], height[right])
        max_area = max(max_area, area)

        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_area
```

---

## 5. Maximal Square
**Problem Statement**: Given an `m x n` binary `matrix`, find the largest square containing only `1`'s and return its area.

### Optimal Python Solution (Dynamic Programming)
```python
def maximalSquare(matrix: list[list[str]]) -> int:
    if not matrix: return 0
    rows, cols = len(matrix), len(matrix[0])
    dp = [[0] * (cols + 1) for _ in range(rows + 1)]
    max_side = 0

    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == '1':
                # Current max square side depends on top, left, and top-left
                dp[r+1][c+1] = min(dp[r][c+1], dp[r+1][c], dp[r][c]) + 1
                max_side = max(max_side, dp[r+1][c+1])

    return max_side * max_side

---

## 6. Largest Rectangle Containing Only 1s
**Problem Statement**: This is identical to the Maximal Rectangle problem. Given a binary matrix, find the largest rectangle filled with 1s.

### Optimal Python Solution
```python
def maximalRectangle(matrix: list[list[str]]) -> int:
    # Refer to Solution 2 (Maximal Rectangle) for implementation details.
    # It uses the Histogram algorithm row-by-row.
    pass
```
```
