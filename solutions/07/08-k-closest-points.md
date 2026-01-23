# K Closest Points to Origin

## Practice Problems

### 1. K Closest Points to Origin
**Difficulty:** Medium
**Concept:** Max heap of size k (evict furthest)

```python
import heapq
from typing import List

def k_closest(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Find k closest points to origin.

    >>> k_closest([[1,3],[-2,2]], 1)
    [[-2, 2]]
    >>> sorted(k_closest([[3,3],[5,-1],[-2,4]], 2))
    [[-2, 4], [3, 3]]

    Time: O(n log k)
    Space: O(k)
    """
    # Max heap to keep k smallest distances
    # Store (-dist, point) to simulate max heap
    max_heap = []
    for x, y in points:
        dist = x*x + y*y
        if len(max_heap) < k:
            heapq.heappush(max_heap, (-dist, [x, y]))
        elif dist < -max_heap[0][0]:
            heapq.heapreplace(max_heap, (-dist, [x, y]))

    return [p for d, p in max_heap]
```
