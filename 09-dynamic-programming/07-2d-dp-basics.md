# 2D DP Basics

> **Prerequisites:** [1D DP Basics](./03-1d-dp-basics.md)

## Overview

2D Dynamic Programming uses a two-dimensional state `dp[i][j]` to represent the answers to subproblems that depend on two distinct parameters. This is common when traversing grids, comparing two sequences, or dealing with multiple constraints.

## Building Intuition

**Why do we need 2D DP?**

1. **Two Independent Dimensions**: When the state of a problem is defined by two independent variables—such as the row and column in a 2D grid, or the current item index and remaining capacity in a knapsack—a single dimension isn't enough to track all combinations.
2. **Grid Problems Are Natural 2D**: In a grid, reaching cell `(i, j)` usually depends on reaching adjacent cells like `(i-1, j)` and `(i, j-1)`. The state naturally maps to the grid coordinates.
3. **The Dependency Insight**: In 2D DP, `dp[i][j]` typically depends on:
   - `dp[i-1][j]` (the cell directly above)
   - `dp[i][j-1]` (the cell directly to the left)
   - `dp[i-1][j-1]` (the cell diagonally above-left)
   This predictable dependency structure dictates how we fill the DP table (usually row by row, left to right).
4. **Mental Model**: Think of the DP table as a spreadsheet. Each cell `(i, j)` contains the answer for a specific subproblem defined by `i` and `j`. You fill it systematically, and each cell's formula references previously calculated cells.

## When NOT to Use 2D DP

Before jumping to a 2D array, consider if it's the right tool:

1. **State Is Actually 1D**: Don't force 2D when 1D suffices. Problems like Fibonacci, Climbing Stairs, or House Robber only need one index to represent the state.
2. **State Requires 3+ Dimensions**: Some complex problems require tracking more parameters, leading to states like `dp[i][j][k]`.
3. **General Graphs (Non-Grids)**: 2D DP works well for grids where transitions only go in specific directions (forming a Directed Acyclic Graph). For general graphs with cycles, use shortest path algorithms like Dijkstra's or BFS.

---

## The Padding Trick (Dummy Cells)

A common source of bugs in 2D DP is boundary handling (checking `if i == 0` or `j == 0`). We can elegantly bypass this by adding an extra column and row of "dummy" values—often referred to as **padding**.

By making our DP array `(m + 1) x (n + 1)` instead of `m x n`, we let the `0`-th row and column act as out-of-bounds boundaries.
- For finding sums or paths, pad with `0`.
- For finding minimums, pad with `float('inf')`.
- For finding maximums, pad with `float('-inf')`.

Then, we carefully seed a single initial value that naturally flows into the `(1, 1)` cell calculation. This completely removes the need for boundary checks inside your loops, resulting in incredibly clean, readable code.

---

## Pattern 1: Grid Path Problems

Grid path problems are the classic introduction to 2D DP. You are asked to find the number of paths, the optimal path sum, or whether a path exists from top-left to bottom-right.

### Unique Paths (LeetCode 62)

Count the number of unique paths from the top-left corner to the bottom-right corner `(m-1, n-1)`. You can only move down or right.

**Formal Recurrence Relation:**
- **State:** Let `dp[i][j]` be the number of unique paths to reach cell `(i, j)`.
- **Recurrence:** `dp[i][j] = dp[i-1][j] + dp[i][j-1]` (Paths from above + paths from left).

#### Top-Down (Memoization)

```python
def unique_paths_memo(m: int, n: int) -> int:
    """
    Top-Down Memoization approach.
    Time: O(m * n), Space: O(m * n)
    """
    memo = {}

    def dfs(r: int, c: int) -> int:
        if r == 0 and c == 0:
            return 1
        if r < 0 or c < 0:
            return 0
        if (r, c) in memo:
            return memo[(r, c)]

        # Recurrence: paths from cell above + paths from cell left
        memo[(r, c)] = dfs(r - 1, c) + dfs(r, c - 1)
        return memo[(r, c)]

    return dfs(m - 1, n - 1)
```

#### Bottom-Up (Tabulation) with 2D Padding

Instead of bounds checking, we use a `(m+1) x (n+1)` padded array.

```python
def unique_paths(m: int, n: int) -> int:
    """
    Count unique paths in m x n grid using a padded 2D array.
    Time: O(m * n), Space: O(m * n)
    """
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Seed value: ensures dp[1][1] becomes 1 (start cell)
    dp[0][1] = 1 
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Paths to current = paths from above + paths from left
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

    return dp[m][n]
```

### Unique Paths II (With Obstacles) (LeetCode 63)

Similar to the previous problem, but the grid contains obstacles (`1` represents an obstacle).

#### Top-Down (Memoization)

```python
def unique_paths_with_obstacles_memo(obstacle_grid: list[list[int]]) -> int:
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    memo = {}

    def dfs(r: int, c: int) -> int:
        if r < 0 or c < 0 or obstacle_grid[r][c] == 1:
            return 0
        if r == 0 and c == 0:
            return 1
        if (r, c) in memo:
            return memo[(r, c)]
            
        memo[(r, c)] = dfs(r - 1, c) + dfs(r, c - 1)
        return memo[(r, c)]

    return dfs(m - 1, n - 1)
```

#### Bottom-Up (Tabulation)

Notice how easily the padding trick adapts to obstacles without any spaghetti code:

```python
def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    """
    Time: O(m * n), Space: O(m * n)
    """
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    dp[0][1] = 1 # Seed value
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if obstacle_grid[i - 1][j - 1] == 1:
                dp[i][j] = 0 # Obstacle blocks all paths
            else:
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

    return dp[m][n]
```

### Minimum Path Sum (LeetCode 64)

Find a path from top-left to bottom-right that minimizes the sum of all numbers along its path.

#### Top-Down (Memoization)

```python
def min_path_sum_memo(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    memo = {}

    def dfs(r: int, c: int) -> int:
        if r < 0 or c < 0:
            return float('inf')
        if r == 0 and c == 0:
            return grid[0][0]
        if (r, c) in memo:
            return memo[(r, c)]
            
        memo[(r, c)] = grid[r][c] + min(dfs(r - 1, c), dfs(r, c - 1))
        return memo[(r, c)]

    return dfs(m - 1, n - 1)
```

#### Bottom-Up (Tabulation)

```python
def min_path_sum(grid: list[list[int]]) -> int:
    """
    Time: O(m * n), Space: O(m * n)
    """
    m, n = len(grid), len(grid[0])
    
    # Pad with infinity to handle boundaries cleanly
    dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]
    
    # Dummy base case: reaching the start of the grid costs 0
    # This ensures dp[1][1] = grid[0][0] + min(inf, 0) = grid[0][0]
    dp[0][1] = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + grid[i - 1][j - 1]

    return dp[m][n]
```

---

## Pattern 2: Bottom-Up Triangles & Grids

Sometimes problems dictate movement from top to bottom but let you start or end anywhere on a row. Working **bottom-up** is often mathematically cleaner.

### Triangle (LeetCode 120)

Find the minimum path sum from top to bottom of a triangle. You can move to adjacent numbers on the row below (`(i+1, j)` or `(i+1, j+1)`).

#### Top-Down (Memoization)

```python
def minimum_total_memo(triangle: list[list[int]]) -> int:
    n = len(triangle)
    memo = {}

    def dfs(r: int, c: int) -> int:
        if r == n:
            return 0
        if (r, c) in memo:
            return memo[(r, c)]
            
        memo[(r, c)] = triangle[r][c] + min(dfs(r + 1, c), dfs(r + 1, c + 1))
        return memo[(r, c)]

    return dfs(0, 0)
```

#### Bottom-Up (Tabulation)

**Key Insight for Bottom-Up:** Process bottom-up, starting from the base of the triangle.

```python
def minimum_total(triangle: list[list[int]]) -> int:
    """
    Time: O(N^2) where N is the number of rows
    Space: O(N^2) for 2D DP
    """
    n = len(triangle)
    dp = [[0] * len(row) for row in triangle]
    
    # Initialize DP array with the bottom row of the triangle
    for j in range(len(triangle[-1])):
        dp[-1][j] = triangle[-1][j]

    # Start from the second to last row, moving upwards
    for i in range(n - 2, -1, -1):
        for j in range(len(triangle[i])):
            # Current cell + min of the two possible choices below it
            dp[i][j] = triangle[i][j] + min(dp[i + 1][j], dp[i + 1][j + 1])

    return dp[0][0]
```

---


### Minimum Falling Path Sum (LeetCode 931)

A natural progression from Triangle is `Minimum Falling Path Sum`. Given an `n x n` integer matrix, find the minimum sum of any falling path through the matrix. You can start anywhere in the first row and move to the element directly below or diagonally left/right.

**State Definition:**
Let `dp[i][j]` be the minimum path sum reaching cell `(i, j)`. It depends on the minimum of three adjacent cells from the row above: `dp[i-1][j-1]`, `dp[i-1][j]`, and `dp[i-1][j+1]`.

#### Top-Down (Memoization)

```python
def min_falling_path_sum_memo(matrix: list[list[int]]) -> int:
    n = len(matrix)
    memo = {}

    def dfs(r: int, c: int) -> int:
        if c < 0 or c >= n:
            return float('inf')
        if r == 0:
            return matrix[0][c]
        if (r, c) in memo:
            return memo[(r, c)]
            
        # Current cell + min of 3 valid paths from the row above
        memo[(r, c)] = matrix[r][c] + min(
            dfs(r - 1, c - 1),
            dfs(r - 1, c),
            dfs(r - 1, c + 1)
        )
        return memo[(r, c)]

    # Try starting from each column in the last row (working bottom-up conceptually for DP)
    return min(dfs(n - 1, c) for c in range(n))
```

#### Bottom-Up (Tabulation)

For the bottom-up approach, we can overwrite the matrix in place (or use an identical DP array), starting from the second row and working downwards.

```python
def min_falling_path_sum(matrix: list[list[int]]) -> int:
    n = len(matrix)
    
    # We can modify the matrix in place to save space (O(1) extra space)
    for r in range(1, n):
        for c in range(n):
            # Boundaries check for the 3 choices
            left = matrix[r - 1][c - 1] if c > 0 else float('inf')
            mid = matrix[r - 1][c]
            right = matrix[r - 1][c + 1] if c < n - 1 else float('inf')
            
            matrix[r][c] += min(left, mid, right)
            
    return min(matrix[-1])
```

## Pattern 3: Square & Diagonal Dependencies

### Maximal Square (LeetCode 221)

Find the largest square containing only `1`s in a binary matrix.

**State Definition Insight:**
Let `dp[i][j]` be the side length of the largest square whose **bottom-right corner** is at `(i-1, j-1)` in the original matrix.
It is constrained by the smallest of its three neighboring squares (left, above, and diagonally above-left).

#### Top-Down (Memoization)

```python
def maximal_square_memo(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0
        
    m, n = len(matrix), len(matrix[0])
    memo = {}
    max_side = 0

    def dfs(r: int, c: int) -> int:
        nonlocal max_side
        if r >= m or c >= n:
            return 0
        if (r, c) in memo:
            return memo[(r, c)]
            
        right = dfs(r, c + 1)
        down = dfs(r + 1, c)
        diag = dfs(r + 1, c + 1)
        
        if matrix[r][c] == '1':
            memo[(r, c)] = 1 + min(right, down, diag)
            max_side = max(max_side, memo[(r, c)])
        else:
            memo[(r, c)] = 0
            
        return memo[(r, c)]

    dfs(0, 0) # Trigger calculation
    return max_side * max_side
```

#### Bottom-Up (Tabulation)

```python
def maximal_square(matrix: list[list[str]]) -> int:
    """
    Time: O(m * n), Space: O(m * n)
    """
    if not matrix or not matrix[0]:
        return 0

    m, n = len(matrix), len(matrix[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_side = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == '1':
                # Depends on left, top, and top-left diagonal
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                max_side = max(max_side, dp[i][j])

    return max_side * max_side
```

---

## Pattern 4: Backwards State Modeling

### Dungeon Game (LeetCode 174)

Find the minimum initial health needed to navigate a dungeon from top-left to bottom-right, keeping health `> 0`. Cells contain potions (positive) or demons (negative).

**Key Insight:** Processing top-down requires tracking *both* current health and minimum health seen so far. Processing **bottom-up** (from destination to start) simplifies the state: "What is the minimum health I need at this cell to survive?"

#### Top-Down (Memoization)

```python
def calculate_minimum_hp_memo(dungeon: list[list[int]]) -> int:
    m, n = len(dungeon), len(dungeon[0])
    memo = {}

    def dfs(r: int, c: int) -> int:
        if r >= m or c >= n:
            return float('inf')
        
        if r == m - 1 and c == n - 1:
            return max(1, 1 - dungeon[r][c])
            
        if (r, c) in memo:
            return memo[(r, c)]
            
        min_hp_on_exit = min(dfs(r + 1, c), dfs(r, c + 1))
        memo[(r, c)] = max(1, min_hp_on_exit - dungeon[r][c])
        return memo[(r, c)]

    return dfs(0, 0)
```

#### Bottom-Up (Tabulation)

```python
def calculate_minimum_hp(dungeon: list[list[int]]) -> int:
    """
    Process backwards to simplify state.
    Time: O(m * n), Space: O(m * n)
    """
    m, n = len(dungeon), len(dungeon[0])
    dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]

    # Base cases: we need at least 1 HP after exiting the bottom-right room
    dp[m][n - 1] = 1
    dp[m - 1][n] = 1

    # Iterate backwards
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            min_hp_on_exit = min(dp[i + 1][j], dp[i][j + 1])
            # We need enough HP to exit, minus what this room gives/takes.
            # We also must ALWAYS have at least 1 HP to stay alive.
            dp[i][j] = max(1, min_hp_on_exit - dungeon[i][j])

    return dp[0][0]
```

---

## Pattern 5: Multi-dimensional State Reduction

### Cherry Pickup (LeetCode 741)

Two robots start from opposite corners and collect cherries. Find the maximum cherries they can collect. This is mathematically equivalent to two robots starting at `(0,0)` and moving simultaneously to `(n-1, n-1)`.

**Key Insight:** A naive state is `dp[r1][c1][r2][c2]` (4D). But since they move simultaneously, they take the same number of steps. Thus, `r1 + c1 = r2 + c2`. We can deduce `r2` from `r1`, `c1`, and `c2`, reducing the state to 3D. 

Top-down memoization makes this much easier to reason about than a 3D/2D bottom-up loop.

```python
def cherry_pickup(grid: list[list[int]]) -> int:
    """
    Two robots moving simultaneously. Reduced from 4D to 3D State.
    Time: O(N^3), Space: O(N^3) due to recursion stack & memo.
    """
    n = len(grid)
    memo = {}

    def dp(r1: int, c1: int, c2: int) -> int:
        r2 = r1 + c1 - c2 # Deduce r2
        
        # Out of bounds or obstacle check
        if (r1 == n or r2 == n or c1 == n or c2 == n or 
            grid[r1][c1] == -1 or grid[r2][c2] == -1):
            return float('-inf')
            
        # Base case: reached the end
        if r1 == n - 1 and c1 == n - 1:
            return grid[r1][c1]
            
        if (r1, c1, c2) in memo:
            return memo[(r1, c1, c2)]

        # Collect cherries
        if c1 == c2: # Both on the same cell, collect once
            cherries = grid[r1][c1]
        else:        # On different cells, collect both
            cherries = grid[r1][c1] + grid[r2][c2]

        # 4 Possible transitions:
        # (Robot 1 moves Down/Right) x (Robot 2 moves Down/Right)
        res = max(
            dp(r1 + 1, c1, c2),     # R1 down, R2 down
            dp(r1, c1 + 1, c2 + 1), # R1 right, R2 right
            dp(r1 + 1, c1, c2 + 1), # R1 down, R2 right
            dp(r1, c1 + 1, c2)      # R1 right, R2 down
        )
        
        memo[(r1, c1, c2)] = res + cherries
        return memo[(r1, c1, c2)]

    return max(0, dp(0, 0, 0))
```

---

## Deep Dive: Space Optimization (2D → 1D)

Once you understand 2D DP, the next level is optimizing the space complexity from $O(M \times N)$ to $O(N)$.

If we analyze the standard recurrence: `dp[i][j] = dp[i-1][j] + dp[i][j-1]`
To compute the values for the current row `i`, we **ONLY** need values from the *immediately preceding row* `i-1`. Any older rows are obsolete.

We can achieve this with a **single 1D array** by overwriting values in-place as we iterate left-to-right:
- `dp[j]` represents the value from the row above (`dp[i-1][j]`).
- `dp[j-1]` represents the freshly updated value from the left (`dp[i][j-1]`).

**Example: Minimum Path Sum (1D Optimized)**

```python
def min_path_sum_optimized(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [float('inf')] * (n + 1)
    dp[1] = 0 # Seed

    for i in range(m):
        for j in range(n):
            # min(dp[j+1] -> above, dp[j] -> left)
            dp[j + 1] = min(dp[j + 1], dp[j]) + grid[i][j]

    return dp[n]
```
*Warning: While impressive in interviews, write the 2D version first. 1D optimization makes code harder to debug and requires caching temporary variables if your recurrence uses diagonals (`dp[i-1][j-1]`).*

---

## Practice Problems

| # | Problem | Difficulty | Pattern / Focus |
| :--- | :--- | :--- | :--- |
| [62](https://leetcode.com/problems/unique-paths/) | Unique Paths | Medium | Basic 2D grid traversal |
| [63](https://leetcode.com/problems/unique-paths-ii/) | Unique Paths II | Medium | Grid traversal with obstacles |
| [64](https://leetcode.com/problems/minimum-path-sum/) | Minimum Path Sum | Medium | Path optimization |
| [120](https://leetcode.com/problems/triangle/) | Triangle | Medium | Bottom-up DP |
| [931](https://leetcode.com/problems/minimum-falling-path-sum/) | Minimum Falling Path Sum | Medium | Bottom-up DP (Square Grid) |
| [221](https://leetcode.com/problems/maximal-square/) | Maximal Square | Medium | Using diagonal dependencies |
| [174](https://leetcode.com/problems/dungeon-game/) | Dungeon Game | Hard | Backwards state modeling |
| [741](https://leetcode.com/problems/cherry-pickup/) | Cherry Pickup | Hard | Multi-dimensional state reduction |

---

## Key Takeaways

1. **Grid DP**: `dp[i][j]` generally depends on its immediate neighbors (above, left, diagonal).
2. **The Padding Trick**: Pad your 2D arrays with an extra row and column to completely eliminate `if/else` boundary logic inside your loops.
3. **Direction Matters**: Sometimes it is significantly easier to process the state backwards (bottom-up or from destination to start).
4. **State Reduction**: Multi-agent problems can often have their state dimensions reduced by finding constraints (like `steps = r1 + c1`).
5. **Space Optimization**: 2D DP arrays can frequently be reduced to 1D arrays by overwriting the active row in place, but master the 2D version first!

---

## Next: [Longest Common Subsequence](./08-longest-common-subsequence.md)

Learn how to apply 2D DP to string comparison problems using the Longest Common Subsequence pattern.
