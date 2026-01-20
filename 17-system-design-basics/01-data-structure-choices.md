# Data Structure Choices for System Design

> **Prerequisites:** Knowledge of basic data structures (HashMap, Trees, Heaps)

## Interview Context

System design interviews frequently ask "why did you choose X over Y?" This section covers the trade-offs between common data structures in real-world scenarios. Understanding these trade-offs shows maturity and experience.

---

## The Big Three: HashMap vs Tree vs Heap

### Quick Reference

| Operation | HashMap | BST/TreeMap | Heap |
|-----------|---------|-------------|------|
| Search | O(1) avg | O(log n) | O(n) |
| Insert | O(1) avg | O(log n) | O(log n) |
| Delete | O(1) avg | O(log n) | O(log n)* |
| Min/Max | O(n) | O(log n) | O(1) |
| Range Query | O(n) | O(log n + k) | O(n) |
| Ordered Iteration | O(n log n) | O(n) | O(n log n) |

*Delete by value in heap is O(n) to find + O(log n) to remove

---

## When to Use HashMap

**Choose HashMap when:**
- You need O(1) lookup by key
- Order doesn't matter
- No range queries needed
- Keys are hashable

### Use Cases

```python
# 1. Caching (fast lookups)
cache = {}
cache["user_123"] = user_data

# 2. Counting frequencies
from collections import Counter
word_count = Counter(words)

# 3. Deduplication
seen = set()  # HashSet is just HashMap with no values

# 4. Two-sum style problems
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

### Limitations

```
- No ordering (can't iterate in sorted order)
- No range queries (can't find "all keys between A and B")
- Hash collisions can degrade to O(n) in pathological cases
- Memory overhead for sparse key spaces
```

---

## When to Use Tree (BST/TreeMap/TreeSet)

**Choose Tree when:**
- You need ordered data
- Range queries are required
- You need floor/ceiling operations
- Keys have natural ordering

### Use Cases

```python
# Python doesn't have TreeMap, but conceptually:
from sortedcontainers import SortedDict

# 1. Sorted data with fast updates
calendar = SortedDict()
calendar[event_time] = event_data

# 2. Range queries
def events_between(start, end):
    # O(log n + k) where k = number of results
    return calendar.irange(start, end)

# 3. Floor/ceiling (nearest key)
def find_nearest_event(time):
    idx = calendar.bisect_left(time)
    # Check calendar[idx] and calendar[idx-1]

# 4. Time-based key-value store
class TimeMap:
    def __init__(self):
        self.store = {}  # key -> SortedDict of (timestamp, value)

    def set(self, key, value, timestamp):
        if key not in self.store:
            self.store[key] = SortedDict()
        self.store[key][timestamp] = value

    def get(self, key, timestamp):
        if key not in self.store:
            return ""
        times = self.store[key]
        idx = times.bisect_right(timestamp) - 1
        if idx < 0:
            return ""
        return times.peekitem(idx)[1]
```

### Limitations

```
- Slower than HashMap for simple lookups (O(log n) vs O(1))
- More complex implementation
- Requires comparable keys
```

---

## When to Use Heap

**Choose Heap when:**
- You need quick access to min or max
- Top-K problems
- Priority scheduling
- Streaming data (can't sort upfront)

### Use Cases

```python
import heapq

# 1. Top K elements
def top_k_frequent(nums, k):
    count = Counter(nums)
    # Min-heap of size k
    return heapq.nlargest(k, count.keys(), key=count.get)

# 2. Merge K sorted lists
def merge_k_lists(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    result = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result

# 3. Running median
class MedianFinder:
    def __init__(self):
        self.small = []  # Max heap (inverted)
        self.large = []  # Min heap

    def addNum(self, num):
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2

# 4. Task scheduling
def schedule_tasks(tasks):
    heap = [(task.priority, task) for task in tasks]
    heapq.heapify(heap)
    while heap:
        _, task = heapq.heappop(heap)
        process(task)
```

### Limitations

```
- Only efficient access to min OR max (not both)
- No efficient search by value (O(n))
- No efficient delete by value (O(n) to find)
```

---

## Combination Patterns

### HashMap + Linked List = LRU Cache

```python
# HashMap: O(1) key lookup
# Doubly Linked List: O(1) reordering

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()  # Combines both!
        self.capacity = capacity
```

### HashMap + Heap = Top K with Updates

```python
# HashMap: Track current values
# Heap: Maintain sorted order

class TopKTracker:
    def __init__(self, k):
        self.k = k
        self.counts = {}
        self.heap = []  # (count, item)
```

### HashMap + TreeMap = Time-Based Store

```python
# HashMap: Key -> history
# TreeMap: Timestamp -> value (per key)

class TimeMap:
    def __init__(self):
        self.store = {}  # key -> SortedDict
```

---

## Decision Flowchart

```
Start: What operation is most critical?

├── Need O(1) lookup by key?
│   ├── Yes → Need ordering?
│   │   ├── No → HashMap
│   │   └── Yes → HashMap + auxiliary structure
│   └── No → Continue...
│
├── Need sorted order / range queries?
│   ├── Yes → TreeMap/BST
│   └── No → Continue...
│
├── Need quick min/max only?
│   ├── Yes → Heap
│   └── No → Continue...
│
├── Need both min AND max quickly?
│   └── Yes → Two heaps or balanced BST
│
└── Need custom eviction policy?
    └── Combine structures (HashMap + LinkedList, etc.)
```

---

## Real System Examples

| System | Data Structure | Why |
|--------|---------------|-----|
| Redis Cache | HashMap + skiplist | O(1) lookup + O(log n) range |
| Database Index | B+ Tree | Range queries on disk |
| Priority Queue | Heap | O(1) min, O(log n) insert |
| LRU Cache | HashMap + DLL | O(1) everything |
| URL Shortener | HashMap | O(1) redirect lookup |
| Leaderboard | Skip List/TreeMap | Range + updates |

---

## Complexity Analysis

| Scenario | Best Choice | Time | Why |
|----------|-------------|------|-----|
| User session lookup | HashMap | O(1) | Just need key→value |
| Price history range | TreeMap | O(log n + k) | Range queries |
| Next event to process | Heap | O(1) get, O(log n) insert | Priority-based |
| LRU eviction | HashMap+DLL | O(1) | Both lookup and order |
| Top 10 scores | Heap | O(n log 10) | Fixed size top-K |

---

## Common Variations

### 1. When HashMap Keys Expire (TTL)

```python
import time

class TTLCache:
    def __init__(self, ttl_seconds):
        self.ttl = ttl_seconds
        self.cache = {}  # key -> (value, expiry_time)

    def get(self, key):
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            del self.cache[key]
        return None

    def put(self, key, value):
        self.cache[key] = (value, time.time() + self.ttl)
```

### 2. When You Need Both Min and Max

```python
from sortedcontainers import SortedList

class MinMaxTracker:
    def __init__(self):
        self.data = SortedList()

    def add(self, val):
        self.data.add(val)

    def get_min(self):
        return self.data[0] if self.data else None

    def get_max(self):
        return self.data[-1] if self.data else None
```

### 3. When Updates Are Frequent

```python
# If data changes often, consider:
# - TreeMap for O(log n) updates with ordering
# - HashMap + periodic resort for batch processing
# - Heap with lazy deletion (mark deleted, ignore on pop)
```

---

## Edge Cases

1. **Empty structure**: Handle gracefully
2. **Single element**: Ensure all operations still work
3. **Duplicate keys/values**: Define behavior (overwrite? error?)
4. **Capacity limits**: What happens when full?
5. **Concurrency**: Not usually required in interviews, but mention it

---

## Interview Tips

1. **State trade-offs explicitly**: "HashMap gives O(1) but loses ordering"
2. **Mention alternatives**: "We could use TreeMap if we need range queries later"
3. **Consider scale**: "At billions of entries, we'd need sharding"
4. **Know Python's options**: `dict`, `collections.OrderedDict`, `heapq`, `sortedcontainers`
5. **Draw the structure**: Visual aids help communication

---

## Practice Problems

| # | Problem | Difficulty | Key Decision |
|---|---------|------------|--------------|
| 1 | Design HashMap | Easy | Collision handling |
| 2 | LRU Cache | Medium | HashMap + DLL |
| 3 | Time Based Key-Value Store | Medium | HashMap + TreeMap |
| 4 | Find Median from Data Stream | Hard | Two heaps |
| 5 | Design Twitter | Medium | HashMap + Heap for feed |
| 6 | Stock Price Fluctuation | Medium | HashMap + TreeMap or 2 heaps |

---

## Related Sections

- [LRU Cache](./02-lru-cache.md) - Combines HashMap + Linked List
- [LFU Cache](./03-lfu-cache.md) - More complex combination
- [Rate Limiter](./04-rate-limiter.md) - Time-based data structure choice
