# Amazon Interview Patterns

## Practice Problems

### 1. Number of Islands
**Difficulty:** Medium
**Key Technique:** BFS/DFS (Customer Obsession: Optimizing for grid-based data)

```python
def num_islands(grid: list[list[str]]) -> int:
    """
    Time: O(m * n)
    Space: O(m * n)
    """
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        grid[r][c] = '0'
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count
```

### 2. Merge K Sorted Lists
**Difficulty:** Hard
**Key Technique:** Min-Heap (Ownership: Ensuring efficient merging for scale)

```python
import heapq

def merge_k_lists(lists: list[list[int]]) -> list[int]:
    """
    Time: O(N log k)
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

### 3. LRU Cache
**Difficulty:** Medium
**Key Technique:** OrderedDict (Highest Standards: O(1) performance)

```python
from collections import OrderedDict

class LRUCache:
    """
    Time: O(1)
    Space: O(capacity)
    """
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache: return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache: self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

### 4. Meeting Rooms II
**Difficulty:** Medium
**Key Technique:** Heap (Dive Deep: Efficiently finding minimum rooms)

```python
import heapq

def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """
    Time: O(n log n)
    Space: O(n)
    """
    if not intervals: return 0
    intervals.sort(key=lambda x: x[0])
    rooms = []
    heapq.heappush(rooms, intervals[0][1])
    for start, end in intervals[1:]:
        if start >= rooms[0]:
            heapq.heappop(rooms)
        heapq.heappush(rooms, end)
    return len(rooms)
```
