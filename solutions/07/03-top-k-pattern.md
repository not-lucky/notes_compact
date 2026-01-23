# Top-K Pattern

## Practice Problems

### 1. Top K Frequent Elements
**Difficulty:** Medium
**Concept:** Counter + nlargest

```python
import heapq
from collections import Counter
from typing import List

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Find k most frequent elements.

    >>> top_k_frequent([1,1,1,2,2,3], 2)
    [1, 2]
    >>> top_k_frequent([1], 1)
    [1]

    Time: O(n log k)
    Space: O(n) for Counter
    """
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

### 2. K Closest Points to Origin
**Difficulty:** Medium
**Concept:** Max heap of size k (evict furthest)

```python
def k_closest(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Find k closest points to (0,0).

    >>> k_closest([[1,3],[-2,2]], 1)
    [[-2, 2]]
    >>> sorted(k_closest([[3,3],[5,-1],[-2,4]], 2))
    [[-2, 4], [3, 3]]

    Time: O(n log k)
    Space: O(k)
    """
    # Max heap: (-dist, x, y)
    max_heap = []
    for x, y in points:
        dist = x*x + y*y
        if len(max_heap) < k:
            heapq.heappush(max_heap, (-dist, [x, y]))
        elif dist < -max_heap[0][0]:
            heapq.heapreplace(max_heap, (-dist, [x, y]))

    return [p for d, p in max_heap]
```
