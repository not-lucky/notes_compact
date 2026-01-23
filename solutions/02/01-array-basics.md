# Solution: Array Basics Practice

## Problem 1: Plus One
Given a large integer represented as an integer array `digits`, where each `digits[i]` is the `i-th` digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading 0's, except the number 0 itself.

Increment the large integer by one and return the resulting array of digits.

### Example
Input: `digits = [1, 2, 3]`
Output: `[1, 2, 4]`

Input: `digits = [9, 9]`
Output: `[1, 0, 0]`

### Constraints
- `1 <= digits.length <= 100`
- `0 <= digits[i] <= 9`

## Python Implementation
```python
def plus_one(digits: list[int]) -> list[int]:
    """
    Time Complexity: O(n)
    Space Complexity: O(1) or O(n) if we need to create a new array for carry.
    """
    n = len(digits)

    # Traverse from right to left
    for i in range(n - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0

    # If we reached here, it means all digits were 9
    return [1] + digits
```

---

## Problem 2: Find All Duplicates in an Array
Given an integer array `nums` of length `n` where all the integers of `nums` are in the range `[1, n]` and each integer appears once or twice, return an array of all the integers that appears twice.

You must write an algorithm that runs in O(n) time and uses only constant extra space.

### Example
Input: `nums = [4,3,2,7,8,2,3,1]`
Output: `[2,3]`

### Python Implementation
```python
def find_duplicates(nums: list[int]) -> list[int]:
    """
    Time Complexity: O(n)
    Space Complexity: O(1) - output array doesn't count towards space complexity.

    Key concept: Use the index as a hash.
    Since numbers are 1 to n, we can map them to indices 0 to n-1.
    """
    result = []
    for x in nums:
        idx = abs(x) - 1
        if nums[idx] < 0:
            result.append(abs(x))
        else:
            nums[idx] *= -1

    # Restore the array (optional)
    for i in range(len(nums)):
        nums[i] = abs(nums[i])

    return result
```
