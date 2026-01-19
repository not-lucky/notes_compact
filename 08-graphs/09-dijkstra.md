# Dijkstra's Algorithm

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md), [07-heaps-priority-queues](../07-heaps-priority-queues/README.md)

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

| Implementation | Time | Space |
|---------------|------|-------|
| Binary heap | O((V + E) log V) | O(V) |
| Fibonacci heap | O(E + V log V) | O(V) |
| Adjacency matrix | O(V²) | O(V) |

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

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Network Delay Time | Medium | Basic Dijkstra |
| 2 | Path with Minimum Effort | Medium | Binary search + Dijkstra |
| 3 | Cheapest Flights Within K Stops | Medium | With stop constraint |
| 4 | Swim in Rising Water | Hard | Binary search + BFS |
| 5 | Path with Maximum Probability | Medium | Product instead of sum |

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
