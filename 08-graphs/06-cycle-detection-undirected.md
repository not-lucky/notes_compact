# Cycle Detection in Undirected Graphs

> **Prerequisites:** [03-dfs-basics](./03-dfs-basics.md), [05-cycle-detection-directed](./05-cycle-detection-directed.md)

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

### Why We Track the Parent

In undirected graphs, edge A-B means both A→B and B→A exist in the adjacency list. Without parent tracking, *every* edge triggers a false positive:

```
Graph: 0 --- 1

DFS from 0:
1. Visit 0
2. Go to neighbor 1 (edge 0-1)
3. From 1, see neighbor 0 (edge 1-0)
4. 0 is visited! CYCLE? NO! That's just the edge we came from!

With parent tracking:
- From 1, parent = 0
- See neighbor 0, but 0 == parent, so skip it
- No false positive ✓
```

**The key insight**: An edge to a visited node that is NOT your parent is a "back edge" — proof of a cycle.

### How This Differs from Directed Cycle Detection

| Aspect                | Undirected                        | Directed                                |
| --------------------- | --------------------------------- | --------------------------------------- |
| Edge semantics        | Bidirectional (A-B = B-A)         | One-way (A→B ≠ B→A)                     |
| False positive source | Parent edge (trivial back-link)   | Cross edges (between sibling branches)  |
| Detection technique   | Track parent to skip trivial edge | Three-color DFS (WHITE/GRAY/BLACK)      |
| Cycle indicator       | Visited neighbor ≠ parent         | Neighbor is GRAY (still on stack)       |
| Complexity            | Simpler — two states suffice      | Needs three states to avoid false alarm |

In directed graphs, seeing a visited node doesn't mean a cycle — it could be a cross edge to a fully explored branch. That's why directed detection needs the GRAY "in-progress" state.
In undirected graphs, the only non-cycle "visited neighbor" is your own parent, which is trivial to check.

### Union-Find Perspective

Process edges one at a time. Before adding each edge, check if both endpoints are already connected. If they are, this edge would create a cycle:

```
Adding edges one by one:
Edge 0-1: 0 and 1 in different sets → union them, OK
Edge 1-2: 1 and 2 in different sets → union them, OK
Edge 2-0: 2 and 0 already in SAME set → CYCLE!
```

This approach is natural when edges arrive as a stream or when you need to identify the *specific* edge that closes the cycle.

---

## Theory: Edge Types in Undirected DFS

When performing DFS on an undirected graph, every edge falls into one of two categories:

1. **Tree Edge**: Leads to an unvisited node. These edges form the DFS spanning tree (or forest, if the graph is disconnected).
2. **Back Edge**: Connects a node to an ancestor in the DFS tree. Finding a back edge is the necessary and sufficient condition for a cycle.

> Unlike directed graphs, undirected DFS does **not** produce "Forward Edges" or "Cross Edges". Any edge connecting two visited nodes in different branches would have been traversed as a tree edge when the first branch explored it.

### Why Parent Tracking Is Sufficient

Because edges are bidirectional, traversing tree edge u→v means v's adjacency list contains u. That reverse entry is trivial — it just points back to the immediate parent. A true back edge must point to a visited node that is **not** the immediate parent. So we only need two states (visited / not visited) plus the parent reference.

---

## When NOT to Use Parent-Tracking DFS

**Wrong tool for the job:**

- **Directed graphs** → Use three-color DFS instead (see [05-cycle-detection-directed](./05-cycle-detection-directed.md))
- **Multiple edges between same pair of nodes (multigraph)** → Node-based parent tracking produces false negatives; use edge-index tracking instead (see section below)
- **Self-loops** → A self-loop (edge from node to itself) is always a cycle; check for it explicitly before DFS

**When to prefer Union-Find over DFS/BFS:**

- Processing edges one at a time (streaming / online)
- Need to identify the *specific* edge that creates the cycle
- Building MST with Kruskal's algorithm
- Don't want to build an adjacency list

**Common mistakes:**

| Mistake | Result |
| ------- | ------ |
| Not tracking parent | False positive on every single edge |
| Using `visited`-only check (like directed DFS) | Every 2-node graph reports a cycle |
| Forgetting disconnected components | Miss cycles in unreachable components |
| Using node-based parent with multigraphs | Miss cycles from duplicate edges |

---

### Interview Context: FANG Variations

**Amazon**: Heavily favors graphs built from 2D grids or constraint lists, not explicit adjacency lists. Common variation: cycle detection in a grid ("Is there a cycle of the same color?"), where the "parent" is the previous (row, col) coordinate.

**Google**: Often tests cycle detection implicitly — "Can we remove one edge to make this graph a tree?" (Redundant Connection) or "Is this sequence of connections valid without creating a loop?" — which pushes you toward Union-Find on a stream of edges.

**Meta**: Graph valid tree problems and variations involving social network connectivity checks.

---

## DFS Approach: Parent Tracking

```python
from collections import defaultdict

def has_cycle_undirected(n: int, edges: list[list[int]]) -> bool:
    """
    Detect cycle in an undirected graph using DFS with parent tracking.

    Args:
        n: Number of nodes (0-indexed: 0 to n-1).
        edges: List of [u, v] undirected edges.

    Returns:
        True if a cycle exists.

    Time:  O(V + E)
    Space: O(V + E) for adjacency list, O(V) for visited set + recursion stack
    """
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited: set[int] = set()

    def dfs(node: int, parent: int) -> bool:
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                # Tree edge — continue DFS
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                # Back edge — visited and NOT parent → cycle
                return True

        return False

    # Must check every component (graph may be disconnected)
    for node in range(n):
        if node not in visited:
            if dfs(node, -1):  # -1 = no parent (root)
                return True

    return False

# --- Examples ---
# print(has_cycle_undirected(3, [[0, 1], [1, 2], [2, 0]]))  # True  (cycle: 0-1-2-0)
# print(has_cycle_undirected(3, [[0, 1], [1, 2]]))           # False (simple path)
```

---

## BFS Approach: Parent Tracking

Same idea as DFS, but uses a queue instead of recursion. Avoids stack overflow on deep/linear graphs.

```python
from collections import deque, defaultdict

def has_cycle_bfs(n: int, edges: list[list[int]]) -> bool:
    """
    Detect cycle in an undirected graph using BFS with parent tracking.

    Time:  O(V + E)
    Space: O(V + E) for adjacency list, O(V) for queue and visited
    """
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited: set[int] = set()

    for start in range(n):
        if start in visited:
            continue

        queue: deque[tuple[int, int]] = deque([(start, -1)])  # (node, parent)
        visited.add(start)

        while queue:
            node, parent = queue.popleft()

            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, node))
                elif neighbor != parent:
                    # Visited neighbor that isn't the node we came from → cycle
                    return True

    return False
```

> **When to use BFS over DFS:** When the graph could be very deep (e.g., a long chain of 100K+ nodes) and recursion depth would cause a stack overflow. BFS processes nodes level-by-level and is immune to this.

---

## Handling Multigraphs (Multiple Edges Between Same Nodes)

Standard parent-node tracking fails with duplicate edges:

```
Multiple edges between 0 and 1:
Edge list: [(0,1), (0,1)]

Parent tracking says: "1's parent is 0, skip edge back to 0"
But there are TWO edges between them — the second one creates a real cycle!

Fix: Track the edge INDEX as the parent, not the node ID.
```

```python
from collections import defaultdict

def has_cycle_multigraph(n: int, edges: list[list[int]]) -> bool:
    """
    Handle graphs with multiple edges between the same pair of nodes.

    Tracks edge index instead of parent node to distinguish
    the tree edge we arrived on from a different parallel edge.

    Time:  O(V + E)
    Space: O(V + E)
    """
    # Adjacency list stores (neighbor, edge_index) pairs
    graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for i, (u, v) in enumerate(edges):
        graph[u].append((v, i))
        graph[v].append((u, i))

    visited: set[int] = set()

    def dfs(node: int, parent_edge_idx: int) -> bool:
        visited.add(node)

        for neighbor, edge_idx in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, edge_idx):
                    return True
            elif edge_idx != parent_edge_idx:
                # Different edge to a visited node → cycle
                return True

        return False

    for node in range(n):
        if node not in visited:
            if dfs(node, -1):
                return True

    return False
```

---

## Union-Find Approach

Often preferred for undirected cycle detection — especially clean when edges arrive as a list or stream.

```python
class UnionFind:
    """Disjoint Set Union with path compression and union by rank."""

    def __init__(self, n: int):
        self.parent = list(range(n))  # Each node is its own root
        self.rank = [0] * n           # Rank for union by rank

    def find(self, x: int) -> int:
        """Find root of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Unite sets containing x and y.

        Returns False if x and y are already in the same set (cycle detected).
        """
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False  # Already connected → adding this edge creates a cycle

        # Union by rank: attach shorter tree under taller tree
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1

        return True

def has_cycle_union_find(n: int, edges: list[list[int]]) -> bool:
    """
    Detect cycle using Union-Find.

    Intuition: Process edges one at a time. Each edge should connect
    two previously disconnected components. If both endpoints are
    already in the same component, this edge creates a cycle.

    Time:  O(E * alpha(V)) ≈ O(E) — alpha is inverse Ackermann, effectively constant
    Space: O(V)
    """
    uf = UnionFind(n)

    for u, v in edges:
        if not uf.union(u, v):
            return True  # u and v already connected → cycle

    return False
```

---

## Application: Graph Valid Tree ([LeetCode 261](https://leetcode.com/problems/graph-valid-tree/))

A graph is a valid tree if and only if:

1. It is **connected** (exactly 1 component), AND
2. It is **acyclic** (no cycles)

Equivalent shortcut: **n nodes with exactly n-1 edges + connected = tree**.

```python
from collections import defaultdict

def valid_tree(n: int, edges: list[list[int]]) -> bool:
    """
    Check if an undirected graph forms a valid tree.

    Time:  O(V + E)
    Space: O(V + E)
    """
    # A tree on n nodes has exactly n-1 edges
    if len(edges) != n - 1:
        return False

    # With exactly n-1 edges, just check connectivity.
    # (n-1 edges + connected → acyclic is guaranteed)
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited: set[int] = set()

    def dfs(node: int) -> None:
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    # Note: since n-1 edges + connected = tree, we just need to verify 
    # all nodes are visited from a single DFS.
    if n > 0:
        dfs(0)
        
    return len(visited) == n

def valid_tree_union_find(n: int, edges: list[list[int]]) -> bool:
    """Union-Find alternative for graph valid tree."""
    if len(edges) != n - 1:
        return False

    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return False  # Cycle detected

    return True  # n-1 edges + no cycle → connected tree
```

---

## Application: Find the Redundant Connection ([LeetCode 684](https://leetcode.com/problems/redundant-connection/))

Given a graph that would be a tree if one edge were removed, find that edge.

```python
def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    """
    Find the edge that creates a cycle (the redundant edge).

    The input has n edges for n nodes (a tree would have n-1).
    Exactly one edge is redundant. Return the last one in the
    input that causes a cycle.

    Time:  O(E * alpha(V)) ≈ O(E)
    Space: O(V)
    """
    n = len(edges)
    uf = UnionFind(n + 1)  # +1 because nodes are 1-indexed

    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]  # This edge closes the cycle

    return []  # Should not reach here given problem constraints

# --- Example ---
# print(find_redundant_connection([[1, 2], [1, 3], [2, 3]]))  # [2, 3]
```

---

## Application: Cycles in a 2D Grid ([LeetCode 1559](https://leetcode.com/problems/detect-cycles-in-2d-grid/))

Implicit graphs like 2D grids require tracking the parent coordinate instead of a node ID. A cycle exists if you can reach the same character moving in 4 directions, path length >= 4.

```python
def containsCycle(grid: list[list[str]]) -> bool:
    """
    Detect cycle of the same characters in a 2D grid.
    
    Time:  O(M * N)
    Space: O(M * N)
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    
    def dfs(r: int, c: int, prev_r: int, prev_c: int) -> bool:
        visited.add((r, c))
        
        # 4-directional movement
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Bounds check & matching character
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == grid[r][c]:
                # If unvisited, keep going
                if (nr, nc) not in visited:
                    if dfs(nr, nc, r, c):
                        return True
                # Visited and NOT the cell we just came from -> Cycle!
                elif (nr, nc) != (prev_r, prev_c):
                    return True
                    
        return False

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                if dfs(r, c, -1, -1):
                    return True
                    
    return False
```

---

## Comparison of Approaches

| Approach     | Time         | Space | Best For                         | Trade-offs                                                                                              |
| ------------ | ------------ | ----- | -------------------------------- | ------------------------------------------------------------------------------------------------------- |
| DFS + Parent | O(V + E)     | O(V+E)| General use, adjacency list      | Simple to write. Risk of stack overflow on deep graphs (O(V) recursion depth).                          |
| BFS + Parent | O(V + E)     | O(V+E)| Large/deep graphs                | No recursion, immune to stack overflow. Slightly more verbose.                                          |
| Union-Find   | O(E * a(V))  | O(V)  | Edge streams, finding cycle edge | No adjacency list needed. Identifies the exact edge causing cycle. Harder to extract full cycle path.   |

> **Note on Union-Find complexity:** a(V) is the inverse Ackermann function, which is effectively constant (<=5 for any practical input). So O(E * a(V)) ≈ O(E) in practice.

---

## Common Mistakes

```python
# ============================================================
# WRONG: No parent tracking → false positive on every edge
# ============================================================
def has_cycle_wrong(n: int, edges: list[list[int]]) -> bool:
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited: set[int] = set()

    def dfs(node: int) -> bool:
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor in visited:
                return True  # BUG: this fires on the parent edge!
            if dfs(neighbor):
                return True
        return False

    return any(dfs(node) for node in range(n) if node not in visited)


# ============================================================
# CORRECT: Track parent to skip the trivial back-link
# ============================================================
def has_cycle_correct(n: int, edges: list[list[int]]) -> bool:
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited: set[int] = set()

    def dfs(node: int, parent: int) -> bool:
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:  # Visited + not parent = back edge → cycle
                return True
        return False

    return any(
        dfs(node, -1) for node in range(n) if node not in visited
    )
```

---

## Practice Problems

Here is a progression of problems to solidify your understanding of cycle detection in undirected graphs:

### Level 1: Basic Cycle Detection
1. **Detect Cycle in an Undirected Graph** (GeeksforGeeks)
   *Goal:* Implement standard DFS/BFS with parent tracking. This is the foundation.

2. **Graph Valid Tree** ([LeetCode 261](https://leetcode.com/problems/graph-valid-tree/))
   *Goal:* Recognize the relationship between cycles, connectivity, and the number of edges. `edges == n - 1` and single component means it's a tree.

### Level 2: Finding Specific Cycles/Edges
3. **Redundant Connection** ([LeetCode 684](https://leetcode.com/problems/redundant-connection/))
   *Goal:* Use Union-Find to find the exact edge that creates the cycle. It highlights why Union-Find is powerful for edge streams.

4. **Maximum Number of Non-Overlapping Cycles** (GeeksforGeeks/Variations)
   *Goal:* Understand how to count multiple independent cycles in disjoint components. Requires running DFS from multiple unvisited nodes.

### Level 3: Cycles in Grids (Implicit Graphs)
5. **Detect Cycles in 2D Grid** ([LeetCode 1559](https://leetcode.com/problems/detect-cycles-in-2d-grid/))
   *Goal:* Apply parent tracking in an implicit graph (2D grid). Instead of tracking `parent` as a node ID, you track `(prev_row, prev_col)`.

### Level 4: Complex Edge Conditions
6. **Number of Operations to Make Network Connected** ([LeetCode 1319](https://leetcode.com/problems/number-of-operations-to-make-network-connected/))
   *Goal:* Count components and redundant edges using Union-Find or DFS. If `total_edges < n - 1`, return -1. Otherwise, you need `components - 1` operations.

7. **Redundant Connection II** ([LeetCode 685](https://leetcode.com/problems/redundant-connection-ii/))
   *Goal:* This is actually a **directed** graph problem, but it serves as a great bridge! You must handle the case where a node has two parents OR there is a cycle.

---

## Key Takeaways

1. **Track the parent** to avoid false positives from bidirectional edges.
2. **Union-Find is elegant** for edge-by-edge processing and identifying the cycle-causing edge.
3. **Tree = connected + acyclic** = n nodes with exactly n-1 edges, all connected.
4. **Simpler than directed**: Two states (visited/not) + parent, vs. three colors for directed graphs.
5. **Edge creates cycle** when it connects two nodes already in the same connected component.

---

## Next: [07-topological-sort.md](./07-topological-sort.md)

Learn topological sorting for directed acyclic graphs.
