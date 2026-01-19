# Cycle Detection in Undirected Graphs

> **Prerequisites:** [03-dfs-basics](./03-dfs-basics.md)

## Interview Context

Cycle detection in undirected graphs is important because:

1. **Graph Valid Tree**: A tree is a connected acyclic graph
2. **Redundant Connection**: Find edge that creates cycle
3. **Union-Find practice**: Classic use case
4. **Different from directed**: Simpler algorithm

"Graph Valid Tree" is a frequently asked FANG+ problem.

---

## Core Concept: Parent Tracking

In undirected graphs, every edge can be traversed both ways. To avoid false positives:
- Track the **parent** of each node in DFS
- An edge back to a visited node (that's not the parent) = cycle

```
    0 --- 1
    |     |
    2 --- 3

DFS from 0: 0 → 1 → 3 → 2
When at 2, we see neighbor 0, but 0 is NOT parent of 2.
This is a back edge → CYCLE!

Compare without cycle:
    0 --- 1 --- 2 --- 3

DFS from 0: 0 → 1 → 2 → 3
At 2, neighbor 1 is parent (not a cycle).
At 3, no unvisited non-parent neighbors. No cycle.
```

---

## DFS Approach: Parent Tracking

```python
from collections import defaultdict

def has_cycle_undirected(n: int, edges: list[list[int]]) -> bool:
    """
    Detect cycle in undirected graph using DFS.

    Time: O(V + E)
    Space: O(V)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()

    def dfs(node: int, parent: int) -> bool:
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                # Visited neighbor that's not parent = back edge
                return True

        return False

    # Check all components
    for node in range(n):
        if node not in visited:
            if dfs(node, -1):  # -1 means no parent
                return True

    return False


# Usage
edges = [[0, 1], [1, 2], [2, 0]]  # Cycle: 0-1-2-0
print(has_cycle_undirected(3, edges))  # True

edges = [[0, 1], [1, 2]]  # No cycle
print(has_cycle_undirected(3, edges))  # False
```

---

## Handling Multiple Edges

If there can be multiple edges between same nodes:

```python
def has_cycle_with_multi_edges(n: int, edges: list[list[int]]) -> bool:
    """
    Handle graphs that may have multiple edges between same nodes.

    Use edge index instead of parent node for tracking.
    """
    graph = defaultdict(list)  # node -> [(neighbor, edge_index)]
    for i, (u, v) in enumerate(edges):
        graph[u].append((v, i))
        graph[v].append((u, i))

    visited = set()

    def dfs(node: int, parent_edge: int) -> bool:
        visited.add(node)

        for neighbor, edge_idx in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, edge_idx):
                    return True
            elif edge_idx != parent_edge:
                return True

        return False

    for node in range(n):
        if node not in visited:
            if dfs(node, -1):
                return True

    return False
```

---

## BFS Approach

```python
from collections import deque, defaultdict

def has_cycle_bfs(n: int, edges: list[list[int]]) -> bool:
    """
    Detect cycle in undirected graph using BFS.

    Time: O(V + E)
    Space: O(V)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()

    for start in range(n):
        if start in visited:
            continue

        queue = deque([(start, -1)])  # (node, parent)
        visited.add(start)

        while queue:
            node, parent = queue.popleft()

            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, node))
                elif neighbor != parent:
                    return True

    return False
```

---

## Union-Find Approach

Classic and often preferred for undirected cycle detection:

```python
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Returns False if x and y are already connected (cycle!)."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Already connected = adding this edge creates cycle

        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

        return True


def has_cycle_union_find(n: int, edges: list[list[int]]) -> bool:
    """
    Detect cycle using Union-Find.

    Time: O(E × α(V)) ≈ O(E)
    Space: O(V)
    """
    uf = UnionFind(n)

    for u, v in edges:
        if not uf.union(u, v):
            return True  # Edge connects already-connected nodes

    return False
```

**Why Union-Find works**: Each edge should connect two previously disconnected components. If an edge connects nodes already in the same component, it creates a cycle.

---

## Graph Valid Tree

A graph is a valid tree if:
1. Connected (exactly 1 component)
2. Acyclic (no cycles)
3. Equivalently: n nodes and exactly n-1 edges, connected

```python
def valid_tree(n: int, edges: list[list[int]]) -> bool:
    """
    Check if graph forms a valid tree.

    Time: O(V + E)
    Space: O(V)
    """
    # Quick check: tree has exactly n-1 edges
    if len(edges) != n - 1:
        return False

    # Check connectivity (if n-1 edges and connected, no cycle)
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()

    def dfs(node: int):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    dfs(0)

    return len(visited) == n


# Alternative: Union-Find
def valid_tree_uf(n: int, edges: list[list[int]]) -> bool:
    if len(edges) != n - 1:
        return False

    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return False

    return True  # n-1 edges, no cycle → connected tree
```

---

## Find the Redundant Edge

```python
def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    """
    Find edge that creates a cycle (redundant edge).

    Given n edges for n nodes (tree would have n-1),
    exactly one edge is redundant.

    Time: O(E × α(V))
    Space: O(V)
    """
    n = len(edges)
    uf = UnionFind(n + 1)  # 1-indexed nodes

    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]

    return []


# Usage
edges = [[1, 2], [1, 3], [2, 3]]
print(find_redundant_connection(edges))  # [2, 3]
```

---

## Comparison of Approaches

| Approach | Time | Space | Best For |
|----------|------|-------|----------|
| DFS + Parent | O(V + E) | O(V) | General use |
| BFS + Parent | O(V + E) | O(V) | Avoid recursion |
| Union-Find | O(E × α(V)) | O(V) | Edge processing, dynamic |

---

## Common Mistakes

```python
# WRONG: Not tracking parent
def has_cycle_wrong(n, edges):
    visited = set()

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor in visited:
                return True  # WRONG! Could be parent
            if dfs(neighbor):
                return True
        return False

# CORRECT: Track parent
def has_cycle_correct(n, edges):
    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:  # Not parent = back edge
                return True
        return False
```

---

## Edge Cases

```python
# 1. No edges (forest of single nodes)
n = 5, edges = []  # No cycle

# 2. Single edge
n = 2, edges = [[0, 1]]  # No cycle

# 3. Self-loop (edge to itself)
n = 1, edges = [[0, 0]]  # Cycle (needs special handling)

# 4. Multiple edges between same nodes
edges = [[0, 1], [0, 1]]  # Cycle (needs special handling)

# 5. Disconnected with cycle in one component
edges = [[0, 1], [1, 2], [2, 0], [3, 4]]  # Cycle in first component
```

---

## Interview Tips

1. **Know parent tracking**: Key insight for DFS approach
2. **Know Union-Find**: Often cleaner for edge-by-edge processing
3. **Graph Valid Tree**: n-1 edges + connected = tree
4. **Clarify multi-edges**: May need edge index tracking
5. **Handle self-loops**: Special case, always a cycle

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Graph Valid Tree | Medium | Tree validation |
| 2 | Redundant Connection | Medium | Find cycle edge |
| 3 | Number of Connected Components | Medium | Component counting |
| 4 | Redundant Connection II | Hard | Directed variation |

---

## Key Takeaways

1. **Track parent**: Essential to avoid false positives
2. **Union-Find alternative**: Elegant for undirected graphs
3. **Tree = connected + acyclic**: Or n nodes with n-1 edges, connected
4. **Simpler than directed**: No need for three colors
5. **Edge creates cycle**: When it connects already-connected nodes

---

## Next: [07-topological-sort.md](./07-topological-sort.md)

Learn topological sorting for directed acyclic graphs.
