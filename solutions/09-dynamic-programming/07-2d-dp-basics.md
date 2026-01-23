# 2D DP Basics Solutions

## Problem: Unique Paths
There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time. Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.

### Constraints
- 1 <= m, n <= 100

### Examples
- Input: m = 3, n = 7 -> Output: 28
- Input: m = 3, n = 2 -> Output: 3

### Implementation

```python
def unique_paths(m: int, n: int) -> int:
    """
    Counts unique paths using space-optimized 2D DP.
    Time complexity: O(m * n)
    Space complexity: O(n)
    """
    # dp[j] stores the number of ways to reach (i, j)
    # Initially all 1s for the first row
    dp = [1] * n

    for i in range(1, m):
        for j in range(1, n):
            # dp[j] = dp[j] (from above) + dp[j-1] (from left)
            dp[j] += dp[j - 1]

    return dp[n - 1]
```

## Problem: Minimum Path Sum
Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right, which minimizes the sum of all numbers along its path. You can only move either down or right at any point in time.

### Constraints
- m == grid.length, n == grid[i].length
- 1 <= m, n <= 200
- 0 <= grid[i][j] <= 200

### Examples
- Input: grid = [[1,3,1],[1,5,1],[4,2,1]] -> Output: 7 (1->3->1->1->1)

### Implementation

```python
def min_path_sum(grid: list[list[int]]) -> int:
    """
    Finds minimum path sum using space-optimized 2D DP.
    Time complexity: O(m * n)
    Space complexity: O(n)
    """
    m, n = len(grid), len(grid[0])
    dp = [float('inf')] * n
    dp[0] = 0

    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                dp[j] = grid[0][0]
            elif i == 0:
                dp[j] = dp[j-1] + grid[i][j]
            elif j == 0:
                dp[j] = dp[j] + grid[i][j]
            else:
                dp[j] = min(dp[j], dp[j-1]) + grid[i][j]

    return dp[n - 1]
```

## Problem: Maximal Square
Given an m x n binary matrix filled with 0's and 1's, find the largest square containing only 1's and return its area.

### Implementation

```python
def maximal_square(matrix: list[list[str]]) -> int:
    """
    Finds area of largest square of 1s.
    Time complexity: O(m * n)
    Space complexity: O(n)
    """
    if not matrix or not matrix[0]:
        return 0

    m, n = len(matrix), len(matrix[0])
    dp = [0] * (n + 1)
    max_side = 0
    prev_diag = 0 # dp[i-1][j-1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            temp = dp[j] # Save dp[i-1][j]
            if matrix[i-1][j-1] == '1':
                # dp[j] is dp[i-1][j], dp[j-1] is dp[i][j-1]
                dp[j] = min(dp[j], dp[j-1], prev_diag) + 1
                max_side = max(max_side, dp[j])
            else:
                dp[j] = 0
            prev_diag = temp

    return max_side * max_side
```
