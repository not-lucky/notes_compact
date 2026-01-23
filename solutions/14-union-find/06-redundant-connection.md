# Practice Problems: Redundant Connection (Cycle Detection)

## Problem 1: Redundant Connection
**LeetCode 684**

### Problem Statement
In this problem, a tree is an **undirected graph** that is connected and has no cycles.

You are given a graph that started as a tree with `n` nodes labeled from `1` to `n`, with one additional edge added. The added edge has two different vertices chosen from `1` to `n`, and was not an edge that already existed. The graph is represented as an array `edges` of length `n` where `edges[i] = [ai, bi]` indicates that there is an edge between nodes `ai` and `bi` in the graph.

Return an edge that can be removed so that the resulting graph is a tree of `n` nodes. If there are multiple answers, return the answer that occurs last in the input.

### Constraints
- `n == edges.length`
- `3 <= n <= 1000`
- `edges[i].length == 2`
- `1 <= ai < bi <= n`
- `ai != bi`
- There are no repeated edges.
- The given graph is connected.

### Example
**Input:** `edges = [[1,2],[1,3],[2,3]]`
**Output:** `[2,3]`

### Python Implementation
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n + 1))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y
            return True
        return False

def findRedundantConnection(edges: list[list[int]]) -> list[int]:
    n = len(edges)
    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
    return []
```

---

## Problem 2: Redundant Connection II
**LeetCode 685**

### Problem Statement
In this problem, a rooted tree is a **directed graph** such that, there is exactly one node (the root) for which all other nodes are descendants of this node, plus every node has exactly one parent, except for the root node which has no parents.

The given input is a directed graph that started as a rooted tree with `n` nodes (with distinct values from `1` to `n`), with one additional directed edge added. The added edge has two different vertices chosen from `1` to `n`, and was not an edge that already existed.

The resulting graph is given as a 2D-array `edges`. Each element of `edges` is a pair `[ui, vi]` that represents a **directed** edge connecting node `ui` to node `vi`, where `ui` is a parent of child `vi`.

Return an edge that can be removed so that the resulting graph is a rooted tree of `n` nodes. If there are multiple answers, return the answer that occurs last in the input.

### Constraints
- `n == edges.length`
- `3 <= n <= 1000`
- `edges[i].length == 2`
- `1 <= ui, vi <= n`
- `ui != vi`

### Example
**Input:** `edges = [[1,2],[1,3],[2,3]]`
**Output:** `[2,3]`

### Python Implementation
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n + 1))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y
            return True
        return False

def findRedundantDirectedConnection(edges: list[list[int]]) -> list[int]:
    n = len(edges)
    parent = [0] * (n + 1)
    cand1 = cand2 = None

    for i, (u, v) in enumerate(edges):
        if parent[v] != 0:
            cand1 = [parent[v], v]
            cand2 = [u, v]
            edges[i] = [-1, -1] # Mark for skipping
            break
        parent[v] = u

    uf = UnionFind(n)
    for u, v in edges:
        if u == -1: continue
        if not uf.union(u, v):
            if cand1: return cand1
            return [u, v]

    return cand2
```

---

## Problem 3: Detect Cycle in 2D Grid
**LeetCode 1559**

### Problem Statement
Given a 2D array of characters `grid` of size `m x n`, you need to find if there exists any cycle consisting of the **same value** in `grid`.

A cycle is a path of length 4 or more in the grid that starts and ends at the same cell. From a given cell, you can move to one of the cells adjacent to it - in up, down, left, or right direction, if it has the same value of the current cell.

Also, you cannot move to the cell that you visited in your last move. For example, if you are at `(1, 1)` and you moved to `(1, 2)`, then in the next move you cannot move back to `(1, 1)`.

Return `true` if any cycle of the same value exists in `grid`, otherwise, return `false`.

### Constraints
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 500`
- `grid[i][j]` is a lowercase English letter.

### Example
**Input:** `grid = [["a","a","a","a"],["a","b","b","a"],["a","b","b","a"],["a","a","a","a"]]`
**Output:** `true`

### Python Implementation
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y
            return True
        return False

def containsCycle(grid: list[list[str]]) -> bool:
    rows, cols = len(grid), len(grid[0])
    uf = UnionFind(rows * cols)

    for r in range(rows):
        for c in range(cols):
            # Check right neighbor
            if c + 1 < cols and grid[r][c] == grid[r][c + 1]:
                if not uf.union(r * cols + c, r * cols + (c + 1)):
                    return True
            # Check down neighbor
            if r + 1 < rows and grid[r][c] == grid[r + 1][c]:
                if not uf.union(r * cols + c, (r + 1) * cols + c):
                    return True

    return False
```

---

## Problem 4: Min Cost to Connect All Points
**LeetCode 1584**

### Problem Statement
You are given an array `points` representing integer coordinates of some points on a 2D-plane, where `points[i] = [xi, yi]`.

The cost of connecting two points `[xi, yi]` and `[xj, yj]` is the **manhattan distance** between them: `|xi - xj| + |yi - yj|`, where `|val|` denotes the absolute value of `val`.

Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.

### Constraints
- `1 <= points.length <= 1000`
- `-10^6 <= xi, yi <= 10^6`
- All points are distinct.

### Example
**Input:** `points = [[0,0],[2,2],[3,10],[5,2],[7,0]]`
**Output:** `20`

### Python Implementation
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
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y
            self.count -= 1
            return True
        return False

def minCostConnectPoints(points: list[list[int]]) -> int:
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            edges.append((dist, i, j))

    edges.sort()
    uf = UnionFind(n)
    min_cost = 0
    num_edges = 0

    for dist, u, v in edges:
        if uf.union(u, v):
            min_cost += dist
            num_edges += 1
            if num_edges == n - 1:
                break

    return min_cost
```
