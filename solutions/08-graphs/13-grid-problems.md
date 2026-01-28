# Solutions: Grid Problems

## Practice Problems

| #   | Problem                     | Difficulty | Key Variation    |
| --- | --------------------------- | ---------- | ---------------- |
| 1   | Number of Islands           | Medium     | Basic counting   |
| 2   | Max Area of Island          | Medium     | Return size      |
| 3   | Flood Fill                  | Easy       | Simple traversal |
| 4   | Surrounded Regions          | Medium     | Border-connected |
| 5   | Number of Distinct Islands  | Medium     | Shape signature  |
| 6   | Making A Large Island       | Hard       | What-if analysis |
| 7   | Island Perimeter            | Easy       | Counting pattern |
| 8   | Pacific Atlantic Water Flow | Medium     | Multi-source     |

---

## 1. Number of Islands

### Problem Statement

Count islands (connected "1"s) in a grid.

### Optimal Python Solution

```python
def numIslands(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])
    islands = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == "0":
            return
        grid[r][c] = "0"
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                islands += 1
                dfs(r, c)
    return islands
```

---

## 2. Max Area of Island

### Problem Statement

Find the area of the largest island.

### Optimal Python Solution

```python
def maxAreaOfIsland(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 0:
            return 0
        grid[r][c] = 0
        return 1 + dfs(r+1, c) + dfs(r-1, c) + dfs(r, c+1) + dfs(r, c-1)

    max_area = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                max_area = max(max_area, dfs(r, c))
    return max_area
```

---

## 3. Flood Fill

### Problem Statement

Change color of connected pixels of the same starting color.

### Optimal Python Solution

```python
def floodFill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    start_color = image[sr][sc]
    if start_color == color: return image
    rows, cols = len(image), len(image[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or image[r][c] != start_color:
            return
        image[r][c] = color
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    dfs(sr, sc)
    return image
```

---

## 4. Surrounded Regions

### Problem Statement

Flip 'O's surrounded by 'X's to 'X's.

### Optimal Python Solution

```python
def solve(board: list[list[str]]) -> None:
    rows, cols = len(board), len(board[0])
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != "O":
            return
        board[r][c] = "T"
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    for r in range(rows):
        dfs(r, 0); dfs(r, cols-1)
    for c in range(cols):
        dfs(0, c); dfs(rows-1, c)

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "O": board[r][c] = "X"
            elif board[r][c] == "T": board[r][c] = "O"
```

---

## 5. Number of Distinct Islands

### Problem Statement

Count distinct shapes of islands.

### Optimal Python Solution

```python
def numDistinctIslands(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    shapes = set()

    def dfs(r, c, dr, dc, shape):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 0:
            return
        grid[r][c] = 0
        shape.append((dr, dc))
        dfs(r+1, c, dr+1, dc, shape)
        dfs(r-1, c, dr-1, dc, shape)
        dfs(r, c+1, dr, dc+1, shape)
        dfs(r, c-1, dr, dc-1, shape)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                shape = []
                dfs(r, c, 0, 0, shape)
                shapes.add(tuple(shape))
    return len(shapes)
```

---

## 6. Making A Large Island

### Problem Statement

Flip one '0' to maximize island area.

### Optimal Python Solution

```python
def largestIsland(grid: list[list[int]]) -> int:
    n = len(grid)
    sizes = {0: 0}
    label = 2

    def dfs(r, c, L):
        if r < 0 or r >= n or c < 0 or c >= n or grid[r][c] != 1:
            return 0
        grid[r][c] = L
        return 1 + dfs(r+1, c, L) + dfs(r-1, c, L) + dfs(r, c+1, L) + dfs(r, c-1, L)

    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                sizes[label] = dfs(r, c, label)
                label += 1

    ans = max(sizes.values())
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                possible = set()
                for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < n and 0 <= nc < n:
                        possible.add(grid[nr][nc])
                ans = max(ans, 1 + sum(sizes[L] for L in possible))
    return ans
```

---

## 7. Island Perimeter

### Problem Statement

Calculate perimeter of an island.

### Optimal Python Solution

```python
def islandPerimeter(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    ans = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                ans += 4
                if r > 0 and grid[r-1][c] == 1: ans -= 2
                if c > 0 and grid[r][c-1] == 1: ans -= 2
    return ans
```

---

## 8. Pacific Atlantic Water Flow

### Problem Statement

Find cells from which water can flow to both Pacific and Atlantic oceans.

### Optimal Python Solution

```python
def pacificAtlantic(heights: list[list[int]]) -> list[list[int]]:
    rows, cols = len(heights), len(heights[0])
    pac, atl = set(), set()

    def dfs(r, c, visit, prev_h):
        if (r, c) in visit or r < 0 or r >= rows or c < 0 or c >= cols or heights[r][c] < prev_h:
            return
        visit.add((r, c))
        dfs(r+1, c, visit, heights[r][c])
        dfs(r-1, c, visit, heights[r][c])
        dfs(r, c+1, visit, heights[r][c])
        dfs(r, c-1, visit, heights[r][c])

    for c in range(cols):
        dfs(0, c, pac, heights[0][c])
        dfs(rows-1, c, atl, heights[rows-1][c])
    for r in range(rows):
        dfs(r, 0, pac, heights[r][0])
        dfs(r, cols-1, atl, heights[r][cols-1])

    return list(pac & atl)
```
