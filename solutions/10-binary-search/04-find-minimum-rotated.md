# Practice Problems - Find Minimum in Rotated Sorted Array

## 1. Find Minimum in Rotated Sorted Array (LeetCode 153)

### Problem Statement
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
        # Compare mid with right to find the "cliff"
        if nums[mid] > nums[right]:
            # Min must be in the right half
            left = mid + 1
        else:
            # Min is mid or in the left half
            right = mid

    return nums[left]
```

## 2. Find Minimum in Rotated Sorted Array II (LeetCode 154)

### Problem Statement
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
            # nums[mid] == nums[right], can't determine side
            # Safely skip the duplicate at right
            right -= 1

    return nums[left]
```

## 3. Search in Rotated Sorted Array (LeetCode 33)

### Problem Statement
Given the array `nums` after possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

### Constraints
- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- All values of `nums` are unique.
- `nums` is possibly rotated.
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

## 4. Rotation Count

### Problem Statement
Given an array `nums` which is a sorted array rotated `k` times, find the value of `k`.

### Example
**Input:** `nums = [15, 18, 2, 3, 6, 12]`
**Output:** `2`

### Python Block
```python
def find_rotation_count(nums: list[int]) -> int:
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

## 5. Check if Array Is Sorted and Rotated (LeetCode 1752)

### Problem Statement
Given an array `nums`, return `true` if the array was originally sorted in non-decreasing order, then rotated some number of positions (including zero). Otherwise, return `false`.
There may be duplicates in the original array.

### Constraints
- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 100`

### Example
**Input:** `nums = [3,4,5,1,2]`
**Output:** `true`

### Python Block
```python
def check(nums: list[int]) -> bool:
    count = 0
    n = len(nums)
    for i in range(n):
        # Count number of decreases (including wrap around)
        if nums[i] > nums[(i + 1) % n]:
            count += 1
            if count > 1:
                return False
    return True
```
