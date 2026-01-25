# Peak Element Solutions

## 1. Find Peak Element
[LeetCode 162](https://leetcode.com/problems/find-peak-element/)

### Problem Description
A peak element is an element that is strictly greater than its neighbors. Given a `0`-indexed integer array `nums`, find a peak element, and return its index. If the array contains multiple peaks, return the index to any of the peaks. You may imagine that `nums[-1] = nums[n] = -∞`.

### Solution
```python
def findPeakElement(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < nums[mid + 1]:
            # We are on an uphill slope, peak must be on the right
            left = mid + 1
        else:
            # We are on a downhill slope, peak could be mid or to the left
            right = mid

    return left
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 2. Peak Index in a Mountain Array
[LeetCode 852](https://leetcode.com/problems/peak-index-in-a-mountain-array/)

### Problem Description
An array `arr` is a mountain if:
- `arr.length >= 3`
- There exists some `i` with `0 < i < arr.length - 1` such that:
  - `arr[0] < arr[1] < ... < arr[i - 1] < arr[i]`
  - `arr[i] > arr[i + 1] > ... > arr[arr.length - 1]`
Given a mountain array `arr`, return the index `i` such that `arr[0] < arr[1] < ... < arr[i - 1] < arr[i] > arr[i + 1] > ... > arr[arr.length - 1]`.

### Solution
```python
def peakIndexInMountainArray(arr: list[int]) -> int:
    left, right = 0, len(arr) - 1

    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid

    return left
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 3. Find in Mountain Array
[LeetCode 1095](https://leetcode.com/problems/find-in-mountain-array/)

### Problem Description
Given a mountain array `mountainArr`, return the minimum `index` such that `mountainArr.get(index) == target`. If such an index does not exist, return `-1`.

### Solution
```python
# """
# This is MountainArray's API interface.
# You should not implement it, or speculate about its implementation
# """
# class MountainArray:
#    def get(self, index: int) -> int:
#    def length(self) -> int:

def findInMountainArray(target: int, mountain_arr: 'MountainArray') -> int:
    n = mountain_arr.length()

    # 1. Find the peak
    left, right = 0, n - 1
    while left < right:
        mid = left + (right - left) // 2
        if mountain_arr.get(mid) < mountain_arr.get(mid + 1):
            left = mid + 1
        else:
            right = mid
    peak = left

    # 2. Search in the ascending part
    left, right = 0, peak
    while left <= right:
        mid = left + (right - left) // 2
        val = mountain_arr.get(mid)
        if val == target:
            return mid
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1

    # 3. Search in the descending part
    left, right = peak + 1, n - 1
    while left <= right:
        mid = left + (right - left) // 2
        val = mountain_arr.get(mid)
        if val == target:
            return mid
        elif val > target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 4. Find a Peak Element II (2D)
[LeetCode 1901](https://leetcode.com/problems/find-a-peak-element-ii/)

### Problem Description
A peak element in a 2D grid is an element that is strictly greater than all of its adjacent neighbors to the left, right, top, and bottom. Given a 0-indexed `m x n` matrix `mat` where no two adjacent cells are equal, find any peak element `[r, c]` and return the length 2 array `[r, c]`.

### Solution
```python
def findPeakGrid(mat: list[list[int]]) -> list[int]:
    rows = len(mat)
    cols = len(mat[0])

    left_col, right_col = 0, cols - 1

    while left_col <= right_col:
        mid_col = left_col + (right_col - left_col) // 2

        # Find global max in mid_col
        max_row = 0
        for r in range(rows):
            if mat[r][mid_col] > mat[max_row][mid_col]:
                max_row = r

        # Check neighbors in the same row
        left_is_greater = mid_col > 0 and mat[max_row][mid_col - 1] > mat[max_row][mid_col]
        right_is_greater = mid_col < cols - 1 and mat[max_row][mid_col + 1] > mat[max_row][mid_col]

        if not left_is_greater and not right_is_greater:
            return [max_row, mid_col]
        elif left_is_greater:
            right_col = mid_col - 1
        else:
            left_col = mid_col + 1

    return [-1, -1]
---

## 5. Longest Mountain in Array
[LeetCode 845](https://leetcode.com/problems/longest-mountain-in-array/)

### Problem Description
Given an integer array `arr`, return the length of the longest subarray, which is a mountain. Return `0` if there is no mountain subarray.
Recall that an array `arr` is a mountain subarray if and only if:
- `arr.length >= 3`
- There exists some index `i` (`0 < i < arr.length - 1`) such that:
    - `arr[0] < arr[1] < ... < arr[i - 1] < arr[i]`
    - `arr[i] > arr[i + 1] > ... > arr[arr.length - 1]`

### Solution
```python
def longestMountain(arr: list[int]) -> int:
    n = len(arr)
    res = 0

    for i in range(1, n - 1):
        # Check if i is a peak
        if arr[i-1] < arr[i] > arr[i+1]:
            # Expand left
            left = i - 1
            while left > 0 and arr[left-1] < arr[left]:
                left -= 1

            # Expand right
            right = i + 1
            while right < n - 1 and arr[right+1] < arr[right]:
                right += 1

            res = max(res, right - left + 1)

    return res
```
- **Time Complexity**: O(n)
- **Space Complexity**: O(1)
