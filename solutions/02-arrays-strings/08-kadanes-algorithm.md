# Kadane's Algorithm - Solutions

## Practice Problems

### 1. Maximum Subarray
**Problem Statement**: Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

**Examples & Edge Cases**:
- Example: `[-2,1,-3,4,-1,2,1,-5,4]` -> `6` (subarray `[4,-1,2,1]`)
- Edge Case: Array with all negative numbers (should return the largest single element).
- Edge Case: Array with one element.

**Optimal Python Solution**:
```python
def maxSubArray(nums: list[int]) -> int:
    # current_sum tracks the max subarray sum ending at the current index
    current_sum = nums[0]
    # max_sum tracks the global maximum seen so far
    max_sum = nums[0]

    for i in range(1, len(nums)):
        # Decide whether to extend the previous subarray or start fresh
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)

    return max_sum
```

**Explanation**:
At each step, we calculate the maximum sum of a subarray ending at the current index. If the sum of the subarray ending at the previous index is positive, it's beneficial to extend it; otherwise, we start a new subarray from the current element. We update the global maximum at each step.

**Complexity Analysis**:
- **Time Complexity**: O(n), where n is the length of the array. We traverse the array once.
- **Space Complexity**: O(1), only a few variables used.

---

### 2. Maximum Product Subarray
**Problem Statement**: Find a contiguous non-empty subarray within an array (containing at least one number) which has the largest product.

**Optimal Python Solution**:
```python
def maxProduct(nums: list[int]) -> int:
    if not nums:
        return 0

    res = max_p = min_p = nums[0]

    for i in range(1, len(nums)):
        n = nums[i]
        # If the number is negative, max and min will swap after multiplication
        if n < 0:
            max_p, min_p = min_p, max_p

        max_p = max(n, max_p * n)
        min_p = min(n, min_p * n)

        res = max(res, max_p)

    return res
```

**Explanation**:
When multiplying by a negative number, the largest product can become the smallest, and the smallest can become the largest. Therefore, we track both the maximum and minimum products ending at the current position.

**Complexity Analysis**:
- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 3. Maximum Sum Circular Subarray
**Problem Statement**: Given a circular integer array `nums` of length `n`, return the maximum possible sum of a non-empty subarray of `nums`.

**Optimal Python Solution**:
```python
def maxSubarraySumCircular(nums: list[int]) -> int:
    # Case 1: Max sum is in the middle (standard Kadane)
    # Case 2: Max sum wraps around (Total - Min sum in the middle)

    total_sum = 0
    curr_max = 0
    max_sum = nums[0]
    curr_min = 0
    min_sum = nums[0]

    for n in nums:
        total_sum += n

        curr_max = max(n, curr_max + n)
        max_sum = max(max_sum, curr_max)

        curr_min = min(n, curr_min + n)
        min_sum = min(min_sum, curr_min)

    # If all numbers are negative, total_sum == min_sum
    # In this case, max_sum (least negative) is the answer
    if total_sum == min_sum:
        return max_sum

    return max(max_sum, total_sum - min_sum)
```

**Explanation**:
A circular subarray can either be a standard subarray (Case 1) or it can wrap around the end. The "wrap around" sum is equal to the total sum minus the minimum subarray sum in the middle. We calculate both using Kadane-style logic.

**Complexity Analysis**:
- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 4. House Robber
**Problem Statement**: You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night. Return the maximum amount of money you can rob.

**Optimal Python Solution**:
```python
def rob(nums: list[int]) -> int:
    # This is effectively "Max sum with no adjacent elements"
    if not nums: return 0
    if len(nums) == 1: return nums[0]

    # prev1: max money robbing up to house i-1
    # prev2: max money robbing up to house i-2
    prev2, prev1 = 0, 0

    for n in nums:
        # For current house, either rob it (n + prev2) or skip it (prev1)
        temp = max(n + prev2, prev1)
        prev2 = prev1
        prev1 = temp

    return prev1
```

**Explanation**:
For each house, we have two choices: rob it (which means we couldn't have robbed the previous house) or skip it (taking the maximum we could have from the previous house).

**Complexity Analysis**:
- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 5. House Robber II
**Problem Statement**: Same as House Robber, but houses are arranged in a circle.

**Optimal Python Solution**:
```python
def rob(nums: list[int]) -> int:
    if not nums: return 0
    if len(nums) == 1: return nums[0]

    def simple_rob(arr):
        p2, p1 = 0, 0
        for x in arr:
            p2, p1 = p1, max(x + p2, p1)
        return p1

    # Either skip the first house or skip the last house
    return max(simple_rob(nums[1:]), simple_rob(nums[:-1]))
```

**Explanation**:
Since the first and last houses are adjacent, we cannot rob both. We solve the problem twice: once excluding the first house and once excluding the last house, then take the maximum.

**Complexity Analysis**:
- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 6. Best Time to Buy and Sell Stock
**Problem Statement**: You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

**Optimal Python Solution**:
```python
def maxProfit(prices: list[int]) -> int:
    if not prices:
        return 0

    min_price = prices[0]
    max_profit = 0

    for p in prices:
        if p < min_price:
            min_price = p
        elif p - min_price > max_profit:
            max_profit = p - min_price

    return max_profit
```

**Explanation**:
This can be viewed as finding the maximum subarray sum of the differences between consecutive days. However, the standard implementation of tracking the minimum price seen so far and calculating the profit if sold today is more intuitive.

**Complexity Analysis**:
- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 7. Maximum Sum Rectangle (2D)
**Problem Statement**: Given a 2D matrix, find the sub-rectangle with the largest sum.

**Optimal Python Solution**:
```python
def maxSumRectangle(matrix: list[list[int]]) -> int:
    if not matrix or not matrix[0]: return 0
    R, C = len(matrix), len(matrix[0])
    max_rect_sum = float('-inf')

    # Try all pairs of columns
    for left in range(C):
        # row_sums[i] is sum of elements in row i between 'left' and 'right' columns
        row_sums = [0] * R
        for right in range(left, C):
            for r in range(R):
                row_sums[r] += matrix[r][right]

            # Use Kadane on the 1D compressed row_sums
            curr_max = 0
            curr_kadane = float('-inf')
            for val in row_sums:
                curr_max = max(val, curr_max + val)
                curr_kadane = max(curr_kadane, curr_max)

            max_rect_sum = max(max_rect_sum, curr_kadane)

    return max_rect_sum
```

**Explanation**:
We iterate over all possible pairs of left and right columns. For each pair, we compress the 2D problem into a 1D problem by summing elements row-wise between those columns. Then we apply standard 1D Kadane's algorithm on the resulting array.

**Complexity Analysis**:
- **Time Complexity**: O(C² * R), where C is columns and R is rows.
- **Space Complexity**: O(R).

---

### 8. Maximum Subarray Sum with One Deletion
**Problem Statement**: Given an array of integers, return the maximum sum for a non-empty subarray (contiguous elements) with at most one element deletion.

**Optimal Python Solution**:
```python
def maximumSum(arr: list[int]) -> int:
    n = len(arr)
    # ignored: max sum ending at i with one element already ignored
    # not_ignored: max sum ending at i with no elements ignored
    ignored = 0
    not_ignored = arr[0]
    res = arr[0]

    for i in range(1, n):
        # To get 'ignored' at i:
        # 1. Skip current element: prev not_ignored
        # 2. Had already skipped one before: prev ignored + current
        ignored = max(not_ignored, ignored + arr[i])

        # Standard Kadane
        not_ignored = max(arr[i], not_ignored + arr[i])

        res = max(res, ignored, not_ignored)

    return res
```

**Explanation**:
We use two variables to track the maximum subarray sum ending at each index: one where we have already deleted one element, and one where we haven't. For the `ignored` state, we can either delete the current element (inheriting the `not_ignored` sum from the previous step) or keep the current element (adding it to the `ignored` sum from the previous step).

**Complexity Analysis**:
- **Time Complexity**: O(n).
- **Space Complexity**: O(1).
