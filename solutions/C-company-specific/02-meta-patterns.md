# Meta Interview Patterns

## Practice Problems

### 1. Valid Parentheses
**Difficulty:** Easy
**Key Technique:** Stack (Velocity target: 8 min)

```python
def is_valid(s: str) -> bool:
    """
    Time: O(n)
    Space: O(n)
    """
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top: return False
        else:
            stack.append(char)
    return not stack
```

### 2. Merge Intervals
**Difficulty:** Medium
**Key Technique:** Sorting + Iteration (Velocity target: 10 min)

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Time: O(n log n)
    Space: O(n)
    """
    if not intervals: return []
    intervals.sort(key=lambda x: x[0])
    res = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= res[-1][1]:
            res[-1][1] = max(res[-1][1], end)
        else:
            res.append([start, end])
    return res
```

### 3. LRU Cache
**Difficulty:** Medium
**Key Technique:** OrderedDict (Velocity target: 18 min)

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

### 4. Number of Islands
**Difficulty:** Medium
**Key Technique:** DFS/BFS (Velocity target: 15 min)

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
