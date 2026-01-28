# Union-Find Basics Solutions

## 1. Number of Provinces
**Problem Statement**:
There are `n` cities. Some of them are connected, while some are not. If city `a` is connected directly with city `b`, and city `b` is connected directly with city `c`, then city `a` is connected indirectly with city `c`. A province is a group of directly or indirectly connected cities and no other cities outside of the group.
Given an `n x n` matrix `isConnected` where `isConnected[i][j] = 1` if the `i-th` city and the `j-th` city are directly connected, and `isConnected[i][j] = 0` otherwise, return the total number of provinces.

**Examples & Edge Cases**:
- **Example 1**: `isConnected = [[1,1,0],[1,1,0],[0,0,1]]` → `2` (Cities 0 and 1 are connected, city 2 is separate).
- **Example 2**: `isConnected = [[1,0,0],[0,1,0],[0,0,1]]` → `3` (All cities are separate).
- **Edge Case**: `n = 1` → `1` province.
- **Edge Case**: Fully connected graph → `1` province.

**Optimal Python Solution**:
```python
class UnionFind:
    def __init__(self, n):
        # Initialize each node as its own parent
        self.parent = list(range(n))
        # Rank tracks the depth of the tree to keep it balanced
        self.rank = [0] * n
        # Count of disjoint sets
        self.count = n

    def find(self, x):
        # Path compression: point node directly to root
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            # Union by rank: attach shorter tree under taller tree
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_x] = root_y
                self.rank[root_y] += 1
            self.count -= 1
            return True
        return False

def findCircleNum(isConnected: list[list[int]]) -> int:
    n = len(isConnected)
    uf = UnionFind(n)

    # Iterate through the matrix (upper triangle only)
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                uf.union(i, j)

    return uf.count
```

**Explanation**:
1. We initialize a `UnionFind` object with `n` elements, where each city is its own province initially.
2. We iterate through the `isConnected` matrix. Since it's symmetric, we only need to check the upper triangle (`j > i`).
3. For every connection (`isConnected[i][j] == 1`), we perform a `union` operation on cities `i` and `j`.
4. The `union` operation merges the sets containing `i` and `j` and decrements the total count of provinces.
5. After processing all connections, the remaining `count` is the number of provinces.

**Complexity Analysis**:
- **Time Complexity**: $O(n^2 \alpha(n))$, where $n$ is the number of cities. We iterate through $n^2/2$ pairs, and each union/find operation takes $O(\alpha(n))$ time.
- **Space Complexity**: $O(n)$ to store the `parent` array.

---

## 2. Graph Valid Tree
**Problem Statement**:
Given `n` nodes labeled from `0` to `n-1` and a list of undirected edges, write a function to check whether these edges make up a valid tree.

**Examples & Edge Cases**:
- **Example 1**: `n = 5, edges = [[0,1], [0,2], [0,3], [1,4]]` → `True`.
- **Example 2**: `n = 5, edges = [[0,1], [1,2], [2,3], [1,3], [1,4]]` → `False` (Cycle detected).
- **Edge Case**: `n = 1, edges = []` → `True`.
- **Edge Case**: `n = 5, edges = [[0,1], [2,3]]` → `False` (Disconnected).

**Optimal Python Solution**:
```python
def validTree(n: int, edges: list[list[int]]) -> bool:
    # A valid tree with n nodes must have exactly n-1 edges
    if len(edges) != n - 1:
        return False

    parent = list(range(n))

    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x == root_y:
            return False # Cycle detected

        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_x] = root_y
            rank[root_y] += 1
        return True

    for u, v in edges:
        if not union(u, v):
            return False # Cycle detected

    return True
```

**Explanation**:
1. For a graph to be a tree, it must satisfy two conditions: it must be connected and it must not contain any cycles.
2. A key property of a tree with `n` nodes is that it must have exactly `n-1` edges. If `len(edges) != n - 1`, we return `False` immediately.
3. We use Union-Find to process each edge. If we find an edge `(u, v)` where `u` and `v` are already in the same set (`find(u) == find(v)`), it means adding this edge creates a cycle.
4. If we successfully process all `n-1` edges without detecting a cycle, the graph must be connected and thus a valid tree.

**Complexity Analysis**:
- **Time Complexity**: $O(n \alpha(n))$, where $n$ is the number of nodes. We process $n-1$ edges, and each operation is nearly constant time.
- **Space Complexity**: $O(n)$ to store the `parent` array.

---

## 3. Number of Connected Components in an Undirected Graph
**Problem Statement**:
You have a graph of `n` nodes. You are given an integer `n` and an array `edges` where `edges[i] = [ai, bi]` indicates that there is an edge between `ai` and `bi` in the graph. Return the number of connected components in the graph.

**Examples & Edge Cases**:
- **Example 1**: `n = 5, edges = [[0,1], [1,2], [3,4]]` → `2`.
- **Example 2**: `n = 5, edges = [[0,1], [1,2], [2,3], [3,4]]` → `1`.
- **Edge Case**: `n = 5, edges = []` → `5`.
- **Edge Case**: `n = 0` → `0` (or `n=1` → `1`).

**Optimal Python Solution**:
```python
def countComponents(n: int, edges: list[list[int]]) -> int:
    parent = list(range(n))
    rank = [0] * n
    count = n # Start with n components

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        nonlocal count
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_x] = root_y
                rank[root_y] += 1
            count -= 1 # Decrement count on merge
            return True
        return False

    for u, v in edges:
        union(u, v)

    return count
```

**Explanation**:
1. This is a direct application of Union-Find for counting disjoint sets.
2. We initialize `count` to `n`.
3. For every edge, we attempt to `union` the two nodes.
4. If the nodes were in different sets, we merge them and decrement `count`.
5. The final value of `count` represents the total number of connected components.

**Complexity Analysis**:
- **Time Complexity**: $O(E \alpha(V))$, where $E$ is the number of edges and $V$ is the number of nodes.
- **Space Complexity**: $O(V)$ to store the `parent` array.

---

## 4. Earliest Moment When Everyone Becomes Friends
**Problem Statement**:
There are `n` people and a list of logs where `logs[i] = [timestamp, x, y]` indicates that `x` and `y` became friends at `timestamp`. Friendship is transitive. Return the earliest timestamp such that everyone is in the same friend group. If no such time exists, return -1.

**Examples & Edge Cases**:
- **Example 1**: `n = 6, logs = [[20190101,0,1], [20190104,3,4], [20190107,2,3], [20190211,1,5], [20190224,2,4], [20190301,0,3]]` → `20190301`.
- **Edge Case**: Not everyone becomes friends → `-1`.
- **Edge Case**: `n = 1` → `0`.

**Optimal Python Solution**:
```python
def earliestAcq(logs: list[list[int]], n: int) -> int:
    # Sort logs by timestamp to process events in order
    logs.sort(key=lambda x: x[0])

    parent = list(range(n))
    rank = [0] * n
    count = n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        nonlocal count
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_x] = root_y
                rank[root_y] += 1
            count -= 1
            return True
        return False

    for ts, u, v in logs:
        if union(u, v):
            if count == 1:
                return ts

    return -1
```

**Explanation**:
1. We must process the logs in chronological order, so we first sort them by `timestamp`.
2. We use Union-Find to track friendship groups, starting with `n` groups.
3. For each log, we merge the two people's groups.
4. The first time `count` becomes `1`, it means everyone is in the same group. We return that timestamp.
5. If we finish all logs and `count > 1`, we return `-1`.

**Complexity Analysis**:
- **Time Complexity**: $O(L \log L + L \alpha(n))$, where $L$ is the number of logs. Sorting takes $O(L \log L)$, and processing logs takes $O(L \alpha(n))$.
- **Space Complexity**: $O(n)$ for the Union-Find structure.

---

## 5. Number of Islands (Union-Find Approach)
**Problem Statement**:
Given an `m x n` 2D binary grid `grid` which represents a map of '1's (land) and '0's (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.

**Examples & Edge Cases**:
- **Example 1**: `grid = [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]` → `1`.
- **Example 2**: `grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]` → `3`.
- **Edge Case**: All '0's → `0`.
- **Edge Case**: All '1's → `1`.

**Optimal Python Solution**:
```python
def numIslands(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    parent = list(range(rows * cols))
    rank = [0] * (rows * cols)
    count = 0

    # Initialize count based on number of land cells
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        nonlocal count
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_x] = root_y
                rank[root_y] += 1
            count -= 1

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                # Check neighbors (right and down) to merge sets
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if nr < rows and nc < cols and grid[nr][nc] == "1":
                        union(r * cols + c, nr * cols + nc)

    return count
```

**Explanation**:
1. We treat each cell `(r, c)` as a node in a graph. We map 2D coordinates to a 1D index: `r * cols + c`.
2. Initially, the number of components is equal to the number of '1' cells.
3. We iterate through the grid. When we find a '1', we check its neighbors to the right and bottom.
4. If a neighbor is also a '1', we perform a `union` and decrement the island `count`.
5. After scanning the whole grid, the remaining `count` is the number of islands.

**Complexity Analysis**:
- **Time Complexity**: $O(m \times n \alpha(m \times n))$, where $m$ and $n$ are grid dimensions.
- **Space Complexity**: $O(m \times n)$ to store the `parent` array.
