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
