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
