# Advanced HashMap Patterns

## Practice Problems

### 1. LRU Cache
**Difficulty:** Medium
**Key Technique:** HashMap + Doubly Linked List

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    """
    Time: O(1)
    Space: O(capacity)
    """
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {} # key -> Node
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _add(self, node):
        prev, nxt = self.tail.prev, self.tail
        prev.next = nxt.prev = node
        node.prev, node.next = prev, nxt

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        self.cache[key] = Node(key, value)
        self._add(self.cache[key])
        if len(self.cache) > self.cap:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]
```

### 2. LFU Cache
**Difficulty:** Hard
**Key Technique:** Multiple HashMaps + Frequency Buckets

```python
from collections import defaultdict, OrderedDict

class LFUCache:
    """
    Time: O(1)
    Space: O(capacity)
    """
    def __init__(self, capacity: int):
        self.cap = capacity
        self.min_f = 0
        self.cache = {} # key -> [val, freq]
        self.freq = defaultdict(OrderedDict) # freq -> {key: None}

    def _update(self, key):
        val, f = self.cache[key]
        self.freq[f].pop(key)
        if not self.freq[f] and f == self.min_f:
            self.min_f += 1
        self.cache[key][1] += 1
        self.freq[f+1][key] = None

    def get(self, key: int) -> int:
        if key not in self.cache: return -1
        self._update(key)
        return self.cache[key][0]

    def put(self, key: int, value: int) -> None:
        if self.cap <= 0: return
        if key in self.cache:
            self.cache[key][0] = value
            self._update(key)
            return
        if len(self.cache) >= self.cap:
            k, _ = self.freq[self.min_f].popitem(last=False)
            del self.cache[k]
        self.cache[key] = [value, 1]
        self.freq[1][key] = None
        self.min_f = 1
```

### 3. Insert Delete GetRandom O(1)
**Difficulty:** Medium
**Key Technique:** HashMap + Array + Swap-to-end

```python
import random

class RandomizedSet:
    """
    Time: O(1)
    Space: O(n)
    """
    def __init__(self):
        self.data = []
        self.pos = {} # val -> index

    def insert(self, val: int) -> bool:
        if val in self.pos: return False
        self.pos[val] = len(self.data)
        self.data.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.pos: return False
        idx, last = self.pos[val], self.data[-1]
        self.data[idx] = last
        self.pos[last] = idx
        self.data.pop()
        del self.pos[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.data)
```

### 4. Time Based Key-Value Store
**Difficulty:** Medium
**Key Technique:** HashMap + Binary Search on Timestamps

```python
import bisect
from collections import defaultdict

class TimeMap:
    """
    Time: O(1) set, O(log N) get
    Space: O(N)
    """
    def __init__(self):
        self.store = defaultdict(list) # key -> [(timestamp, value)]

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store: return ""
        arr = self.store[key]
        idx = bisect.bisect_right(arr, (timestamp, chr(127)))
        return arr[idx-1][1] if idx else ""
```
