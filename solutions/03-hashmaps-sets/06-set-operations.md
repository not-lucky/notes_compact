# Solution: Set Operations

## Problem Statement
Given two integer arrays `nums1` and `nums2`, return an array of their intersection. Each element in the result must be unique and you may return the result in any order.

## Constraints
- `1 <= nums1.length, nums2.length <= 1000`
- `0 <= nums1[i], nums2[i] <= 1000`

## Example (Input/Output)
```
Input: nums1 = [1, 2, 2, 1], nums2 = [2, 2]
Output: [2]
```

## Python Implementation
```python
def intersection(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Find elements that appear in both arrays (unique).

    Time: O(n + m)
    Space: O(n + m)
    """
    return list(set(nums1) & set(nums2))
```
