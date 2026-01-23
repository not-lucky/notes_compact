# Python heapq Module

## Practice Problems

### 1. Maintain K Smallest Elements from Stream
**Difficulty:** Medium
**Concept:** Max heap of size k

```python
import heapq
from typing import List

def maintain_k_smallest(nums: List[int], k: int) -> List[int]:
    """
    Maintain k smallest elements from a stream.

    >>> maintain_k_smallest([5, 3, 8, 1, 9, 2, 7], 3)
    [1, 2, 3]

    Time: O(n log k)
    Space: O(k)
    """
    if not nums or k <= 0:
        return []

    # Max heap (negated) to track k smallest
    max_heap = []
    for num in nums:
        if len(max_heap) < k:
            heapq.heappush(max_heap, -num)
        elif num < -max_heap[0]:
            heapq.heapreplace(max_heap, -num)

    return sorted([-x for x in max_heap])
```

### 2. Priority Queue with Tiebreaker
**Difficulty:** Easy
**Concept:** (priority, counter, item) pattern

```python
class PriorityQueue:
    """
    Priority queue that handles any item type by using a counter for ties.

    >>> pq = PriorityQueue()
    >>> pq.push(1, "task A")
    >>> pq.push(1, "task B")
    >>> pq.pop()
    (1, 'task A')
    >>> pq.pop()
    (1, 'task B')
    """
    def __init__(self):
        self.heap = []
        self.counter = 0

    def push(self, priority: int, item: any) -> None:
        heapq.heappush(self.heap, (priority, self.counter, item))
        self.counter += 1

    def pop(self) -> any:
        priority, _, item = heapq.heappop(self.heap)
        return priority, item
```
