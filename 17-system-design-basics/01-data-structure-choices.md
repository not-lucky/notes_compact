# Data Structure Choices for System Design

> **Prerequisites:** Knowledge of basic data structures (HashMap, Trees, Heaps)

## Building Intuition

### The Core Question Every Interviewer Is Asking

When an interviewer asks "why did you choose X over Y?", they're not testing your memorization of Big-O tables. They're testing whether you understand **what problem each data structure was designed to solve**.

Here's the mental framework:

> **Every data structure is optimized for specific access patterns. Your job is to match access patterns to data structures.**

### The Three Fundamental Trade-offs

All data structure choices come down to three trade-offs:

**1. Speed vs. Ordering**

```
HashMap: O(1) lookup/insert/delete, but no ordering
TreeMap: O(log n) lookup/insert/delete, but maintains sorted order

Question to ask: "Do I ever need items in sorted order?"
- No → HashMap
- Yes → TreeMap (or HashMap + separate sorting)
```

**2. Memory vs. Speed**

```
Array: Compact memory, O(n) search
HashMap: Extra memory for buckets, O(1) search

Question to ask: "How often do I search vs. how much memory can I spare?"
- Rarely search, tight memory → Array
- Frequent search, memory available → HashMap
```

**3. Read vs. Write Optimization**

```
Sorted Array: O(log n) search, O(n) insert
HashMap: O(1) search, O(1) insert
Heap: O(n) search, O(log n) insert, O(1) min/max

Question to ask: "What's my read/write ratio?"
- Read-heavy → Optimize for search (sorted array, hash)
- Write-heavy → Optimize for insert (heap, unsorted structures)
```

### Why These Trade-offs Exist: A Deeper Look

**HashMap's O(1) "Magic":**
HashMap achieves O(1) by trading space for time. It pre-allocates buckets and uses a hash function to directly compute where an item lives. No searching required—just calculate and jump. The cost? Wasted space (load factor), no ordering (hash destroys order), and worst-case O(n) if hash function is bad.

**Tree's O(log n) Balance:**
Trees achieve O(log n) by maintaining a sorted structure. Each comparison eliminates half the remaining elements. The cost? You must maintain the sorted property on every insert, and you need extra pointers (left/right children).

**Heap's Selective Optimization:**
Heaps are brilliant because they're "partially sorted"—just enough to give O(1) access to min or max, but not fully sorted. This saves work on insert (O(log n) instead of O(n) for sorted array) while still giving fast access to the extreme value.

## Interview Context

With those fundamentals in mind, let's look at how these trade-offs play out in actual interview scenarios. System design interviews frequently ask "why did you choose X over Y?" The sections below cover the trade-offs between common data structures in real-world scenarios. Understanding these trade-offs shows maturity and experience.

---

## The Big Three: HashMap vs Tree vs Heap

### Quick Reference

| Operation         | HashMap    | BST/TreeMap  | Heap          |
| ----------------- | ---------- | ------------ | ------------- |
| Search            | O(1) avg   | O(log n)     | O(n)          |
| Insert            | O(1) avg   | O(log n)     | O(log n)      |
| Delete (by key)   | O(1) avg   | O(log n)     | O(n)\*        |
| Delete min/max    | O(n)       | O(log n)     | O(log n)      |
| Min/Max           | O(n)       | O(log n)     | O(1)          |
| Range Query       | O(n)       | O(log n + k) | O(n)          |
| Ordered Iteration | O(n log n) | O(n)         | O(n log n)    |

\*Heap delete by arbitrary key/value requires O(n) search + O(log n) removal. Use a HashMap alongside the heap for O(log n) indexed deletion.

---

## When to Use HashMap

**Choose HashMap when:**

- You need O(1) lookup by key
- Order doesn't matter
- No range queries needed
- Keys are hashable

### Use Cases

```python
from collections import Counter
from typing import Any

# 1. Caching (fast lookups)
cache: dict[str, Any] = {}
cache["user_123"] = user_data

# 2. Counting frequencies
word_count = Counter(words)

# 3. Deduplication
seen: set[int] = set()  # HashSet is just HashMap with no values

# 4. Two-sum style problems
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []  # No solution found
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
# Python doesn't have a built-in TreeMap, but sortedcontainers provides one:
from sortedcontainers import SortedDict
from typing import Any, Iterator

# 1. Sorted data with fast updates
calendar: SortedDict = SortedDict()
calendar[event_time] = event_data

# 2. Range queries
def events_between(start: int, end: int) -> Iterator[int]:
    # O(log n + k) where k = number of results
    return calendar.irange(start, end)

# 3. Floor/ceiling (nearest key)
def find_nearest_event(time: int) -> int | None:
    idx = calendar.bisect_left(time)
    candidates: list[int] = []
    if idx < len(calendar):
        candidates.append(calendar.keys()[idx])
    if idx > 0:
        candidates.append(calendar.keys()[idx - 1])
    if not candidates:
        return None
    return min(candidates, key=lambda t: abs(t - time))

# 4. Time-based key-value store
class TimeMap:
    def __init__(self) -> None:
        self.store: dict[str, SortedDict] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = SortedDict()
        self.store[key][timestamp] = value

    def get(self, key: str, timestamp: int) -> str:
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
from collections import Counter

# 1. Top K elements
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    # Min-heap of size k
    return heapq.nlargest(k, count.keys(), key=count.get)

# 2. Merge K sorted lists
def merge_k_lists(lists: list[list[int]]) -> list[int]:
    heap: list[tuple[int, int, int]] = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    result: list[int] = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result

# 3. Running median
class MedianFinder:
    def __init__(self) -> None:
        self.small: list[int] = []  # Max heap (inverted)
        self.large: list[int] = []  # Min heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0

# 4. Task scheduling
# NOTE: In Python 3, heap tuples with equal first elements will compare the
# second element. If tasks aren't comparable, this crashes with TypeError.
# Fix: add a tiebreaker (e.g., an incrementing counter) as the second element.
def schedule_tasks(tasks: list[tuple[int, str]]) -> list[str]:
    """Schedule tasks by priority (lower number = higher priority).

    Args:
        tasks: list of (priority, task_name) tuples
    Returns:
        list of task names in priority order
    """
    counter = 0  # Tiebreaker for equal priorities
    heap: list[tuple[int, int, str]] = []
    for priority, task_name in tasks:
        heapq.heappush(heap, (priority, counter, task_name))
        counter += 1

    result: list[str] = []
    while heap:
        _, _, task_name = heapq.heappop(heap)
        result.append(task_name)
    return result
```

### Limitations

```
- Only efficient access to min OR max (not both)
- No efficient search by value (O(n))
- No efficient delete by value (O(n) to find)
```

---

## When NOT to Use Each Structure

Knowing when to use a data structure is only half the picture. In interviews, recognizing when a structure is a **poor fit** can be even more impressive — it shows you've thought critically about trade-offs, not just memorized a cheat sheet.

### When NOT to Use HashMap

```
❌ DON'T use HashMap when:
1. You need range queries ("all keys between A and B")
   → Use TreeMap/SortedDict instead

2. You need ordered iteration
   → Use TreeMap or OrderedDict (insertion order)

3. Keys aren't hashable (mutable objects, complex nested structures)
   → Use TreeMap with custom comparator

4. Memory is extremely tight and you have small, fixed data
   → Use array with linear search

5. You need both min AND max efficiently
   → Use two heaps or balanced BST
```

**Real-World Example:**

```python
# WRONG: Using HashMap for a time-series database
# Can't efficiently query "all readings between 2pm and 4pm"
readings = {}  # timestamp → value

# RIGHT: Using SortedDict for time-series
from sortedcontainers import SortedDict
readings = SortedDict()  # O(log n + k) range queries
```

### When NOT to Use Tree (BST/TreeMap)

```
❌ DON'T use Tree when:
1. You only need key-value lookup (no ordering, no range)
   → HashMap is simpler and faster

2. Keys don't have natural ordering
   → HashMap or define custom comparator

3. You need O(1) operations (performance-critical hot path)
   → HashMap + auxiliary structure

4. Data is mostly static and you can preprocess
   → Sorted array with binary search (more cache-friendly)
```

**Real-World Example:**

```python
# WRONG: Using TreeMap for user session storage
# We only do key lookups, never range queries
from sortedcontainers import SortedDict
sessions = SortedDict()  # Unnecessary O(log n)

# RIGHT: Using HashMap for sessions
sessions = {}  # O(1) lookup
```

### When NOT to Use Heap

```
❌ DON'T use Heap when:
1. You need to search by value (not just min/max)
   → Use HashMap or TreeMap

2. You need both min AND max
   → Use two heaps or balanced BST

3. You need to delete arbitrary elements frequently
   → Use TreeMap (O(log n) delete by key vs O(n) in heap)

4. You need the k-th smallest element frequently (not just the smallest)
   → Use order statistics tree or sorted structure

5. Data can be sorted upfront
   → Just sort and iterate
```

**Real-World Example:**

```python
# WRONG: Using heap to track both highest and lowest prices
prices_heap: list[float] = []  # Can only efficiently track ONE extreme

# RIGHT: Using two heaps or SortedList
import heapq
min_heap: list[float] = []  # Track lowest
max_heap: list[float] = []  # Track highest (use negation)
# OR
from sortedcontainers import SortedList
prices: SortedList = SortedList()  # Supports both min AND max in O(log n)
```

---

## Combination Patterns

### HashMap + Linked List = LRU Cache

```python
# HashMap: O(1) key lookup
# Doubly Linked List: O(1) reordering
# OrderedDict combines both internally
from collections import OrderedDict
from typing import Any


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cache: OrderedDict[str, Any] = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> Any | None:
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)  # Mark as recently used, O(1)
        return self.cache[key]

    def put(self, key: str, value: Any) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Evict least recently used, O(1)
```

### HashMap + Heap = Top K with Updates

```python
# HashMap: Track current counts — O(1) lookup/update
# Heap: Extract top-k efficiently — O(n log k)
# Why both? HashMap alone can't find top-k without O(n) scan + sort.
#           Heap alone can't update counts by key in O(1).
import heapq


class TopKTracker:
    def __init__(self, k: int) -> None:
        self.k = k
        self.counts: dict[str, int] = {}

    def increment(self, item: str) -> None:
        """Increment the count for an item. O(1)."""
        self.counts[item] = self.counts.get(item, 0) + 1

    def top_k(self) -> list[tuple[int, str]]:
        """Return the top-k items by count. O(n log k)."""
        return heapq.nlargest(
            self.k,
            [(count, item) for item, count in self.counts.items()],
        )
```

### HashMap + TreeMap = Time-Based Store

```python
# HashMap: O(1) key lookup to find the right history
# TreeMap: O(log n) timestamp queries within each key's history
# See the full TimeMap implementation in the "When to Use Tree" section above.
from sortedcontainers import SortedDict


class TimeMap:
    def __init__(self) -> None:
        self.store: dict[str, SortedDict] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = SortedDict()
        self.store[key][timestamp] = value

    def get(self, key: str, timestamp: int) -> str:
        """Return value at or before the given timestamp. O(log n)."""
        if key not in self.store:
            return ""
        times = self.store[key]
        idx = times.bisect_right(timestamp) - 1
        if idx < 0:
            return ""
        return times.peekitem(idx)[1]
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

| System         | Data Structure     | Why                          |
| -------------- | ------------------ | ---------------------------- |
| Redis Cache    | HashMap + skiplist | O(1) lookup + O(log n) range |
| Database Index | B+ Tree            | Range queries on disk        |
| Priority Queue | Heap               | O(1) min, O(log n) insert    |
| LRU Cache      | HashMap + DLL      | O(1) everything              |
| URL Shortener  | HashMap            | O(1) redirect lookup         |
| Leaderboard    | Skip List/TreeMap  | Range + updates              |

---

## Complexity Analysis

| Scenario              | Best Choice | Time                      | Why                   |
| --------------------- | ----------- | ------------------------- | --------------------- |
| User session lookup   | HashMap     | O(1)                      | Just need key→value   |
| Price history range   | TreeMap     | O(log n + k)              | Range queries         |
| Next event to process | Heap        | O(1) get, O(log n) insert | Priority-based        |
| LRU eviction          | HashMap+DLL | O(1)                      | Both lookup and order |
| Top 10 scores         | Heap        | O(n log 10)               | Fixed size top-K      |

---

## Common Variations

### 1. When HashMap Keys Expire (TTL)

```python
import time
from typing import Any

class TTLCache:
    def __init__(self, ttl_seconds: float) -> None:
        self.ttl = ttl_seconds
        self.cache: dict[str, tuple[Any, float]] = {}  # key -> (value, expiry_time)

    def get(self, key: str) -> Any | None:
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            del self.cache[key]
        return None

    def put(self, key: str, value: Any) -> None:
        self.cache[key] = (value, time.time() + self.ttl)
```

### 2. When You Need Both Min and Max

```python
from sortedcontainers import SortedList

class MinMaxTracker:
    def __init__(self) -> None:
        self.data: SortedList = SortedList()

    def add(self, val: float) -> None:
        self.data.add(val)  # O(log n)

    def get_min(self) -> float | None:
        return self.data[0] if self.data else None  # O(log n)

    def get_max(self) -> float | None:
        return self.data[-1] if self.data else None  # O(log n)
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

| #   | Problem                      | Difficulty | Key Decision                 |
| --- | ---------------------------- | ---------- | ---------------------------- |
| 1   | Design HashMap               | Easy       | Collision handling           |
| 2   | LRU Cache                    | Medium     | HashMap + DLL                |
| 3   | Time Based Key-Value Store   | Medium     | HashMap + TreeMap            |
| 4   | Find Median from Data Stream | Hard       | Two heaps                    |
| 5   | Design Twitter               | Medium     | HashMap + Heap for feed      |
| 6   | Stock Price Fluctuation      | Medium     | HashMap + TreeMap or 2 heaps |

### Progressive Coding Exercises

These exercises build on each other. Each one forces you to think about **why** one
data structure is better than another for a given access pattern.

#### Exercise 1: Frequency-Based Lookup (Easy)

**Problem:** Given a stream of events (strings), support two operations:
1. `record(event)` — record that an event occurred.
2. `get_top_k(k)` — return the k most frequent events.

**Key decision:** HashMap for O(1) counting + Heap for top-K extraction.

```python
import heapq
from collections import defaultdict


class EventTracker:
    """Tracks event frequencies and retrieves top-k most frequent events.

    Uses a HashMap (dict) for O(1) frequency counting and a heap for
    O(n log k) top-k extraction. A TreeMap/SortedList would give O(log n)
    per update but is overkill since we only need top-k on demand.
    """

    def __init__(self) -> None:
        self.counts: dict[str, int] = defaultdict(int)

    def record(self, event: str) -> None:
        """Record an event occurrence. O(1)."""
        self.counts[event] += 1

    def get_top_k(self, k: int) -> list[tuple[int, str]]:
        """Return the k most frequent events as (count, event) pairs.

        Uses heapq.nlargest which is O(n log k) — better than full sort
        O(n log n) when k << n.
        """
        return heapq.nlargest(k, [(count, event) for event, count in self.counts.items()])


# --- Demo ---
if __name__ == "__main__":
    tracker = EventTracker()
    for event in ["click", "scroll", "click", "hover", "click", "scroll"]:
        tracker.record(event)

    print(tracker.get_top_k(2))
    # [(3, 'click'), (2, 'scroll')]
```

#### Exercise 2: Sliding Window Maximum (Medium)

**Problem:** Given a stream of numbers and a window size `k`, efficiently return
the maximum value in the current window as each new number arrives.

**Key decision:** A naive approach recalculates max each time (O(k) per query).
A SortedList gives O(log k) add/remove with O(log k) max access. But the optimal
approach uses a **monotonic deque** for amortized O(1) per element.

This exercise shows that sometimes *none* of the Big Three (HashMap, Tree, Heap) is
the best choice — understanding access patterns matters more than memorizing tables.

```python
from collections import deque


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    """Return the max of each sliding window of size k.

    Uses a monotonic decreasing deque:
    - Front of deque is always the index of the current window max.
    - We remove indices that are out of the window.
    - We remove indices whose values are ≤ the new value (they can
      never be the max while the new value is in the window).

    Time: O(n) amortized — each element is pushed/popped at most once.
    Space: O(k) for the deque.

    Why not a heap? Heap gives O(1) max but O(k) to remove expired elements
    (since we can't efficiently remove arbitrary elements).
    Why not a SortedList? O(log k) per operation works, but the deque
    approach is O(1) amortized and uses less memory.
    """
    dq: deque[int] = deque()  # Stores indices, values are monotonically decreasing
    result: list[int] = []

    for i, num in enumerate(nums):
        # Remove indices outside the current window
        while dq and dq[0] <= i - k:
            dq.popleft()

        # Remove indices whose values are ≤ num (they'll never be the max)
        while dq and nums[dq[-1]] <= num:
            dq.pop()

        dq.append(i)

        # Window is fully formed once we've seen at least k elements
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


# --- Demo ---
if __name__ == "__main__":
    print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], k=3))
    # [3, 3, 5, 5, 6, 7]
```

#### Exercise 3: Stock Price Tracker (Medium-Hard)

**Problem:** Design a data structure that supports:
1. `update(timestamp, price)` — update/correct the price at a given timestamp.
2. `current()` — return the price at the latest timestamp.
3. `maximum()` — return the highest price seen across all timestamps.
4. `minimum()` — return the lowest price seen across all timestamps.

**Key decision:** This requires multiple data structures working together:
- **HashMap** for O(1) lookup by timestamp and tracking the latest timestamp.
- **SortedList** (or two heaps) for O(log n) insert/remove and O(log n) min/max access.

This is a real interview question (LeetCode 2034) that tests whether you can
combine data structures to cover multiple access patterns.

```python
from sortedcontainers import SortedList


class StockPrice:
    """Track stock prices with corrections, supporting min/max/current queries.

    Data structure choice rationale:
    - dict: O(1) lookup/update by timestamp.
    - SortedList: O(log n) insert/remove, O(log n) access to min and max.
      A heap won't work here because updates require removing the old price,
      which is O(n) in a heap. SortedList supports O(log n) removal by value.
    - Two heaps with lazy deletion is an alternative but more complex.
    """

    def __init__(self) -> None:
        self.prices: dict[int, int] = {}      # timestamp -> price
        self.sorted_prices: SortedList = SortedList()  # all current prices, sorted
        self.latest_time: int = 0

    def update(self, timestamp: int, price: int) -> None:
        """Update or correct the price at the given timestamp. O(log n)."""
        if timestamp in self.prices:
            old_price = self.prices[timestamp]
            self.sorted_prices.remove(old_price)  # O(log n)

        self.prices[timestamp] = price
        self.sorted_prices.add(price)  # O(log n)
        self.latest_time = max(self.latest_time, timestamp)

    def current(self) -> int:
        """Return the price at the latest timestamp. O(1)."""
        return self.prices[self.latest_time]

    def maximum(self) -> int:
        """Return the maximum price across all timestamps. O(log n)."""
        return self.sorted_prices[-1]

    def minimum(self) -> int:
        """Return the minimum price across all timestamps. O(log n)."""
        return self.sorted_prices[0]


# --- Demo ---
if __name__ == "__main__":
    sp = StockPrice()
    sp.update(1, 10)
    sp.update(2, 5)
    print(f"Current: {sp.current()}")    # 5
    print(f"Max: {sp.maximum()}")        # 10
    print(f"Min: {sp.minimum()}")        # 5

    sp.update(1, 3)  # Correct timestamp 1's price from 10 -> 3
    print(f"Max after correction: {sp.maximum()}")  # 5
    print(f"Min after correction: {sp.minimum()}")  # 3
```

---

## Related Sections

- [LRU Cache](./02-lru-cache.md) - Combines HashMap + Linked List
- [LFU Cache](./03-lfu-cache.md) - More complex combination
- [Rate Limiter](./04-rate-limiter.md) - Time-based data structure choice
