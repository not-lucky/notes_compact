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

## Interview Context

Understanding graph representations is critical because:

1. **Foundation for all graph problems**: Every graph algorithm builds on this
2. **Trade-off decisions**: Space vs time, sparse vs dense graphs
3. **Interview input formats**: You'll receive edges as lists, must build your own structure
4. **Conversion skills**: Often need to convert between representations

Interviewers expect you to quickly build a graph from edge lists and choose the right representation.

---

## Core Concept: What is a Graph?

A **graph** G = (V, E) consists of:
- **Vertices (V)**: Nodes/points
- **Edges (E)**: Connections between vertices

```
Undirected Graph:           Directed Graph:
    0 --- 1                     0 --> 1
    |     |                     |     |
    2 --- 3                     v     v
                                2 --> 3
```

### Graph Types

| Type | Description |
|------|-------------|
| **Undirected** | Edges go both ways |
| **Directed** | Edges have direction |
| **Weighted** | Edges have costs/distances |
| **Unweighted** | All edges equal cost (or cost = 1) |
| **Cyclic** | Contains at least one cycle |
| **Acyclic** | No cycles (DAG for directed) |
| **Connected** | Path exists between all vertices |
| **Sparse** | Few edges (E << V²) |
| **Dense** | Many edges (E ≈ V²) |

---

## Representation 1: Adjacency List

**Most common for interviews.** Store neighbors for each vertex.

```python
from collections import defaultdict

def build_adjacency_list(n: int, edges: list[list[int]],
                          directed: bool = False) -> dict[int, list[int]]:
    """
    Build adjacency list from edge list.

    Time: O(E)
    Space: O(V + E)

    Args:
        n: Number of vertices (0 to n-1)
        edges: List of [u, v] pairs
        directed: If True, only add u -> v
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

### With Weights

```python
def build_weighted_graph(n: int, edges: list[list[int]],
                          directed: bool = False) -> dict[int, list[tuple[int, int]]]:
    """
    Build weighted adjacency list.
    edges format: [u, v, weight]
    """
    graph = defaultdict(list)

    for i in range(n):
        graph[i]

    for u, v, w in edges:
        graph[u].append((v, w))
        if not directed:
            graph[v].append((u, w))

    return graph


# Example
edges = [[0, 1, 5], [0, 2, 3], [1, 3, 1]]
graph = build_weighted_graph(4, edges, directed=True)
# {0: [(1, 5), (2, 3)], 1: [(3, 1)], 2: [], 3: []}
```

---

## Representation 2: Adjacency Matrix

**Best for dense graphs** or when checking edge existence frequently.

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


# Example
edges = [[0, 1], [0, 2], [1, 3]]
matrix = build_adjacency_matrix(4, edges)
# [[0, 1, 1, 0],
#  [1, 0, 0, 1],
#  [1, 0, 0, 0],
#  [0, 1, 0, 0]]
```

### With Weights

```python
def build_weighted_matrix(n: int, edges: list[list[int]],
                           directed: bool = False) -> list[list[int]]:
    """
    Build weighted adjacency matrix.
    Use infinity for no edge.
    """
    INF = float('inf')
    matrix = [[INF] * n for _ in range(n)]

    # Distance to self is 0
    for i in range(n):
        matrix[i][i] = 0

    for u, v, w in edges:
        matrix[u][v] = w
        if not directed:
            matrix[v][u] = w

    return matrix
```

---

## Representation 3: Edge List

**Simplest form**, often the input format. Convert to adjacency list for processing.

```python
# Edge list format
edges = [(0, 1), (0, 2), (1, 3), (2, 3)]

# Weighted edge list
weighted_edges = [(0, 1, 5), (0, 2, 3), (1, 3, 1)]

# Direct usage (e.g., Bellman-Ford)
for u, v, w in weighted_edges:
    # Process edge
    pass
```

---

## Comparison of Representations

| Operation | Adjacency List | Adjacency Matrix |
|-----------|----------------|------------------|
| Space | O(V + E) | O(V²) |
| Add edge | O(1) | O(1) |
| Remove edge | O(E) | O(1) |
| Check edge exists | O(degree) | O(1) |
| Get all neighbors | O(1) | O(V) |
| Iterate all edges | O(V + E) | O(V²) |

**Use Adjacency List when:**
- Graph is sparse (E << V²)
- Most interview problems
- Need to iterate neighbors frequently

**Use Adjacency Matrix when:**
- Graph is dense (E ≈ V²)
- Need frequent edge existence checks
- Floyd-Warshall algorithm

---

## Building Graphs from Common Input Formats

### Format 1: Edge List with N Nodes

```python
# Input: n = 4, edges = [[0,1], [1,2], [2,3]]
def solve(n: int, edges: list[list[int]]) -> ...:
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)  # Undirected
    # Now use graph...
```

### Format 2: Adjacency List Already Given

```python
# Input: graph = [[1,2], [0,3], [0], [1]]
# graph[i] = list of neighbors of node i
def solve(graph: list[list[int]]) -> ...:
    # Use directly
    for neighbor in graph[0]:
        print(neighbor)
```

### Format 3: Prerequisites (Directed)

```python
# Input: numCourses = 4, prerequisites = [[1,0], [2,1], [3,2]]
# [a, b] means b -> a (b is prereq of a)
def solve(numCourses: int, prerequisites: list[list[int]]) -> ...:
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)  # b -> a
```

### Format 4: Grid as Graph

```python
# Input: grid (2D array)
def solve(grid: list[list[int]]) -> ...:
    rows, cols = len(grid), len(grid[0])

    # Neighbors using directions
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def get_neighbors(r: int, c: int):
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                yield nr, nc
```

---

## Grid as Implicit Graph

Grids are graphs where:
- Each cell is a vertex
- Adjacent cells are connected by edges

```
Grid:               Implicit Graph:
1 1 0               (0,0)-(0,1)  (0,2)
1 1 0                 |    |
0 0 1               (1,0)-(1,1)  (1,2)

                    (2,0) (2,1)  (2,2)
```

```python
# Grid traversal template
def grid_bfs(grid: list[list[int]], start: tuple[int, int]):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    visited = set([start])
    queue = deque([start])

    while queue:
        r, c = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in visited and grid[nr][nc] == 1):
                visited.add((nr, nc))
                queue.append((nr, nc))
```

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
5. **Use defaultdict**: Cleaner than checking if key exists

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Find if Path Exists in Graph | Easy | Basic graph traversal |
| 2 | Clone Graph | Medium | Graph construction |
| 3 | Number of Islands | Medium | Grid as graph |
| 4 | Graph Valid Tree | Medium | Connected + acyclic |

---

## Key Takeaways

1. **Adjacency list** is default for interviews (sparse, efficient)
2. **Adjacency matrix** for dense graphs or edge existence checks
3. **Always handle disconnected graphs**: Iterate over all nodes
4. **Grids are implicit graphs**: Each cell is a node
5. **Know the input format**: Build graph accordingly

---

## Next: [02-bfs-basics.md](./02-bfs-basics.md)

Learn BFS traversal, the foundation for shortest path in unweighted graphs.
