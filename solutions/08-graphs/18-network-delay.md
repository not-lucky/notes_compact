# Network Delay Time

## Practice Problems

### 1. Network Delay Time
**Difficulty:** Medium
**Concept:** Core Dijkstra

```python
import heapq
from collections import defaultdict
from typing import List

def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """
    Find time for signal from k to reach all nodes.

    >>> network_delay_time([[2,1,1],[2,3,1],[3,4,1]], 4, 2)
    2

    Time: O((V + E) log V)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    # (time, node)
    min_heap = [(0, k)]
    dist = {}

    while min_heap:
        time, node = heapq.heappop(min_heap)
        if node in dist:
            continue
        dist[node] = time

        for neighbor, weight in graph[node]:
            if neighbor not in dist:
                heapq.heappush(min_heap, (time + weight, neighbor))

    return max(dist.values()) if len(dist) == n else -1
```

### 2. Path with Maximum Probability
**Difficulty:** Medium
**Concept:** Multiply instead of add

```python
import heapq
from collections import defaultdict
from typing import List

def max_probability(n: int, edges: List[List[int]],
                    succ_prob: List[float], start: int, end: int) -> float:
    """
    Find path with maximum probability.

    Time: O(E log V)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for i, (u, v) in enumerate(edges):
        p = succ_prob[i]
        graph[u].append((v, p))
        graph[v].append((u, p))

    # (-probability, node)
    max_heap = [(-1.0, start)]
    max_prob = [0.0] * n
    max_prob[start] = 1.0

    while max_heap:
        p, u = heapq.heappop(max_heap)
        p = -p

        if u == end:
            return p

        if p < max_prob[u]:
            continue

        for v, prob in graph[u]:
            if p * prob > max_prob[v]:
                max_prob[v] = p * prob
                heapq.heappush(max_heap, (-max_prob[v], v))

    return 0.0
```

### 3. Cheapest Flights Within K Stops
**Difficulty:** Medium
**Concept:** Limited hops

```python
import heapq
from collections import defaultdict
from typing import List

def find_cheapest_price(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    """
    Find cheapest price with at most k stops.

    Time: O(K * E) or O(E log V)
    Space: O(V + E)
    """
    adj = defaultdict(list)
    for u, v, w in flights:
        adj[u].append((v, w))

    # (price, stops, node)
    pq = [(0, 0, src)]
    visited_stops = [float('inf')] * n

    while pq:
        p, s, u = heapq.heappop(pq)
        if u == dst: return p
        if s > k or s >= visited_stops[u]: continue
        visited_stops[u] = s

        for v, w in adj[u]:
            heapq.heappush(pq, (p + w, s + 1, v))
    return -1
```

### 4. Path with Minimum Effort
**Difficulty:** Medium
**Concept:** Maximum edge weight

```python
import heapq
from typing import List

def minimum_effort_path(heights: List[List[int]]) -> int:
    """
    Find path that minimizes the maximum difference between consecutive cells.

    Time: O(MN log MN)
    Space: O(MN)
    """
    rows, cols = len(heights), len(heights[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[0][0] = 0
    pq = [(0, 0, 0)] # effort, r, c

    while pq:
        e, r, c = heapq.heappop(pq)
        if r == rows - 1 and c == cols - 1: return e
        if e > dist[r][c]: continue

        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_effort = max(e, abs(heights[r][c] - heights[nr][nc]))
                if new_effort < dist[nr][nc]:
                    dist[nr][nc] = new_effort
                    heapq.heappush(pq, (new_effort, nr, nc))
    return 0
```

### 5. Swim in Rising Water
**Difficulty:** Hard
**Concept:** Binary search + BFS or Dijkstra

```python
import heapq
from typing import List

def swim_in_water(grid: List[List[int]]) -> int:
    """
    Minimum time to reach bottom right.

    Time: O(N^2 log N)
    Space: O(N^2)
    """
    n = len(grid)
    pq = [(grid[0][0], 0, 0)]
    visited = {(0, 0)}
    res = 0

    while pq:
        t, r, c = heapq.heappop(pq)
        res = max(res, t)
        if r == n - 1 and c == n - 1: return res

        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                visited.add((nr, nc))
                heapq.heappush(pq, (grid[nr][nc], nr, nc))
    return res
```
