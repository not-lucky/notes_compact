# Matrix Search Solutions

## 1. Search a 2D Matrix

[LeetCode 74](https://leetcode.com/problems/search-a-2d-matrix/)

### Problem Description

You are given an `m x n` integer matrix `matrix` with the following two properties:

- Each row is sorted in non-decreasing order.
- The first integer of each row is greater than the last integer of the previous row.
  Given an integer `target`, return `true` if `target` is in `matrix` or `false` otherwise.

### Solution

```python
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1

    while left <= right:
        mid = left + (right - left) // 2
        row, col = divmod(mid, n)
        val = matrix[row][col]

        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False
```

- **Time Complexity**: O(log(m\*n))
- **Space Complexity**: O(1)

---

## 2. Search a 2D Matrix II

[LeetCode 240](https://leetcode.com/problems/search-a-2d-matrix-ii/)

### Problem Description

Write an efficient algorithm that searches for a value `target` in an `m x n` integer matrix `matrix`. This matrix has the following properties:

- Integers in each row are sorted in ascending from left to right.
- Integers in each column are sorted in ascending from top to bottom.

### Solution

```python
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1  # Start top-right

    while row < m and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1
        else:
            row += 1

    return False
```

- **Time Complexity**: O(m + n)
- **Space Complexity**: O(1)

---

## 3. Kth Smallest Element in a Sorted Matrix

[LeetCode 378](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/)

### Problem Description

Given an `n x n` matrix where each of the rows and columns is sorted in ascending order, return the `k`-th smallest element in the matrix.

### Solution

```python
def kthSmallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)

    def countLessEqual(val: int) -> int:
        count = 0
        row, col = n - 1, 0  # Start bottom-left
        while row >= 0 and col < n:
            if matrix[row][col] <= val:
                count += row + 1
                col += 1
            else:
                row -= 1
        return count

    left, right = matrix[0][0], matrix[n-1][n-1]
    res = left
    while left <= right:
        mid = left + (right - left) // 2
        if countLessEqual(mid) >= k:
            res = mid
            right = mid - 1
        else:
            left = mid + 1

    return res
```

- **Time Complexity**: O(n log(max-min))
- **Space Complexity**: O(1)

---

## 4. Count Negative Numbers in a Sorted Matrix

[LeetCode 1351](https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/)

### Problem Description

Given a `m x n` matrix `grid` which is sorted in non-increasing order both row-wise and column-wise, return the number of negative numbers in `grid`.

### Solution

```python
def countNegatives(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    count = 0
    row, col = m - 1, 0  # Start from bottom-left

    while row >= 0 and col < n:
        if grid[row][col] < 0:
            count += (n - col)
            row -= 1
        else:
            col += 1

    return count
```

- **Time Complexity**: O(m + n)
- **Space Complexity**: O(1)

---

## 5. Median of Row-Wise Sorted Matrix

[LeetCode Premium/GeeksforGeeks](https://www.geeksforgeeks.org/find-median-row-wise-sorted-matrix/)

### Problem Description

Given a row-wise sorted matrix of size `m x n` where `m x n` is always odd, find the median of the matrix.

### Solution

```python
import bisect

def findMedian(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    target = (m * n + 1) // 2

    def countLessEqual(val: int) -> int:
        count = 0
        for row in matrix:
            count += bisect.bisect_right(row, val)
        return count

    low = min(row[0] for row in matrix)
    high = max(row[-1] for row in matrix)

    while low < high:
        mid = low + (high - low) // 2
        if countLessEqual(mid) < target:
            low = mid + 1
        else:
            high = mid

    return low
```

- **Time Complexity**: O(m _ log n _ log(max-min))
- **Space Complexity**: O(1)

---

## 6. Row with Maximum Ones

[GeeksforGeeks](https://www.geeksforgeeks.org/find-the-row-with-maximum-number-1s/)

### Problem Description

Given a boolean 2D array, where each row is sorted. Find the row with the maximum number of 1s.

### Solution

```python
def rowWithMax1s(mat: list[list[int]]) -> int:
    m = len(mat)
    if m == 0: return -1
    n = len(mat[0])

    max_row_idx = -1
    j = n - 1  # Start from top-right corner

    for i in range(m):
        while j >= 0 and mat[i][j] == 1:
            j -= 1
            max_row_idx = i

    return max_row_idx
```

- **Time Complexity**: O(m + n)
- **Space Complexity**: O(1)
