# Bellman-Ford Algorithm

> **Prerequisites:** [09-dijkstra](./09-dijkstra.md)

## Interview Context

Bellman-Ford is important because:

1. **Handles negative edges**: Unlike Dijkstra
2. **Detects negative cycles**: Returns error if unreachable minimum
3. **Simpler implementation**: Just iterate over all edges
4. **Less common in interviews**: But important to know for completeness

If an interviewer says "edges can be negative", Bellman-Ford is your answer.

---

## Core Concept

Bellman-Ford finds shortest paths by **relaxing all edges V-1 times**. After V-1 iterations, all shortest paths are found (if no negative cycle).

**Relaxation**: If `dist[u] + weight(u,v) < dist[v]`, update `dist[v]`.

```
Why V-1 iterations?
- Shortest path has at most V-1 edges
- Each iteration guarantees at least one more edge is correctly set
- After V-1 iterations, paths of length V-1 are correct
```

---

## Algorithm Template

```python
def bellman_ford(n: int, edges: list[list[int]], source: int) -> list[float]:
    """
    Bellman-Ford algorithm for shortest paths.
    Handles negative edge weights.

    Time: O(V × E)
    Space: O(V)

    edges format: [u, v, weight]
    Returns: distance array, or None if negative cycle exists
    """
    dist = [float('inf')] * n
    dist[source] = 0

    # Relax all edges V-1 times
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True

        # Early termination if no updates
        if not updated:
            break

    # Check for negative cycles
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # Negative cycle exists

    return dist


# Usage
edges = [[0, 1, 4], [0, 2, 5], [1, 2, -3], [2, 3, 4]]
dist = bellman_ford(4, edges, 0)
print(dist)  # [0, 4, 1, 5]
```

---

## Visual Walkthrough

```
Graph:
  0 --4--> 1
  |        |
  5       -3
  |        |
  v        v
  2 --4--> 3

Initial: dist = [0, ∞, ∞, ∞]

Iteration 1 (relax all edges):
  0→1: dist[1] = min(∞, 0+4) = 4
  0→2: dist[2] = min(∞, 0+5) = 5
  1→2: dist[2] = min(5, 4+(-3)) = 1
  2→3: dist[3] = min(∞, 5+4) = 9  [but 2's dist changes]
       Need to recalculate in next iteration

Iteration 2:
  0→1: no change (4 ≤ 0+4)
  0→2: no change (1 < 0+5)
  1→2: no change (1 ≤ 4-3)
  2→3: dist[3] = min(9, 1+4) = 5

Iteration 3: No changes → terminate early

Final: dist = [0, 4, 1, 5]

Path to 3: 0 → 1 → 2 → 3 (cost: 4 + (-3) + 4 = 5)
```

---

## Negative Cycle Detection

```python
def has_negative_cycle(n: int, edges: list[list[int]]) -> bool:
    """
    Check if graph has a negative cycle.

    Time: O(V × E)
    Space: O(V)
    """
    dist = [0] * n  # Start with 0 to detect any negative cycle

    # Relax V-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # One more relaxation - if anything changes, negative cycle exists
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return True

    return False
```

---

## Finding the Negative Cycle

```python
def find_negative_cycle(n: int, edges: list[list[int]]) -> list[int]:
    """
    Find and return nodes in a negative cycle.

    Returns empty list if no negative cycle.
    """
    dist = [0] * n
    parent = [-1] * n

    # Track which node gets updated in the Vth iteration
    cycle_node = -1

    for i in range(n):
        cycle_node = -1
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                cycle_node = v

    if cycle_node == -1:
        return []  # No negative cycle

    # Go back n times to ensure we're in the cycle
    for _ in range(n):
        cycle_node = parent[cycle_node]

    # Collect cycle
    cycle = []
    current = cycle_node
    while True:
        cycle.append(current)
        current = parent[current]
        if current == cycle_node:
            cycle.append(current)
            break

    return cycle[::-1]
```

---

## SPFA: Optimized Bellman-Ford

Shortest Path Faster Algorithm - uses queue to only process updated nodes:

```python
from collections import deque

def spfa(n: int, edges: list[list[int]], source: int) -> list[float]:
    """
    SPFA: Optimized Bellman-Ford with queue.

    Time: O(V × E) worst case, often O(E) in practice
    Space: O(V)
    """
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = [float('inf')] * n
    dist[source] = 0
    in_queue = [False] * n
    count = [0] * n  # For cycle detection

    queue = deque([source])
    in_queue[source] = True

    while queue:
        u = queue.popleft()
        in_queue[u] = False

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

                if not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True
                    count[v] += 1

                    if count[v] >= n:
                        return None  # Negative cycle

    return dist
```

---

## Comparison: Dijkstra vs Bellman-Ford

| Aspect | Dijkstra | Bellman-Ford |
|--------|----------|--------------|
| Time | O((V+E) log V) | O(V × E) |
| Negative edges | No | Yes |
| Negative cycle detection | No | Yes |
| Implementation | Heap-based | Simple iteration |
| When to use | Non-negative weights | Negative weights possible |

---

## Cheapest Flights with K Stops (Bellman-Ford Variant)

```python
def find_cheapest_price_bf(n: int, flights: list[list[int]],
                            src: int, dst: int, k: int) -> int:
    """
    Find cheapest price with at most k stops using Bellman-Ford variant.

    Limit iterations to k+1 (at most k stops = k+1 edges).

    Time: O(k × E)
    Space: O(V)
    """
    dist = [float('inf')] * n
    dist[src] = 0

    for _ in range(k + 1):  # At most k+1 edges
        temp = dist[:]  # Use previous iteration's values

        for u, v, price in flights:
            if temp[u] != float('inf'):
                dist[v] = min(dist[v], temp[u] + price)

    return dist[dst] if dist[dst] != float('inf') else -1
```

---

## When to Use Each Algorithm

| Scenario | Algorithm |
|----------|-----------|
| Non-negative weights | Dijkstra (faster) |
| Negative weights, no negative cycle | Bellman-Ford |
| Need to detect negative cycle | Bellman-Ford |
| Limited hops/stops | Bellman-Ford with limited iterations |
| Dense graph, non-negative | Dijkstra |
| Sparse graph, any weights | Bellman-Ford |

---

## Edge Cases

```python
# 1. No edges
n = 3, edges = []
# Only source reachable

# 2. Negative self-loop
edges = [[0, 0, -1]]
# Negative cycle at node 0

# 3. Disconnected graph
# Unreachable nodes have infinity distance

# 4. All negative edges (no cycle)
edges = [[0, 1, -2], [1, 2, -3]]
# Valid shortest paths with negative weights

# 5. Negative cycle not reachable from source
# Shortest paths still valid for reachable nodes
```

---

## Common Mistakes

```python
# WRONG: Not using previous iteration's values
for _ in range(n - 1):
    for u, v, w in edges:
        dist[v] = min(dist[v], dist[u] + w)
        # Problem: dist[u] might have just changed!

# CORRECT for limited edges problem:
for _ in range(k + 1):
    temp = dist[:]  # Copy previous state
    for u, v, w in edges:
        dist[v] = min(dist[v], temp[u] + w)

# Note: For standard Bellman-Ford, updating in-place is fine
# because we do V-1 iterations. But for limited hops, must copy.


# WRONG: Relaxing from unreachable nodes
if dist[u] + w < dist[v]:  # dist[u] might be infinity!
    dist[v] = dist[u] + w  # inf + w is still inf (or overflow)

# CORRECT: Check if source is reachable
if dist[u] != float('inf') and dist[u] + w < dist[v]:
    dist[v] = dist[u] + w
```

---

## Interview Tips

1. **Know when to use**: Negative edges → Bellman-Ford
2. **V-1 iterations**: Maximum path length in graph
3. **Cycle detection**: One more iteration after V-1
4. **Limited hops variant**: Use temp array for each iteration
5. **Simple to implement**: Just nested loops over edges

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Cheapest Flights Within K Stops | Medium | Limited iterations |
| 2 | Network Delay Time | Medium | Can use either |
| 3 | Negative Cycle Detection | Medium | Extra iteration |
| 4 | Path with Minimum Effort | Medium | Binary search variant |

---

## Key Takeaways

1. **O(V × E) time**: Slower than Dijkstra but handles negative edges
2. **V-1 iterations**: Each iteration sets one more edge correctly
3. **Vth iteration for cycles**: Any update means negative cycle
4. **Use copy for limited hops**: Prevent using same-iteration updates
5. **SPFA optimization**: Queue-based, faster in practice

---

## Next: [11-shortest-path-unweighted.md](./11-shortest-path-unweighted.md)

Review BFS for shortest path in unweighted graphs.
