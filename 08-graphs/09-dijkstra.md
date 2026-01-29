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
- This is the **optimal substructure** that makes Dijkstra correct

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

**The negative weight trap - why Dijkstra fails:**

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

```python
import heapq
from collections import defaultdict

def dijkstra(n: int, edges: list[list[int]], source: int) -> list[int]:
    """
    Dijkstra's algorithm for shortest paths from source.

    Time: O((V + E) log V)
    Space: O(V + E)

    edges format: [u, v, weight]
    Returns: distance array where dist[i] = shortest distance to i
    """
    # Build adjacency list
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))  # Remove for directed graph

    # Distance array
    dist = [float('inf')] * n
    dist[source] = 0

    # Min-heap: (distance, node)
    heap = [(0, source)]

    while heap:
        d, node = heapq.heappop(heap)

        # Skip if we've found a better path
        if d > dist[node]:
            continue

        for neighbor, weight in graph[node]:
            new_dist = dist[node] + weight

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return dist


# Usage
edges = [[0, 1, 2], [0, 2, 4], [1, 3, 1], [2, 3, 1]]
dist = dijkstra(4, edges, 0)
print(dist)  # [0, 2, 4, 3]
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
def dijkstra_with_path(n: int, edges: list[list[int]],
                        source: int, target: int) -> tuple[int, list[int]]:
    """
    Dijkstra's with path reconstruction.

    Returns: (distance, path)
    """
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    dist = [float('inf')] * n
    dist[source] = 0
    parent = {source: None}

    heap = [(0, source)]

    while heap:
        d, node = heapq.heappop(heap)

        if node == target:
            break

        if d > dist[node]:
            continue

        for neighbor, weight in graph[node]:
            new_dist = dist[node] + weight

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                parent[neighbor] = node
                heapq.heappush(heap, (new_dist, neighbor))

    if dist[target] == float('inf'):
        return -1, []

    # Reconstruct path
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = parent[current]

    return dist[target], path[::-1]
```

---

## Network Delay Time (Classic Problem)

```python
def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    """
    Find time for signal to reach all nodes from node k.

    times[i] = [u, v, w]: edge from u to v with time w
    n: number of nodes (1-indexed)
    k: starting node

    Returns: minimum time to reach all nodes, or -1 if impossible

    Time: O((V + E) log V)
    """
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0

    heap = [(0, k)]

    while heap:
        d, node = heapq.heappop(heap)

        if d > dist[node]:
            continue

        for neighbor, weight in graph[node]:
            new_dist = d + weight

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    max_dist = max(dist.values())
    return max_dist if max_dist < float('inf') else -1
```

---

## Cheapest Flights Within K Stops

Modified Dijkstra with stop constraint:

```python
def find_cheapest_price(n: int, flights: list[list[int]],
                        src: int, dst: int, k: int) -> int:
    """
    Find cheapest price from src to dst with at most k stops.

    Time: O(E × K)
    Space: O(V)

    Note: Regular Dijkstra doesn't work here because we need
    to track the number of stops, not just minimum distance.
    """
    graph = defaultdict(list)
    for u, v, price in flights:
        graph[u].append((v, price))

    # (cost, node, stops)
    heap = [(0, src, 0)]
    # Best cost to reach node with certain number of stops
    best = defaultdict(lambda: float('inf'))

    while heap:
        cost, node, stops = heapq.heappop(heap)

        if node == dst:
            return cost

        if stops > k:
            continue

        if cost > best[(node, stops)]:
            continue
        best[(node, stops)] = cost

        for neighbor, price in graph[node]:
            new_cost = cost + price
            if new_cost < best[(neighbor, stops + 1)]:
                heapq.heappush(heap, (new_cost, neighbor, stops + 1))

    return -1
```

---

## Why Dijkstra Fails with Negative Weights

```
Graph with negative edge:
    0 --1-- 1
     \     /
      3  -2
       \ /
        2

Dijkstra from 0:
  Step 1: Process 0, update dist[1]=1, dist[2]=3
  Step 2: Process 1 (dist=1), no improvements
  Step 3: Process 2 (dist=3), can't go back

But: 0→2→1 costs 3+(-2)=1, same as direct!
     If edge 0→2 was 4: 0→2→1 = 4+(-2)=2 < 1
     Dijkstra would miss this.

Use Bellman-Ford for negative edges.
```

---

## Complexity Analysis

| Implementation   | Time             | Space |
| ---------------- | ---------------- | ----- |
| Binary heap      | O((V + E) log V) | O(V)  |
| Fibonacci heap   | O(E + V log V)   | O(V)  |
| Adjacency matrix | O(V²)            | O(V)  |

Binary heap is standard for interviews.

---

## Common Mistakes

```python
# WRONG: Not skipping outdated entries
while heap:
    d, node = heapq.heappop(heap)
    # Process without checking if d > dist[node]
    # This processes the same node multiple times!

# CORRECT: Skip if we found a better path
while heap:
    d, node = heapq.heappop(heap)
    if d > dist[node]:
        continue  # Already found better path
    # Process...


# WRONG: Using visited set (may skip better paths in some cases)
visited = set()
while heap:
    d, node = heapq.heappop(heap)
    if node in visited:
        continue
    visited.add(node)
    # This works for basic Dijkstra but fails for variations

# For basic Dijkstra, both work, but distance check is more general


# WRONG: Not handling unreachable nodes
return max(dist)  # May return infinity!

# CORRECT
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
║ ITERATION 1: Pop (0, node 0) - smallest distance                 ║
╚══════════════════════════════════════════════════════════════════╝
  dist[0] = 0 (final, because smallest in heap)

  Relaxing edges from node 0:
    Edge 0→1 (weight 4): 0 + 4 = 4 < ∞  → Update dist[1] = 4, push (4, 1)
    Edge 0→2 (weight 2): 0 + 2 = 2 < ∞  → Update dist[2] = 2, push (2, 2)
    Edge 0→3 (weight 1): 0 + 1 = 1 < ∞  → Update dist[3] = 1, push (1, 3)

  Distances: {0: 0, 1: 4, 2: 2, 3: 1, 4: ∞}
  Min-Heap: [(1, 3), (2, 2), (4, 1)]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 2: Pop (1, node 3) - smallest distance                 ║
╚══════════════════════════════════════════════════════════════════╝
  dist[3] = 1 (final)

  Relaxing edges from node 3:
    Edge 3→4 (weight 2): 1 + 2 = 3 < ∞  → Update dist[4] = 3, push (3, 4)

  Distances: {0: 0, 1: 4, 2: 2, 3: 1, 4: 3}
  Min-Heap: [(2, 2), (3, 4), (4, 1)]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 3: Pop (2, node 2) - smallest distance                 ║
╚══════════════════════════════════════════════════════════════════╝
  dist[2] = 2 (final)

  Relaxing edges from node 2:
    Edge 2→4 (weight 3): 2 + 3 = 5 > 3  → No update (current path better)

  Distances: {0: 0, 1: 4, 2: 2, 3: 1, 4: 3}
  Min-Heap: [(3, 4), (4, 1)]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 4: Pop (3, node 4) - smallest distance                 ║
╚══════════════════════════════════════════════════════════════════╝
  dist[4] = 3 (final)

  Node 4 has no outgoing edges.

  Distances: {0: 0, 1: 4, 2: 2, 3: 1, 4: 3}
  Min-Heap: [(4, 1)]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 5: Pop (4, node 1)                                     ║
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
3. Priority queue: O(V) or O(E) with duplicates
4. Total: O(V + E)
```

**Why the greedy choice is correct (optimality proof):**

```
Theorem: When Dijkstra extracts a node u, dist[u] is the true shortest distance.

Proof by contradiction:
1. Suppose dist[u] is NOT the shortest when extracted.
2. Then there exists a shorter path P to u.
3. Let v be the first unprocessed node on P.
4. Since all edges have non-negative weight:
   dist[v] ≤ length(P to v) ≤ length(P) < dist[u]
5. But then v would have been extracted before u (min-heap property).
6. Contradiction! ∎

Key: This proof fails with negative edges because step 4 doesn't hold.
```

---

## Edge Cases

```python
# 1. Source equals target
dijkstra(n, edges, 0) with target 0
# Distance = 0

# 2. Unreachable node
# Disconnected graph
# Return infinity or -1

# 3. No edges
# Only source has distance 0

# 4. Self-loop
edges = [[0, 0, 5]]
# Ignore, doesn't help shortest path

# 5. Multiple edges between same nodes
edges = [[0, 1, 5], [0, 1, 3]]
# Keep both, algorithm handles naturally
```

---

## Interview Tips

1. **Know the template**: Heap-based implementation
2. **Explain the greedy choice**: Always process minimum distance
3. **State the constraint**: Non-negative weights only
4. **Know when it fails**: Negative weights → Bellman-Ford
5. **Handle unreachable**: Check for infinity in result

---

## Practice Problems

| #   | Problem                         | Difficulty | Key Variation            |
| --- | ------------------------------- | ---------- | ------------------------ |
| 1   | Network Delay Time              | Medium     | Basic Dijkstra           |
| 2   | Path with Minimum Effort        | Medium     | Binary search + Dijkstra |
| 3   | Cheapest Flights Within K Stops | Medium     | With stop constraint     |
| 4   | Swim in Rising Water            | Hard       | Binary search + BFS      |
| 5   | Path with Maximum Probability   | Medium     | Product instead of sum   |

---

## Key Takeaways

1. **Greedy on minimum distance**: Always process closest unvisited
2. **Priority queue**: Essential for efficiency
3. **Non-negative weights only**: Otherwise use Bellman-Ford
4. **Skip outdated heap entries**: Check `d > dist[node]`
5. **O((V + E) log V)**: Standard complexity with binary heap

---

## Next: [10-bellman-ford.md](./10-bellman-ford.md)

Learn Bellman-Ford for graphs with negative edge weights.
