# Solution: Two Pointers Same Direction

## Problem 1: Remove Duplicates from Sorted Array
Given an integer array `nums` sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. Then return the number of unique elements in `nums`.

### Python Implementation
```python
def remove_duplicates(nums: list[int]) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not nums:
        return 0

    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]

    return slow + 1
```

---

## Problem 2: Move Zeroes
Given an integer array `nums`, move all 0's to the end of it while maintaining the relative order of the non-zero elements.

### Python Implementation
```python
def move_zeroes(nums: list[int]) -> None:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
```
