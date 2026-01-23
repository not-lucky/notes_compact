# House Robber Solutions

## Problem: House Robber I
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night. Given an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

### Constraints
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 400

### Examples
- Input: [1, 2, 3, 1] -> Output: 4
- Input: [2, 7, 9, 3, 1] -> Output: 12

### Implementation

```python
def rob(nums: list[int]) -> int:
    """
    Maximum sum of non-adjacent elements.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    # dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    prev2, prev1 = nums[0], max(nums[0], nums[1])

    for i in range(2, len(nums)):
        curr = max(prev1, prev2 + nums[i])
        prev2, prev1 = prev1, curr

    return prev1
```

## Problem: House Robber II (Circular Houses)
All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent houses were broken into on the same night.

### Constraints
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 1000

### Examples
- Input: [2, 3, 2] -> Output: 3
- Input: [1, 2, 3, 1] -> Output: 4

### Implementation

```python
def rob_circular(nums: list[int]) -> int:
    """
    Circular variant of House Robber.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    def rob_linear(houses):
        p2, p1 = 0, 0
        for h in houses:
            curr = max(p1, p2 + h)
            p2, p1 = p1, curr
        return p1

    # Choice: Either rob from 0 to n-2 or 1 to n-1
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

## Problem: Delete and Earn
You are given an integer array `nums`. You want to maximize the number of points you get by performing the following operation any number of times: Pick any `nums[i]` and delete it to earn `nums[i]` points. Afterwards, you must delete every element equal to `nums[i] - 1` and every element equal to `nums[i] + 1`.

### Implementation

```python
def delete_and_earn(nums: list[int]) -> int:
    """
    Transforms problem into House Robber.
    Time complexity: O(n + max(nums))
    Space complexity: O(max(nums))
    """
    if not nums:
        return 0

    max_val = max(nums)
    points = [0] * (max_val + 1)
    for n in nums:
        points[n] += n

    # Standard House Robber on the points array
    p2, p1 = 0, 0
    for p in points:
        curr = max(p1, p2 + p)
        p2, p1 = p1, curr
    return p1
```
