# Histogram Problems

## Practice Problems

### 1. Largest Rectangle in Histogram
**Difficulty:** Hard
**Key Technique:** Monotonic increasing stack + Sentinel

```python
def largest_rectangle_area(heights: list[int]) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    heights.append(0)
    stack = [-1]
    res = 0
    for i in range(len(heights)):
        while heights[i] < heights[stack[-1]]:
            h = heights[stack.pop()]
            w = i - stack[-1] - 1
            res = max(res, h * w)
        stack.append(i)
    heights.pop()
    return res
```

### 2. Maximal Rectangle
**Difficulty:** Hard
**Key Technique:** Histogram per row + Largest Rectangle in Histogram

```python
def maximal_rectangle(matrix: list[list[str]]) -> int:
    """
    Time: O(R * C)
    Space: O(C)
    """
    if not matrix: return 0
    cols = len(matrix[0])
    heights = [0] * cols
    res = 0
    for row in matrix:
        for i in range(cols):
            heights[i] = heights[i] + 1 if row[i] == "1" else 0
        res = max(res, largest_rectangle_area(heights))
    return res
```

### 3. Trapping Rain Water
**Difficulty:** Hard
**Key Technique:** Monotonic decreasing stack or Two pointers

```python
def trap(height: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    l, r = 0, len(height) - 1
    l_max, r_max = 0, 0
    res = 0
    while l < r:
        if height[l] < height[r]:
            if height[l] >= l_max: l_max = height[l]
            else: res += l_max - height[l]
            l += 1
        else:
            if height[r] >= r_max: r_max = height[r]
            else: res += r_max - height[r]
            r -= 1
    return res
```

### 4. Container With Most Water
**Difficulty:** Medium
**Key Technique:** Two pointers (Moving shorter line)

```python
def max_area(height: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    l, r = 0, len(height) - 1
    res = 0
    while l < r:
        h = min(height[l], height[r])
        res = max(res, h * (r - l))
        if height[l] < height[r]: l += 1
        else: r -= 1
    return res
```
