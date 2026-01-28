# Solutions for LFU Cache

This file provides optimal Python solutions for practice problems related to Least Frequently Used (LFU) cache and frequency-based patterns.

## 1. LFU Cache (Standard)

### Problem Statement
Design and implement a data structure for a Least Frequently Used (LFU) cache. It should support `get(key)` and `put(key, value)`. When the cache reaches its capacity, it should invalidate the least frequently used item before inserting a new item. If there is a tie (multiple keys with the same minimum frequency), the **Least Recently Used (LRU)** key among them should be invalidated.

### Examples & Edge Cases
- **Example**: `capacity = 2`. `put(1, 1)`, `put(2, 2)`, `get(1)` (freq=2), `put(3, 3)` (evicts 2 because freq=1), `get(2)` -> -1.
- **Edge Cases**:
  - Capacity = 0: Ignore all operations.
  - All items have the same frequency: Tie-breaks using LRU.
  - Updating a key: Increases its frequency and updates value.

### Optimal Python Solution
```python
from collections import defaultdict

class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_at_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def remove_tail(self):
        if self.size == 0: return None
        node = self.tail.prev
        self.remove(node)
        return node

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self.min_freq = 0
        self.cache = {} # key -> Node
        self.freq_map = defaultdict(DoublyLinkedList) # freq -> DLL

    def _update_node(self, node):
        freq = node.freq
        self.freq_map[freq].remove(node)
        if freq == self.min_freq and self.freq_map[freq].size == 0:
            self.min_freq += 1

        node.freq += 1
        self.freq_map[node.freq].add_at_head(node)

    def get(self, key: int) -> int:
        if key not in self.cache: return -1
        node = self.cache[key]
        self._update_node(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0: return

        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._update_node(node)
        else:
            if self.size == self.capacity:
                lru_node = self.freq_map[self.min_freq].remove_tail()
                del self.cache[lru_node.key]
                self.size -= 1

            new_node = Node(key, value)
            self.cache[key] = new_node
            self.freq_map[1].add_at_head(new_node)
            self.min_freq = 1
            self.size += 1
```

### Explanation
We use two HashMaps:
1. `cache`: Maps `key` to its `Node` for $O(1)$ access.
2. `freq_map`: Maps a frequency value to a **Doubly Linked List** of nodes that have that frequency.
The DLL inside `freq_map` handles the LRU tie-breaking (new/accessed items go to the head, tail is evicted). `min_freq` is maintained to find the LFU bucket in $O(1)$.

### Complexity Analysis
- **Time Complexity**: $O(1)$ for both `get` and `put`.
- **Space Complexity**: $O(\text{capacity})$ for storing the entries.

---

## 2. LRU Cache (See 17/02)
*Note: This problem is a prerequisite and is covered in detail in the [LRU Cache Solution File](./02-lru-cache.md). The implementation uses a HashMap and a single Doubly Linked List.*

---

## 3. All O(1) Data Structure
*Note: This problem also involves tracking frequencies and is covered in the [LRU Cache Solution File](./02-lru-cache.md#3-all-o1-data-structure).*

---

## 4. Design Hit Counter

### Problem Statement
Design a hit counter which counts the number of hits received in the past 5 minutes (300 seconds).
- `recordHit(timestamp)`
- `getHits(timestamp)`

### Examples & Edge Cases
- **Example**: `hit(1)`, `hit(2)`, `hit(3)`, `getHits(4)` -> 3, `hit(300)`, `getHits(300)` -> 4, `getHits(301)` -> 3.
- **Edge Cases**:
  - Concurrent hits at the same timestamp.
  - Long periods of inactivity.

### Optimal Python Solution
```python
class HitCounter:
    def __init__(self):
        # We store hits in 300 buckets (one per second)
        self.window = 300
        self.hits = [0] * self.window
        self.times = [0] * self.window

    def hit(self, timestamp: int) -> None:
        idx = timestamp % self.window
        if self.times[idx] != timestamp:
            self.times[idx] = timestamp
            self.hits[idx] = 1
        else:
            self.hits[idx] += 1

    def getHits(self, timestamp: int) -> int:
        total = 0
        for i in range(self.window):
            if timestamp - self.times[i] < self.window:
                total += self.hits[i]
        return total
```

### Explanation
Instead of storing a massive list of timestamps, we use **Buckets**. Since we only care about the last 300 seconds, we use an array of size 300. Each index corresponds to `timestamp % 300`.
- If a new hit arrives at a timestamp that has been "lapsed" (old data at that index), we reset the count.
- `getHits` sums up all buckets that are within the 300s window.

### Complexity Analysis
- **Time Complexity**:
  - `hit`: $O(1)$.
  - `getHits`: $O(300) = O(1)$ since the window size is constant.
- **Space Complexity**: $O(1)$ as we only ever use 300 buckets.

---

## 5. First Unique Character in Stream

### Problem Statement
Given a stream of characters, find the first unique character in the stream at any given moment.

### Examples & Edge Cases
- **Examples**: Stream: "a", "a", "b", "c" -> first unique after "a" is "a", after second "a" is None, after "b" is "b", after "c" is "b".
- **Edge Cases**:
  - All characters repeated.
  - Stream with many unique characters.

### Optimal Python Solution
```python
from collections import OrderedDict

class FirstUnique:
    def __init__(self, nums: list[int]):
        self.counts = {} # num -> count
        self.uniques = OrderedDict() # num -> None (preserves order)
        for n in nums:
            self.add(n)

    def showFirstUnique(self) -> int:
        if not self.uniques:
            return -1
        # OrderedDict gives the first inserted element in O(1)
        return next(iter(self.uniques))

    def add(self, value: int) -> None:
        if value not in self.counts:
            self.counts[value] = 1
            self.uniques[value] = None
        else:
            self.counts[value] += 1
            if value in self.uniques:
                del self.uniques[value]
```

### Explanation
We use an **OrderedDict** to keep track of characters that have appeared exactly once.
1. When a character is seen for the first time, add it to `uniques`.
2. When seen a second time, remove it from `uniques`.
3. If seen more than twice, it's already gone from `uniques`, so we do nothing.
The first item in the `OrderedDict` is always the first unique character.

### Complexity Analysis
- **Time Complexity**:
  - `add`: $O(1)$.
  - `showFirstUnique`: $O(1)$.
- **Space Complexity**: $O(N)$ where $N$ is the number of distinct characters in the stream.
