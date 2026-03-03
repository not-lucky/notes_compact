# Shortest Path in Unweighted Graphs

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md)

## Interview Context

BFS for shortest path is fundamental because:

1. **Optimal for unweighted**: O(V + E) is the best we can do
2. **Foundation for other algorithms**: Dijkstra extends this concept
3. **Very common in interviews**: Grid shortest paths, word ladders (especially Amazon)
4. **Simpler than Dijkstra**: No heap needed

> **FANG Focus: Amazon Grid Problems**
> Amazon heavily favors grid-based shortest path problems in both phone screens and onsite interviews. Expect variations like "minimum steps to reach a target while avoiding obstacles," "shortest path with a given number of obstacle removals," or "multi-source BFS" (like rotting oranges). Mastery of the 4-directional and 8-directional BFS templates is non-negotiable for Amazon.

When all edges have equal weight, BFS is the answer.

---

## Why BFS Guarantees Shortest Path (Intuition)

BFS explores nodes **level by level**. Every node at distance `d` from the source is visited before any node at distance `d + 1`. This creates a strict ordering guarantee:

1. **Level 0**: The source node (distance 0).
2. **Level 1**: All neighbors of the source (distance 1).
3. **Level k**: All nodes reachable in exactly `k` steps that haven't been seen at an earlier level.

**The key insight**: When BFS first reaches a node, the path it took is guaranteed to be shortest. Why? Because if a shorter path existed (say length `k-1`), BFS would have discovered that node at level `k-1` — but it didn't, so no shorter path exists.

**Formal argument** (proof by contradiction): Suppose BFS assigns distance `d` to node `v`, but there exists a path of length `d' < d`. That path passes through nodes at distances `0, 1, ..., d'-1, d'`. BFS processes nodes in non-decreasing order of distance, so it would have discovered `v` via that shorter path at level `d'` before level `d`. Contradiction — BFS marks nodes visited when first seen, so `v` can only be assigned one distance.

> **This guarantee breaks with weighted edges.** If edges have different weights, a path with fewer edges can be longer than one with more edges. That's why we need Dijkstra for weighted graphs.

```
Graph:              BFS from 0:
    0 --- 1         Level 0: {0}  (dist 0)
    |     |         Level 1: {1, 2}  (dist 1)
    2 --- 3         Level 2: {3}  (dist 2)

Shortest path 0→3: 0→1→3 or 0→2→3, both length 2
```

---

## Theory: Edge Types in BFS

When performing BFS on a graph, the edges can be classified into two types based on the BFS tree:

1. **Tree Edges**: Edges that lead to an unvisited node, discovering it for the first time.
2. **Cross Edges**: Edges connecting two already-discovered nodes. In an undirected graph, cross edges always connect nodes at the same level or adjacent levels (level difference is at most 1).

**Why it matters:**
- If a cross edge connects nodes at the same level, it creates an odd-length cycle.
- If a cross edge connects nodes at adjacent levels, it creates an even-length cycle.
- BFS cannot produce "back edges" in undirected graphs (unlike DFS), which is why it's ideal for shortest paths — every edge either discovers a new node at the next level or connects nodes at nearby levels.

---

## Complexity Analysis: Sparse vs Dense Representations

The time complexity of BFS is O(V + E), but practical performance depends on graph representation:

### 1. Adjacency List (Sparse Graphs)
- **Time Complexity**: O(V + E). Each vertex dequeued once, each edge examined once.
- **Space Complexity**: O(V + E) to store the graph.
- **When to use**: Almost always preferred in interviews. Most interview graphs (grids, social networks, word ladders) are sparse (E << V²).

### 2. Adjacency Matrix (Dense Graphs)
- **Time Complexity**: O(V²). For every dequeued vertex, we scan the entire row of size V to find neighbors.
- **Space Complexity**: O(V²) to store the graph.
- **When to use**: Rarely for BFS, unless the graph is extremely dense (E ≈ V²) or you need O(1) edge lookups with small V (e.g., V ≤ 1000).

---

## BFS Shortest Path Template

```python
from collections import deque


def shortest_path_bfs(
    graph: dict[int, list[int]], start: int, end: int
) -> int:
    """
    Find shortest path distance in an unweighted graph.

    Time:  O(V + E)
    Space: O(V)

    Returns -1 if no path exists.
    """
    if start == end:
        return 0

    visited = {start}
    queue = deque([(start, 0)])  # (node, distance)

    while queue:
        node, dist = queue.popleft()

        for neighbor in graph[node]:
            if neighbor == end:
                return dist + 1  # early termination

            if neighbor not in visited:
                visited.add(neighbor)  # mark BEFORE enqueuing
                queue.append((neighbor, dist + 1))

    return -1  # no path exists
```

### Grid BFS (4-Directional)

```python
from collections import deque


def shortest_path_grid(
    grid: list[list[int]],
    start: tuple[int, int],
    end: tuple[int, int],
) -> int:
    """
    Shortest path in a grid (0 = passable, 1 = blocked).

    Time:  O(rows * cols)
    Space: O(rows * cols)
    """
    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
        return -1

    if start == end:
        return 0

    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    visited = {start}
    queue = deque([(start[0], start[1], 0)])  # (row, col, distance)

    while queue:
        r, c, dist = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if (nr, nc) == end:
                return dist + 1

            if (0 <= nr < rows and 0 <= nc < cols
                    and (nr, nc) not in visited
                    and grid[nr][nc] == 0):
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))

    return -1
```

---

## Path Reconstruction

Often you need the actual path, not just the distance. Track each node's parent during BFS and backtrack from the destination.

```python
from collections import deque


def shortest_path_with_reconstruction(
    graph: dict[int, list[int]], start: int, end: int
) -> list[int] | None:
    """
    Find a shortest path and return the full node sequence.
    Returns None if no path exists.

    Time:  O(V + E)
    Space: O(V) for parent map
    """
    if start == end:
        return [start]

    visited = {start}
    parent: dict[int, int] = {}  # child -> parent
    queue = deque([start])

    while queue:
        node = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)

                if neighbor == end:
                    # Backtrack from end to start
                    path = []
                    current = end
                    while current != start:
                        path.append(current)
                        current = parent[current]
                    path.append(start)
                    return path[::-1]

    return None  # no path
```

---

## Multi-Source BFS

When the problem has **multiple starting points** (e.g., "distance from nearest 0", "rotting oranges"), initialize the queue with all sources at distance 0. BFS then expands outward from all sources simultaneously.

```python
from collections import deque


def multi_source_shortest(
    grid: list[list[int]],
) -> list[list[int]]:
    """
    For each cell, find the shortest distance to the nearest 0.
    (LeetCode 542 - 01 Matrix)

    Time:  O(rows * cols)
    Space: O(rows * cols)
    """
    rows, cols = len(grid), len(grid[0])
    dist = [[float("inf")] * cols for _ in range(rows)]
    queue: deque[tuple[int, int]] = deque()

    # Enqueue ALL sources (cells with value 0) at distance 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                dist[r][c] = 0
                queue.append((r, c))

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        r, c = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and dist[nr][nc] > dist[r][c] + 1):
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))

    return dist
```

**Why it works**: By starting BFS from all sources at once, the first time we reach any cell is via the nearest source. This is exactly like adding a virtual super-source connected to all real sources with 0-weight edges.

---


## State-Space BFS

In many FANG problems, the graph isn't explicitly given as nodes and edges. Instead, the problem asks for the minimum steps to reach a target state, where each "step" is a valid transformation.

The "nodes" are the states (e.g., a board configuration, a string, a tuple of variables).
The "edges" are the valid transitions between states.

### Key differences from standard graph BFS:
1. **Implicit Graph**: You generate neighbors dynamically using rules.
2. **State Representation**: The state must be immutable and hashable (e.g., tuple, string) to store in `visited`.
3. **Queue Elements**: The queue usually stores `(state, distance)`.

### Template for State-Space BFS

```python
from collections import deque

def shortest_path_state_space(start_state, target_state) -> int:
    if start_state == target_state:
        return 0
        
    queue = deque([(start_state, 0)])
    visited = {start_state}
    
    while queue:
        current_state, steps = queue.popleft()
        
        # get_next_states() is a helper you must write based on problem rules
        for next_state in get_next_states(current_state):
            if next_state == target_state:
                return steps + 1
                
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, steps + 1))
                
    return -1
```

*(Examples: Word Ladder, Open the Lock, Minimum Genetic Mutation)*

## Shortest Path in Binary Matrix (8 Directions)

```python
from collections import deque


def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    """
    Shortest path from (0,0) to (n-1,n-1) with 8-directional movement.
    0 = passable, 1 = blocked. (LeetCode 1091)

    Time:  O(n²)
    Space: O(n²)
    """
    n = len(grid)

    if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
        return -1

    if n == 1:
        return 1  # already at destination, path length = 1 cell

    # 8 directions including diagonals
    directions = [
        (0, 1), (0, -1), (1, 0), (-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1),
    ]

    visited = {(0, 0)}
    queue = deque([(0, 0, 1)])  # (row, col, path_length) — count cells, not edges

    while queue:
        r, c, length = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if nr == n - 1 and nc == n - 1:
                return length + 1

            if (0 <= nr < n and 0 <= nc < n
                    and (nr, nc) not in visited
                    and grid[nr][nc] == 0):
                visited.add((nr, nc))
                queue.append((nr, nc, length + 1))

    return -1
```

---

## All Shortest Paths

```python
from collections import deque, defaultdict


def all_shortest_paths(
    graph: dict[int, list[int]], start: int, end: int
) -> list[list[int]]:
    """
    Find ALL shortest paths from start to end.

    Key idea: Run BFS to compute distances and collect all predecessors
    that lie on a shortest path, then backtrack.

    Time:  O(V + E + P) where P is the total length of all paths
    Space: O(V + P)
    """
    if start == end:
        return [[start]]

    # BFS to find distances and predecessor lists
    dist: dict[int, int] = {start: 0}
    predecessors: dict[int, list[int]] = defaultdict(list)
    queue = deque([start])

    while queue:
        node = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)

            # Record as predecessor if this edge is on a shortest path
            if dist.get(neighbor) == dist[node] + 1:
                predecessors[neighbor].append(node)

    if end not in dist:
        return []

    # Backtrack from end to start to reconstruct all paths
    paths: list[list[int]] = []

    def backtrack(node: int, path: list[int]) -> None:
        if node == start:
            paths.append(path[::-1])
            return
        for pred in predecessors[node]:
            path.append(pred)
            backtrack(pred, path)
            path.pop()

    backtrack(end, [end])
    return paths
```

---


## Optimization: Bidirectional BFS

When the branching factor is large and you know both the `start` and `end` nodes (e.g., Word Ladder), you can search simultaneously from both ends. This dramatically reduces the search space.

- Standard BFS expands $b^d$ nodes (where $b$ is branching factor, $d$ is distance).
- Bidirectional BFS expands $b^{d/2} + b^{d/2}$ nodes.

### Concept:
1. Maintain two sets of currently active nodes: `forward_front` and `backward_front`.
2. Maintain two visited sets (or dictionaries storing distances) to prevent cycles and detect intersection.
3. In each step, **expand the smaller front** to minimize the branching factor.
4. If a neighbor is in the other visited set, the paths have met.

```python
def bidirectional_bfs(graph: dict[int, list[int]], start: int, end: int) -> int:
    """
    Find shortest path distance using bidirectional BFS.
    Time: O(b^(d/2)) where b is branching factor and d is distance.
    Space: O(b^(d/2))
    """
    if start == end:
        return 0

    front_f = {start}
    front_b = {end}
    
    visited_f = {start: 0}
    visited_b = {end: 0}

    # As long as both fronts have nodes to expand
    while front_f and front_b:
        # Optimization: Expand the smaller front
        if len(front_f) <= len(front_b):
            current_front, other_front = front_f, front_b
            current_visited, other_visited = visited_f, visited_b
        else:
            current_front, other_front = front_b, front_f
            current_visited, other_visited = visited_b, visited_f

        next_front = set()
        
        # Expand all nodes in the current front (level by level)
        for node in current_front:
            dist = current_visited[node]
            
            for neighbor in graph[node]:
                # Intersection found! Paths connect here.
                if neighbor in other_visited:
                    return dist + 1 + other_visited[neighbor]

                if neighbor not in current_visited:
                    current_visited[neighbor] = dist + 1
                    next_front.add(neighbor)
                    
        # Update the front we just expanded
        if current_front is front_f:
            front_f = next_front
        else:
            front_b = next_front

    return -1
```
## 0-1 BFS

Special case: edges have weight 0 or 1. Use a deque — add weight-0 neighbors to the **front**, weight-1 neighbors to the **back**. This maintains the invariant that the deque is sorted by distance, so we always process the closest node first (like Dijkstra but in O(V + E)).

```python
from collections import deque


def shortest_path_01(
    graph: dict[int, list[tuple[int, int]]], start: int, end: int
) -> int:
    """
    Shortest path when edges have weight 0 or 1.

    graph[u] = [(v, weight), ...]  where weight is 0 or 1.

    Time:  O(V + E)
    Space: O(V)
    """
    INF = float("inf")
    dist: dict[int, float] = {start: 0}
    queue = deque([start])

    while queue:
        node = queue.popleft()
        current_dist = dist[node]

        # Skip stale entries: if we already found a shorter path
        # to this node, this deque entry is outdated.
        # (A node can be enqueued multiple times with different distances.)
        if current_dist > dist.get(node, INF):
            continue

        if node == end:
            return int(current_dist)

        for neighbor, weight in graph[node]:
            new_dist = current_dist + weight

            if new_dist < dist.get(neighbor, INF):
                dist[neighbor] = new_dist
                if weight == 0:
                    queue.appendleft(neighbor)  # front — same distance level
                else:
                    queue.append(neighbor)       # back — next distance level

    return dist.get(end, -1) if dist.get(end, INF) != INF else -1
```

---

## Comparison with Other Algorithms

| Algorithm      | Graph Type          | Time           | When to Use                     |
| -------------- | ------------------- | -------------- | ------------------------------- |
| BFS            | Unweighted          | O(V + E)       | All edges same weight           |
| Bidirectional BFS | Unweighted, known target | O(b^(d/2)) | Huge branching factor          |
| 0-1 BFS        | Weights 0 or 1      | O(V + E)       | Binary edge weights             |
| Dijkstra       | Weighted (positive) | O((V+E) log V) | Different positive weights      |
| Bellman-Ford   | Weighted (any)      | O(V × E)       | Negative weights                |
| Floyd-Warshall | All pairs           | O(V³)          | Multiple source-target queries  |

---

## Minimum Knight Moves

```python
from collections import deque


def min_knight_moves(x: int, y: int) -> int:
    """
    Minimum moves for a knight to reach (x, y) from (0, 0).
    (LeetCode 1197)

    Time:  O(|x| * |y|)  — bounded search space
    Space: O(|x| * |y|)
    """
    moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2),
    ]

    # Exploit symmetry: work in first quadrant
    x, y = abs(x), abs(y)

    visited = {(0, 0)}
    queue = deque([(0, 0, 0)])  # (cx, cy, steps)

    while queue:
        cx, cy, steps = queue.popleft()

        if cx == x and cy == y:
            return steps

        for dx, dy in moves:
            nx, ny = cx + dx, cy + dy

            # Allow small negatives (-2) to handle edge cases near origin
            # (e.g., reaching (1,0) requires going to (-1,1) first)
            if (nx, ny) not in visited and nx >= -2 and ny >= -2:
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))

    return -1  # unreachable (shouldn't happen on infinite board)
```

---

## Edge Cases

```python
# 1. Start equals end → return 0
shortest_path_bfs(graph, 0, 0)  # 0

# 2. No path exists (disconnected graph) → return -1

# 3. Empty graph → handle gracefully (start not in graph)
graph: dict[int, list[int]] = {}

# 4. Single node, no edges
graph = {0: []}
shortest_path_bfs(graph, 0, 0)  # 0

# 5. Large grid → must use deque (not list) for O(1) popleft
#    list.pop(0) is O(n) and will TLE on large inputs
```

---

## Common Mistakes

```python
# MISTAKE 1: Using DFS for shortest path in unweighted graph
# DFS finds *a* path, not the *shortest* path.
# BFS is the only correct choice for unweighted shortest path.


# MISTAKE 2: Marking visited when DEQUEUING instead of ENQUEUING
# WRONG — allows the same node to be enqueued multiple times:
while queue:
    node = queue.popleft()
    visited.add(node)  # TOO LATE! Duplicates already in queue

# CORRECT — mark visited immediately when adding to queue:
if neighbor not in visited:
    visited.add(neighbor)  # mark BEFORE enqueuing
    queue.append(neighbor)


# MISTAKE 3: Using list as queue instead of collections.deque
# list.pop(0) is O(n), deque.popleft() is O(1).
# This turns O(V + E) BFS into O(V² + VE).


# MISTAKE 4: Forgetting to handle start == end
# Always check this as a base case before BFS.


# NOTE: Checking destination at enqueue vs dequeue
# Checking at DEQUEUE is always correct:
while queue:
    node, dist = queue.popleft()
    if node == end:
        return dist  # correct

# Checking at ENQUEUE is an optimization (fewer iterations):
for neighbor in graph[node]:
    if neighbor == end:
        return dist + 1  # also correct, terminates sooner

# Both approaches are valid for standard BFS. The enqueue check
# is a minor optimization. Use whichever feels more natural.
```

---

## Interview Tips

1. **BFS = shortest in unweighted**: State this explicitly to your interviewer.
2. **Use deque**: `popleft()` is O(1). `list.pop(0)` is O(n) — instant red flag.
3. **Mark visited when enqueuing**: Prevents duplicate work and is the #1 BFS bug.
4. **Grid = implicit graph**: Each cell is a node, 4 or 8 neighbors are edges.
5. **Multi-source BFS**: Enqueue all sources at distance 0 for "nearest X" problems.
6. **Path reconstruction**: Track a `parent` dict and backtrack from destination.

---

## Practice Problems

| #   | Problem                                      | LC # | Difficulty | Hint                                                                 |
| --- | -------------------------------------------- | ---- | ---------- | -------------------------------------------------------------------- |
| 1   | Shortest Path in Binary Matrix               | 1091 | Medium     | 8-directional BFS; count cells not edges (path length starts at 1).  |
| 2   | 01 Matrix                                    | 542  | Medium     | Multi-source BFS: enqueue all 0-cells first, expand outward.         |
| 3   | Rotting Oranges                               | 994  | Medium     | Multi-source BFS from all rotten oranges; answer is max distance.    |
| 4   | Open the Lock                                | 752  | Medium     | State-space BFS: each lock state is a node, turns are edges.         |
| 5   | Word Ladder                                  | 127  | Hard       | Implicit graph — build adjacency via wildcard patterns (h*t → hot).  |
| 6   | Shortest Path with Alternating Colors        | 1129 | Medium     | BFS with state = (node, last_color); track visited per color.        |
| 7   | Shortest Bridge                              | 934  | Medium     | DFS to find one island, then multi-source BFS to reach the other.    |
| 8   | Minimum Knight Moves                         | 1197 | Medium     | Exploit symmetry (first quadrant); allow small negative coords.      |

---

## Key Takeaways

1. **BFS guarantees shortest path** in unweighted graphs because it explores level by level — first visit is always via the shortest path.
2. **O(V + E) is optimal** — every shortest path algorithm must examine the graph.
3. **Mark visited on enqueue, not dequeue** — the single most common BFS bug.
4. **Multi-source BFS** solves "nearest X" problems — enqueue all sources at once.
5. **Path reconstruction** — store a parent map during BFS, backtrack from destination.
6. **0-1 BFS** — deque trick for binary-weight edges, still O(V + E).

---

## Next: [12-clone-graph.md](./12-clone-graph.md)

Learn to deep copy graphs.
