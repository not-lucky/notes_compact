# Bisect Module

> **Prerequisites:** Understanding of binary search

## Building Intuition

### Why Does bisect Exist?

Binary search is fundamental but error-prone. The off-by-one errors, the "should I use `<=` or `<`" decisions, the "left or right?" confusion - these cause bugs even for experienced programmers. `bisect` handles these edge cases correctly, every time.

**The core insight**: Most binary search problems reduce to "find where this value belongs in a sorted list." That's exactly what `bisect` does.

### The Key Mental Model

Imagine a sorted list as a number line with positions:

```
Values:    [1, 3, 5, 5, 5, 7, 9]
Positions:  0  1  2  3  4  5  6  7
                 ↑        ↑
            bisect_left(5)=2  bisect_right(5)=5
```

- **bisect_left(x)**: "Where would x go if we want it BEFORE any equal elements?"
- **bisect_right(x)**: "Where would x go if we want it AFTER any equal elements?"

### Why Two Functions?

They answer different questions:

```python
arr = [1, 3, 5, 5, 5, 7, 9]

# "How many elements are < 5?"
bisect.bisect_left(arr, 5)   # 2 (elements 1, 3)

# "How many elements are <= 5?"
bisect.bisect_right(arr, 5)  # 5 (elements 1, 3, 5, 5, 5)

# "How many 5s are there?"
bisect.bisect_right(arr, 5) - bisect.bisect_left(arr, 5)  # 3
```

### Visual Trace: What bisect Actually Does

```
bisect_left([1, 3, 5, 7, 9], 4):

Step 1: lo=0, hi=5, mid=2, arr[2]=5
        4 < 5, so hi = 2

Step 2: lo=0, hi=2, mid=1, arr[1]=3
        4 > 3, so lo = 2

Step 3: lo=2, hi=2, lo >= hi, return 2

Result: 2 (4 would be inserted between 3 and 5)
```

### insort: Insert + Sort in One Step

`insort` combines finding the position and inserting:

```python
arr = [1, 3, 5, 7]
bisect.insort(arr, 4)
# arr is now [1, 3, 4, 5, 7]
```

**But note**: The insertion itself is O(n) because it shifts elements. The binary search is O(log n), but the total is O(n). For true O(log n) insertion, use `sortedcontainers.SortedList`.

## When NOT to Use

### Don't use bisect when:
- **Data isn't sorted**: bisect assumes sorted input. Using it on unsorted data gives garbage results (silently!)
- **You need O(log n) insertion**: `insort` is O(n) due to list shifting
- **You're searching once**: A simple `in` check or linear scan may be clearer for one-time lookups
- **The list is tiny**: Binary search has overhead; for 10 elements, linear is fine

### Use different approaches when:
- **You need frequent insertions + lookups**: Use `sortedcontainers.SortedList` or a balanced tree
- **You're finding min/max dynamically**: Use a heap
- **Data arrives unsorted**: Sort first, or use a self-balancing structure

### Common mistakes:
```python
# WRONG: Forgetting to check bounds
arr = [1, 3, 5, 7]
i = bisect.bisect_left(arr, 10)
# i = 4, but arr[4] raises IndexError!
# Always check: if i < len(arr) and arr[i] == target

# WRONG: Using on unsorted list
arr = [5, 1, 3, 7]  # Not sorted!
bisect.bisect_left(arr, 4)  # Returns 2, but that's meaningless

# WRONG: Confusing bisect_left and bisect_right for existence check
arr = [1, 3, 5, 7]
i = bisect.bisect_right(arr, 5)  # Returns 3
# arr[3] is 7, not 5! Use bisect_left for "find element"
```

---

## Interview Context

The `bisect` module provides binary search utilities for maintaining sorted lists. It's useful for:

- **Finding insertion points**: Where to insert to keep sorted
- **Binary search**: Find elements or boundaries
- **Sorted containers**: Maintain sorted order with inserts
- **Range queries**: Count elements in a range

---

## Core Functions

```python
import bisect

arr = [1, 3, 5, 7, 9, 11]

# bisect_left: Find leftmost insertion point (before existing equal elements)
bisect.bisect_left(arr, 5)   # 2 (index where 5 is)
bisect.bisect_left(arr, 6)   # 3 (where 6 would go)
bisect.bisect_left(arr, 0)   # 0 (before all elements)
bisect.bisect_left(arr, 12)  # 6 (after all elements)

# bisect_right (same as bisect): Find rightmost insertion point
bisect.bisect_right(arr, 5)  # 3 (after existing 5)
bisect.bisect(arr, 5)        # 3 (alias for bisect_right)

# insort_left: Insert and maintain sorted order
arr = [1, 3, 5, 7]
bisect.insort_left(arr, 4)   # arr = [1, 3, 4, 5, 7]

# insort_right: Insert after existing equal elements
arr = [1, 3, 5, 5, 7]
bisect.insort_right(arr, 5)  # arr = [1, 3, 5, 5, 5, 7]
```

---

## bisect_left vs bisect_right

```python
import bisect

arr = [1, 3, 5, 5, 5, 7, 9]
#      0  1  2  3  4  5  6

# For existing element 5:
bisect.bisect_left(arr, 5)   # 2 (first 5's index)
bisect.bisect_right(arr, 5)  # 5 (after last 5)

# Useful for:
# - bisect_left: "first occurrence" or "lower bound"
# - bisect_right: "upper bound" or "after last occurrence"

# Count occurrences of 5:
left = bisect.bisect_left(arr, 5)
right = bisect.bisect_right(arr, 5)
count = right - left  # 3

# Check if element exists:
def binary_search(arr, x):
    i = bisect.bisect_left(arr, x)
    return i < len(arr) and arr[i] == x
```

---

## Pattern: Binary Search with Bisect

### Find Element

```python
import bisect

def binary_search(arr: list[int], target: int) -> int:
    """Return index of target, or -1 if not found."""
    i = bisect.bisect_left(arr, target)
    if i < len(arr) and arr[i] == target:
        return i
    return -1

arr = [1, 3, 5, 7, 9]
print(binary_search(arr, 5))   # 2
print(binary_search(arr, 6))   # -1
```

### Find First/Last Occurrence

```python
import bisect

def first_occurrence(arr: list[int], target: int) -> int:
    """Return index of first occurrence, or -1."""
    i = bisect.bisect_left(arr, target)
    if i < len(arr) and arr[i] == target:
        return i
    return -1

def last_occurrence(arr: list[int], target: int) -> int:
    """Return index of last occurrence, or -1."""
    i = bisect.bisect_right(arr, target) - 1
    if i >= 0 and arr[i] == target:
        return i
    return -1

arr = [1, 2, 2, 2, 3, 4]
print(first_occurrence(arr, 2))  # 1
print(last_occurrence(arr, 2))   # 3
```

### Find Floor and Ceiling

```python
import bisect

def floor(arr: list[int], x: int) -> int | None:
    """Largest element <= x."""
    i = bisect.bisect_right(arr, x) - 1
    return arr[i] if i >= 0 else None

def ceiling(arr: list[int], x: int) -> int | None:
    """Smallest element >= x."""
    i = bisect.bisect_left(arr, x)
    return arr[i] if i < len(arr) else None

arr = [1, 3, 5, 7, 9]
print(floor(arr, 6))    # 5
print(ceiling(arr, 6))  # 7
print(floor(arr, 5))    # 5
print(ceiling(arr, 5))  # 5
```

---

## Pattern: Count Elements in Range

```python
import bisect

def count_in_range(arr: list[int], low: int, high: int) -> int:
    """Count elements in [low, high]."""
    left = bisect.bisect_left(arr, low)
    right = bisect.bisect_right(arr, high)
    return right - left

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(count_in_range(arr, 3, 7))  # 5 (elements 3,4,5,6,7)
print(count_in_range(arr, 5, 5))  # 1 (just 5)
```

---

## Pattern: Maintain Sorted List

```python
import bisect

class SortedList:
    """Simple sorted list using bisect."""

    def __init__(self):
        self.data = []

    def add(self, x: int) -> None:
        """Add element maintaining sorted order. O(n)"""
        bisect.insort(self.data, x)

    def remove(self, x: int) -> bool:
        """Remove first occurrence of x. O(n)"""
        i = bisect.bisect_left(self.data, x)
        if i < len(self.data) and self.data[i] == x:
            self.data.pop(i)
            return True
        return False

    def __contains__(self, x: int) -> bool:
        """Check if x exists. O(log n)"""
        i = bisect.bisect_left(self.data, x)
        return i < len(self.data) and self.data[i] == x

    def rank(self, x: int) -> int:
        """Count elements < x. O(log n)"""
        return bisect.bisect_left(self.data, x)


# For production: use sortedcontainers.SortedList instead
```

---

## Pattern: H-Index Problem

```python
import bisect

def h_index(citations: list[int]) -> int:
    """
    Find h-index: max h where h papers have >= h citations.

    Time: O(n log n) for sort + O(log n) for binary search
    """
    citations.sort()
    n = len(citations)

    # Binary search for the h-index
    left, right = 0, n

    while left < right:
        mid = (left + right + 1) // 2
        # Count papers with >= mid citations
        # Using bisect_left to find first paper with >= mid
        count = n - bisect.bisect_left(citations, mid)
        if count >= mid:
            left = mid
        else:
            right = mid - 1

    return left


# Test
print(h_index([3, 0, 6, 1, 5]))  # 3
```

---

## Pattern: Time-Based Key-Value Store

```python
import bisect

class TimeMap:
    """
    Store (key, value) pairs with timestamps.
    Get returns value at largest timestamp <= given timestamp.
    """

    def __init__(self):
        self.store = {}  # key -> (list of timestamps, list of values)

    def set(self, key: str, value: str, timestamp: int) -> None:
        """O(1) assuming timestamps are increasing."""
        if key not in self.store:
            self.store[key] = ([], [])
        self.store[key][0].append(timestamp)
        self.store[key][1].append(value)

    def get(self, key: str, timestamp: int) -> str:
        """O(log n) using binary search."""
        if key not in self.store:
            return ""

        times, values = self.store[key]
        i = bisect.bisect_right(times, timestamp) - 1

        if i < 0:
            return ""
        return values[i]


# Test
tm = TimeMap()
tm.set("foo", "bar", 1)
tm.set("foo", "bar2", 4)
print(tm.get("foo", 1))   # "bar"
print(tm.get("foo", 3))   # "bar" (largest timestamp <= 3 is 1)
print(tm.get("foo", 4))   # "bar2"
print(tm.get("foo", 5))   # "bar2"
```

---

## Pattern: Search Insert Position (LeetCode 35)

```python
import bisect

def search_insert(nums: list[int], target: int) -> int:
    """
    Find index where target should be inserted.

    Equivalent to: bisect.bisect_left(nums, target)
    """
    return bisect.bisect_left(nums, target)

# Test
print(search_insert([1, 3, 5, 6], 5))  # 2
print(search_insert([1, 3, 5, 6], 2))  # 1
print(search_insert([1, 3, 5, 6], 7))  # 4
```

---

## Using Key Function (Python 3.10+)

```python
import bisect

# Before Python 3.10: transform the list
data = [(1, 'a'), (3, 'b'), (5, 'c')]
keys = [x[0] for x in data]
i = bisect.bisect_left(keys, 3)

# Python 3.10+: use key parameter
i = bisect.bisect_left(data, 3, key=lambda x: x[0])
```

### Workaround for Older Python

```python
import bisect

class KeyWrapper:
    """Wrapper to use key function with bisect."""
    def __init__(self, items, key):
        self.items = items
        self.key = key

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        return self.key(self.items[i])


# Usage
data = [(1, 'a'), (3, 'b'), (5, 'c')]
keys = KeyWrapper(data, key=lambda x: x[0])
i = bisect.bisect_left(keys, 3)  # Works!
```

---

## Complexity Summary

| Operation | Time | Notes |
|-----------|------|-------|
| bisect_left | O(log n) | Find insertion point |
| bisect_right | O(log n) | Find insertion point (after equals) |
| insort | O(n) | Insert + shift elements |

**Note**: While finding the position is O(log n), inserting into a list is O(n) due to shifting. For true O(log n) insertion, use `sortedcontainers.SortedList`.

---

## sortedcontainers (Third-Party)

For interviews, mention that `sortedcontainers` provides O(log n) for all operations:

```python
from sortedcontainers import SortedList

sl = SortedList([5, 1, 3])
print(sl)  # SortedList([1, 3, 5])

sl.add(2)           # O(log n)
sl.remove(3)        # O(log n)
print(sl.bisect_left(2))  # O(log n)

# More methods
print(sl[0])        # Smallest: 1
print(sl[-1])       # Largest: 5
print(sl[1:3])      # Slicing works
```

---

## Common Mistakes

1. **Off-by-one errors**: bisect_left vs bisect_right
2. **Forgetting insort is O(n)**: List insertion is O(n)
3. **Unsorted input**: Bisect assumes sorted array
4. **Index bounds**: Check `i < len(arr)` after bisect

---

## Practice Problems

| # | Problem | Concept |
|---|---------|---------|
| 1 | Search Insert Position | bisect_left |
| 2 | Find First and Last Position | bisect_left + bisect_right |
| 3 | Time Based Key-Value Store | bisect_right for floor |
| 4 | Count of Smaller Numbers | bisect + update |
| 5 | Russian Doll Envelopes | LIS with bisect |
| 6 | H-Index II | bisect on sorted array |

---

## Related Sections

- [Heapq Module](./02-heapq-module.md) - Alternative for dynamic data
- [Binary Search](../10-binary-search/README.md) - Core concept
