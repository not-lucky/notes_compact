# Burst Balloons Solutions

## Problem: Burst Balloons
You are given `n` balloons, indexed from 0 to `n - 1`. Each balloon is painted with a number on it represented by an array `nums`. You are asked to burst all the balloons. If you burst the `i-th` balloon, you will get `nums[i - 1] * nums[i] * nums[i + 1]` coins. After the burst, the `i - 1` and `i + 1` then becomes adjacent. Find the maximum coins you can collect by bursting the balloons wisely.

### Constraints
- 1 <= n <= 300
- 0 <= nums[i] <= 100

### Examples
- Input: nums = [3, 1, 5, 8] -> Output: 167

### Implementation

```python
def max_coins(nums: list[int]) -> int:
    """
    Finds max coins by bursting balloons.
    Uses interval DP with 'last burst' insight.
    Time complexity: O(n^3)
    Space complexity: O(n^2)
    """
    # Add boundary balloons
    balls = [1] + nums + [1]
    n = len(balls)
    # dp[i][j] is max coins for balloons strictly between i and j
    dp = [[0] * n for _ in range(n)]

    # length is distance between i and j
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):
                # k is the LAST balloon to burst in range (i, j)
                coins = balls[i] * balls[k] * balls[j]
                dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + coins)

    return dp[0][n-1]
```

## Problem: Minimum Score Triangulation of Polygon
You have a convex polygon with `n` vertices. You want to triangulate the polygon into `n - 2` triangles. For each triangle, the weight of that triangle is the product of the values of its vertices, and the total weight of the triangulation is the sum of these weights. Return the minimum total weight of the triangulation of the polygon.

### Implementation

```python
def min_score_triangulation(values: list[int]) -> int:
    """
    Min weight to triangulate a polygon.
    Time complexity: O(n^3)
    Space complexity: O(n^2)
    """
    n = len(values)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            if length == 2:
                dp[i][j] = 0 # No triangles can be formed with 2 vertices
            else:
                dp[i][j] = float('inf')
                for k in range(i + 1, j):
                    score = values[i] * values[k] * values[j]
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + score)

    return dp[0][n-1]
```
