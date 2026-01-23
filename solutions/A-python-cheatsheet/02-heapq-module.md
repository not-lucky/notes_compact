# Heapq Module

## Practice Problems

### 1. Kth Largest Element in an Array
**Difficulty:** Medium
**Key Technique:** Min-heap of size k

```python
import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    """
    Time: O(n log k)
    Space: O(k)
    """
    heap = nums[:k]
    heapq.heapify(heap)
    for n in nums[k:]:
        if n > heap[0]:
            heapq.heapreplace(heap, n)
    return heap[0]
```

### 2. Top K Frequent Elements
**Difficulty:** Medium
**Key Technique:** Counter + heap

```python
from collections import Counter
import heapq

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    Time: O(n log k)
    Space: O(n)
    """
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

### 3. Merge K Sorted Lists
**Difficulty:** Hard
**Key Technique:** Min-heap of size k

```python
import heapq

def merge_k_lists(lists: list[list[int]]) -> list[int]:
    """
    Time: O(N log k) where N is total elements
    Space: O(k)
    """
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    res = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        res.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            heapq.heappush(heap, (lists[list_idx][elem_idx+1], list_idx, elem_idx+1))
    return res
```

### 4. Find Median from Data Stream
**Difficulty:** Hard
**Key Technique:** Two heaps (Min-heap and Max-heap)

```python
import heapq

class MedianFinder:
    """
    Time: O(log n) for add, O(1) for median
    Space: O(n)
    """
    def __init__(self):
        self.small = [] # Max-heap
        self.large = [] # Min-heap

    def add_num(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0
```

### 5. Task Scheduler
**Difficulty:** Medium
**Key Technique:** Max-heap + simulation

```python
from collections import Counter
import heapq

def least_interval(tasks: list[str], n: int) -> int:
    """
    Time: O(T log 26) where T is total tasks
    Space: O(1) - only 26 characters
    """
    count = Counter(tasks)
    heap = [-c for c in count.values()]
    heapq.heapify(heap)

    time = 0
    while heap:
        temp = []
        for _ in range(n + 1):
            time += 1
            if heap:
                c = heapq.heappop(heap) + 1
                if c < 0: temp.append(c)
            if not heap and not temp: break
        for c in temp:
            heapq.heappush(heap, c)
    return time
```
