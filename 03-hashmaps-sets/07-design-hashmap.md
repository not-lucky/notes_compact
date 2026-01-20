# Design HashMap

> **Prerequisites:** [01-hash-table-basics.md](./01-hash-table-basics.md)

## Interview Context

"Design a HashMap" is a classic interview problem that tests:

1. **Hash function understanding**: How to map keys to indices
2. **Collision handling**: Chaining vs open addressing
3. **API design**: put, get, remove operations
4. **Trade-off awareness**: Time vs space, load factor

This problem appears at Google, Amazon, and many other companies.

**Interview frequency**: Medium. Important for demonstrating data structure knowledge.

---

## Building Intuition

**Why This Problem Matters**

"Design a HashMap" isn't about memorizing code—it tests whether you truly understand:
- How hash tables achieve O(1) average time
- What happens when things go wrong (collisions)
- The trade-offs between different approaches

**Mental Model: The Postal System**

Think of a HashMap like a post office with numbered PO boxes:
```
Key "John" → hash("John") = 42 → PO Box #42

To find John's mail:
- Don't search all boxes (O(n))
- Calculate his box number directly → O(1)
```

But what if two people hash to the same box? That's collision handling.

**Chaining: One Box, Many Cubbies**

```
Box #42: [("John", mail1), ("Jane", mail2)]

When both hash to 42:
- Store both in the same box
- Look through the list to find the right person
- Average case: still O(1) if boxes aren't too crowded
```

**Open Addressing: Find Another Box**

```
"John" → Box #42 (occupied by "Jane")
→ Try #43 (occupied)
→ Try #44 (empty!) → Store here

Lookup: Same process—start at hash, probe until found or empty.
```

**Why Prime Numbers for Bucket Size?**

Keys often have patterns (IDs like 100, 200, 300...). If bucket size is 100:
```
100 % 100 = 0
200 % 100 = 0
300 % 100 = 0  ← All collide!
```

Prime bucket size (e.g., 97) breaks patterns:
```
100 % 97 = 3
200 % 97 = 6
300 % 97 = 9  ← Better distribution!
```

**Load Factor: How Full Is Too Full?**

```
Load factor = items / buckets

α = 0.3: Wasteful (too many empty buckets)
α = 0.7: Good balance
α = 1.5: Too crowded (long chains, slow lookups)
```

Python dict resizes at ~0.66 load factor.

---

## When NOT to Implement Your Own HashMap

**1. Production Code**

Built-in `dict` is:
- Heavily optimized (C implementation)
- Tested for edge cases
- Thread-safe for basic operations (GIL)

Roll your own only for learning or specialized needs.

**2. Ordered Access Required**

Standard hashmaps don't maintain order:
```python
# Need sorted keys? → Use sortedcontainers.SortedDict
# Need insertion order? → Use collections.OrderedDict (or Python 3.7+ dict)
```

**3. Range Queries**

Hashmaps only support exact key lookup:
```python
# "All keys between 10 and 20" → O(n) scan
# Use BST or sorted structure instead
```

**4. Persistent/Immutable Version Needed**

Standard hashmap mutates in place. For immutable versions:
- Functional data structures (HAMTs)
- Copy-on-write patterns

**5. Memory Is Extremely Constrained**

Hashmaps trade space for time:
```python
# 1000 integers: list ~8KB, dict ~36KB
# For embedded/constrained environments, consider alternatives
```

**Interview Tip:**
Interviewers want to see you CAN implement a hashmap. But always mention that in production, you'd use the built-in `dict`.

---

## Core Design Decisions

### 1. Hash Function
- Use Python's built-in `hash()` or a custom function
- Apply modulo to fit within array bounds

### 2. Collision Handling
- **Chaining**: Each bucket stores a list of key-value pairs
- **Open Addressing**: Probe for next available slot

### 3. Bucket Size
- Larger = fewer collisions, more space
- Common choice: 1000 or prime number

---

## Template: Design HashMap (Chaining)

```python
class MyHashMap:
    """
    LeetCode 706: Design HashMap

    Operations:
    - put(key, value): Insert or update
    - get(key): Return value or -1 if not found
    - remove(key): Remove if exists

    Time: O(n/k) average for all operations, where k = bucket count
    Space: O(n + k)
    """

    def __init__(self):
        self.size = 1000  # Number of buckets
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        """Compute bucket index for a key."""
        return key % self.size

    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair."""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        # Check if key exists, update if found
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Key not found, append new pair
        bucket.append((key, value))

    def get(self, key: int) -> int:
        """Return value for key, or -1 if not found."""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for k, v in bucket:
            if k == key:
                return v

        return -1

    def remove(self, key: int) -> None:
        """Remove key if it exists."""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return
```

### Visual Representation

```
buckets (size=5):

[0]: []
[1]: [(1, "one"), (6, "six")]  ← 1 % 5 = 1, 6 % 5 = 1
[2]: [(7, "seven")]
[3]: [(3, "three"), (8, "eight")]
[4]: [(4, "four")]

get(6):
1. hash(6) = 6 % 5 = 1
2. Search bucket[1]: [(1, "one"), (6, "six")]
3. Found (6, "six") → return "six"
```

---

## Template: Design HashSet

```python
class MyHashSet:
    """
    LeetCode 705: Design HashSet

    Operations:
    - add(key): Insert key
    - contains(key): Check if key exists
    - remove(key): Remove if exists

    Time: O(n/k) average
    Space: O(n + k)
    """

    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def add(self, key: int) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]

        if key not in bucket:
            bucket.append(key)

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]

        if key in bucket:
            bucket.remove(key)

    def contains(self, key: int) -> bool:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        return key in bucket
```

---

## Template: HashMap with Linked List Buckets

```python
class ListNode:
    def __init__(self, key=-1, val=-1, next=None):
        self.key = key
        self.val = val
        self.next = next


class MyHashMapLinked:
    """
    HashMap using linked list for buckets.
    More memory efficient than list of tuples for sparse data.
    """

    def __init__(self):
        self.size = 1000
        # Each bucket starts with a dummy head
        self.buckets = [ListNode() for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def put(self, key: int, value: int) -> None:
        idx = self._hash(key)
        curr = self.buckets[idx]

        while curr.next:
            if curr.next.key == key:
                curr.next.val = value
                return
            curr = curr.next

        curr.next = ListNode(key, value)

    def get(self, key: int) -> int:
        idx = self._hash(key)
        curr = self.buckets[idx].next

        while curr:
            if curr.key == key:
                return curr.val
            curr = curr.next

        return -1

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        curr = self.buckets[idx]

        while curr.next:
            if curr.next.key == key:
                curr.next = curr.next.next
                return
            curr = curr.next
```

---

## Template: HashMap with Open Addressing

```python
class MyHashMapOpenAddressing:
    """
    HashMap using linear probing for collision handling.

    Uses sentinel values:
    - None: never used
    - DELETED: was used, now deleted (tombstone)
    """

    DELETED = object()  # Tombstone marker

    def __init__(self):
        self.size = 10007  # Prime number for better distribution
        self.keys = [None] * self.size
        self.values = [None] * self.size
        self.count = 0

    def _hash(self, key: int) -> int:
        return key % self.size

    def _find_slot(self, key: int) -> int:
        """Find slot for key (existing or empty)."""
        idx = self._hash(key)
        first_deleted = -1

        while self.keys[idx] is not None:
            if self.keys[idx] == key:
                return idx
            if self.keys[idx] is self.DELETED and first_deleted == -1:
                first_deleted = idx
            idx = (idx + 1) % self.size

        return first_deleted if first_deleted != -1 else idx

    def put(self, key: int, value: int) -> None:
        idx = self._find_slot(key)

        if self.keys[idx] != key:
            self.count += 1

        self.keys[idx] = key
        self.values[idx] = value

        # Resize if load factor > 0.7
        if self.count > 0.7 * self.size:
            self._resize()

    def get(self, key: int) -> int:
        idx = self._hash(key)

        while self.keys[idx] is not None:
            if self.keys[idx] == key:
                return self.values[idx]
            idx = (idx + 1) % self.size

        return -1

    def remove(self, key: int) -> None:
        idx = self._hash(key)

        while self.keys[idx] is not None:
            if self.keys[idx] == key:
                self.keys[idx] = self.DELETED
                self.values[idx] = None
                self.count -= 1
                return
            idx = (idx + 1) % self.size

    def _resize(self):
        """Double size and rehash all elements."""
        old_keys = self.keys
        old_values = self.values

        self.size *= 2
        self.keys = [None] * self.size
        self.values = [None] * self.size
        self.count = 0

        for i, key in enumerate(old_keys):
            if key is not None and key is not self.DELETED:
                self.put(key, old_values[i])
```

---

## Template: HashMap with Better Hash Function

```python
class MyHashMapBetterHash:
    """
    HashMap with multiplicative hash function.
    Better distribution for integer keys.
    """

    def __init__(self):
        self.size = 1009  # Prime number
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        """
        Multiplicative hashing.
        Uses golden ratio for better distribution.
        """
        # Knuth's multiplicative hash
        A = 0.6180339887  # (sqrt(5) - 1) / 2
        return int(self.size * ((key * A) % 1))

    # ... rest same as basic implementation
```

---

## Template: HashMap Supporting String Keys

```python
class StringHashMap:
    """
    HashMap that supports string keys.
    """

    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: str) -> int:
        """
        Polynomial rolling hash for strings.

        h = s[0]*p^(n-1) + s[1]*p^(n-2) + ... + s[n-1]*p^0
        """
        hash_value = 0
        p = 31  # Prime base
        p_pow = 1

        for char in key:
            hash_value = (hash_value + (ord(char) - ord('a') + 1) * p_pow) % self.size
            p_pow = (p_pow * p) % self.size

        return hash_value

    def put(self, key: str, value) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))

    def get(self, key: str):
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for k, v in bucket:
            if k == key:
                return v

        return None

    def remove(self, key: str) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return
```

---

## Chaining vs Open Addressing

| Aspect | Chaining | Open Addressing |
|--------|----------|-----------------|
| Collision handling | Linked list per bucket | Probe for next slot |
| Space | Extra for pointers | Compact |
| Cache performance | Poor (pointer chasing) | Good (contiguous) |
| Deletion | Simple | Needs tombstones |
| Load factor tolerance | Can exceed 1.0 | Must stay < 1.0 |
| Implementation | Simpler | More complex |

**Interview tip**: Chaining is easier to implement and explain. Choose it unless asked specifically about open addressing.

---

## Load Factor and Resizing

```python
def _should_resize(self) -> bool:
    """Check if resizing is needed."""
    load_factor = self.count / self.size
    return load_factor > 0.75

def _resize(self):
    """
    Double size and rehash all elements.

    Time: O(n)
    Amortized: Still O(1) per operation
    """
    old_buckets = self.buckets

    self.size *= 2
    self.buckets = [[] for _ in range(self.size)]
    self.count = 0

    for bucket in old_buckets:
        for key, value in bucket:
            self.put(key, value)
```

---

## Choosing Bucket Size

| Size | Pros | Cons |
|------|------|------|
| Small (100) | Less memory | More collisions |
| Medium (1000) | Good balance | Standard choice |
| Large (10007) | Fewer collisions | More memory |
| Prime | Better distribution | Slightly slower mod |

**Why prime?** Reduces clustering when keys have patterns (e.g., multiples of 10).

---

## Edge Cases

```python
# Key = 0
hashmap.put(0, "zero")  # 0 % size = 0, bucket[0]

# Negative keys (Python handles mod correctly)
(-5) % 1000  # 995 in Python (not -5)

# Very large keys
(10**9) % 1000  # Works fine

# Duplicate puts (update)
hashmap.put(1, "a")
hashmap.put(1, "b")  # Should update, not add

# Remove non-existent key
hashmap.remove(999)  # Should do nothing, not error

# Get non-existent key
hashmap.get(999)  # Should return -1 or None
```

---

## Common Interview Follow-ups

1. **"How would you handle resizing?"**
   - Double the size when load factor > 0.75
   - Rehash all existing elements

2. **"What if keys are strings?"**
   - Use polynomial rolling hash

3. **"How do you handle hash collisions?"**
   - Explain chaining vs open addressing

4. **"What's the worst-case complexity?"**
   - O(n) when all keys hash to same bucket

5. **"How would you make it thread-safe?"**
   - Lock per bucket or read-write locks

---

## Practice Problems

| # | Problem | Difficulty | Focus |
|---|---------|------------|-------|
| 1 | Design HashMap | Easy | Basic implementation |
| 2 | Design HashSet | Easy | Simpler variant |
| 3 | Two Sum | Easy | Use HashMap |
| 4 | LRU Cache | Medium | HashMap + doubly linked list |
| 5 | Insert Delete GetRandom O(1) | Medium | HashMap + array |
| 6 | First Unique Character | Easy | HashMap counting |
| 7 | Logger Rate Limiter | Easy | HashMap with timestamps |

---

## Key Takeaways

1. **Use chaining for interviews** - simpler to implement and explain
2. **Bucket size ~1000** is a reasonable default
3. **Prime sizes reduce clustering** for patterned keys
4. **Load factor ~0.75** triggers resizing
5. **Time complexity is O(n/k)** where k = bucket count
6. **Hash function must be deterministic** - same key = same hash

---

## Next: [08-advanced-patterns.md](./08-advanced-patterns.md)

Learn advanced hashmap patterns including LRU Cache and RandomizedSet.
