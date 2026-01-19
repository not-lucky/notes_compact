# Grid Problems (Islands, Flood Fill)

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md), [03-dfs-basics](./03-dfs-basics.md)

## Interview Context

Grid problems are FANG+ favorites because:

1. **Very common**: Number of Islands appears constantly
2. **Multiple patterns**: DFS, BFS, Union-Find all applicable
3. **Edge case testing**: Bounds checking, visited tracking
4. **Real-world analogy**: Image processing, game maps

Expect at least one grid problem in most interview loops.

---

## Core Concept: Grid as Graph

A grid is an **implicit graph** where:
- Each cell is a vertex
- Adjacent cells (up, down, left, right) are connected

```
Grid:               Implicit Graph:
1 1 0               (0,0)-(0,1)  (0,2)
1 0 0                 |
0 0 1               (1,0)        (1,2)

                    (2,0) (2,1)  (2,2)
```

---

## Number of Islands

```python
def num_islands(grid: list[list[str]]) -> int:
    """
    Count islands (connected groups of 1s).

    Time: O(rows × cols)
    Space: O(rows × cols) worst case for recursion
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r: int, c: int):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] != '1'):
            return

        grid[r][c] = '0'  # Mark visited

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
```

---

## Flood Fill

```python
def flood_fill(image: list[list[int]], sr: int, sc: int,
               color: int) -> list[list[int]]:
    """
    Fill connected region with new color.

    Time: O(rows × cols)
    Space: O(rows × cols)
    """
    if image[sr][sc] == color:
        return image  # No change needed

    rows, cols = len(image), len(image[0])
    original_color = image[sr][sc]

    def dfs(r: int, c: int):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            image[r][c] != original_color):
            return

        image[r][c] = color

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(sr, sc)
    return image
```

---

## Max Area of Island

```python
def max_area_of_island(grid: list[list[int]]) -> int:
    """
    Find the largest island by area.

    Time: O(rows × cols)
    Space: O(rows × cols)
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    max_area = 0

    def dfs(r: int, c: int) -> int:
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] != 1):
            return 0

        grid[r][c] = 0  # Mark visited
        area = 1

        area += dfs(r + 1, c)
        area += dfs(r - 1, c)
        area += dfs(r, c + 1)
        area += dfs(r, c - 1)

        return area

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                max_area = max(max_area, dfs(r, c))

    return max_area
```

---

## Surrounded Regions

```python
def solve(board: list[list[str]]) -> None:
    """
    Capture all 'O' regions not connected to border.
    Modify board in-place.

    Time: O(rows × cols)
    Space: O(rows × cols)

    Strategy: Mark border-connected 'O's, then capture the rest.
    """
    if not board:
        return

    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            board[r][c] != 'O'):
            return

        board[r][c] = 'T'  # Temporarily mark as safe

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    # Mark border-connected O's
    for r in range(rows):
        dfs(r, 0)
        dfs(r, cols - 1)
    for c in range(cols):
        dfs(0, c)
        dfs(rows - 1, c)

    # Capture surrounded O's, restore border-connected
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == 'T':
                board[r][c] = 'O'
```

---

## Number of Distinct Islands

```python
def num_distinct_islands(grid: list[list[int]]) -> int:
    """
    Count distinct island shapes.

    Time: O(rows × cols)
    Space: O(rows × cols)

    Use relative positions as shape signature.
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    shapes = set()

    def dfs(r: int, c: int, origin_r: int, origin_c: int,
            shape: list[tuple[int, int]]):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] != 1):
            return

        grid[r][c] = 0
        shape.append((r - origin_r, c - origin_c))

        dfs(r + 1, c, origin_r, origin_c, shape)
        dfs(r - 1, c, origin_r, origin_c, shape)
        dfs(r, c + 1, origin_r, origin_c, shape)
        dfs(r, c - 1, origin_r, origin_c, shape)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                shape = []
                dfs(r, c, r, c, shape)
                shapes.add(tuple(shape))

    return len(shapes)
```

---

## Island Perimeter

```python
def island_perimeter(grid: list[list[int]]) -> int:
    """
    Calculate perimeter of island.

    Time: O(rows × cols)
    Space: O(1)

    Each land cell contributes 4, minus 2 for each adjacent land.
    """
    rows, cols = len(grid), len(grid[0])
    perimeter = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                perimeter += 4

                # Subtract for adjacent land cells
                if r > 0 and grid[r-1][c] == 1:
                    perimeter -= 2
                if c > 0 and grid[r][c-1] == 1:
                    perimeter -= 2

    return perimeter
```

---

## Making a Large Island (Flip One 0)

```python
def largest_island(grid: list[list[int]]) -> int:
    """
    Flip at most one 0 to 1, find largest island.

    Time: O(rows × cols)
    Space: O(rows × cols)

    Strategy: Label each island, store sizes, check each 0.
    """
    rows, cols = len(grid), len(grid[0])

    def dfs(r: int, c: int, label: int) -> int:
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] != 1):
            return 0

        grid[r][c] = label
        size = 1

        size += dfs(r + 1, c, label)
        size += dfs(r - 1, c, label)
        size += dfs(r, c + 1, label)
        size += dfs(r, c - 1, label)

        return size

    # Label islands and store sizes
    island_size = {}
    label = 2  # Start from 2 (0 is water, 1 is unlabeled land)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                island_size[label] = dfs(r, c, label)
                label += 1

    if not island_size:
        return 1  # All water, flip one

    max_size = max(island_size.values())

    # Check each 0: what if we flip it?
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                neighbors = set()

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] > 1:
                        neighbors.add(grid[nr][nc])

                size = 1 + sum(island_size[n] for n in neighbors)
                max_size = max(max_size, size)

    return max_size
```

---

## BFS for Grid (Avoids Stack Overflow)

```python
from collections import deque

def num_islands_bfs(grid: list[list[str]]) -> int:
    """
    Number of islands using BFS.
    Better for very large grids.
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                grid[r][c] = '0'
                queue = deque([(r, c)])

                while queue:
                    cr, cc = queue.popleft()

                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if (0 <= nr < rows and 0 <= nc < cols and
                            grid[nr][nc] == '1'):
                            grid[nr][nc] = '0'
                            queue.append((nr, nc))

    return count
```

---

## 4-Direction vs 8-Direction

```python
# 4-directional (most common)
directions_4 = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# 8-directional (includes diagonals)
directions_8 = [
    (0, 1), (0, -1), (1, 0), (-1, 0),
    (1, 1), (1, -1), (-1, 1), (-1, -1)
]
```

---

## Edge Cases

```python
# 1. Empty grid
grid = []
# Return 0

# 2. All water
grid = [['0', '0'], ['0', '0']]
# Return 0

# 3. All land
grid = [['1', '1'], ['1', '1']]
# Return 1 island

# 4. Single cell
grid = [['1']]
# Return 1 island

# 5. Diagonal only (8-directional problem)
grid = [['1', '0'], ['0', '1']]
# 4-dir: 2 islands, 8-dir: 1 island
```

---

## Common Mistakes

```python
# WRONG: Not checking bounds first
def dfs(r, c):
    if grid[r][c] != '1':  # May cause IndexError
        return

# CORRECT: Check bounds first
def dfs(r, c):
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return
    if grid[r][c] != '1':
        return


# WRONG: Separate visited set when modifying grid is allowed
visited = set()
# Using extra O(rows × cols) space unnecessarily

# CORRECT: Modify grid in-place if allowed
grid[r][c] = '0'  # or 'X' or any marker


# WRONG: Not marking before recursing
def dfs(r, c):
    dfs(r+1, c)  # May revisit from neighbor
    grid[r][c] = '0'

# CORRECT: Mark before recursing
def dfs(r, c):
    grid[r][c] = '0'  # Mark first
    dfs(r+1, c)
```

---

## Interview Tips

1. **Ask about modifying grid**: Saves space if allowed
2. **Clarify connectivity**: 4-directional or 8-directional?
3. **Watch bounds**: Check before accessing grid
4. **Consider BFS**: For very large grids (avoid stack overflow)
5. **Think about edge cases**: Empty, all same value

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Number of Islands | Medium | Basic counting |
| 2 | Max Area of Island | Medium | Return size |
| 3 | Flood Fill | Easy | Simple traversal |
| 4 | Surrounded Regions | Medium | Border-connected |
| 5 | Number of Distinct Islands | Medium | Shape signature |
| 6 | Making A Large Island | Hard | What-if analysis |
| 7 | Island Perimeter | Easy | Counting pattern |
| 8 | Pacific Atlantic Water Flow | Medium | Multi-source |

---

## Key Takeaways

1. **Grid = implicit graph**: Adjacent cells are connected
2. **Mark visited**: Modify grid or use set
3. **DFS or BFS**: Both work, BFS avoids stack overflow
4. **Check bounds first**: Before any other condition
5. **4 vs 8 directions**: Know both patterns

---

## Next: [14-rotting-oranges.md](./14-rotting-oranges.md)

Learn multi-source BFS with the Rotting Oranges problem.
