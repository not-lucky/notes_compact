2# Practice Problems - First and Last Occurrence

## 1. Find First and Last Position of Element in Sorted Array (LeetCode 34)

### Problem Statement
Given an array of integers `nums` sorted in non-decreasing order, find the starting and ending position of a given `target` value. If `target` is not found in the array, return `[-1, -1]`.

You must write an algorithm with `O(log n)` runtime complexity.

### Constraints
- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `nums` is a non-decreasing array.
- `-10^9 <= target <= 10^9`

### Example
**Input:** `nums = [5,7,7,8,8,10], target = 8`
**Output:** `[3, 4]`

### Python Block
```python
def search_range(nums: list[int], target: int) -> list[int]:
    def find_boundary(find_first: bool) -> int:
        left, right = 0, len(nums) - 1
        result = -1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                result = mid
                if find_first:
                    right = mid - 1
                else:
                    left = mid + 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result

    return [find_boundary(True), find_boundary(False)]
```

## 2. Find Smallest Letter Greater Than Target (LeetCode 744)

### Problem Statement
You are given an array of characters `letters` that is sorted in non-decreasing order, and a character `target`. There are at least two unique characters in `letters`.
Return the smallest character in `letters` that is lexicographically greater than `target`. If such a character does not exist, return the first character in `letters`.

### Constraints
- `2 <= letters.length <= 10^4`
- `letters[i]` is a lowercase English letter.
- `letters` is sorted in non-decreasing order.
- `letters` contains at least two unique characters.
- `target` is a lowercase English letter.

### Example
**Input:** `letters = ["c","f","j"], target = "a"`
**Output:** `"c"`

### Python Block
```python
def next_greatest_letter(letters: list[str], target: str) -> str:
    left, right = 0, len(letters) - 1

    # If target is greater than or equal to the last letter, wrap around
    if target >= letters[-1]:
        return letters[0]

    while left < right:
        mid = left + (right - left) // 2
        if letters[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return letters[left]
```

## 3. Single Element in a Sorted Array (LeetCode 540)

### Problem Statement
You are given a sorted array consisting of only integers where every element appears exactly twice, except for one element which appears exactly once.
Return the single element that appears only once.
Your solution must run in `O(log n)` time and `O(1)` space.

### Constraints
- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^5`

### Example
**Input:** `nums = [1,1,2,3,3,4,4,8,8]`
**Output:** `2`

### Python Block
```python
def single_non_duplicate(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        # Ensure mid is even for easy pair checking
        if mid % 2 == 1:
            mid -= 1

        # If the pair is intact (nums[mid] == nums[mid+1]),
        # the single element is to the right.
        if nums[mid] == nums[mid + 1]:
            left = mid + 2
        else:
            # Otherwise, the single element is to the left or is mid itself.
            right = mid

    return nums[left]
```

## 4. Find Minimum in Rotated Sorted Array (LeetCode 153)

### Problem Statement
Suppose an array of length `n` sorted in ascending order is rotated between `1` and `n` times. For example, the array `nums = [0,1,2,4,5,6,7]` might become:
- `[4,5,6,7,0,1,2]` if it was rotated 4 times.
- `[0,1,2,4,5,6,7]` if it was rotated 7 times.

Given the sorted rotated array `nums` of unique elements, return the minimum element of this array.
You must write an algorithm that runs in `O(log n)` time.

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
        # Compare mid with right boundary
        if nums[mid] > nums[right]:
            # Minimum is in the right half
            left = mid + 1
        else:
            # Minimum is in the left half (including mid)
            right = mid

    return nums[left]
```

## 5. Search Insert Position (LeetCode 35)

### Problem Statement
Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

### Constraints
- `1 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` contains distinct values sorted in ascending order.
- `-10^4 <= target <= 10^4`

### Example
**Input:** `nums = [1,3,5,6], target = 2`
**Output:** `1`

### Python Block
```python
def search_insert(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return left
```
