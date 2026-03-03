# Chapter 17: System Design Basics

This chapter bridges the gap between data structures/algorithms and system design interviews. While full system design requires understanding of distributed systems, here we focus on the **data structure choices** that appear in both coding rounds and system design discussions.

## Prerequisites

- Solid understanding of **HashMap**, **Linked List**, and **Heap** (Chapters 1-16)
- Familiarity with Big-O analysis for time and space
- Basic knowledge of how caches and APIs work (helpful, not required)

## Learning Objectives

By the end of this chapter, you should be able to:

1. **Choose the right data structure** for a given access pattern and justify the trade-offs
2. **Implement an LRU Cache** from scratch using HashMap + Doubly Linked List (O(1) get/put)
3. **Implement an LFU Cache** with frequency buckets and min_freq tracking (O(1) get/put)
4. **Implement common rate limiting algorithms** (Token Bucket, Sliding Window, Leaky Bucket)
5. **Reason about trade-offs** aloud: memory vs speed, accuracy vs simplicity, read vs write optimization
6. **Connect coding problems to system design**: extend LRU to distributed caching, rate limiters to API gateways

---

## Chapter Contents

| #   | Topic | Summary | Key Concepts |
| --- | ----- | ------- | ------------ |
| 01  | [Data Structure Choices](./01-data-structure-choices.md) | When to use HashMap vs Tree vs Heap. Covers the three fundamental trade-offs (speed/ordering, memory/speed, read/write), decision flowcharts, "when NOT to use" guidance, and combination patterns (HashMap+DLL, HashMap+Heap, HashMap+TreeMap). Includes worked exercises: frequency tracker, sliding window max, stock price tracker. | Trade-offs, decision flowcharts, combination patterns |
| 02  | [LRU Cache](./02-lru-cache.md) | Full implementation of Least Recently Used cache using both OrderedDict and from-scratch HashMap + Doubly Linked List. Covers why doubly-linked (not singly), sentinel nodes, visual traces, when LRU fails (scans, frequency-heavy workloads), and variants (TTL, callbacks, thread-safe). Includes progressive exercises. | HashMap + DLL, O(1) get/put, temporal locality |
| 03  | [LFU Cache](./03-lfu-cache.md) | Least Frequently Used cache with O(1) operations using frequency buckets. Covers the min_freq trick, LRU tie-breaking within frequency groups, cache pollution problem, LRU vs LFU decision matrix, and decay/aging strategies. Includes both DLL-based and OrderedDict-based implementations. | Frequency buckets, min_freq tracking, LRU tie-breaking |
| 04  | [Rate Limiter](./04-rate-limiter.md) | Five rate limiting algorithms with implementations: Token Bucket, Leaky Bucket, Fixed Window, Sliding Window Log, and Sliding Window Counter. Covers algorithm selection, distributed rate limiting with Redis + Lua scripts, HTTP rate limit headers, per-user tiered limits, and testable clock injection. | Token bucket, sliding window, distributed coordination |

### Suggested Reading Order

```
1. Data Structure Choices (01) -- foundational trade-offs used everywhere
2. LRU Cache (02)              -- the canonical "combine two structures" problem
3. LFU Cache (03)              -- builds directly on LRU concepts
4. Rate Limiter (04)           -- bridges into system design thinking
```

---

## Building Intuition

### Why System Design Questions Test Data Structures

System design questions aren't just about drawing boxes and arrows--they're fundamentally about **choosing the right data structures for the right job**. Here's the key insight:

> **Every system design decision is a data structure decision in disguise.**

When someone asks "Design a URL shortener," they're really asking "What data structure gives O(1) bidirectional lookup?" (Answer: Two hashmaps--one mapping short->long, one mapping long->short). When they ask "Design a rate limiter," they're asking "What data structure efficiently tracks time-bounded events?" (Answer: Queue/deque with timestamps, or a token bucket with a counter).

### The Mental Model: Building Blocks

Think of system design data structures as LEGO blocks:

```
+-----------------------------------------------------------------+
|                       BUILDING BLOCKS                           |
+-----------------------------------------------------------------+
|  HashMap     ->  O(1) avg lookup by key (the "index")           |
|  Linked List ->  O(1) insert/delete at known node (the "shuffler")|
|  Heap        ->  O(1) peek min/max, O(log n) push/pop ("priority")|
|  Queue/Deque ->  O(1) ends access (the "time orderer")          |
|  Trie        ->  O(L) prefix lookup, L=key length ("autocomplete")|
+-----------------------------------------------------------------+
```

The magic happens when you **combine** these blocks. LRU Cache isn't a new data structure--it's HashMap + Doubly Linked List working together. This modular thinking is what interviewers want to see.

> **Note on Heap complexity**: A common misconception is that heaps give O(1) insertion and extraction. Heaps give O(1) *peek* at the min/max, but push and pop are O(log n) due to the heapify step. This matters when comparing heap-based vs. bucket-based approaches (e.g., LFU cache).

### Why O(1) Matters So Much

In interviews, you'll notice an obsession with O(1) operations. Here's why:

**Scale amplifies differences.** At 10 requests/second, O(1) vs O(log n) doesn't matter. At 100,000 requests/second:

- O(1) = consistent microsecond latency regardless of data size
- O(log n) = grows with data size (e.g., log2(1 billion) ~ 30 operations), causes tail latency spikes
- O(n) = completely unusable at scale--scanning a million items per request is a non-starter

Real systems like Redis, Memcached, and API gateways handle millions of operations per second. Every extra operation counts.

## Why This Matters for Interviews

1. **Hybrid questions**: "Design an LRU cache" is both a coding and design question
2. **Trade-off discussions**: Interviewers want to hear you reason about choices
3. **Follow-up questions**: "How would this scale?" after coding solutions
4. **System design warm-up**: Shows you can think beyond just algorithms

---

## Core Topics

| Topic                  | Interview Relevance         | Example Questions                    |
| ---------------------- | --------------------------- | ------------------------------------ |
| Data Structure Choices | Trade-off discussions       | "Why HashMap over TreeMap?"          |
| LRU Cache              | Very common coding question | "Implement LRU with O(1) operations" |
| LFU Cache              | Advanced cache question     | "Implement LFU cache"                |
| Rate Limiter           | System design staple        | "Design API rate limiting"           |

---

## When These Topics Appear

### Coding Interviews

- **LRU Cache**: Frequently asked at Google, Meta, Amazon
- **LFU Cache**: Asked at top-tier companies for senior roles
- **Rate Limiter**: Sliding window, token bucket implementations

### System Design Interviews

- **Cache Design**: Eviction policies, distributed caching
- **Rate Limiting**: API gateways, DDoS protection
- **Data Store Selection**: When to use Redis vs DynamoDB vs PostgreSQL

---

## Key Patterns

### 1. Combining Data Structures

Most system design data structure problems require **combining** structures:

```
LRU Cache = HashMap + Doubly Linked List
LFU Cache = HashMap + Frequency Map + Doubly Linked Lists
Rate Limiter = Queue/Deque + Counter or HashMap
```

### 2. O(1) Requirement

System design problems often require O(1) for core operations:

```
Common O(1) building blocks:
* HashMap: O(1) avg lookup, insert, delete (amortized)
* Doubly Linked List: O(1) insert/delete at known node (requires pointer to node)
* Deque: O(1) append/pop at both ends
* OrderedDict: O(1) lookup + maintains insertion order (HashMap + DLL under the hood)
```

### 3. Eviction Strategies

| Strategy                    | When to Evict | Use Case        |
| --------------------------- | ------------- | --------------- |
| LRU (Least Recently Used)   | Oldest access | General caching |
| LFU (Least Frequently Used) | Lowest count  | Hot/cold data   |
| FIFO (First In First Out)   | Oldest insert | Simple queue    |
| TTL (Time To Live)          | Expired items | Session data    |

#### Choosing the Right Eviction Strategy

**LRU (Least Recently Used):**

- Best for: General-purpose caching where recent access predicts future access
- Key insight: Temporal locality--if you accessed it recently, you'll likely access it again
- Example: Browser cache, OS page cache

**LFU (Least Frequently Used):**

- Best for: Workloads with clear "hot" and "cold" items where popularity is stable over time
- Key insight: Frequency matters more than recency when popularity is stable
- Warning: Suffers from "cache pollution"--items that were popular early on may never get evicted even after they become cold. Mitigate with aging (decay counts over time) or a hybrid LRU-LFU approach
- Example: CDN caching for popular static assets, database query plan caches

**FIFO (First In First Out):**

- Best for: When insertion order is the only signal
- Key insight: Simplest to implement, no access tracking needed
- Example: Message queues, log buffers

**TTL (Time To Live):**

- Best for: Data that becomes stale after a known time
- Key insight: Time-based validity, not access-based
- Example: Session tokens, DNS cache, API response cache

---

## When NOT to Use These Patterns

Understanding when NOT to apply system design patterns is just as important as knowing how to implement them.

### Don't Over-Engineer Simple Requirements

```
X WRONG: Using LFU cache for a config store that's read once at startup
V RIGHT: Simple dictionary, no eviction needed

X WRONG: Token bucket rate limiter for a batch job that runs once daily
V RIGHT: No rate limiting, or simple counter if needed

X WRONG: Complex distributed cache for 100 key-value pairs
V RIGHT: In-memory dictionary, replicated to each node
```

### Anti-Patterns to Avoid

1. **Caching Write-Heavy Data**: Caches work best for read-heavy workloads. If you're updating cached data more often than reading it, you're adding complexity without benefit.

2. **Rate Limiting Everything**: Not every endpoint needs rate limiting. Internal service-to-service calls often don't need it. Focus on external APIs and expensive operations.

3. **Premature Optimization**: Don't design for 1 million requests/second when you have 100. Start simple, measure, then optimize.

4. **Ignoring Cache Invalidation**: "There are only two hard things in computer science: cache invalidation and naming things." If you can't define when cached data is stale, don't cache it.

5. **Single-Structure Thinking**: If you find yourself adding O(n) operations to maintain a property, you probably need a second data structure.

---

## Important Trade-offs

When choosing data structures for system design, consider these common trade-offs:

1. **Memory vs. Time:** Caching (using more memory) to avoid repeated computations (saving time). This is the most common trade-off--almost every cache, index, or precomputed lookup table is an instance of this.
2. **Read vs. Write Performance:** Some structures optimize for fast reads (e.g., HashMaps, B-trees with indexes), while others optimize for fast writes (e.g., LSM trees, append-only logs). You rarely get both--this is why databases offer different storage engines.
3. **Consistency vs. Availability (CAP Theorem):** In distributed systems, during a network partition you must choose: return stale data (Availability, AP) or reject requests until data is confirmed fresh (Consistency, CP). Note: CAP is about behavior *during partitions*--outside of partitions, you can have both.
4. **Complexity vs. Performance:** A simple array might be slower than a balanced tree for lookups, but it's easier to implement, debug, and maintain. Start simple and optimize when profiling shows a bottleneck.

## Implementation Template: Generic Cache

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Hashable

K = TypeVar('K', bound=Hashable)  # Keys must be hashable for dict-based caches
V = TypeVar('V')

class Cache(ABC, Generic[K, V]):
    """
    Abstract base class for cache implementations.
    All core operations (get, put, evict) should aim for O(1) time complexity.
    
    Subclasses: LRUCache, LFUCache, FIFOCache, etc.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError(f"Capacity must be positive, got {capacity}")
        self.capacity: int = capacity

    @abstractmethod
    def get(self, key: K) -> Optional[V]:
        """Retrieve value by key and update access metadata (e.g., recency, frequency)."""
        ...

    @abstractmethod
    def put(self, key: K, value: V) -> None:
        """Insert or update a key-value pair. Evict if at capacity."""
        ...

    @abstractmethod
    def _evict(self) -> None:
        """Remove one entry according to the eviction policy."""
        ...

    @abstractmethod
    def __len__(self) -> int:
        """Return current number of items in the cache."""
        ...

    @abstractmethod
    def __contains__(self, key: K) -> bool:
        """
        Check if key exists WITHOUT updating access metadata.
        
        WARNING: Do NOT implement this as `self.get(key) is not None` --
        get() has side effects (updates recency/frequency). Each subclass
        must implement this by checking the underlying HashMap directly.
        """
        ...

    def is_full(self) -> bool:
        """Check if the cache is at capacity."""
        return len(self) >= self.capacity
```

---

## Common Mistakes

1. **Forgetting edge cases**: Capacity of 1, duplicate keys (put with existing key should update, not add), getting a non-existent key
2. **Not maintaining order**: LRU must move accessed items to front--both on `get()` and `put()` of existing keys
3. **Wrong complexity**: Using `list.remove(value)` is O(n)--use a doubly linked list with a hashmap pointing to nodes for O(1) removal
4. **Thread safety**: Production caches need locks or concurrent data structures (usually not required in interviews, but worth mentioning)
5. **Ignoring capacity**: Not evicting when full, or evicting before checking if the key already exists (updating an existing key shouldn't trigger eviction)
6. **Off-by-one in capacity**: Inserting first and then evicting can momentarily exceed capacity--evict first, then insert

---

## Time Complexity Goals

| Operation       | Target      | How to Achieve                                                |
| --------------- | ----------- | ------------------------------------------------------------- |
| Get (lookup)    | O(1) avg    | HashMap for direct key->value (or key->node) mapping            |
| Put (insert)    | O(1) avg    | HashMap insert + linked list append                           |
| Evict           | O(1)        | Maintain a pointer/reference to the eviction candidate (e.g., list tail) |
| Update access   | O(1)        | Doubly linked list: unlink node + relink at head (requires node reference from HashMap) |
| Update frequency| O(1)        | LFU: frequency bucket map with DLL per bucket (see [LFU Cache](./03-lfu-cache.md)) |

---

## Interview Tips

1. **Start with the interface**: Define `get()` and `put()` signatures first--this shows structured thinking
2. **Explain trade-offs aloud**: "I'm using a HashMap for O(1) lookup, combined with a doubly linked list for O(1) reordering..."
3. **Draw the structure**: Sketch node connections on the whiteboard. Show how the HashMap points into the linked list
4. **Handle edge cases explicitly**: Empty cache, single-item cache, updating an existing key, eviction when full
5. **Mention production concerns**: Thread safety (locks/CAS), persistence, distributed invalidation, TTL expiry
6. **Know the Python shortcuts**: `collections.OrderedDict` gives you LRU for free with `move_to_end()` and `popitem(last=False)`. Use it to show awareness, then offer to implement from scratch

---

## Connection to Full System Design

| Coding Problem        | System Design Extension                                          |
| --------------------- | ---------------------------------------------------------------- |
| LRU Cache             | Distributed cache (Redis, Memcached), consistent hashing for sharding |
| LFU Cache             | CDN edge caching, database buffer pool management                |
| Rate Limiter          | API Gateway, load balancer, DDoS protection, per-user throttling |
| Data structure choice | Database selection (SQL vs NoSQL), indexing strategies, LSM vs B-tree |
| Hit Counter           | Real-time analytics, monitoring dashboards, time-series databases |

---

## Classic Problems by Company

| Company   | Favorite Problems                                          |
| --------- | ---------------------------------------------------------- |
| Google    | LRU Cache, Design HashMap, Design Hit Counter              |
| Meta      | LRU Cache, LFU Cache, Design Twitter Feed                  |
| Amazon    | LRU Cache, Design Rate Limiter, Time-Based Key-Value Store |
| Microsoft | LRU Cache, Design In-Memory File System                    |
| Apple     | Design Data Structure (multiple ops O(1))                  |

---

## Practice Problems (Progressive Difficulty)

Build your skills from foundational to advanced. Each tier builds on the previous one.

### Tier 1: Foundations (Warm-Up)

These ensure you understand the building blocks before combining them.

| #   | Problem                                                                                             | Key Concept                          | Target Complexity |
| --- | --------------------------------------------------------------------------------------------------- | ------------------------------------ | ----------------- |
| 1   | [Design HashMap](https://leetcode.com/problems/design-hashmap/) (LC 706)                            | Hash function, collision handling    | O(1) avg          |
| 2   | [Design HashSet](https://leetcode.com/problems/design-hashset/) (LC 705)                            | Hashing without values               | O(1) avg          |
| 3   | [Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) (LC 232)| Combining structures for new behavior| O(1) amortized    |
| 4   | [Min Stack](https://leetcode.com/problems/min-stack/) (LC 155)                                      | Auxiliary structure for O(1) min     | O(1) all ops      |

### Tier 2: Core Cache & Counter Problems

The bread-and-butter of system design coding rounds.

| #   | Problem                                                                                                         | Key Concept                           | Target Complexity   |
| --- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------- | ------------------- |
| 5   | [LRU Cache](https://leetcode.com/problems/lru-cache/) (LC 146)                                                  | HashMap + Doubly Linked List          | O(1) get/put        |
| 6   | [Design Hit Counter](https://leetcode.com/problems/design-hit-counter/) (LC 362)                                 | Queue/deque with timestamps           | O(1) hit, O(n) get* |
| 7   | [Logger Rate Limiter](https://leetcode.com/problems/logger-rate-limiter/) (LC 359)                               | HashMap + TTL concept                 | O(1)                |
| 8   | [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) (LC 981)                 | HashMap + Binary Search on timestamps | O(1) set, O(log n) get |

*\*Hit Counter `getHits` can be O(1) with a fixed-size circular buffer if the time window is bounded.*

### Tier 3: Advanced Cache & Design

These are the problems that separate good from great in interviews.

| #   | Problem                                                                                                                 | Key Concept                                 | Target Complexity |
| --- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ----------------- |
| 9   | [LFU Cache](https://leetcode.com/problems/lfu-cache/) (LC 460)                                                          | Frequency buckets + HashMap + DLL           | O(1) get/put      |
| 10  | [Design In-Memory File System](https://leetcode.com/problems/design-in-memory-file-system/) (LC 588)                     | Trie (directory tree) + HashMap             | O(path length)    |
| 11  | [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) (LC 380)                       | HashMap + dynamic array (swap trick)        | O(1) all ops      |
| 12  | [Design Twitter](https://leetcode.com/problems/design-twitter/) (LC 355)                                                 | HashMap + Heap merge (k sorted lists)       | O(k log k) feed   |

### Tier 4: System Design Coding Challenges

These bridge pure coding into system design thinking.

| #   | Problem                                                                                                                          | Key Concept                         | System Design Tie-In      |
| --- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------- |
| 13  | [Design a Leaderboard](https://leetcode.com/problems/design-a-leaderboard/) (LC 1244)                                            | HashMap + sorted structure           | Real-time ranking systems |
| 14  | [Snapshot Array](https://leetcode.com/problems/snapshot-array/) (LC 1146)                                                         | Versioning via binary search         | MVCC / copy-on-write      |
| 15  | [Design Underground System](https://leetcode.com/problems/design-underground-system/) (LC 1396)                                   | HashMap for in-flight + aggregation  | Metrics / analytics       |
| 16  | [Insert Delete GetRandom O(1) - Duplicates](https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed/) (LC 381)| HashMap (key->set of indices) + array | Multiset with random      |

### Suggested Practice Order

```
Week 1: Tier 1 (problems 1-4)  -- Build foundations, get comfortable with structure design
Week 2: Tier 2 (problems 5-8)  -- Master the core patterns (LRU is a must-know)
Week 3: Tier 3 (problems 9-12) -- Tackle advanced problems, practice explaining trade-offs
Week 4: Tier 4 (problems 13-16)-- Bridge to system design, practice extending solutions
```

### How to Approach Each Problem

1. **Define the API first**: What methods are needed? What are the inputs/outputs?
2. **State complexity goals**: "I need O(1) for get and put" -- this drives data structure selection
3. **Pick building blocks**: Which combination of HashMap / LinkedList / Heap / Array achieves those goals?
4. **Implement and test**: Walk through examples manually before coding
5. **Discuss extensions**: How would this change in a distributed setting? What about thread safety?

---

## Solved Practice Problems

These worked examples demonstrate the core patterns from the building blocks above. Study the approach before looking at the code.

### Problem 1: Design HashMap (LC 706) -- Easy

**Problem:** Implement a HashMap without using any built-in hash table libraries. Support `put(key, value)`, `get(key)`, and `remove(key)`. Keys and values are integers in range `[0, 10^6]`.

**Approach:**
- Use an array of buckets (chaining with linked lists for collision handling).
- Hash function: `key % num_buckets`. A prime-sized bucket count reduces clustering.
- Each bucket is a list of `(key, value)` pairs. On collision, append to the list.
- Trade-off: More buckets = fewer collisions = faster lookup, but more memory.

```python
class MyHashMap:
    """
    Hash map using separate chaining (list of lists).
    
    Time:  O(1) average for all operations (O(n/k) worst case per bucket)
    Space: O(n + k) where n = number of entries, k = number of buckets
    """

    def __init__(self) -> None:
        self._size = 1009  # Prime number reduces hash collisions
        self._buckets: list[list[tuple[int, int]]] = [[] for _ in range(self._size)]

    def _hash(self, key: int) -> int:
        return key % self._size

    def put(self, key: int, value: int) -> None:
        bucket = self._buckets[self._hash(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update existing key
                return
        bucket.append((key, value))  # New key

    def get(self, key: int) -> int:
        bucket = self._buckets[self._hash(key)]
        for k, v in bucket:
            if k == key:
                return v
        return -1  # Not found

    def remove(self, key: int) -> None:
        bucket = self._buckets[self._hash(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return
```

**Key takeaway:** This is the foundation -- understanding how HashMaps work internally helps you reason about O(1) amortized complexity and worst-case degradation.

---

### Problem 2: LRU Cache (LC 146) -- Medium

**Problem:** Design a data structure that follows the Least Recently Used (LRU) eviction policy. Implement `get(key)` and `put(key, value)`, both in O(1) time. When the cache exceeds capacity, evict the least recently used item.

**Approach:**
- **HashMap** maps `key -> node` for O(1) lookup.
- **Doubly Linked List** maintains access order (most recent at head, least recent at tail).
- On `get`: move the accessed node to the head.
- On `put`: insert at head; if over capacity, remove from tail.
- Sentinel head/tail nodes simplify edge cases (no null checks).

```python
class _DLLNode:
    """Doubly linked list node for LRU cache."""
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0) -> None:
        self.key = key
        self.val = val
        self.prev: "_DLLNode | None" = None
        self.next: "_DLLNode | None" = None


class LRUCache:
    """
    LRU Cache using HashMap + Doubly Linked List.
    
    Time:  O(1) for both get and put
    Space: O(capacity)
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: dict[int, _DLLNode] = {}  # key -> node

        # Sentinel nodes: head.next = MRU, tail.prev = LRU
        self.head = _DLLNode()
        self.tail = _DLLNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _DLLNode) -> None:
        """Unlink a node from the doubly linked list. O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node: _DLLNode) -> None:
        """Insert a node right after the head sentinel (marks as MRU). O(1)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        # Move to head (mark as most recently used)
        self._remove(node)
        self._add_to_head(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing: change value, move to head
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_head(node)
        else:
            # Insert new node at head
            new_node = _DLLNode(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

            # Evict LRU (tail.prev) if over capacity
            if len(self.cache) > self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
```

**Alternative -- using Python's `OrderedDict`:**

```python
from collections import OrderedDict

class LRUCacheSimple:
    """LRU Cache using OrderedDict (interview shortcut)."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # Mark as most recently used
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Evict least recently used (front)
```

**Key takeaway:** LRU Cache is the canonical "combine two data structures" problem. Know both the from-scratch implementation (for coding rounds) and the `OrderedDict` shortcut (for speed).

---

### Problem 3: Insert Delete GetRandom O(1) (LC 380) -- Medium

**Problem:** Implement a data structure that supports `insert(val)`, `remove(val)`, and `getRandom()` -- all in average O(1) time. `getRandom` returns a random element with equal probability.

**Approach:**
- **HashMap** maps `value -> index` in an array for O(1) lookup.
- **Dynamic array (list)** stores values for O(1) random access via `random.choice`.
- **Trick for O(1) removal:** Swap the element to remove with the last element, then pop from the end (O(1) list pop from the end vs. O(n) pop from the middle).

```python
import random


class RandomizedSet:
    """
    O(1) insert, remove, and getRandom using HashMap + array swap trick.
    
    Time:  O(1) average for all operations
    Space: O(n)
    """

    def __init__(self) -> None:
        self.val_to_index: dict[int, int] = {}  # value -> index in self.values
        self.values: list[int] = []

    def insert(self, val: int) -> bool:
        """Insert val if not present. Returns True if inserted."""
        if val in self.val_to_index:
            return False
        self.val_to_index[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val: int) -> bool:
        """Remove val if present. Returns True if removed."""
        if val not in self.val_to_index:
            return False

        # Swap val with the last element, then pop
        idx = self.val_to_index[val]
        last_val = self.values[-1]

        self.values[idx] = last_val           # Overwrite with last
        self.val_to_index[last_val] = idx     # Update last's index
        self.values.pop()                     # Remove last (O(1))
        del self.val_to_index[val]            # Remove val from map
        return True

    def getRandom(self) -> int:
        """Return a random element with equal probability."""
        return random.choice(self.values)
```

**Key takeaway:** The swap-to-end trick is a versatile pattern. It appears whenever you need O(1) deletion from an unordered collection while maintaining random access.

---

### Problem 4: LFU Cache (LC 460) -- Hard

**Problem:** Design a Least Frequently Used (LFU) cache. When evicting, remove the item with the lowest frequency. If there's a tie in frequency, evict the least recently used item among them. Both `get` and `put` must be O(1).

**Approach:**
- **`key_to_val`** HashMap: `key -> value` for O(1) value lookup.
- **`key_to_freq`** HashMap: `key -> frequency` for O(1) frequency lookup.
- **`freq_to_keys`** HashMap: `frequency -> OrderedDict` -- each frequency bucket is an OrderedDict maintaining insertion/access order (acts as a mini-LRU within each frequency tier).
- **`min_freq`** integer: tracks the current minimum frequency for O(1) eviction.
- On `get`: increment the key's frequency, move it from old bucket to new bucket.
- On `put` (new key at capacity): evict the LRU item from the `min_freq` bucket.

```python
from collections import OrderedDict, defaultdict


class LFUCache:
    """
    LFU Cache with O(1) get and put using frequency buckets.
    
    Each frequency bucket is an OrderedDict acting as an LRU within that
    frequency tier. This handles the tie-breaking rule: among items with
    the same frequency, evict the least recently used.
    
    Time:  O(1) for get and put
    Space: O(capacity)
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.key_to_val: dict[int, int] = {}
        self.key_to_freq: dict[int, int] = {}
        # Each frequency maps to an OrderedDict of keys (preserves LRU order)
        self.freq_to_keys: defaultdict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)
        self.min_freq = 0

    def _update_freq(self, key: int) -> None:
        """Move key from its current frequency bucket to the next one."""
        freq = self.key_to_freq[key]
        # Remove from old frequency bucket
        del self.freq_to_keys[freq][key]

        # If old bucket is now empty and was the min, increment min_freq
        if not self.freq_to_keys[freq] and freq == self.min_freq:
            self.min_freq += 1

        # Add to new frequency bucket
        new_freq = freq + 1
        self.key_to_freq[key] = new_freq
        self.freq_to_keys[new_freq][key] = None  # OrderedDict as ordered set

    def get(self, key: int) -> int:
        if key not in self.key_to_val:
            return -1
        self._update_freq(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.key_to_val:
            # Update existing key
            self.key_to_val[key] = value
            self._update_freq(key)
            return

        # Evict if at capacity
        if len(self.key_to_val) >= self.capacity:
            # Evict LRU key from the lowest frequency bucket
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]

        # Insert new key with frequency 1
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1  # New key always has freq 1, which is the new minimum
```

**Key takeaway:** LFU is the hardest cache problem you'll see in interviews. The critical insight is using `min_freq` to achieve O(1) eviction, and OrderedDict per frequency bucket for LRU tie-breaking. If you can implement this cleanly, you can handle any cache variant.

---

## Navigation

| Previous | Next |
| -------- | ---- |
| [Chapter 16: Math Basics](../16-math-basics/) | [Chapter 18: Low-Level Design (LLD)](../18-low-level-design/) |

For large-scale architecture topics, see [Chapter 19: High-Level Design (HLD)](../19-high-level-design/).
