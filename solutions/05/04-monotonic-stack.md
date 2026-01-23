# Monotonic Stack

## Practice Problems

### 1. Next Greater Element I
**Difficulty:** Easy
**Key Technique:** Monotonic decreasing stack + HashMap

```python
def next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Time: O(N + M)
    Space: O(M)
    """
    res = {}
    stack = []
    for n in nums2:
        while stack and stack[-1] < n:
            res[stack.pop()] = n
        stack.append(n)
    return [res.get(n, -1) for n in nums1]
```

### 2. Next Greater Element II
**Difficulty:** Medium
**Key Technique:** Monotonic decreasing stack + Circular traversal

```python
def next_greater_elements(nums: list[int]) -> list[int]:
    """
    Time: O(n)
    Space: O(n)
    """
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(2 * n):
        while stack and nums[stack[-1]] < nums[i % n]:
            res[stack.pop()] = nums[i % n]
        if i < n:
            stack.append(i)
    return res
```

### 3. Daily Temperatures
**Difficulty:** Medium
**Key Technique:** Monotonic decreasing stack of indices

```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    """
    Time: O(n)
    Space: O(n)
    """
    res = [0] * len(temperatures)
    stack = [] # indices
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            prev_idx = stack.pop()
            res[prev_idx] = i - prev_idx
        stack.append(i)
    return res
```

### 4. Largest Rectangle in Histogram
**Difficulty:** Hard
**Key Technique:** Monotonic increasing stack + boundary detection

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

### 5. Sum of Subarray Minimums
**Difficulty:** Medium
**Key Technique:** Monotonic stack (Contribution of each element)

```python
def sum_subarray_mins(arr: list[int]) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    n = len(arr)
    left = [-1] * n
    right = [n] * n
    stack = []

    # Previous smaller
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        if stack: left[i] = stack[-1]
        stack.append(i)

    stack = []
    # Next smaller
    for i in range(n-1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        if stack: right[i] = stack[-1]
        stack.append(i)

    res = 0
    mod = 10**9 + 7
    for i in range(n):
        res = (res + arr[i] * (i - left[i]) * (right[i] - i)) % mod
    return res
```
