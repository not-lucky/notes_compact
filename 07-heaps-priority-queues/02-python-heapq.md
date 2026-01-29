# Python heapq Module

> **Prerequisites:** [01-heap-basics](./01-heap-basics.md)

## Interview Context

Knowing Python's heapq module is essential because:

1. **Standard library**: No need to implement heap from scratch
2. **Interview expectation**: Use library functions for efficiency
3. **Common pitfall**: heapq is min heap only — must handle max heap
4. **Tuple comparison**: Understanding how heapq handles ties matters

Using heapq correctly shows you're a practical Python programmer, not just theoretical.

---

## Building Intuition

**Why Does Python Only Have Min Heap?**

Design simplicity. One heap type means one mental model. Max heap is trivially achieved by negating values—the sorted order inverts:

```
Values:   5   3   8   1   2
Negated: -5  -3  -8  -1  -2

Min of negated = -8 → corresponds to max of original (8)
```

**The Negation Pattern Deeply Explained**

```python
# What you want: max heap that pops largest first
# What heapq does: min heap that pops smallest first

# Solution: Store -x, pop -result
#
# Original values: [5, 3, 8]
# Stored as:       [-5, -3, -8]
# Min of stored:   -8
# Negate result:   8  ← This IS the max!

# Push 10: store -10
# [-10, -5, -3, -8]
# Min = -10 → negate → 10 (correct max)
```

**Why Tuples Work as Priority Queues**

Python compares tuples lexicographically (element by element):

```python
(1, "zebra") < (2, "apple")  # True: 1 < 2, stop comparing
(1, "apple") < (1, "zebra")  # True: 1 == 1, so compare "apple" < "zebra"
(1, 100) < (1, 200)          # True: 1 == 1, so compare 100 < 200
```

So `(priority, data)` naturally sorts by priority first. But there's a trap:

```python
(1, {"a": 1}) < (1, {"b": 2})  # ERROR! Dicts aren't comparable

# Fix: (priority, tiebreaker, data) where tiebreaker is always unique
(1, 0, {"a": 1}) < (1, 1, {"b": 2})  # True: priority tie, 0 < 1, never compares dicts
```

**Mental Model: The Hospital Waiting Room**

Think of heapq as a hospital triage system:

- Lower number = higher priority (more urgent)
- When you call `heappop()`, the most urgent patient (lowest number) leaves
- Ties are broken by arrival order (that's why we use counter)

```python
# (severity, arrival_order, patient)
(1, 0, "heart attack")    # Seen first
(1, 1, "stroke")          # Same severity, but arrived later
(3, 2, "broken finger")   # Seen last
```

**heappushpop vs heapreplace: What's the Difference?**

Both do two operations in one, but the order differs:

```python
# heappushpop: PUSH first, then POP
# Returns min(new_item, current_min)
heap = [2, 3, 5]
heappushpop(heap, 1)  # Push 1, pop min → returns 1 (the item we just pushed!)

# heapreplace: POP first, then PUSH
# Always returns what was the minimum
heap = [2, 3, 5]
heapreplace(heap, 1)  # Pop 2, push 1 → returns 2

# Use heapreplace for "sliding window minimum" patterns
# Use heappushpop for "keep k largest" patterns
```

---

## When NOT to Use heapq

**1. You Need a Max Heap and Code Clarity Matters**

Negation works but clutters code. For complex logic:

```python
# Confusing with negation everywhere
if -heap[0] > threshold:
    result = -heappop(heap)
    heappush(heap, -new_val)

# Consider: wrapper class or different data structure
```

**2. You Need to Update Priorities**

heapq has no decrease-key or increase-key operation:

```python
# Can't do this efficiently:
# "Change task X's priority from 5 to 2"

# Options:
# 1. Lazy deletion: mark old entry invalid, push new entry
# 2. Use sortedcontainers.SortedList instead
# 3. Implement indexed heap yourself
```

**3. You Need Thread Safety**

heapq is not thread-safe. For concurrent access:

```python
# Use queue.PriorityQueue instead
from queue import PriorityQueue
pq = PriorityQueue()  # Thread-safe, but slower
```

**4. You Need K ≈ N Elements**

For large K relative to N, sorting is better:

```python
# K = 1: just use min() or max()
# K = N/2 or more: just sort the array

# heapq.nlargest(k, arr) internally checks this and may sort anyway
```

**5. You Need the Heap to Stay Sorted**

heapq only guarantees heap property, not full sorting:

```python
heap = [1, 3, 2, 7, 4]
heapq.heapify(heap)
print(heap)  # [1, 3, 2, 7, 4] - NOT [1, 2, 3, 4, 7]!

# To get sorted: list(heapq.nsmallest(len(heap), heap))
# Or: [heappop(heap) for _ in range(len(heap))]
```

**Red Flags:**

- "Need to look up or modify specific elements" → Use dict + sorted structure
- "Multiple threads accessing heap" → Use queue.PriorityQueue
- "Need sorted order at all times" → Use sortedcontainers.SortedList
- "K is close to N" → Just sort the array

---

## heapq Basics

Python's heapq module provides heap operations on regular lists.

```python
import heapq

# Create empty heap (just a list)
heap = []

# Push elements
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 4)
heapq.heappush(heap, 1)
heapq.heappush(heap, 5)

print(heap)  # [1, 1, 4, 3, 5] - min heap, not fully sorted

# Pop minimum
min_val = heapq.heappop(heap)  # Returns 1
print(heap)  # [1, 3, 4, 5]

# Peek at minimum (don't pop)
min_val = heap[0]  # 1

# Get length
size = len(heap)  # 4
```

---

## Core Functions

### heappush(heap, item)

```python
import heapq

heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 3)
heapq.heappush(heap, 7)
# heap = [3, 5, 7]

# Time: O(log n)
```

### heappop(heap)

```python
import heapq

heap = [1, 3, 2, 7, 4]
heapq.heapify(heap)

smallest = heapq.heappop(heap)  # 1
# heap = [2, 3, 4, 7]

# Time: O(log n)
# Raises IndexError if heap is empty
```

### heapify(list)

```python
import heapq

arr = [5, 3, 8, 1, 2]
heapq.heapify(arr)  # In-place conversion
# arr = [1, 2, 8, 5, 3]

# Time: O(n) - NOT O(n log n)
```

### heappushpop(heap, item)

Push item, then pop smallest. More efficient than separate push + pop.

```python
import heapq

heap = [1, 3, 5]
result = heapq.heappushpop(heap, 2)
# result = 1, heap = [2, 3, 5]

result = heapq.heappushpop(heap, 0)
# result = 0, heap = [2, 3, 5] (0 pushed then immediately popped)

# Time: O(log n)
```

### heapreplace(heap, item)

Pop smallest, then push item. More efficient than separate pop + push.

```python
import heapq

heap = [1, 3, 5]
result = heapq.heapreplace(heap, 4)
# result = 1, heap = [3, 4, 5]

# Time: O(log n)
# Raises IndexError if heap is empty
```

### nlargest(n, iterable, key=None)

```python
import heapq

nums = [3, 1, 4, 1, 5, 9, 2, 6]

# Get 3 largest
largest = heapq.nlargest(3, nums)
# [9, 6, 5]

# With key function
words = ['apple', 'pie', 'strawberry', 'fig']
longest = heapq.nlargest(2, words, key=len)
# ['strawberry', 'apple']

# Time: O(n log k) where k is n parameter
```

### nsmallest(n, iterable, key=None)

```python
import heapq

nums = [3, 1, 4, 1, 5, 9, 2, 6]

# Get 3 smallest
smallest = heapq.nsmallest(3, nums)
# [1, 1, 2]

# Time: O(n log k) where k is n parameter
```

---

## Max Heap Pattern (CRITICAL)

Python heapq is **min heap only**. For max heap, negate values:

```python
import heapq

# Max heap simulation
max_heap = []

# Push (negate)
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -3)
heapq.heappush(max_heap, -8)
# max_heap = [-8, -3, -5]

# Pop (negate result)
max_val = -heapq.heappop(max_heap)  # 8
# max_heap = [-5, -3]

# Peek (negate)
current_max = -max_heap[0]  # 5
```

**Common Pattern for Max Heap:**

```python
import heapq

def push_max(heap: list, val: int) -> None:
    """Push to max heap."""
    heapq.heappush(heap, -val)

def pop_max(heap: list) -> int:
    """Pop from max heap."""
    return -heapq.heappop(heap)

def peek_max(heap: list) -> int:
    """Peek max heap."""
    return -heap[0]
```

---

## Tuple Comparison (Important!)

heapq compares tuples element by element. First element is primary key.

```python
import heapq

# Priority queue: (priority, item)
pq = []
heapq.heappush(pq, (2, "task B"))
heapq.heappush(pq, (1, "task A"))
heapq.heappush(pq, (3, "task C"))

priority, task = heapq.heappop(pq)
# priority = 1, task = "task A"
```

### Handling Ties

If first elements are equal, Python compares second elements. This can cause errors with non-comparable types:

```python
import heapq

# This will error if priorities tie!
pq = []
heapq.heappush(pq, (1, {"name": "A"}))
heapq.heappush(pq, (1, {"name": "B"}))  # Error: dicts not comparable
```

**Solution: Add unique index as tiebreaker:**

```python
import heapq

class PriorityQueue:
    """Priority queue that handles any item type."""
    def __init__(self):
        self.heap = []
        self.counter = 0  # Unique sequence count

    def push(self, priority: int, item) -> None:
        # (priority, counter, item) - counter breaks ties
        heapq.heappush(self.heap, (priority, self.counter, item))
        self.counter += 1

    def pop(self):
        priority, _, item = heapq.heappop(self.heap)
        return priority, item


pq = PriorityQueue()
pq.push(1, {"name": "A"})
pq.push(1, {"name": "B"})  # Works! Counter breaks tie
priority, item = pq.pop()  # Returns first inserted with priority 1
```

---

## Common Patterns

### Pattern 1: Maintain Sorted Stream

```python
import heapq

def add_to_sorted_stream(heap: list, val: int, k: int) -> list:
    """
    Maintain k smallest elements from stream.

    Time: O(log k) per element
    """
    if len(heap) < k:
        heapq.heappush(heap, -val)  # Max heap of k smallest
    elif val < -heap[0]:  # New val smaller than current max
        heapq.heapreplace(heap, -val)

    return [-x for x in sorted(heap)]  # Return sorted k smallest
```

### Pattern 2: Merge Multiple Sorted Sources

```python
import heapq

def merge_sorted_lists(lists: list[list[int]]) -> list[int]:
    """
    Merge k sorted lists.

    Time: O(n log k) where n is total elements, k is number of lists
    """
    result = []
    # (value, list_index, element_index)
    heap = []

    # Initialize with first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Add next element from same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result
```

### Pattern 3: K Largest with Counter

```python
import heapq
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    Find k most frequent elements.

    Time: O(n log k)
    """
    count = Counter(nums)

    # Min heap of size k: (frequency, num)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

---

## Complexity Summary

| Function     | Time       | Space | Notes                |
| ------------ | ---------- | ----- | -------------------- |
| heappush     | O(log n)   | O(1)  | Add element          |
| heappop      | O(log n)   | O(1)  | Remove minimum       |
| heapify      | O(n)       | O(1)  | Convert list to heap |
| heappushpop  | O(log n)   | O(1)  | Push then pop        |
| heapreplace  | O(log n)   | O(1)  | Pop then push        |
| nlargest(k)  | O(n log k) | O(k)  | K largest elements   |
| nsmallest(k) | O(n log k) | O(k)  | K smallest elements  |
| heap[0]      | O(1)       | O(1)  | Peek minimum         |

---

## When to Use nlargest/nsmallest

| Scenario          | Best Approach       | Time       |
| ----------------- | ------------------- | ---------- |
| K = 1             | min()/max()         | O(n)       |
| K small (< log n) | nlargest/nsmallest  | O(n log k) |
| K ≈ n             | sorted()[:k]        | O(n log n) |
| K large (> n/2)   | sorted() then slice | O(n log n) |

---

## Edge Cases

```python
import heapq

# 1. Empty heap
heap = []
# heappop(heap) raises IndexError

# 2. Single element
heap = [5]
heapq.heappop(heap)  # Returns 5, heap = []

# 3. All same values
heap = [3, 3, 3]
heapq.heapify(heap)  # Still valid: [3, 3, 3]

# 4. Negative numbers
heap = [-5, -3, -8]
heapq.heapify(heap)
heapq.heappop(heap)  # Returns -8 (most negative = smallest)

# 5. Floats work too
heap = [3.14, 2.71, 1.41]
heapq.heapify(heap)
```

---

## Interview Tips

1. **Always import heapq**: `import heapq` not `from heapq import *`
2. **Know it's min heap only**: Max heap needs negation
3. **Use tuples for priority queue**: `(priority, item)` or `(priority, index, item)`
4. **heapify is O(n)**: Not O(n log n) — interviewers test this
5. **Check empty heap**: `if heap:` before `heap[0]` or use try/except
6. **nlargest/nsmallest**: Great for quick solutions, but know the complexity

---

## Practice Problems

| #   | Problem                         | Difficulty | Key Concept            |
| --- | ------------------------------- | ---------- | ---------------------- |
| 1   | Kth Largest Element in a Stream | Easy       | heappush, len check    |
| 2   | Last Stone Weight               | Easy       | Max heap with negation |
| 3   | Top K Frequent Elements         | Medium     | Counter + nlargest     |
| 4   | Merge k Sorted Lists            | Medium     | Tuple comparison       |
| 5   | Find Median from Data Stream    | Hard       | Two heaps              |

---

## Key Takeaways

1. **heapq operates on lists**: `heap = []`, not a special class
2. **Min heap only**: Negate values for max heap behavior
3. **heapify is O(n)**: Build heap from list efficiently
4. **Tuple comparison**: First element is primary key
5. **Add counter for ties**: `(priority, counter, item)` pattern

---

## Next: [03-top-k-pattern.md](./03-top-k-pattern.md)

Learn the Top-K pattern, the most common heap interview pattern.
