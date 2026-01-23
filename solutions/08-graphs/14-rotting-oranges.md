# Rotting Oranges (Multi-Source BFS)

## Practice Problems

### 1. Rotting Oranges
**Difficulty:** Medium
**Concept:** Core problem

```python
from collections import deque
from typing import List

def oranges_rotting(grid: List[List[int]]) -> int:
    """
    Find minimum time for all oranges to rot.

    >>> oranges_rotting([[2,1,1],[1,1,0],[0,1,1]])
    4
    >>> oranges_rotting([[2,1,1],[0,1,1],[1,0,1]])
    -1
    >>> oranges_rotting([[0,2]])
    0

    Time: O(M * N)
    Space: O(M * N)
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0

    max_time = 0
    while queue:
        r, c, t = queue.popleft()
        max_time = max(max_time, t)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                queue.append((nr, nc, t + 1))

    return max_time if fresh == 0 else -1
```

### 2. 01 Matrix
**Difficulty:** Medium
**Concept:** Distance to 0

```python
from collections import deque
from typing import List

def update_matrix(mat: List[List[int]]) -> List[List[int]]:
    """
    For each cell, find distance to nearest 0.

    Time: O(M * N)
    Space: O(M * N)
    """
    rows, cols = len(mat), len(mat[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    queue = deque()

    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                dist[r][c] = 0
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if dist[nr][nc] > dist[r][c] + 1:
                    dist[nr][nc] = dist[r][c] + 1
                    queue.append((nr, nc))

    return dist
```

### 3. Walls and Gates
**Difficulty:** Medium
**Concept:** Distance to gate

```python
from collections import deque
from typing import List

def walls_and_gates(rooms: List[List[int]]) -> None:
    """
    Fill distance to nearest gate for each empty room.
    -1: wall, 0: gate, INF: empty room.

    Time: O(M * N)
    Space: O(M * N)
    """
    if not rooms:
        return

    rows, cols = len(rooms), len(rooms[0])
    INF = 2147483647
    queue = deque()

    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] == 0:
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF:
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
```
