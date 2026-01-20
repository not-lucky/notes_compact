# Number of Islands

## Problem Statement

Given an `m x n` 2D grid map of `'1'`s (land) and `'0'`s (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.

**Example:**
```
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3
```

## Approach

### DFS Flood Fill
1. Iterate through each cell
2. When finding a '1', increment count and flood fill (mark all connected land)
3. Marking prevents counting same island twice

### BFS Alternative
Same logic but uses queue for exploration.

### Union-Find
Group connected cells, count distinct groups.

## Implementation

```python
def num_islands(grid: list[list[str]]) -> int:
    """
    Count islands using DFS flood fill.

    Time: O(m × n) - visit each cell once
    Space: O(m × n) - recursion stack in worst case
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r: int, c: int):
        # Boundary check and water check
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return

        # Mark as visited
        grid[r][c] = '0'

        # Explore all 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)

    return count


def num_islands_bfs(grid: list[list[str]]) -> int:
    """
    Count islands using BFS.

    Time: O(m × n)
    Space: O(min(m, n)) - queue size
    """
    if not grid or not grid[0]:
        return 0

    from collections import deque

    rows, cols = len(grid), len(grid[0])
    count = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                grid[r][c] = '0'
                queue = deque([(r, c)])

                while queue:
                    row, col = queue.popleft()
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                            grid[nr][nc] = '0'
                            queue.append((nr, nc))

    return count


def num_islands_union_find(grid: list[list[str]]) -> int:
    """
    Count islands using Union-Find.

    Time: O(m × n × α(m × n)) ≈ O(m × n)
    Space: O(m × n)
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])

    parent = {}
    rank = {}

    def find(x):
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

    # Initialize and union adjacent land cells
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                find((r, c))
                # Check right and down neighbors
                if c + 1 < cols and grid[r][c + 1] == '1':
                    union((r, c), (r, c + 1))
                if r + 1 < rows and grid[r + 1][c] == '1':
                    union((r, c), (r + 1, c))

    # Count unique roots
    roots = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                roots.add(find((r, c)))

    return len(roots)
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| DFS | O(m×n) | O(m×n) | Stack in worst case |
| BFS | O(m×n) | O(min(m,n)) | Queue size |
| Union-Find | O(m×n×α) | O(m×n) | Nearly O(m×n) |

## Visual Walkthrough

```
Grid:
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1

Start scanning:
(0,0) = '1' → Island 1! DFS marks all connected:
0 0 0 0 0
0 0 0 0 0
0 0 1 0 0
0 0 0 1 1

(0,1) = '0' → skip
...
(2,2) = '1' → Island 2! DFS marks:
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 1 1

(3,3) = '1' → Island 3! DFS marks:
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0

Total: 3 islands
```

## Edge Cases

1. **Empty grid**: Return 0
2. **All water**: Return 0
3. **All land**: Return 1
4. **Single cell**: Return 1 if land, 0 if water
5. **Diagonal islands**: Not connected (only horizontal/vertical)

## Common Mistakes

1. **Forgetting to mark visited**: Causes infinite loop
2. **Including diagonals**: Only 4-directional, not 8
3. **Modifying grid when not allowed**: Use separate visited set
4. **Off-by-one in boundaries**: Check bounds carefully

## Variations

### Max Area of Island
```python
def max_area_of_island(grid: list[list[int]]) -> int:
    """
    Find area of largest island.

    Time: O(m × n)
    Space: O(m × n)
    """
    rows, cols = len(grid), len(grid[0])

    def dfs(r: int, c: int) -> int:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
            return 0

        grid[r][c] = 0
        return 1 + dfs(r+1, c) + dfs(r-1, c) + dfs(r, c+1) + dfs(r, c-1)

    return max(
        (dfs(r, c) for r in range(rows) for c in range(cols)),
        default=0
    )
```

### Surrounded Regions
```python
def solve(board: list[list[str]]) -> None:
    """
    Capture all 'O's not connected to border.
    """
    if not board:
        return

    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int):
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
            return
        board[r][c] = 'S'  # Safe
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            dfs(r + dr, c + dc)

    # Mark border-connected O's as safe
    for r in range(rows):
        dfs(r, 0)
        dfs(r, cols - 1)
    for c in range(cols):
        dfs(0, c)
        dfs(rows - 1, c)

    # Capture surrounded O's, restore safe ones
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == 'S':
                board[r][c] = 'O'
```

### Pacific Atlantic Water Flow
```python
def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    """
    Find cells that can flow to both oceans.
    """
    rows, cols = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()

    def dfs(r: int, c: int, visited: set, prev_height: int):
        if (r, c) in visited:
            return
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if heights[r][c] < prev_height:
            return

        visited.add((r, c))
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            dfs(r + dr, c + dc, visited, heights[r][c])

    # Start from ocean borders
    for c in range(cols):
        dfs(0, c, pacific, 0)
        dfs(rows - 1, c, atlantic, 0)
    for r in range(rows):
        dfs(r, 0, pacific, 0)
        dfs(r, cols - 1, atlantic, 0)

    return list(pacific & atlantic)
```

## Related Problems

- **Max Area of Island** - Find largest island area
- **Surrounded Regions** - Capture surrounded cells
- **Pacific Atlantic Water Flow** - Bidirectional reachability
- **Number of Distinct Islands** - Count unique island shapes
- **Making A Large Island** - Change one 0 to maximize island
