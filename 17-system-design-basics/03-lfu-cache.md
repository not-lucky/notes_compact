# LFU Cache

> **Prerequisites:** [LRU Cache](./02-lru-cache.md), Understanding of frequency-based eviction

## Interview Context

LFU (Least Frequently Used) Cache is a harder variant of LRU Cache. It's asked at senior-level interviews and tests:

- Managing multiple data structures simultaneously
- Handling tie-breaking logic (when frequencies are equal)
- Maintaining O(1) complexity for all operations
- Clean code organization with complex state

**LeetCode 460** is considered a "Hard" problem.

---

## Pattern: HashMap + Frequency Buckets

The key insight is tracking frequencies and maintaining a "minimum frequency" pointer:

```
Three HashMaps:
1. key → (value, frequency)     # Main cache
2. key → Node                   # For O(1) node access
3. frequency → DoublyLinkedList # Nodes with same frequency

Plus: min_freq variable to find LFU quickly
```

### Visualization

```
Main HashMap: key → Node(key, val, freq)

Frequency Map:
freq=1: [Node3] ← min_freq points here (LFU candidates)
freq=2: [Node1, Node5]
freq=3: [Node2, Node4]

On access to Node5:
1. Remove from freq=2 list
2. Increment freq to 3
3. Add to freq=3 list
4. Update min_freq if freq=2 list is now empty
```

---

## Implementation

### O(1) LFU Cache (Full Implementation)

```python
from collections import defaultdict

class DLinkedNode:
    """Doubly linked list node."""
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.freq = 1
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """
    Doubly linked list with dummy head/tail.
    Used to maintain insertion order within a frequency bucket.
    """
    def __init__(self):
        self.head = DLinkedNode()  # Dummy
        self.tail = DLinkedNode()  # Dummy
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_first(self, node: DLinkedNode) -> None:
        """Add node at the front (most recent within frequency)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node: DLinkedNode) -> None:
        """Remove a specific node."""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def remove_last(self) -> DLinkedNode:
        """Remove and return the last node (LRU within this frequency)."""
        if self.size == 0:
            return None
        last = self.tail.prev
        self.remove(last)
        return last

    def is_empty(self) -> bool:
        return self.size == 0


class LFUCache:
    """
    LFU Cache with O(1) get and put.

    Uses:
    - HashMap: key → Node (for O(1) lookup)
    - HashMap: frequency → DoublyLinkedList (nodes with same freq)
    - Variable: min_freq (to find LFU in O(1))

    Time: O(1) for get and put
    Space: O(capacity)
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.cache = {}  # key → DLinkedNode
        self.freq_map = defaultdict(DoublyLinkedList)  # freq → DLL

    def _update_freq(self, node: DLinkedNode) -> None:
        """Increment frequency and move node to new frequency bucket."""
        freq = node.freq
        self.freq_map[freq].remove(node)

        # Update min_freq if this bucket is now empty
        if self.freq_map[freq].is_empty() and self.min_freq == freq:
            self.min_freq += 1

        node.freq += 1
        self.freq_map[node.freq].add_first(node)

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._update_freq(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.cache:
            # Update existing key
            node = self.cache[key]
            node.value = value
            self._update_freq(node)
        else:
            # Evict if at capacity
            if len(self.cache) >= self.capacity:
                # Remove LFU (and LRU among LFU)
                lfu_list = self.freq_map[self.min_freq]
                lfu_node = lfu_list.remove_last()
                del self.cache[lfu_node.key]

            # Add new key
            node = DLinkedNode(key, value)
            self.cache[key] = node
            self.freq_map[1].add_first(node)
            self.min_freq = 1  # New node always has freq=1


# Test
cache = LFUCache(2)
cache.put(1, 1)       # freq: {1:1}
cache.put(2, 2)       # freq: {1:1, 2:1}
print(cache.get(1))   # 1, freq: {1:2, 2:1}
cache.put(3, 3)       # Evicts key 2 (LFU), freq: {1:2, 3:1}
print(cache.get(2))   # -1 (not found)
print(cache.get(3))   # 3, freq: {1:2, 3:2}
cache.put(4, 4)       # Evicts key 1 (same freq as 3, but 1 is LRU)
print(cache.get(1))   # -1 (not found)
print(cache.get(3))   # 3
print(cache.get(4))   # 4
```

---

## Why This Design Achieves O(1)

### get(key) - O(1)

```
1. HashMap lookup: O(1)
2. Remove from current freq list: O(1) - doubly linked
3. Add to new freq list: O(1)
4. Update min_freq: O(1) - just check if list is empty
```

### put(key, value) - O(1)

```
Existing key:
1. HashMap lookup: O(1)
2. Update value: O(1)
3. Update freq (same as get): O(1)

New key:
1. Check capacity and evict: O(1)
   - Find min_freq list: O(1)
   - Remove last node: O(1)
   - Delete from cache: O(1)
2. Create and add node: O(1)
3. Set min_freq = 1: O(1)
```

---

## Tie-Breaking: When Frequencies Are Equal

When multiple keys have the same minimum frequency, we evict the **Least Recently Used** among them.

```
freq=1: [A, B, C]  ← if min_freq=1 and need to evict
                     evict C (oldest/last in the list)

This is why we use a DoublyLinkedList within each frequency:
- New/accessed items go to the front
- Evictions remove from the back
```

---

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| get() | O(1) | - |
| put() (update) | O(1) | - |
| put() (insert) | O(1) | - |
| put() (evict) | O(1) | - |

**Space: O(capacity)** for the cache entries

---

## Common Variations

### 1. Simplified LFU (O(log n) using Heap)

If O(1) isn't required, a heap-based approach is simpler:

```python
import heapq

class LFUCacheHeap:
    """
    Simpler LFU with O(log n) operations.
    Uses min-heap keyed by (frequency, time, key).
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key → value
        self.freq = {}   # key → frequency
        self.time = {}   # key → last access time
        self.heap = []   # (freq, time, key)
        self.counter = 0

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        self.freq[key] += 1
        self.counter += 1
        self.time[key] = self.counter
        heapq.heappush(self.heap, (self.freq[key], self.time[key], key))

        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.cache:
            self.cache[key] = value
            self.get(key)  # Update frequency
            return

        if len(self.cache) >= self.capacity:
            self._evict()

        self.cache[key] = value
        self.freq[key] = 1
        self.counter += 1
        self.time[key] = self.counter
        heapq.heappush(self.heap, (1, self.counter, key))

    def _evict(self) -> None:
        while self.heap:
            freq, time, key = heapq.heappop(self.heap)
            # Check if this entry is stale
            if key in self.cache and self.freq[key] == freq and self.time[key] == time:
                del self.cache[key]
                del self.freq[key]
                del self.time[key]
                return
```

### 2. LFU with Decay (Aging)

In production, pure LFU can suffer from "old popular items" staying forever:

```python
class LFUWithDecay:
    """
    LFU where frequencies decay over time.
    Periodically halve all frequencies to allow old items to be evicted.
    """

    def __init__(self, capacity: int, decay_interval: int = 100):
        self.capacity = capacity
        self.decay_interval = decay_interval
        self.ops_count = 0
        self.cache = {}  # key → (value, frequency)

    def _maybe_decay(self):
        self.ops_count += 1
        if self.ops_count >= self.decay_interval:
            self.ops_count = 0
            for key in self.cache:
                value, freq = self.cache[key]
                self.cache[key] = (value, max(1, freq // 2))

    def get(self, key: int) -> int:
        self._maybe_decay()
        if key not in self.cache:
            return -1
        value, freq = self.cache[key]
        self.cache[key] = (value, freq + 1)
        return value

    # ... put with eviction of min frequency
```

### 3. LFU vs LRU Hybrid

```python
class LRFUCache:
    """
    Combines recency and frequency with weighted scoring.
    score = frequency * alpha + recency * (1 - alpha)
    """
    pass  # Implementation depends on weight parameter
```

---

## LRU vs LFU: When to Use Each

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| General caching | LRU | Simpler, works well for most access patterns |
| Hot/cold data | LFU | Frequently accessed items stay cached |
| Streaming data | LRU | Recent items more likely to be accessed |
| Static popular content | LFU | Popular items don't get evicted |
| Mixed workload | LRU | More predictable behavior |

---

## Edge Cases

1. **Capacity 0**: All operations should handle gracefully
2. **Capacity 1**: Every new key evicts the previous
3. **Same frequency tie**: Use LRU among same-frequency items
4. **Frequency overflow**: In practice, use modular frequency or decay
5. **Get updates frequency**: Don't forget get() increments freq

---

## Interview Tips

1. **Explain the three maps**: Make the design clear upfront
2. **Draw frequency buckets**: Visual helps understanding
3. **Mention the tie-breaker**: LRU within same frequency
4. **Start with LRU**: "This builds on LRU but adds frequency tracking"
5. **Know the tradeoffs**: LFU is more complex but better for some patterns

### Common Interview Follow-ups

```
Q: When would LFU perform worse than LRU?
A: When access patterns change over time. Old frequent items
   stay cached even if they're no longer popular.

Q: How would you handle this in production?
A: Add frequency decay - periodically reduce all frequencies
   so old items can eventually be evicted.

Q: What about thread safety?
A: Use fine-grained locks per frequency bucket, or
   lock-free structures with CAS operations.
```

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | LFU Cache | Hard | Core implementation |
| 2 | LRU Cache | Medium | Prerequisite |
| 3 | All O(1) Data Structure | Hard | Similar multi-map design |
| 4 | Design Hit Counter | Medium | Frequency counting |
| 5 | First Unique Character in Stream | Medium | Frequency + order tracking |

---

## Related Sections

- [LRU Cache](./02-lru-cache.md) - Simpler eviction policy
- [Data Structure Choices](./01-data-structure-choices.md) - When to use each
