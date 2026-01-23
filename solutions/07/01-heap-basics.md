# Heaps and Priority Queues

## Practice Problems

### 1. Top K Frequent Elements
**Difficulty:** Medium
**Concept:** Frequency + heap

```python
import heapq
from collections import Counter
from typing import List

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Finds the k most frequent elements.
    Time: O(n log k)
    Space: O(n) for counter
    """
    count = Counter(nums)
    # Min heap of (frequency, value)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

### 2. Kth Largest Element in an Array
**Difficulty:** Medium
**Concept:** Core top-k

```python
def find_kth_largest(nums: List[int], k: int) -> int:
    """
    Finds the kth largest element using a min heap of size k.
    Time: O(n log k)
    Space: O(k)
    """
    heap = nums[:k]
    heapq.heapify(heap)
    for i in range(k, len(nums)):
        if nums[i] > heap[0]:
            heapq.heapreplace(heap, nums[i])
    return heap[0]
```

### 3. Merge k Sorted Lists
**Difficulty:** Hard
**Concept:** Merging with heap

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merges k sorted linked lists.
    Time: O(n log k)
    Space: O(k)
    """
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode()
    curr = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

### 4. Find Median from Data Stream
**Difficulty:** Hard
**Concept:** Two heaps (Min-Max)

```python
class MedianFinder:
    def __init__(self):
        """
        Maintains two heaps:
        1. max_heap (small half): largest of the smaller elements
        2. min_heap (large half): smallest of the larger elements
        """
        self.small = [] # max_heap (negated)
        self.large = [] # min_heap

    def add_num(self, num: int) -> None:
        # Add to small half
        heapq.heappush(self.small, -num)

        # Make sure every num in small is <= every num in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Balance sizes
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        if len(self.large) > len(self.small):
            return self.large[0]
        return (-self.small[0] + self.large[0]) / 2.0
```

### 5. Task Scheduler
**Difficulty:** Medium
**Concept:** Greedy + heap

```python
def least_interval(tasks: List[str], n: int) -> int:
    """
    Calculates the least number of intervals to finish all tasks with cooldown n.
    Time: O(n_tasks)
    Space: O(1) - only 26 characters
    """
    counts = Counter(tasks)
    max_heap = [-cnt for cnt in counts.values()]
    heapq.heapify(max_heap)

    time = 0
    queue = deque() # [(rem_cnt, available_time)]

    while max_heap or queue:
        time += 1
        if max_heap:
            cnt = 1 + heapq.heappop(max_heap)
            if cnt:
                queue.append((cnt, time + n))

        if queue and queue[0][1] == time:
            heapq.heappush(max_heap, queue.popleft()[0])

    return time
```

### 6. K Closest Points to Origin
**Difficulty:** Medium
**Concept:** Distance-based heap

```python
def k_closest(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Finds k closest points to (0,0).
    Time: O(n log k)
    Space: O(k)
    """
    max_heap = []
    for x, y in points:
        dist = -(x*x + y*y)
        if len(max_heap) < k:
            heapq.heappush(max_heap, (dist, x, y))
        elif dist > max_heap[0][0]:
            heapq.heapreplace(max_heap, (dist, x, y))

    return [[x, y] for d, x, y in max_heap]
```
