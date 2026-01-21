# Appendix A: Python Interview Cheatsheet

This appendix covers Python-specific knowledge that gives you an edge in technical interviews. While algorithms are language-agnostic, knowing Python's standard library can help you write cleaner, faster solutions.

## Building Intuition

### Why Learn Python's Standard Library?

The difference between a good solution and a great solution often lies in knowing what tools already exist. Consider this scenario:

**Without standard library knowledge:**
```python
# Count character frequencies - manual approach
def count_chars(s):
    freq = {}
    for c in s:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1
    return freq
```

**With standard library knowledge:**
```python
from collections import Counter
def count_chars(s):
    return Counter(s)
```

Both solutions work. But the second one:
- Takes 10 seconds to write instead of 60
- Has zero chance of bugs
- Shows the interviewer you know Python
- Lets you focus on the actual algorithm, not boilerplate

### The Mental Model

Think of Python's standard library as a "solved problems" catalog:

| Problem Type | Solved By |
|--------------|-----------|
| "I need to count things" | `Counter` |
| "I need a dictionary that auto-initializes" | `defaultdict` |
| "I need fast operations at both ends" | `deque` |
| "I need the k largest/smallest" | `heapq.nlargest/nsmallest` |
| "I need to find where an element goes in sorted list" | `bisect` |
| "I need all combinations/permutations" | `itertools` |

When you recognize a pattern, reach for the right tool automatically.

## When NOT to Use These Modules

1. **When the interview explicitly asks you to implement the data structure**: If asked to "implement a heap", don't use `heapq` - they want to see you understand the mechanics

2. **When it obscures the core algorithm**: If the interesting part is the algorithm itself, using a one-liner might hide what you understand

3. **When simpler is clearer**: Don't use `Counter` when you only need to check if something exists (use a set)

4. **When learning**: Build things from scratch first to understand the internals, then use the library

5. **When interviewing at companies that want low-level knowledge**: Some roles (systems, embedded) may value seeing you implement fundamentals

## Why Python for Interviews

1. **Concise syntax**: Write less code, fewer bugs
2. **Rich standard library**: Built-in solutions for common patterns
3. **Interview-friendly**: Most FANG companies allow Python
4. **Readable**: Easy for interviewers to follow your logic

---

## Key Modules for Interviews

| Module | Primary Use | Example |
|--------|-------------|---------|
| `collections` | Specialized containers | Counter, deque, defaultdict |
| `heapq` | Priority queue operations | Top-K problems |
| `bisect` | Binary search utilities | Sorted insertions |
| `itertools` | Combinatorial iterators | Permutations, combinations |

---

## Appendix Contents

| # | Topic | Key Concepts |
|---|-------|--------------|
| 01 | [Collections Module](./01-collections-module.md) | Counter, defaultdict, deque, OrderedDict |
| 02 | [Heapq Module](./02-heapq-module.md) | Min/max heap, top-K patterns |
| 03 | [Bisect Module](./03-bisect-module.md) | Binary search, sorted containers |
| 04 | [Itertools Module](./04-itertools-module.md) | Permutations, combinations, product |
| 05 | [Common Gotchas](./05-common-gotchas.md) | Python-specific pitfalls |
| 06 | [Constraint Analysis](./constraint_analysis.md) | $N$ to Complexity mapping |

---

## Quick Reference: One-Liners

### Frequency Counting
```python
from collections import Counter
count = Counter("abracadabra")  # {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}
count.most_common(2)            # [('a', 5), ('b', 2)]
```

### Default Values
```python
from collections import defaultdict
graph = defaultdict(list)
graph["a"].append("b")  # No KeyError!
```

### Double-Ended Queue
```python
from collections import deque
dq = deque([1, 2, 3])
dq.appendleft(0)  # O(1): [0, 1, 2, 3]
dq.pop()          # O(1): returns 3
```

### Heap Operations
```python
import heapq
heap = [3, 1, 4, 1, 5]
heapq.heapify(heap)           # O(n): convert to min-heap
heapq.heappush(heap, 2)       # O(log n): add element
smallest = heapq.heappop(heap) # O(log n): remove min
```

### Binary Search
```python
import bisect
arr = [1, 3, 5, 7, 9]
bisect.bisect_left(arr, 5)   # 2 (index where 5 is)
bisect.bisect_right(arr, 5)  # 3 (index after 5)
bisect.insort(arr, 6)        # arr = [1, 3, 5, 6, 7, 9]
```

### Combinations & Permutations
```python
from itertools import permutations, combinations, product

list(permutations([1, 2, 3], 2))  # [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]
list(combinations([1, 2, 3], 2))   # [(1,2), (1,3), (2,3)]
list(product([0, 1], repeat=3))    # All binary strings of length 3
```

---

## Time Complexity Cheat Sheet

| Operation | list | dict | set | deque |
|-----------|------|------|-----|-------|
| Access by index | O(1) | - | - | O(n) |
| Search | O(n) | O(1) | O(1) | O(n) |
| Insert at end | O(1)* | O(1) | O(1) | O(1) |
| Insert at front | O(n) | - | - | O(1) |
| Delete by value | O(n) | O(1) | O(1) | O(n) |
| Min/Max | O(n) | O(n) | O(n) | O(n) |

*Amortized O(1)

---

## Common Patterns

### 1. Graph with Adjacency List
```python
from collections import defaultdict

graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # For undirected
```

### 2. BFS Template
```python
from collections import deque

def bfs(start):
    queue = deque([start])
    visited = {start}

    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### 3. Top-K with Heap
```python
import heapq

def top_k(nums, k):
    return heapq.nlargest(k, nums)  # Or use Counter.most_common(k)
```

### 4. Sliding Window with Deque
```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()  # Store indices
    result = []

    for i, num in enumerate(nums):
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)

        if dq[0] <= i - k:
            dq.popleft()

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

---

## Interview Tips

1. **Know the stdlib**: `collections`, `heapq`, `bisect` save time
2. **Avoid reinventing**: Use `Counter` instead of manual counting
3. **Watch mutability**: Lists as default args, shallow copies
4. **Mention complexity**: "Using deque for O(1) popleft"
5. **Keep it readable**: Pythonic code is easy to debug

---

## Python vs Other Languages

| Feature | Python | Java | C++ |
|---------|--------|------|-----|
| HashMap | `dict` | `HashMap` | `unordered_map` |
| TreeMap | `sortedcontainers.SortedDict` | `TreeMap` | `map` |
| Heap | `heapq` (min only) | `PriorityQueue` | `priority_queue` |
| Deque | `collections.deque` | `ArrayDeque` | `deque` |

---

## Start: [01-collections-module.md](./01-collections-module.md)

Begin with the collections module—the most frequently used in interviews.
