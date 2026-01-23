# Bellman-Ford Algorithm

## Practice Problems

### 1. Cheapest Flights Within K Stops
**Difficulty:** Medium
**Concept:** Limited iterations

```python
from typing import List

def find_cheapest_price(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    """
    Find the cheapest price from src to dst with at most k stops.

    Time: O(K * E)
    Space: O(V)
    """
    prices = [float('inf')] * n
    prices[src] = 0

    for _ in range(k + 1):
        temp_prices = prices[:]
        for u, v, w in flights:
            if prices[u] == float('inf'):
                continue
            if prices[u] + w < temp_prices[v]:
                temp_prices[v] = prices[u] + w
        prices = temp_prices

    return prices[dst] if prices[dst] != float('inf') else -1
```

### 2. Network Delay Time
**Difficulty:** Medium
**Concept:** Bellman-Ford variant

```python
from typing import List

def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """
    Find time for signal to reach all nodes from node k.

    Time: O(V * E)
    Space: O(V)
    """
    dist = [float('inf')] * (n + 1)
    dist[k] = 0

    for _ in range(n - 1):
        updated = False
        for u, v, w in times:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break

    max_dist = max(dist[1:])
    return max_dist if max_dist != float('inf') else -1
```
