# Data Structure & Algorithm Selection

## Practice Problems

### 1. Two Sum
**Difficulty:** Easy
**Key Technique:** HashMap (Trade space for time)

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Time: O(n)
    Space: O(n)
    """
    seen = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in seen:
            return [seen[diff], i]
        seen[n] = i
    return []
```

### 2. Find Median from Data Stream
**Difficulty:** Hard
**Key Technique:** Two Heaps (Optimization for frequent median queries)

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

### 3. Number of Connected Components in an Undirected Graph
**Difficulty:** Medium
**Key Technique:** Union-Find vs DFS/BFS

```python
def count_components(n: int, edges: list[list[int]]) -> int:
    """
    Time: O(E * alpha(V)) where alpha is inverse Ackermann
    Space: O(V)
    """
    parent = list(range(n))
    def find(i):
        if parent[i] == i: return i
        parent[i] = find(parent[i])
        return parent[i]

    count = n
    for u, v in edges:
        root_u, root_v = find(u), find(v)
        if root_u != root_v:
            parent[root_u] = root_v
            count -= 1
    return count
```

### 4. K Closest Points to Origin
**Difficulty:** Medium
**Key Technique:** Max-Heap (O(n log k)) or QuickSelect (O(n))

```python
import heapq

def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Time: O(n log k)
    Space: O(k)
    """
    heap = []
    for x, y in points:
        dist = -(x*x + y*y)
        heapq.heappush(heap, (dist, [x, y]))
        if len(heap) > k:
            heapq.heappop(heap)
    return [p for d, p in heap]
```
