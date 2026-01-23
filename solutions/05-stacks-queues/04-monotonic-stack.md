# Solution: Monotonic Stack Practice Problems

## Problem 1: Next Greater Element I
### Problem Statement
The next greater element of some element `x` in an array is the first greater element that is to the right of `x` in the same array.

You are given two distinct 0-indexed integer arrays `nums1` and `nums2`, where `nums1` is a subset of `nums2`.

For each `0 <= i < nums1.length`, find the index `j` such that `nums1[i] == nums2[j]` and determine the next greater element of `nums2[j]` in `nums2`. If there is no next greater element, then the answer for this query is -1.

Return an array `ans` of length `nums1.length` such that `ans[i]` is the next greater element as described above.

### Constraints
- `1 <= nums1.length <= nums2.length <= 1000`
- `0 <= nums1[i], nums2[i] <= 10^4`
- All integers in `nums1` and `nums2` are unique.
- All the integers of `nums1` appear in `nums2`.

### Example
Input: `nums1 = [4,1,2], nums2 = [1,3,4,2]`
Output: `[-1,3,-1]`

### Python Implementation
```python
def nextGreaterElement(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Time Complexity: O(n + m) where n is len(nums1) and m is len(nums2)
    Space Complexity: O(m)
    """
    stack = []
    mapping = {}
    for num in nums2:
        while stack and stack[-1] < num:
            mapping[stack.pop()] = num
        stack.append(num)

    return [mapping.get(num, -1) for num in nums1]
```

---

## Problem 2: Next Greater Element II
### Problem Statement
Given a circular integer array `nums` (i.e., the next element of `nums[nums.length - 1]` is `nums[0]`), return the next greater number for every element in `nums`.

The next greater number of a number `x` is the first greater number to its traversing-order next in the array, which means you could search circularly to find its next greater number. If it doesn't exist, return -1 for this number.

### Constraints
- `1 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`

### Example
Input: `nums = [1,2,1]`
Output: `[2,-1,2]`

### Python Implementation
```python
def nextGreaterElements(nums: list[int]) -> list[int]:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(2 * n):
        num = nums[i % n]
        while stack and nums[stack[-1]] < num:
            res[stack.pop()] = num
        if i < n:
            stack.append(i)
    return res
```

---

## Problem 3: Daily Temperatures
### Problem Statement
Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i`th day to get a warmer temperature. If there is no future day for which this is possible, keep `answer[i] == 0` instead.

### Constraints
- `1 <= temperatures.length <= 10^5`
- `30 <= temperatures[i] <= 100`

### Example
Input: `temperatures = [73,74,75,71,69,72,76,73]`
Output: `[1,1,4,2,1,1,0,0]`

### Python Implementation
```python
def dailyTemperatures(temperatures: list[int]) -> list[int]:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    n = len(temperatures)
    ans = [0] * n
    stack = []
    for i in range(n):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            prev_idx = stack.pop()
            ans[prev_idx] = i - prev_idx
        stack.append(i)
    return ans
```

---

## Problem 4: Online Stock Span
### Problem Statement
Design an algorithm that collects daily price quotes for some stock and returns the span of that stock's price for the current day.

The span of the stock's price in one day is the maximum number of consecutive days (starting from that day and going backward) for which the stock price was less than or equal to the price of that day.

Implement the `StockSpanner` class:
- `StockSpanner()` Initializes the object of the class.
- `int next(int price)` Returns the span of the stock's price given that today's price is `price`.

### Constraints
- `1 <= price <= 10^5`
- At most `10^4` calls will be made to `next`.

### Example
Input: `["StockSpanner", "next", "next", "next", "next", "next", "next", "next"]`, `[[], [100], [80], [60], [70], [60], [75], [85]]`
Output: `[null, 1, 1, 1, 2, 1, 4, 6]`

### Python Implementation
```python
class StockSpanner:
    def __init__(self):
        self.stack = [] # (price, span)

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span
```
