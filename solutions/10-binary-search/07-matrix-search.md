# Practice Problems - Matrix Search

## 1. Search a 2D Matrix (LeetCode 74)

### Problem Statement
Write an efficient algorithm that searches for a value `target` in an `m x n` integer matrix `matrix`. This matrix has the following properties:
- Integers in each row are sorted from left to right.
- The first integer of each row is greater than the last integer of the previous row.

### Constraints
- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 100`
- `-10^4 <= matrix[i][j], target <= 10^4`

### Example
**Input:** `matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3`
**Output:** `true`

### Python Block
```python
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1

    while left <= right:
        mid = left + (right - left) // 2
        # Convert 1D index to 2D
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

## 2. Search a 2D Matrix II (LeetCode 240)

### Problem Statement
Write an efficient algorithm that searches for a value `target` in an `m x n` integer matrix `matrix`. This matrix has the following properties:
- Integers in each row are sorted in ascending from left to right.
- Integers in each column are sorted in ascending from top to bottom.

### Constraints
- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 300`
- `-10^9 <= matrix[i][j], target <= 10^9`

### Example
**Input:** `matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5`
**Output:** `true`

### Python Block
```python
def search_matrix_2(matrix: list[list[int]], target: int) -> bool:
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    # Start from top-right corner
    row, col = 0, n - 1

    while row < m and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            # Eliminate this column
            col -= 1
        else:
            # Eliminate this row
            row += 1

    return False
```

## 3. Kth Smallest Element in a Sorted Matrix (LeetCode 378)

### Problem Statement
Given an `n x n` `matrix` where each of the rows and columns is sorted in ascending order, return the `k-th` smallest element in the matrix.
Note that it is the `k-th` smallest element **in the sorted order**, not the `k-th` **distinct** element.
You must find a solution with a memory complexity better than `O(n^2)`.

### Constraints
- `n == matrix.length == matrix[i].length`
- `1 <= n <= 300`
- `-10^9 <= matrix[i][j] <= 10^9`
- `1 <= k <= n^2`

### Example
**Input:** `matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8`
**Output:** `13`

### Python Block
```python
def kth_smallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)

    def count_less_equal(mid: int) -> int:
        count = 0
        row, col = n - 1, 0
        while row >= 0 and col < n:
            if matrix[row][col] <= mid:
                # All elements above in this column are also <=
                count += row + 1
                col += 1
            else:
                row -= 1
        return count

    left, right = matrix[0][0], matrix[n - 1][n - 1]
    while left < right:
        mid = left + (right - left) // 2
        if count_less_equal(mid) < k:
            left = mid + 1
        else:
            right = mid
    return left
```

## 4. Count Negative Numbers in Sorted Matrix (LeetCode 1351)

### Problem Statement
Given a `m x n` matrix `grid` which is sorted in non-increasing order both row-wise and column-wise, return the number of negative numbers in `grid`.

### Constraints
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 100`
- `-100 <= grid[i][j] <= 100`

### Example
**Input:** `grid = [[4,3,2,-1],[3,2,1,-1],[1,1,-1,-2],[-1,-1,-2,-3]]`
**Output:** `8`

### Python Block
```python
def count_negatives(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    count = 0
    # Start from top-right
    row, col = 0, n - 1

    while row < m and col >= 0:
        if grid[row][col] < 0:
            # This whole column from this row down is negative
            count += (m - row)
            col -= 1
        else:
            row += 1
    return count
```

## 5. Median of Row-Wise Sorted Matrix

### Problem Statement
Given an `m x n` matrix `matrix` where each row is sorted in non-decreasing order, find the median of the matrix. `m * n` is always odd.

### Python Block
```python
import bisect

def find_median(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    target = (m * n + 1) // 2

    def count_less_equal(mid: int) -> int:
        count = 0
        for row in matrix:
            count += bisect.bisect_right(row, mid)
        return count

    left = min(row[0] for row in matrix)
    right = max(row[-1] for row in matrix)

    while left < right:
        mid = left + (right - left) // 2
        if count_less_equal(mid) < target:
            left = mid + 1
        else:
            right = mid
    return left
```

## 6. Row with Maximum Ones

### Problem Statement
Given a binary `m x n` matrix `matrix` where each row is sorted in non-decreasing order, find the row index with the maximum number of ones. If there are multiple rows, return any of them.

### Python Block
```python
def row_with_max_ones(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    max_row = -1
    # Start from top-right corner
    col = n - 1

    for row in range(m):
        # Move left as long as we see 1s
        while col >= 0 and matrix[row][col] == 1:
            col -= 1
            max_row = row

    return max_row
```
