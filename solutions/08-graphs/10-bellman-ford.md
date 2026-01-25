# Solutions: Bellman-Ford Algorithm

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Cheapest Flights Within K Stops | Medium | Limited iterations |
| 2 | Network Delay Time | Medium | Can use either |
| 3 | Negative Cycle Detection | Medium | Extra iteration |
| 4 | Path with Minimum Effort | Medium | Binary search variant |

---

## 1. Cheapest Flights Within K Stops

### Problem Statement
Find the cheapest price from `src` to `dst` with at most `k` stops.

### Optimal Python Solution

```python
def findCheapestPrice(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    dist = [float('inf')] * n
    dist[src] = 0

    # Relax k+1 times
    for _ in range(k + 1):
        temp = dist[:]
        for u, v, p in flights:
            if temp[u] != float('inf') and temp[u] + p < dist[v]:
                dist[v] = temp[u] + p
    return dist[dst] if dist[dst] != float('inf') else -1
```

### Explanation
- **Algorithm**: Bellman-Ford variant. We limit the number of relaxations to `k+1` to respect the stop constraint.
- **Copying**: Using `temp` is essential to ensure we only use results from the previous "layer" of stops.
- **Complexity**: Time O(K * E), Space O(V).

---

## 2. Network Delay Time

### Problem Statement
Minimum time for all nodes to receive a signal.

### Optimal Python Solution

```python
def networkDelayTime(times: list[list[int]], n: int, k: int) -> int:
    dist = [float('inf')] * (n + 1)
    dist[k] = 0

    for _ in range(n - 1):
        updated = False
        for u, v, w in times:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated: break

    res = max(dist[1:])
    return res if res < float('inf') else -1
```

### Explanation
- **Complexity**: Time O(VE), Space O(V).
- **Note**: While Dijkstra is usually faster, Bellman-Ford works and is simpler to implement.

---

## 3. Negative Cycle Detection

### Problem Statement
Determine if a graph contains a cycle with a negative total weight.

### Optimal Python Solution

```python
def hasNegativeCycle(n: int, edges: list[list[int]]) -> bool:
    dist = [0] * n # Use 0 to detect cycles reachable from any node

    # Relax V-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # V-th iteration
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return True # If we can still relax, a negative cycle exists
    return False
```

### Explanation
- **Logic**: A shortest path in a graph without negative cycles has at most `V-1` edges. If we can still improve after `V-1` relaxations, there's a negative cycle.
- **Complexity**: Time O(VE), Space O(V).

---

## 4. Path with Minimum Effort

### Problem Statement
(Binary Search + BFS approach as a Bellman-Ford "variant" style of thought).

### Optimal Python Solution (Binary Search + BFS)

```python
from collections import deque

def minimumEffortPath(heights: list[list[int]]) -> int:
    r_len, c_len = len(heights), len(heights[0])

    def can_reach(limit):
        queue = deque([(0, 0)])
        visited = {(0, 0)}
        while queue:
            r, c = queue.popleft()
            if r == r_len - 1 and c == c_len - 1: return True
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < r_len and 0 <= nc < c_len and (nr, nc) not in visited:
                    if abs(heights[nr][nc] - heights[r][c]) <= limit:
                        visited.add((nr, nc))
                        queue.append((nr, nc))
        return False

    low, high = 0, 10**6
    ans = high
    while low <= high:
        mid = (low + high) // 2
        if can_reach(mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans
```

### Explanation
- **Variation**: Instead of pathfinding, we binary search on the "effort" limit and use BFS to check reachability.
- **Complexity**: Time O(MN log(max_height)), Space O(MN).
