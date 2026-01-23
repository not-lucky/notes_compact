# Solution: Advanced Array Patterns

## Problem 1: Subarray Sum Equals K
Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals to `k`.

### Python Implementation
```python
def subarray_sum(nums: list[int], k: int) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    prefix_map = {0: 1}
    curr_sum = 0
    count = 0

    for num in nums:
        curr_sum += num
        if curr_sum - k in prefix_map:
            count += prefix_map[curr_sum - k]
        prefix_map[curr_sum] = prefix_map.get(curr_sum, 0) + 1

    return count
```

---

## Problem 2: Car Pooling
There is a car with `capacity` empty seats. The car only drives east. You are given the integer `capacity` and an array `trips` where `trips[i] = [numPassengers_i, from_i, to_i]`. Return `true` if it is possible to pick up and drop off all passengers for all the given trips, or `false` otherwise.

### Python Implementation
```python
def car_pooling(trips: list[list[int]], capacity: int) -> bool:
    """
    Time Complexity: O(n + max_location)
    Space Complexity: O(max_location)
    """
    # Using difference array / timeline
    timeline = [0] * 1001 # Constraints often 0 to 1000
    for num, start, end in trips:
        timeline[start] += num
        timeline[end] -= num

    curr_passengers = 0
    for passengers in timeline:
        curr_passengers += passengers
        if curr_passengers > capacity:
            return False

    return True
```

---

## Problem 3: Maximum Subarray (Kadane's Algorithm)
Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

### Python Implementation
```python
def max_subarray(nums: list[int]) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    max_sum = curr_sum = nums[0]
    for i in range(1, len(nums)):
        curr_sum = max(nums[i], curr_sum + nums[i])
        max_sum = max(max_sum, curr_sum)
    return max_sum
```
