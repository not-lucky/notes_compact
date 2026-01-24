# Practice Problems - Search in Rotated Sorted Array

## 1. Search in Rotated Sorted Array (LeetCode 33)

### Problem Statement
There is an integer array `nums` sorted in ascending order (with distinct values).
Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k` (`1 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (0-indexed). For example, `[0,1,2,4,5,6,7]` might be rotated at pivot index 3 and become `[4,5,6,7,0,1,2]`.
Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

You must write an algorithm with `O(log n)` runtime complexity.

### Constraints
- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- All values of `nums` are unique.
- `nums` is an ascending array that is possibly rotated.
- `-10^4 <= target <= 10^4`

### Example
**Input:** `nums = [4,5,6,7,0,1,2], target = 0`
**Output:** `4`

### Python Block
```python
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid

        # Identify which half is sorted
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

## 2. Search in Rotated Sorted Array II (LeetCode 81)

### Problem Statement
There is an integer array `nums` sorted in ascending order (with duplicates).
Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k`.
Given the array `nums` after the possible rotation and an integer `target`, return `true` if `target` is in `nums`, or `false` if it is not in `nums`.

### Constraints
- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- `nums` is guaranteed to be rotated at some pivot.
- `-10^4 <= target <= 10^4`

### Example
**Input:** `nums = [2,5,6,0,0,1,2], target = 0`
**Output:** `true`

### Python Block
```python
def search_with_duplicates(nums: list[int], target: int) -> bool:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return True

        # Handle duplicates: can't determine sorted half
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

## 3. Find Minimum in Rotated Sorted Array (LeetCode 153)

### Problem Statement
Suppose an array of length `n` sorted in ascending order is rotated between `1` and `n` times.
Given the sorted rotated array `nums` of unique elements, return the minimum element of this array.

### Constraints
- `n == nums.length`
- `1 <= n <= 5000`
- `-5000 <= nums[i] <= 5000`
- All the integers of `nums` are unique.
- `nums` is sorted and possibly rotated.

### Example
**Input:** `nums = [3,4,5,1,2]`
**Output:** `1`

### Python Block
```python
def find_min(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return nums[left]
```

## 4. Find Minimum in Rotated Sorted Array II (LeetCode 154)

### Problem Statement
Suppose an array of length `n` sorted in ascending order is rotated between `1` and `n` times.
Given the sorted rotated array `nums` that may contain duplicates, return the minimum element of this array.

### Constraints
- `n == nums.length`
- `1 <= n <= 5000`
- `-5000 <= nums[i] <= 5000`
- `nums` is sorted and possibly rotated.

### Example
**Input:** `nums = [2,2,2,0,1]`
**Output:** `0`

### Python Block
```python
def find_min_with_duplicates(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        elif nums[mid] < nums[right]:
            right = mid
        else:
            # nums[mid] == nums[right], can't determine
            right -= 1

    return nums[left]
```

## 5. Rotation Count

### Problem Statement
Given an array `nums` which is a sorted array rotated `k` times, find the value of `k`. Assume the array was originally sorted in ascending order and all elements are unique.

### Example
**Input:** `nums = [15, 18, 2, 3, 6, 12]`
**Output:** `2` (The original array was [2, 3, 6, 12, 15, 18] and it was rotated 2 times).

### Python Block
```python
def find_rotation_count(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1

    # Check if array is not rotated
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
