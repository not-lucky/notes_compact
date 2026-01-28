# Union by Rank Solutions

## 1. Most Stones Removed with Same Row or Column
**Problem Statement**:
On a 2D plane, we place `n` stones at some integer coordinate points. Each coordinate point may have at most one stone. A stone can be removed if it shares either the same row or the same column as another stone that has not been removed. Return the largest possible number of stones that can be removed.

**Examples & Edge Cases**:
- **Example 1**: `stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]` → `5` (One stone remains in the single connected component).
- **Example 2**: `stones = [[0,0],[0,2],[1,1],[2,0],[2,2]]` → `3`.
- **Edge Case**: `n = 1` → `0`.
- **Edge Case**: Stones on completely different rows and columns → `0`.

**Optimal Python Solution**:
```python
def removeStones(stones: list[list[int]]) -> int:
    parent = {}
    rank = {}

    def find(x):
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
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
            return True
        return False

    # We use a trick: bitwise NOT (or large offset) for columns
    # to distinguish row 0 from column 0.
    num_islands = 0
    for r, c in stones:
        if r not in parent:
            num_islands += 1
        if ~c not in parent:
            num_islands += 1
        if union(r, ~c):
            num_islands -= 1

    return len(stones) - num_islands
```

**Explanation**:
1. Two stones are "connected" if they share a row or a column. We want to find connected components of stones.
2. For each component of size $k$, we can remove $k-1$ stones, leaving one behind.
3. Total stones removed = Total stones - Number of components.
4. We treat rows and columns as nodes in our graph. A stone at `(r, c)` creates an edge between row `r` and column `c`.
5. We use `~c` (bitwise NOT) to ensure column indices don't collide with row indices.

**Complexity Analysis**:
- **Time Complexity**: $O(n \alpha(n))$, where $n$ is the number of stones.
- **Space Complexity**: $O(n)$ to store parents of rows and columns.

---

## 2. Swim in Rising Water
**Problem Statement**:
In an `n x n` grid, each square `grid[i][j]` represents the elevation at that point. At time `t`, you can swim from a square to any adjacent square if both elevations are at most `t`. You start at `(0, 0)` and want to reach `(n-1, n-1)`. Return the least time `t` such that you can reach your destination.

**Examples & Edge Cases**:
- **Example 1**: `grid = [[0,2],[1,3]]` → `3` (Must wait until time 3 to reach (1,1)).
- **Example 2**: `grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]` → `16`.
- **Edge Case**: `n = 1` → `grid[0][0]`.

**Optimal Python Solution**:
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
                self.parent[root_x] = root_y
                self.rank[root_y] += 1
            return True
        return False

def swimInWater(grid: list[list[int]]) -> int:
    n = len(grid)
    # Map elevation to coordinates
    pos = [0] * (n * n)
    for r in range(n):
        for c in range(n):
            pos[grid[r][c]] = (r, c)

    uf = UnionFind(n * n)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Process each time t (elevation level)
    for t in range(n * n):
        r, c = pos[t]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] <= t:
                uf.union(r * n + c, nr * n + nc)

        # Check if start and end are connected
        if uf.find(0) == uf.find(n * n - 1):
            return t
    return n * n - 1
```

**Explanation**:
1. We can view this as a connectivity problem. At time `t`, we can move across any cell with elevation $\le t$.
2. We sort all cells by their elevation (or use an array since elevations are unique from $0$ to $n^2-1$).
3. We add cells one by one to our Union-Find structure in increasing order of elevation.
4. For each cell added, we connect it to any adjacent cells that have already been added.
5. The first time `find(start)` equals `find(end)`, the current elevation is our answer.

**Complexity Analysis**:
- **Time Complexity**: $O(n^2 \alpha(n^2))$, since we process each of the $n^2$ cells once.
- **Space Complexity**: $O(n^2)$ for Union-Find and position mapping.

---

## 3. Minimize Malware Spread
**Problem Statement**:
You are given a network of `n` nodes represented as an adjacency matrix `graph`. Some nodes `initial` are infected with malware. Malware spreads to connected nodes. We can remove exactly one node from `initial` to minimize the total number of infected nodes in the final state. Return the node that, if removed, minimizes the final number of infected nodes. If multiple nodes yield the same result, return the one with the smallest index.

**Examples & Edge Cases**:
- **Example 1**: `graph = [[1,1,0],[1,1,0],[0,0,1]], initial = [0,1]` → `0`.
- **Example 2**: `graph = [[1,0,0],[0,1,0],[0,0,1]], initial = [0,1,2]` → `0`.
- **Edge Case**: Multiple infected nodes in the same component → Removing one won't stop the spread in that component.

**Optimal Python Solution**:
```python
def minMalwareSpread(graph: list[list[int]], initial: list[int]) -> int:
    n = len(graph)
    parent = list(range(n))
    size = [1] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_x] = root_y
            size[root_y] += size[root_x]

    # 1. Group nodes into connected components
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                union(i, j)

    # 2. Count how many initial infected nodes are in each component
    from collections import Counter
    comp_infected_count = Counter()
    for node in initial:
        comp_infected_count[find(node)] += 1

    # 3. Find the best node to remove
    initial.sort()
    ans = initial[0]
    max_saved = -1

    for node in initial:
        root = find(node)
        # If this is the ONLY infected node in its component
        if comp_infected_count[root] == 1:
            if size[root] > max_saved:
                max_saved = size[root]
                ans = node

    return ans
```

**Explanation**:
1. We group the network into connected components using Union-Find.
2. For each component, we count how many initially infected nodes it contains.
3. If a component has more than one infected node, removing one node from `initial` will not save the component (it will still be infected by the other node).
4. If a component has exactly one infected node, removing that node saves the entire component (all `size[root]` nodes).
5. We choose the node that saves the largest component. If no node can save a component, we return the smallest index from `initial`.

**Complexity Analysis**:
- **Time Complexity**: $O(n^2 + |initial| \log |initial|)$, where $n$ is number of nodes. Union-Find takes $O(n^2 \alpha(n))$.
- **Space Complexity**: $O(n)$ for Union-Find arrays.

---

## 4. Minimize Malware Spread II
**Problem Statement**:
Similar to Minimize Malware Spread, but when we remove a node from `initial`, we remove it and all its incident edges from the graph. Return the node that minimizes the final number of infected nodes.

**Optimal Python Solution**:
```python
from collections import defaultdict, Counter

def minMalwareSpread(graph: list[list[int]], initial: list[int]) -> int:
    n = len(graph)
    initial_set = set(initial)
    clean = [i for i in range(n) if i not in initial_set]

    parent = list(range(n))
    size = [1] * n
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry
            size[ry] += size[rx]

    # Union clean nodes
    for i in range(len(clean)):
        for j in range(i + 1, len(clean)):
            if graph[clean[i]][clean[j]]:
                union(clean[i], clean[j])

    # For each infected node, find which clean components it can infect
    infected_by = defaultdict(set)
    for u in initial:
        for v in clean:
            if graph[u][v]:
                infected_by[find(v)].add(u)

    # Count components uniquely infected by exactly one malware node
    count = Counter()
    for root, malware_sources in infected_by.items():
        if len(malware_sources) == 1:
            count[list(malware_sources)[0]] += size[root]

    # Result
    res = min(initial)
    max_saved = -1
    for node in initial:
        if count[node] > max_saved:
            max_saved = count[node]
            res = node
        elif count[node] == max_saved:
            res = min(res, node)
    return res
```

**Explanation**:
1. We only consider "clean" nodes (not in `initial`) and group them into components.
2. For each infected node, we check which clean components it is adjacent to.
3. A clean component is saved if it is adjacent to **exactly one** infected node and we remove that specific node.
4. If a clean component is adjacent to two or more infected nodes, removing one won't save it.
5. We sum the sizes of saved components for each infected node and pick the maximum.

**Complexity Analysis**:
- **Time Complexity**: $O(n^2)$ to build components and check adjacency.
- **Space Complexity**: $O(n)$ to store components and mappings.

---

## 5. Making A Large Island
**Problem Statement**:
You are given an `n x n` binary matrix `grid`. You are allowed to change at most one `0` to be `1`. Return the size of the largest island in the grid after applying this operation.

**Examples & Edge Cases**:
- **Example 1**: `grid = [[1,0],[0,1]]` → `3`.
- **Example 2**: `grid = [[1,1],[1,1]]` → `4`.
- **Edge Case**: All `1`s → return `n*n`.
- **Edge Case**: All `0`s → return `1`.

**Optimal Python Solution**:
```python
def largestIsland(grid: list[list[int]]) -> int:
    n = len(grid)
    parent = list(range(n * n))
    size = [1] * (n * n)

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x != root_y:
            if size[root_x] < size[root_y]:
                root_x, root_y = root_y, root_x
            parent[root_y] = root_x
            size[root_x] += size[root_y]

    # 1. Connect existing islands
    has_zero = False
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if nr < n and nc < n and grid[nr][nc] == 1:
                        union(r * n + c, nr * n + nc)
            else:
                has_zero = True

    if not has_zero: return n * n

    # 2. Try changing each 0 to 1
    max_area = 0
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                seen_roots = set()
                current_area = 1
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                        root = find(nr * n + nc)
                        if root not in seen_roots:
                            current_area += size[root]
                            seen_roots.add(root)
                max_area = max(max_area, current_area)

    return max_area if max_area > 0 else 1
```

**Explanation**:
1. First, we use Union-Find to group all existing connected '1's into islands and calculate the size of each.
2. Then, for every '0' in the grid, we check its 4 neighbors.
3. If a neighbor belongs to an island, we note its root (using a set to avoid double-counting the same island).
4. The potential size of a new island created by flipping this '0' is $1 + \sum \text{sizes of unique neighboring islands}$.
5. We return the maximum size found.

**Complexity Analysis**:
- **Time Complexity**: $O(n^2 \alpha(n^2)) \approx O(n^2)$.
- **Space Complexity**: $O(n^2)$ for Union-Find arrays.
