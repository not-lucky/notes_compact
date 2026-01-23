# Solution: Subarray Sum with HashMap

## Problem Statement
Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals to `k`.

## Constraints
- `1 <= nums.length <= 2 * 10^4`
- `-1000 <= nums[i] <= 1000`
- `-10^7 <= k <= 10^7`

## Example (Input/Output)
```
Input: nums = [1, 1, 1], k = 2
Output: 2
```

## Python Implementation
```python
def subarray_sum(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum equal to k using prefix sums and a hashmap.

    Time: O(n)
    Space: O(n)
    """
    count = 0
    prefix_sum = 0
    prefix_count = {0: 1}  # prefix_sum -> how many times seen

    for num in nums:
        prefix_sum += num

        # If (prefix_sum - k) exists, found subarrays ending here
        if prefix_sum - k in prefix_count:
            count += prefix_count[prefix_sum - k]

        # Record current prefix sum
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return count
```
