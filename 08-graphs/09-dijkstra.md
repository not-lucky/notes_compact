# Dijkstra's Algorithm

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md), [07-heaps-priority-queues](../07-heaps-priority-queues/README.md)

## Building Intuition

**The Greedy Expansion Mental Model**: Imagine you're at the center of a city and roads have different lengths. To find the shortest path to everywhere:

1. First, explore roads directly connected to you (shortest first)
2. From each new intersection, discover new roads
3. Always expand from the closest unexplored point
4. Eventually, you've found the shortest path to everywhere

```
     2
  A ←── B
  │     │
 1│     │3
  ↓     ↓
  C ──→ D
     1

From A: dist = {A:0, B:∞, C:∞, D:∞}
Step 1: A is closest (0), explore A→C (1), A←B (can't, directed)
        dist = {A:0, C:1, B:∞, D:∞}
Step 2: C is closest (1), explore C→D (1+1=2)
        dist = {A:0, C:1, D:2, B:∞}
Step 3: D is closest (2), no outgoing
Step 4: B unreachable (directed graph)
```

**Why the greedy choice works**:

- We always process the node with smallest known distance
- All edge weights are non-negative
- Therefore, no later path through unprocessed nodes can be shorter
- This is the **greedy choice property** that makes Dijkstra correct
- Dijkstra also relies on **optimal substructure**: every subpath of a shortest path is itself a shortest path

**What is "relaxation"?**

Relaxation is the core operation in Dijkstra's. When we process a node `u` and look at an edge `u → v` with weight `w`, we ask: "Is the path through `u` shorter than what we currently know for `v`?"

```
if dist[u] + w < dist[v]:
    dist[v] = dist[u] + w    # "relax" the edge — tighten the upper bound
```

The name comes from the idea that `dist[v]` starts as a loose upper bound (infinity) and we progressively *relax* (tighten) it until it equals the true shortest distance.

### The Formal Proof of Greedy Correctness

**Theorem**: When Dijkstra's algorithm extracts a vertex $u$ from the min-heap, its shortest path distance from the source $s$ is finalized. The distance value `dist[u]` equals the true shortest distance $\delta(s, u)$.

**Proof by Contradiction**:
1. **Assumption**: Suppose for contradiction that `dist[u]` is *not* the true shortest distance when $u$ is extracted. Therefore, the true shortest path must be shorter: $\delta(s, u) < \text{dist}[u]$.
2. Let $P$ be the actual true shortest path from the source $s$ to $u$.
3. As we trace along path $P$ from $s$, let $y$ be the first vertex on $P$ that has *not yet* been extracted from the heap (it's still in the queue). Let $x$ be the vertex just before $y$ on path $P$ (which has been extracted).
4. Because $x$ was extracted, we relaxed its edges, which updated $y$'s distance. Thus, `dist[y]` represents the shortest path from $s$ to $y$ using only extracted vertices. This value is optimal for subpath $s \to y$: $\text{dist}[y] = \delta(s, y)$.
5. Since all edge weights in the graph are non-negative, any additional edges beyond $y$ to reach $u$ can only add more distance (or 0). Therefore: $\delta(s, y) \le \delta(s, u)$.
6. Combining step 4 and 5 gives: $\text{dist}[y] \le \delta(s, u)$.
7. From our initial assumption in step 1, $\delta(s, u) < \text{dist}[u]$. Substituting this in gives: $\text{dist}[y] < \text{dist}[u]$.
8. **The Contradiction**: If $\text{dist}[y] < \text{dist}[u]$, the min-heap should have popped $y$ *before* $u$! But the algorithm chose to pop $u$. This contradicts how min-heaps work.
9. **Conclusion**: Therefore, our assumption in step 1 is false. When $u$ is extracted, `dist[u]` must equal the true shortest distance. $\blacksquare$

> **Key Takeaway**: This proof breaks completely if negative weights exist because step 5 ($\delta(s, y) \le \delta(s, u)$) is no longer true. A negative edge after $y$ could make the path to $u$ shorter!

**The priority queue insight**:

- BFS uses a queue → processes by discovery order
- Dijkstra uses a min-heap → processes by distance order
- Same algorithm structure, different ordering!

**Complexity derivation**:

```
Each vertex: extracted from heap once → O(V log V)
Each edge: may add entry to heap once → O(E log V)
Total: O((V + E) log V)

Why log V? Heap operations on V elements.
```

---

## When NOT to Use

**Don't use Dijkstra when:**

- **Negative edge weights exist** → Dijkstra fails! Use Bellman-Ford
- **All edges have same weight** → BFS is simpler and faster O(V+E)
- **Need to count stops/hops** → Modified Dijkstra or BFS needed
- **Finding longest path** → NP-hard problem, different approach needed

**Dijkstra is overkill when:**

- Unweighted graph → BFS is O(V+E) vs O((V+E)log V)
- Very small graph → Simple O(V²) approach may be clearer
- Single target → Can terminate early (optimization)

**Common mistake scenarios:**

- Applying to graphs with negative weights → Wrong answers
- Not skipping outdated heap entries → Correctness issue or TLE
- Using visited set incorrectly → May skip better paths for variants

**The negative weight trap — why Dijkstra fails:**

```
    0 ──1──→ 1
    │        │
    3       -2
    │        │
    ↓        ↓
    2 ←─────

Dijkstra from 0: Visits 1 first (dist=1), then 2 (dist=3)
But actual shortest to 2: 0→1→2 = 1+(-2) = -1 < 3
Dijkstra already "finalized" 2 at dist=3, misses the better path!
```

---

## Interview Context

Dijkstra's algorithm is essential because:

1. **Weighted shortest paths**: BFS doesn't work when edges have different costs
2. **Real applications**: Maps, routing, network delay
3. **Heap practice**: Priority queue is central to the algorithm
4. **FANG+ frequency**: Network Delay Time is a common problem

If edges have positive weights, Dijkstra is the answer.

---

## Core Concept

Dijkstra's algorithm finds the shortest path from a source to all other vertices in a weighted graph with **non-negative edge weights**.

**Greedy strategy**: Always process the unvisited vertex with the smallest known distance.

```
Graph:
    0 --2-- 1
    |       |
    4       1
    |       |
    2 --1-- 3

Shortest from 0:
  to 1: 2 (direct)
  to 2: 4 (direct)
  to 3: 3 (0→1→3, cost 2+1=3)
```

---

## Dijkstra's Algorithm Template

### Python

```python
import heapq
from collections import defaultdict


def dijkstra(n: int, edges: list[list[int]], source: int) -> list[float]:
    """
    Standard Dijkstra's shortest path from source to all nodes.

    Args:
        n: number of nodes (0-indexed)
        edges: list of [u, v, weight] (undirected)
        source: starting node

    Returns:
        dist: list where dist[i] = shortest distance from source to i
              (float('inf') if unreachable)

    Time:  O((V + E) log V)
    Space: O(V + E)
    """
    # Build adjacency list
    graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))  # remove for directed graphs

    # Initialize distances to infinity, source to 0
    dist = [float('inf')] * n
    dist[source] = 0

    # Min-heap of (distance, node)
    heap: list[tuple[float, int]] = [(0, source)]

    while heap:
        d, node = heapq.heappop(heap)

        # Skip outdated entries: if we already found a shorter path
        # to this node, this heap entry is stale
        if d > dist[node]:
            continue

        # Relax all edges from this node
        for neighbor, weight in graph[node]:
            new_dist = d + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return dist
```

---

## Visual Walkthrough

```
Graph:
    0 --2-- 1
    |       |
    4       1
    |       |
    2 --1-- 3

Initial: dist = [0, ∞, ∞, ∞], heap = [(0, 0)]

Step 1: Pop (0, 0)
        Check neighbors: 1 (cost 2), 2 (cost 4)
        Update: dist = [0, 2, 4, ∞]
        heap = [(2, 1), (4, 2)]

Step 2: Pop (2, 1)
        Check neighbors: 0 (cost 2), 3 (cost 1)
        0: 2+2=4 > 0, skip
        3: 2+1=3 < ∞, update
        dist = [0, 2, 4, 3]
        heap = [(3, 3), (4, 2)]

Step 3: Pop (3, 3)
        Check neighbors: 1 (cost 1), 2 (cost 1)
        1: 3+1=4 > 2, skip
        2: 3+1=4 = 4, no improvement
        dist = [0, 2, 4, 3]
        heap = [(4, 2)]

Step 4: Pop (4, 2)
        Check neighbors: 0 (cost 4), 3 (cost 1)
        0: 4+4=8 > 0, skip
        3: 4+1=5 > 3, skip
        Done!

Final: dist = [0, 2, 4, 3]
```

---

## Path Reconstruction

```python
import heapq
from collections import defaultdict


def dijkstra_with_path(
    n: int,
    edges: list[list[int]],
    source: int,
    target: int,
) -> tuple[float, list[int]]:
    """
    Dijkstra's with path reconstruction.

    Returns:
        (distance, path) — path is [] and distance is -1 if unreachable.
    """
    graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    dist = [float('inf')] * n
    dist[source] = 0
    parent: dict[int, int | None] = {source: None}

    heap: list[tuple[float, int]] = [(0, source)]

    while heap:
        d, node = heapq.heappop(heap)

        # Early termination: target found
        if node == target:
            break

        if d > dist[node]:
            continue

        for neighbor, weight in graph[node]:
            new_dist = d + weight

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                parent[neighbor] = node
                heapq.heappush(heap, (new_dist, neighbor))

    if dist[target] == float('inf'):
        return -1, []

    # Reconstruct path by walking parent pointers backward
    path: list[int] = []
    current: int | None = target
    while current is not None:
        path.append(current)
        current = parent[current]

    return dist[target], path[::-1]
```

---

## Network Delay Time (Classic Problem)

**FANG Context**: This is practically the "Hello World" of weighted graphs for FANG interviews. Often asked as a warm-up or screening question because it perfectly maps to standard Dijkstra. Usually dressed up as network packets, disease spread, or messages propagating across servers.

```python
import heapq
from collections import defaultdict


def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    """
    Find time for signal to reach all nodes from node k.
    LeetCode 743: Network Delay Time.

    times[i] = [u, v, w]: directed edge from u to v with time w
    n: number of nodes (1-indexed)
    k: starting node

    Returns: minimum time to reach all nodes, or -1 if impossible

    Time:  O((V + E) log V)
    Space: O(V + E)
    """
    graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    # Use dict for 1-indexed nodes
    dist: dict[int, float] = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0

    heap: list[tuple[float, int]] = [(0, k)]

    while heap:
        d, node = heapq.heappop(heap)

        # Skip stale entries
        if d > dist[node]:
            continue

        for neighbor, weight in graph[node]:
            new_dist = d + weight

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    max_dist = max(dist.values())
    return int(max_dist) if max_dist < float('inf') else -1
```

---

## Path With Minimum Effort (Grid Dijkstra)

Dijkstra isn't just for sum of weights! In this variation, the "cost" of a path is the **maximum absolute difference** in heights between two consecutive cells along the path. We want to find the path that minimizes this maximum effort.

This is a classic "Min-Max Path" problem. We can still use Dijkstra because the cost of a path only monotonically increases (or stays the same) as we add edges.

```python
import heapq

def minimum_effort_path(heights: list[list[int]]) -> int:
    """
    Find path from top-left to bottom-right minimizing max effort.
    LeetCode 1631: Path With Minimum Effort.
    
    Effort of edge (u, v) = abs(heights[u] - heights[v])
    Effort of path = max(effort of all edges on path)
    
    Time: O(R*C log(R*C)) where R, C are grid dimensions
    Space: O(R*C)
    """
    ROWS, COLS = len(heights), len(heights[0])
    
    # max_effort[r][c] = min effort needed to reach (r, c)
    max_effort = [[float('inf')] * COLS for _ in range(ROWS)]
    max_effort[0][0] = 0
    
    # Min-heap of (current_max_effort, r, c)
    heap: list[tuple[float, int, int]] = [(0, 0, 0)]
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while heap:
        effort, r, c = heapq.heappop(heap)
        
        # Reached destination! Because it's a min-heap, this is the 
        # optimal (minimum possible maximum effort) path.
        if r == ROWS - 1 and c == COLS - 1:
            return int(effort)
            
        # Skip stale entries
        if effort > max_effort[r][c]:
            continue
            
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                # Effort for this specific step
                step_effort = abs(heights[r][c] - heights[nr][nc])
                
                # New max effort for the path ending at (nr, nc)
                new_max_effort = max(effort, step_effort)
                
                # Relaxation: if we found a path with a smaller max effort
                if new_max_effort < max_effort[nr][nc]:
                    max_effort[nr][nc] = new_max_effort
                    heapq.heappush(heap, (new_max_effort, nr, nc))
                    
    return -1
```

---

## Cheapest Flights Within K Stops

Modified Dijkstra with stop constraint. This is **not** standard Dijkstra — the greedy property doesn't hold because a costlier path with fewer stops may lead to a cheaper final answer. We must allow revisiting nodes if we arrive with fewer stops.

```python
import heapq
from collections import defaultdict


def find_cheapest_price(
    n: int,
    flights: list[list[int]],
    src: int,
    dst: int,
    k: int,
) -> int:
    """
    Find cheapest price from src to dst with at most k stops.
    LeetCode 787: Cheapest Flights Within K Stops.

    Time:  O(E * K * log(E * K)) worst case
    Space: O(V * K)

    Note: Regular Dijkstra doesn't work here because we need
    to track the number of stops, not just minimum distance.
    A more expensive path with fewer stops might lead to a
    cheaper overall route.
    """
    graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, price in flights:
        graph[u].append((v, price))

    # (cost, node, stops_used)
    heap: list[tuple[int, int, int]] = [(0, src, 0)]

    # best[node] = fewest stops used to reach node with acceptable cost
    # We only skip if we've reached this node with fewer-or-equal stops
    best_stops: dict[int, int] = {}

    while heap:
        cost, node, stops = heapq.heappop(heap)

        # Reached destination — first pop is cheapest due to min-heap
        if node == dst:
            return cost

        # Skip if we've already visited this node with fewer stops
        if node in best_stops and best_stops[node] <= stops:
            continue
        best_stops[node] = stops

        # Can't take any more flights
        if stops > k:
            continue

        for neighbor, price in graph[node]:
            heapq.heappush(heap, (cost + price, neighbor, stops + 1))

    return -1
```

---

## Why Dijkstra Fails with Negative Weights

In theory, Dijkstra's algorithm assumes that once a node is popped from the min-heap, its shortest path is final. Negative edges break this assumption.

```text
Directed Graph:
    0 --1-→ 1
     \     ↗
      3  -5
       \ /
        2
```

**Trace from node 0:**
1. **Pop 0**: Updates `dist[1]=1`, `dist[2]=3`.
2. **Pop 1** (dist=1): Since 1 is the smallest in the heap, the greedy property states `dist[1]=1` is final.
3. **Pop 2** (dist=3): Edge 2→1 has weight -5. The new path 0→2→1 costs `3 + (-5) = -2`.

**What happens next depends on the implementation:**
- **Strict Dijkstra (with `visited` set)**: Ignores the update to node 1 because it has already been visited/finalized. The algorithm finishes and returns `dist[1]=1`, which is **wrong**.
- **Modern Queue Template (checking `new_dist < dist[neighbor]`)**: Updates `dist[1]=-2` and pushes node 1 back into the heap. It eventually finds the correct answer, BUT it re-evaluates a "finalized" node. In a graph with many negative edges, this causes a cascade of re-evaluations, degrading time complexity to an **exponential $O(2^V)$ worst-case**. Moreover, if there is a negative cycle, it loops infinitely!

**The rule**: The greedy assumption — "once popped, it's final" — is violated because negative edges can retroactively create shorter paths. Always use **Bellman-Ford** if negative weights exist.

---

## Complexity Analysis

| Implementation   | Time             | Space  | Notes                                 |
| ---------------- | ---------------- | ------ | ------------------------------------- |
| Binary heap      | O((V + E) log V) | O(V+E) | Standard for interviews, most common. |
| Fibonacci heap   | O(E + V log V)   | O(V+E) | Theoretically faster for dense graphs.|
| Adjacency matrix | O(V²)            | O(V²)  | Good for very dense graphs (E ≈ V²).  |

**Deep Dive: Binary Heap vs Fibonacci Heap**

- **Binary Heap**: Finding the minimum takes $O(\log V)$, and updating distances (inserting new ones in the standard implementation, or `decrease-key` if supported) takes $O(\log V)$. This happens up to $E$ times, yielding $O((V+E)\log V)$ overall. It is practical and cache-friendly, making it the standard choice in interviews and production code.
- **Fibonacci Heap**: Extracting the minimum is $O(\log V)$ amortized (done $V$ times). However, `decrease-key` is strictly $O(1)$ amortized (done up to $E$ times). The total theoretical time is improved to $O(E + V \log V)$. While technically faster for dense graphs, Fibonacci heaps have huge constant factors, terrible cache locality, and are incredibly complex to implement. You will **never** need to write one in an interview, but mentioning the theoretical bound shows deep fundamental knowledge.

---

## Common Mistakes

```python
# WRONG: Not skipping outdated entries
while heap:
    d, node = heapq.heappop(heap)
    # Processing without checking if d > dist[node] means
    # we process the same node multiple times with stale distances!

# CORRECT: Skip if we already found a better path
while heap:
    d, node = heapq.heappop(heap)
    if d > dist[node]:
        continue  # Stale entry — already found shorter path
    # Process...


# WRONG: Using visited set (may skip better paths in some variants)
visited = set()
while heap:
    d, node = heapq.heappop(heap)
    if node in visited:
        continue
    visited.add(node)
    # This works for basic Dijkstra but fails for variations
    # like "K stops" where you may need to revisit a node

# For basic Dijkstra, both approaches work.
# The distance-check pattern is more general and idiomatic.


# WRONG: Not handling unreachable nodes
return max(dist)  # May return infinity!

# CORRECT: Check for infinity
max_dist = max(dist)
return max_dist if max_dist < float('inf') else -1
```

---

## Step-by-Step Dijkstra Trace with ASCII Visualization

**Weighted graph for demonstration:**

```
        (0)
       / | \
      4  2  1
     /   |   \
   (1)  (2)  (3)
     \   |   /
      1  3  2
       \ | /
        (4)
```

Edges: `[(0,1,4), (0,2,2), (0,3,1), (1,4,1), (2,4,3), (3,4,2)]`

**Complete Dijkstra trace from node 0:**

```
INITIAL STATE:
Distances: {0: 0, 1: ∞, 2: ∞, 3: ∞, 4: ∞}
Min-Heap: [(0, node 0)]
Processed: {}

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 1: Pop (0, node 0) — smallest distance               ║
╚══════════════════════════════════════════════════════════════════╝
  dist[0] = 0 (final, because smallest in heap)

  Relaxing edges from node 0:
    Edge 0→1 (weight 4): 0 + 4 = 4 < ∞  → Update dist[1] = 4, push (4, 1)
    Edge 0→2 (weight 2): 0 + 2 = 2 < ∞  → Update dist[2] = 2, push (2, 2)
    Edge 0→3 (weight 1): 0 + 1 = 1 < ∞  → Update dist[3] = 1, push (1, 3)

  Distances: {0: 0, 1: 4, 2: 2, 3: 1, 4: ∞}
  Min-Heap: [(1, 3), (2, 2), (4, 1)]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 2: Pop (1, node 3) — smallest distance               ║
╚══════════════════════════════════════════════════════════════════╝
  dist[3] = 1 (final)

  Relaxing edges from node 3:
    Edge 3→4 (weight 2): 1 + 2 = 3 < ∞  → Update dist[4] = 3, push (3, 4)

  Distances: {0: 0, 1: 4, 2: 2, 3: 1, 4: 3}
  Min-Heap: [(2, 2), (3, 4), (4, 1)]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 3: Pop (2, node 2) — smallest distance               ║
╚══════════════════════════════════════════════════════════════════╝
  dist[2] = 2 (final)

  Relaxing edges from node 2:
    Edge 2→4 (weight 3): 2 + 3 = 5 > 3  → No update (current path better)

  Distances: {0: 0, 1: 4, 2: 2, 3: 1, 4: 3}
  Min-Heap: [(3, 4), (4, 1)]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 4: Pop (3, node 4) — smallest distance               ║
╚══════════════════════════════════════════════════════════════════╝
  dist[4] = 3 (final)

  Node 4 has no outgoing edges.

  Distances: {0: 0, 1: 4, 2: 2, 3: 1, 4: 3}
  Min-Heap: [(4, 1)]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 5: Pop (4, node 1)                                    ║
╚══════════════════════════════════════════════════════════════════╝
  dist[1] = 4 (final)

  Relaxing edges from node 1:
    Edge 1→4 (weight 1): 4 + 1 = 5 > 3  → No update

  Min-Heap: [] (empty)

FINAL DISTANCES: {0: 0, 1: 4, 2: 2, 3: 1, 4: 3}

Shortest paths:
  0 → 0: distance 0 (source)
  0 → 1: distance 4 (path: 0 → 1)
  0 → 2: distance 2 (path: 0 → 2)
  0 → 3: distance 1 (path: 0 → 3)
  0 → 4: distance 3 (path: 0 → 3 → 4)
```

---

## Complexity Derivation with Proof

**Time Complexity: O((V + E) log V)**

```
Proof:
1. Heap operations per vertex:
   - Each vertex extracted from heap at most once → O(V × log V)
   - (Some implementations allow duplicates; we skip outdated entries)

2. Heap operations per edge:
   - Each edge relaxation may push to heap → O(E × log V)
   - Push operation is O(log V)

3. Total: O(V log V) + O(E log V) = O((V + E) log V)

Note: With Fibonacci heap, can achieve O(E + V log V),
but Python's heapq uses binary heap.
```

**Space Complexity: O(V + E)**

```
Proof:
1. Distance array/dict: O(V)
2. Adjacency list: O(V + E)
3. Priority queue: O(V) in theory, O(E) worst case with duplicates
4. Total: O(V + E)
```

**Why the greedy choice is correct (optimality proof):**

See the formal proof in the **Building Intuition** section.

---

## Edge Cases

```python
# 1. Source equals target
dijkstra(n, edges, source=0)  # dist[0] = 0

# 2. Unreachable node (disconnected graph)
# dist[node] remains float('inf') — return -1 or handle accordingly

# 3. No edges
# Only source has distance 0, everything else is unreachable

# 4. Self-loop
edges = [[0, 0, 5]]
# 0 + 5 = 5 > 0, so self-loop is never beneficial — handled naturally

# 5. Multiple edges between same nodes (parallel edges)
edges = [[0, 1, 5], [0, 1, 3]]
# Both are added to adjacency list; the cheaper one wins during relaxation

# 6. Very large graph with 0-weight edges
# Still correct! Dijkstra requires non-negative, not strictly positive
```

---

## Interview Tips

1. **Know the template**: Heap-based implementation cold
2. **Explain the greedy choice**: "We always process the minimum distance node because non-negative weights guarantee no shorter path can appear later"
3. **State the constraint**: Non-negative weights only
4. **Know when it fails**: Negative weights → Bellman-Ford
5. **Handle unreachable**: Check for infinity in result
6. **Explain relaxation**: "We check if going through the current node offers a shorter path to its neighbor"

---

## Practice Problems

| #   | Problem                                       | Difficulty | Key Variation                     | Hint                                                               |
| --- | --------------------------------------------- | ---------- | --------------------------------- | ------------------------------------------------------------------ |
| 1   | Network Delay Time (LC 743)                   | Medium     | Basic Dijkstra                    | Standard template. Answer is `max(dist)`.                          |
| 2   | Path with Minimum Effort (LC 1631)            | Medium     | Min-max path (Dijkstra on max)    | Dijkstra where "distance" = max absolute height diff along path.   |
| 3   | Cheapest Flights Within K Stops (LC 787)      | Medium     | With stop constraint              | Modified Dijkstra tracking stops; allow revisits with fewer stops.  |
| 4   | Swim in Rising Water (LC 778)                 | Hard       | Min-max path on grid              | Like #2: Dijkstra where cost = max cell value along path.          |
| 5   | Path with Maximum Probability (LC 1514)       | Medium     | Max product instead of min sum    | Use max-heap (negate log-probabilities, or negate probabilities).   |

**Progression**: Start with #1 (pure template), then #2/#5 (modified cost functions), then #3 (extra state dimension), then #4 (grid + modified cost).

---

## Key Takeaways

1. **Greedy on minimum distance**: Always process closest unvisited node
2. **Relaxation**: Core operation — tighten upper bounds on distances
3. **Priority queue**: Essential for efficient greedy selection
4. **Non-negative weights only**: Negative weights break the greedy proof
5. **Skip stale entries**: Check `d > dist[node]` after every pop
6. **O((V + E) log V)**: Standard complexity with binary heap

---

## Next: [10-bellman-ford.md](./10-bellman-ford.md)

Learn Bellman-Ford for graphs with negative edge weights.
