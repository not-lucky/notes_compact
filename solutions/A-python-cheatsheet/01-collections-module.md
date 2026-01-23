# Collections Module

## Practice Problems

### 1. Valid Anagram
**Difficulty:** Easy
**Key Technique:** Counter

```python
from collections import Counter

def is_anagram(s: str, t: str) -> bool:
    """
    Time: O(n)
    Space: O(1) - alphabet size is fixed
    """
    return Counter(s) == Counter(t)
```

### 2. Top K Frequent Elements
**Difficulty:** Medium
**Key Technique:** Counter + heapq.nlargest

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

### 3. Group Anagrams
**Difficulty:** Medium
**Key Technique:** defaultdict(list)

```python
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Time: O(n * k log k) where k is max length of string
    Space: O(n * k)
    """
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())
```

### 4. Sliding Window Maximum
**Difficulty:** Hard
**Key Technique:** deque (Monotonic)

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Time: O(n)
    Space: O(k)
    """
    dq = deque()  # Store indices
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

### 5. LRU Cache
**Difficulty:** Medium
**Key Technique:** OrderedDict

```python
from collections import OrderedDict

class LRUCache:
    """
    Time: O(1) for get and put
    Space: O(capacity)
    """
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```
