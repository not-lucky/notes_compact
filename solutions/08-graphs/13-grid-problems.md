# Grid Problems (Islands, Flood Fill)

## Practice Problems

### 1. Number of Islands
**Difficulty:** Medium
**Concept:** Basic counting

```python
from typing import List

def num_islands(grid: List[List[str]]) -> int:
    """
    Count islands (connected groups of 1s).

    >>> num_islands([["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]])
    1
    >>> num_islands([["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]])
    3

    Time: O(M * N)
    Space: O(M * N)
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r: int, c: int):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return

        grid[r][c] = "0" # Mark visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)

    return count
```

### 2. Max Area of Island
**Difficulty:** Medium
**Concept:** Return size

```python
from typing import List

def max_area_island(grid: List[List[int]]) -> int:
    """
    Find the largest island by area.

    >>> max_area_island([[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0]])
    4

    Time: O(M * N)
    Space: O(M * N)
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    max_area = 0

    def dfs(r: int, c: int) -> int:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
            return 0

        grid[r][c] = 0 # Mark visited
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

### 3. Island Perimeter
**Difficulty:** Easy
**Concept:** Counting pattern

```python
from typing import List

def island_perimeter(grid: List[List[int]]) -> int:
    """
    Calculate perimeter of island.

    >>> island_perimeter([[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]])
    16

    Time: O(M * N)
    Space: O(1)
    """
    rows, cols = len(grid), len(grid[0])
    perimeter = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                perimeter += 4
                if r > 0 and grid[r-1][c] == 1:
                    perimeter -= 2
                if c > 0 and grid[r][c-1] == 1:
                    perimeter -= 2

    return perimeter
```

### 4. Flood Fill
**Difficulty:** Easy
**Concept:** Simple traversal

```python
from typing import List

def flood_fill(image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
    """
    Perform a flood fill.

    Time: O(M * N)
    Space: O(M * N)
    """
    start_color = image[sr][sc]
    if start_color == color: return image
    rows, cols = len(image), len(image[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or image[r][c] != start_color:
            return
        image[r][c] = color
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    dfs(sr, sc)
    return image
```

### 5. Surrounded Regions
**Difficulty:** Medium
**Concept:** Border-connected

```python
from typing import List

def solve(board: List[List[str]]) -> None:
    """
    Capture all regions surrounded by 'X'.

    Time: O(M * N)
    Space: O(M * N)
    """
    if not board: return
    rows, cols = len(board), len(board[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
            return
        board[r][c] = 'T'
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    for r in range(rows):
        dfs(r, 0)
        dfs(r, cols-1)
    for c in range(cols):
        dfs(0, c)
        dfs(rows-1, c)

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O': board[r][c] = 'X'
            elif board[r][c] == 'T': board[r][c] = 'O'
```

### 6. Number of Distinct Islands
**Difficulty:** Medium
**Concept:** Shape signature

```python
from typing import List, Set, Tuple

def num_distinct_islands(grid: List[List[int]]) -> int:
    """
    Count number of distinct island shapes.

    Time: O(M * N)
    Space: O(M * N)
    """
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    visited = set()
    shapes = set()

    def dfs(r, c, r0, c0, shape):
        if r < 0 or r >= rows or c < 0 or c >= cols or \
           grid[r][c] == 0 or (r, c) in visited:
            return
        visited.add((r, c))
        shape.append((r - r0, c - c0))
        dfs(r+1, c, r0, c0, shape)
        dfs(r-1, c, r0, c0, shape)
        dfs(r, c+1, r0, c0, shape)
        dfs(r, c-1, r0, c0, shape)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                shape = []
                dfs(r, c, r, c, shape)
                shapes.add(tuple(shape))

    return len(shapes)
```

### 7. Making A Large Island
**Difficulty:** Hard
**Concept:** What-if analysis

```python
from typing import List, Dict, Set

def largest_island(grid: List[List[int]]) -> int:
    """
    Return the maximum area of an island you can get by flipping one 0 to 1.

    Time: O(N^2)
    Space: O(N^2)
    """
    n = len(grid)
    island_id = 2
    area = {0: 0}

    def dfs(r, c, id_):
        if r < 0 or r >= n or c < 0 or c >= n or grid[r][c] != 1:
            return 0
        grid[r][c] = id_
        res = 1
        for nr, nc in [(r+1,c), (r-1,c), (r,c+1), (r,c-1)]:
            res += dfs(nr, nc, id_)
        return res

    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                area[island_id] = dfs(r, c, island_id)
                island_id += 1

    ans = max(area.values())
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                seen = {0}
                curr = 1
                for nr, nc in [(r+1,c), (r-1,c), (r,c+1), (r,c-1)]:
                    if 0 <= nr < n and 0 <= nc < n:
                        id_ = grid[nr][nc]
                        if id_ not in seen:
                            curr += area[id_]
                            seen.add(id_)
                ans = max(ans, curr)
    return ans
```

### 8. Pacific Atlantic Water Flow
**Difficulty:** Medium
**Concept:** Multi-source

```python
from typing import List, Set, Tuple

def pacific_atlantic(heights: List[List[int]]) -> List[List[int]]:
    """
    Find cells that can flow to both Pacific and Atlantic.

    Time: O(M * N)
    Space: O(M * N)
    """
    if not heights: return []
    rows, cols = len(heights), len(heights[0])
    p_vis, a_vis = set(), set()

    def dfs(r, c, visited, prev_h):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or \
           heights[r][c] < prev_h:
            return
        visited.add((r, c))
        for nr, nc in [(r+1,c), (r-1,c), (r,c+1), (r,c-1)]:
            dfs(nr, nc, visited, heights[r][c])

    for c in range(cols):
        dfs(0, c, p_vis, heights[0][c])
        dfs(rows-1, c, a_vis, heights[rows-1][c])
    for r in range(rows):
        dfs(r, 0, p_vis, heights[r][0])
        dfs(r, cols-1, a_vis, heights[r][cols-1])

    return [[r, c] for r in range(rows) for c in range(cols) if (r, c) in p_vis and (r, c) in a_vis]
```
