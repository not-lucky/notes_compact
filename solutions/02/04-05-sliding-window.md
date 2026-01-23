# Solution: Sliding Window Practice

## Problem 1: Maximum Average Subarray I
You are given an integer array `nums` consisting of `n` elements, and an integer `k`. Find a contiguous subarray whose length is equal to `k` that has the maximum average value and return this value.

### Python Implementation
```python
def find_max_average(nums: list[int], k: int) -> float:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    curr_sum = sum(nums[:k])
    max_sum = curr_sum

    for i in range(k, len(nums)):
        curr_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, curr_sum)

    return max_sum / k
```

---

## Problem 2: Longest Substring Without Repeating Characters
Given a string `s`, find the length of the longest substring without repeating characters.

### Python Implementation
```python
def length_of_longest_substring(s: str) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(min(n, alphabet_size))
    """
    char_map = {}
    left = 0
    max_len = 0

    for right in range(len(s)):
        if s[right] in char_map and char_map[s[right]] >= left:
            left = char_map[s[right]] + 1

        char_map[s[right]] = right
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

## Problem 3: Minimum Size Subarray Sum
Given an array of positive integers `nums` and a positive integer `target`, return the minimal length of a contiguous subarray of which the sum is greater than or equal to `target`. If there is no such subarray, return 0 instead.

### Python Implementation
```python
def min_subarray_len(target: int, nums: list[int]) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    left = 0
    curr_sum = 0
    min_l = float('inf')

    for right in range(len(nums)):
        curr_sum += nums[right]
        while curr_sum >= target:
            min_l = min(min_l, right - left + 1)
            curr_sum -= nums[left]
            left += 1

    return min_l if min_l != float('inf') else 0
```
