# Connected Components

## Practice Problems

### 1. Number of Connected Components in an Undirected Graph
**Difficulty:** Medium
**Concept:** Graph components

```python
from collections import defaultdict
from typing import List

def count_components(n: int, edges: List[List[int]]) -> int:
    """
    You have a graph of n nodes. You are given an integer n and an array edges
    where edges[i] = [ai, bi] indicates that there is an edge between ai and bi in the graph.
    Return the number of connected components in the graph.

    >>> count_components(5, [[0,1],[1,2],[3,4]])
    2
    >>> count_components(5, [[0,1],[1,2],[2,3],[3,4]])
    1

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    count = 0

    def dfs(node: int):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    for i in range(n):
        if i not in visited:
            count += 1
            dfs(i)

    return count
```

### 2. Max Area of Island
**Difficulty:** Medium
**Concept:** Component size

```python
from typing import List

def max_area_island(grid: List[List[int]]) -> int:
    """
    You are given an m x n binary matrix grid. An island is a group of 1's
    (representing land) connected 4-directionally (horizontal or vertical).
    You may assume all four edges of the grid are surrounded by water.
    The area of an island is the number of cells with a value 1 in the island.
    Return the maximum area of an island in grid. If there is no island, return 0.

    >>> max_area_island([[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0]])
    4

    Time: O(M * N)
    Space: O(M * N)
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    max_area = 0
    visited = set()

    def dfs(r: int, c: int) -> int:
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] == 0 or (r, c) in visited):
            return 0

        visited.add((r, c))
        area = 1
        area += dfs(r + 1, c)
        area += dfs(r - 1, c)
        area += dfs(r, c + 1)
        area += dfs(r, c - 1)
        return area

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                max_area = max(max_area, dfs(r, c))

    return max_area
```

### 3. Number of Provinces
**Difficulty:** Medium
**Concept:** Adjacency matrix

```python
from typing import List

def find_circle_num(is_connected: List[List[int]]) -> int:
    """
    There are n cities. Some of them are connected, while some are not.
    If city a is connected directly with city b, and city b is connected
    directly with city c, then city a is connected indirectly with city c.
    A province is a group of directly or indirectly connected cities and
    no other cities outside of the group.
    You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the
    ith city and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.
    Return the total number of provinces.

    >>> find_circle_num([[1,1,0],[1,1,0],[0,0,1]])
    2
    >>> find_circle_num([[1,0,0],[0,1,0],[0,0,1]])
    3

    Time: O(N^2)
    Space: O(N)
    """
    n = len(is_connected)
    visited = set()
    provinces = 0

    def dfs(city: int):
        for neighbor, connected in enumerate(is_connected[city]):
            if connected == 1 and neighbor not in visited:
                visited.add(neighbor)
                dfs(neighbor)

    for i in range(n):
        if i not in visited:
            provinces += 1
            visited.add(i)
            dfs(i)

    return provinces
```

### 4. Surrounded Regions
**Difficulty:** Medium
**Concept:** Border-connected

```python
from typing import List

def solve(board: List[List[str]]) -> None:
    """
    Given an m x n matrix board containing 'X' and 'O', capture all regions
    that are 4-directionally surrounded by 'X'.
    A region is captured by flipping all 'O's into 'X's in that surrounded region.

    Time: O(M * N)
    Space: O(M * N)
    """
    if not board:
        return

    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int):
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
            return

        board[r][c] = 'T' # Temporary marker
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    # Mark border-connected 'O's
    for r in range(rows):
        dfs(r, 0)
        dfs(r, cols - 1)
    for c in range(cols):
        dfs(0, c)
        dfs(rows - 1, c)

    # Flip 'O' to 'X' (captured) and 'T' back to 'O' (not captured)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == 'T':
                board[r][c] = 'O'
```
