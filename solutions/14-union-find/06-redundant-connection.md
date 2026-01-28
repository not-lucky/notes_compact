# Redundant Connection Solutions

## 1. Redundant Connection
**Problem Statement**:
In this problem, a rooted tree is an undirected graph such that there is exactly one path between any two nodes. You are given a graph that started as a tree with `n` nodes, and then one additional edge was added. Find the edge that can be removed so that the resulting graph is a tree of `n` nodes. If there are multiple answers, return the one that occurs last in the input.

**Examples & Edge Cases**:
- **Example 1**: `edges = [[1,2], [1,3], [2,3]]` → `[2,3]`.
- **Example 2**: `edges = [[1,2], [2,3], [3,4], [1,4], [1,5]]` → `[1,4]`.
- **Edge Case**: The redundant edge connects the root to a leaf or two leaves.

**Optimal Python Solution**:
```python
def findRedundantConnection(edges: list[list[int]]) -> list[int]:
    n = len(edges)
    parent = list(range(n + 1))
    rank = [0] * (n + 1)

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x]) # Path compression
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
            return [u, v]

    return []
```

**Explanation**:
1. A tree with $n$ nodes has exactly $n-1$ edges and no cycles.
2. We are given $n$ edges, which means there is exactly one cycle.
3. We use Union-Find to process edges one by one.
4. For each edge $(u, v)$, we check if $u$ and $v$ are already connected.
5. If they are, then $(u, v)$ is the redundant edge that creates the cycle. Since we return the first one that triggers this (and there is only one extra edge), we fulfill the "last in input" requirement.

**Complexity Analysis**:
- **Time Complexity**: $O(n \alpha(n))$, where $n$ is the number of nodes.
- **Space Complexity**: $O(n)$ for the parent and rank arrays.

---

## 2. Redundant Connection II
**Problem Statement**:
This is similar to Redundant Connection I, but the graph is directed. The graph started as a directed tree (every node has exactly one parent except the root) and then one directed edge was added.

**Optimal Python Solution**:
```python
def findRedundantDirectedConnection(edges: list[list[int]]) -> list[int]:
    n = len(edges)
    parent_in = [0] * (n + 1)
    cand1 = cand2 = None

    # 1. Check for a node with two parents
    for u, v in edges:
        if parent_in[v] == 0:
            parent_in[v] = u
        else:
            cand1 = [parent_in[v], v]
            cand2 = [u, v]
            break

    # 2. Check for cycles using Union-Find
    def find(parent, rank, i):
        if parent[i] == i:
            return i
        parent[i] = find(parent, rank, parent[i])
        return parent[i]

    def is_cycle(edge_to_skip):
        p = list(range(n + 1))
        r = [0] * (n + 1)
        for u, v in edges:
            if [u, v] == edge_to_skip: continue
            root_u = find(p, r, u)
            root_v = find(p, r, v)
            if root_u == root_v: return True
            if r[root_u] < r[root_v]:
                p[root_u] = root_v
            elif r[root_u] > r[root_v]:
                p[root_v] = root_u
            else:
                p[root_u] = root_v
                r[root_v] += 1
        return False

    if not cand2:
        # No node with two parents, there must be a cycle
        p = list(range(n + 1))
        r = [0] * (n + 1)
        for u, v in edges:
            root_u = find(p, r, u)
            root_v = find(p, r, v)
            if root_u == root_v: return [u, v]
            if r[root_u] < r[root_v]:
                p[root_u] = root_v
            elif r[root_u] > r[root_v]:
                p[root_v] = root_u
            else:
                p[root_u] = root_v
                r[root_v] += 1
    else:
        # If removing cand2 solves the cycle, cand2 is redundant
        if not is_cycle(cand2): return cand2
        # Otherwise, cand1 must be the redundant one
        return cand1
```

**Explanation**:
1. There are two potential issues in a directed "tree + 1 edge":
   - A node has two parents (in-degree 2).
   - There is a directed cycle.
2. Case A: Only a cycle (root points back). Removing the cycle-forming edge works.
3. Case B: Only a node with two parents. Removing the second incoming edge (last in input) works.
4. Case C: Both. One of the two incoming edges to the node with in-degree 2 is part of the cycle. We must remove that one.

**Complexity Analysis**:
- **Time Complexity**: $O(n \alpha(n))$.
- **Space Complexity**: $O(n)$.

---

## 3. Graph Valid Tree
**Problem Statement**:
Check if an undirected graph with `n` nodes and `edges` forms a valid tree.

**Optimal Python Solution**:
```python
def validTree(n: int, edges: list[list[int]]) -> bool:
    if len(edges) != n - 1:
        return False

    parent = list(range(n))
    rank = [0] * n
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry: return False # Cycle
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:
            parent[rx] = ry
            rank[ry] += 1
        return True

    for u, v in edges:
        if not union(u, v): return False # Cycle
    return True
```

**Explanation**:
1. A tree must have $n-1$ edges and no cycles.
2. We first check the edge count.
3. Then we use Union-Find to ensure no cycles exist while processing the edges.

**Complexity Analysis**:
- **Time Complexity**: $O(n \alpha(n))$.
- **Space Complexity**: $O(n)$.

---

## 4. Detect Cycles in 2D Grid
**Problem Statement**:
Given an `m x n` grid of characters, find if there is a cycle of length 4 or more consisting of the same character.

**Optimal Python Solution**:
```python
def containsCycle(grid: list[list[str]]) -> bool:
    rows, cols = len(grid), len(grid[0])
    parent = list(range(rows * cols))
    rank = [0] * (rows * cols)

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root1 = find(x)
        root2 = find(y)
        if root1 == root2:
            return False
        if rank[root1] < rank[root2]:
            parent[root1] = root2
        elif rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
            rank[root2] += 1
        return True

    for r in range(rows):
        for c in range(cols):
            # Check right and down
            for dr, dc in [(0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if nr < rows and nc < cols and grid[r][c] == grid[nr][nc]:
                    if not union(r * cols + c, nr * cols + nc):
                        return True
    return False
```

**Explanation**:
1. We use Union-Find on grid cells.
2. Two adjacent cells with the same character are "connected".
3. If we try to connect two cells that are already in the same component, we've found a cycle.

**Complexity Analysis**:
- **Time Complexity**: $O(mn \alpha(mn))$.
- **Space Complexity**: $O(mn)$.

---

## 5. Min Cost to Connect All Points
**Problem Statement**:
You are given an array `points` representing coordinates. The cost of connecting two points is the Manhattan distance. Return the minimum cost to make all points connected.

**Optimal Python Solution**:
```python
def minCostConnectPoints(points: list[list[int]]) -> int:
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            edges.append((dist, i, j))

    # Kruskal's Algorithm
    edges.sort()
    parent = list(range(n))
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    cost = 0
    num_edges = 0
    for d, u, v in edges:
        root_u, root_v = find(u), find(v)
        if root_u != root_v:
            parent[root_u] = root_v
            cost += d
            num_edges += 1
            if num_edges == n - 1: break
    return cost
```

**Explanation**:
1. This is a Minimum Spanning Tree (MST) problem.
2. We generate all possible edges between points and sort them by distance.
3. We use Kruskal's algorithm (Union-Find) to pick the smallest edges that don't form cycles until everyone is connected.

**Complexity Analysis**:
- **Time Complexity**: $O(n^2 \log n)$ due to sorting $n^2$ edges.
- **Space Complexity**: $O(n^2)$ to store all edges.

---

## 6. Critical Connections in a Network
**Problem Statement**:
Find all bridges in an undirected graph. A bridge is an edge whose removal increases the number of connected components.

**Optimal Python Solution**:
```python
def criticalConnections(n: int, connections: list[list[int]]) -> list[list[int]]:
    # Note: While Union-Find can detect cycles, Tarjan's Bridge-Finding
    # algorithm (DFS-based) is the standard optimal approach for bridges.
    adj = [[] for _ in range(n)]
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)

    discovery_time = [-1] * n
    low_link = [-1] * n
    res = []
    timer = 0

    def dfs(node, parent):
        nonlocal timer
        discovery_time[node] = low_link[node] = timer
        timer += 1

        for neighbor in adj[node]:
            if neighbor == parent: continue
            if discovery_time[neighbor] == -1:
                dfs(neighbor, node)
                low_link[node] = min(low_link[node], low_link[neighbor])
                if low_link[neighbor] > discovery_time[node]:
                    res.append([node, neighbor])
            else:
                low_link[node] = min(low_link[node], discovery_time[neighbor])

    dfs(0, -1)
    return res
```

**Explanation**:
1. A "critical connection" is a bridge.
2. We use Tarjan's algorithm (or similar DFS approach). We track the `discovery_time` and the `low_link` (the earliest discovered node reachable through a back-edge in the DFS tree).
3. If a neighbor `v` of `u` cannot reach `u` or any ancestor of `u` through any other path (`low_link[v] > discovery_time[u]`), then `(u, v)` is a bridge.

**Complexity Analysis**:
- **Time Complexity**: $O(V + E)$.
- **Space Complexity**: $O(V + E)$ for adjacency list.
