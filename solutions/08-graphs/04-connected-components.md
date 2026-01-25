# Solutions: Connected Components

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Number of Islands | Medium | Grid components |
| 2 | Max Area of Island | Medium | Component size |
| 3 | Number of Connected Components in an Undirected Graph | Medium | Graph components |
| 4 | Friend Circles (Number of Provinces) | Medium | Adjacency matrix |
| 5 | Surrounded Regions | Medium | Border-connected |
| 6 | Number of Provinces | Medium | Same as friend circles |

---

## 1. Number of Islands

### Problem Statement
Given an `m x n` 2D binary grid, count the number of islands.

### Optimal Python Solution

```python
def numIslands(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    islands = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == "0":
            return
        grid[r][c] = "0" # Mark visited
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                islands += 1
                dfs(r, c)
    return islands
```

### Explanation
- **Concept**: Each connected group of "1"s forms a component.
- **Algorithm**: Iterate through the grid. When a "1" is found, increment the counter and trigger a DFS to mark all connected "1"s as "0".
- **Complexity**: Time O(MN), Space O(MN) due to recursion.

---

## 2. Max Area of Island

### Problem Statement
Given an `m x n` binary grid, return the maximum area of an island. The area of an island is the number of cells with value 1 in the island.

### Examples & Edge Cases
- **Example 1**: `grid = [[0,1,1],[1,1,0],[0,0,1]]` -> Output: 4 (The island at top-left)

### Optimal Python Solution

```python
def maxAreaOfIsland(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    max_area = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 0:
            return 0

        grid[r][c] = 0 # Mark visited
        # Return 1 (current cell) + area of neighbors
        return 1 + dfs(r+1, c) + dfs(r-1, c) + dfs(r, c+1) + dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                max_area = max(max_area, dfs(r, c))

    return max_area
```

### Explanation
- **Concept**: Finding the size of each component.
- **Algorithm**: Instead of just marking nodes as visited, the DFS returns the total number of nodes it visited in that component.
- **Complexity**: Time O(MN), Space O(MN).

---

## 3. Number of Connected Components in an Undirected Graph

### Problem Statement
Given `n` nodes and a list of edges, find the number of connected components.

### Optimal Python Solution

```python
from collections import defaultdict

def countComponents(n: int, edges: list[list[int]]) -> int:
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = set()
    components = 0

    def dfs(node):
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                dfs(neighbor)

    for i in range(n):
        if i not in visited:
            components += 1
            dfs(i)

    return components
```

### Explanation
- **Concept**: Finding components in an explicit graph.
- **Algorithm**: Standard graph traversal (DFS or BFS) applied to every node. If a node hasn't been visited, it's part of a new component.
- **Complexity**: Time O(V + E), Space O(V + E).

---

## 4. Friend Circles (Number of Provinces)

### Problem Statement
There are `n` cities. Some of them are connected, while some are not. If city `a` is connected directly with city `b`, and city `b` is connected directly with city `c`, then city `a` is connected indirectly with city `c`. A province is a group of directly or indirectly connected cities. Given an `n x n` matrix `isConnected` where `isConnected[i][j] = 1` if the `i-th` city and the `j-th` city are directly connected, return the total number of provinces.

### Optimal Python Solution

```python
def findCircleNum(isConnected: list[list[int]]) -> int:
    n = len(isConnected)
    visited = set()
    provinces = 0

    def dfs(city):
        for neighbor, connected in enumerate(isConnected[city]):
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

### Explanation
- **Input Format**: The graph is given as an adjacency matrix.
- **Algorithm**: We iterate through each city. If it's not visited, we start a DFS. Inside DFS, we check all other cities (`enumerate(isConnected[city])`) to find neighbors.
- **Complexity**: Time O(N²), Space O(N).

---

## 5. Surrounded Regions

### Problem Statement
Given an `m x n` matrix `board` containing 'X' and 'O', capture all regions that are 4-directionally surrounded by 'X'. A region is captured by flipping all 'O's into 'X's in that surrounded region.

### Optimal Python Solution

```python
def solve(board: list[list[str]]) -> None:
    if not board: return
    rows, cols = len(board), len(board[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
            return
        board[r][c] = 'T' # Temporarily mark as "Not Surrounded"
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    # 1. Start DFS from 'O's on the border
    for r in range(rows):
        dfs(r, 0)
        dfs(r, cols - 1)
    for c in range(cols):
        dfs(0, c)
        dfs(rows - 1, c)

    # 2. Reconstruct board
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O': # Surrounded
                board[r][c] = 'X'
            elif board[r][c] == 'T': # Not surrounded
                board[r][c] = 'O'
```

### Explanation
- **Insight**: An 'O' region is *not* surrounded if and only if it is connected to the border.
- **Algorithm**:
    1. Identify all 'O's on the borders and run DFS to mark all reachable 'O's with a temporary character 'T'.
    2. Any remaining 'O's are surrounded and should be flipped to 'X'.
    3. Flip 'T' back to 'O'.
- **Complexity**: Time O(MN), Space O(MN).

---

## 6. Number of Provinces

### Problem Statement
Same as **Friend Circles** (Problem 4).

### Optimal Python Solution (Union-Find Approach)

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.count = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX, rootY = self.find(x), self.find(y)
        if rootX != rootY:
            self.parent[rootX] = rootY
            self.count -= 1

def findCircleNum(isConnected: list[list[int]]) -> int:
    n = len(isConnected)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                uf.union(i, j)
    return uf.count
```

### Explanation
- **Union-Find**: Excellent for connectivity problems. Each connection between cities `i` and `j` results in a `union` operation.
- **Complexity**: Time O(N² × α(N)), Space O(N).
