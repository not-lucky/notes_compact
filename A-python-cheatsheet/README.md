# Appendix A: Python Interview Cheatsheet

This appendix covers Python-specific knowledge that gives you an edge in technical interviews. While algorithms are language-agnostic, knowing Python's standard library can help you write cleaner, faster solutions.

## Building Intuition

### Why Learn Python's Standard Library?

The difference between a good solution and a great solution often lies in knowing what tools already exist. Consider this scenario:

**Without standard library knowledge:**

```python
from collections import Counter
from typing import Dict

def count_chars(s: str) -> Dict[str, int]:
    freq: Dict[str, int] = {}
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

def count_chars(s: str) -> Counter[str]:
    return Counter(s)
```

Both solutions work. But the second one:

- Takes 10 seconds to write instead of 60
- Has zero chance of bugs
- Shows the interviewer you know Python
- Lets you focus on the actual algorithm, not boilerplate

### The Mental Model

Think of Python's standard library as a "solved problems" catalog:

| Problem Type                                          | Solved By                  |
| ----------------------------------------------------- | -------------------------- |
| "I need to count things"                              | `Counter`                  |
| "I need a dictionary that auto-initializes"           | `defaultdict`              |
| "I need fast operations at both ends"                 | `deque`                    |
| "I need the k largest/smallest"                       | `heapq.nlargest/nsmallest` |
| "I need to find where an element goes in sorted list" | `bisect`                   |
| "I need all combinations/permutations"                | `itertools`                |

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

| Module        | Primary Use               | Example                     |
| ------------- | ------------------------- | --------------------------- |
| `collections` | Specialized containers    | Counter, deque, defaultdict |
| `heapq`       | Priority queue operations | Top-K problems              |
| `bisect`      | Binary search utilities   | Sorted insertions           |
| `itertools`   | Combinatorial iterators   | Permutations, combinations  |

---

## Appendix Contents

| #   | Topic                                            | Key Concepts                             |
| --- | ------------------------------------------------ | ---------------------------------------- |
| 01  | [Collections Module](./01-collections-module.md) | Counter, defaultdict, deque, OrderedDict |
| 02  | [Heapq Module](./02-heapq-module.md)             | Min/max heap, top-K patterns             |
| 03  | [Bisect Module](./03-bisect-module.md)           | Binary search, sorted containers         |
| 04  | [Itertools Module](./04-itertools-module.md)     | Permutations, combinations, product      |
| 05  | [Common Gotchas](./05-common-gotchas.md)         | Python-specific pitfalls                 |

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
from typing import List

graph: defaultdict[str, List[str]] = defaultdict(list)
graph["a"].append("b")  # No KeyError!

# Useful for counting without Counter:
freq: defaultdict[str, int] = defaultdict(int)
freq["a"] += 1
```

### Double-Ended Queue

```python
from collections import deque

dq = deque([1, 2, 3])
dq.appendleft(0)  # O(1): [0, 1, 2, 3]
dq.pop()          # O(1): returns 3, dq is now [0, 1, 2]
# Note: dq[k] (indexing) takes O(n) time, except for dq[0] and dq[-1] which are O(1)
```

### Heap Operations

```python
import heapq

heap = [3, 1, 4, 1, 5]
heapq.heapify(heap)            # O(n): convert to min-heap in-place
heapq.heappush(heap, 2)        # O(log n): add element
smallest = heapq.heappop(heap) # O(log n): remove and return min
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

| Operation       | list   | dict/set | deque |
| --------------- | ------ | -------- | ----- |
| Access by index | O(1)   | N/A      | O(n)  |
| Search (`in`)   | O(n)   | O(1)     | O(n)  |
| Insert at end   | O(1)*  | O(1)     | O(1)  |
| Insert at front | O(n)   | N/A      | O(1)  |
| Delete by value | O(n)   | O(1)     | O(n)  |
| Min/Max         | O(n)   | O(n)     | O(n)  |
| len()           | O(1)   | O(1)     | O(1)  |

\*Amortized O(1)

---

## Common Patterns

### 1. Graph with Adjacency List

```python
from collections import defaultdict
from typing import List, Tuple

edges = [("A", "B"), ("A", "C"), ("B", "D")]
graph: defaultdict[str, List[str]] = defaultdict(list)

for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # Omit for directed graphs
```

### 2. BFS Template

```python
from collections import deque
from typing import Dict, List, Set

def bfs(start_node: str, graph: Dict[str, List[str]]) -> None:
    queue = deque([start_node])
    visited: Set[str] = {start_node}

    while queue:
        current_node = queue.popleft()

        # Process current_node here

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### 3. Top-K with Heap

```python
import heapq
from typing import List

def top_k(nums: List[int], k: int) -> List[int]:
    """Returns the k largest elements in O(n + k log n) time."""
    return heapq.nlargest(k, nums)
    # Alternatively, use Counter(nums).most_common(k) for frequencies
```

### 4. Sliding Window with Deque

```python
from collections import deque
from typing import List

def max_sliding_window(nums: List[int], k: int) -> List[int]:
    dq: deque[int] = deque()  # Stores indices, not values
    result: List[int] = []

    for i, num in enumerate(nums):
        # 1. Remove elements out of window
        if dq and dq[0] <= i - k:
            dq.popleft()

        # 2. Maintain monotonic property (decreasing order)
        while dq and nums[dq[-1]] < num:
            dq.pop()

        # 3. Add current element's index
        dq.append(i)

        # 4. Add window's max to result once window size is at least k
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

---

## Interview Tips

1. **Know the stdlib**: `collections`, `heapq`, `bisect` save time and prevent bugs.
2. **Avoid reinventing the wheel**: Use `Counter` instead of manual counting when appropriate.
3. **Watch mutability gotchas**: Never use lists as default arguments in Python functions (`def foo(l=[])`). It evaluates once at definition time.
4. **Articulate complexity continuously**: "I'm using a `deque` here because I need O(1) `popleft` operations."
5. **Beware hidden O(n) operations**: `list.pop(0)`, `in` checks on a list, string concatenations (`s += "a"` in a loop instead of `"a".join()`).
6. **Use `.get()` for safe dict access**: `val = my_dict.get(key, default_value)` prevents `KeyError`.

---

## Python vs Other Languages

| Feature | Python                        | Java            | C++              |
| ------- | ----------------------------- | --------------- | ---------------- |
| HashMap | `dict`                        | `HashMap`       | `unordered_map`  |
| TreeMap | `sortedcontainers.SortedDict` | `TreeMap`       | `map`            |
| Heap    | `heapq` (min only)            | `PriorityQueue` | `priority_queue` |
| Deque   | `collections.deque`           | `ArrayDeque`    | `deque`          |

---

## Start: [01-collections-module.md](./01-collections-module.md)

Begin with the collections module—the most frequently used in interviews.
