# Dijkstra's Algorithm

## Practice Problems

### 1. Network Delay Time
**Difficulty:** Medium
**Concept:** Basic Dijkstra

```python
import heapq
from collections import defaultdict
from typing import List

def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """
    You are given a network of n nodes, labeled from 1 to n. You are also
    given times, a list of travel times as directed edges times[i] = (ui, vi, wi).
    We will send a signal from a given node k. Return the minimum time it
    takes for all the n nodes to receive the signal. If it is impossible
    for all the n nodes to receive the signal, return -1.

    >>> network_delay_time([[2,1,1],[2,3,1],[3,4,1]], 4, 2)
    2
    >>> network_delay_time([[1,2,1]], 2, 1)
    1
    >>> network_delay_time([[1,2,1]], 2, 2)
    -1

    Time: O(E log V)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    # (distance, node)
    min_heap = [(0, k)]
    visited = {}

    while min_heap:
        d, node = heapq.heappop(min_heap)
        if node in visited:
            continue
        visited[node] = d

        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (d + weight, neighbor))

    return max(visited.values()) if len(visited) == n else -1
```

### 2. Path with Minimum Effort
**Difficulty:** Medium
**Concept:** Dijkstra variant

```python
import heapq
from typing import List

def minimum_effort_path(heights: List[List[int]]) -> int:
    """
    Find a path that minimizes the maximum absolute difference in heights
    between two consecutive cells of the path.

    Time: O(M*N log(M*N))
    Space: O(M*N)
    """
    rows, cols = len(heights), len(heights[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[0][0] = 0
    min_heap = [(0, 0, 0)] # effort, r, c

    while min_heap:
        effort, r, c = heapq.heappop(min_heap)
        if r == rows - 1 and c == cols - 1:
            return effort

        if effort > dist[r][c]:
            continue

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_effort = max(effort, abs(heights[r][c] - heights[nr][nc]))
                if new_effort < dist[nr][nc]:
                    dist[nr][nc] = new_effort
                    heapq.heappush(min_heap, (new_effort, nr, nc))
    return 0
```

### 3. Cheapest Flights Within K Stops
**Difficulty:** Medium
**Concept:** With stop constraint

```python
import heapq
from collections import defaultdict
from typing import List

def find_cheapest_price(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    """
    Find the cheapest price from src to dst with at most k stops.

    Time: O(E * K log V) in worst case
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))

    # (price, stops, node)
    min_heap = [(0, 0, src)]
    # Track min stops to reach a node with a certain price is hard,
    # but we can track min price to reach a node with a certain number of stops.
    # Actually, tracking min stops for a node is simpler.
    visited_stops = [float('inf')] * n

    while min_heap:
        p, s, node = heapq.heappop(min_heap)

        if node == dst:
            return p

        if s > k or s >= visited_stops[node]:
            continue

        visited_stops[node] = s

        for neighbor, weight in graph[node]:
            heapq.heappush(min_heap, (p + weight, s + 1, neighbor))

    return -1
```
