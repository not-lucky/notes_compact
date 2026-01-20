# LRU Cache

> **Prerequisites:** [Data Structure Choices](./01-data-structure-choices.md), Understanding of HashMap and Linked Lists

## Interview Context

LRU (Least Recently Used) Cache is one of the most frequently asked coding interview questions at FANG companies. It's a "must-know" problem that tests:

- Combining data structures creatively
- Achieving O(1) time complexity
- Understanding cache eviction policies
- Code organization and clean implementation

**LeetCode 146** is asked in virtually every company's interview pool.

---

## Pattern: HashMap + Doubly Linked List

The key insight is combining two structures:

```
HashMap: O(1) lookup by key → Node
Doubly Linked List: O(1) reordering (move to front, remove from end)

Together: O(1) get + O(1) put
```

### Visualization

```
HashMap                   Doubly Linked List
┌─────────┐              ┌──────┐   ┌──────┐   ┌──────┐
│ key1 ───┼─────────────→│ key1 │←→│ key2 │←→│ key3 │
├─────────┤              │ val1 │   │ val2 │   │ val3 │
│ key2 ───┼───────┐      └──────┘   └──────┘   └──────┘
├─────────┤       │        HEAD                   TAIL
│ key3 ───┼───┐   └──────────↑        (MRU)      (LRU)
└─────────┘   └──────────────┼──────────↑

On access: Move node to HEAD (most recently used)
On eviction: Remove from TAIL (least recently used)
```

---

## Implementation

### Using OrderedDict (Python's Built-in)

```python
from collections import OrderedDict

class LRUCache:
    """
    LRU Cache using Python's OrderedDict.

    OrderedDict maintains insertion order and allows
    moving items to the end in O(1).

    Time: O(1) for get and put
    Space: O(capacity)
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update and move to end
            self.cache.move_to_end(key)

        self.cache[key] = value

        # Evict if over capacity
        if len(self.cache) > self.capacity:
            # Remove first item (least recently used)
            self.cache.popitem(last=False)


# Test
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))       # 1
cache.put(3, 3)           # Evicts key 2
print(cache.get(2))       # -1 (not found)
cache.put(4, 4)           # Evicts key 1
print(cache.get(1))       # -1 (not found)
print(cache.get(3))       # 3
print(cache.get(4))       # 4
```

### From Scratch (HashMap + Doubly Linked List)

This is what interviewers usually want to see:

```python
class DLinkedNode:
    """Doubly linked list node."""
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    LRU Cache with HashMap + Doubly Linked List.

    Time: O(1) for get and put
    Space: O(capacity)
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> DLinkedNode

        # Dummy head and tail to avoid edge cases
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: DLinkedNode) -> None:
        """Add node right after head (most recently used)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: DLinkedNode) -> None:
        """Remove a node from the list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: DLinkedNode) -> None:
        """Move existing node to head (mark as most recently used)."""
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self) -> DLinkedNode:
        """Remove the tail node (least recently used) and return it."""
        node = self.tail.prev
        self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # Add new
            node = DLinkedNode(key, value)
            self.cache[key] = node
            self._add_to_head(node)

            if len(self.cache) > self.capacity:
                # Remove LRU (tail)
                lru = self._remove_tail()
                del self.cache[lru.key]


# Test
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))       # 1
cache.put(3, 3)           # Evicts key 2
print(cache.get(2))       # -1
cache.put(4, 4)           # Evicts key 1
print(cache.get(1))       # -1
print(cache.get(3))       # 3
print(cache.get(4))       # 4
```

---

## Why Doubly Linked List?

```
Singly Linked List:
- Remove from middle: O(n) - need to find previous node

Doubly Linked List:
- Remove from middle: O(1) - have direct access to prev

For LRU:
- We need to remove any node when it's accessed (to move to head)
- We need to remove tail when evicting
- Both require O(1) → Doubly Linked List
```

---

## Why Dummy Head/Tail?

Without dummy nodes, we'd have edge cases:

```python
# Without dummy nodes:
def _add_to_head(self, node):
    if self.head is None:
        self.head = self.tail = node
    else:
        node.next = self.head
        self.head.prev = node
        self.head = node

# With dummy nodes - always the same:
def _add_to_head(self, node):
    node.prev = self.head
    node.next = self.head.next
    self.head.next.prev = node
    self.head.next = node
```

Dummy nodes eliminate all null checks and edge cases.

---

## Complexity Analysis

| Operation | Time | Explanation |
|-----------|------|-------------|
| get() | O(1) | HashMap lookup + linked list move |
| put() (update) | O(1) | HashMap lookup + linked list move |
| put() (insert) | O(1) | HashMap insert + linked list add |
| put() (evict) | O(1) | Remove tail + delete from HashMap |

**Space: O(capacity)** - we store at most `capacity` nodes

---

## Common Variations

### 1. LRU Cache with TTL

```python
import time

class LRUCacheWithTTL(LRUCache):
    def __init__(self, capacity: int, ttl_seconds: int):
        super().__init__(capacity)
        self.ttl = ttl_seconds
        self.timestamps = {}  # key -> expiry time

    def get(self, key: int) -> int:
        if key in self.timestamps:
            if time.time() > self.timestamps[key]:
                self._evict(key)
                return -1
        return super().get(key)

    def put(self, key: int, value: int) -> None:
        super().put(key, value)
        self.timestamps[key] = time.time() + self.ttl

    def _evict(self, key: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            self._remove_node(node)
            del self.cache[key]
            del self.timestamps[key]
```

### 2. LRU Cache with Get Callback

```python
class LRUCacheWithCallback:
    """LRU Cache that fetches missing values."""

    def __init__(self, capacity: int, fetch_func):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.fetch_func = fetch_func

    def get(self, key: int) -> int:
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]

        # Cache miss - fetch value
        value = self.fetch_func(key)
        self.put(key, value)
        return value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# Usage
def expensive_fetch(key):
    # Simulate database lookup
    return key * 100

cache = LRUCacheWithCallback(10, expensive_fetch)
```

### 3. Thread-Safe LRU Cache

```python
from threading import Lock
from collections import OrderedDict

class ThreadSafeLRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.lock = Lock()

    def get(self, key: int) -> int:
        with self.lock:
            if key not in self.cache:
                return -1
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: int, value: int) -> None:
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
```

---

## Edge Cases

1. **Capacity 1**: Only one item, every put evicts
2. **Get non-existent key**: Return -1
3. **Put existing key**: Update value, move to head
4. **Put then immediate get**: Should work
5. **Eviction order**: Oldest accessed item goes first

---

## Interview Tips

1. **Explain the design first**: "I'll use HashMap for O(1) lookup and doubly linked list for O(1) reordering"
2. **Draw the structure**: Show how nodes connect
3. **Use dummy nodes**: Explain why they simplify code
4. **Mention OrderedDict**: Shows you know Python, but implement from scratch
5. **Discuss extensions**: TTL, thread safety, distributed caching

### Common Interview Follow-ups

```
Q: How would you make this distributed?
A: Consistent hashing to partition keys across nodes,
   or use Redis which has built-in LRU eviction.

Q: How would you handle concurrent access?
A: Add locks around get/put, or use lock-free structures
   with CAS operations.

Q: What if cache misses are expensive?
A: Add a callback function to fetch on miss,
   or use read-through caching pattern.
```

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | LRU Cache | Medium | Core implementation |
| 2 | Design Linked List | Medium | Practice DLL operations |
| 3 | All O(1) Data Structure | Hard | Similar combination pattern |
| 4 | Design Browser History | Medium | Simpler linked list |
| 5 | LRU Cache (Follow-up) | Hard | With TTL or persistence |

---

## Related Sections

- [Data Structure Choices](./01-data-structure-choices.md) - When to use which structure
- [LFU Cache](./03-lfu-cache.md) - More complex eviction policy
