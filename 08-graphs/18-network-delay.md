# Network Delay Time

> **Prerequisites:** [09-dijkstra](./09-dijkstra.md)

## Interview Context

Network Delay Time is a classic Dijkstra application because:

1. **Clean problem statement**: Time for signal to reach all nodes
2. **Weighted shortest paths**: Edge weights represent delay
3. **Single source, all destinations**: Classic Dijkstra use case
4. **Interview favorite**: Appears at Amazon, Google, Meta

This is often the first Dijkstra problem in interview prep.

---

## Problem Statement

There are `n` network nodes labeled `1` to `n`. Given `times[i] = (u, v, w)` representing a directed edge from `u` to `v` with delay `w`, and a source node `k`, find the minimum time for all nodes to receive a signal from `k`.

Return -1 if impossible.

```
Example:
times = [[2,1,1], [2,3,1], [3,4,1]]
n = 4
k = 2

Graph:
    2 --1--> 1
    |
    1
    |
    v
    3 --1--> 4

From node 2:
- Node 1: 1
- Node 3: 1
- Node 4: 2 (via 3)

Answer: 2 (time when last node receives signal)
```

---

## Solution: Dijkstra's Algorithm

```python
import heapq
from collections import defaultdict

def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    """
    Find time for signal from k to reach all nodes.

    Time: O((V + E) log V)
    Space: O(V + E)
    """
    # Build adjacency list
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    # Dijkstra's algorithm
    dist = {k: 0}
    heap = [(0, k)]  # (time, node)

    while heap:
        time, node = heapq.heappop(heap)

        # Skip if we've found a better path
        if time > dist.get(node, float('inf')):
            continue

        for neighbor, weight in graph[node]:
            new_time = time + weight

            if new_time < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_time
                heapq.heappush(heap, (new_time, neighbor))

    # Check if all nodes are reachable
    if len(dist) != n:
        return -1

    return max(dist.values())
```

---

## Alternative: Without defaultdict

```python
import heapq

def network_delay_time_alt(times: list[list[int]], n: int, k: int) -> int:
    """
    Same algorithm with explicit arrays.
    """
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]  # 1-indexed
    for u, v, w in times:
        graph[u].append((v, w))

    # Distance array
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[k] = 0

    # Priority queue
    heap = [(0, k)]

    while heap:
        time, node = heapq.heappop(heap)

        if time > dist[node]:
            continue

        for neighbor, weight in graph[node]:
            new_time = time + weight

            if new_time < dist[neighbor]:
                dist[neighbor] = new_time
                heapq.heappush(heap, (new_time, neighbor))

    # Find maximum (ignoring index 0)
    max_time = max(dist[1:])

    return max_time if max_time < INF else -1
```

---

## Visual Walkthrough

```
times = [[2,1,1], [2,3,1], [3,4,1]]
n = 4, k = 2

Graph:
    2 --1--> 1
    |
    1
    v
    3 --1--> 4

Initial: dist = {2: 0}, heap = [(0, 2)]

Step 1: Pop (0, 2)
        Process neighbors:
          1: dist[1] = 0 + 1 = 1
          3: dist[3] = 0 + 1 = 1
        heap = [(1, 1), (1, 3)]

Step 2: Pop (1, 1)
        No outgoing edges
        heap = [(1, 3)]

Step 3: Pop (1, 3)
        Process neighbors:
          4: dist[4] = 1 + 1 = 2
        heap = [(2, 4)]

Step 4: Pop (2, 4)
        No outgoing edges
        heap = []

Final: dist = {2: 0, 1: 1, 3: 1, 4: 2}
All 4 nodes reached
Max time = 2

Answer: 2
```

---

## Bellman-Ford Alternative

If edges could be negative (they can't in this problem, but good to know):

```python
def network_delay_time_bf(times: list[list[int]], n: int, k: int) -> int:
    """
    Bellman-Ford solution.

    Time: O(V × E)
    Space: O(V)
    """
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[k] = 0

    # Relax all edges n-1 times
    for _ in range(n - 1):
        for u, v, w in times:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    max_time = max(dist[1:])
    return max_time if max_time < INF else -1
```

---

## BFS for Unweighted (Simplified Version)

If all delays were 1 (unweighted), could use BFS:

```python
from collections import deque

def network_delay_time_unweighted(times: list[list[int]], n: int, k: int) -> int:
    """
    BFS if all weights are 1.
    Note: Original problem has varying weights, so use Dijkstra.
    """
    graph = defaultdict(list)
    for u, v, _ in times:  # Ignore weight
        graph[u].append(v)

    dist = {k: 0}
    queue = deque([k])

    while queue:
        node = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)

    if len(dist) != n:
        return -1

    return max(dist.values())
```

---

## Related: Path with Maximum Probability

Similar structure, different operation (multiply instead of add):

```python
import heapq
from collections import defaultdict

def max_probability(n: int, edges: list[list[int]],
                    succProb: list[float], start: int, end: int) -> float:
    """
    Find path with maximum probability.

    Use max-heap (negate probabilities) or modify Dijkstra.
    """
    graph = defaultdict(list)
    for i, (u, v) in enumerate(edges):
        prob = succProb[i]
        graph[u].append((v, prob))
        graph[v].append((u, prob))

    # Max-heap: use negative probabilities
    max_prob = [0.0] * n
    max_prob[start] = 1.0
    heap = [(-1.0, start)]  # Negate for max-heap

    while heap:
        neg_prob, node = heapq.heappop(heap)
        prob = -neg_prob

        if node == end:
            return prob

        if prob < max_prob[node]:
            continue

        for neighbor, edge_prob in graph[node]:
            new_prob = prob * edge_prob

            if new_prob > max_prob[neighbor]:
                max_prob[neighbor] = new_prob
                heapq.heappush(heap, (-new_prob, neighbor))

    return 0.0
```

---

## Edge Cases

```python
# 1. Source is only node
n = 1, k = 1, times = []
# Return 0 (no delay needed)

# 2. Unreachable node
times = [[1, 2, 1]]  # Only 1 → 2
n = 3, k = 1
# Node 3 unreachable, return -1

# 3. All nodes directly connected to source
times = [[1, 2, 1], [1, 3, 1], [1, 4, 1]]
n = 4, k = 1
# All at distance 1, return 1

# 4. Linear chain
times = [[1, 2, 1], [2, 3, 1], [3, 4, 1]]
n = 4, k = 1
# Cumulative delays: 1, 2, 3
# Return 3
```

---

## Common Mistakes

```python
# WRONG: Using BFS for weighted graph
queue = deque([k])
dist[k] = 0
while queue:
    node = queue.popleft()
    for neighbor, weight in graph[node]:
        # BFS doesn't guarantee shortest path with weights!

# CORRECT: Use Dijkstra for weighted graphs


# WRONG: Not checking if all nodes reached
return max(dist.values())
# If some nodes unreachable, should return -1

# CORRECT:
if len(dist) != n:
    return -1
return max(dist.values())


# WRONG: 0-indexed vs 1-indexed confusion
dist = [INF] * n
dist[k] = 0  # If k is 1-indexed, this is wrong!

# CORRECT: Use n+1 for 1-indexed, or use dict
dist = [INF] * (n + 1)  # 1-indexed
```

---

## Complexity Analysis

| Algorithm | Time | Space |
|-----------|------|-------|
| Dijkstra | O((V + E) log V) | O(V + E) |
| Bellman-Ford | O(V × E) | O(V) |
| BFS (unweighted) | O(V + E) | O(V) |

---

## Interview Tips

1. **Recognize Dijkstra pattern**: Weighted single-source shortest paths
2. **Handle 1-indexed nodes**: Problem often uses 1 to n
3. **Check reachability**: Return -1 if not all nodes reached
4. **Know the algorithm**: Be able to write from scratch
5. **Mention alternatives**: BFS for unweighted, Bellman-Ford for negative

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Network Delay Time | Medium | Core Dijkstra |
| 2 | Path with Maximum Probability | Medium | Multiply instead of add |
| 3 | Cheapest Flights Within K Stops | Medium | Limited hops |
| 4 | Path with Minimum Effort | Medium | Maximum edge weight |
| 5 | Swim in Rising Water | Hard | Binary search + BFS |

---

## Key Takeaways

1. **Single-source shortest paths**: Classic Dijkstra
2. **Answer is max distance**: Time when last node receives signal
3. **Handle unreachable**: Check if all nodes in distance map
4. **1-indexed nodes**: Be careful with array sizes
5. **Heap-based implementation**: Standard and efficient

---

## Summary: Graph Chapter Complete!

You've now covered all major graph patterns:

| Topic | Key Algorithm |
|-------|---------------|
| Graph representations | Adjacency list/matrix |
| BFS | Level-order, shortest unweighted |
| DFS | Traversal, backtracking |
| Connected components | Union-Find or DFS |
| Cycle detection | Colors (directed), parent (undirected) |
| Topological sort | Kahn's or DFS |
| Shortest paths | Dijkstra, Bellman-Ford |
| Grid problems | BFS/DFS as implicit graph |

These patterns cover 90%+ of graph problems in FANG+ interviews.
