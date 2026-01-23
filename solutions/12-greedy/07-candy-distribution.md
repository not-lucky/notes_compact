# Practice Problems - Candy Distribution

## 1. Candy

### Problem Statement
There are `n` children standing in a line. Each child is assigned a rating value given in the integer array `ratings`.
You are giving candies to these children subjected to the following requirements:
- Each child must have at least one candy.
- Children with a higher rating get more candies than their neighbors.
Return the minimum number of candies you need to have to distribute the candies to the children.

### Constraints
- `n == ratings.length`
- `1 <= n <= 2 * 10^4`
- `0 <= ratings[i] <= 2 * 10^4`

### Example
**Input:** `ratings = [1,0,2]`
**Output:** `5`
**Explanation:** You can allocate to the first, second and third child with 2, 1, 2 candies respectively.

### Python Implementation
```python
def candy(ratings: list[int]) -> int:
    n = len(ratings)
    res = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i-1]:
            res[i] = res[i-1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i+1]:
            res[i] = max(res[i], res[i+1] + 1)
    return sum(res)
```

## 2. Trapping Rain Water

### Problem Statement
Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

### Constraints
- `n == height.length`
- `1 <= n <= 2 * 10^4`
- `0 <= height[i] <= 10^5`

### Example
**Input:** `height = [0,1,0,2,1,0,1,3,2,1,2,1]`
**Output:** `6`

### Python Implementation
```python
def trap(height: list[int]) -> int:
    if not height: return 0
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])

    right_max[n-1] = height[n-1]
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i+1], height[i])

    res = 0
    for i in range(n):
        res += min(left_max[i], right_max[i]) - height[i]
    return res
```

## 3. Product of Array Except Self

### Problem Statement
Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.
The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.
You must write an algorithm that runs in `O(n)` time and without using the division operation.

### Constraints
- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

### Example
**Input:** `nums = [1,2,3,4]`
**Output:** `[24,12,8,6]`

### Python Implementation
```python
def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [1] * n
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n-1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
    return res
```

## 4. Container With Most Water

### Problem Statement
You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i-th` line are `(i, 0)` and `(i, height[i])`.
Find two lines that together with the x-axis form a container, such that the container contains the most water.
Return the maximum amount of water a container can store.

### Constraints
- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`

### Example
**Input:** `height = [1,8,6,2,5,4,8,3,7]`
**Output:** `49`

### Python Implementation
```python
def maxArea(height: list[int]) -> int:
    l, r = 0, len(height) - 1
    res = 0
    while l < r:
        area = (r - l) * min(height[l], height[r])
        res = max(res, area)
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return res
```

## 5. Increasing Triplet Subsequence

### Problem Statement
Given an integer array `nums`, return `true` if there exists a triple of indices `(i, j, k)` such that `i < j < k` and `nums[i] < nums[j] < nums[k]`. If no such indices exists, return `false`.

### Constraints
- `1 <= nums.length <= 5 * 10^5`
- `-2^31 <= nums[i] <= 2^31 - 1`

### Example
**Input:** `nums = [1,2,3,4,5]`
**Output:** `true`

### Python Implementation
```python
def increasingTriplet(nums: list[int]) -> bool:
    first = float('inf')
    second = float('inf')
    for x in nums:
        if x <= first:
            first = x
        elif x <= second:
            second = x
        else:
            return True
    return False
```
