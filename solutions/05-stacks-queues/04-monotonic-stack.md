# Monotonic Stack - Practice Solutions

This file provides optimal Python solutions and explanations for the practice problems listed in the Monotonic Stack notes.

## 1. Next Greater Element I
**Problem Statement**: The next greater element of some element `x` in an array is the first greater element that is to the right of `x` in the same array. Given two arrays `nums1` and `nums2` where `nums1` is a subset of `nums2`, return an array of the next greater elements for `nums1` in `nums2`.

### Optimal Python Solution
```python
def nextGreaterElement(nums1: list[int], nums2: list[int]) -> list[int]:
    # Map to store next greater element for each value in nums2
    mapping = {}
    stack = [] # Monotonic decreasing stack

    for num in nums2:
        # If current number is greater than top of stack
        while stack and stack[-1] < num:
            # We found the next greater for the element at top
            mapping[stack.pop()] = num
        stack.append(num)

    # For elements remaining in stack, there is no next greater
    return [mapping.get(num, -1) for num in nums1]
```

### Explanation
We use a monotonic decreasing stack to process `nums2`. For each number, we pop all smaller numbers from the stack; the current number is the "next greater" for those popped elements. We store these pairs in a hash map for O(1) retrieval when iterating through `nums1`.

### Complexity Analysis
- **Time Complexity**: O(n + m), where n and m are lengths of `nums1` and `nums2`. We traverse `nums2` once and `nums1` once.
- **Space Complexity**: O(m), for the map and stack.

---

## 2. Next Greater Element II
**Problem Statement**: Given a circular integer array `nums`, return the next greater number for every element in `nums`.

### Optimal Python Solution
```python
def nextGreaterElements(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [-1] * n
    stack = [] # Indices of elements

    # Iterate twice to simulate circularity
    for i in range(2 * n):
        num = nums[i % n]
        while stack and nums[stack[-1]] < num:
            res[stack.pop()] = num
        if i < n:
            stack.append(i)

    return res
```

### Complexity Analysis
- **Time Complexity**: O(n), where n is the length of `nums`. Each index is pushed and popped exactly twice (once per pass) across the 2n iterations.
- **Space Complexity**: O(n), to store the indices in the stack.

---

## 3. Daily Temperatures
**Problem Statement**: Return an array such that `ans[i]` is the number of days you have to wait after the `i-th` day to get a warmer temperature.

### Optimal Python Solution
```python
def dailyTemperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    ans = [0] * n
    stack = [] # Monotonic decreasing stack of indices

    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            prev_idx = stack.pop()
            ans[prev_idx] = i - prev_idx
        stack.append(i)

    return ans
```

### Complexity Analysis
- **Time Complexity**: O(n), each index is pushed and popped at most once.
- **Space Complexity**: O(n), for the stack.

---

## 4. Online Stock Span
**Problem Statement**: Design an algorithm that collects daily price quotes and returns the span of that day's price. The span is the maximum number of consecutive days for which the price was less than or equal to that day's price.

### Optimal Python Solution
```python
class StockSpanner:
    def __init__(self):
        # Stack stores (price, span)
        self.stack = []

    def next(self, price: int) -> int:
        span = 1
        # While previous prices are less or equal to today's
        while self.stack and self.stack[-1][0] <= price:
            # Accumulate their spans
            span += self.stack.pop()[1]
### Complexity Analysis
- **Time Complexity**: O(n) amortized. Each call to `next()` might involve multiple pops, but every price is pushed onto the stack exactly once. Across the lifetime of the object, total pops ≤ total pushes.
- **Space Complexity**: O(n), to store the price history in the stack.

---

## 5. Sum of Subarray Minimums
**Problem Statement**: Given an array of integers `arr`, find the sum of `min(b)`, where `b` ranges over every (contiguous) subarray of `arr`.

### Optimal Python Solution
```python
def sumSubarrayMins(arr: list[int]) -> int:
    MOD = 10**9 + 7
    stack = [] # Monotonic increasing stack
    arr = [0] + arr + [0] # Add sentinels
    res = 0

    for i, x in enumerate(arr):
        while stack and arr[stack[-1]] > x:
            mid = stack.pop()
            left = stack[-1]
            right = i
            # count = (mid - left) * (right - mid)
            res += arr[mid] * (mid - left) * (right - mid)
        stack.append(i)

### Complexity Analysis
- **Time Complexity**: O(n), where n is the length of the array. Each element is added to the stack once and removed once.
- **Space Complexity**: O(n), for the monotonic stack.

---

## 6. Largest Rectangle in Histogram
**Problem Statement**: Find the area of the largest rectangle in a histogram.

### Optimal Python Solution
```python
def largestRectangleArea(heights: list[int]) -> int:
    stack = [-1]
    max_area = 0
    heights.append(0) # Sentinel

    for i, h in enumerate(heights):
        while heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

### Complexity Analysis
- **Time Complexity**: O(n), where n is the number of bars. Each bar's index is pushed and popped exactly once.
- **Space Complexity**: O(n), for the stack.

---

## 7. Maximal Rectangle
**Problem Statement**: Given a `rows x cols` binary `matrix` filled with `0`'s and `1`'s, find the largest rectangle containing only `1`'s and return its area.

### Optimal Python Solution
```python
def maximalRectangle(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]: return 0

    rows, cols = len(matrix), len(matrix[0])
    heights = [0] * cols
    max_area = 0

    for row in matrix:
        for j in range(cols):
            if row[j] == '1':
                heights[j] += 1
            else:
                heights[j] = 0

        # Largest Rectangle in Histogram for each row
        stack = [-1]
        row_heights = heights + [0]
        for i, h in enumerate(row_heights):
            while row_heights[stack[-1]] > h:
                height = row_heights[stack.pop()]
                width = i - stack[-1] - 1
                max_area = max(max_area, height * width)
            stack.append(i)

### Complexity Analysis
- **Time Complexity**: O(rows * cols), as we iterate through each cell in the binary matrix and perform a linear time histogram calculation for each row.
- **Space Complexity**: O(cols), to store the histogram heights for the current row.

---

## 8. Remove K Digits

**Problem Statement**: Given a non-negative integer represented as a string `num`, and an integer `k`, remove `k` digits from the number so that the new number is the smallest possible.

### Optimal Python Solution
```python
def removeKdigits(num: str, k: int) -> str:
    stack = []

    for digit in num:
        # Maintain monotonic increasing order to keep smallest digits at start
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)

    # Remove leading zeros and handle empty result
    return "".join(stack).lstrip('0') or "0"

### Complexity Analysis
- **Time Complexity**: O(n), where n is the number of digits in `num`. We iterate once, and each digit is pushed/popped at most once.
- **Space Complexity**: O(n), to store the digits in the stack.

    ## 9. 132 Pattern
**Problem Statement**: Given an array of `n` integers `nums`, a 132 pattern is a subsequence of three integers `nums[i]`, `nums[j]` and `nums[k]` such that `i < j < k` and `nums[i] < nums[k] < nums[j]`. Return `true` if there is a 132 pattern in `nums`, otherwise, return `false`.

### Optimal Python Solution
```python
def find132pattern(nums: list[int]) -> bool:
    # s3 is the '2' in the '132' pattern (the middle value)
    s3 = float('-inf')
    stack = [] # Monotonic decreasing stack (stores '3' values)

    # Iterate from right to left
    for n in reversed(nums):
        # If we find a value smaller than s3, we found our '1'
        if n < s3:
            return True
        # Maintain monotonic stack: if current is larger than top,
        # it's a potential '3', and the popped top is a potential '2'
        while stack and stack[-1] < n:
            s3 = stack.pop()
        stack.append(n)

### Complexity Analysis
- **Time Complexity**: O(n), where n is the length of `nums`. We traverse the array once, and each element is pushed/popped from the stack at most once.
- **Space Complexity**: O(n), for the monotonic stack.

### Explanation
We search for the pattern from right to left. We use a stack to keep track of the largest values (`3` in the `132` pattern) and a variable `s3` to keep track of the second largest value (`2` in the `132` pattern). If we encounter a value smaller than `s3`, it means we've found our `1`, completing the `1-3-2` sequence.
