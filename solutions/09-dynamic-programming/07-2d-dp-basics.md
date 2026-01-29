# Solutions: 2D DP Basics (Grid Problems)

## 1. Unique Paths

**Problem:** Count paths from top-left to bottom-right in $m \times n$ grid.

### Optimal Python Solution

```python
def unique_paths(m: int, n: int) -> int:
    # State: dp[i][j] = paths to reach cell (i, j)
    # Space Optimization: Only need current and previous row
    dp = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    return dp[n-1]
```

### Complexity Analysis

- **Time:** $O(mn)$
- **Space:** $O(n)$

---

## 2. Unique Paths II (With Obstacles)

**Problem:** Count paths, avoiding obstacles (1 = obstacle).

### Optimal Python Solution

```python
def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = 1 if grid[0][0] == 0 else 0

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j-1]
    return dp[-1]
```

### Complexity Analysis

- **Time:** $O(mn)$
- **Space:** $O(n)$

---

## 3. Minimum Path Sum

**Problem:** Find path with minimum sum from top-left to bottom-right.

### Optimal Python Solution

```python
def min_path_sum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [float('inf')] * n
    dp[0] = 0

    for i in range(m):
        for j in range(n):
            if j == 0:
                dp[j] += grid[i][j]
            else:
                dp[j] = min(dp[j], dp[j-1]) + grid[i][j]
    return dp[-1]
```

### Complexity Analysis

- **Time:** $O(mn)$
- **Space:** $O(n)$

---

## 4. Triangle

**Problem:** Minimum path sum from top to bottom of a triangle.

### Optimal Python Solution

````python
def minimum_total(triangle: list[list[int]]) -> int:
    # Process bottom-up to avoid edge cases
    dp = triangle[-1][:]
    for i in range(len(triangle) - 2, -1, -1):
        for j in range(len(triangle[i])):
            dp[j] = triangle[i][j] + min(dp[j], dp[j+1])
    return dp[0]

```
---

## 7. Cherry Pickup
**Problem:** Two agents (or one agent going round-trip) collecting cherries in a grid. Maximize total cherries.

### Optimal Python Solution
```python
def cherry_pickup(grid: list[list[int]]) -> int:
    n = len(grid)
    # Use memoization to avoid 3D/4D DP table initialization
    memo = {}

    def dp(r1, c1, r2):
        # c2 is derived: r1 + c1 = r2 + c2 (total steps must be equal)
        c2 = r1 + c1 - r2

        # Out of bounds or obstacle
        if r1 == n or c1 == n or r2 == n or c2 == n or \
           grid[r1][c1] == -1 or grid[r2][c2] == -1:
            return float('-inf')

        # Reached end
        if r1 == n - 1 and c1 == n - 1:
            return grid[r1][c1]

        state = (r1, c1, r2)
        if state in memo: return memo[state]

        # Collect cherries
        cherries = grid[r1][c1]
        if r1 != r2: # Avoid double counting same cell
            cherries += grid[r2][c2]

        # 4 possible combinations of moves for two agents:
        # (Down, Down), (Down, Right), (Right, Down), (Right, Right)
        res = cherries + max(
            dp(r1 + 1, c1, r2 + 1),
            dp(r1 + 1, c1, r2),
            dp(r1, c1 + 1, r2 + 1),
            dp(r1, c1 + 1, r2)
        )

        memo[state] = res
        return res

    result = dp(0, 0, 0)
    return max(0, result)
````

### Explanation

1.  **Dual Traversal**: Instead of one round trip (start to end, then end to start), we simulate two agents moving from `(0,0)` to `(n-1, n-1)` simultaneously.
2.  **State Reduction**: Normally we need 4 coordinates `(r1, c1, r2, c2)`. However, since both move one step at a time, `r1 + c1` must equal `r2 + c2`. We can derive `c2` as `r1 + c1 - r2`, reducing the state to 3 variables.
3.  **Cherry Collection**: If both agents are on the same cell, they only collect the cherry once.
4.  **Transitions**: Each agent can move Right or Down, leading to 4 possible combined movements.

### Complexity Analysis

- **Time:** $O(n^3)$ - There are $n \times n \times n$ possible states.
- **Space:** $O(n^3)$ - For the memoization table.

````

### Complexity Analysis
- **Time:** $O(n^2)$ - Number of elements in triangle.
- **Space:** $O(n)$ - Size of the bottom row.

---

## 5. Maximal Square
**Problem:** Find the area of the largest square of '1's in a binary matrix.

### Optimal Python Solution
```python
def maximal_square(matrix: list[list[str]]) -> int:
    # State: dp[i][j] = side of largest square ending at (i, j)
    # Recurrence: dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
    if not matrix: return 0
    m, n = len(matrix), len(matrix[0])
    dp = [0] * (n + 1)
    max_side = 0
    prev_diag = 0 # stores dp[i-1][j-1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            temp = dp[j]
            if matrix[i-1][j-1] == '1':
                dp[j] = min(dp[j], dp[j-1], prev_diag) + 1
                max_side = max(max_side, dp[j])
            else:
                dp[j] = 0
            prev_diag = temp

    return max_side * max_side
````

### Complexity Analysis

- **Time:** $O(mn)$
- **Space:** $O(n)$

---

## 6. Dungeon Game

**Problem:** Minimum initial HP to reach bottom-right.

### Optimal Python Solution

````python
def calculate_minimum_hp(dungeon: list[list[int]]) -> int:
    # Process backwards from destination to start
    m, n = len(dungeon), len(dungeon[0])
    dp = [float('inf')] * (n + 1)
    dp[n-1] = 1 # At destination, need 1 HP

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            needed = min(dp[j], dp[j+1]) - dungeon[i][j]
            dp[j] = max(1, needed)
        dp[n] = float('inf') # Reset boundary for next row

    return dp[0]

```
---

## 7. Cherry Pickup
**Problem:** Two agents (or one agent going round-trip) collecting cherries in a grid. Maximize total cherries.

### Optimal Python Solution
```python
def cherry_pickup(grid: list[list[int]]) -> int:
    n = len(grid)
    # Use memoization to avoid 3D/4D DP table initialization
    memo = {}

    def dp(r1, c1, r2):
        # c2 is derived: r1 + c1 = r2 + c2 (total steps must be equal)
        c2 = r1 + c1 - r2

        # Out of bounds or obstacle
        if r1 == n or c1 == n or r2 == n or c2 == n or \
           grid[r1][c1] == -1 or grid[r2][c2] == -1:
            return float('-inf')

        # Reached end
        if r1 == n - 1 and c1 == n - 1:
            return grid[r1][c1]

        state = (r1, c1, r2)
        if state in memo: return memo[state]

        # Collect cherries
        cherries = grid[r1][c1]
        if r1 != r2: # Avoid double counting same cell
            cherries += grid[r2][c2]

        # 4 possible combinations of moves for two agents:
        # (Down, Down), (Down, Right), (Right, Down), (Right, Right)
        res = cherries + max(
            dp(r1 + 1, c1, r2 + 1),
            dp(r1 + 1, c1, r2),
            dp(r1, c1 + 1, r2 + 1),
            dp(r1, c1 + 1, r2)
        )

        memo[state] = res
        return res

    result = dp(0, 0, 0)
    return max(0, result)
````

### Explanation

1.  **Dual Traversal**: Instead of one round trip (start to end, then end to start), we simulate two agents moving from `(0,0)` to `(n-1, n-1)` simultaneously.
2.  **State Reduction**: Normally we need 4 coordinates `(r1, c1, r2, c2)`. However, since both move one step at a time, `r1 + c1` must equal `r2 + c2`. We can derive `c2` as `r1 + c1 - r2`, reducing the state to 3 variables.
3.  **Cherry Collection**: If both agents are on the same cell, they only collect the cherry once.
4.  **Transitions**: Each agent can move Right or Down, leading to 4 possible combined movements.

### Complexity Analysis

- **Time:** $O(n^3)$ - There are $n \times n \times n$ possible states.
- **Space:** $O(n^3)$ - For the memoization table.

```

### Complexity Analysis
- **Time:** $O(mn)$
- **Space:** $O(n)$
```
