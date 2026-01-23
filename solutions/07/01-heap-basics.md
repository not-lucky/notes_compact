# Heap Basics

## Practice Problems

### 1. Kth Largest Element in a Stream
**Difficulty:** Easy
**Concept:** Maintain min heap of size k

```python
import heapq
from typing import List

class KthLargest:
    """
    Design a class to find the kth largest element in a stream.
    Note that it is the kth largest element in the sorted order,
    not the kth distinct element.

    >>> kth = KthLargest(3, [4, 5, 8, 2])
    >>> kth.add(3)
    4
    >>> kth.add(5)
    5
    >>> kth.add(10)
    5
    >>> kth.add(9)
    8
    >>> kth.add(4)
    8
    """
    def __init__(self, k: int, nums: List[int]):
        """
        Time: O(n log k)
        Space: O(k)
        """
        self.k = k
        self.min_heap = nums
        heapq.heapify(self.min_heap)
        while len(self.min_heap) > k:
            heapq.heappop(self.min_heap)

    def add(self, val: int) -> int:
        """
        Time: O(log k)
        Space: O(1)
        """
        if len(self.min_heap) < self.k:
            heapq.heappush(self.min_heap, val)
        elif val > self.min_heap[0]:
            heapq.heapreplace(self.min_heap, val)
        return self.min_heap[0]
```

### 2. Last Stone Weight
**Difficulty:** Easy
**Concept:** Max heap simulation

```python
def last_stone_weight(stones: List[int]) -> int:
    """
    You are given an array of integers stones where stones[i] is the weight
    of the ith stone. Each turn, we choose the heaviest two stones and smash
    them together.

    >>> last_stone_weight([2,7,4,1,8,1])
    1
    >>> last_stone_weight([1])
    1

    Time: O(n log n)
    Space: O(n)
    """
    # Max heap (negated)
    max_heap = [-s for s in stones]
    heapq.heapify(max_heap)

    while len(max_heap) > 1:
        s1 = -heapq.heappop(max_heap)
        s2 = -heapq.heappop(max_heap)
        if s1 != s2:
            heapq.heappush(max_heap, -(s1 - s2))

    return -max_heap[0] if max_heap else 0
```
