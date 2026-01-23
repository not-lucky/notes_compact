# Practice Problems: Union by Rank

## Problem 1: Most Stones Removed with Same Row or Column
**LeetCode 947**

### Problem Statement
On a 2D plane, we place `n` stones at some integer coordinate points. Each coordinate point may have at most one stone.

A stone can be removed if it shares either the same row or the same column as another stone that has not been removed.

Given an array `stones` of length `n` where `stones[i] = [ri, ci]` represents the location of the `ith` stone, return the largest possible number of stones that can be removed.

### Constraints
- `1 <= stones.length <= 1000`
- `0 <= ri, ci <= 10^4`
- All the `[ri, ci]` are unique.

### Example
**Input:** `stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]`
**Output:** `5`
**Explanation:** One way to remove 5 stones is as follows:
1. Remove stone [2,2] because it shares the same row as [2,1].
2. Remove stone [2,1] because it shares the same column as [0,1].
3. Remove stone [1,2] because it shares the same column as [2,2] (wait, this depends on order).
Actually, the insight is: `Answer = total stones - number of connected components`.

### Python Implementation
```python
class UnionFind:
    def __init__(self):
        self.parent = {}
        self.count = 0

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.count += 1
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y
            self.count -= 1

def removeStones(stones: list[list[int]]) -> int:
    uf = UnionFind()
    for r, c in stones:
        # Offset column to distinguish from row index
        uf.union(r, c + 10001)
    return len(stones) - uf.count
```

---

## Problem 2: Swim in Rising Water
**LeetCode 778**

### Problem Statement
You are given an `n x n` integer matrix `grid` where each value `grid[i][j]` represents the elevation at that point `(i, j)`.

The rain starts to fall. At time `t`, the depth of the water everywhere is `t`. You can swim from a square to another 4-directionally adjacent square if and only if the elevation of both squares individually are at most `t`. You can swim infinite distances in zero time. Of course, you must stay within the boundaries of the grid during your swim.

Return the least time until you can reach the bottom right square `(n - 1, n - 1)` if you start at the top left square `(0, 0)`.

### Constraints
- `n == grid.length`
- `n == grid[i].length`
- `1 <= n <= 50`
- `0 <= grid[i][j] < n^2`
- Each value `grid[i][j]` is **unique**.

### Example
**Input:** `grid = [[0,2],[1,3]]`
**Output:** `3`

### Python Implementation
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1

def swimInWater(grid: list[list[int]]) -> int:
    n = len(grid)
    positions = [None] * (n * n)
    for r in range(n):
        for c in range(n):
            positions[grid[r][c]] = (r, c)

    uf = UnionFind(n * n)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for t in range(n * n):
        r, c = positions[t]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] <= t:
                uf.union(r * n + c, nr * n + nc)

        if uf.find(0) == uf.find(n * n - 1):
            return t

    return -1
```

---

## Problem 3: Minimize Malware Spread
**LeetCode 924**

### Problem Statement
You are given a network of `n` nodes represented as an `n x n` adjacency matrix `graph`, where `graph[i][j] = 1` if there is a direct connection between nodes `i` and `j`.

Some nodes `initial` are initially infected by malware. Whenever two nodes are directly connected, and at least one of those two nodes is infected by malware, both nodes will be infected by malware. This spread of malware will continue until no more nodes can be infected.

Suppose `M(initial)` is the final number of nodes infected with malware in the entire network after the spread of malware stops. We will remove exactly one node from `initial`.

Return the node that, if removed, would minimize `M(initial)`. If multiple nodes could be removed to minimize `M(initial)`, return such a node with the smallest index.

### Constraints
- `n == graph.length`
- `n == graph[i].length`
- `2 <= n <= 300`
- `graph[i][j]` is `0` or `1`.
- `graph[i][i]` is `1`.
- `graph[i][j] == graph[j][i]`
- `1 <= initial.length <= n`
- `0 <= initial[i] <= n - 1`
- All the numbers in `initial` are **unique**.

### Example
**Input:** `graph = [[1,1,0],[1,1,0],[0,0,1]]`, `initial = [0,1]`
**Output:** `0`

### Python Implementation
```python
import collections

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.size[root_x] < self.size[root_y]:
                root_x, root_y = root_y, root_x
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]

def minMalwareSpread(graph: list[list[int]], initial: list[int]) -> int:
    n = len(graph)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                uf.union(i, j)

    # Count how many infected nodes in each component
    count = collections.Counter()
    for node in initial:
        count[uf.find(node)] += 1

    initial.sort()
    res = initial[0]
    max_saved = -1

    for node in initial:
        root = uf.find(node)
        if count[root] == 1: # Only this node infects the component
            saved = uf.size[root]
            if saved > max_saved:
                max_saved = saved
                res = node

    return res
```

---

## Problem 4: Making A Large Island
**LeetCode 827**

### Problem Statement
You are given an `n x n` binary matrix `grid`. You are allowed to change at most one `0` to be `1`.

Return the size of the largest island in `grid` after applying this operation.

An **island** is a 4-directionally connected group of `1`s.

### Constraints
- `n == grid.length`
- `n == grid[i].length`
- `1 <= n <= 500`
- `grid[i][j]` is either `0` or `1`.

### Example
**Input:** `grid = [[1,0],[0,1]]`
**Output:** `3`

### Python Implementation
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.size[root_x] < self.size[root_y]:
                root_x, root_y = root_y, root_x
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]

def largestIsland(grid: list[list[int]]) -> int:
    n = len(grid)
    uf = UnionFind(n * n)
    has_zero = False

    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                        uf.union(r * n + c, nr * n + nc)
            else:
                has_zero = True

    if not has_zero:
        return n * n

    max_size = 0
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                roots = set()
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                        roots.add(uf.find(nr * n + nc))

                current_size = 1
                for root in roots:
                    current_size += uf.size[root]
                max_size = max(max_size, current_size)

    return max_size
```
