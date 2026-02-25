# Histogram Problems

> **Prerequisites:** [04-monotonic-stack](./04-monotonic-stack.md)

## Overview

Histogram problems ask you to find the largest rectangle that can be inscribed in a histogram (bar chart). The key insight is that for any rectangle to be valid, it must use one of the bar heights as its limiting height. A monotonic stack efficiently finds, for each bar, how far left and right it can extend before hitting a shorter bar.

## Building Intuition

**Why is finding the largest rectangle hard?**

The brute force approach: For each bar, expand left and right until you hit a shorter bar. This is $\mathcal{O}(n)$ per bar = $\mathcal{O}(n^2)$ total.

**The Key Insight**:

```
For any bar to be the height of a rectangle, it can extend left
until it hits a shorter bar, and extend right until it hits a shorter bar.

If we know the "first shorter bar on the left" and "first shorter bar
on the right" for each bar, we can compute the rectangle width!
```

**Why Monotonic Stack?**

Finding "first shorter on left/right" is exactly what monotonic stacks do!

```
heights = [2, 1, 5, 6, 2, 3]

For bar at index 2 (height 5):
- First shorter on left: index 1 (height 1)
- First shorter on right: index 4 (height 2)
- Width: 4 - 1 - 1 = 2
- Area: 5 × 2 = 10

This is the maximum rectangle!
```

**The Elegant Single-Pass Solution**:

Instead of two passes (one for left boundaries, one for right), we can do it in one pass:

```
Key observation: When we pop a bar from the stack, the current
index is its right boundary, and the new stack top is its left boundary!

heights = [2, 1, 5, 6, 2, 3] + [0] (sentinel)

i=0: push 0, stack=[0]
i=1: height[0]=2 > 1, pop 0
     Right boundary: 1, Left boundary: none → width = 1
     Area = 2 × 1 = 2
     push 1, stack=[1]
i=2: push 2, stack=[1,2]
i=3: push 3, stack=[1,2,3]
i=4: height[3]=6 > 2, pop 3
     Right: 4, Left: 2 → width = 4-2-1 = 1
     Area = 6 × 1 = 6
     height[2]=5 > 2, pop 2
     Right: 4, Left: 1 → width = 4-1-1 = 2
     Area = 5 × 2 = 10  ← Maximum!
     push 4, stack=[1,4]
...
```

**Mental Model**: Imagine you're stacking people by height (increasing from bottom). When a short person joins:

1. All taller people in front get their "rightmost extent" (they can't extend past the short person)
2. Their "leftmost extent" is whoever was behind them in the stack
3. You calculate each tall person's rectangle as they leave

## When NOT to Use This Pattern

The histogram rectangle pattern is wrong when:

1. **Rectangles Don't Need to Be Axis-Aligned**: If rectangles can be rotated, this approach doesn't apply.

2. **Non-Integer Heights**: For continuous functions, you need calculus-based optimization or discretization.

3. **Bars Can Have Gaps**: The standard approach assumes all bars are adjacent. Gaps require modifications.

4. **2D Without Row Structure**: The maximal rectangle in matrix works by treating each row as a histogram. If there's no natural row structure, this doesn't apply.

5. **You Need All Rectangles**: If you need to enumerate all possible rectangles (not just the largest), different approaches are needed.

**Related Problems and Their Approaches**:
| Problem | Approach |
|---------|----------|
| Largest rectangle in histogram | Monotonic stack |
| Maximal rectangle in binary matrix | Per-row histograms + monotonic stack |
| Trapping rain water | Monotonic stack OR two pointers |
| Container with most water | Two pointers (not monotonic stack) |
| Maximal square in binary matrix | Dynamic programming (not stack) |

## Interview Context

Histogram problems are **classic hard problems** at FANG+ companies because:

1. **Monotonic stack mastery**: Tests deep understanding of the pattern
2. **Non-obvious optimization**: Brute force is $\mathcal{O}(n^2)$, optimal is $\mathcal{O}(n)$
3. **Building block**: Foundation for maximal rectangle in matrix
4. **Pattern recognition**: Similar approach applies to trapping water problems

Interviewers use this to assess your ability to apply monotonic stack to geometric problems.

---

## Problem: Largest Rectangle in Histogram

Given an array of integers representing histogram bar heights, find the largest rectangle that can be formed.

```
Example:
heights = [2, 1, 5, 6, 2, 3]

    6
   ┌┐
  5├┤
 ┌┤├┤
 │├┤├┤  3
2│├┤├┤ ┌┤
├┤│├┤├┐├┤
├┤├┤├┤├┤├┤
├┤├┤├┤├┤├┤
└┴┴┴┴┴┴┴┴┘
 0 1 2 3 4 5

Largest rectangle: 5 × 2 = 10 (bars at index 2 and 3)
```

---

## Approach Comparison

| Approach           | Time       | Space    | Notes                           |
| ------------------ | ---------- | -------- | ------------------------------- |
| Brute force        | $\mathcal{O}(n^2)$      | $\mathcal{O}(1)$     | For each bar, expand left/right |
| Divide and conquer | $\mathcal{O}(n \log n)$ | $\mathcal{O}(\log n)$ | Segment tree or recursion       |
| Monotonic stack    | $\mathcal{O}(n)$       | $\mathcal{O}(n)$     | Optimal solution                |

---

## Brute Force Approach

```python
def largest_rectangle_brute(heights: list[int]) -> int:
    """
    For each bar, find how far it can extend left and right.

    Time Complexity: $\mathcal{O}(n^2)$
    Space Complexity: $\mathcal{O}(1)$
    """
    max_area = 0

    for i in range(len(heights)):
        # Find left boundary
        left = i
        while left > 0 and heights[left - 1] >= heights[i]:
            left -= 1

        # Find right boundary
        right = i
        while right < len(heights) - 1 and heights[right + 1] >= heights[i]:
            right += 1

        # Calculate area with bar i as the shortest
        width = right - left + 1
        area = heights[i] * width
        max_area = max(max_area, area)

    return max_area
```

---

## Optimal Solution: Monotonic Stack

```python
def largest_rectangle_in_histogram(heights: list[int]) -> int:
    """
    Find largest rectangle using monotonic increasing stack.

    LeetCode 84: Largest Rectangle in Histogram

    Key insight: For each bar, find the first smaller bar on left and right.
    The rectangle with that bar as height extends from left+1 to right-1.

    Time Complexity: $\mathcal{O}(n)$ - each bar pushed and popped once
    Space Complexity: $\mathcal{O}(n)$ - for stack
    """
    stack = []  # Monotonic increasing stack of indices
    max_area = 0
    n = len(heights)

    for i in range(n + 1):
        # Use 0 as sentinel to pop remaining bars at the end
        h = heights[i] if i < n else 0

        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]

            # Width extends from stack[-1]+1 to i-1
            if stack:
                width = i - stack[-1] - 1
            else:
                width = i

            area = height * width
            max_area = max(max_area, area)

        stack.append(i)

    return max_area


# Example
heights = [2, 1, 5, 6, 2, 3]
print(largest_rectangle_in_histogram(heights))  # 10
```

---

## Step-by-Step Walkthrough

```
heights = [2, 1, 5, 6, 2, 3]
Adding sentinel 0 at end: [2, 1, 5, 6, 2, 3, 0]

i=0, h=2:
  stack empty, push 0
  stack = [0]

i=1, h=1:
  heights[0]=2 > 1, pop 0
    height=2, width=1 (no left boundary), area=2
  push 1
  stack = [1], max_area = 2

i=2, h=5:
  heights[1]=1 < 5, push 2
  stack = [1, 2]

i=3, h=6:
  heights[2]=5 < 6, push 3
  stack = [1, 2, 3]

i=4, h=2:
  heights[3]=6 > 2, pop 3
    height=6, width=4-2-1=1, area=6
  heights[2]=5 > 2, pop 2
    height=5, width=4-1-1=2, area=10
  push 4
  stack = [1, 4], max_area = 10

i=5, h=3:
  heights[4]=2 < 3, push 5
  stack = [1, 4, 5]

i=6, h=0 (sentinel):
  heights[5]=3 > 0, pop 5
    height=3, width=6-4-1=1, area=3
  heights[4]=2 > 0, pop 4
    height=2, width=6-1-1=4, area=8
  heights[1]=1 > 0, pop 1
    height=1, width=6 (no left), area=6
  stack = [6]

Result: max_area = 10
```

---

## Visual Explanation

```
heights = [2, 1, 5, 6, 2, 3]

When we pop height=5 at index 2:
- Right boundary: index 4 (first smaller)
- Left boundary: index 1 (first smaller)
- Width: 4 - 1 - 1 = 2
- Area: 5 × 2 = 10

    6
   ┌┐
  5├┤
 ┌┴┴┐     ← Rectangle of height 5, width 2
 │  │
2│  │  3
├┤  ├┐├┤
├┤├┤├┤├┤
└┴┴┴┴┴┴┘
 0 1 2 3 4 5
```

---

## Alternative: Precompute Left and Right Boundaries

```python
def largest_rectangle_v2(heights: list[int]) -> int:
    """
    Precompute left and right boundaries separately.

    Time Complexity: $\mathcal{O}(n)$
    Space Complexity: $\mathcal{O}(n)$
    """
    n = len(heights)
    if n == 0:
        return 0

    # left[i] = index of first smaller element to the left
    left = [0] * n
    stack = []
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    # right[i] = index of first smaller element to the right
    right = [0] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    # Calculate max area
    max_area = 0
    for i in range(n):
        width = right[i] - left[i] - 1
        area = heights[i] * width
        max_area = max(max_area, area)

    return max_area
```

---

## Related Problem: Maximal Rectangle

```python
def maximal_rectangle(matrix: list[list[str]]) -> int:
    """
    Find largest rectangle containing only 1s.

    LeetCode 85: Maximal Rectangle

    Idea: Build histogram for each row, apply histogram algorithm.

    Time Complexity: $\mathcal{O}(r \times c)$ where $r$ is rows and $c$ is cols
    Space Complexity: $\mathcal{O}(c)$ for the heights array
    """
    if not matrix or not matrix[0]:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    heights = [0] * cols
    max_area = 0

    for row in matrix:
        # Update heights
        for j in range(cols):
            if row[j] == '1':
                heights[j] += 1
            else:
                heights[j] = 0

        # Apply histogram algorithm
        max_area = max(max_area, largest_rectangle_in_histogram(heights))

    return max_area


# Example
matrix = [
    ["1", "0", "1", "0", "0"],
    ["1", "0", "1", "1", "1"],
    ["1", "1", "1", "1", "1"],
    ["1", "0", "0", "1", "0"]
]
print(maximal_rectangle(matrix))  # 6
```

### How It Works

```
Matrix:
1 0 1 0 0
1 0 1 1 1
1 1 1 1 1
1 0 0 1 0

After each row, histogram heights:
Row 0: [1, 0, 1, 0, 0] → max = 1
Row 1: [2, 0, 2, 1, 1] → max = 3
Row 2: [3, 1, 3, 2, 2] → max = 6 ★
Row 3: [4, 0, 0, 3, 0] → max = 4

Final answer: 6
```

---

## Related Problem: Trapping Rain Water

```python
def trap_water(height: list[int]) -> int:
    """
    Calculate trapped rain water.

    LeetCode 42: Trapping Rain Water

    Time Complexity: $\mathcal{O}(n)$
    Space Complexity: $\mathcal{O}(n)$
    """
    stack = []  # Monotonic decreasing stack of indices
    water = 0

    for i in range(len(height)):
        while stack and height[stack[-1]] < height[i]:
            bottom = stack.pop()
            if not stack:
                break

            # Width between current and previous bar
            width = i - stack[-1] - 1
            # Height is min of walls minus bottom
            h = min(height[stack[-1]], height[i]) - height[bottom]
            water += width * h

        stack.append(i)

    return water


# Example
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
print(trap_water(height))  # 6
```

### Alternative: Two Pointers

```python
def trap_water_two_pointers(height: list[int]) -> int:
    """
    Two-pointer approach for $\mathcal{O}(1)$ space.

    Time Complexity: $\mathcal{O}(n)$
    Space Complexity: $\mathcal{O}(1)$
    """
    if not height:
        return 0

    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1

    return water
```

---

## Related Problem: Container With Most Water

```python
def max_area_container(height: list[int]) -> int:
    """
    Find two lines that form container with max water.

    LeetCode 11: Container With Most Water

    Time Complexity: $\mathcal{O}(n)$
    Space Complexity: $\mathcal{O}(1)$
    """
    left, right = 0, len(height) - 1
    max_area = 0

    while left < right:
        # Area = width × min(left_height, right_height)
        width = right - left
        h = min(height[left], height[right])
        area = width * h
        max_area = max(max_area, area)

        # Move the shorter line inward
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_area


# Example
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
print(max_area_container(height))  # 49
```

---

## Comparison of Water Problems

| Problem              | Bars Used      | Calculation                      |
| -------------------- | -------------- | -------------------------------- |
| Largest Rectangle    | Any contiguous | height × width                   |
| Container With Water | Any two        | min(h1, h2) × distance           |
| Trapping Rain Water  | All            | Sum of water above each position |

---

## Complexity Summary

| Problem              | Time     | Space                  |
| -------------------- | -------- | ---------------------- |
| Largest Rectangle    | $\mathcal{O}(n)$     | $\mathcal{O}(n)$                   |
| Maximal Rectangle    | $\mathcal{O}(r \times c)$ | $\mathcal{O}(c)$                   |
| Trapping Rain Water  | $\mathcal{O}(n)$     | $\mathcal{O}(1)$ with two pointers |
| Container With Water | $\mathcal{O}(n)$     | $\mathcal{O}(1)$                   |

---

## Common Mistakes

1. **Forgetting sentinel**: Don't forget to pop remaining elements
2. **Width calculation**: When stack empty, width extends to beginning
3. **Off-by-one**: `width = right - left - 1` (exclusive boundaries)
4. **Wrong stack type**: Increasing for histogram (find smaller), decreasing for water (find larger)

---

## Practice Problems

| #   | Problem                              | Difficulty | Key Concept                      |
| --- | ------------------------------------ | ---------- | -------------------------------- |
| 1   | Largest Rectangle in Histogram       | Hard       | Core pattern                     |
| 2   | Maximal Rectangle                    | Hard       | Histogram per row                |
| 3   | Trapping Rain Water                  | Hard       | Decreasing stack or two pointers |
| 4   | Container With Most Water            | Medium     | Two pointers                     |
| 5   | Maximal Square                       | Medium     | DP variant                       |
| 6   | Largest Rectangle Containing Only 1s | Hard       | Same as Maximal Rectangle        |

---

## Key Takeaways

1. **Monotonic increasing stack**: Find first smaller on both sides
2. **Width = right - left - 1**: Distance between boundaries (exclusive)
3. **Sentinel value**: Append 0 to pop remaining elements
4. **Build histograms**: Convert 2D matrix problem to 1D
5. **$\mathcal{O}(n)$ is achievable**: Each element pushed and popped once

---

## Chapter Summary

This chapter covered the essential stack and queue patterns for interviews:

1. **Stack/Queue basics**: LIFO vs FIFO, Python implementations
2. **Valid parentheses**: Classic stack matching
3. **Monotonic stack**: Next greater/smaller element problems
4. **Monotonic deque**: Sliding window maximum
5. **Min Stack**: $\mathcal{O}(1)$ getMin with auxiliary stack
6. **Stack ↔ Queue conversions**: Design problems
7. **Expression evaluation**: Parsing with operator precedence
8. **Histogram problems**: Geometric applications

Master these patterns and you'll be prepared for stack/queue questions at any FANG+ interview.
