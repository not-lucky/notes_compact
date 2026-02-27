# Graph Representations

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

## Building Intuition

**Why do we need different representations?** Think of a social network:

- **Sparse network**: Most people have 100-500 friends out of billions of users
- **Dense network**: A small club where everyone knows everyone

For sparse networks (most real-world graphs), storing "who knows whom" as a list is efficient. For dense networks, a matrix makes lookups instant.

**The key insight**: Graph representation is about trade-offs between:

1. **Space**: How much memory do we use?
2. **Access patterns**: What operations do we do most?

**Mental model - The Phone Book Analogy**:

- **Adjacency List** = Phone book with each person's contacts listed under their name
  - Finding all of Alice's friends: O(1) - just look up Alice's entry
  - Checking if Alice knows Bob: O(degree) - scan Alice's contact list
- **Adjacency Matrix** = Giant grid where row=caller, column=receiver, cell=connected?
  - Finding all of Alice's friends: O(n) - scan entire row
  - Checking if Alice knows Bob: O(1) - instant lookup at [Alice][Bob]

**When the representation matters most**:

- BFS/DFS traverse neighbors → Adjacency List wins (O(degree) per node)
- Floyd-Warshall checks all pairs → Adjacency Matrix wins (O(1) per check)
- Most interview problems → Default to Adjacency List

---

## When NOT to Use

**Don't use Adjacency Matrix when:**

- Graph is sparse (E << V²) - wastes O(V²) space
- You need to iterate all edges - O(V²) vs O(E) for list
- Memory is constrained - matrix scales quadratically

**Don't use Adjacency List when:**

- Frequent "does edge exist?" queries - O(degree) vs O(1) for matrix
- Graph is dense (E ≈ V²) - list overhead exceeds matrix
- Using Floyd-Warshall algorithm - needs matrix structure

**Don't over-engineer representation when:**

- Problem gives adjacency list directly - use it as-is
- Grid problem - use implicit neighbors, don't build explicit graph
- Tree problem - parent/children pointers often cleaner

---

## Interview Context & FANG Focus

Understanding graph representations is critical because:

1. **Foundation for all graph problems**: Every graph algorithm builds on this
2. **Trade-off decisions**: Space vs time, sparse vs dense graphs
3. **Interview input formats**: You'll receive edges as lists, must build your own structure
4. **Conversion skills**: Often need to convert between representations

### FANG Perspective
- **Amazon** loves Grid/Matrix traversal problems (like "Rotting Oranges" or "Number of Islands") and often asks them as a disguised graph problem. You must recognize when a 2D matrix *is* the graph vs when a 2D matrix is an adjacency matrix.
- **Google/Meta** often present problems with an edge list input and ask follow-ups about dense vs sparse implications. Being able to fluently write an adjacency list from an edge list is a non-negotiable prerequisite.
- Expect questions on the recursion stack limit. When working with Deep DFS, you must know your language's limits (Python hits a recursion limit around 1000).

---

## Core Concept: What is a Graph?

A **graph** G = (V, E) consists of:

- **Vertices (V)**: Nodes/points
- **Edges (E)**: Connections between vertices

```
Undirected Graph:           Directed Graph:
    0 ─── 1                     0 ──▶ 1
    │     │                     │     │
    2 ─── 3                     ▼     ▼
                                2 ──▶ 3
```

### Graph Types

| Type           | Description                        |
| -------------- | ---------------------------------- |
| **Undirected** | Edges go both ways                 |
| **Directed**   | Edges have direction               |
| **Weighted**   | Edges have costs/distances         |
| **Unweighted** | All edges equal cost (or cost = 1) |
| **Cyclic**     | Contains at least one cycle        |
| **Acyclic**    | No cycles (DAG for directed)       |
| **Connected**  | Path exists between all vertices   |
| **Sparse**     | Few edges (E << V²)                |
| **Dense**      | Many edges (E ≈ V²)                |

---

## Edge Types (DFS/BFS Context)

When traversing a directed graph (especially using DFS), edges are categorized into four types. This theory is heavily tested in cycle detection and topological sorting.

1. **Tree Edge**: Edges that form the DFS spanning tree (visiting an unvisited node).
2. **Back Edge**: Edge pointing from a node to one of its ancestors in the DFS tree. **Presence of a back edge indicates a cycle.**
3. **Forward Edge**: Edge pointing from a node to a descendant in the DFS tree (that is not a direct child).
4. **Cross Edge**: Edge pointing from a node to another node that is neither an ancestor nor descendant (typically to a node already fully processed).

In an **undirected graph**, every edge is either a Tree Edge or a Back Edge. Forward and Cross edges do not exist because if an edge could be a cross edge, it would have been traversed in the opposite direction and classified differently.

---

## Representation 1: Adjacency List

**Most common for interviews.** Store neighbors for each vertex.

<details>
<summary>Python</summary>

```python
from collections import defaultdict

def build_adjacency_list(n: int, edges: list[list[int]],
                          directed: bool = False) -> dict[int, list[int]]:
    """
    Build adjacency list from edge list.

    Time: O(E)
    Space: O(V + E)
    """
    graph = defaultdict(list)

    # Initialize all vertices (important for disconnected graphs)
    for i in range(n):
        graph[i]  # Creates empty list

    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)

    return graph

# Example
edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
graph = build_adjacency_list(4, edges)
# {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}
```
</details>

### With Weights

For weighted graphs, store tuples/pairs/objects containing `(neighbor, weight)`.

---

## Representation 2: Adjacency Matrix

**Best for dense graphs** or when checking edge existence frequently.

<details>
<summary>Python</summary>

```python
def build_adjacency_matrix(n: int, edges: list[list[int]],
                            directed: bool = False) -> list[list[int]]:
    """
    Build adjacency matrix from edge list.

    Time: O(V² + E)
    Space: O(V²)
    """
    matrix = [[0] * n for _ in range(n)]

    for u, v in edges:
        matrix[u][v] = 1
        if not directed:
            matrix[v][u] = 1

    return matrix
```
</details>

---

## Comparison of Representations and Complexity Analysis

| Operation         | Adjacency List | Adjacency Matrix | Edge List |
| ----------------- | -------------- | ---------------- | --------- |
| **Space**             | **O(V + E)**       | **O(V²)**            | O(E)      |
| Add edge          | O(1)           | O(1)             | O(1)      |
| Remove edge       | O(degree)      | O(1)             | O(E)      |
| Check edge exists | O(degree)      | O(1)             | O(E)      |
| Get all neighbors | O(degree)      | O(V)             | O(E)      |
| Iterate all edges | O(V + E)       | O(V²)            | O(E)      |

### Sparse vs Dense Representation Analysis

1. **Sparse Graphs ($E \ll V^2$)**:
   - For example, cities connected by highways, or users in a social network.
   - Using an **Adjacency Matrix** here is extremely wasteful. A matrix for 1 million users takes $10^6 \times 10^6$ bytes = 1 Terabyte of memory, mostly storing `0`s (no connection).
   - An **Adjacency List** only stores actual connections, keeping memory proportional to the actual data $O(V + E)$.

2. **Dense Graphs ($E \approx V^2$)**:
   - For example, flight paths between major hubs, or small highly connected clusters.
   - An **Adjacency Matrix** is very efficient here. It offers $O(1)$ edge lookups and has lower constant overhead than a list of lists or hash maps. The $O(V^2)$ memory is justified because almost all cells are `1`.

### Language Limits: Recursion Stack Space

When analyzing Space Complexity for graphs, you **must include the recursion stack** for DFS.

- **Python**: Default recursion limit is typically 1000. For graphs deeper than this (e.g., a linked list shaped graph of 10,000 nodes), DFS will throw `RecursionError`.
  - *Interview tip*: You can use `sys.setrecursionlimit(2000)` in Python, but interviewers prefer iterative DFS using an explicit stack for deep graphs.

---

## Grid as Implicit Graph

Grids (2D arrays) are graphs where:

- Each cell is a **vertex**
- Adjacent cells (up, down, left, right) represent **edges**

**Crucial Theory**: *Never build an explicit Adjacency List for a grid problem.* Grids are already their own adjacency matrix / graph representation. The connections are implicitly defined by the indices.

```
Grid:               Implicit Graph:
1 1 0               (0,0) ─── (0,1)   (0,2)
1 1 0                 │         │
0 0 1               (1,0) ─── (1,1)   (1,2)

                    (2,0)     (2,1)   (2,2)
```

### Grid Traversal Template

<details>
<summary>Python</summary>

```python
from collections import deque

def grid_bfs(grid: list[list[int]], start: tuple[int, int]):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    visited = set([start])
    queue = deque([start])

    while queue:
        r, c = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # 1. Bounds check
            # 2. Visited check
            # 3. Validity check (e.g., grid[nr][nc] == 1)
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] == 1:
                visited.add((nr, nc))
                queue.append((nr, nc))
```
</details>

---

## Edge Cases

```python
# 1. Empty graph
n = 0, edges = []

# 2. Single node, no edges
n = 1, edges = []

# 3. Disconnected graph
#   0 - 1    3 - 4
edges = [[0, 1], [3, 4]]

# 4. Self-loop
edges = [[0, 0]]  # Node connected to itself

# 5. Multiple edges between same nodes
edges = [[0, 1], [0, 1]]  # Usually should deduplicate

# 6. Node with no edges
n = 3, edges = [[0, 1]]  # Node 2 is isolated
```

---

## Interview Tips

1. **Ask about input format**: Edge list? Adjacency list? What represents edges?
2. **Clarify directed/undirected**: Critical for building graph correctly
3. **Handle disconnected graphs**: Don't assume all nodes are reachable
4. **Initialize all nodes**: Important for graphs with isolated nodes
5. **Use correct data structure**: Default to Array/Vector of Arrays/Vectors when node IDs are `0` to `n-1`. Only use HashMap/Dictionary if nodes are arbitrary strings/values.

---

## Practice Problems

| #   | Problem                      | Difficulty | Key Concept           |
| --- | ---------------------------- | ---------- | --------------------- |
| 1   | Find if Path Exists in Graph | Easy       | Basic graph traversal |
| 2   | Clone Graph                  | Medium     | Graph construction    |
| 3   | Number of Islands            | Medium     | Grid as graph         |
| 4   | Graph Valid Tree             | Medium     | Connected + acyclic   |

---

## Key Takeaways

1. **Adjacency list** is default for interviews (sparse, efficient)
2. **Adjacency matrix** for dense graphs or edge existence checks
3. **Always handle disconnected graphs**: Iterate over all nodes
4. **Grids are implicit graphs**: Each cell is a node, never build an explicit graph for a grid.
5. **Know the input format**: Build graph accordingly
6. **Mind the recursion limits**: Especially important in Python when dealing with deep graphs.

---

## Next: [02-bfs-basics.md](./02-bfs-basics.md)

Learn BFS traversal, the foundation for shortest path in unweighted graphs.
