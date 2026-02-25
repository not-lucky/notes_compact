# Hash Table Basics

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

## Interview Context

Understanding hash tables at a conceptual level is crucial because:

1. **Design questions**: "Design a HashMap" is a common interview problem.
2. **Optimization discussions**: Knowing why $O(1)$ is an "average case" (amortized) and $O(n)$ in the worst case (due to hash collisions).
3. **Trade-off awareness**: Space vs time, load factor decisions.
4. **Edge case handling**: Collision scenarios, worst-case behavior.

Interviewers want to see that you understand _why_ hash tables work, not just _that_ they work.

---

## Building Intuition

**Why $O(1)$ Lookup Is "Magic"**

Think of a hash table like a huge filing cabinet with numbered drawers:

```
Regular list: "Find John's file"
→ Open drawer 1, not there
→ Open drawer 2, not there
→ ... (check every drawer) → O(n)

Hash table: "Find John's file"
→ hash("John") = 47
→ Open drawer 47 directly → O(1)
```

The hash function is like a magical index that tells you EXACTLY where to look.

**The Fundamental Trade-off: Space for Time**

Hash tables sacrifice memory for speed:

- You allocate MORE buckets than you have items.
- Most buckets are empty (wasted space).
- But lookups are instant (no searching).

```
Items: 10
Buckets: 16 (typical, with ~60% load factor)
Wasted space: 6 buckets

BUT: Every lookup is O(1) instead of O(n)
```

**Why Collisions Are Inevitable (Birthday Paradox)**

Even with a good hash function, collisions happen surprisingly often:

- With 23 people, there's a 50% chance two share a birthday.
- With $n$ buckets and $\sqrt{n}$ items, expect at least one collision.

This is why collision handling isn't optional—it's essential.

**Mental Model: Phone Book vs. Library**

```
Phone Book (Sorted List):
- Find "Smith" → binary search → O(log n)
- Must be kept sorted

Hash Table (Direct Dial):
- hash("Smith") → extension 4721
- Call directly → O(1)
- No sorting needed
```

**Why Only Immutable Keys?**

Imagine you file "John Doe" in drawer 47 (based on hash). Then "John" changes to "Jonathan":

- New hash = 89
- But the file is still in drawer 47
- Looking for "Jonathan" checks drawer 89 → NOT FOUND

The file is "lost" because the key changed. This is why Python requires immutable keys.

---

## When NOT to Use Hash Tables

**1. Order Matters**

Hash tables historically don't maintain insertion order or sorted order:

```python
# Need sorted iteration? → Use list + sort, or sortedcontainers
# Need oldest-first? → Use collections.deque
```

_Note: Python 3.7+ dicts guarantee insertion order, but many interviews are language-agnostic. Always clarify this if you rely on it._

**2. Memory Is Critical**

Hash tables use $2-3\times$ more memory than the data alone:

```python
import sys
# 1000 integers
l = [i for i in range(1000)]
d = {i: i for i in range(1000)}

sys.getsizeof(l)  # ~8KB
sys.getsizeof(d)  # ~36KB (4.5× more!)
```

For embedded systems or huge datasets, arrays may be better.

**3. Keys Aren't Hashable**

Lists, dicts, and other mutable objects can't be keys:

```python
d: dict[Any, int] = {}
d[["a", "b"]] = 1  # TypeError: unhashable type: 'list'
# Solution: d[tuple(["a", "b"])] = 1
```

If your keys are naturally mutable, you need a different structure or must convert them to an immutable representation.

**4. Range Queries or Nearest Neighbors**

Hash tables only support exact match lookups:

```python
# "Find all keys between 10 and 20" → O(n) scan
# "Find key closest to 15" → O(n) scan

# Use instead: Sorted array + binary search, or balanced BST
```

**5. Very Small Data Sets ($n < 10$)**

The overhead of hashing isn't worth it:

```python
# For 5 items, linear search in a list is often faster
# Cache locality matters more than O(1) vs O(n) at small scales
```

**Red Flags:**

- "Maintain sorted order" → Use sorted structure.
- "Find range of keys" → Use BST or sorted array.
- "Memory-constrained environment" → Use arrays.
- "Keys are mutable objects" → Convert to tuples or use a different approach.

---

## Core Concept: How Hash Tables Work

A hash table maps keys to values using a **hash function** that converts keys into array indices.

```
Key → Hash Function → Index → Bucket → Value

Example:
"apple" → hash("apple") → 17284 → 17284 % 10 → 4 → buckets[4]
```

### Visual Representation

```
Hash Function: key → index

     key          hash(key)    index (% size)
     ────         ─────────    ──────────────
    "cat"    →      294     →      4
    "dog"    →      317     →      7
    "bird"   →      412     →      2
    "fish"   →      414     →      4  ← Collision with "cat"!

Bucket Array (size=10):
    ┌───┬───┬────────┬───┬──────────────┬───┬───┬────────┬───┬───┐
    │   │   │ "bird" │   │ "cat"→"fish" │   │   │ "dog"  │   │   │
    ├───┼───┼────────┼───┼──────────────┼───┼───┼────────┼───┼───┤
    │ 0 │ 1 │   2    │ 3 │      4       │ 5 │ 6 │   7    │ 8 │ 9 │
    └───┴───┴────────┴───┴──────────────┴───┴───┴────────┴───┴───┘
              index       collision chain
```

---

## Hash Functions

### What Makes a Good Hash Function?

1. **Deterministic**: The same input always produces the exact same output.
2. **Uniform distribution**: Spreads keys evenly across buckets (minimizes collisions).
3. **Fast to compute**: $O(1)$ calculation for fixed-size keys, or $O(k)$ where $k$ is the length of the string/key.

### Python's Built-in hash()

```python
# Python computes hash for immutable types
print(hash("hello"))    # Varies by Python session (security feature)
print(hash(42))         # → 42 (small integers hash to themselves)
print(hash((1, 2, 3)))  # Varies

# Mutable types are NOT hashable
hash([1, 2, 3])  # TypeError: unhashable type: 'list'
hash({1: 2})     # TypeError: unhashable type: 'dict'
```

### Interview Insight: Why Lists Can't Be Keys

```python
# This is WHY mutable objects can't be dictionary keys:
my_list: list[int] = [1, 2, 3]
d: dict[Any, str] = {}
d[my_list] = "value"  # TypeError: unhashable type: 'list'

# If this worked, what happens after:
my_list.append(4)     # The list's contents change, so a new hash would be computed
# → The value would be lost in the wrong bucket!

# Solution: Convert to immutable
d[tuple(my_list)] = "value"  # Works!
```

---

## Collision Handling

When two keys hash to the same index, we have a **collision**. There are two main strategies:

### 1. Chaining (Separate Chaining)

Each bucket stores a linked list (or dynamic array) of key-value pairs.

```
Bucket 4 (at [0x500]):
[ ("cat", 1) | next: 0x540 ] ──→ [ ("fish", 2) | next: None ]
      [addr: 0x500]                    [addr: 0x540]

Lookup "fish":
1. hash("fish") % size = 4
2. Go to bucket 4
3. Traverse list: "cat"? No. "fish"? Yes!
4. Return value 2
```

```python
# Chaining implementation sketch (often expected in "Design HashMap" interviews)
class HashMapChaining:
    def __init__(self, size: int = 1000) -> None:
        self.size = size
        self.buckets: list[list[tuple[Any, Any]]] = [[] for _ in range(size)]

    def _hash(self, key: Any) -> int:
        return hash(key) % self.size

    def put(self, key: Any, value: Any) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update existing
                return

        bucket.append((key, value))  # Insert new

    def get(self, key: Any) -> Optional[Any]:
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for k, v in bucket:
            if k == key:
                return v

        return None  # Not found
```

### 2. Open Addressing (Linear Probing)

If a bucket is occupied, search for the next empty bucket sequentially (or using a probing sequence).

```
Insert "fish" (hash = 4), but bucket 4 is occupied by "cat":
→ Try bucket 5: empty!
→ Store "fish" at bucket 5

    ┌───┬───┬───┬───┬─────┬──────┬───┬───┬───┬───┐
    │   │   │   │   │"cat"│"fish"│   │   │   │   │
    └───┴───┴───┴───┴─────┴──────┴───┴───┴───┴───┘
      0   1   2   3    4     5     6   7   8   9
```

---

## Time Complexity Analysis

| Operation | Average Case (Amortized) | Worst Case (Many Collisions) |
| --------- | ------------------------ | ---------------------------- |
| Insert    | $\Theta(1)$              | $O(n)$                       |
| Lookup    | $\Theta(1)$              | $O(n)$                       |
| Delete    | $\Theta(1)$              | $O(n)$                       |

### Why Worst Case is $O(n)$

```
If all keys hash to the same bucket (a "Hash DOS" attack or terrible hash function):
Bucket 0: [k1] → [k2] → [k3] → ... → [kn]

Lookup kn requires traversing entire chain = O(n)
```

### Why Average Case is $O(1)$

With a good hash function and reasonable **load factor**, collisions are rare and mostly uniform.

```
Load Factor = n / m
where n = number of elements, m = number of buckets

Python dict maintains a max load factor of 2/3 (≈ 0.66)
→ Average bucket has < 1 element
→ Lookups require checking 1 or 2 items effectively giving O(1) time
```

---

## Load Factor and Resizing

### Load Factor

```
Load Factor α = n / m

α < 0.5  → Wasting space
α ≈ 0.7  → Good balance (Python resizes at 0.66)
α > 1.0  → Severe collisions (chaining) or probing delays (open addressing)
```

### Automatic Resizing

When the load factor exceeds the threshold:

1. Create a new array, typically with $2\times$ size (or more).
2. Rehash all existing keys using the new size `m`.
3. Insert into the new buckets.

```python
def _resize(self) -> None:
    """Double the size and rehash all elements. O(n) operation."""
    old_buckets = self.buckets
    self.size *= 2
    self.buckets = [[] for _ in range(self.size)]
    # count remains unchanged

    for bucket in old_buckets:
        for key, value in bucket:
            self.put(key, value)  # Rehash with new size
```

**Amortized $O(1)$**: An individual `_resize()` takes $O(n)$, but happens rarely enough (every $2^k$ insertions) that the _average_ insert operation remains $O(1)$.

---

## Python `dict` Internals (Interview Knowledge)

### Key Facts to Know

1. **Compact Representation**: Since Python 3.6, dicts use a compact representation that significantly reduces memory usage by storing an array of indices that point to a dense array of key-value-hash entries.
2. **Implementation**: Open addressing with pseudo-random probing for collision resolution (unlike chaining used in languages like Java).
3. **Load factor**: ~66% before resize.
4. **Growth**: Typically doubles ($2\times$) when resizing.
5. **Ordering**: Insertion order is guaranteed (language spec since Python 3.7).
6. **Negative Hash Modulo**: In Python, the modulo operator (`%`) with a negative dividend and positive divisor always returns a positive result (e.g., `-5 % 3 == 1`). This is different from C++ or Java where it can be negative (`-5 % 3 == -2`). Python handles negative hashes cleanly without needing `abs()` before modulo.
7. **Space**: While more efficient than older versions, dicts still use more memory than an equivalent list of tuples due to the hash table overhead.

```python
import sys

# Memory comparison
d = {i: i for i in range(1000)}
l = [(i, i) for i in range(1000)]

print(sys.getsizeof(d))  # ~36,960 bytes
print(sys.getsizeof(l))  # ~8,056 bytes (but lookups take O(n) instead of O(1))
```

---

## Template: Basic HashMap Operations

```python
from typing import Any, Optional

# Initialization
d: dict[str, int] = {}             # Empty dict
d = {"a": 1, "b": 2}               # With initial values
d = dict.fromkeys([1, 2, 3], 0)    # Keys mapping to a default 0

# Insert/Update -> O(1) amortized
d["key"] = 100

# Lookup -> O(1) amortized
value = d["key"]                   # Raises KeyError if missing
opt_val = d.get("missing")         # Returns None if missing
def_val = d.get("missing", -1)     # Returns default (-1) if missing

# Check existence -> O(1) amortized
if "key" in d:
    pass

# Deletion -> O(1) amortized
del d["key"]                       # Raises KeyError if missing
popped = d.pop("key", None)        # Returns value, or None if missing

# Iteration -> O(N) where N is the current size
for key in d:                      # Iterate keys
    pass
for value in d.values():           # Iterate values
    pass
for key, value in d.items():       # Iterate key-value tuples
    pass
```

---

## Template: defaultdict and Counter

```python
from collections import defaultdict, Counter

# defaultdict - Auto-initializes missing keys
freq: defaultdict[str, int] = defaultdict(int)  # Missing keys default to 0
freq["a"] += 1                                  # No KeyError! (Creates "a": 1)

graph: defaultdict[str, list[str]] = defaultdict(list)  # Missing default to []
graph["nodeA"].append("nodeB")                          # No KeyError!

# Counter - Specialized hash map for counting iterables
nums = [1, 2, 2, 3, 3, 3]
counts = Counter(nums)          # -> Counter({3: 3, 2: 2, 1: 1})

# Counter operations
top_k = counts.most_common(2)   # O(N log K) -> [(3, 3), (2, 2)]
counts["missing_key"]           # Returns 0, not KeyError
counts.update([1, 4])           # Add multiple counts
```

---

## Template: setdefault Pattern

```python
# setdefault: get value or set default if missing
# Returns the value (existing or newly set)

words = ["apple", "banana", "cherry", "apricot", "blueberry"]
groups: dict[str, list[str]] = {}

# Without setdefault
for word in words:
    char = word[0]
    if char not in groups:
        groups[char] = []
    groups[char].append(word)

# With setdefault (cleaner)
groups_clean: dict[str, list[str]] = {}
for word in words:
    groups_clean.setdefault(word[0], []).append(word)

# Result: {'a': ['apple', 'apricot'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}
```

---

## Edge Cases

```python
# Empty Dict
d: dict[str, Any] = {}
print(len(d))       # 0
print("key" in d)   # False
print(d.get("key")) # None

# None Value vs Missing Key
d = {"key": None}
print(d.get("key"))     # None
print(d.get("missing")) # None  <-- Same result!
print("key" in d)       # True  <-- Distinguishes key existence

# Mutable Default Arguments (Python Gotcha!)
# Never use empty mutable defaults `dict={}` or `list=[]`
def bad_function(d: dict = {}) -> dict:  # WRONG
    d["count"] = d.get("count", 0) + 1   # Modifies the persistent default object!
    return d

def good_function(d: Optional[dict] = None) -> dict:  # RIGHT
    if d is None:
        d = {}
    d["count"] = d.get("count", 0) + 1
    return d
```

---

## Complexity Summary

| Operation | `dict`              | `set`               | `list` (comparison)          |
| --------- | ------------------- | ------------------- | ---------------------------- |
| Insert    | $\Theta(1)$ amort.  | $\Theta(1)$ amort.  | $\Theta(1)$ amort. (append)  |
| Lookup    | $\Theta(1)$ amort.  | $\Theta(1)$ amort.  | $O(n)$                       |
| Delete    | $\Theta(1)$ amort.  | $\Theta(1)$ amort.  | $O(n)$                       |
| Space     | $O(n)$              | $O(n)$              | $O(n)$ (less overhead)       |

---

## Practice Problems

| #   | Problem                | Difficulty | Key Concept             |
| --- | ---------------------- | ---------- | ----------------------- |
| 1   | Design HashMap         | Easy       | Chaining implementation |
| 2   | Design HashSet         | Easy       | Set implementation      |
| 3   | Contains Duplicate     | Easy       | Set for uniqueness      |
| 4   | Jewels and Stones      | Easy       | Set lookup              |
| 5   | First Unique Character | Easy       | Frequency counting      |

---

## Key Takeaways

1. **Hash tables give $\Theta(1)$ amortized** time for insert, lookup, and delete.
2. **Collisions are handled** via chaining (linked lists) or open addressing (probing).
3. **Load factor matters** - Python maintains a max load factor of ~0.66.
4. **Only immutable types** can be dictionary keys (must be hashable).
5. **Use `defaultdict` and `Counter`** for cleaner frequency counting.
6. **Space-time trade-off**: Hash tables use significantly more memory to achieve their faster access times.

---

## Next: [02-two-sum-pattern.md](./02-two-sum-pattern.md)

Learn the classic two-sum pattern that appears in countless interview problems.
