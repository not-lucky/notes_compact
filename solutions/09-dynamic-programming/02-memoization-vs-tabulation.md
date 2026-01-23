# Memoization vs Tabulation Solutions

## Problem: Unique Paths
There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.

### Constraints
- 1 <= m, n <= 100

### Examples
- Input: m = 3, n = 7 -> Output: 28
- Input: m = 3, n = 2 -> Output: 3

### Implementation

```python
def unique_paths_memo(m: int, n: int) -> int:
    """
    Top-down memoization approach.
    Time complexity: O(m * n)
    Space complexity: O(m * n)
    """
    memo = {}
    def dp(i, j):
        if i == 0 or j == 0:
            return 1
        if (i, j) in memo:
            return memo[(i, j)]
        memo[(i, j)] = dp(i - 1, j) + dp(i, j - 1)
        return memo[(i, j)]
    return dp(m - 1, n - 1)

def unique_paths_tab(m: int, n: int) -> int:
    """
    Bottom-up tabulation approach.
    Time complexity: O(m * n)
    Space complexity: O(m * n)
    """
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]

def unique_paths_opt(m: int, n: int) -> int:
    """
    Space optimized tabulation approach.
    Time complexity: O(m * n)
    Space complexity: O(n)
    """
    dp = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            dp[j] = dp[j] + dp[j - 1]
    return dp[n - 1]
```
