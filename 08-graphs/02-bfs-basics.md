# BFS Basics

> **Prerequisites:** [01-graph-representations](./01-graph-representations.md), [05-stacks-queues](../05-stacks-queues/README.md)

## Building Intuition

**The Wave Propagation Mental Model**: Imagine dropping a stone in still water. Ripples spread outward in concentric circles - each ring represents vertices at the same distance from the center. BFS works exactly like this:

```
Time 0:     Time 1:     Time 2:     Time 3:
    ○           ●           ●           ●
                ○ ○       ● ● ●       ● ● ●
                          ○ ○ ○ ○     ● ● ● ●
                                      ○ ○ ○ ○ ○
```

**Why BFS guarantees shortest path in unweighted graphs**:

1. We process nodes level-by-level (distance 0, then 1, then 2...)
2. When we first reach a node, we've taken the minimum hops
3. All edges have equal weight (1), so "minimum hops" = shortest path

**Why level-by-level? The FIFO queue is everything**:

- FIFO (First-In-First-Out) ensures we exhaust all distance-k nodes before distance-(k+1)
- Nodes discovered at distance k are enqueued *before* any distance-(k+1) nodes
- So when we dequeue, we always finish the current "wave" before starting the next
- Using a **stack** instead would make it DFS (depth-first, not breadth-first)
- Using a **priority queue** instead would make it Dijkstra (weighted shortest path)

**Visual proof of correctness**:

```
If BFS visits node X at distance d, can there be a shorter path?
No! Because:
1. All nodes at distance < d were already processed
2. None of them led to X (or we'd have seen X earlier)
3. Therefore d is the minimum distance to X
```

---

## When NOT to Use

**Don't use BFS when:**

- **Edges have different weights** → Use Dijkstra instead
- **You need all paths, not just shortest** → Use DFS with backtracking
- **Graph is very deep but narrow** → DFS uses less memory (O(depth) vs O(width))
- **You're detecting cycles in a directed graph** → DFS with three colors is cleaner

**BFS is overkill when:**

- Simple reachability check → DFS is equally valid and often simpler
- Tree traversal without level info → Specialized tree algorithms may be cleaner
- Graph has special structure (DAG) → Topological sort may be better

**Common mistake scenarios:**

- Using BFS on weighted graphs expecting shortest path → **Wrong answer**
- Using `list` instead of `deque` → `list.pop(0)` is O(n), kills performance
- Marking visited when dequeuing instead of enqueueing → Duplicates flood the queue, TLE

---

## Interview Context

BFS is essential because:

1. **Shortest path in unweighted graphs**: The go-to algorithm
2. **Level-order traversal**: Process nodes layer by layer
3. **Multi-source BFS**: Handle problems with multiple starting points
4. **Foundation for Dijkstra**: Same pattern with priority queue

### FANG Context (Especially Amazon)
- BFS appears in almost every FANG+ interview loop involving graphs or grids.
- **Amazon strongly favors BFS**, specifically for their online assessment (OA) and onsite coding rounds.
- Look out for problems framed as "Delivery routing", "Spreading infections", or "Minimum steps to reach a package in a warehouse".
- Amazon interviewers frequently ask you to trace the shortest path, not just its length (e.g., using a `parent` pointer map).

---

## Core Concept: How BFS Works

BFS explores vertices level by level using a **queue**:

1. Start from source, mark visited, add to queue
2. Dequeue current vertex, process it, enqueue unvisited neighbors (mark them visited immediately)
3. Repeat until queue is empty

```
Graph:          BFS from 0:
    0           Level 0: 0
   / \          Level 1: 1, 2
  1   2         Level 2: 3, 4
  |   |
  3   4

Order visited: 0 → 1 → 2 → 3 → 4
```

### Theory: Edge Types in BFS

When performing BFS on a connected, undirected graph, the edges can be classified into two types:

1. **Tree Edges**: Edges that discover new, unvisited vertices. These edges form the "BFS Tree" (a spanning tree of the graph).
2. **Cross Edges**: Edges that connect two vertices that are already in the BFS Tree.
   - Crucial property: In a standard BFS on an undirected graph, a cross edge only ever connects vertices at the same level (distance d) or at adjacent levels (distance d and d+1). They never connect vertices skipping a level.

> **Note**: For *directed* graphs, BFS can also produce **back edges** (to an ancestor in the BFS tree). The two-type classification above is specific to undirected graphs.

### Theory: Grid Implicit Graphs

Many BFS problems don't give you an explicit `Graph = (V, E)` representation (like an adjacency list). Instead, they give you a 2D grid (e.g., a maze, a matrix of 1s and 0s).

- **Vertices**: Each cell `(r, c)` in the grid is a vertex.
- **Edges**: Implicitly defined by the valid moves. Typically, an edge exists between `(r, c)` and its 4-direction neighbors `(r+1, c)`, `(r-1, c)`, `(r, c+1)`, `(r, c-1)` if the neighbor is within bounds and not an obstacle.

In these "implicit" graphs, you don't build an adjacency list. You compute the neighbors on the fly during the BFS loop.

---

## BFS Template (Must Know!)

### Python

```python
from collections import deque


def bfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    Basic BFS traversal.

    Time:  O(V + E) — each vertex enqueued once, each edge examined once
    Space: O(V) — for visited set and queue
    """
    visited = {start}            # Mark source visited BEFORE enqueueing
    queue = deque([start])
    order: list[int] = []

    while queue:
        node = queue.popleft()   # FIFO: process oldest node first
        order.append(node)

        for neighbor in graph.get(node, []):  # .get() handles missing keys
            if neighbor not in visited:
                visited.add(neighbor)          # Mark visited NOW, not later
                queue.append(neighbor)

    return order


# Usage
graph = {0: [1, 2], 1: [0, 3], 2: [0, 4], 3: [1], 4: [2]}
print(bfs(graph, 0))  # [0, 1, 2, 3, 4]
```

---

## BFS for Shortest Path (Unweighted)

```python
from collections import deque


def shortest_path(graph: dict[int, list[int]],
                  start: int, end: int) -> int:
    """
    Find shortest path length in unweighted graph.

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

        for neighbor in graph.get(node, []):
            if neighbor == end:
                return dist + 1         # Found target — return immediately

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return -1  # No path found
```

---

## BFS with Path Reconstruction

```python
from collections import deque


def shortest_path_with_path(graph: dict[int, list[int]],
                            start: int, end: int) -> list[int]:
    """
    Find shortest path and return the actual path (not just length).
    Uses a parent pointer map to reconstruct the path.

    Time:  O(V + E)
    Space: O(V)
    """
    if start == end:
        return [start]

    visited = {start}
    queue = deque([start])
    parent: dict[int, int | None] = {start: None}  # child -> parent mapping

    while queue:
        node = queue.popleft()

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)

                if neighbor == end:
                    # Reconstruct path by walking parent pointers backward
                    path: list[int] = []
                    current: int | None = end
                    while current is not None:
                        path.append(current)
                        current = parent[current]
                    return path[::-1]  # Reverse: start → end

    return []  # No path exists


# Usage
graph = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}
print(shortest_path_with_path(graph, 0, 3))  # [0, 1, 3] or [0, 2, 3]
```

---

## Level-Order BFS (Track Levels)

This pattern processes all nodes at the same distance together. The trick: snapshot `len(queue)` at the start of each level, then dequeue exactly that many nodes.

```python
from collections import deque


def bfs_by_level(graph: dict[int, list[int]],
                 start: int) -> list[list[int]]:
    """
    BFS with explicit level tracking.
    Returns nodes grouped by their distance from start.

    Time:  O(V + E)
    Space: O(V)
    """
    visited = {start}
    queue = deque([start])
    levels: list[list[int]] = []

    while queue:
        level_size = len(queue)    # Number of nodes at current distance
        current_level: list[int] = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        levels.append(current_level)

    return levels


# Usage
graph = {0: [1, 2], 1: [0, 3], 2: [0, 4], 3: [1], 4: [2]}
print(bfs_by_level(graph, 0))  # [[0], [1, 2], [3, 4]]
```

---

## Grid BFS Template

```python
from collections import deque

# 4-directional movement: right, left, down, up
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def grid_bfs(grid: list[list[int]],
             start: tuple[int, int]) -> set[tuple[int, int]]:
    """
    BFS on a 2D grid. Visits all reachable cells with value 1.

    Time:  O(rows × cols) — each cell visited at most once
    Space: O(rows × cols) — worst case all cells in queue
    """
    rows, cols = len(grid), len(grid[0])

    visited = {start}
    queue = deque([start])

    while queue:
        r, c = queue.popleft()

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc

            if (0 <= nr < rows and 0 <= nc < cols     # Within bounds
                    and (nr, nc) not in visited        # Not yet seen
                    and grid[nr][nc] == 1):            # Passable cell
                visited.add((nr, nc))
                queue.append((nr, nc))

    return visited
```

---

## Grid Shortest Path

Very common in FAANG: find the shortest path from start to end in a maze.

```python
from collections import deque

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def grid_shortest_path(grid: list[list[int]],
                       start: tuple[int, int], end: tuple[int, int]) -> int:
    """
    Find shortest path in a 2D grid from start to end.
    Assuming 0 is empty space and 1 is a wall.

    Time:  O(rows × cols)
    Space: O(rows × cols)
    """
    rows, cols = len(grid), len(grid[0])
    
    # Check if start or end is blocked
    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
        return -1
        
    if start == end:
        return 0

    visited = {start}
    queue = deque([(start[0], start[1], 0)])  # (row, col, distance)

    while queue:
        r, c, dist = queue.popleft()

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc

            if (0 <= nr < rows and 0 <= nc < cols
                    and (nr, nc) not in visited
                    and grid[nr][nc] == 0):          # 0 is empty space
                
                if (nr, nc) == end:
                    return dist + 1
                    
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))

    return -1  # No path found
```

## Multi-Source BFS

Start from multiple sources simultaneously. All sources begin at distance 0. The BFS "wave" expands from all sources in parallel.

**When to use**: Any problem that asks for the minimum distance from *any* source to each cell (e.g., Rotting Oranges, 01 Matrix).

```python
from collections import deque

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def multi_source_bfs(grid: list[list[int]],
                     sources: list[tuple[int, int]]) -> list[list[int]]:
    """
    BFS from multiple sources simultaneously.
    Returns distance grid where each cell has min distance to any source.

    Time:  O(rows × cols)
    Space: O(rows × cols)

    Example use: LC 994 Rotting Oranges, LC 542 01 Matrix
    """
    rows, cols = len(grid), len(grid[0])

    # Distance grid: -1 means unvisited/unreachable
    dist = [[-1] * cols for _ in range(rows)]

    # Seed the queue with ALL sources at distance 0
    queue: deque[tuple[int, int]] = deque()
    for r, c in sources:
        dist[r][c] = 0
        queue.append((r, c))

    while queue:
        r, c = queue.popleft()

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc

            if (0 <= nr < rows and 0 <= nc < cols
                    and dist[nr][nc] == -1              # Unvisited
                    and grid[nr][nc] == 1):             # Passable
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))

    return dist
```

---

## BFS for All Nodes (Disconnected Graph)

```python
from collections import deque


def bfs_all_components(graph: dict[int, list[int]],
                       n: int) -> list[list[int]]:
    """
    BFS over all nodes, handling disconnected components.
    Returns a list of components, each component is a list of nodes.

    Time:  O(V + E)
    Space: O(V)
    """
    visited: set[int] = set()
    components: list[list[int]] = []

    for node in range(n):
        if node not in visited:
            # BFS for this component
            component: list[int] = []
            queue = deque([node])
            visited.add(node)

            while queue:
                curr = queue.popleft()
                component.append(curr)

                for neighbor in graph.get(curr, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            components.append(component)

    return components
```

---

## When to Use BFS vs DFS

| Scenario                        | Use BFS    | Use DFS                |
| ------------------------------- | ---------- | ---------------------- |
| Shortest path (unweighted)      | ✓          | ✗                      |
| Level-order traversal           | ✓          | ✗                      |
| Bipartite check                 | ✓          | ✓                      |
| Closest node to source          | ✓          | ✗                      |
| Explore all paths               | ✗          | ✓                      |
| Cycle detection                 | Either     | ✓ (simpler)            |
| Topological sort                | ✓ (Kahn's) | ✓ (reverse post-order) |
| Memory constrained (deep graph) | ✗          | ✓                      |
| Connected components            | Either     | Either                 |

**Memory trade-off intuition**:
- BFS queue holds all nodes at the current "frontier" (the widest level). In a balanced binary tree with N nodes, the last level has ~N/2 nodes → O(N) memory.
- DFS stack holds nodes along a single root-to-leaf path → O(depth) memory. For a balanced tree, that's O(log N).
- In a graph that's wide but shallow, BFS uses more memory. In a graph that's narrow but deep, DFS uses more memory.

---

## Complexity Analysis

**Time Complexity: O(V + E)** for Adjacency List (Sparse Graph)
- **O(V²)** for Adjacency Matrix (Dense Graph). When using an adjacency matrix, we must check all V possible neighbors for each of the V nodes, regardless of whether edges exist. This makes scanning neighbors an O(V) operation per node, resulting in total time `V × O(V) = O(V²)`.
- **O(rows × cols)** for Grid Implicit Graphs, assuming constant-time neighbor checks in 4 or 8 directions. Here V = rows × cols and E = O(V) since each cell has at most 4 (or 8) neighbors.

**Space Complexity: O(V)**
Space is primarily used by the `visited` data structure and the BFS `queue`.
- **Adjacency List**: We only track actual edges in memory, and iterating neighbors is optimal per-node.
- **Adjacency Matrix**: This representation itself takes O(V²) space, separate from BFS's own O(V) space.

| Operation        | Time           | Space          |
| ---------------- | -------------- | -------------- |
| BFS traversal    | O(V + E)       | O(V)           |
| Shortest path    | O(V + E)       | O(V)           |
| Grid BFS         | O(rows × cols) | O(rows × cols) |
| Multi-source BFS | O(V + E)       | O(V)           |

Space includes both visited set and queue.

---

## Common Mistakes

```python
# ❌ WRONG: Marking visited when DEQUEUING (too late!)
# Why it's wrong: Between enqueueing and dequeuing, the SAME node
# can be added to the queue multiple times by different neighbors.
# This wastes time (TLE) and can use O(E) queue space instead of O(V).
while queue:
    node = queue.popleft()
    visited.add(node)        # Too late! Duplicates already in queue
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            queue.append(neighbor)

# ✅ CORRECT: Mark visited when ENQUEUEING
while queue:
    node = queue.popleft()
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            visited.add(neighbor)  # Mark visited IMMEDIATELY
            queue.append(neighbor)


# ❌ WRONG: Using list as queue (O(n) pop from front)
queue = [start]
while queue:
    node = queue.pop(0)  # O(n) — shifts all elements left!

# ✅ CORRECT: Use collections.deque
from collections import deque
queue = deque([start])
while queue:
    node = queue.popleft()  # O(1) — doubly-linked list


# ❌ WRONG: Forgetting to handle disconnected graphs
def count_components(graph, n):
    visited = set()
    bfs(graph, 0)  # Only visits the component containing node 0!

# ✅ CORRECT: Iterate over all nodes
for node in range(n):
    if node not in visited:
        bfs(graph, node)


# ❌ WRONG: Not checking if start node exists / graph is empty
# ✅ CORRECT: Guard against edge cases
def bfs_safe(graph: dict[int, list[int]], start: int) -> list[int]:
    if start not in graph:
        return []
    # ... rest of BFS
```

---

## Step-by-Step BFS Trace with ASCII Visualization

**Graph for demonstration:**

```
        0
       /|\
      1 2 3
     /|   |
    4 5   6
```

Adjacency list: `{0:[1,2,3], 1:[0,4,5], 2:[0], 3:[0,6], 4:[1], 5:[1], 6:[3]}`

**Complete BFS trace from node 0:**

```
INITIAL STATE:
Queue: [0]
Visited: {0}
Result: []

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 1: Dequeue 0                                         ║
╚══════════════════════════════════════════════════════════════════╝
  Processing: 0
  Neighbors of 0: [1, 2, 3]

  Check 1: not visited → add to queue, mark visited
  Check 2: not visited → add to queue, mark visited
  Check 3: not visited → add to queue, mark visited

  Queue: [1, 2, 3]
  Visited: {0, 1, 2, 3}
  Result: [0]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 2: Dequeue 1                                         ║
╚══════════════════════════════════════════════════════════════════╝
  Processing: 1
  Neighbors of 1: [0, 4, 5]

  Check 0: already visited → skip
  Check 4: not visited → add to queue, mark visited
  Check 5: not visited → add to queue, mark visited

  Queue: [2, 3, 4, 5]
  Visited: {0, 1, 2, 3, 4, 5}
  Result: [0, 1]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 3: Dequeue 2                                         ║
╚══════════════════════════════════════════════════════════════════╝
  Processing: 2
  Neighbors of 2: [0]

  Check 0: already visited → skip

  Queue: [3, 4, 5]
  Visited: {0, 1, 2, 3, 4, 5}
  Result: [0, 1, 2]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 4: Dequeue 3                                         ║
╚══════════════════════════════════════════════════════════════════╝
  Processing: 3
  Neighbors of 3: [0, 6]

  Check 0: already visited → skip
  Check 6: not visited → add to queue, mark visited

  Queue: [4, 5, 6]
  Visited: {0, 1, 2, 3, 4, 5, 6}
  Result: [0, 1, 2, 3]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATIONS 5-7: Dequeue 4, 5, 6                                ║
╚══════════════════════════════════════════════════════════════════╝
  All neighbors already visited
  Queue becomes empty

FINAL RESULT: [0, 1, 2, 3, 4, 5, 6]
Distance from 0: {0:0, 1:1, 2:1, 3:1, 4:2, 5:2, 6:2}
```

**Level visualization:**

```
Level 0:        0           (distance 0)
               /|\
Level 1:      1 2 3         (distance 1)
             /|   |
Level 2:    4 5   6         (distance 2)
```

---

## Complexity Derivation with Proof

**Time Complexity: O(V + E)**

```
Proof:
1. Each vertex is enqueued at most once
   - We mark visited BEFORE enqueueing
   - Visited check prevents re-enqueueing
   - Therefore: exactly V enqueue operations

2. Each vertex is dequeued exactly once
   - Once dequeued, never re-added (visited)
   - Therefore: exactly V dequeue operations

3. For each vertex, we examine all its neighbors
   - When processing vertex v, we look at all edges from v
   - Each edge (u,v) is examined twice in undirected graph
     (once from u's perspective, once from v's)
   - Therefore: O(E) edge examinations total

4. Total: O(V) + O(V) + O(E) = O(V + E)
```

**Space Complexity: O(V)**

```
Proof:
1. Visited set: stores up to V vertices → O(V)
2. Queue: at most all vertices at once → O(V)
   (worst case: star graph where center connects to all)
3. No recursion, so no call-stack space
4. Total: O(V) + O(V) = O(V)
```

**Why BFS is optimal for unweighted shortest path:**

```
Theorem: BFS finds shortest path in unweighted graphs.

Proof by induction on distance d:

Base case (d=0): Source node s has distance 0. ✓

Inductive step: Assume all nodes at distance d are correct.
For any node v at distance d+1:
- There exists a node u at distance d with edge (u,v)
- u is processed (dequeued) before v (by FIFO property)
- When u is processed, v is added to queue with dist[v] = d+1
- No shorter path exists (induction hypothesis)
- Therefore, v has correct distance d+1. ✓

By induction, all distances are correct. □
```

---

## Edge Cases

```python
# 1. Single node graph
graph = {0: []}
bfs(graph, 0)  # [0]

# 2. Disconnected graph — must iterate over all nodes (see bfs_all_components)

# 3. Start node not in graph — handle gracefully with `graph.get(node, [])` or check `if start not in graph`

# 4. Cycle in graph — visited set prevents infinite loop

# 5. Start equals end — return immediately with distance 0

# 6. Empty graph / Start node not found
# If using `graph[node]`, it raises KeyError. Our template uses `graph.get(node, [])`
# which avoids the crash, but will return `[start]` even if `start` isn't in the graph.
# If you want to strictly return `[]` for missing start nodes, add an explicit check:
graph: dict[int, list[int]] = {}
bfs_safe(graph, 0)  # []

# 7. Self-loops — visited set handles these automatically
graph = {0: [0, 1], 1: [0]}
bfs(graph, 0)  # [0, 1] — node 0 is already visited, self-loop skipped
```

---

## Interview Tips

1. **Always use `deque`**: `queue.popleft()` is O(1), `list.pop(0)` is O(n)
2. **Mark visited when enqueueing**: Prevents duplicates in queue — this is the #1 BFS bug
3. **Handle disconnected graphs**: Iterate over all nodes
4. **Know level-order pattern**: Process by level using the `len(queue)` snapshot trick
5. **Draw the traversal**: Show the interviewer you understand the processing order
6. **State assumptions**: Tell the interviewer whether the graph is directed/undirected, connected/disconnected, and whether it has cycles
7. **Mention early termination**: For shortest-path problems, return as soon as you find the target (don't drain the entire queue)

---

## Practice Problems

Problems are ordered easy → medium → hard. Master each level before moving on.

| #   | Problem (LeetCode)                        | Difficulty | Key Pattern          | Hint                                                                                    |
| --- | ----------------------------------------- | ---------- | -------------------- | --------------------------------------------------------------------------------------- |
| 1   | **733. Flood Fill**                       | Easy       | Basic grid BFS       | Start BFS from the given pixel. Only spread to neighbors with the same original color.  |
| 2   | **102. Binary Tree Level Order Traversal**| Medium     | Level-order BFS      | Tree traversal, use `len(queue)` to process level by level.                             |
| 3   | **200. Number of Islands**                | Medium     | Multi-component BFS  | Iterate every cell; if it's `'1'` and unvisited, run BFS to mark the whole island.      |
| 4   | **994. Rotting Oranges**                  | Medium     | Multi-source BFS     | Seed queue with ALL rotten oranges at time 0. Each BFS level = 1 minute.                |
| 5   | **542. 01 Matrix**                        | Medium     | Multi-source BFS     | Reverse thinking: start BFS from all `0` cells simultaneously.                          |
| 6   | **1091. Shortest Path in Binary Matrix**  | Medium     | Shortest path (grid) | 8-directional BFS. Track distance. Return -1 if blocked.                                |
| 7   | **863. All Nodes Distance K in Binary Tree**| Medium   | Graph from Tree      | Build parent pointers to convert tree to graph, then BFS from target.                   |
| 8   | **127. Word Ladder**                      | Hard       | Implicit graph BFS   | Each word is a node. Neighbors differ by 1 letter. Use wildcard patterns `h*t`.         |
| 9   | **864. Shortest Path to Get All Keys**    | Hard       | BFS with State       | Queue stores `(r, c, keys_bitmask)`. Same cell can be visited with different keys.      |
| 10  | **126. Word Ladder II**                   | Hard       | BFS + DFS            | BFS to find shortest path distances, then DFS to reconstruct all valid shortest paths.  |
| 11  | **1368. Min Cost to Make Valid Path**     | Hard       | 0-1 BFS              | Use a `deque`. Cost 0 moves go to `appendleft`, cost 1 moves go to `append`.            |

---

## Key Takeaways

1. **BFS uses a queue**: FIFO ordering gives level-by-level traversal
2. **Shortest path in unweighted**: BFS guarantees minimum hops
3. **Mark visited when enqueueing**: Critical for correctness and performance
4. **Level-order trick**: Snapshot `len(queue)` at each level, then dequeue exactly that many
5. **Multi-source**: Initialize queue with all sources at distance 0
6. **Use `deque`**: Never use `list.pop(0)` — it's O(n) per operation
7. **BFS vs DFS**: BFS for shortest path and level-order; DFS for exhaustive search, cycle detection, and lower memory on deep graphs

---

## Next: [03-dfs-basics.md](./03-dfs-basics.md)

Learn DFS traversal, recursive and iterative approaches.
