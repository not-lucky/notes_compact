# Advanced HashMap Patterns - Solutions

## 1. LRU Cache
Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

### Optimal Python Solution
```python
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """
    HashMap for O(1) access to nodes.
    Doubly Linked List for O(1) removal and insertion at the front (most recent).
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # key -> node
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        p, n = node.prev, node.next
        p.next, n.prev = n, p

    def _add(self, node):
        # Add to the front (next to head)
        h_next = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = h_next
        h_next.prev = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])

        node = Node(key, value)
        self._add(node)
        self.cache[key] = node

        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

---

## 2. LFU Cache
Design a data structure that follows the constraints of a Least Frequently Used (LFU) cache.

### Optimal Python Solution
```python
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # key -> (value, frequency)
        self.freq_map = defaultdict(OrderedDict) # frequency -> keys
        self.min_freq = 0

    def get(self, key: int) -> int:
        if key not in self.cache: return -1
        val, freq = self.cache[key]
        self._update(key, val, freq)
        return val

    def _update(self, key, val, freq):
        # Move key from current freq to freq + 1
        del self.freq_map[freq][key]
        if not self.freq_map[freq] and self.min_freq == freq:
            self.min_freq += 1
        self.cache[key] = (val, freq + 1)
        self.freq_map[freq + 1][key] = None

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0: return
        if key in self.cache:
            _, freq = self.cache[key]
            self._update(key, value, freq)
            return

        if len(self.cache) >= self.capacity:
            # Evict LFU (and LRU if tied)
            evict_key, _ = self.freq_map[self.min_freq].popitem(last=False)
            del self.cache[evict_key]

        self.cache[key] = (value, 1)
        self.freq_map[1][key] = None
        self.min_freq = 1
```

---

## 3. Insert Delete GetRandom O(1)
Implement `RandomizedSet` class.

### Optimal Python Solution
```python
import random

class RandomizedSet:
    def __init__(self):
        self.dict = {} # val -> index
        self.list = []

    def insert(self, val: int) -> bool:
        if val in self.dict: return False
        self.dict[val] = len(self.list)
        self.list.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.dict: return False
        # Move last element to the slot of the element to delete
        idx, last = self.dict[val], self.list[-1]
        self.list[idx], self.dict[last] = last, idx
        self.list.pop()
        del self.dict[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.list)
```

---

## 4. Insert Delete GetRandom O(1) - Duplicates Allowed
Similar to above, but `self.dict` maps `val` to a `set` of indices.

---

## 5. Time Based Key-Value Store
Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

### Optimal Python Solution
```python
import bisect
from collections import defaultdict

class TimeMap:
    def __init__(self):
        self.store = defaultdict(list) # key -> list of (timestamp, value)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        arr = self.store[key]
        # Binary search for the largest timestamp <= target
        idx = bisect.bisect_right(arr, (timestamp, chr(127)))
        return arr[idx-1][1] if idx else ""
```

---

## 6. Snapshot Array
Implement a `SnapshotArray` that supports `set`, `snap`, and `get` operations.

### Optimal Python Solution
```python
import bisect

class SnapshotArray:
    def __init__(self, length: int):
        # index -> list of (snap_id, value)
        self.arr = [[(-1, 0)] for _ in range(length)]
        self.snap_id = 0

    def set(self, index: int, val: int) -> None:
        self.arr[index].append((self.snap_id, val))

    def snap(self) -> int:
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        idx = bisect.bisect_right(self.arr[index], (snap_id, float('inf')))
        return self.arr[index][idx-1][1]
```

---

## 7. All O'one Data Structure
Design a data structure to store strings' counts with `inc`, `dec`, `getMaxKey`, `getMinKey` in O(1) time.
Implemented using HashMap + DLL of frequency buckets.

---

## 8. Logger Rate Limiter
(Discussed in Design HashMap file).

---

## 9. Design Twitter
Design a simplified version of Twitter where users can post tweets, follow/unfollow each other and is able to see the 10 most recent tweets in the user's news feed.
Implemented using HashMap for following relationships and Heaps to merge tweet lists from followed users.

---

## 10. Design Hit Counter
Design a hit counter which counts the number of hits received in the past 5 minutes (300 seconds).
Implemented using a queue or a fixed-size array of 300 buckets (circular buffer).
