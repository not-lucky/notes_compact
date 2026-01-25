# Solutions: Dijkstra's Algorithm

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Network Delay Time | Medium | Basic Dijkstra |
| 2 | Path with Minimum Effort | Medium | Dijkstra on Grid |
| 3 | Cheapest Flights Within K Stops | Medium | Hops constraint |
| 4 | Swim in Rising Water | Hard | Dijkstra on Grid |
| 5 | Path with Maximum Probability | Medium | Product of weights |

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

    max_dist = max(dist.values())
    return max_dist if max_dist < float('inf') else -1
```

### Explanation
- **Algorithm**: Standard Dijkstra.
- **Complexity**: Time O(E log V), Space O(V + E).

---

## 2. Path with Minimum Effort

### Problem Statement
Find a path from top-left to bottom-right such that the maximum absolute difference in heights between adjacent cells is minimized.

### Optimal Python Solution

```python
import heapq

def minimumEffortPath(heights: list[list[int]]) -> int:
    rows, cols = len(heights), len(heights[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[0][0] = 0
    pq = [(0, 0, 0)] # (effort, r, c)

    while pq:
        effort, r, c = heapq.heappop(pq)
        if r == rows - 1 and c == cols - 1: return effort
        if effort > dist[r][c]: continue

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_effort = max(effort, abs(heights[nr][nc] - heights[r][c]))
                if new_effort < dist[nr][nc]:
                    dist[nr][nc] = new_effort
                    heapq.heappush(pq, (new_effort, nr, nc))
    return 0
```

### Explanation
- **Logic**: Use Dijkstra where the "distance" is the maximum edge weight on the path.
- **Complexity**: Time O(MN log(MN)), Space O(MN).

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

    # stops[i] stores the minimum stops to reach node i with the current price
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

### Explanation
- **Constraint**: Regular Dijkstra can fail because a more expensive path with fewer stops might be better later.
- **Optimization**: We track the number of stops to prune paths.
- **Complexity**: Time O(E * K log E), Space O(V + E).

---

## 4. Swim in Rising Water

### Problem Statement
Find the minimum time to swim from top-left to bottom-right, where you can swim in water of level `t` if the grid value is `≤ t`.

### Optimal Python Solution

```python
import heapq

def swimInWater(grid: list[list[int]]) -> int:
    n = len(grid)
    pq = [(grid[0][0], 0, 0)] # (time, r, c)
    visited = {(0, 0)}

    while pq:
        t, r, c = heapq.heappop(pq)
        if r == n - 1 and c == n - 1: return t

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                visited.add((nr, nc))
                heapq.heappush(pq, (max(t, grid[nr][nc]), nr, nc))
```

### Explanation
- **Logic**: Similar to Path with Minimum Effort. The time is the maximum height on the path.
- **Complexity**: Time O(N² log N), Space O(N²).

---

## 5. Path with Maximum Probability

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

    probs = [0.0] * n
    probs[start] = 1.0
    pq = [(-1.0, start)] # Use max-heap (negative values)

    while pq:
        p, u = heapq.heappop(pq)
        p = -p
        if u == end: return p
        if p < probs[u]: continue

        for v, prob in adj[u]:
            if p * prob > probs[v]:
                probs[v] = p * prob
                heapq.heappush(pq, (-probs[v], v))
    return 0.0
```

### Explanation
- **Variation**: Instead of adding weights, we multiply probabilities. Instead of minimizing, we maximize.
- **Complexity**: Time O(E log V), Space O(V + E).
