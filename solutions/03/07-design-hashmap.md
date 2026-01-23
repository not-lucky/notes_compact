# Design HashMap

## Practice Problems

### 1. Design HashMap (Separate Chaining)
**Difficulty:** Easy
**Key Technique:** Array of buckets with list of pairs

```python
class MyHashMap:
    """
    Design a HashMap without using built-in hash table libraries.
    Time: O(N/K) where N is total keys, K is buckets
    Space: O(N + K)
    """
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def put(self, key: int, value: int) -> None:
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx][i] = (key, value)
                return
        self.buckets[idx].append((key, value))

    def get(self, key: int) -> int:
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx].pop(i)
                return
```

### 2. Design HashSet
**Difficulty:** Easy
**Key Technique:** Array of buckets with list of values

```python
class MyHashSet:
    """
    Time: O(N/K)
    Space: O(N + K)
    """
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def add(self, key: int) -> None:
        idx = self._hash(key)
        if key not in self.buckets[idx]:
            self.buckets[idx].append(key)

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        if key in self.buckets[idx]:
            self.buckets[idx].remove(key)

    def contains(self, key: int) -> bool:
        idx = self._hash(key)
        return key in self.buckets[idx]
```

### 3. LRU Cache
**Difficulty:** Medium
**Key Technique:** HashMap + Doubly Linked List

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    """
    Design a data structure that follows the Least Recently Used (LRU) cache policy.
    Time: O(1) for both get and put
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
            self._remove(self.cache[key])
            self._add(self.cache[key])
            return self.cache[key].val
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

### 4. Insert Delete GetRandom O(1)
**Difficulty:** Medium
**Key Technique:** HashMap + Array

```python
import random

class RandomizedSet:
    """
    Time: O(1) average for all operations
    Space: O(n)
    """
    def __init__(self):
        self.nums = []
        self.pos = {} # val -> index

    def insert(self, val: int) -> bool:
        if val in self.pos: return False
        self.pos[val] = len(self.nums)
        self.nums.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.pos: return False
        idx, last = self.pos[val], self.nums[-1]
        self.nums[idx] = last
        self.pos[last] = idx
        self.nums.pop()
        del self.pos[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)
```
