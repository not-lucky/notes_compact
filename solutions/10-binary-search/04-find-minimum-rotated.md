# Find Minimum in Rotated Sorted Array Solutions

## 1. Find Minimum in Rotated Sorted Array

[LeetCode 153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

### Problem Description

Given the sorted rotated array `nums` of unique elements, return the minimum element of this array.

### Solution

```python
def findMin(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1

    # Array not rotated or single element
    if nums[left] <= nums[right]:
        return nums[left]

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            # Minimum is in the right half, not including mid
            left = mid + 1
        else:
            # Minimum is in the left half, including mid
            right = mid

    return nums[left]
```

- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 2. Find Minimum in Rotated Sorted Array II

[LeetCode 154](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/)

### Problem Description

Similar to the previous problem, but the array may contain duplicates.

### Solution

```python
def findMin(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            left = mid + 1
        elif nums[mid] < nums[right]:
            right = mid
        else:
            # nums[mid] == nums[right], cannot determine which half to go
            # safely shrink the right boundary
            right -= 1

    return nums[left]
```

- **Time Complexity**: O(log n) average, O(n) worst case
- **Space Complexity**: O(1)

---

## 3. Search in Rotated Sorted Array

[LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/)

### Problem Description

Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

### Solution

```python
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid

        # Identify the sorted half
        if nums[left] <= nums[mid]:
            # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
```

- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 4. Rotation Count

[GeeksforGeeks](https://www.geeksforgeeks.org/find-rotation-count-rotated-sorted-array/)

### Problem Description

Given an array of distinct integers sorted in increasing order and rotated of some unknown number of times, find the number of times the array is rotated.

### Solution

```python
def findRotationCount(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1

    # If array is not rotated
    if nums[left] <= nums[right]:
        return 0

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return left
```

- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 5. Check if Array is Sorted and Rotated

[LeetCode 1752](https://leetcode.com/problems/check-if-array-is-sorted-and-rotated/)

### Problem Description

Given an array `nums`, return `true` if the array was originally sorted in non-decreasing order, then rotated some number of positions (including zero). Otherwise, return `false`.

### Solution

```python
def check(nums: list[int]) -> bool:
    count = 0
    n = len(nums)
    for i in range(n):
        if nums[i] > nums[(i + 1) % n]:
            count += 1
            if count > 1:
                return False
    return True
```

- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
