# Cycle Detection in Undirected Graphs

> **Prerequisites:** [03-dfs-basics](./03-dfs-basics.md)

## Building Intuition

**The "Back Road" Mental Model**: In undirected graphs, every edge is a two-way street. When exploring, if you find a road leading back to somewhere you've been (that's not where you just came from), you've found a loop!

```
Road Network:          DFS from 0:
    0 --- 1            Visit 0 (from start)
    |     |            Visit 1 (from 0)
    2 --- 3            Visit 3 (from 1)
                       Visit 2 (from 3)
                       Edge to 0 exists! 0 is visited but NOT parent of 2
                       → CYCLE FOUND!
```

**Why we need to track "parent"**:
In undirected graphs, edge A-B means both A→B and B→A exist. Without parent tracking:

```
Graph: 0 --- 1

DFS from 0:
1. Visit 0
2. Go to neighbor 1 (edge 0-1)
3. From 1, see neighbor 0 (edge 1-0)
4. 0 is visited! CYCLE? NO! That's just the edge we came from!

With parent tracking:
- From 1, parent = 0
- See neighbor 0, but 0 = parent, so skip
- No false positive ✓
```

**The key insight**: An edge to a visited node that's NOT your parent is a "back edge" - proof of a cycle.

**Union-Find perspective**:
Before adding any edge, check if endpoints are already connected. If yes → adding this edge would create a cycle!

```
Adding edges one by one:
Edge 0-1: 0 and 1 in different sets → union them, OK
Edge 1-2: 1 and 2 in different sets → union them, OK
Edge 2-0: 2 and 0 already in SAME set → CYCLE!
```

---

## Theory: Formalizing Edge Types in Undirected DFS

When we perform a DFS on an undirected graph, every edge falls into one of two categories relative to the DFS traversal tree:

1.  **Tree Edge**: An edge that leads to an unvisited node. These edges form the DFS spanning tree (or forest, if disconnected).
2.  **Back Edge**: An edge that connects a node to an ancestor in the DFS tree. *Finding a back edge is the necessary and sufficient condition for a cycle to exist.*

*(Note: Unlike directed graphs, undirected DFS does not produce "Forward Edges" or "Cross Edges". If an edge connects two branches, it would have been traversed as a tree edge or back edge depending on which branch explored it first.)*

### Why Parent Tracking Works

Because edges in an undirected graph are bidirectional, when we traverse a tree edge from $u \to v$, the adjacency list for $v$ will contain an edge back to $u$.
This edge $(v, u)$ is trivial; it just points back to the immediate parent in the DFS tree.
A true **back edge** must point to a visited node that is *not* the immediate parent.

---

## When NOT to Use

**Parent-tracking DFS is wrong when:**

- **Graph is directed** → Use three-color DFS instead
- **Multiple edges between same nodes** → Need edge-index tracking
- **Self-loops exist** → Special case (always a cycle)

**Union-Find is better when:**

- Processing edges one at a time (streaming)
- Need to find the SPECIFIC edge causing cycle
- Building minimum spanning tree (Kruskal's)

**Common mistake scenarios:**

- Not tracking parent → False positives on every edge
- Using visited-only (like directed) → Every 2-node graph looks like a cycle
- Forgetting about multiple connected components → Must check all

**The multi-edge trap:**

```
Multiple edges between 0 and 1:
Edge list: [(0,1), (0,1)]  ← duplicate edge

Parent tracking says: "1's parent is 0, so edge back to 0 is fine"
But there are TWO edges! The second one creates a cycle!

Solution: Track edge INDEX as parent, not node ID
```

---

### Interview Context: FANG Variations

**Amazon Context**: Amazon heavily favors graph problems where the graph is *not* given explicitly as an adjacency list. You often have to build it from a 2D grid or a list of constraints. A common variation is cycle detection in a grid (e.g., "Is there a cycle of the same color?"), where you can move in 4 directions. In this grid variation, the "parent" is simply the previous $(r, c)$ coordinate you came from.

**Google Context**: Google often tests cycle detection implicitly. They might ask "Can we remove one edge to make this graph a tree?" (Redundant Connection) or "Is this sequence of connections valid without creating a loop?" which forces you to use Union-Find on a stream of edges.

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

## Comparison of Approaches & Complexity Trade-offs

| Approach     | Time        | Space | Best For                 | Pros/Cons |
| ------------ | ----------- | ----- | ------------------------ | --------- |
| DFS + Parent | O(V + E)    | O(V)  | General use              | **Pros:** Extremely short, simple to write. Native call stack. <br> **Cons:** Recursion depth = $O(V)$. Stack Overflow risk on deep lines (e.g. 100,000 nodes in a chain). |
| BFS + Parent | O(V + E)    | O(V)  | Avoid recursion          | **Pros:** Immune to Stack Overflow. Level-order processing finds shortest cycles early. <br> **Cons:** slightly more verbose (managing the queue). Memory spike if the tree is wide. |
| Union-Find   | O(E × α(V)) | O(V)  | Edge processing, dynamic | **Pros:** Best for "online" algorithms where edges are streamed. Don't need to build adjacency list. <br> **Cons:** Slower asymptotically than O(V+E) if E is huge. Hard to extract the actual cycle path. |

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

| #   | Problem                        | Difficulty | Key Variation      |
| --- | ------------------------------ | ---------- | ------------------ |
| 1   | Graph Valid Tree               | Medium     | Tree validation    |
| 2   | Redundant Connection           | Medium     | Find cycle edge    |
| 3   | Number of Connected Components | Medium     | Component counting |
| 4   | Redundant Connection II        | Hard       | Directed variation |

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
