# LFU Cache

> **Prerequisites:** [LRU Cache](./02-lru-cache.md), understanding of frequency-based eviction

## Building Intuition

### Why Frequency Matters: The "Popular Content" Problem

LRU assumes recency predicts future access. But what about content that's popular regardless of when it was last accessed?

> **If something has been accessed many times, it's probably important and will be accessed again.**

This is **frequency-based locality** — the observation that past access count is a strong predictor of future access:

- The homepage of a website is accessed constantly
- Popular API endpoints are called more than obscure ones
- Commonly used functions are invoked repeatedly

### The Core Insight: Track Hits, Not Just Recency

LFU adds a counter to each item:

```
LRU:  "When was this last used?"
LFU:  "How many times has this been used?"

LRU evicts: oldest access
LFU evicts: fewest accesses (ties broken by LRU)
```

### The Challenge: O(1) Eviction with Frequency Tracking

Finding the item with minimum frequency seems like it needs a min-heap (O(log n)), but we can do O(1):

```
Key Insight: Group items by frequency!

Frequency 1: [item_D, item_E]  ← min_freq points here
Frequency 2: [item_B, item_C]
Frequency 3: [item_A]

To evict:
1. Look at min_freq list                    → O(1)
2. Remove oldest from that list             → O(1) (LRU within frequency)
3. Update min_freq if list becomes empty    → O(1) (just increment by 1)

Tie-breaking rule: when multiple items share the same minimum frequency,
evict the Least Recently Used one among them (LRU within the freq bucket).
```

### Visual Trace: How LFU Differs from LRU

Let's compare with capacity=2 (within each freq bucket, front = most recent):

```
                    LRU Cache              LFU Cache (with min_freq state)
                    ----------             ----------
put(A, 1)           [A]                    freq=1: [A]                  min_freq=1
put(B, 2)           [B, A]                 freq=1: [B, A]              min_freq=1
get(A) → 1          [A, B]                 freq=1: [B], freq=2: [A]    min_freq=1
get(A) → 1          [A, B]                 freq=1: [B], freq=3: [A]    min_freq=1
get(A) → 1          [A, B]                 freq=1: [B], freq=4: [A]    min_freq=1
put(C, 3)           [C, A] (evicts B)      freq=1: [C], freq=4: [A]    min_freq=1
                    evicts B (LRU)         evicts B (LFU, freq=1)
get(C) → 3          [C, A]                 freq=2: [C], freq=4: [A]    min_freq=2
                                           (freq=1 bucket now empty, min_freq bumps to 2)
put(D, 4)           [D, C] (evicts A!)     freq=1: [D], freq=4: [A]    min_freq=1
                    ↑ LRU loses A!          evicts C (freq=2 < A's freq=4), then inserts D
                                           ↑ LFU keeps A (it's popular!)
```

**The difference**: In LRU, A was evicted because it hadn't been accessed recently (even though it was the most popular item). In LFU, A survives because its high access count reflects its importance. C is evicted instead — it has a lower frequency (freq=2 vs A's freq=4).

### The Data Structures: Two HashMaps + One Variable

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Map 1 (cache):    key → Node              "Where is this item?"           │
│  Map 2 (freq_map): freq → DoublyLinkedList  "Which items share this freq?" │
│  Variable:         min_freq                 "What's the lowest frequency?" │
│                                                                             │
│  Each Node stores: key, value, freq                                        │
│  Together: O(1) for get, put, and evict!                                   │
│                                                                             │
│  Within each freq bucket, nodes are ordered by recency (most recent at     │
│  front, least recent at back). This gives LRU tie-breaking for free.       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Interview Context

LFU (Least Frequently Used) Cache is a harder variant of LRU Cache. It's asked at senior-level interviews and tests:

- Managing multiple data structures simultaneously
- Handling tie-breaking logic (when frequencies are equal)
- Maintaining O(1) complexity for all operations
- Clean code organization with complex state

**LeetCode 460** is considered a "Hard" problem.

---

## Pattern: HashMap + Frequency Buckets

The key insight is grouping items by frequency and tracking which frequency group is the smallest:

```
Two HashMaps + One Variable:
1. key → Node(key, val, freq)     # O(1) lookup by key
2. frequency → DoublyLinkedList   # Nodes grouped by frequency
                                  # (LRU order within each group)
Plus: min_freq variable to find LFU in O(1)

Why a DoublyLinkedList per frequency?
- Adding to front = O(1) (marks "most recently used" within freq)
- Removing from back = O(1) (evicts "least recently used" within freq)
- Removing a specific node = O(1) (when promoting to next freq)
```

### Visualization

```
Main HashMap: key → Node(key, val, freq)

Frequency Map (each bucket is a DoublyLinkedList in LRU order):
freq=1: [Node3]          ← min_freq points here (LFU candidates)
freq=2: [Node1, Node5]     (Node1 = most recent, Node5 = least recent)
freq=3: [Node2, Node4]

On access to Node5 (currently in freq=2):
1. Remove Node5 from freq=2 list
2. Increment Node5.freq to 3
3. Add Node5 to front of freq=3 list  (now most-recent in that bucket)
4. Check: is freq=2 list now empty?
   → No (Node1 still there), so min_freq stays unchanged
   → If yes AND min_freq == 2, then min_freq = 3
```

---

## Implementation

### O(1) LFU Cache (Full Implementation)

```python
from collections import defaultdict
from typing import Optional


class DLinkedNode:
    """Doubly linked list node storing key, value, and access frequency."""
    __slots__ = ("key", "value", "freq", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key: int = key
        self.value: int = value
        self.freq: int = 1  # Every new node starts with frequency 1
        self.prev: Optional[DLinkedNode] = None
        self.next: Optional[DLinkedNode] = None


class DoublyLinkedList:
    """
    Doubly linked list with dummy head/tail sentinels.
    Maintains LRU ordering within a frequency bucket:
    - Front (head.next) = most recently used
    - Back (tail.prev)  = least recently used → eviction candidate
    """
    def __init__(self) -> None:
        self.head: DLinkedNode = DLinkedNode()  # Dummy head sentinel
        self.tail: DLinkedNode = DLinkedNode()  # Dummy tail sentinel
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size: int = 0

    def add_first(self, node: DLinkedNode) -> None:
        """Add node right after head (most recently used position)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node: DLinkedNode) -> None:
        """Remove a specific node from the list in O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def remove_last(self) -> Optional[DLinkedNode]:
        """Remove and return the last real node (LRU within this frequency)."""
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

    Data structures:
    - cache:    key → Node            (O(1) key lookup)
    - freq_map: frequency → DLL       (nodes grouped by access count)
    - min_freq: int                   (tracks lowest frequency for O(1) eviction)

    Eviction policy:
    - Evict the node with the lowest frequency (LFU).
    - Among nodes with the same lowest frequency, evict the least recently
      used one (LRU tie-breaking).

    Time:  O(1) for both get and put
    Space: O(capacity)
    """

    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.min_freq: int = 0
        self.cache: dict[int, DLinkedNode] = {}  # key → DLinkedNode
        self.freq_map: defaultdict[int, DoublyLinkedList] = defaultdict(DoublyLinkedList)

    def _update_freq(self, node: DLinkedNode) -> None:
        """
        Increment node's frequency and move it to the next frequency bucket.

        Critical detail: if the node was in the min_freq bucket and that
        bucket is now empty, min_freq must increase by exactly 1 (since the
        node just moved to freq+1, that bucket is guaranteed to be non-empty).
        """
        old_freq = node.freq
        self.freq_map[old_freq].remove(node)

        # If this was the last node in the min_freq bucket, bump min_freq
        if self.freq_map[old_freq].is_empty() and self.min_freq == old_freq:
            self.min_freq += 1

        node.freq += 1
        self.freq_map[node.freq].add_first(node)

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._update_freq(node)  # Access increments frequency
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.cache:
            # Update existing key's value and bump its frequency
            node = self.cache[key]
            node.value = value
            self._update_freq(node)
        else:
            # Evict if at capacity
            if len(self.cache) >= self.capacity:
                # Remove the LRU node among those with min_freq
                lfu_list = self.freq_map[self.min_freq]
                evicted = lfu_list.remove_last()
                if evicted:
                    del self.cache[evicted.key]

            # Insert new key with freq=1
            node = DLinkedNode(key, value)
            self.cache[key] = node
            self.freq_map[1].add_first(node)
            self.min_freq = 1  # New node always has freq=1, which is the new minimum


# --- Test (matches LeetCode 460 Example 1) ---
cache = LFUCache(2)
cache.put(1, 1)       # cache: {1: freq=1}
cache.put(2, 2)       # cache: {1: freq=1, 2: freq=1}
print(cache.get(1))   # 1  → key 1 freq becomes 2
cache.put(3, 3)       # Evicts key 2 (min_freq=1, key 2 is LRU among freq=1)
print(cache.get(2))   # -1 (evicted)
print(cache.get(3))   # 3  → key 3 freq becomes 2
cache.put(4, 4)       # Evicts key 1 (min_freq=2, keys 1 & 3 tied; key 1 is LRU)
print(cache.get(1))   # -1 (evicted)
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

When multiple keys have the same minimum frequency, we evict the **Least Recently Used** among them. This is why each frequency bucket is a doubly linked list maintaining insertion/access order:

```
freq=1: [A, B, C]  ← if min_freq=1 and need to evict
         ↑     ↑
       front  back
       (MRU)  (LRU) → evict C (least recently used in this bucket)

Within each frequency bucket:
- Newly inserted / recently accessed items → added to front
- Eviction candidates → removed from back (LRU position)
```

---

## Complexity Analysis

| Operation      | Time | Space |
| -------------- | ---- | ----- |
| get()          | O(1) | -     |
| put() (update) | O(1) | -     |
| put() (insert) | O(1) | -     |
| put() (evict)  | O(1) | -     |

**Space: O(capacity)** for the cache entries. The `freq_map` holds at most `capacity` nodes spread across buckets, plus a constant-size DLL wrapper per non-empty frequency level (at most `capacity` distinct frequencies).

### Complexity Derivation: Why min_freq Update is O(1)

The trickiest part is understanding why `min_freq` never needs scanning:

**When does min_freq change?**

```
Case 1: New item inserted via put()
→ min_freq = 1 (always — new items start at freq=1)
→ O(1): unconditional assignment

Case 2: Existing item accessed via get() or updated via put()
→ Item moves from freq F to freq F+1
→ If F == min_freq AND the freq=F bucket is now empty:
  → min_freq = F + 1
  → Why this works: the item that just left was IN the min_freq bucket,
    and it moved to F+1, so F+1 is guaranteed to be non-empty.
    No other frequency between F and F+1 can exist (frequencies only
    increase by 1), so F+1 is the correct new minimum.
→ O(1): check emptiness + conditional increment

Case 3: Item evicted during put()
→ We remove from the min_freq bucket
→ If min_freq bucket becomes empty, it doesn't matter — we're about
  to insert a new item which sets min_freq = 1
→ O(1)
```

**Key insight**: min_freq can only increase by 1 at a time (because we increment frequencies by 1), and any insertion resets it to 1. No scanning needed!

---

## When NOT to Use LFU Cache

LFU has significant drawbacks. Understanding these is as important as the implementation.

### The "Cache Pollution" Problem

The biggest issue with pure LFU — stale popular items monopolize cache space:

```
Problem: Old popular items NEVER leave

Timeline:
- Day 1: Item A accessed 1000 times (viral content)
- Day 2-30: Item A never accessed again
- Day 30: Item A still in cache with freq=1000!
           New items can't compete — they start at freq=1

Why it's bad:
- Stale data occupies cache space permanently
- New potentially-popular items can't survive long enough to build frequency
- The cache reflects past popularity, not current demand
```

**Solutions:**

1. **Frequency Decay**: Periodically halve all frequencies
2. **Window-Based LFU**: Only count accesses in recent time window
3. **Hybrid Policies**: TinyLFU combines recency + frequency (used by Caffeine/Java)

### When LFU is the Wrong Choice

```
DON'T use LFU when:

1. Access patterns change over time
   Problem: Old popular items block new ones
   Better: LRU or LFU with decay

2. All items have similar access frequency
   Problem: LFU degenerates to insertion-order (like FIFO)
   Better: LRU (simpler, same effectiveness)

3. You need simplicity
   Problem: LFU is complex (3 data structures, tie-breaking)
   Better: LRU is simpler and usually "good enough"

4. Items have TTL requirements
   Problem: Pure LFU ignores time
   Better: TTL-based cache or LRU with TTL

5. Burst traffic is common
   Problem: Burst inflates frequency unfairly
   Better: LRU or rate-limited frequency counting
```

### LRU vs LFU Decision Matrix

```
Choose LRU when:                     Choose LFU when:
├── Access patterns change often     ├── Clear hot/cold data distinction
├── Simplicity matters               ├── Popularity is stable over time
├── Streaming/sequential access      ├── Same items accessed repeatedly
├── Time-sensitive data              ├── Cache pollution is acceptable
└── Default choice when unsure       └── You can implement decay
```

### Real-World Usage

**Where LFU is used:**

- CDN caching for stable popular content
- Database query plan caching (same queries repeat)
- DNS caching (popular domains queried constantly)

**Where LFU is NOT used:**

- Web browser cache (pages/interests change)
- Session storage (recency matters more)
- Real-time systems (complexity adds latency)

---

## Common Variations

### 1. Simplified LFU (O(log n) using Heap)

If O(1) isn't required, a heap-based approach is simpler to implement:

```python
import heapq


class LFUCacheHeap:
    """
    Simpler LFU with O(log n) operations using a min-heap.

    Heap entries are (frequency, timestamp, key) tuples.
    - frequency: primary sort key (evict lowest)
    - timestamp: secondary sort key (breaks ties by LRU — evict oldest)

    Stale entries are lazily cleaned: when we pop from the heap, we check
    if the entry matches the current freq/time for that key. If not, it's
    outdated and we skip it.

    Trade-off: Simpler code, but O(log n) per operation and heap can grow
    to O(n * avg_accesses) due to stale entries (lazy deletion).
    """

    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.cache: dict[int, int] = {}       # key → value
        self.freq: dict[int, int] = {}        # key → current frequency
        self.time: dict[int, int] = {}        # key → last access timestamp
        self.heap: list[tuple[int, int, int]] = []  # min-heap of (freq, time, key)
        self.counter: int = 0                 # monotonic timestamp

    def _bump(self, key: int) -> None:
        """Increment key's frequency and timestamp, push updated entry to heap."""
        self.freq[key] += 1
        self.counter += 1
        self.time[key] = self.counter
        heapq.heappush(self.heap, (self.freq[key], self.time[key], key))

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self._bump(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.cache:
            self.cache[key] = value
            self._bump(key)
            return

        if len(self.cache) >= self.capacity:
            self._evict()

        self.cache[key] = value
        self.freq[key] = 1
        self.counter += 1
        self.time[key] = self.counter
        heapq.heappush(self.heap, (1, self.counter, key))

    def _evict(self) -> None:
        """Pop from heap until we find a non-stale entry, then evict it."""
        while self.heap:
            freq, time, key = heapq.heappop(self.heap)
            # Verify this heap entry is still current (not stale)
            if key in self.cache and self.freq[key] == freq and self.time[key] == time:
                del self.cache[key]
                del self.freq[key]
                del self.time[key]
                return
```

### 2. Compact O(1) LFU using OrderedDict

Python's `OrderedDict` gives insertion-order iteration and O(1) `move_to_end()` / `popitem()`, so it can replace the manual DoublyLinkedList for each frequency bucket:

```python
from collections import defaultdict, OrderedDict


class LFUCacheCompact:
    """
    Compact O(1) LFU using OrderedDict as frequency buckets.

    Each frequency bucket is an OrderedDict that preserves insertion order,
    giving us LRU semantics within a frequency group for free.

    Time:  O(1) amortized get and put
    Space: O(capacity)
    """

    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.min_freq: int = 0
        self.key_to_val: dict[int, int] = {}
        self.key_to_freq: dict[int, int] = {}
        self.freq_to_keys: defaultdict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)

    def _touch(self, key: int) -> None:
        """Move key from its current freq bucket to freq+1."""
        freq = self.key_to_freq[key]
        del self.freq_to_keys[freq][key]

        # Clean up empty bucket and update min_freq if needed
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq = freq + 1

        self.key_to_freq[key] = freq + 1
        self.freq_to_keys[freq + 1][key] = None  # OrderedDict tracks order

    def get(self, key: int) -> int:
        if key not in self.key_to_val:
            return -1
        self._touch(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._touch(key)
            return

        if len(self.key_to_val) >= self.capacity:
            # Evict LFU (LRU among ties) — first item in min_freq bucket
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]

        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1


# --- Test (matches LeetCode 460 examples) ---
cache = LFUCacheCompact(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))   # 1
cache.put(3, 3)       # Evicts key 2
print(cache.get(2))   # -1
print(cache.get(3))   # 3
cache.put(4, 4)       # Evicts key 1 (freq tied at 2; key 1 is LRU)
print(cache.get(1))   # -1
print(cache.get(3))   # 3
print(cache.get(4))   # 4
```

### 3. LFU with Decay (Aging)

In production, pure LFU suffers from the "stale popular item" problem. Decay periodically reduces all frequencies so old items lose their advantage:

```python
class LFUWithDecay:
    """
    LFU where frequencies decay (halve) over time.

    Every `decay_interval` operations, all frequencies are halved (min 1).
    This prevents old popular items from permanently occupying cache space.

    Simplified O(n) eviction version to illustrate the decay concept.
    For O(1) eviction, combine decay with the full DLL-based LFU above.
    """

    def __init__(self, capacity: int, decay_interval: int = 100) -> None:
        self.capacity: int = capacity
        self.decay_interval: int = decay_interval
        self.ops_count: int = 0
        self.cache: dict[int, tuple[int, int]] = {}  # key → (value, frequency)

    def _maybe_decay(self) -> None:
        """Halve all frequencies every `decay_interval` operations."""
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

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        self._maybe_decay()

        if key in self.cache:
            _, freq = self.cache[key]
            self.cache[key] = (value, freq + 1)
            return

        if len(self.cache) >= self.capacity:
            # Evict the key with minimum frequency (O(n) scan)
            lfu_key = min(self.cache, key=lambda k: self.cache[k][1])
            del self.cache[lfu_key]

        self.cache[key] = (value, 1)
```

---

## LRU vs LFU: When to Use Each

| Aspect                 | LRU                                     | LFU                                         |
| ---------------------- | --------------------------------------- | ------------------------------------------- |
| Eviction criterion     | Least recently accessed                 | Least frequently accessed (LRU for ties)    |
| Implementation         | 1 HashMap + 1 DLL                       | 2 HashMaps + freq DLLs + min_freq variable  |
| Complexity             | Simpler                                 | More complex                                |
| General caching        | **Best choice** — works for most cases  | Overkill unless access patterns are skewed  |
| Hot/cold data          | May evict hot items during cold streaks | **Best choice** — hot items stay cached     |
| Streaming data         | **Best choice** — recent items favored  | Poor — one-time items pollute freq counts   |
| Static popular content | Popular items can be evicted            | **Best choice** — popular items persist     |
| Changing workloads     | **Adapts quickly**                      | Slow to adapt (old counts linger)           |
| Default choice         | Yes — simpler and good enough           | Only when frequency skew is well-understood |

---

## Edge Cases

1. **Capacity 0**: `put()` should return immediately, `get()` always returns -1
2. **Capacity 1**: Every new key evicts the previous one
3. **Same frequency tie**: Use LRU among same-frequency items (why each freq bucket is a DLL)
4. **Frequency overflow**: In practice, use modular frequency or periodic decay
5. **`get()` updates frequency**: Don't forget — `get()` increments freq, not just `put()`
6. **Update existing key via `put()`**: Must also increment frequency (same as `get()`)
7. **Eviction then insert in `put()`**: After eviction, `min_freq` is set to 1 for the new item

---

## Interview Tips

1. **Explain the two maps + min_freq**: Make the design clear upfront
2. **Draw frequency buckets**: Visual helps understanding
3. **Mention the tie-breaker**: LRU within same frequency
4. **Start with LRU**: "This builds on LRU but adds frequency tracking"
5. **Know the tradeoffs**: LFU is more complex but better for some patterns

### Common Interview Follow-ups

```
Q: When would LFU perform worse than LRU?
A: When access patterns change over time. Old frequent items
   stay cached even if they're no longer popular. Also, LFU
   handles streaming/sequential access poorly — each item gets
   freq=1 and the cache churns constantly with no benefit.

Q: How would you handle this in production?
A: Add frequency decay — periodically halve all frequencies
   so old items can eventually be evicted. Or use a hybrid
   like TinyLFU (used in Caffeine/Java) that combines a
   frequency sketch with an LRU admission window.

Q: What about thread safety?
A: Use fine-grained locks per frequency bucket, or a single
   read-write lock (reads for get, writes for put/evict).
   For high concurrency, consider lock-free structures with
   CAS operations or sharded caches.

Q: Can you implement this without a DoublyLinkedList?
A: Yes — use Python's OrderedDict for each frequency bucket.
   OrderedDict preserves insertion order and supports O(1)
   move_to_end() and popitem(). See the compact version above.
```

---

## Practice Problems

| #   | Problem                                   | Difficulty | Key Concept                        |
| --- | ----------------------------------------- | ---------- | ---------------------------------- |
| 1   | LRU Cache (LC 146)                        | Medium     | Prerequisite                       |
| 2   | Design Hit Counter (LC 362)               | Medium     | Frequency counting                 |
| 3   | First Unique Character in Stream (LC 387) | Medium     | Frequency + order tracking         |
| 4   | LFU Cache (LC 460)                        | Hard       | Core implementation                |
| 5   | All O(1) Data Structure (LC 432)          | Hard       | Similar multi-map design           |

---

## Progressive Exercises

### Exercise 1: Frequency Counter with Min Tracking (Warm-up)

Build a data structure that tracks element frequencies and can report the element
with the minimum frequency in O(1). This is the core primitive behind LFU eviction.

**Requirements:**
- `increment(key)` — increment the frequency of `key` by 1. O(1).
- `get_min_freq_key()` — return any key with the lowest frequency. O(1).
- `remove(key)` — remove a key entirely. O(1).

<details>
<summary>Solution</summary>

```python
from collections import defaultdict
from typing import Optional


class FrequencyTracker:
    """
    Tracks element frequencies with O(1) min-frequency lookup.

    This is the core bookkeeping used inside an LFU cache:
    two maps (key→freq, freq→set-of-keys) plus a min_freq variable.
    """

    def __init__(self) -> None:
        self.key_freq: dict[int, int] = {}                          # key → freq
        self.freq_keys: defaultdict[int, set[int]] = defaultdict(set)  # freq → {keys}
        self.min_freq: int = 0

    def increment(self, key: int) -> None:
        """Increment frequency of key (insert with freq=1 if new)."""
        if key in self.key_freq:
            old_freq = self.key_freq[key]
            self.freq_keys[old_freq].discard(key)
            if not self.freq_keys[old_freq]:
                del self.freq_keys[old_freq]
                if self.min_freq == old_freq:
                    self.min_freq = old_freq + 1
            new_freq = old_freq + 1
        else:
            new_freq = 1
            if not self.key_freq:  # First element
                self.min_freq = 1
            else:
                self.min_freq = min(self.min_freq, 1)

        self.key_freq[key] = new_freq
        self.freq_keys[new_freq].add(key)

    def get_min_freq_key(self) -> Optional[int]:
        """Return any key with the lowest frequency, or None if empty."""
        if not self.key_freq:
            return None
        # Peek at one element from the min_freq bucket
        return next(iter(self.freq_keys[self.min_freq]))

    def remove(self, key: int) -> None:
        """Remove a key entirely."""
        if key not in self.key_freq:
            return
        freq = self.key_freq.pop(key)
        self.freq_keys[freq].discard(key)
        if not self.freq_keys[freq]:
            del self.freq_keys[freq]
        # Recalculate min_freq if needed
        if not self.key_freq:
            self.min_freq = 0
        elif self.min_freq == freq and freq not in self.freq_keys:
            # Must scan — but this only happens on remove, which LFU
            # always follows with an insert (resetting min_freq = 1).
            self.min_freq = min(self.freq_keys) if self.freq_keys else 0


# --- Test ---
ft = FrequencyTracker()
ft.increment(1)        # freq: {1: 1}
ft.increment(2)        # freq: {1: 1, 2: 1}
ft.increment(1)        # freq: {1: 2, 2: 1}
ft.increment(1)        # freq: {1: 3, 2: 1}
print(ft.get_min_freq_key())  # 2  (freq=1, the minimum)
ft.increment(2)        # freq: {1: 3, 2: 2}
ft.increment(2)        # freq: {1: 3, 2: 3}
ft.increment(3)        # freq: {1: 3, 2: 3, 3: 1}
print(ft.get_min_freq_key())  # 3  (freq=1)
ft.remove(3)
print(ft.get_min_freq_key())  # 1 or 2  (both freq=3)
```
</details>

### Exercise 2: Full O(1) LFU Cache (LeetCode 460)

Implement an LFU Cache with O(1) `get` and `put`.

**Requirements (same as LeetCode 460):**
- `LFUCache(capacity)` — initialize with positive capacity.
- `get(key)` — return value if key exists (and increment its frequency), else -1.
- `put(key, value)` — insert or update. If at capacity, evict the LFU key
  (tie-break by LRU among same frequency).

<details>
<summary>Solution</summary>

See the full [O(1) LFU Cache implementation](#o1-lfu-cache-full-implementation) above.

Alternatively, see the [Compact O(1) LFU using OrderedDict](#2-compact-o1-lfu-using-ordereddict) variation which uses `OrderedDict` for the frequency buckets (each `OrderedDict` gives LRU ordering within a frequency):

**Key implementation checklist:**
1. Two maps: `key → node` and `freq → ordered_collection`
2. A `min_freq` variable, updated on every access and insertion
3. On `get()`: look up node, remove from old freq bucket, add to freq+1 bucket
4. On `put()` (new key): evict from `min_freq` bucket if full, then insert at freq=1
5. On `put()` (existing key): update value, then same as `get()` for freq bump

</details>

### Exercise 3: LFU Cache with Time-Based Decay

Extend the LFU cache so that frequencies decay over time, preventing stale
popular items from permanently occupying the cache.

**Requirements:**
- Same API as LFU Cache (`get`, `put`).
- Every `decay_interval` operations, halve all frequencies (min 1).
- After decay, the minimum-frequency bookkeeping must still be correct.

**Why this matters:** Pure LFU is rarely used in production without some form of
decay or aging. This exercise bridges the gap between the textbook algorithm and
real-world cache implementations.

<details>
<summary>Solution</summary>

```python
from collections import defaultdict, OrderedDict


class LFUCacheWithDecay:
    """
    LFU cache whose frequencies decay (halve) every `decay_interval` ops.

    After decay, items that were once popular lose their advantage,
    preventing the "stale popular item" problem of pure LFU.

    Decay is O(n) but amortised over `decay_interval` O(1) operations,
    so the average cost per operation is O(n / decay_interval).
    Choose a large interval to keep this negligible.

    Time:  O(1) amortised get/put (ignoring infrequent decay)
    Space: O(capacity)
    """

    def __init__(self, capacity: int, decay_interval: int = 100) -> None:
        self.capacity: int = capacity
        self.decay_interval: int = decay_interval
        self.ops_count: int = 0
        self.min_freq: int = 0
        self.key_to_val: dict[int, int] = {}
        self.key_to_freq: dict[int, int] = {}
        self.freq_to_keys: defaultdict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)

    # -- internal helpers --------------------------------------------------

    def _maybe_decay(self) -> None:
        """Halve all frequencies every `decay_interval` operations."""
        self.ops_count += 1
        if self.ops_count < self.decay_interval:
            return

        self.ops_count = 0
        # Rebuild freq_to_keys from scratch after halving
        new_freq_to_keys: defaultdict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)
        new_min_freq: int = float("inf")  # type: ignore[assignment]

        for key, freq in self.key_to_freq.items():
            new_freq = max(1, freq // 2)
            self.key_to_freq[key] = new_freq
            new_freq_to_keys[new_freq][key] = None
            new_min_freq = min(new_min_freq, new_freq)

        self.freq_to_keys = new_freq_to_keys
        if self.key_to_freq:
            self.min_freq = new_min_freq
        else:
            self.min_freq = 0

    def _touch(self, key: int) -> None:
        """Move key from current freq bucket to freq+1."""
        freq = self.key_to_freq[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq = freq + 1
        self.key_to_freq[key] = freq + 1
        self.freq_to_keys[freq + 1][key] = None

    # -- public API --------------------------------------------------------

    def get(self, key: int) -> int:
        self._maybe_decay()
        if key not in self.key_to_val:
            return -1
        self._touch(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        self._maybe_decay()

        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._touch(key)
            return

        if len(self.key_to_val) >= self.capacity:
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]

        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1


# --- Test ---
cache = LFUCacheWithDecay(2, decay_interval=5)

# Build up frequency for key 1
cache.put(1, 10)       # op 1 — freq: {1: 1}
cache.put(2, 20)       # op 2 — freq: {1: 1, 2: 1}
cache.get(1)           # op 3 — freq: {1: 2, 2: 1}
cache.get(1)           # op 4 — freq: {1: 3, 2: 1}
# op 5 triggers decay: freqs halved → {1: 1, 2: 1}
cache.get(1)           # op 5 (decay!) then touch → freq: {1: 2, 2: 1}

# Now key 1's advantage is reduced.  Without decay it would be freq=4.
cache.put(3, 30)       # op 6 — evicts key 2 (LFU, freq=1)
print(cache.get(2))    # -1  (evicted)
print(cache.get(1))    # 10  (still present, freq was higher after decay)
print(cache.get(3))    # 30
```
</details>

### Exercise 4: Design a Cache with Multiple Eviction Policies

Design a cache system that can switch between LRU and LFU eviction policies at
runtime. This tests your understanding of both algorithms and how to abstract
their shared interface.

**Requirements:**
- `AdaptiveCache(capacity, policy="lfu")` — initialize with a policy (`"lru"` or `"lfu"`).
- `get(key)` and `put(key, value)` — same semantics as before.
- `set_policy(policy)` — switch eviction policy. Existing cache contents are preserved.

**Hint:** Both LRU and LFU need `get` and `put`. Think about what state you need
to track to support both policies simultaneously, and what happens to the frequency
data when switching from LFU to LRU (and vice versa).

<details>
<summary>Solution</summary>

```python
from collections import defaultdict, OrderedDict
from typing import Literal


class AdaptiveCache:
    """
    Cache that can switch between LRU and LFU eviction at runtime.

    Internally maintains both LRU ordering (via an OrderedDict) and
    LFU frequency tracking. The active policy decides which is used
    for eviction. Both are always kept in sync so switching is O(1).

    Time:  O(1) get/put for both policies
    Space: O(capacity)
    """

    def __init__(
        self,
        capacity: int,
        policy: Literal["lru", "lfu"] = "lfu",
    ) -> None:
        self.capacity: int = capacity
        self.policy: str = policy

        # Shared key→value store with LRU ordering
        self.lru_order: OrderedDict[int, int] = OrderedDict()  # key → value

        # LFU-specific bookkeeping
        self.key_to_freq: dict[int, int] = {}
        self.freq_to_keys: defaultdict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)
        self.min_freq: int = 0

    def _lfu_touch(self, key: int) -> None:
        """Move key to the next frequency bucket (LFU bookkeeping)."""
        freq = self.key_to_freq[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq = freq + 1
        self.key_to_freq[key] = freq + 1
        self.freq_to_keys[freq + 1][key] = None

    def _lfu_add(self, key: int) -> None:
        """Register a new key in LFU bookkeeping at freq=1."""
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1

    def _lfu_remove(self, key: int) -> None:
        """Remove key from LFU bookkeeping."""
        freq = self.key_to_freq.pop(key)
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]

    def _evict_one(self) -> None:
        """Evict one item according to the active policy."""
        if self.policy == "lru":
            evict_key, _ = self.lru_order.popitem(last=False)  # oldest
            self._lfu_remove(evict_key)
        else:  # lfu
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.lru_order[evict_key]
            del self.key_to_freq[evict_key]
            # Clean up empty bucket (already removed from freq_to_keys by popitem)
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]

    def get(self, key: int) -> int:
        if key not in self.lru_order:
            return -1

        # Update LRU ordering
        self.lru_order.move_to_end(key)

        # Update LFU frequency
        self._lfu_touch(key)

        return self.lru_order[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.lru_order:
            self.lru_order[key] = value
            self.lru_order.move_to_end(key)
            self._lfu_touch(key)
            return

        if len(self.lru_order) >= self.capacity:
            self._evict_one()

        self.lru_order[key] = value
        self._lfu_add(key)

    def set_policy(self, policy: Literal["lru", "lfu"]) -> None:
        """Switch eviction policy. Cache contents are preserved."""
        self.policy = policy


# --- Test ---
cache = AdaptiveCache(2, policy="lfu")
cache.put(1, 10)
cache.put(2, 20)
cache.get(1)            # key 1 freq=2, key 2 freq=1
cache.put(3, 30)        # LFU evicts key 2 (lowest freq)
print(cache.get(2))     # -1

cache.set_policy("lru")
cache.put(4, 40)        # LRU evicts key 1 (least recently used)
print(cache.get(1))     # -1
print(cache.get(3))     # 30  (was more recently used than key 1)
print(cache.get(4))     # 40
```
</details>

---

## Related Sections

- [LRU Cache](./02-lru-cache.md) - Simpler eviction policy
- [Data Structure Choices](./01-data-structure-choices.md) - When to use each
