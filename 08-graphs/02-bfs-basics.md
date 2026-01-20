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

**Key insight - The Queue is Everything**:
- FIFO (First-In-First-Out) ensures we exhaust all distance-k nodes before distance-(k+1)
- Using a stack would make it DFS (depth-first, not breadth-first)
- Using a priority queue would make it Dijkstra (weighted shortest path)

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
- **You're detecting cycles** → DFS with three colors is cleaner for directed graphs

**BFS is overkill when:**
- Simple reachability check → DFS is equally valid and often simpler
- Tree traversal → Specialized tree algorithms may be cleaner
- Graph has special structure (DAG) → Topological sort may be better

**Common mistake scenarios:**
- Using BFS on weighted graphs expecting shortest path → Wrong answer
- Using list instead of deque → O(n) popleft() kills performance
- Marking visited when dequeuing → Duplicates in queue, TLE

---

## Interview Context

BFS is essential because:

1. **Shortest path in unweighted graphs**: The go-to algorithm
2. **Level-order traversal**: Process nodes layer by layer
3. **Multi-source BFS**: Handle problems with multiple starting points
4. **Foundation for Dijkstra**: Same pattern with priority queue

BFS appears in almost every FANG+ interview loop involving graphs or grids.

---

## Core Concept: How BFS Works

BFS explores vertices level by level using a **queue**:
1. Start from source, add to queue
2. Process current vertex, add unvisited neighbors to queue
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

---

## BFS Template (Must Know!)

```python
from collections import deque

def bfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    Basic BFS traversal.

    Time: O(V + E)
    Space: O(V) for visited set and queue
    """
    visited = set([start])
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
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

    Time: O(V + E)
    Space: O(V)

    Returns -1 if no path exists.
    """
    if start == end:
        return 0

    visited = set([start])
    queue = deque([(start, 0)])  # (node, distance)

    while queue:
        node, dist = queue.popleft()

        for neighbor in graph[node]:
            if neighbor == end:
                return dist + 1

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
    Find shortest path and return the actual path.

    Time: O(V + E)
    Space: O(V)
    """
    if start == end:
        return [start]

    visited = set([start])
    queue = deque([start])
    parent = {start: None}  # Track path

    while queue:
        node = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)

                if neighbor == end:
                    # Reconstruct path
                    path = []
                    current = end
                    while current is not None:
                        path.append(current)
                        current = parent[current]
                    return path[::-1]

    return []  # No path


# Usage
graph = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}
print(shortest_path_with_path(graph, 0, 3))  # [0, 1, 3] or [0, 2, 3]
```

---

## Level-Order BFS (Track Levels)

```python
from collections import deque

def bfs_by_level(graph: dict[int, list[int]],
                  start: int) -> list[list[int]]:
    """
    BFS with explicit level tracking.
    Returns nodes grouped by level.

    Time: O(V + E)
    Space: O(V)
    """
    visited = set([start])
    queue = deque([start])
    levels = []

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node)

            for neighbor in graph[node]:
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

def grid_bfs(grid: list[list[int]],
             start: tuple[int, int]) -> set[tuple[int, int]]:
    """
    BFS on a grid.

    Time: O(rows × cols)
    Space: O(rows × cols)
    """
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

    return visited
```

---

## Multi-Source BFS

Start from multiple sources simultaneously. All sources are at distance 0.

```python
from collections import deque

def multi_source_bfs(grid: list[list[int]],
                      sources: list[tuple[int, int]]) -> list[list[int]]:
    """
    BFS from multiple sources.
    Returns distance grid where each cell has min distance to any source.

    Time: O(rows × cols)
    Space: O(rows × cols)

    Example use: Rotting oranges, 01 Matrix
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Distance grid, -1 = unvisited
    dist = [[-1] * cols for _ in range(rows)]

    queue = deque()
    for r, c in sources:
        dist[r][c] = 0
        queue.append((r, c))

    while queue:
        r, c = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if (0 <= nr < rows and 0 <= nc < cols and
                dist[nr][nc] == -1 and grid[nr][nc] == 1):
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

    Time: O(V + E)
    Space: O(V)
    """
    visited = set()
    components = []

    for node in range(n):
        if node not in visited:
            # BFS for this component
            component = []
            queue = deque([node])
            visited.add(node)

            while queue:
                curr = queue.popleft()
                component.append(curr)

                for neighbor in graph[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            components.append(component)

    return components
```

---

## When to Use BFS vs DFS

| Scenario | Use BFS | Use DFS |
|----------|---------|---------|
| Shortest path (unweighted) | ✓ | ✗ |
| Level-order traversal | ✓ | ✗ |
| Closest node to source | ✓ | ✗ |
| Explore all paths | ✗ | ✓ |
| Cycle detection | Either | ✓ (simpler) |
| Topological sort | ✓ (Kahn's) | ✓ (reverse post-order) |
| Memory constrained (deep graph) | ✗ | ✓ |

---

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| BFS traversal | O(V + E) | O(V) |
| Shortest path | O(V + E) | O(V) |
| Grid BFS | O(rows × cols) | O(rows × cols) |
| Multi-source BFS | O(V + E) | O(V) |

Space includes both visited set and queue.

---

## Common Mistakes

```python
# WRONG: Adding to visited when processing
while queue:
    node = queue.popleft()
    visited.add(node)  # Too late! May add duplicates to queue
    for neighbor in graph[node]:
        if neighbor not in visited:
            queue.append(neighbor)

# CORRECT: Add to visited when enqueueing
while queue:
    node = queue.popleft()
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)  # Mark visited immediately
            queue.append(neighbor)


# WRONG: Using list as queue
queue = [start]
while queue:
    node = queue.pop(0)  # O(n) operation!

# CORRECT: Use deque
from collections import deque
queue = deque([start])
while queue:
    node = queue.popleft()  # O(1)


# WRONG: Forgetting to handle disconnected graphs
def count_components(graph, n):
    visited = set()
    bfs(graph, 0)  # Only visits component containing 0!

# CORRECT: Iterate all nodes
for node in range(n):
    if node not in visited:
        bfs(graph, node)
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
║ ITERATION 1: Dequeue 0                                           ║
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
║ ITERATION 2: Dequeue 1                                           ║
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
║ ITERATION 3: Dequeue 2                                           ║
╚══════════════════════════════════════════════════════════════════╝
  Processing: 2
  Neighbors of 2: [0]

  Check 0: already visited → skip

  Queue: [3, 4, 5]
  Visited: {0, 1, 2, 3, 4, 5}
  Result: [0, 1, 2]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 4: Dequeue 3                                           ║
╚══════════════════════════════════════════════════════════════════╝
  Processing: 3
  Neighbors of 3: [0, 6]

  Check 0: already visited → skip
  Check 6: not visited → add to queue, mark visited

  Queue: [4, 5, 6]
  Visited: {0, 1, 2, 3, 4, 5, 6}
  Result: [0, 1, 2, 3]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATIONS 5-7: Dequeue 4, 5, 6                                  ║
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
3. No recursion, so no stack space
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

# 2. Disconnected graph
# Must iterate over all nodes

# 3. Start node not in graph
# Handle gracefully

# 4. Cycle in graph
# Visited set prevents infinite loop

# 5. Start equals end
# Return immediately with distance 0
```

---

## Interview Tips

1. **Always use deque**: `queue.popleft()` is O(1), `list.pop(0)` is O(n)
2. **Mark visited when enqueueing**: Prevents duplicates in queue
3. **Handle disconnected graphs**: Iterate over all nodes
4. **Know level-order pattern**: Process by level using size trick
5. **Draw the traversal**: Show interviewer you understand the order

---

## Practice Problems

| # | Problem | Difficulty | Key Pattern |
|---|---------|------------|-------------|
| 1 | Flood Fill | Easy | Basic grid BFS |
| 2 | Number of Islands | Medium | Multi-component BFS |
| 3 | Shortest Path in Binary Matrix | Medium | Shortest path |
| 4 | Rotting Oranges | Medium | Multi-source BFS |
| 5 | Word Ladder | Hard | Implicit graph BFS |
| 6 | 01 Matrix | Medium | Multi-source BFS |

---

## Key Takeaways

1. **BFS uses a queue**: FIFO ordering gives level-by-level traversal
2. **Shortest path in unweighted**: BFS guarantees minimum hops
3. **Mark visited when enqueueing**: Critical for correctness
4. **Level-order trick**: Process `len(queue)` nodes per level
5. **Multi-source**: Initialize queue with all sources at distance 0

---

## Next: [03-dfs-basics.md](./03-dfs-basics.md)

Learn DFS traversal, recursive and iterative approaches.
