# 2D DP Basics

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

2D DP uses a two-dimensional state dp[i][j] representing answers for subproblems involving two indices, positions, or parameters.

## Building Intuition

**Why do we need 2D DP?**

1. **Two Independent Dimensions**: When the state of a problem depends on two independent variables—like position in two strings, row and column in a grid, or items and capacity—we need two dimensions to track all combinations.

2. **Grid Problems Are Natural 2D**: In a grid, reaching cell (i, j) depends on cells (i-1, j) and (i, j-1). The state naturally has two coordinates.

3. **String Comparison Needs Pairs**: For LCS or Edit Distance, we compare s1[0..i] with s2[0..j]. The answer for each (i, j) pair is different—1D can't capture this.

4. **The Dependency Insight**: In 2D DP, dp[i][j] typically depends on:
   - dp[i-1][j] (above), dp[i][j-1] (left), dp[i-1][j-1] (diagonal)
   - This determines the filling order: row by row or by increasing diagonal

5. **Space Optimization Key**: Since dp[i][j] usually only depends on row i-1 and the current row i, we can often reduce O(m×n) space to O(n) by keeping only one or two rows.

6. **Mental Model**: Think of a spreadsheet where each cell (i, j) contains the answer for "first i elements of X and first j elements of Y." You fill it systematically, and each cell formula references cells above, left, or diagonally above-left.

## Interview Context

2D DP problems are common because:

1. **Grid traversal**: Natural 2D structure
2. **Two sequences**: Compare strings/arrays
3. **Two parameters**: Capacity and items
4. **Space optimization**: 2D → 1D reduction

---

## When NOT to Use 2D DP

1. **State Is Actually 1D**: Don't force 2D when 1D suffices. Fibonacci, House Robber—these only need one index.

2. **State Requires 3+ Dimensions**: Some problems need dp[i][j][k] (like 3D grid or stock with k transactions). Recognizing this prevents wrong solutions.

3. **Non-Grid Graphs**: 2D DP works for grids (DAGs). For general graphs with cycles, use shortest path algorithms (Dijkstra, Bellman-Ford), not DP.

4. **Sparse State Space**: If only a few (i, j) pairs are valid, use memoization with a dictionary instead of a 2D array to save space.

5. **Dependencies Aren't Local**: If dp[i][j] depends on all dp[k][l] for k < i and l < j (not just neighbors), you may still get O(n²) per cell, giving O(n⁴) total. Consider optimization techniques.

**Signs 2D DP is Appropriate:**
- Two input sequences/arrays being compared
- Grid with row and column indices
- Knapsack-like problems with items and capacity
- Dependencies only on adjacent cells

---

## Pattern 1: Grid Path Problems

### Unique Paths

Count paths from top-left to bottom-right (only right/down moves).

```python
def unique_paths(m: int, n: int) -> int:
    """
    Count unique paths in m×n grid.

    State: dp[i][j] = paths to reach (i, j)
    Recurrence: dp[i][j] = dp[i-1][j] + dp[i][j-1]

    Time: O(m × n)
    Space: O(n)
    """
    dp = [1] * n  # First row all 1s

    for i in range(1, m):
        for j in range(1, n):
            dp[j] = dp[j] + dp[j - 1]

    return dp[n - 1]
```

### Unique Paths II (With Obstacles)

```python
def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    """
    Count paths avoiding obstacles (1 = obstacle).

    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(grid), len(grid[0])

    if grid[0][0] == 1:
        return 0

    dp = [0] * n
    dp[0] = 1

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] = dp[j] + dp[j - 1]

    return dp[n - 1]
```

### Minimum Path Sum

```python
def min_path_sum(grid: list[list[int]]) -> int:
    """
    Minimum sum path from top-left to bottom-right.

    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(grid), len(grid[0])
    dp = [float('inf')] * n
    dp[0] = 0

    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                dp[j] = grid[0][0]
            elif i == 0:
                dp[j] = dp[j - 1] + grid[i][j]
            elif j == 0:
                dp[j] = dp[j] + grid[i][j]
            else:
                dp[j] = min(dp[j], dp[j - 1]) + grid[i][j]

    return dp[n - 1]
```

---

## Pattern 2: Triangle

```python
def minimum_total(triangle: list[list[int]]) -> int:
    """
    Minimum path sum from top to bottom of triangle.

    Process bottom-up for cleaner code.

    Time: O(n²)
    Space: O(n)
    """
    n = len(triangle)
    dp = triangle[-1][:]  # Start with bottom row

    for i in range(n - 2, -1, -1):
        for j in range(len(triangle[i])):
            dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])

    return dp[0]
```

---

## Pattern 3: Maximum Square

```python
def maximal_square(matrix: list[list[str]]) -> int:
    """
    Find largest square of 1s.

    State: dp[i][j] = side length of largest square ending at (i,j)
    Recurrence: dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1

    Time: O(m × n)
    Space: O(n)
    """
    if not matrix:
        return 0

    m, n = len(matrix), len(matrix[0])
    dp = [0] * n
    max_side = 0
    prev = 0

    for i in range(m):
        for j in range(n):
            temp = dp[j]
            if matrix[i][j] == '1':
                if i == 0 or j == 0:
                    dp[j] = 1
                else:
                    dp[j] = min(dp[j], dp[j - 1], prev) + 1
                max_side = max(max_side, dp[j])
            else:
                dp[j] = 0
            prev = temp

    return max_side * max_side
```

---

## Pattern 4: Dungeon Game

```python
def calculate_minimum_hp(dungeon: list[list[int]]) -> int:
    """
    Minimum initial HP to reach bottom-right with HP > 0.

    Process backwards from destination.

    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(dungeon), len(dungeon[0])
    dp = [float('inf')] * (n + 1)
    dp[n - 1] = 1  # Need at least 1 HP at destination

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            min_hp = min(dp[j], dp[j + 1]) - dungeon[i][j]
            dp[j] = max(1, min_hp)  # Need at least 1 HP

    return dp[0]
```

---

## Pattern 5: Cherry Pickup

Two robots collecting cherries simultaneously.

```python
def cherry_pickup(grid: list[list[int]]) -> int:
    """
    Two robots start from corners, collect max cherries.

    State: dp[i][j1][j2] = max cherries when both at row i,
           robot1 at col j1, robot2 at col j2

    Time: O(m × n²)
    Space: O(n²)
    """
    m, n = len(grid), len(grid[0])

    # dp[j1][j2] = max cherries with robot1 at j1, robot2 at j2
    dp = [[float('-inf')] * n for _ in range(n)]
    dp[0][n - 1] = grid[0][0] + grid[0][n - 1]

    for i in range(1, m):
        new_dp = [[float('-inf')] * n for _ in range(n)]

        for j1 in range(n):
            for j2 in range(n):
                if dp[j1][j2] == float('-inf'):
                    continue

                # Try all combinations of moves
                for d1 in [-1, 0, 1]:
                    for d2 in [-1, 0, 1]:
                        nj1, nj2 = j1 + d1, j2 + d2

                        if 0 <= nj1 < n and 0 <= nj2 < n:
                            cherries = grid[i][nj1]
                            if nj1 != nj2:
                                cherries += grid[i][nj2]
                            new_dp[nj1][nj2] = max(
                                new_dp[nj1][nj2],
                                dp[j1][j2] + cherries
                            )

        dp = new_dp

    return max(max(row) for row in dp)
```

---

## Space Optimization Techniques

### 2D → 1D Reduction

When dp[i][j] depends only on dp[i-1][...] and dp[i][j-1]:

```python
# Original O(m × n) space
dp = [[0] * n for _ in range(m)]
for i in range(m):
    for j in range(n):
        dp[i][j] = f(dp[i-1][j], dp[i][j-1])

# Optimized O(n) space
dp = [0] * n
for i in range(m):
    for j in range(n):
        dp[j] = f(dp[j], dp[j-1])  # dp[j] is previous row's value
```

### When We Need dp[i-1][j-1]

```python
# Need to save dp[i-1][j-1] before overwriting
dp = [0] * n
for i in range(m):
    prev = 0  # dp[i-1][j-1]
    for j in range(n):
        temp = dp[j]  # Save before overwriting
        dp[j] = f(dp[j], dp[j-1], prev)
        prev = temp
```

---

## Common Mistakes

```python
# WRONG: Wrong iteration direction for space optimization
dp = [0] * n
for i in range(m):
    for j in range(n):  # Left to right
        dp[j] = dp[j] + dp[j-1]  # dp[j-1] already updated!

# CORRECT for some problems: Right to left
for j in range(n-1, -1, -1):
    dp[j] = dp[j] + dp[j+1]


# WRONG: Forgetting boundary initialization
for i in range(m):
    for j in range(n):
        dp[i][j] = dp[i-1][j] + dp[i][j-1]  # IndexError at i=0 or j=0

# CORRECT: Handle boundaries
if i == 0:
    dp[i][j] = dp[i][j-1] + grid[i][j]
elif j == 0:
    dp[i][j] = dp[i-1][j] + grid[i][j]
else:
    dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
```

---

## Visual: 2D DP State Transitions

```
Unique Paths:
  0   1   2   3
0 [1] [1] [1] [1]
1 [1] [2] [3] [4]
2 [1] [3] [6] [10]

dp[i][j] = dp[i-1][j] + dp[i][j-1]
         =    ↑      +    ←


Minimum Path Sum:
  1   3   1
  1   5   1
  4   2   1

  1   4   5
  2   7   6
  6   8   7  ← Answer
```

---

## Complexity Summary

| Problem | Time | Space | Optimized Space |
|---------|------|-------|-----------------|
| Unique Paths | O(mn) | O(mn) | O(n) |
| Min Path Sum | O(mn) | O(mn) | O(n) |
| Maximum Square | O(mn) | O(mn) | O(n) |
| Triangle | O(n²) | O(n²) | O(n) |
| Cherry Pickup | O(mn²) | O(mn²) | O(n²) |

---

## Interview Tips

1. **Draw the grid**: Visualize state transitions
2. **Identify dependencies**: What cells does dp[i][j] need?
3. **Handle boundaries**: First row/column often special
4. **Space optimize**: Usually possible after working solution
5. **Consider direction**: Some problems easier backwards

---

## Practice Problems

| # | Problem | Difficulty | Pattern |
|---|---------|------------|---------|
| 1 | Unique Paths | Medium | Path counting |
| 2 | Unique Paths II | Medium | With obstacles |
| 3 | Minimum Path Sum | Medium | Path optimization |
| 4 | Triangle | Medium | Variable width |
| 5 | Maximal Square | Medium | Square detection |
| 6 | Dungeon Game | Hard | Backwards DP |
| 7 | Cherry Pickup | Hard | Two agents |

---

## Key Takeaways

1. **Grid DP**: dp[i][j] depends on neighbors
2. **Space optimization**: 2D often reduces to 1D
3. **Direction matters**: Sometimes process backwards
4. **Boundary handling**: First row/column need care
5. **Multiple agents**: Add dimensions for each agent

---

## Next: [08-longest-common-subsequence.md](./08-longest-common-subsequence.md)

Learn string comparison DP with LCS.
