# Redundant Connection (Cycle Detection)

> **Prerequisites:** [Union-Find Basics](./01-union-find-basics.md), [Path Compression](./02-path-compression.md)

## Interview Context

"Redundant Connection" (LeetCode 684, 685) is a classic Union-Find application for cycle detection in undirected graphs. The key insight: an edge creates a cycle if and only if it connects two already-connected nodes.

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
    |     |    ← This creates a loop: 1-2-3-1
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

**1. For Directed Graphs**

Union-Find treats all edges as undirected. For directed cycle detection:

```python
# Directed graph: A → B → C → A is a cycle
# But A → B, C → B, C → A might not form a directed cycle!

# Use instead:
# - DFS with coloring (white/gray/black)
# - Topological sort (cycle = failed sort)
```

**2. When You Need to Find ALL Cycles**

Union-Find only detects that A cycle exists. To enumerate all cycles:

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

Process edges in order. The first edge that connects already-connected nodes is redundant. Since we want the last such edge, we return the last one that creates a cycle.

Wait, re-reading: in this problem there's exactly ONE extra edge, so exactly ONE edge will trigger "already connected." That's our answer.

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

**LeetCode 685**: Same as above, but the graph is **directed**. One extra edge was added to a tree to form a graph. Find the edge to remove.

### Key Differences

In a directed tree (rooted):

- Every node except root has exactly one parent
- One extra edge means either:
  1. A node has two parents (in-degree 2), OR
  2. There's a cycle

### Cases

```
Case 1: Node with two parents, no cycle
    1 → 2
    ↓   ↓
    3 ←
Remove either incoming edge to the node with in-degree 2.
(Return the later one in input)

Case 2: Cycle exists
    1 → 2
    ↑   ↓
    4 ← 3
Remove the edge that creates the cycle.

Case 3: Both (node with two parents is IN the cycle)
    1 → 2
        ↓
        4 → 3
        ↑   ↓
        ← ←
Node 4 has two parents (1→4 and 3→4) and is in cycle.
Must remove the edge that's part of the cycle.
```

### Solution

```python
def findRedundantDirectedConnection(edges: list[list[int]]) -> list[int]:
    """
    Find redundant directed edge.

    Time: O(n × α(n))
    Space: O(n)
    """
    n = len(edges)
    parent = list(range(n + 1))

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False
        parent[py] = px
        return True

    # Step 1: Find if any node has two parents
    incoming = [0] * (n + 1)  # incoming[v] = parent of v
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
        if candidate2 and [u, v] == candidate2:
            continue  # Skip candidate2

        if not union(u, v):
            # Found cycle
            if candidate1:
                # Had node with 2 parents, and there's a cycle
                # candidate1 must be the one in the cycle
                return candidate1
            else:
                # No node with 2 parents, just a cycle
                return [u, v]

    # No cycle found → candidate2 is the answer
    return candidate2


# Example traces

# Case 1: [[1,2],[1,3],[2,3]] directed
# Node 3 has two parents: 1→3 and 2→3
# candidate1 = [1,3], candidate2 = [2,3]
# Union without [2,3]: 1→2, 1→3, no cycle
# Return candidate2 = [2,3]

# Case 2: [[1,2],[2,3],[3,1]]
# No node with 2 parents
# Union finds cycle at [3,1]
# Return [3,1]
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
3. n nodes, n-1 edges (implied by 1+2)

```python
def validTree(n: int, edges: list[list[int]]) -> bool:
    """
    Check if edges form a valid tree.
    """
    if len(edges) != n - 1:
        return False  # Tree must have exactly n-1 edges

    parent = list(range(n))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return False  # Cycle detected
        parent[pv] = pu

    return True
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

    Time: O(m × n × α(m × n))
    Space: O(m × n)
    """
    m, n = len(grid), len(grid[0])
    parent = list(range(m * n))

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
                    # Same character neighbor
                    pi = find(idx(r, c))
                    pj = find(idx(nr, nc))

                    if pi == pj:
                        return True  # Cycle!

                    parent[pj] = pi

    return False
```

---

## Pattern: Process Edges to Find Cycle

```python
def find_cycle_edge(n: int, edges: list[list[int]]) -> list[int] | None:
    """
    Generic pattern: return first edge that creates a cycle, or None.
    """
    parent = list(range(n))

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return [u, v]  # This edge creates a cycle
        parent[pv] = pu

    return None  # No cycle
```

---

## Minimum Spanning Tree (Kruskal's Algorithm)

Union-Find is essential for Kruskal's MST algorithm:

```python
def kruskal_mst(n: int, edges: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """
    Find MST using Kruskal's algorithm.

    edges: list of (weight, u, v)

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

    # Sort edges by weight
    edges.sort()

    mst = []
    for weight, u, v in edges:
        if union(u, v):  # Add edge if no cycle
            mst.append((weight, u, v))
            if len(mst) == n - 1:
                break  # MST complete

    return mst
```

---

## Complexity Analysis

| Operation         | Time             |
| ----------------- | ---------------- |
| Process one edge  | O(α(n))          |
| Process all edges | O(E × α(n))      |
| Cycle detection   | O(α(n)) per edge |

For Redundant Connection:

- n edges (since n+1 would make it not a near-tree)
- Total: O(n × α(n)) ≈ O(n)

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

| #   | Problem                           | Difficulty | Key Concept                    |
| --- | --------------------------------- | ---------- | ------------------------------ |
| 1   | Redundant Connection              | Medium     | Basic cycle detection          |
| 2   | Redundant Connection II           | Hard       | Directed graph, multiple cases |
| 3   | Graph Valid Tree                  | Medium     | No cycles + connected          |
| 4   | Detect Cycles in 2D Grid          | Medium     | Grid as graph                  |
| 5   | Min Cost to Connect All Points    | Medium     | Kruskal's MST                  |
| 6   | Critical Connections in a Network | Hard       | Bridges (harder, uses Tarjan)  |

---

## Related Sections

- [Union-Find Basics](./01-union-find-basics.md) - Foundation
- [Connected Components](./04-connected-components.md) - Counting groups
- [Graph DFS](../08-graphs/README.md) - Alternative cycle detection
