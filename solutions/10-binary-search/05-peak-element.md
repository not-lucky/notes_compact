# Practice Problems - Peak Element

## 1. Find Peak Element (LeetCode 162)

### Problem Statement
A peak element is an element that is strictly greater than its neighbors.
Given a **0-indexed** integer array `nums`, find a peak element, and return its index. If the array contains multiple peaks, return the index to **any of the peaks**.
You may imagine that `nums[-1] = nums[n] = -∞`. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.
You must write an algorithm that runs in `O(log n)` time.

### Constraints
- `1 <= nums.length <= 1000`
- `-2^31 <= nums[i] <= 2^31 - 1`
- `nums[i] != nums[i + 1]` for all valid `i`.

### Example
**Input:** `nums = [1,2,3,1]`
**Output:** `2`

### Python Block
```python
def find_peak_element(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        # Follow the uphill direction
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid

    return left
```

## 2. Peak Index in Mountain Array (LeetCode 852)

### Problem Statement
An array `arr` is a **mountain** if the following properties hold:
- `arr.length >= 3`
- There exists some `i` with `0 < i < arr.length - 1` such that:
    - `arr[0] < arr[1] < ... < arr[i - 1] < arr[i]`
    - `arr[i] > arr[i + 1] > ... > arr[arr.length - 1]`
Given a mountain array `arr`, return the index `i` such that `arr[0] < arr[1] < ... < arr[i - 1] < arr[i] > arr[i + 1] > ... > arr[arr.length - 1]`.
You must solve it in `O(log(arr.length))` time complexity.

### Constraints
- `3 <= arr.length <= 10^5`
- `0 <= arr[i] <= 10^6`
- `arr` is guaranteed to be a mountain array.

### Example
**Input:** `arr = [0,1,0]`
**Output:** `1`

### Python Block
```python
def peak_index_in_mountain_array(arr: list[int]) -> int:
    left, right = 0, len(arr) - 1

    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid

    return left
```

## 3. Find in Mountain Array (LeetCode 1095)

### Problem Statement
(This problem requires a specific API `MountainArray`. Here is the implementation logic.)
Given a mountain array `mountainArr`, return the minimum `index` such that `mountainArr.get(index) == target`. If such an index does not exist, return `-1`.
You cannot access the mountain array directly. You may only access the array using a `MountainArray` interface.

### Python Block
```python
# This is the MountainArray's API interface.
# You should not implement it, or speculate about its implementation
# class MountainArray:
#    def get(self, index: int) -> int:
#    def length(self) -> int:

def find_in_mountain_array(target: int, mountain_arr: 'MountainArray') -> int:
    n = mountain_arr.length()

    # 1. Find the peak index
    left, right = 0, n - 1
    while left < right:
        mid = left + (right - left) // 2
        if mountain_arr.get(mid) < mountain_arr.get(mid + 1):
            left = mid + 1
        else:
            right = mid
    peak = left

    # 2. Binary search in the increasing part
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

    # 3. Binary search in the decreasing part
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

## 4. Find a Peak Element II (LeetCode 1901)

### Problem Statement
A **peak** element in a 2D grid is an element that is **strictly greater** than all of its **adjacent** neighbors to the left, right, top, and bottom.
Given a **0-indexed** `m x n` matrix `mat` where no two adjacent cells are equal, find **any** peak element `mat[i][j]` and return its length 2 array `[i, j]`.

### Constraints
- `m == mat.length`
- `n == mat[i].length`
- `1 <= m, n <= 500`
- `1 <= mat[i][j] <= 10^5`
- No two adjacent cells are equal.

### Example
**Input:** `mat = [[1,4],[3,2]]`
**Output:** `[0,1]` (4 is a peak)

### Python Block
```python
def find_peak_grid(mat: list[list[int]]) -> list[int]:
    rows = len(mat)
    cols = len(mat[0])
    left, right = 0, cols - 1

    while left <= right:
        mid_col = left + (right - left) // 2

        # Find max in this column
        max_row = 0
        for r in range(rows):
            if mat[r][mid_col] > mat[max_row][mid_col]:
                max_row = r

        # Check neighbors in adjacent columns
        left_is_greater = mid_col > 0 and mat[max_row][mid_col - 1] > mat[max_row][mid_col]
        right_is_greater = mid_col < cols - 1 and mat[max_row][mid_col + 1] > mat[max_row][mid_col]

        if not left_is_greater and not right_is_greater:
            return [max_row, mid_col]
        elif left_is_greater:
            right = mid_col - 1
        else:
            left = mid_col + 1

    return []
```

## 5. Longest Mountain in Array (LeetCode 845)

### Problem Statement
Given an integer array `arr`, return the length of the longest subarray, which is a mountain. Return `0` if there is no mountain subarray.

### Constraints
- `1 <= arr.length <= 10^4`
- `0 <= arr[i] <= 10^4`

### Example
**Input:** `arr = [2,1,4,7,3,2,5]`
**Output:** `5` ([1, 4, 7, 3, 2] is the longest mountain)

### Python Block
```python
def longest_mountain(arr: list[int]) -> int:
    n = len(arr)
    ans = 0
    base = 0

    while base < n:
        end = base
        # If we have a peak candidate
        if end + 1 < n and arr[end] < arr[end + 1]:
            # Climb up
            while end + 1 < n and arr[end] < arr[end + 1]:
                end += 1

            # If it's a real peak (we reached the top and there's a slope down)
            if end + 1 < n and arr[end] > arr[end + 1]:
                # Climb down
                while end + 1 < n and arr[end] > arr[end + 1]:
                    end += 1
                ans = max(ans, end - base + 1)
            else:
                end += 1
        else:
            end += 1
        base = max(base + 1, end if (end > base and not (end < n and arr[end-1] < arr[end])) else base + 1)
        # Simplified logic:
        # base = end if the current 'end' can't be part of next mountain start.
        # But safer to just move base.

    # Alternative clearer O(n) approach:
    res = 0
    for i in range(1, n - 1):
        if arr[i-1] < arr[i] > arr[i+1]: # Peak
            l = r = i
            while l > 0 and arr[l-1] < arr[l]: l -= 1
            while r < n - 1 and arr[r+1] < arr[r]: r += 1
            res = max(res, r - l + 1)
    return res
```
