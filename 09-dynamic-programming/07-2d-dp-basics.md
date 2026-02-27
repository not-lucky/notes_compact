# 2D DP Basics

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

2D Dynamic Programming uses a two-dimensional state `dp[i][j]` to represent the answers to subproblems that depend on two distinct parameters. This is common when traversing grids, comparing two sequences, or dealing with multiple constraints (like items and capacity).

## Building Intuition

**Why do we need 2D DP?**

1. **Two Independent Dimensions**: When the state of a problem is defined by two independent variables—such as the position in two different strings, the row and column in a 2D grid, or the current item index and remaining capacity in a knapsack—a single dimension isn't enough to track all combinations.
2. **Grid Problems Are Natural 2D**: In a grid, reaching cell `(i, j)` usually depends on reaching adjacent cells like `(i-1, j)` and `(i, j-1)`. The state naturally maps to the grid coordinates.
3. **Sequence Comparison Needs Pairs**: For problems like Longest Common Subsequence (LCS) or Edit Distance, we compare a prefix of the first string `s1[0..i]` with a prefix of the second string `s2[0..j]`. The answer for each `(i, j)` pair is unique.
4. **The Dependency Insight**: In 2D DP, `dp[i][j]` typically depends on:
   - `dp[i-1][j]` (the cell directly above)
   - `dp[i][j-1]` (the cell directly to the left)
   - `dp[i-1][j-1]` (the cell diagonally above-left)
   This predictable dependency structure dictates how we fill the DP table (usually row by row, left to right).
5. **Space Optimization is Key**: Because `dp[i][j]` often only depends on the previous row `i-1` and the current row `i`, we can frequently optimize the space complexity from $O(M \times N)$ to $O(N)$ by only storing one or two rows at a time.
6. **Mental Model**: Think of the DP table as a spreadsheet. Each cell `(i, j)` contains the answer for a specific subproblem defined by `i` and `j`. You fill it systematically, and each cell's formula references previously calculated cells (usually above, left, or diagonally above-left).

## Interview Context

2D DP problems are frequently asked because they test your ability to:
1. **Model state**: Identify when two parameters are needed.
2. **Find recurrence relations**: Connect `dp[i][j]` to its neighbors.
3. **Handle boundaries**: Correctly initialize the first row and column.
4. **Optimize space**: Demonstrate advanced understanding by reducing $O(M \times N)$ space to $O(N)$.

---

## When NOT to Use 2D DP

Before jumping to a 2D array, consider if it's the right tool:

1. **State Is Actually 1D**: Don't force 2D when 1D suffices. Problems like Fibonacci, Climbing Stairs, or House Robber only need one index to represent the state.
2. **State Requires 3+ Dimensions**: Some complex problems require tracking more parameters, leading to states like `dp[i][j][k]` (e.g., trading stocks with `k` transactions allowed, or pathfinding in a 3D grid).
3. **General Graphs (Non-Grids)**: 2D DP works well for grids where transitions only go in specific directions (forming a Directed Acyclic Graph, or DAG). For general graphs with cycles or arbitrary edge weights, use shortest path algorithms like Dijkstra's or Bellman-Ford.
4. **Sparse State Space**: If only a small fraction of all possible `(i, j)` pairs are ever visited or valid, an $O(M \times N)$ table wastes space and time. Use top-down memoization with a hash map instead.

**Signs 2D DP is Appropriate:**
- You are given a 2D matrix or grid and need to find a path, optimal sum, or pattern.
- You are comparing or aligning two input sequences/strings/arrays.
- You are choosing items with a capacity constraint (Knapsack pattern).
- The problem constraints are small enough to allow $O(M \times N)$ time complexity.

---

## Pattern 1: Grid Path Problems

Grid path problems are the classic introduction to 2D DP. You are typically asked to find the number of paths, the minimum/maximum path sum, or whether a path exists from the top-left to the bottom-right.

### Unique Paths (LeetCode 62)

Count the number of unique paths from the top-left corner `(0, 0)` to the bottom-right corner `(m-1, n-1)`. You can only move down or right.

**Formal Recurrence Relation:**
- **State:** Let $dp[i][j]$ be the number of unique paths to reach cell $(i, j)$.
- **Base Case:**
  - $dp[i][0] = 1$ for all $i$ (there is only one way to move straight down the left edge).
  - $dp[0][j] = 1$ for all $j$ (there is only one way to move straight right along the top edge).
- **Recurrence:** $dp[i][j] = dp[i-1][j] + dp[i][j-1]$
  - Paths to the current cell come from the cell directly above + the cell directly to the left.

#### Top-Down (Memoization)

```python
def unique_paths_memo(m: int, n: int) -> int:
    """
    Top-Down Memoization approach.

    Time: O(m * n) - each cell calculated once
    Space: O(m * n) for memo dictionary and recursion stack
    """
    memo = {}

    def dfs(r: int, c: int) -> int:
        # Base case: reached the starting cell
        if r == 0 and c == 0:
            return 1
        # Out of bounds
        if r < 0 or c < 0:
            return 0

        if (r, c) in memo:
            return memo[(r, c)]

        # Recurrence: paths from cell above + paths from cell left
        memo[(r, c)] = dfs(r - 1, c) + dfs(r, c - 1)
        return memo[(r, c)]

    return dfs(m - 1, n - 1)
```

#### Bottom-Up (Tabulation) with Space Optimization

```python
def uniquePaths(m: int, n: int) -> int:
    """
    Count unique paths in m x n grid. Space optimized.

    Time: O(m * n)
    Space: O(n) - we only need the previous row's values
    """
    # Initialize the DP array for the first row
    # There is only 1 path to reach any cell in the first row (move right)
    dp = [1] * n

    for _ in range(1, m):
        # We start j from 1 because dp[0] (the first column) is always 1
        for j in range(1, n):
            # dp[j] before update represents dp[i-1][j] (cell above)
            # dp[j-1] represents the newly calculated cell to the left
            dp[j] = dp[j] + dp[j - 1]

    return dp[n - 1]
```

### Unique Paths II (With Obstacles) (LeetCode 63)

Similar to the previous problem, but the grid contains obstacles (`1` represents an obstacle, `0` is empty). Paths cannot pass through obstacles.

```python
def uniquePathsWithObstacles(obstacleGrid: list[list[int]]) -> int:
    """
    Count paths avoiding obstacles.

    Time: O(m * n)
    Space: O(n)
    """
    m, n = len(obstacleGrid), len(obstacleGrid[0])

    # If the starting cell has an obstacle, there are no paths
    if obstacleGrid[0][0] == 1:
        return 0

    dp = [0] * n
    dp[0] = 1 # 1 path to start cell

    for i in range(m):
        for j in range(n):
            if obstacleGrid[i][j] == 1:
                dp[j] = 0 # Cannot reach an obstacle cell
            elif j > 0:
                # Same logic: paths from above (dp[j]) + paths from left (dp[j-1])
                # Note: if j == 0, dp[j] just retains its previous value (from the row above)
                dp[j] += dp[j - 1]

    return dp[n - 1]
```

### Minimum Path Sum (LeetCode 64)

Find a path from top-left to bottom-right that minimizes the sum of all numbers along its path.

```python
def minPathSum(grid: list[list[int]]) -> int:
    """
    Minimum sum path from top-left to bottom-right.

    Time: O(m * n)
    Space: O(n)
    """
    m, n = len(grid), len(grid[0])
    dp = [float('inf')] * n
    dp[0] = 0 # Start with 0 accumulated sum before entering the grid

    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                dp[j] = grid[0][0]
            elif i == 0:
                # First row: can only come from the left
                dp[j] = dp[j - 1] + grid[i][j]
            elif j == 0:
                # First column: can only come from above
                dp[j] = dp[j] + grid[i][j]
            else:
                # Normal case: minimum of coming from above or left
                dp[j] = min(dp[j], dp[j - 1]) + grid[i][j]

    return dp[n - 1]
```

---

## Pattern 2: Triangle (LeetCode 120)

Given a `triangle` array, find the minimum path sum from top to bottom. You can move to adjacent numbers on the row below (`(i+1, j)` or `(i+1, j+1)`).

**Key Insight:** This problem is much easier to solve **bottom-up**, starting from the base of the triangle and moving towards the top. This avoids having to check boundaries on the sides of the triangle as it narrows.

```python
def minimumTotal(triangle: list[list[int]]) -> int:
    """
    Minimum path sum from top to bottom of a triangle.
    Process bottom-up for cleaner code and automatic boundary handling.

    Time: O(n^2) where n is the number of rows
    Space: O(n)
    """
    n = len(triangle)
    # Initialize DP array with the bottom row of the triangle
    dp = triangle[-1][:]

    # Start from the second to last row, moving upwards
    for i in range(n - 2, -1, -1):
        for j in range(len(triangle[i])):
            # To reach (i, j), we must come from either (i+1, j) or (i+1, j+1)
            # Since we are going upwards, the value at (i, j) is its own value
            # plus the minimum of the two possible choices below it.
            dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])

    # The top element now holds the minimum path sum
    return dp[0]
```

---

## Pattern 3: Maximum Square (LeetCode 221)

Find the largest square containing only `1`s in a binary matrix and return its area.

**State Definition Insight:**
Let `dp[i][j]` be the side length of the largest square whose **bottom-right corner** is at `(i, j)`.

If `matrix[i][j] == '1'`, it can only form a larger square if the cells to its left, above, and diagonally above-left *also* form squares. The size of the square ending at `(i, j)` is constrained by the smallest of those three neighboring squares.

**Recurrence:** `dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1`

```python
def maximalSquare(matrix: list[list[str]]) -> int:
    """
    Find largest square of 1s.

    Time: O(m * n)
    Space: O(n)
    """
    if not matrix or not matrix[0]:
        return 0

    m, n = len(matrix), len(matrix[0])
    dp = [0] * n
    max_side = 0
    prev_diagonal = 0 # Tracks dp[i-1][j-1]

    for i in range(m):
        for j in range(n):
            # Save the current dp[j] before it's updated, as it will become
            # the dp[i-1][j-1] (prev_diagonal) for the next cell (i, j+1)
            temp = dp[j]

            if matrix[i][j] == '1':
                if i == 0 or j == 0:
                    dp[j] = 1 # Base case: first row or column can at most form a 1x1 square
                else:
                    # dp[j] = above, dp[j-1] = left, prev_diagonal = top-left
                    dp[j] = min(dp[j], dp[j - 1], prev_diagonal) + 1
                max_side = max(max_side, dp[j])
            else:
                dp[j] = 0 # Reset to 0 if the cell is '0'

            prev_diagonal = temp

    return max_side * max_side
```

---

## Pattern 4: Backwards DP - Dungeon Game (LeetCode 174)

Find the minimum initial health needed to navigate a dungeon from top-left to bottom-right, keeping health `> 0` at all times. Cells can contain health potions (positive) or demons (negative).

**Key Insight:** If you process top-down (start to finish), your state depends on *two* variables: the minimum health required so far AND the current health. This is complex.
If you process **bottom-up** (from the destination to the start), the state simplifies: "What is the minimum health I need at this cell to survive the rest of the journey?"

```python
def calculateMinimumHP(dungeon: list[list[int]]) -> int:
    """
    Minimum initial HP to reach bottom-right. Process backwards.

    Time: O(m * n)
    Space: O(n)
    """
    m, n = len(dungeon), len(dungeon[0])
    # Initialize with infinity. We use n+1 to handle boundaries easily.
    dp = [float('inf')] * (n + 1)

    # Base case: to survive after reaching the destination, we need at least 1 HP
    dp[n - 1] = 1

    # Iterate backwards from bottom-right to top-left
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            # Minimum health needed to step to the next cell (either right or down)
            min_hp_needed = min(dp[j], dp[j + 1])

            # The health we need at current cell = health needed for next steps - current cell's effect
            # If current cell is a potion (+), we need less health now.
            # If current cell is a demon (-), we need more health now.
            current_needed = min_hp_needed - dungeon[i][j]

            # We must ALWAYS have at least 1 HP at any given cell to stay alive
            dp[j] = max(1, current_needed)

    return dp[0]
```

---

## Pattern 5: Multi-dimensional State - Cherry Pickup (LeetCode 741)

Two robots start from opposite corners and collect cherries. Find the maximum cherries they can collect. This is equivalent to two robots moving simultaneously from top-left to bottom-right.

**Key Insight:** We need to track the state of *both* robots. A naive state would be `dp[r1][c1][r2][c2]` (4D, $O(N^4)$).
However, since they move simultaneously down/right, they always take the same number of steps. Thus, `r1 + c1 = r2 + c2 = steps`.
We can deduce `r1 = steps - c1` and `r2 = steps - c2`. Therefore, the state only needs 3 dimensions: `dp[steps][c1][c2]` or just keeping the previous step's DP array to reduce to 2 dimensions space: `dp[c1][c2]`.

```python
def cherryPickup(grid: list[list[int]]) -> int:
    """
    Two robots moving simultaneously from top-left to bottom-right.

    Time: O(N^3)
    Space: O(N^2)
    """
    n = len(grid)
    # State: dp[c1][c2] represents max cherries when robot 1 is at column c1
    # and robot 2 is at column c2.
    # We initialize with -infinity because some states might be unreachable (obstacles).
    dp = [[float('-inf')] * n for _ in range(n)]

    # Start position: step 0. Both robots at (0, 0). Column is 0 for both.
    dp[0][0] = grid[0][0]

    # Total steps from (0,0) to (n-1, n-1) is 2 * (n - 1)
    for step in range(1, 2 * n - 1):
        # We need a new DP array for the current step
        new_dp = [[float('-inf')] * n for _ in range(n)]

        # Iterate over all possible columns for robot 1
        for c1 in range(max(0, step - n + 1), min(n, step + 1)):
            r1 = step - c1 # Calculate row for robot 1
            if grid[r1][c1] == -1: # Obstacle
                continue

            # Iterate over all possible columns for robot 2
            for c2 in range(max(0, step - n + 1), min(n, step + 1)):
                r2 = step - c2 # Calculate row for robot 2
                if grid[r2][c2] == -1: # Obstacle
                    continue

                # Cherries collected at this step
                cherries = grid[r1][c1]
                if c1 != c2: # If they are on different cells, collect both
                    cherries += grid[r2][c2]

                # Transition: to reach (c1, c2) at `step`, where could they have been at `step-1`?
                # R1 could come from top (c1) or left (c1-1)
                # R2 could come from top (c2) or left (c2-1)
                # Four possible previous states:
                # 1. Both came from top: dp[c1][c2]
                # 2. R1 from left, R2 from top: dp[c1-1][c2]
                # 3. R1 from top, R2 from left: dp[c1][c2-1]
                # 4. Both came from left: dp[c1-1][c2-1]

                max_prev = float('-inf')
                for prev_c1 in (c1, c1 - 1):
                    for prev_c2 in (c2, c2 - 1):
                        if 0 <= prev_c1 < n and 0 <= prev_c2 < n:
                            max_prev = max(max_prev, dp[prev_c1][prev_c2])

                new_dp[c1][c2] = max_prev + cherries if max_prev != float('-inf') else float('-inf')

        dp = new_dp

    return max(0, dp[n - 1][n - 1])
```

---

## Deep Dive: Space Optimization Techniques

### The Logic Behind 2D → 1D Reduction

Why does Space Optimization work in Grid Path / 2D problems?
If we carefully analyze the recurrence relation for problems like Unique Paths:
`dp[i][j] = dp[i-1][j] + dp[i][j-1]`

To compute the values for the current row `i`, we **ONLY** need values from the *immediately preceding row* `i-1`. Any rows calculated before `i-1` (like `i-2`, `i-3`) are completely obsolete and can be discarded. By tracking just a `current_row` and `previous_row`, we immediately drop the space complexity from $O(M \times N)$ to $O(N)$.

Even better, we can often achieve this with a **single 1D array** by overwriting values in-place as we iterate left-to-right.
- When we are about to update `dp[j]`, its current value is the result from the row above (`dp[i-1][j]`).
- The value at `dp[j-1]` has *already* been updated in the current loop, so it represents the cell directly to the left in the current row (`dp[i][j-1]`).

```python
# Original O(m * n) space approach
dp = [[0] * n for _ in range(m)]
for i in range(m):
    for j in range(n):
        # We need the full 2D grid
        dp[i][j] = f(dp[i-1][j], dp[i][j-1])

# Optimized O(n) space approach using a single array
dp_row = [0] * n
for i in range(m):
    for j in range(n):
        # dp_row[j] (before assignment) IS dp[i-1][j] (the cell above)
        # dp_row[j-1] IS dp[i][j-1] (the cell to the left, already updated)
        dp_row[j] = f(dp_row[j], dp_row[j-1])
```

### When We Need `dp[i-1][j-1]` (The Diagonal Element)

For problems like Maximum Square, Longest Common Subsequence (LCS), or Edit Distance, the recurrence relation relies on the diagonal element `dp[i-1][j-1]`.

If we blindly overwrite `dp_row[j]`, we lose the diagonal value needed for the *next* calculation at `j+1`. We must cache this value in a temporary variable before overwriting.

```python
# Need to save dp[i-1][j-1] before overwriting
dp_row = [0] * n
for i in range(m):
    prev_diagonal = 0  # Initialize variable to hold dp[i-1][j-1]

    for j in range(n):
        # Save the current value before it gets overwritten.
        # This value is dp[i-1][j] now, but in the next iteration (when we process j+1),
        # it will be the top-left diagonal element.
        temp = dp_row[j]

        # Calculate new value using current above (dp_row[j]), left (dp_row[j-1]), and diagonal (prev_diagonal)
        dp_row[j] = f(dp_row[j], dp_row[j-1], prev_diagonal)

        # Pass the saved value to the next iteration
        prev_diagonal = temp
```

---

## Common Mistakes

1. **Incorrect Iteration Direction for Space Optimization**:
   If a recurrence depends on `dp[i][j+1]` (the cell to the right), you **must** iterate backwards (right-to-left). If you iterate left-to-right, you will overwrite the old value before you need it.
   ```python
   # WRONG if current cell needs the unupdated cell to its right:
   for j in range(n):
       dp[j] = dp[j] + dp[j+1] # dp[j+1] hasn't been updated for the current row yet!

   # CORRECT: Iterate right to left
   for j in range(n-2, -1, -1):
       dp[j] = dp[j] + dp[j+1]
   ```

2. **Forgetting Boundary Initialization**:
   Failing to handle the first row or first column leads to `IndexError` or incorrect calculations.
   ```python
   # WRONG:
   for i in range(m):
       for j in range(n):
           dp[i][j] = dp[i-1][j] + dp[i][j-1]  # IndexError at i=0 or j=0

   # CORRECT:
   if i == 0 and j == 0:
       dp[i][j] = grid[0][0]
   elif i == 0:
       dp[i][j] = dp[i][j-1] + grid[i][j]
   elif j == 0:
       dp[i][j] = dp[i-1][j] + grid[i][j]
   else:
       dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
   ```

---

## Visual: 2D DP State Transitions

**Unique Paths:**
```text
|     | c=0 | c=1 | c=2 | c=3 |
|-----|-----|-----|-----|-----|
| r=0 | [1] | [1] | [1] | [1] |
| r=1 | [1] | [2] | [3] | [4] |
| r=2 | [1] | [3] | [6] | [10]|
```

Formula: $dp[i][j] = dp[i-1][j] + dp[i][j-1]$
The value in any cell is the sum of the cell directly above (↑) and the cell directly to the left (←).

**Minimum Path Sum:**
Grid:
```text
| 1 | 3 | 1 |
| 1 | 5 | 1 |
| 4 | 2 | 1 |
```

DP Table:
```text
|   | c=0 | c=1 | c=2 |
|---|-----|-----|-----|
|r=0| [1] | [4] | [5] |
|r=1| [2] | [7] | [6] |
|r=2| [6] | [8] | [7] |  ← Answer: 7
```

---

## Complexity Summary

| Problem | Time Complexity | Original Space | Optimized Space |
| :--- | :--- | :--- | :--- |
| Unique Paths | $O(M \times N)$ | $O(M \times N)$ | $O(N)$ |
| Minimum Path Sum | $O(M \times N)$ | $O(M \times N)$ | $O(N)$ |
| Maximum Square | $O(M \times N)$ | $O(M \times N)$ | $O(N)$ |
| Triangle | $O(N^2)$ | $O(N^2)$ | $O(N)$ |
| Cherry Pickup | $O(N^3)$ | $O(N^4)$ | $O(N^2)$ |

*(Where N is typically the number of columns, and M is the number of rows).*

---

## Interview Tips

1. **Draw the grid**: Always visualize the grid and manually trace the state transitions for a small example (e.g., 3x3).
2. **Identify dependencies**: Clearly state to the interviewer: "To calculate cell `(i, j)`, I need the values from..." This proves you understand the recurrence.
3. **Handle boundaries first**: Explicitly mention how you handle the first row, first column, and `(0, 0)`.
4. **Solve 2D first, then optimize**: Always write the $O(M \times N)$ space solution first unless you are extremely confident. Mention space optimization as a follow-up, then implement it if asked.
5. **Consider processing backwards**: If the state feels overly complex or requires knowing the future, try defining the state as "cost to reach the end from here" instead of "cost to reach here from the start".

---

## Practice Problems

| # | Problem | Difficulty | Pattern / Focus |
| :--- | :--- | :--- | :--- |
| 62 | Unique Paths | Medium | Basic 2D grid traversal |
| 63 | Unique Paths II | Medium | Grid traversal with obstacles |
| 64 | Minimum Path Sum | Medium | Path optimization |
| 120 | Triangle | Medium | Bottom-up DP |
| 221 | Maximal Square | Medium | Using diagonal dependencies |
| 174 | Dungeon Game | Hard | Backwards state modeling |
| 741 | Cherry Pickup | Hard | Multi-agent simultaneous movement |

---

## Key Takeaways

1. **Grid DP**: `dp[i][j]` generally depends on its immediate neighbors (above, left, diagonal).
2. **Space optimization**: 2D DP arrays can almost always be reduced to 1D arrays by keeping only the active rows.
3. **Direction matters**: Sometimes it is significantly easier to process the state backwards (from destination to start).
4. **Boundary handling**: The first row and column often require specific initialization outside the main nested loop.
5. **Diagonal Cache**: If space-optimizing a recurrence that uses `dp[i-1][j-1]`, you must cache it in a temporary variable.

---

## Next: [08-longest-common-subsequence.md](./08-longest-common-subsequence.md)

Learn how to apply 2D DP to string comparison problems using the Longest Common Subsequence pattern.