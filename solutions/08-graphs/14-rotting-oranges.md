# Solutions: Rotting Oranges (Multi-Source BFS)

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Rotting Oranges | Medium | Core problem |
| 2 | 01 Matrix | Medium | Distance to 0 |
| 3 | Walls and Gates | Medium | Distance to gate |
| 4 | Shortest Bridge | Medium | Two islands |
| 5 | As Far from Land as Possible | Medium | Max distance |
| 6 | Map of Highest Peak | Medium | Distance from water |

---

## 1. Rotting Oranges

### Problem Statement
Minimum minutes until no fresh oranges remain.

### Optimal Python Solution

```python
from collections import deque

def orangesRotting(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2: queue.append((r, c))
            elif grid[r][c] == 1: fresh += 1

    if fresh == 0: return 0
    time = -1
    while queue:
        time += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
    return time if fresh == 0 else -1
```

### Explanation
- **Algorithm**: Multi-source BFS.
- **Complexity**: Time O(MN), Space O(MN).

---

## 2. 01 Matrix

### Problem Statement
Distance of the nearest 0 for each cell.

### Optimal Python Solution

```python
from collections import deque

def updateMatrix(mat: list[list[int]]) -> list[list[int]]:
    rows, cols = len(mat), len(mat[0])
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0: queue.append((r, c))
            else: mat[r][c] = float('inf')

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and mat[nr][nc] > mat[r][c] + 1:
                mat[nr][nc] = mat[r][c] + 1
                queue.append((nr, nc))
    return mat
```

---

## 3. Walls and Gates

### Problem Statement
Fill empty rooms with distance to the nearest gate.

### Optimal Python Solution

```python
from collections import deque

def wallsAndGates(rooms: list[list[int]]) -> None:
    if not rooms: return
    rows, cols = len(rooms), len(rooms[0])
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] == 0: queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == 2147483647:
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
```

---

## 4. Shortest Bridge

### Problem Statement
Find the shortest path between two islands.

### Optimal Python Solution

```python
from collections import deque

def shortestBridge(grid: list[list[int]]) -> int:
    n = len(grid)
    queue = deque()

    def dfs(r, c):
        if r < 0 or r >= n or c < 0 or c >= n or grid[r][c] != 1: return
        grid[r][c] = 2
        queue.append((r, c, 0))
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    found = False
    for r in range(n):
        if found: break
        for c in range(n):
            if grid[r][c] == 1:
                dfs(r, c)
                found = True
                break

    while queue:
        r, c, d = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                if grid[nr][nc] == 1: return d
                if grid[nr][nc] == 0:
                    grid[nr][nc] = 2
                    queue.append((nr, nc, d + 1))
    return -1
```

---

## 5. As Far from Land as Possible

### Problem Statement
Find a water cell such that its distance to the nearest land cell is maximized.

### Optimal Python Solution

```python
from collections import deque

def maxDistance(grid: list[list[int]]) -> int:
    n = len(grid)
    queue = deque()
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1: queue.append((r, c))

    if len(queue) == 0 or len(queue) == n * n: return -1
    dist = -1
    while queue:
        dist += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1
                    queue.append((nr, nc))
    return dist
```

---

## 6. Map of Highest Peak

### Problem Statement
Assign heights to each cell such that the maximum height is minimized, with water cells at height 0.

### Optimal Python Solution

```python
from collections import deque

def highestPeak(isWater: list[list[int]]) -> list[list[int]]:
    rows, cols = len(isWater), len(isWater[0])
    res = [[-1] * cols for _ in range(rows)]
    queue = deque()

    for r in range(rows):
        for c in range(cols):
            if isWater[r][c] == 1:
                res[r][c] = 0
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and res[nr][nc] == -1:
                res[nr][nc] = res[r][c] + 1
                queue.append((nr, nc))
    return res
```
