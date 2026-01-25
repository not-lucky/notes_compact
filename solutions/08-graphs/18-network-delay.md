# Solutions: Network Delay Time

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Network Delay Time | Medium | Core Dijkstra |
| 2 | Path with Maximum Probability | Medium | Multiply instead of add |
| 3 | Cheapest Flights Within K Stops | Medium | Limited hops |
| 4 | Path with Minimum Effort | Medium | Maximum edge weight |
| 5 | Swim in Rising Water | Hard | Binary search + BFS |

---

## 1. Network Delay Time

### Problem Statement
Find the minimum time for all nodes to receive a signal from a source node `k`.

### Optimal Python Solution

```python
import heapq
from collections import defaultdict

def networkDelayTime(times: list[list[int]], n: int, k: int) -> int:
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))

    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0
    pq = [(0, k)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue

        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    ans = max(dist.values())
    return ans if ans < float('inf') else -1
```

### Explanation
- **Algorithm**: Dijkstra's.
- **Complexity**: Time O(E log V), Space O(V + E).

---

## 2. Path with Maximum Probability

### Problem Statement
Find the path with the maximum probability of success.

### Optimal Python Solution

```python
import heapq
from collections import defaultdict

def maxProbability(n: int, edges: list[list[int]], succProb: list[float], start: int, end: int) -> float:
    adj = defaultdict(list)
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, succProb[i]))
        adj[v].append((u, succProb[i]))

    prob = [0.0] * n
    prob[start] = 1.0
    pq = [(-1.0, start)] # Max-heap using negative values

    while pq:
        p, u = heapq.heappop(pq)
        p = -p
        if p < prob[u]: continue
        if u == end: return p

        for v, pr in adj[u]:
            if p * pr > prob[v]:
                prob[v] = p * pr
                heapq.heappush(pq, (-prob[v], v))
    return 0.0
```

---

## 3. Cheapest Flights Within K Stops

### Problem Statement
Find the cheapest price from `src` to `dst` with at most `k` stops.

### Optimal Python Solution

```python
import heapq
from collections import defaultdict

def findCheapestPrice(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    adj = defaultdict(list)
    for u, v, p in flights:
        adj[u].append((v, p))

    # Track minimum stops to reach each node for pruning
    stops = [float('inf')] * n
    pq = [(0, 0, src)] # (price, num_stops, node)

    while pq:
        price, s, u = heapq.heappop(pq)
        if s > k + 1 or s > stops[u]: continue
        if u == dst: return price
        stops[u] = s

        for v, p in adj[u]:
            heapq.heappush(pq, (price + p, s + 1, v))
    return -1
```

---

## 4. Path with Minimum Effort

### Problem Statement
Find path with minimum maximum edge weight.

### Optimal Python Solution

```python
import heapq

def minimumEffortPath(heights: list[list[int]]) -> int:
    rows, cols = len(heights), len(heights[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[0][0] = 0
    pq = [(0, 0, 0)] # (effort, r, c)

    while pq:
        eff, r, c = heapq.heappop(pq)
        if r == rows - 1 and c == cols - 1: return eff
        if eff > dist[r][c]: continue

        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_eff = max(eff, abs(heights[nr][nc] - heights[r][c]))
                if new_eff < dist[nr][nc]:
                    dist[nr][nc] = new_eff
                    heapq.heappush(pq, (new_eff, nr, nc))
    return 0
```

---

## 5. Swim in Rising Water

### Problem Statement
Find the minimum time to swim to the destination.

### Optimal Python Solution

```python
import heapq

def swimInWater(grid: list[list[int]]) -> int:
    n = len(grid)
    pq = [(grid[0][0], 0, 0)]
    visited = {(0, 0)}

    while pq:
        t, r, c = heapq.heappop(pq)
        if r == n - 1 and c == n - 1: return t

        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                visited.add((nr, nc))
                heapq.heappush(pq, (max(t, grid[nr][nc]), nr, nc))
```
