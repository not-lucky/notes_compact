# LRU Cache

> **Prerequisites:** [Data Structure Choices](./01-data-structure-choices.md), Understanding of HashMap and Linked Lists

## Building Intuition

### Why LRU? The Principle of Temporal Locality

LRU Cache is built on a simple observation about how we access data:

> **If you accessed something recently, you're likely to access it again soon.**

This is called **temporal locality**, and it's everywhere:

- You re-read the same documentation page while coding
- You visit the same websites repeatedly during a day
- You use the same files in your editor
- Operating systems keep recently accessed disk blocks in memory

### The Core Problem: O(1) for Everything

Here's the challenge that makes LRU Cache an interview favorite:

```
We need THREE operations, ALL in O(1):
1. get(key)     → Find value by key
2. put(key,val) → Insert or update
3. evict()      → Remove the least recently used item

Why is this hard?
- HashMap gives O(1) get/put, but how do you know which item is oldest?
- Sorted structure knows age, but get/put become O(log n)
- Array with timestamps? Finding/removing oldest is O(n)
```

### The "Aha!" Moment: Two Structures Working Together

The insight is that **no single data structure can do this**. You need two:

```
HashMap              Doubly Linked List

                     ┌──────┐      ┌──────┐      ┌──────┐
┌─────────┐    ┌────→│ key1 │←────→│ key2 │←────→│ key3 │
│ key1  ──┼────┘     │ val1 │   ┌─→│ val2 │  ┌──→│ val3 │
├─────────┤          └──────┘   │  └──────┘  │   └──────┘
│ key2  ──┼─────────────────────┘            │
├─────────┤              ↑                   │       ↑
│ key3  ──┼──────────────────────────────────┘
└─────────┘            HEAD                        TAIL
                       (MRU)                       (LRU)

HashMap: "WHERE is the data?"    → O(1) lookup by key to node
Linked List: "WHEN was it used?" → O(1) reordering via pointer surgery

Each HashMap value is a pointer directly to a node in the linked list.

On access: Move that node to HEAD (most recently used)
On eviction: Remove the node at TAIL (least recently used)
```

**Why Doubly Linked?** Because to remove a node from the middle, you need to
update both its neighbors' pointers. With a singly linked list, you'd need to
traverse from the head to find the previous node — that's O(n). With a doubly
linked list, each node already knows its `prev`, so removal is O(1).

### Visual Trace: How It Actually Works

Let's trace through operations with capacity=3:

```
Initial: Empty
HashMap: {}
List: HEAD <-> TAIL

put(A, 1):
HashMap: {A: node_A}
List: HEAD <-> [A] <-> TAIL

put(B, 2):
HashMap: {A: node_A, B: node_B}
List: HEAD <-> [B] <-> [A] <-> TAIL
              (MRU)         (LRU)

put(C, 3):
HashMap: {A: node_A, B: node_B, C: node_C}
List: HEAD <-> [C] <-> [B] <-> [A] <-> TAIL

get(A) → 1:  (Move A to front)
List: HEAD <-> [A] <-> [C] <-> [B] <-> TAIL
              (now MRU)        (now LRU)

put(D, 4):  (Cache full! Evict B, the LRU)
HashMap: {A: node_A, C: node_C, D: node_D}  ← B removed
List: HEAD <-> [D] <-> [A] <-> [C] <-> TAIL
```

---

## Interview Context

LRU (Least Recently Used) Cache is one of the most frequently asked coding
interview questions at FANG companies. It's a "must-know" problem that tests:

- Combining data structures creatively
- Achieving O(1) time complexity for all operations
- Understanding cache eviction policies
- Code organization and clean implementation under pressure

**LeetCode 146** is asked in virtually every company's interview pool.

---

## Implementation

### Using OrderedDict (Python's Built-in)

Python's `OrderedDict` maintains insertion order and supports O(1)
`move_to_end()`. This gives us LRU semantics with minimal code. Mention this
in interviews to show Python fluency, but be prepared to implement from
scratch.

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

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()

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
            # popitem(last=False) removes the FIRST item (least recently used)
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

This is what interviewers usually want to see. The key elements:

1. **`DLinkedNode`** — stores key, value, and prev/next pointers
2. **`cache` dict** — maps key to its node for O(1) lookup
3. **Sentinel head/tail** — dummy nodes that eliminate null-check edge cases
4. **Four helper methods** — `_add_to_head`, `_remove_node`, `_move_to_head`, `_remove_tail`

```python
from __future__ import annotations


class DLinkedNode:
    """Doubly linked list node storing a key-value pair."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev: DLinkedNode | None = None
        self.next: DLinkedNode | None = None


class LRUCache:
    """
    LRU Cache with HashMap + Doubly Linked List.

    The HashMap provides O(1) key-to-node lookup.
    The Doubly Linked List maintains access order with O(1) reordering.

    Sentinel (dummy) head and tail nodes simplify all pointer operations
    by guaranteeing that every real node always has valid prev/next neighbors.

    Time: O(1) amortized for get and put (HashMap is O(1) amortized)
    Space: O(capacity)
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: dict[int, DLinkedNode] = {}  # key -> DLinkedNode

        # Sentinel head and tail — never hold real data.
        # Real nodes are always between head and tail.
        #   head <-> [node1] <-> [node2] <-> ... <-> tail
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: DLinkedNode) -> None:
        """Add node right after head (most recently used position).

        Before: head <-> old_first <-> ...
        After:  head <-> node <-> old_first <-> ...
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node  # type: ignore[union-attr]
        self.head.next = node

    def _remove_node(self, node: DLinkedNode) -> None:
        """Remove a node from its current position in the list.

        Before: ... <-> A <-> node <-> B <-> ...
        After:  ... <-> A <-> B <-> ...
        """
        node.prev.next = node.next  # type: ignore[union-attr]
        node.next.prev = node.prev  # type: ignore[union-attr]

    def _move_to_head(self, node: DLinkedNode) -> None:
        """Move existing node to head (mark as most recently used)."""
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self) -> DLinkedNode:
        """Remove and return the node just before tail (least recently used).

        We return the node so the caller can read its key and delete it
        from the HashMap.
        """
        node = self.tail.prev  # type: ignore[union-attr]
        self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_head(node)  # Mark as recently used
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing node's value and move to head
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # Create new node, add to HashMap and list
            node = DLinkedNode(key, value)
            self.cache[key] = node
            self._add_to_head(node)

            # Evict LRU if over capacity
            if len(self.cache) > self.capacity:
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

> **Note on `__slots__`:** Adding `__slots__` to `DLinkedNode` prevents Python
> from creating a `__dict__` for each node instance, reducing memory overhead.
> This is a nice detail to mention in interviews when discussing optimization.

---

## Why Doubly Linked List? (Detailed)

```
Singly Linked List:
- Remove from middle: O(n) — need to traverse to find previous node

Doubly Linked List:
- Remove from middle: O(1) — have direct access to prev pointer

For LRU we need:
- Remove any node when it's accessed (to move it to head)  → must be O(1)
- Remove the tail node when evicting                       → must be O(1)
- Both require updating the predecessor → Doubly Linked List
```

### Concrete Comparison: Singly vs Doubly

```python
# --- Singly Linked List: removing a node is O(n) ---
# Given only a reference to `target_node`, you CANNOT remove it
# without traversing from head to find the previous node.

def remove_singly(head, target_node):
    """Must traverse to find the node before target. O(n)."""
    current = head
    while current and current.next is not target_node:
        current = current.next
    if current:
        current.next = target_node.next  # Skip over target


# --- Doubly Linked List: removing a node is O(1) ---
# Each node has a .prev pointer, so we can rewire immediately.

def remove_doubly(target_node):
    """Direct pointer access — no traversal needed. O(1)."""
    target_node.prev.next = target_node.next
    target_node.next.prev = target_node.prev
```

With a singly linked list the HashMap would give us the node in O(1), but
we'd still pay O(n) to remove it. The doubly linked list makes the entire
get/put pipeline O(1).

---

## Why Sentinel (Dummy) Head/Tail?

Sentinel nodes eliminate all null checks and edge cases for an empty list,
single-element list, or removing the first/last real node. Every real node
is guaranteed to have valid `prev` and `next` pointers.

```python
# Without sentinel nodes — must handle empty list and boundary cases:
def _add_to_head(self, node):
    if self.head is None:          # Edge case: empty list
        self.head = self.tail = node
    else:
        node.next = self.head
        self.head.prev = node
        self.head = node

# With sentinel nodes — always uniform, no branches:
def _add_to_head(self, node):
    node.prev = self.head
    node.next = self.head.next
    self.head.next.prev = node
    self.head.next = node
```

```
Sentinel layout (capacity 3, holding 2 items):

  HEAD (dummy) <-> [A] <-> [B] <-> TAIL (dummy)
        |                               |
  Never removed,                  Never removed,
  never holds data                never holds data

  - Inserting at front: always insert between HEAD and HEAD.next
  - Removing from back: always remove TAIL.prev
  - No special cases!
```

---

## Complexity Analysis

| Operation      | Time            | Explanation                       |
| -------------- | --------------- | --------------------------------- |
| get()          | O(1) amortized  | HashMap lookup + linked list move |
| put() (update) | O(1) amortized  | HashMap lookup + linked list move |
| put() (insert) | O(1) amortized  | HashMap insert + linked list add  |
| put() (evict)  | O(1) amortized  | Remove tail + delete from HashMap |

**Space: O(capacity)** — we store at most `capacity` nodes plus the two
sentinel nodes and the HashMap.

> **Why "amortized"?** The HashMap operations are O(1) *amortized*, not
> worst-case. In rare cases, a HashMap resize or hash collision chain can cause
> a single operation to take O(n). In practice this is negligible, and
> interviewers accept "O(1)" without the amortized qualifier — but knowing the
> distinction shows depth.

### Complexity Derivation: Why Each Operation is O(1)

**get(key):**

```
Step 1: HashMap lookup           → O(1) amortized
Step 2: Access node.prev/next    → O(1) pointer access
Step 3: Update 4 pointers        → O(1) constant work
Total: O(1)
```

**put(key, value) — existing key:**

```
Step 1: HashMap lookup           → O(1)
Step 2: Update node.value        → O(1)
Step 3: Move to head (4 pointers)→ O(1)
Total: O(1)
```

**put(key, value) — new key, no eviction:**

```
Step 1: Create new node          → O(1)
Step 2: HashMap insert           → O(1)
Step 3: Add to head (4 pointers) → O(1)
Total: O(1)
```

**put(key, value) — new key, with eviction:**

```
Step 1-3: Same as above          → O(1)
Step 4: Access tail.prev         → O(1)
Step 5: Remove from list         → O(1)
Step 6: HashMap delete           → O(1)
Total: O(1)
```

---

## Python's Built-in `functools.lru_cache`

Python provides a decorator for memoization with LRU eviction. It won't
satisfy a "design LRU cache" interview question, but interviewers may ask
about it, and it's useful in real-world code.

```python
from functools import lru_cache


@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """Memoized Fibonacci — repeated calls with same n are O(1)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(50))         # 12586269025  (instant, not exponential)
print(fibonacci.cache_info()) # Hits, misses, maxsize, currsize

# Clear the cache
fibonacci.cache_clear()
```

Key points:
- `maxsize=None` disables eviction (unbounded cache)
- `maxsize=128` (default) enables LRU eviction after 128 entries
- Only works with **hashable** arguments (no lists or dicts)
- Uses a **doubly linked list + dict** internally — the same pattern!

---

## When NOT to Use LRU Cache

LRU isn't always the right choice. Here's when to consider alternatives:

### Access Patterns Where LRU Fails

**1. Scan-Based Access (Sequential Reading)**

```
Problem: You sequentially scan through data (e.g., reading a file)
What happens: Each new access evicts old items, cache is useless

Example: SELECT * FROM users (full table scan)
→ LRU cache fills with records you'll never read again
→ Evicts actually useful cached queries

Solution: Don't cache, or use scan-resistant variants (LRU-K, 2Q)
```

**2. Frequency-Based Popularity**

```
Problem: Some items are accessed frequently, others rarely
What happens: A burst of access to cold items can evict hot items

Example: A viral article floods the cache, evicting your homepage
→ After the burst, homepage must be re-fetched

Solution: LFU (Least Frequently Used) or hybrid (ARC, LIRS, TinyLFU)
```

**3. Predictable Access Patterns**

```
Problem: You know exactly when data will be needed
What happens: LRU ignores your domain knowledge

Example: Video streaming — you know frames are accessed in order
→ LRU might evict frame N+1 while buffering N+5

Solution: Use prefetching or domain-specific eviction
```

### When Simple is Better

```
DON'T use LRU when:
1. Data fits in memory     → Just keep everything, no eviction needed
2. Data never changes      → Preload and never evict
3. Uniform access pattern  → FIFO is simpler and nearly as good
4. Write-heavy workload    → Cache provides little benefit (stale reads)
5. TTL is more important   → Use time-based expiration instead
```

### Red Flags in Interviews

If you suggest LRU and the interviewer asks about these scenarios, consider
alternatives:

```
Q: "What if some items are accessed millions of times more than others?"
A: LFU might be better, or hybrid approaches like TinyLFU (used in Caffeine,
   a popular Java cache library).

Q: "What if data has an expiration time?"
A: Add TTL tracking to each entry, or use a pure TTL-based cache.
   Redis supports both LRU eviction and per-key TTL.

Q: "What if we're streaming large files?"
A: LRU will thrash — every new block evicts the previous one.
   Consider FIFO or specialized streaming buffers.

Q: "What if the cache needs to survive restarts?"
A: Add persistence (write-ahead log or snapshots).
   Redis and Memcached handle this in production.
```

---

## Common Variations

### 1. LRU Cache with TTL

```python
import time


# Extends the from-scratch LRUCache implementation above (not the OrderedDict version).
# Inherits: cache (dict), head/tail (DLinkedNode), _add_to_head, _remove_node,
#           _move_to_head, _remove_tail, get, put.
class LRUCacheWithTTL(LRUCache):
    """LRU Cache where entries expire after a fixed time-to-live."""

    def __init__(self, capacity: int, ttl_seconds: float) -> None:
        super().__init__(capacity)
        self.ttl = ttl_seconds
        self.timestamps: dict[int, float] = {}  # key -> expiry time

    def get(self, key: int) -> int:
        # Check expiry before delegating to parent
        if key in self.timestamps and time.time() > self.timestamps[key]:
            self._evict_key(key)
            return -1
        return super().get(key)

    def put(self, key: int, value: int) -> None:
        super().put(key, value)
        self.timestamps[key] = time.time() + self.ttl

    def _evict_key(self, key: int) -> None:
        """Remove a specific key from cache, list, and timestamps."""
        if key in self.cache:
            node = self.cache[key]
            self._remove_node(node)
            del self.cache[key]
        self.timestamps.pop(key, None)
```

### 2. LRU Cache with Get Callback (Read-Through Cache)

```python
from collections import OrderedDict
from typing import Callable


class LRUCacheWithCallback:
    """
    LRU Cache that automatically fetches missing values via a callback.

    This is the "read-through" caching pattern: callers never deal with
    cache misses directly — the cache handles fetching transparently.
    """

    def __init__(self, capacity: int, fetch_func: Callable[[int], int]) -> None:
        self.capacity = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()
        self.fetch_func = fetch_func

    def get(self, key: int) -> int:
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]

        # Cache miss — fetch value via callback and insert
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
def expensive_fetch(key: int) -> int:
    """Simulate an expensive database lookup."""
    print(f"  [DB] Fetching key {key}...")
    return key * 100

cache = LRUCacheWithCallback(10, expensive_fetch)
print(cache.get(5))   # Prints "[DB] Fetching key 5..." then 500
print(cache.get(5))   # 500 (served from cache, no fetch)
```

### 3. Thread-Safe LRU Cache

```python
from threading import Lock
from collections import OrderedDict


class ThreadSafeLRUCache:
    """LRU Cache safe for concurrent access from multiple threads.

    Uses a single Lock to serialize all operations. For higher throughput
    under heavy contention, consider sharding (multiple caches, each with
    its own lock, partitioned by key hash).
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()
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

1. **Capacity 1**: Only one item; every new `put` evicts the previous entry
2. **Get non-existent key**: Return -1, no side effects
3. **Put existing key**: Update value *and* move to head (don't insert a duplicate node)
4. **Put then immediate get**: Must return the just-inserted value
5. **Eviction order**: The item whose last access is oldest goes first
6. **Capacity 0**: Degenerate case — every `put` is immediately evicted (LeetCode guarantees capacity >= 1, but worth considering)
7. **Rapid update of same key**: `put(1,A)` then `put(1,B)` should not increase cache size — only update the value in-place
8. **Get updates recency**: `get(key)` counts as an access — it must move the node to head, not just return the value

---

## Interview Tips

1. **Explain the design first**: "I'll use a HashMap for O(1) lookup and a doubly linked list for O(1) reordering"
2. **Draw the structure**: Show how the HashMap points into the linked list
3. **Use sentinel nodes**: Explain why they simplify code (no null checks)
4. **Mention OrderedDict**: Shows you know Python, but implement from scratch
5. **Discuss extensions**: TTL, thread safety, distributed caching
6. **State complexities**: Explicitly say "O(1) time, O(capacity) space"

### Common Interview Follow-ups

```
Q: How would you make this distributed?
A: Consistent hashing to partition keys across nodes. Each node runs
   its own LRU cache. A coordinator routes requests by key hash.
   In practice, use Redis with built-in LRU eviction policy.

Q: How would you handle concurrent access?
A: Wrap get/put with a mutex (Lock). For higher throughput, shard the
   cache by key hash so different shards can be accessed in parallel.
   Lock-free approaches exist (CAS-based) but are much more complex.

Q: What if cache misses are expensive?
A: Use a read-through pattern: the cache itself calls a fetch function
   on miss. Add request coalescing (singleflight) so concurrent misses
   for the same key only trigger one fetch.

Q: LRU vs LFU — when would you pick each?
A: LRU is simpler and works well when recent access predicts future access.
   LFU is better when some items are consistently popular regardless of
   recency (e.g., a homepage). LFU is harder to implement (LC 460).
```

---

## Quick Reference / Cheat Sheet

```
┌─────────────────────────────────────────────────────────┐
│  LRU Cache = HashMap + Doubly Linked List               │
│                                                         │
│  HashMap:  key → Node        (O(1) lookup)              │
│  DLL:      head ↔ ... ↔ tail (O(1) reorder/evict)      │
│                                                         │
│  get(key):                                              │
│    1. Look up node in HashMap                           │
│    2. Move node to head (most recently used)            │
│    3. Return node.value                                 │
│                                                         │
│  put(key, val):                                         │
│    1. If key exists: update value, move to head          │
│    2. If new: create node, add to head + HashMap        │
│    3. If over capacity: remove tail.prev, delete from   │
│       HashMap using the evicted node's key              │
│                                                         │
│  Key details:                                           │
│    - Sentinel head/tail eliminate edge cases             │
│    - Node stores KEY so we can delete from HashMap      │
│      during eviction                                    │
│    - Doubly linked (not singly) for O(1) removal        │
│                                                         │
│  Time: O(1) all ops  |  Space: O(capacity)              │
└─────────────────────────────────────────────────────────┘
```

---

## Practice Problems

| #   | Problem                          | Difficulty | Key Concept                 |
| --- | -------------------------------- | ---------- | --------------------------- |
| 1   | Design Linked List (LC 707)      | Medium     | Practice DLL operations     |
| 2   | LRU Cache (LC 146)              | Medium     | Core implementation         |
| 3   | Design Browser History (LC 1472) | Medium     | Linked list navigation      |
| 4   | All O(1) Data Structure (LC 432) | Hard       | Similar combination pattern |
| 5   | LFU Cache (LC 460)              | Hard       | More complex eviction       |

### Progressive Coding Exercises

Work through these in order. Each builds on the previous one.

#### Exercise 1: Most Recent Key Tracker (Easy)

**Problem:** Build a class that always knows the N most recently accessed keys.
- `touch(key)` — mark a key as recently used
- `get_recent(n)` — return the n most recently used keys, most recent first
- If a key is touched again, it moves to the front (no duplicates)

This isolates the "recency tracking" part of LRU without the HashMap cache
layer.

```python
from collections import OrderedDict


class RecentKeyTracker:
    """Track the N most recently used keys using OrderedDict."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.keys: OrderedDict[str, None] = OrderedDict()

    def touch(self, key: str) -> None:
        """Mark key as recently used. If already present, move to end."""
        if key in self.keys:
            self.keys.move_to_end(key)
        else:
            self.keys[key] = None
            if len(self.keys) > self.capacity:
                self.keys.popitem(last=False)  # Drop oldest

    def get_recent(self, n: int) -> list[str]:
        """Return the n most recently used keys, most recent first."""
        all_keys = list(self.keys.keys())
        # OrderedDict keeps insertion order; end = most recent
        return list(reversed(all_keys[-n:]))


# --- Tests ---
tracker = RecentKeyTracker(4)
tracker.touch("a")
tracker.touch("b")
tracker.touch("c")
assert tracker.get_recent(2) == ["c", "b"]

tracker.touch("a")  # "a" moves to most recent
assert tracker.get_recent(3) == ["a", "c", "b"]

tracker.touch("d")
tracker.touch("e")  # Capacity 4: "b" is evicted
assert tracker.get_recent(5) == ["e", "d", "a", "c"]  # Only 4 exist

print("Exercise 1: All tests passed")
```

#### Exercise 2: LRU Cache with Miss Counter (Medium)

**Problem:** Implement a standard LRU cache (using OrderedDict) that also
tracks:
- Total number of cache hits
- Total number of cache misses
- A method `hit_rate()` that returns the hit ratio as a float (0.0 to 1.0)

This practices the core LRU pattern while adding observability — a common
real-world requirement.

```python
from collections import OrderedDict


class LRUCacheWithStats:
    """LRU Cache that tracks hit/miss statistics."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: int) -> int:
        if key in self.cache:
            self.hits += 1
            self.cache.move_to_end(key)
            return self.cache[key]
        self.misses += 1
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


# --- Tests ---
cache = LRUCacheWithStats(2)

cache.put(1, 10)
cache.put(2, 20)
assert cache.get(1) == 10    # Hit
assert cache.get(3) == -1    # Miss
assert cache.get(2) == 20    # Hit
assert cache.hits == 2
assert cache.misses == 1
assert abs(cache.hit_rate() - 2 / 3) < 1e-9

cache.put(3, 30)             # Evicts key 1
assert cache.get(1) == -1    # Miss (was evicted)
assert cache.misses == 2

# Edge case: no gets yet
empty = LRUCacheWithStats(5)
assert empty.hit_rate() == 0.0

print("Exercise 2: All tests passed")
```

#### Exercise 3: LRU Cache from Scratch with `peek` and `keys_by_recency` (Hard)

**Problem:** Build an LRU cache from scratch (HashMap + Doubly Linked List, no
OrderedDict) with two extra methods:
- `peek(key)` — return the value without changing recency order (useful for
  debugging/monitoring without perturbing the cache)
- `keys_by_recency()` — return all keys from most recently used to least
  recently used

This forces you to understand the linked list internals, since `peek` must
bypass the move-to-head logic and `keys_by_recency` must traverse the list.

```python
from __future__ import annotations


class Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev: Node | None = None
        self.next: Node | None = None


class LRUCacheExtended:
    """
    From-scratch LRU Cache with peek() and keys_by_recency().

    Time: O(1) for get, put, peek
    Time: O(n) for keys_by_recency (must traverse list)
    Space: O(capacity)
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: dict[int, Node] = {}
        # Sentinel nodes
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    # --- internal helpers ---

    def _add_after_head(self, node: Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node  # type: ignore[union-attr]
        self.head.next = node

    def _detach(self, node: Node) -> None:
        node.prev.next = node.next  # type: ignore[union-attr]
        node.next.prev = node.prev  # type: ignore[union-attr]

    def _move_to_head(self, node: Node) -> None:
        self._detach(node)
        self._add_after_head(node)

    def _pop_tail(self) -> Node:
        node = self.tail.prev  # type: ignore[union-attr]
        assert node is not self.head, "Cannot pop from empty cache"
        self._detach(node)
        return node

    # --- public API ---

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            node = Node(key, value)
            self.cache[key] = node
            self._add_after_head(node)
            if len(self.cache) > self.capacity:
                lru = self._pop_tail()
                del self.cache[lru.key]

    def peek(self, key: int) -> int:
        """Return value WITHOUT updating recency. O(1).

        Useful for monitoring or debugging the cache state without
        perturbing the eviction order.
        """
        if key not in self.cache:
            return -1
        return self.cache[key].value

    def keys_by_recency(self) -> list[int]:
        """Return keys from most recently used to least. O(n).

        Traverses the linked list from head to tail.
        """
        result: list[int] = []
        current = self.head.next
        while current is not self.tail:
            result.append(current.key)  # type: ignore[union-attr]
            current = current.next      # type: ignore[union-attr]
        return result


# --- Tests ---
cache = LRUCacheExtended(3)
cache.put(1, 10)
cache.put(2, 20)
cache.put(3, 30)
assert cache.keys_by_recency() == [3, 2, 1]  # 3 is most recent

# get(1) moves key 1 to head
assert cache.get(1) == 10
assert cache.keys_by_recency() == [1, 3, 2]

# peek(2) returns value WITHOUT changing order
assert cache.peek(2) == 20
assert cache.keys_by_recency() == [1, 3, 2]  # Order unchanged

# Eviction: put(4) should evict key 2 (LRU)
cache.put(4, 40)
assert cache.get(2) == -1  # Evicted
assert cache.keys_by_recency() == [4, 1, 3]

# peek on missing key
assert cache.peek(99) == -1

# Update existing key
cache.put(3, 300)
assert cache.get(3) == 300
assert cache.keys_by_recency() == [3, 4, 1]  # 3 moved to front

# Capacity 1 edge case
tiny = LRUCacheExtended(1)
tiny.put(1, 100)
tiny.put(2, 200)  # Evicts key 1
assert tiny.get(1) == -1
assert tiny.get(2) == 200
assert tiny.keys_by_recency() == [2]

print("Exercise 3: All tests passed")
```

---

## Related Sections

- [Data Structure Choices](./01-data-structure-choices.md) - When to use which structure
- [LFU Cache](./03-lfu-cache.md) - More complex eviction policy (frequency-based)
