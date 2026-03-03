# Redundant Connection (Cycle Detection)

> **Prerequisites:** [Union-Find Basics](./01-union-find-basics.md), [Path Compression](./02-path-compression.md)

## Interview Context

"Redundant Connection" (LeetCode 684, 685) is a classic Union-Find application for cycle detection. The key insight: in an undirected graph, an edge creates a cycle if and only if it connects two already-connected nodes. The directed variant (685) layers additional complexity with parent-tracking.

---

## Building Intuition

**The "One Wire Too Many" Mental Model**

Imagine you're wiring a network of computers. A tree network needs exactly n-1 cables to connect n computers with no loops. Someone added one extra cable, creating a loop—find which one!

```
Correct tree (5 nodes, 4 cables):
    1 --- 2
    |
    3 --- 4
    |
    5

With redundant cable (5 nodes, 5 cables):
    1 --- 2
    |     |    ← This creates a loop: 1-2-4-3-1
    3 --- 4
    |
    5
```

**The Key Insight: Union Reveals Cycles**

When processing edges one by one:

- `union(a, b)` succeeds → a and b were in different components → no cycle
- `union(a, b)` fails → a and b were already connected → THIS EDGE CREATES A CYCLE!

```
Processing edges: [1-2], [1-3], [2-3]

[1-2]: union(1,2) → Success! Components: {1,2}, {3}
[1-3]: union(1,3) → Success! Components: {1,2,3}
[2-3]: union(2,3) → FAIL! 2 and 3 already connected!
       → Edge [2-3] is redundant
```

**Why This Works**

In a tree:

- Every edge connects two previously disconnected subtrees
- Adding an edge between already-connected nodes creates a cycle

Union-Find tracks connectivity. If `find(a) == find(b)` before adding edge (a,b), that edge would create a cycle.

```
Visual proof:

Before edge (2,3):          After edge (2,3):
    1                           1
   / \                         / \
  2   3                       2---3  ← Cycle!

find(2) = 1, find(3) = 1 → Already connected!
```

---

## When NOT to Use Union-Find for Cycle Detection

**1. For General Directed Graphs**

Union-Find treats all edges as undirected. For general directed cycle detection:

```python
# Directed graph: A → B → C → A is a cycle
# But A → B, C → B, C → A might not form a directed cycle!

# Use instead:
# - DFS with coloring (white/gray/black)
# - Topological sort (cycle = failed sort)
#
# Exception: Redundant Connection II (LeetCode 685) uses Union-Find on a
# directed tree with one extra edge — a special structure, not a general
# directed graph. It works because the underlying tree is undirected in nature.
```

**2. When You Need to Find ALL Cycles**

Union-Find only detects that a cycle exists. To enumerate all cycles:

```python
# Union-Find: "There's a cycle" (boolean)
# For all cycles: Use DFS backtracking or Johnson's algorithm
```

**3. When You Need the Cycle Path**

Union-Find can identify the redundant edge but not the complete cycle path:

```python
# Union-Find: "Edge (2,3) creates a cycle"
# Doesn't tell you: "The cycle is 1 → 2 → 3 → 1"

# For the actual cycle path, use DFS with parent tracking
```

**4. For Weighted "Negative Cycle" Detection**

To detect negative cycles (Bellman-Ford territory), Union-Find doesn't help—you need to track distances:

```python
# Negative cycle in weighted graph: sum of edge weights < 0
# Completely different problem from Union-Find's connectivity check
```

**5. When Graph is Given as Adjacency List**

If you already have an adjacency list, DFS might be simpler:

```python
# Adjacency list + DFS: Natural cycle detection with visited set
# Union-Find: Need to extract edges first, then process

# Union-Find shines when input IS an edge list
```

---

## Warm-Up: Does the Graph Contain a Cycle?

Before tackling "which edge is redundant," start with the simpler question: **does an undirected graph contain any cycle at all?**

Given `n` nodes (0-indexed) and a list of undirected edges, return `True` if the graph contains a cycle.

```
Example 1:                  Example 2:
  0 --- 1                     0 --- 1
  |   /                       |
  | /                         |
  2                           2 --- 3

  Edges: [[0,1],[1,2],[0,2]]  Edges: [[0,1],[0,2],[2,3]]
  Output: True (cycle 0-1-2)  Output: False (it's a tree)
```

### Solution

```python
def has_cycle(n: int, edges: list[list[int]]) -> bool:
    """
    Detect if an undirected graph contains a cycle using Union-Find.

    For each edge, if both endpoints are already in the same component,
    adding this edge would create a cycle.

    Time: O(E × α(n)) ≈ O(E)
    Space: O(n)
    """
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> bool:
        """Returns False if x and y are already connected (cycle detected)."""
        px, py = find(x), find(y)
        if px == py:
            return False  # Same component → cycle!
        # Union by rank
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    for u, v in edges:
        if not union(u, v):
            return True  # Cycle found

    return False


# Trace: edges = [[0,1], [1,2], [0,2]]
# [0,1]: union(0,1) → True.  Components: {0,1}, {2}
# [1,2]: union(1,2) → True.  Components: {0,1,2}
# [0,2]: find(0)=0, find(2)=0, same root → False → cycle detected!
# Return True
```

> **Why this is simpler than Redundant Connection:** Here we just need a boolean (is there a cycle?). Redundant Connection asks us to identify *which specific edge* creates the cycle.

---

## Problem: Redundant Connection I

**LeetCode 684**: Given a graph that was a tree with one additional edge, find the edge that can be removed to restore the tree. If there are multiple answers, return the one that appears last.

### Example

```
Input: edges = [[1,2], [1,3], [2,3]]
Output: [2,3]

Visual:
    1 --- 2
    |   /
    | /
    3

The edge [2,3] creates the cycle 1-2-3-1.
Removing it gives a tree.
```

### Key Insight

Process edges in order. Since the graph has exactly n nodes and n edges (one extra), exactly one edge creates a cycle. That's the redundant edge.

Because there's exactly one cycle, only one edge triggers `find(u) == find(v)`. The "return the last such edge" constraint from the problem is automatically satisfied — it's the only one.

### Solution

```python
def findRedundantConnection(edges: list[list[int]]) -> list[int]:
    """
    Find the edge that creates a cycle.

    Time: O(n × α(n)) ≈ O(n)
    Space: O(n)
    """
    n = len(edges)
    parent = list(range(n + 1))  # 1-indexed nodes
    rank = [0] * (n + 1)

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        """Returns False if x and y are already connected (cycle!)."""
        px, py = find(x), find(y)

        if px == py:
            return False  # Already connected → cycle

        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

        return True

    for a, b in edges:
        if not union(a, b):
            return [a, b]  # This edge creates a cycle

    return []  # Should not reach here


# Trace
edges = [[1,2], [1,3], [2,3]]

# Process [1,2]: union(1,2) → True, parent[2] = 1
# Process [1,3]: union(1,3) → True, parent[3] = 1
# Process [2,3]: find(2)=1, find(3)=1, same root → False → return [2,3]
```

---

## Problem: Redundant Connection II

**LeetCode 685**: A rooted directed tree (each node has at most one parent, root has none) had one extra directed edge added. Find the edge that can be removed to restore a valid rooted tree. If multiple answers exist, return the one that appears last in the input.

### Key Differences

In a directed tree (rooted):

- Every node except root has exactly one parent
- One extra edge means one of three scenarios:
  1. A node has two parents (in-degree 2), but no cycle
  2. There's a cycle, but no node with two parents
  3. Both: a node has two parents AND is part of a cycle

### The Three Cases (Critical to Understand)

```
Case 1: Node with two parents, no cycle
    Edges: [[1,2], [1,3], [2,3]]

        1 → 2
        ↓   ↓
        3 ← ┘

    Node 3 has two parents: 1→3 and 2→3 (in-degree 2).
    No directed cycle exists.
    Remove the later incoming edge to the node with in-degree 2.
    Answer: [2,3]

Case 2: Cycle exists, no node with two parents
    Edges: [[1,2], [2,3], [3,1]]

        1 → 2
        ↑   ↓
        └── 3

    Every node has in-degree 1 — no dual-parent node.
    Directed cycle: 1 → 2 → 3 → 1.
    Remove the edge that creates the cycle (treat as undirected).
    Answer: [3,1]

Case 3: Node with two parents AND that node is IN the cycle
    Edges: [[1,2], [2,3], [3,1], [4,1]]

        4
        ↓
        1 → 2
        ↑   ↓
        └── 3

    Node 1 has two parents: 3→1 and 4→1
    Cycle: 1 → 2 → 3 → 1
    Must remove the in-cycle edge pointing to the dual-parent node (3→1),
    not the other parent edge (4→1).
    Answer: [3,1]
```

**Why Case 3 is tricky:** When a node has two parent edges, we don't know *which one*
to remove. If neither creates a cycle, the answer is the later edge (Case 1).
But if one of them participates in a cycle, we must remove *that one* (Case 3).
The algorithm tests this by temporarily ignoring the second parent edge: if a
cycle still exists, the first parent edge must be the culprit.

### Solution

```python
def findRedundantDirectedConnection(edges: list[list[int]]) -> list[int]:
    """
    Find redundant directed edge in a rooted tree with one extra edge.

    Three cases: (1) node with two parents, no cycle → remove later parent edge,
    (2) cycle, no dual-parent node → remove cycle-forming edge,
    (3) node with two parents AND in a cycle → remove in-cycle parent edge.

    Algorithm:
      1. Scan edges to find if any node has two parents (in-degree 2).
         If found, record both edges as candidate1 (first) and candidate2 (second).
      2. Re-run Union-Find on all edges, skipping candidate2 (if it exists).
         - If a cycle is detected AND candidate1 exists → Case 3: return candidate1.
         - If a cycle is detected AND no candidates → Case 2: return the cycle edge.
      3. If no cycle detected → Case 1: candidate2 was the problem, return it.

    Time: O(n log n) with path compression only; O(n × α(n)) with rank
    Space: O(n)
    """
    n = len(edges)
    parent = list(range(n + 1))

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    # Union by rank omitted for clarity in this already-complex 3-case problem.
    # Path compression alone gives O(n log n) amortized — fast enough for n ≤ 1000.
    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False
        parent[py] = px
        return True

    # Step 1: Find if any node has two parents
    incoming = [0] * (n + 1)  # incoming[v] = source node of the first edge pointing to v
    candidate1 = candidate2 = None

    for u, v in edges:
        if incoming[v] != 0:
            # v already has a parent → found node with 2 parents
            candidate1 = [incoming[v], v]  # First edge to v
            candidate2 = [u, v]             # Second edge to v
            break
        incoming[v] = u

    # Step 2: Build Union-Find ignoring candidate2 (if exists)
    parent = list(range(n + 1))

    for u, v in edges:
        # Python compares lists by value, so [u, v] == candidate2
        # checks element equality, not identity
        if candidate2 and [u, v] == candidate2:
            continue  # Skip candidate2

        if not union(u, v):
            # Found cycle
            if candidate1:
                # Case 3: node with 2 parents AND a cycle
                # → candidate1 is the in-cycle parent edge
                return candidate1
            else:
                # Case 2: no node with 2 parents, just a cycle
                return [u, v]

    # No cycle when candidate2 removed → candidate2 was the problem
    # Case 1: node with 2 parents, no cycle
    return candidate2


# Example traces

# Case 1: [[1,2],[1,3],[2,3]] directed
# Node 3 has two parents: 1→3 and 2→3
# candidate1 = [1,3], candidate2 = [2,3]
# Union without [2,3]: (1,2) OK, (1,3) OK → no cycle
# Return candidate2 = [2,3] ✓

# Case 2: [[1,2],[2,3],[3,1]]
# No node with 2 parents (candidate1=candidate2=None)
# Union: (1,2) OK, (2,3) OK, (3,1) find(3)=1, find(1)=1 → cycle!
# Return [3,1] ✓

# Case 3: [[1,2],[2,3],[3,1],[4,1]]  (trickiest!)
# Scan: incoming[2]=1, incoming[3]=2, incoming[1]=3, then [4,1]: incoming[1]≠0
#   → candidate1=[3,1], candidate2=[4,1]
# Union without [4,1]:
#   (1,2): parent[2]=1 → OK
#   (2,3): find(2)=1, find(3)=3, parent[3]=1 → OK
#   (3,1): find(3)=1, find(1)=1 → same root → cycle!
#   → candidate1 exists → return candidate1=[3,1] ✓
# The in-cycle edge [3,1] is correctly identified, not [4,1].
```

---

## Why Union-Find Works for Cycle Detection

```
In an undirected graph:
- Adding edge (u, v) creates a cycle ⟺ u and v are already connected
- Union-Find can check this in O(α(n))

Before adding edge (u, v):
  find(u) == find(v)  →  u and v connected  →  cycle!
  find(u) != find(v)  →  u and v disconnected  →  no cycle, safe to add

This is exactly what union() returns:
  - True: merged two components (no cycle)
  - False: already same component (would create cycle)
```

---

## Problem: Graph Valid Tree Revisited

A graph is a valid tree if:

1. Connected (one component)
2. No cycles
3. n nodes, n-1 edges

Any two of these three conditions imply the third.

```python
def validTree(n: int, edges: list[list[int]]) -> bool:
    """
    Check if edges form a valid tree.

    The n-1 edge check is sufficient for connectedness: if n-1 edges
    produce no cycle, the graph must be a single connected tree.

    Time: O(n × α(n)) ≈ O(n)
    Space: O(n)
    """
    if len(edges) != n - 1:
        return False  # Tree must have exactly n-1 edges

    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return False  # Cycle detected
        # Union by rank
        if rank[pu] < rank[pv]:
            pu, pv = pv, pu
        parent[pv] = pu
        if rank[pu] == rank[pv]:
            rank[pu] += 1

    return True
```

---

## Problem: Number of Operations to Make Network Connected

**LeetCode 1319**: There are `n` computers numbered `0` to `n-1` connected by ethernet cables (edges). You can disconnect one cable from a connected pair and connect two previously disconnected computers. Return the minimum number of operations needed to connect all computers, or `-1` if not possible.

This problem bridges basic cycle detection and MST thinking: redundant edges (those that would create cycles) are the "spare cables" available for reconnecting disconnected components.

### Key Insight

- You need `n - 1` cables to connect `n` computers (a spanning tree).
- If you have fewer than `n - 1` cables total, it's impossible → return `-1`.
- Otherwise, count the number of connected components `c`. You need `c - 1` operations to link them together. Any redundant cable (one that creates a cycle) can be repurposed.

```python
def makeConnected(n: int, connections: list[list[int]]) -> int:
    """
    Minimum operations to connect all computers.

    Count connected components using Union-Find. Each union that succeeds
    reduces the component count by 1. The remaining components minus 1
    is the number of reconnections needed.

    Time: O(E × α(n)) ≈ O(E)
    Space: O(n)
    """
    if len(connections) < n - 1:
        return -1  # Not enough cables

    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    components = n
    for u, v in connections:
        if union(u, v):
            components -= 1

    return components - 1  # Need this many operations to link remaining components


# Trace: n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]
# 5 cables, need 5 minimum → possible
# union(0,1): OK → components = 5
# union(0,2): OK → components = 4
# union(0,3): OK → components = 3
# union(1,2): 1 and 2 already connected (redundant cable)
# union(1,3): 1 and 3 already connected (redundant cable)
# components = 3, so we need 3 - 1 = 2 operations
# (Repurpose 2 redundant cables to connect nodes 4 and 5)
```

---

## Problem: Detect Cycle in 2D Grid

Given a 2D grid of characters, check if there's a cycle of the same character with length ≥ 4.

**LeetCode 1559**

```python
def containsCycle(grid: list[list[str]]) -> bool:
    """
    Detect cycle using Union-Find on grid.

    Key insight: Connect same-character neighbors.
    If we try to connect already-connected cells → cycle.

    Only checks right and down neighbors — each edge is processed
    exactly once, avoiding duplicate checks from bidirectional traversal.

    The length ≥ 4 constraint is automatically satisfied: the minimum
    cycle in a 4-directional grid is a 2×2 square (length 4).

    Time: O(m × n × α(m × n))
    Space: O(m × n)
    """
    m, n = len(grid), len(grid[0])
    parent = list(range(m * n))
    rank = [0] * (m * n)

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def idx(r: int, c: int) -> int:
        return r * n + c

    for r in range(m):
        for c in range(n):
            char = grid[r][c]

            # Only check right and down to avoid duplicate checks
            for dr, dc in [(0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if nr < m and nc < n and grid[nr][nc] == char:
                    pi = find(idx(r, c))
                    pj = find(idx(nr, nc))

                    if pi == pj:
                        return True  # Cycle!

                    # Union by rank
                    if rank[pi] < rank[pj]:
                        pi, pj = pj, pi
                    parent[pj] = pi
                    if rank[pi] == rank[pj]:
                        rank[pi] += 1

    return False
```

---

## Pattern: Process Edges to Find Cycle

```python
def find_cycle_edge(n: int, edges: list[list[int]]) -> list[int] | None:
    """
    Generic pattern: return first edge that creates a cycle, or None.

    Note: list[int] | None syntax requires Python 3.10+.
    For earlier versions, use Optional[list[int]] from typing.
    """
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return [u, v]  # This edge creates a cycle
        # Union by rank
        if rank[pu] < rank[pv]:
            pu, pv = pv, pu
        parent[pv] = pu
        if rank[pu] == rank[pv]:
            rank[pu] += 1

    return None  # No cycle
```

---

## Minimum Spanning Tree (Kruskal's Algorithm)

Union-Find is essential for Kruskal's MST algorithm:

> **Edge format: (weight, u, v)** — Weight is first so that `edges.sort()` sorts
> by weight naturally (Python sorts tuples lexicographically). This avoids needing
> a custom key function. If your input uses `(u, v, weight)`, convert first:
> `edges = [(w, u, v) for u, v, w in original_edges]`.

```python
def kruskal_mst(n: int, edges: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """
    Find MST using Kruskal's algorithm.

    Args:
        n: Number of nodes (0-indexed: 0 to n-1).
        edges: List of (weight, u, v) tuples. Weight-first format enables
               direct sorting by weight via edges.sort() — no key function needed.

    Returns:
        List of (weight, u, v) tuples forming the MST.

    Time: O(E log E + E × α(V)) = O(E log E)
    Space: O(V)
    """
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False  # Would create cycle
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    edges.sort()  # Sort by weight (first tuple element). Mutates input list.
    # Use sorted(edges) instead if you need to preserve the original order.

    mst = []
    for weight, u, v in edges:
        if union(u, v):  # Add edge if no cycle
            mst.append((weight, u, v))
            if len(mst) == n - 1:
                break  # MST complete

    return mst


# Example usage:
# edges = [(1, 0, 1), (2, 0, 2), (3, 1, 2)]  # (weight, u, v)
# mst = kruskal_mst(3, edges)
# → [(1, 0, 1), (2, 0, 2)]  — total weight 3, connects all 3 nodes
```

---

## Problem: Min Cost to Connect All Points

**LeetCode 1584**: Given `n` points on a 2D plane, connect all points with minimum total Manhattan distance. Return the minimum cost to make all points connected.

This is a direct application of Kruskal's MST — the points are nodes, and the edge weight between any two points is their Manhattan distance.

### Example

```
Input: points = [[0,0], [2,2], [3,10], [5,2], [7,0]]

Distances between all pairs:
  (0,0)-(2,2) = |0-2|+|0-2| = 4
  (0,0)-(5,2) = |0-5|+|0-2| = 7
  (2,2)-(5,2) = |2-5|+|2-2| = 3
  ... (10 total edges for 5 points)

Output: 20 (MST total weight)
```

### Solution

```python
def minCostConnectPoints(points: list[list[int]]) -> int:
    """
    Minimum cost to connect all points using Kruskal's MST.

    Build all pairwise edges with Manhattan distance, then run Kruskal's.

    Time: O(n² log n) — n² edges, sorting dominates
    Space: O(n²) for edge list
    """
    n = len(points)
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    # Build all edges: (manhattan_distance, i, j)
    edges: list[tuple[int, int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            edges.append((dist, i, j))

    edges.sort()  # Sort by distance (weight-first format)

    total_cost = 0
    edges_used = 0
    for cost, u, v in edges:
        if union(u, v):
            total_cost += cost
            edges_used += 1
            if edges_used == n - 1:
                break  # MST complete

    return total_cost


# Trace: points = [[0,0], [2,2], [3,10], [5,2], [7,0]]
# All 10 edges sorted by distance:
#   (3, 1, 3)   ← (2,2)-(5,2)
#   (4, 0, 1)   ← (0,0)-(2,2)
#   (4, 3, 4)   ← (5,2)-(7,0)
#   (7, 0, 3)   ← (0,0)-(5,2)
#   (7, 0, 4)   ← (0,0)-(7,0)
#   ...
# Kruskal picks: (3,1,3) + (4,0,1) + (4,3,4) + (9,1,2) = 20
```

> **Why Kruskal's over Prim's here?** Both work. Kruskal's is simpler to implement
> with Union-Find and natural when edges are explicit. For this dense graph (n²
> edges), Kruskal's is O(n² log n) due to sorting. Prim's with an adjacency matrix
> would be O(n²) — asymptotically faster but more complex to implement.

---

## Complexity Analysis

| Operation         | Time             |
| ----------------- | ---------------- |
| Process one edge  | O(α(n))          |
| Process all edges | O(E × α(n))      |
| Cycle detection   | O(α(n)) per edge |
| Kruskal's MST     | O(E log E)       |

For Redundant Connection: the graph has n nodes and exactly n edges (one extra
beyond tree's n-1). Total: O(n × α(n)) ≈ O(n).

---

## Edge Cases

1. **Self-loop [u, u]**: find(u) == find(u), always cycle
2. **Duplicate edges**: Second occurrence creates "cycle"
3. **1-indexed vs 0-indexed**: Match parent array size
4. **Empty graph**: No edges → no cycles
5. **Directed vs undirected**: Different cycle definitions

---

## Interview Tips

1. **Clarify graph type**: Directed or undirected?
2. **Edge order matters**: "Return last edge" vs "any edge"
3. **Explain detection**: "Edge creates cycle iff endpoints already connected"
4. **Mention Kruskal's**: Shows broader understanding

---

## Practice Problems

| #   | Problem                              | LeetCode | Difficulty | Key Concept                       |
| --- | ------------------------------------ | -------- | ---------- | --------------------------------- |
| 1   | Graph Valid Tree                     | 261      | Medium     | No cycles + connected             |
| 2   | Redundant Connection                 | 684      | Medium     | Find the cycle-creating edge      |
| 3   | Number of Operations to Make Network | 1319     | Medium     | Redundant edges + components      |
| 4   | Detect Cycles in 2D Grid            | 1559     | Medium     | Grid as graph                     |
| 5   | Min Cost to Connect All Points       | 1584     | Medium     | Kruskal's MST                     |
| 6   | Redundant Connection II              | 685      | Hard       | Directed graph, 3-case analysis   |
| 7   | Critical Connections in a Network    | 1192     | Hard       | Bridges (harder, uses Tarjan)     |

---

## Related Sections

- [Union-Find Basics](./01-union-find-basics.md) - Foundation
- [Connected Components](./04-connected-components.md) - Counting groups
- [Graph DFS](../08-graphs/README.md) - Alternative cycle detection
