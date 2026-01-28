# Search in Rotated Sorted Array Solutions

## 1. Search in Rotated Sorted Array

[LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/)

### Problem Description

There is an integer array `nums` sorted in ascending order (with distinct values). Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k`. Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

### Solution

```python
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # Determine which half is sorted
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

## 2. Search in Rotated Sorted Array II

[LeetCode 81](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)

### Problem Description

Similar to the previous problem, but `nums` may contain duplicates. Return `true` if `target` is in `nums`, or `false` otherwise.

### Solution

```python
def search(nums: list[int], target: int) -> bool:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return True

        # When left, mid, and right are all the same, we can't tell which half is sorted
        if nums[left] == nums[mid] == nums[right]:
            left += 1
            right -= 1
        elif nums[left] <= nums[mid]:
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

    return False
```

- **Time Complexity**: O(log n) average, O(n) worst case
- **Space Complexity**: O(1)

---

## 4. Find Minimum in Rotated Sorted Array

[LeetCode 153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

### Problem Description

Given the sorted rotated array `nums` of unique elements, return the minimum element of this array.

### Solution

```python
def findMin(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    if nums[left] <= nums[right]:
        return nums[left]

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]
```

- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 5. Find Minimum in Rotated Sorted Array II

[LeetCode 154](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/)

### Problem Description

Similar to the previous problem, but the array may contain duplicates.

### Solution

```python
def findMinWithDuplicates(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        elif nums[mid] < nums[right]:
            right = mid
        else:
            right -= 1
    return nums[left]
```

- **Time Complexity**: O(log n) average, O(n) worst case
- **Space Complexity**: O(1)

---

## 6. Rotation Count

[GeeksforGeeks](https://www.geeksforgeeks.org/find-rotation-count-rotated-sorted-array/)

### Problem Description

Find the number of times a sorted array has been rotated.

### Solution

```python
def findRotationCount(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
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
