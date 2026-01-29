# Advanced HashMap Patterns

> **Prerequisites:** [07-design-hashmap.md](./07-design-hashmap.md)

## Interview Context

Advanced hashmap patterns combine hash tables with other data structures to achieve complex O(1) operations. These appear in:

- LRU/LFU Cache design problems
- Randomized data structures
- Time-based key-value stores
- Snapshot arrays

These problems are **FAANG favorites** and test both data structure knowledge and system design thinking.

**Interview frequency**: High for senior roles. LRU Cache is extremely common.

---

## Building Intuition

**Why Combine Data Structures?**

Each structure excels at one thing:

- HashMap: O(1) lookup by key
- Array: O(1) access by index, random selection
- Linked List: O(1) insertion/deletion if you have the node
- Heap: O(1) min/max access

But real problems need MULTIPLE O(1) operations. The trick: use multiple structures that reference the same data.

**LRU Cache: The Classic Combo**

The requirements:

- O(1) get by key → need HashMap
- O(1) update recency → need quick reordering
- O(1) evict oldest → need access to oldest element

Array fails reordering. Heap fails arbitrary access. But Doubly Linked List:

- Move any node to front in O(1) (if you have the node pointer)
- Access oldest (tail) in O(1)

HashMap stores key → node pointer. DLL handles ordering. Together: O(1) everything.

**Mental Model: Library Book Tracking**

```
HashMap = Card catalog (find any book's location instantly)
DLL = Stack of "recently touched" books

Access a book:
1. Card catalog → find book's position in stack → O(1)
2. Move book to top of stack → O(1)
3. When shelf is full, remove bottom book → O(1)
```

**RandomizedSet: Why HashMap Alone Fails**

HashMap can't select random element in O(1):

```python
# To pick random key, you'd need to:
random.choice(list(hashmap.keys()))  # O(n) to create list!
```

Array gives O(1) random selection, but O(n) deletion (shifting).

The trick: **swap-to-end**:

```
[A, B, C, D] → delete B
Step 1: Swap B with D → [A, D, C, B]
Step 2: Pop last → [A, D, C]
```

HashMap tracks current index of each element.

**LFU Cache: The Harder Version**

LRU = evict "used longest ago"
LFU = evict "used fewest times" (with LRU as tiebreaker)

Why it's harder:

- Need to track frequency of each key
- Need O(1) access to "minimum frequency" keys
- Among min-frequency keys, need LRU order

Solution: HashMap + frequency buckets (each bucket is its own LRU list).

**Time-Based Store: When History Matters**

```
set("price", 100, timestamp=1)
set("price", 200, timestamp=5)
get("price", timestamp=3) → 100 (value at or before time 3)
```

Store sorted list of (timestamp, value) per key. Binary search for queries.

---

## When NOT to Use These Patterns

**1. Simpler Cache Policies Suffice**

LRU/LFU are complex. Consider simpler alternatives:

```python
# Random eviction: O(1), surprisingly effective
# FIFO: Just use deque, simple to implement
# LRU without full O(1): Use ordered dict (good enough for most cases)
```

**2. Cache Size Is Very Small**

For capacity < 100:

- O(n) operations are fast enough
- Use simple list + linear search
- Complexity overhead not worth it

**3. Memory Is More Constrained Than Time**

These patterns use 2-3× more memory than minimal structures:

```python
# LRU: HashMap + DLL = pointers + extra overhead
# RandomizedSet: HashMap + Array = store data twice
```

For memory-constrained systems, consider time/space trade-offs.

**4. Concurrency Is Critical**

These single-threaded implementations break under concurrent access:

- LRU: Updating recency while reading is a race condition
- RandomizedSet: Swap-delete is not atomic

Use concurrent data structures or proper locking.

**5. Distributed Systems**

Single-node caches don't scale:

```python
# For distributed cache: Redis, Memcached
# For distributed random selection: Reservoir sampling
```

**Red Flags:**

- "High concurrency" → Lock-free structures or external systems
- "Distributed system" → Redis, Memcached, etc.
- "Very small capacity" → Simple O(n) is fine
- "Memory-critical" → Simpler, leaner structures

---

## Template: LRU Cache

**Problem**: Design a data structure that follows the constraints of a Least Recently Used (LRU) cache. It should support `get(key)` and `put(key, value)` in O(1) time. When the cache reaches its capacity, it should invalidate the least recently used item before inserting a new item.

**Explanation**: We combine a hashmap with a doubly linked list. The hashmap provides O(1) access to any node in the list. The doubly linked list maintains the order of access, where the head is the most recently used and the tail is the least recently used. When an item is accessed or added, we move it to the head of the list.

```python
class LRUCache:
    """
    LeetCode 146: LRU Cache

    Least Recently Used cache with O(1) get and put.

    Key insight: HashMap for O(1) lookup, Doubly Linked List for O(1) reordering.

    Time: O(1) for both get and put
    Space: O(capacity)
    """

    class Node:
        def __init__(self, key=0, val=0):
            self.key = key
            self.val = val
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key → Node

        # Dummy head and tail for easier insertion/deletion
        self.head = self.Node()
        self.tail = self.Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Remove node from linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node):
        """Add node right after head (most recent)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]

        # Move to front (most recently used)
        self._remove(node)
        self._add_to_front(node)

        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_front(node)
        else:
            # Add new
            if len(self.cache) >= self.capacity:
                # Remove LRU (node before tail)
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

            node = self.Node(key, value)
            self.cache[key] = node
            self._add_to_front(node)
```

### Visual Representation

```
Capacity = 3

After put(1, 1), put(2, 2), put(3, 3):

head ⟷ [3] ⟷ [2] ⟷ [1] ⟷ tail
        ↑ most recent   ↑ least recent

cache = {1: Node(1), 2: Node(2), 3: Node(3)}

After get(1):

head ⟷ [1] ⟷ [3] ⟷ [2] ⟷ tail
        ↑ 1 moved to front

After put(4, 4) (capacity exceeded):

head ⟷ [4] ⟷ [1] ⟷ [3] ⟷ tail
                    ↑ 2 was evicted
```

---

## Template: LRU Cache (Using OrderedDict)

```python
from collections import OrderedDict

class LRUCacheSimple:
    """
    LRU Cache using Python's OrderedDict.
    Simpler but less instructive for interviews.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        # Move to end (most recent)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove oldest
```

---

## Template: LFU Cache

**Problem**: Design and implement a data structure for a Least Frequently Used (LFU) cache. It should support `get` and `put` operations in O(1) time. When the cache is full, it should remove the item with the lowest frequency. If there is a tie in frequency, the least recently used item among them should be removed.

**Explanation**: We use two hashmaps. One maps keys to their (value, frequency) pair. The second maps each frequency to an `OrderedDict` of keys that have that frequency. The `OrderedDict` acts as an LRU list for that specific frequency. We also maintain a `min_freq` variable to quickly find which frequency bucket to evict from when the cache is full.

```python
from collections import defaultdict

class LFUCache:
    """
    LeetCode 460: LFU Cache

    Least Frequently Used cache with O(1) get and put.

    Uses:
    - key → (value, frequency) mapping
    - frequency → OrderedDict of keys (for LRU within same frequency)
    - min_freq to track minimum frequency

    Time: O(1) for both get and put
    Space: O(capacity)
    """

    def __init__(self, capacity: int):
        from collections import OrderedDict

        self.capacity = capacity
        self.cache = {}  # key → [value, freq]
        self.freq_to_keys = defaultdict(OrderedDict)  # freq → OrderedDict of keys
        self.min_freq = 0

    def _update_freq(self, key: int):
        """Increment frequency and update structures."""
        value, freq = self.cache[key]

        # Remove from old frequency bucket
        del self.freq_to_keys[freq][key]

        # Update min_freq if needed
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        # Add to new frequency bucket
        new_freq = freq + 1
        self.freq_to_keys[new_freq][key] = None
        self.cache[key] = [value, new_freq]

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        self._update_freq(key)
        return self.cache[key][0]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.cache:
            self.cache[key][0] = value
            self._update_freq(key)
        else:
            if len(self.cache) >= self.capacity:
                # Evict LFU (and LRU among those)
                lfu_keys = self.freq_to_keys[self.min_freq]
                evict_key, _ = lfu_keys.popitem(last=False)
                del self.cache[evict_key]

            # Add new key with frequency 1
            self.cache[key] = [value, 1]
            self.freq_to_keys[1][key] = None
            self.min_freq = 1
```

---

## Template: Insert Delete GetRandom O(1)

**Problem**: Implement the `RandomizedSet` class which supports `insert`, `remove`, and `getRandom` operations, all in O(1) average time complexity.

**Explanation**: To achieve O(1) for all operations, we combine a hashmap and a dynamic array (list). The hashmap stores the value as a key and its index in the array as the value. For `getRandom`, we pick a random index from the array. For `remove`, we swap the element to be deleted with the last element in the array to avoid O(n) shifting, then update the hashmap and pop from the array.

```python
import random

class RandomizedSet:
    """
    LeetCode 380: Insert Delete GetRandom O(1)

    All operations in O(1) average time.

    Key insight: HashMap for O(1) lookup, Array for O(1) random access.
    Swap-to-end trick for O(1) deletion.

    Time: O(1) for all operations
    Space: O(n)
    """

    def __init__(self):
        self.val_to_idx = {}  # value → index in array
        self.values = []      # array of values

    def insert(self, val: int) -> bool:
        if val in self.val_to_idx:
            return False

        self.val_to_idx[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.val_to_idx:
            return False

        # Swap with last element
        idx = self.val_to_idx[val]
        last_val = self.values[-1]

        self.values[idx] = last_val
        self.val_to_idx[last_val] = idx

        # Remove last element
        self.values.pop()
        del self.val_to_idx[val]

        return True

    def getRandom(self) -> int:
        return random.choice(self.values)
```

### Visual: Remove Operation

```
values = [3, 7, 2, 5]
val_to_idx = {3: 0, 7: 1, 2: 2, 5: 3}

remove(7):
1. idx = 1
2. last_val = 5
3. Swap: values = [3, 5, 2, 5]
4. Update: val_to_idx = {3: 0, 5: 1, 2: 2, 5: 3}
5. Pop: values = [3, 5, 2]
6. Delete: val_to_idx = {3: 0, 5: 1, 2: 2}
```

---

## Template: Insert Delete GetRandom O(1) - Duplicates Allowed

**Problem**: Similar to `RandomizedSet`, but the data structure should allow duplicate elements.

**Explanation**: Instead of storing a single index in the hashmap, we store a `set` of indices for each value. When removing an element, we pick any one of its indices and swap it with the last element in the array, updating the index sets for both values accordingly.

```python
import random
from collections import defaultdict

class RandomizedCollection:
    """
    LeetCode 381: Insert Delete GetRandom O(1) - Duplicates allowed

    Time: O(1) for all operations
    Space: O(n)
    """

    def __init__(self):
        self.val_to_indices = defaultdict(set)  # value → set of indices
        self.values = []

    def insert(self, val: int) -> bool:
        self.val_to_indices[val].add(len(self.values))
        self.values.append(val)
        return len(self.val_to_indices[val]) == 1

    def remove(self, val: int) -> bool:
        if not self.val_to_indices[val]:
            return False

        # Get an index of val to remove
        remove_idx = self.val_to_indices[val].pop()

        last_val = self.values[-1]

        if remove_idx != len(self.values) - 1:
            # Swap with last
            self.values[remove_idx] = last_val
            self.val_to_indices[last_val].add(remove_idx)
            self.val_to_indices[last_val].discard(len(self.values) - 1)

        self.values.pop()

        return True

    def getRandom(self) -> int:
        return random.choice(self.values)
```

---

## Template: Time-Based Key-Value Store

**Problem**: Design a time-based key-value data structure that can store multiple values for the same key at different timestamps and retrieve the key's value at a certain timestamp.

**Explanation**: We use a hashmap where each key maps to a list of `(timestamp, value)` pairs. Since timestamps are added in increasing order, the lists remain sorted. To retrieve a value at or before a specific timestamp, we use binary search (`bisect_right`) on the list for that key.

```python
import bisect
from collections import defaultdict

class TimeMap:
    """
    LeetCode 981: Time Based Key-Value Store

    Store key-value pairs with timestamps.
    get(key, timestamp) returns value at or before timestamp.

    Time: O(1) for set, O(log n) for get
    Space: O(n)
    """

    def __init__(self):
        self.store = defaultdict(list)  # key → [(timestamp, value), ...]

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""

        values = self.store[key]

        # Binary search for largest timestamp <= given timestamp
        # bisect_right finds insertion point, so -1 gives us the answer
        idx = bisect.bisect_right(values, (timestamp, chr(127)))

        if idx == 0:
            return ""

        return values[idx - 1][1]
```

---

## Template: Snapshot Array

**Problem**: Implement a `SnapshotArray` that supports `set(index, val)`, `snap()`, and `get(index, snap_id)`. `get` returns the value at the given index at the time the snapshot with `snap_id` was taken.

**Explanation**: Instead of copying the entire array during a snapshot (which is inefficient), we store the history of changes for each index. Each index maps to a list of `(snap_id, value)` pairs. When `get` is called, we perform binary search on the history list of that index to find the largest `snap_id` that is less than or equal to the requested `snap_id`.

```python
import bisect

class SnapshotArray:
    """
    LeetCode 1146: Snapshot Array

    Support snapshots and historical lookups.

    Time: O(log S) for get where S = number of snaps for that index
    Space: O(n + S)
    """

    def __init__(self, length: int):
        # Each index stores list of (snap_id, value)
        self.history = [[(-1, 0)] for _ in range(length)]
        self.snap_id = 0

    def set(self, index: int, val: int) -> None:
        self.history[index].append((self.snap_id, val))

    def snap(self) -> int:
        current_snap = self.snap_id
        self.snap_id += 1
        return current_snap

    def get(self, index: int, snap_id: int) -> int:
        history = self.history[index]
        # Binary search for largest snap_id <= given snap_id
        idx = bisect.bisect_right(history, (snap_id, float('inf'))) - 1
        return history[idx][1]
```

---

## Template: All O'one Data Structure

**Problem**: Design a data structure that supports `inc(key)`, `dec(key)`, `getMaxKey()`, and `getMinKey()` in O(1) time.

**Explanation**: This requires a hashmap combined with a doubly linked list of "buckets." Each bucket represents a specific frequency (count) and contains a set of keys with that count. When a key's frequency changes, it moves to an adjacent bucket in the list. This ensures that the buckets with minimum and maximum counts are always at the ends of the linked list.

```python
class AllOne:
    """
    LeetCode 432: All O'one Data Structure

    Inc, Dec, GetMaxKey, GetMinKey all in O(1).

    Uses: HashMap + Doubly Linked List of frequency buckets.
    """

    class Bucket:
        def __init__(self, count=0):
            self.count = count
            self.keys = set()
            self.prev = None
            self.next = None

    def __init__(self):
        self.key_to_bucket = {}  # key → Bucket

        # Dummy head and tail
        self.head = self.Bucket(0)
        self.tail = self.Bucket(float('inf'))
        self.head.next = self.tail
        self.tail.prev = self.head

    def _insert_after(self, prev_bucket, new_bucket):
        new_bucket.prev = prev_bucket
        new_bucket.next = prev_bucket.next
        prev_bucket.next.prev = new_bucket
        prev_bucket.next = new_bucket

    def _remove_bucket(self, bucket):
        bucket.prev.next = bucket.next
        bucket.next.prev = bucket.prev

    def inc(self, key: str) -> None:
        if key not in self.key_to_bucket:
            # New key with count 1
            if self.head.next.count != 1:
                new_bucket = self.Bucket(1)
                self._insert_after(self.head, new_bucket)
            self.head.next.keys.add(key)
            self.key_to_bucket[key] = self.head.next
        else:
            # Increment existing key
            curr_bucket = self.key_to_bucket[key]
            new_count = curr_bucket.count + 1

            if curr_bucket.next.count != new_count:
                new_bucket = self.Bucket(new_count)
                self._insert_after(curr_bucket, new_bucket)

            curr_bucket.next.keys.add(key)
            self.key_to_bucket[key] = curr_bucket.next

            curr_bucket.keys.remove(key)
            if not curr_bucket.keys:
                self._remove_bucket(curr_bucket)

    def dec(self, key: str) -> None:
        if key not in self.key_to_bucket:
            return

        curr_bucket = self.key_to_bucket[key]
        new_count = curr_bucket.count - 1

        if new_count == 0:
            del self.key_to_bucket[key]
        else:
            if curr_bucket.prev.count != new_count:
                new_bucket = self.Bucket(new_count)
                self._insert_after(curr_bucket.prev, new_bucket)

            curr_bucket.prev.keys.add(key)
            self.key_to_bucket[key] = curr_bucket.prev

        curr_bucket.keys.remove(key)
        if not curr_bucket.keys:
            self._remove_bucket(curr_bucket)

    def getMaxKey(self) -> str:
        if self.tail.prev == self.head:
            return ""
        return next(iter(self.tail.prev.keys))

    def getMinKey(self) -> str:
        if self.head.next == self.tail:
            return ""
        return next(iter(self.head.next.keys))
```

---

## Template: Logger Rate Limiter

**Problem**: Design a logger system that receives a stream of messages with their timestamps. Each unique message should only be printed at most every 10 seconds.

**Explanation**: We use a hashmap to store each message and the timestamp of its last successful print. When a new message arrives, we check if it has been printed in the last 10 seconds. If not, we update the timestamp and return `true`; otherwise, we return `false`.

```python
class Logger:
    """
    LeetCode 359: Logger Rate Limiter

    Returns true if message should be printed (not printed in last 10 seconds).

    Time: O(1)
    Space: O(M) where M = number of unique messages
    """

    def __init__(self):
        self.message_time = {}  # message → last timestamp

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if message not in self.message_time:
            self.message_time[message] = timestamp
            return True

        if timestamp - self.message_time[message] >= 10:
            self.message_time[message] = timestamp
            return True

        return False
```

---

## Pattern Summary

| Problem          | Data Structures               | Key Insight                 |
| ---------------- | ----------------------------- | --------------------------- |
| LRU Cache        | HashMap + Doubly Linked List  | DLL for O(1) reorder        |
| LFU Cache        | HashMap + Freq Buckets        | Track min frequency         |
| RandomizedSet    | HashMap + Array               | Swap-to-end for O(1) delete |
| Time-Based Store | HashMap + Sorted List         | Binary search on timestamps |
| Snapshot Array   | Array of history lists        | Binary search per index     |
| All O'one        | HashMap + DLL of freq buckets | Bucket per frequency        |

---

## Common Interview Follow-ups

1. **"What if the cache is distributed?"**
   - Consistent hashing for key distribution
   - Each node runs local LRU

2. **"How would you handle cache eviction policies?"**
   - LRU, LFU, FIFO, Random
   - Trade-offs between implementation complexity and hit rate

3. **"What about thread safety?"**
   - Lock-free data structures or fine-grained locking
   - Read-write locks for read-heavy workloads

4. **"How would you handle TTL (expiration)?"**
   - Lazy expiration on access + background cleanup thread

---

## Practice Problems

| #   | Problem                            | Difficulty | Pattern                  |
| --- | ---------------------------------- | ---------- | ------------------------ |
| 1   | LRU Cache                          | Medium     | HashMap + DLL            |
| 2   | LFU Cache                          | Hard       | HashMap + Freq buckets   |
| 3   | Insert Delete GetRandom O(1)       | Medium     | HashMap + Array          |
| 4   | Insert Delete GetRandom Duplicates | Hard       | HashMap + Array + Set    |
| 5   | Time Based Key-Value Store         | Medium     | HashMap + Binary Search  |
| 6   | Snapshot Array                     | Medium     | History + Binary Search  |
| 7   | All O'one Data Structure           | Hard       | HashMap + DLL of buckets |
| 8   | Logger Rate Limiter                | Easy       | HashMap with timestamp   |
| 9   | Design Twitter                     | Medium     | HashMap + Merge K        |
| 10  | Design Hit Counter                 | Medium     | Queue or array buffer    |

---

## Key Takeaways

1. **Combine data structures** for complex O(1) operations
2. **HashMap + DLL** is the pattern for LRU/ordering problems
3. **HashMap + Array** with swap-to-end for random + delete
4. **Binary search on sorted history** for time-based problems
5. **Frequency buckets** (not counters) for LFU-style problems
6. **Always consider** thread safety and distributed scenarios in follow-ups

---

## Chapter Complete

You've completed Chapter 03: HashMaps & Sets. Continue to Chapter 04: Linked Lists for the next topic.
