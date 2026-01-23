# Google Interview Patterns

## Practice Problems

### 1. LRU Cache
**Difficulty:** Medium
**Key Technique:** HashMap + Double Linked List

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

### 2. Word Search
**Difficulty:** Medium
**Key Technique:** DFS + Backtracking

```python
def exist(board: list[list[str]], word: str) -> bool:
    """
    Time: O(N * 3^L) where N is cells, L is word length
    Space: O(L)
    """
    rows, cols = len(board), len(board[0])
    def dfs(r, c, i):
        if i == len(word): return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[i]:
            return False
        temp = board[r][c]
        board[r][c] = '#'
        res = (dfs(r+1, c, i+1) or dfs(r-1, c, i+1) or
               dfs(r, c+1, i+1) or dfs(r, c-1, i+1))
        board[r][c] = temp
        return res

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0): return True
    return False
```

### 3. Word Ladder
**Difficulty:** Hard
**Key Technique:** BFS (Shortest path in graph)

```python
from collections import deque

def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    """
    Time: O(M^2 * N) where M is word length, N is list size
    Space: O(M^2 * N)
    """
    word_set = set(word_list)
    if end_word not in word_set: return 0
    q = deque([(begin_word, 1)])
    while q:
        word, dist = q.popleft()
        if word == end_word: return dist
        for i in range(len(word)):
            for char in "abcdefghijklmnopqrstuvwxyz":
                next_word = word[:i] + char + word[i+1:]
                if next_word in word_set:
                    word_set.remove(next_word)
                    q.append((next_word, dist + 1))
    return 0
```

### 4. Sliding Window Maximum
**Difficulty:** Hard
**Key Technique:** Monotonic Deque

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Time: O(n)
    Space: O(k)
    """
    dq = deque()
    res = []
    for i, n in enumerate(nums):
        while dq and nums[dq[-1]] < n:
            dq.pop()
        dq.append(i)
        if dq[0] == i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res
```
