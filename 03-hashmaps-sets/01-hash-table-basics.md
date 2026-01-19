# Hash Table Basics

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

## Interview Context

Understanding hash tables at a conceptual level is crucial because:

1. **Design questions**: "Design a HashMap" is a common interview problem
2. **Optimization discussions**: Knowing why O(1) is "average case" not "always"
3. **Trade-off awareness**: Space vs time, load factor decisions
4. **Edge case handling**: Collision scenarios, worst-case behavior

Interviewers want to see that you understand *why* hash tables work, not just *that* they work.

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
    ┌───┬───┬──────┬───┬────────────┬───┬───┬─────┬───┬───┐
    │   │   │"bird"│   │"cat"→"fish"│   │   │"dog"│   │   │
    └───┴───┴──────┴───┴────────────┴───┴───┴─────┴───┴───┘
      0   1    2     3       4        5   6    7    8   9
```

---

## Hash Functions

### What Makes a Good Hash Function?

1. **Deterministic**: Same input always produces same output
2. **Uniform distribution**: Spreads keys evenly across buckets
3. **Fast to compute**: O(1) for fixed-size keys

### Python's Built-in hash()

```python
# Python computes hash for immutable types
hash("hello")    # → 8733897261432381906 (varies by session)
hash(42)         # → 42
hash((1, 2, 3))  # → 529344067295497451

# Mutable types are NOT hashable
hash([1, 2, 3])  # TypeError: unhashable type: 'list'
hash({1: 2})     # TypeError: unhashable type: 'dict'
```

### Interview Insight: Why Lists Can't Be Keys

```python
# This is WHY mutable objects can't be dictionary keys:
my_list = [1, 2, 3]
d = {}
d[my_list] = "value"  # TypeError!

# If this worked, what happens after:
my_list.append(4)     # Hash would change, but key is "same" object
# → The value would be lost in the wrong bucket!

# Solution: Convert to immutable
d[tuple(my_list)] = "value"  # Works!
```

---

## Collision Handling

When two keys hash to the same index, we have a **collision**. Two main strategies:

### 1. Chaining (Separate Chaining)

Each bucket stores a linked list of key-value pairs.

```
Bucket 4: [("cat", 1)] → [("fish", 2)] → None

Lookup "fish":
1. hash("fish") % size = 4
2. Go to bucket 4
3. Traverse list: "cat"? No. "fish"? Yes!
4. Return value 2
```

```python
# Chaining implementation sketch
class HashMapChaining:
    def __init__(self, size=1000):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def put(self, key, value):
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update
                return

        bucket.append((key, value))  # Insert

    def get(self, key):
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for k, v in bucket:
            if k == key:
                return v

        return None  # Not found
```

### 2. Open Addressing (Linear Probing)

If a bucket is occupied, look for the next empty one.

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

| Operation | Average Case | Worst Case |
|-----------|--------------|------------|
| Insert    | O(1)         | O(n)       |
| Lookup    | O(1)         | O(n)       |
| Delete    | O(1)         | O(n)       |

### Why Worst Case is O(n)

```
If all keys hash to the same bucket:
Bucket 0: [k1] → [k2] → [k3] → ... → [kn]

Lookup kn requires traversing entire chain = O(n)
```

### Why Average Case is O(1)

With a good hash function and reasonable **load factor**, collisions are rare.

```
Load Factor = n / m
where n = number of elements, m = number of buckets

Python dict maintains load factor ≈ 0.66
→ Average bucket has < 1 element
→ Lookups are effectively O(1)
```

---

## Load Factor and Resizing

### Load Factor

```
Load Factor α = n / m

α < 0.5  → Wasting space
α ≈ 0.7  → Good balance (Python uses ~0.66)
α > 1.0  → Many collisions (for chaining)
```

### Automatic Resizing

When load factor exceeds threshold:

1. Create new array with 2× size
2. Rehash all existing keys
3. Insert into new buckets

```python
def _resize(self):
    """Double the size and rehash all elements."""
    old_buckets = self.buckets
    self.size *= 2
    self.buckets = [[] for _ in range(self.size)]
    self.count = 0

    for bucket in old_buckets:
        for key, value in bucket:
            self.put(key, value)  # Rehash with new size
```

**Amortized O(1)**: Resizing is O(n), but happens rarely enough that average insert is still O(1).

---

## Python dict Internals (Interview Knowledge)

### Key Facts to Know

1. **Implementation**: Open addressing with pseudo-random probing
2. **Load factor**: ~66% before resize
3. **Growth**: 2× or 4× when resizing
4. **Ordering**: Insertion order preserved (Python 3.7+)
5. **Space**: ~3× memory of equivalent list of tuples

```python
# Memory comparison
import sys

d = {i: i for i in range(1000)}
l = [(i, i) for i in range(1000)]

sys.getsizeof(d)  # ~36,960 bytes
sys.getsizeof(l)  # ~9,024 bytes (but lookup is O(n))
```

---

## Template: Basic HashMap Operations

```python
# Creating and using dictionaries

# Initialize
d = {}                      # Empty dict
d = {"a": 1, "b": 2}        # With initial values
d = dict.fromkeys([1,2,3])  # Keys with None values

# Insert/Update
d["key"] = value            # O(1)

# Lookup
value = d["key"]            # O(1), raises KeyError if missing
value = d.get("key")        # O(1), returns None if missing
value = d.get("key", 0)     # O(1), returns default if missing

# Check existence
if "key" in d:              # O(1)
    pass

# Delete
del d["key"]                # O(1), raises KeyError if missing
value = d.pop("key")        # O(1), returns value
value = d.pop("key", None)  # O(1), returns default if missing

# Iteration (all O(n))
for key in d:
    pass
for value in d.values():
    pass
for key, value in d.items():
    pass
```

---

## Template: defaultdict and Counter

```python
from collections import defaultdict, Counter

# defaultdict - auto-initializes missing keys
freq = defaultdict(int)     # Missing keys default to 0
freq["a"] += 1              # No KeyError!

graph = defaultdict(list)   # Missing keys default to []
graph["a"].append("b")      # No KeyError!

# Counter - specialized for counting
nums = [1, 2, 2, 3, 3, 3]
count = Counter(nums)       # Counter({3: 3, 2: 2, 1: 1})

# Counter operations
count.most_common(2)        # [(3, 3), (2, 2)]
count["new_key"]            # Returns 0, not KeyError
count.update([1, 1, 1])     # Add more counts
count.total()               # Sum of all counts (Python 3.10+)
```

---

## Template: setdefault Pattern

```python
# setdefault: get value or set default if missing
# Returns the value (existing or newly set)

# Without setdefault
if key not in d:
    d[key] = []
d[key].append(value)

# With setdefault (cleaner)
d.setdefault(key, []).append(value)

# Example: Group words by first letter
words = ["apple", "banana", "cherry", "apricot", "blueberry"]
groups = {}

for word in words:
    groups.setdefault(word[0], []).append(word)

# Result: {'a': ['apple', 'apricot'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}
```

---

## Edge Cases

```python
# Empty dict
d = {}
len(d)       # 0
"key" in d   # False
d.get("key") # None

# None as value vs missing key
d = {"key": None}
d.get("key")        # None
d.get("missing")    # None  <- Same result!
"key" in d          # True  <- Use this to distinguish

# Mutable default values (gotcha!)
def bad_function(d={}):  # WRONG: same dict reused
    d["count"] = d.get("count", 0) + 1
    return d

def good_function(d=None):  # RIGHT: create new each time
    if d is None:
        d = {}
    d["count"] = d.get("count", 0) + 1
    return d
```

---

## Complexity Summary

| Operation | dict | set | list (for comparison) |
|-----------|------|-----|----------------------|
| Insert | O(1) avg | O(1) avg | O(1) append, O(n) insert |
| Lookup | O(1) avg | O(1) avg | O(n) |
| Delete | O(1) avg | O(1) avg | O(n) |
| Space | O(n) | O(n) | O(n) |

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Design HashMap | Easy | Chaining implementation |
| 2 | Design HashSet | Easy | Set implementation |
| 3 | Contains Duplicate | Easy | Set for uniqueness |
| 4 | Jewels and Stones | Easy | Set lookup |
| 5 | First Unique Character | Easy | Frequency counting |

---

## Key Takeaways

1. **Hash tables give O(1) average** for insert, lookup, delete
2. **Collisions are handled** via chaining or open addressing
3. **Load factor matters** - Python maintains ~0.66
4. **Only immutable types** can be dict keys (hashable requirement)
5. **Use defaultdict/Counter** for cleaner frequency counting
6. **Space-time trade-off**: Hash tables use more memory for faster access

---

## Next: [02-two-sum-pattern.md](./02-two-sum-pattern.md)

Learn the classic two-sum pattern that appears in countless interview problems.
