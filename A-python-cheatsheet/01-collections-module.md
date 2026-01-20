# Collections Module

> **Prerequisites:** Basic Python knowledge

## Interview Context

The `collections` module provides specialized container datatypes that are more efficient and convenient than built-in containers. Knowing these can save significant time in interviews:

- **Counter**: Frequency counting in one line
- **defaultdict**: No KeyError, cleaner graph code
- **deque**: O(1) operations at both ends
- **OrderedDict**: LRU cache building block

---

## Counter

A dictionary subclass for counting hashable objects.

### Basic Usage

```python
from collections import Counter

# Count elements
counter = Counter("abracadabra")
print(counter)  # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

# Count from list
nums = [1, 2, 2, 3, 3, 3]
count = Counter(nums)
print(count)  # Counter({3: 3, 2: 2, 1: 1})

# Access count (returns 0 for missing, not KeyError)
print(count[3])   # 3
print(count[99])  # 0 (not KeyError!)
```

### Most Common Operations

```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
count = Counter(words)

# Get k most common
print(count.most_common(2))  # [('apple', 3), ('banana', 2)]

# Get all elements (with repetition)
print(list(count.elements()))  # ['apple', 'apple', 'apple', 'banana', 'banana', 'cherry']

# Update counts
count.update(["apple", "date"])
print(count["apple"])  # 4

# Subtract counts
count.subtract(["apple", "apple"])
print(count["apple"])  # 2

# Total count
print(count.total())  # 6 (Python 3.10+)
print(sum(count.values()))  # Works in all versions
```

### Counter Arithmetic

```python
from collections import Counter

a = Counter("aaabbc")
b = Counter("abbccc")

# Addition
print(a + b)  # Counter({'c': 4, 'a': 3, 'b': 4})

# Subtraction (keeps only positive counts)
print(a - b)  # Counter({'a': 2})

# Intersection (min of each)
print(a & b)  # Counter({'a': 1, 'b': 2, 'c': 1})

# Union (max of each)
print(a | b)  # Counter({'a': 3, 'b': 2, 'c': 3})
```

### Interview Patterns with Counter

```python
from collections import Counter

# 1. Check anagrams
def is_anagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)

# 2. Top K frequent elements
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    return [x for x, _ in Counter(nums).most_common(k)]

# 3. Check if one string can be formed from another
def can_construct(target: str, source: str) -> bool:
    return Counter(target) <= Counter(source)

# 4. Find first unique character
def first_uniq_char(s: str) -> int:
    count = Counter(s)
    for i, c in enumerate(s):
        if count[c] == 1:
            return i
    return -1
```

---

## defaultdict

A dictionary that provides a default value for missing keys.

### Basic Usage

```python
from collections import defaultdict

# With list as default factory
graph = defaultdict(list)
graph["a"].append("b")  # No need to check if "a" exists
graph["a"].append("c")
print(graph)  # defaultdict(<class 'list'>, {'a': ['b', 'c']})

# With int as default factory (defaults to 0)
count = defaultdict(int)
for char in "abracadabra":
    count[char] += 1
print(count)  # defaultdict(<class 'int'>, {'a': 5, 'b': 2, ...})

# With set as default factory
index = defaultdict(set)
for i, word in enumerate(["hello", "world", "hello"]):
    index[word].add(i)
print(index)  # defaultdict(<class 'set'>, {'hello': {0, 2}, 'world': {1}})
```

### Custom Default Factory

```python
from collections import defaultdict

# Lambda for custom default
counter = defaultdict(lambda: 10)
print(counter["missing"])  # 10

# Nested defaultdict (for 2D dictionaries)
def nested_dict():
    return defaultdict(int)

matrix = defaultdict(nested_dict)
matrix[0][1] = 5
matrix[2][3] = 10
print(matrix[0][1])  # 5
print(matrix[5][5])  # 0 (default)
```

### Interview Patterns with defaultdict

```python
from collections import defaultdict

# 1. Build adjacency list (most common use)
def build_graph(edges: list[tuple[int, int]]) -> dict:
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)  # Undirected
    return graph

# 2. Group anagrams
def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())

# 3. Build index
def build_word_index(words: list[str]) -> dict:
    index = defaultdict(list)
    for i, word in enumerate(words):
        index[word].append(i)
    return index
```

---

## deque (Double-Ended Queue)

A list-like container with fast O(1) appends and pops from both ends.

### Basic Usage

```python
from collections import deque

# Create deque
dq = deque([1, 2, 3])
dq = deque()  # Empty
dq = deque(maxlen=5)  # Bounded (auto-evicts old items)

# Operations at both ends
dq.append(4)       # Add right: [1, 2, 3, 4]
dq.appendleft(0)   # Add left: [0, 1, 2, 3, 4]
dq.pop()           # Remove right: returns 4
dq.popleft()       # Remove left: returns 0

# Extend
dq.extend([5, 6])        # Add multiple right
dq.extendleft([0, -1])   # Add multiple left (reversed!)
```

### Time Complexity

| Operation | list | deque |
|-----------|------|-------|
| append | O(1)* | O(1) |
| appendleft | O(n) | O(1) |
| pop | O(1) | O(1) |
| popleft | O(n) | O(1) |
| access by index | O(1) | O(n) |

*Amortized

### Interview Patterns with deque

```python
from collections import deque

# 1. BFS (most common use)
def bfs(graph: dict, start: int) -> list[int]:
    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()  # O(1)!
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order

# 2. Sliding window maximum
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq = deque()  # Store indices of candidates
    result = []

    for i, num in enumerate(nums):
        # Remove smaller elements from back
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)

        # Remove elements outside window
        if dq[0] <= i - k:
            dq.popleft()

        # Add to result once window is full
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

# 3. Recent calls counter
class RecentCounter:
    def __init__(self):
        self.requests = deque()

    def ping(self, t: int) -> int:
        self.requests.append(t)
        while self.requests[0] < t - 3000:
            self.requests.popleft()
        return len(self.requests)

# 4. Implement queue using fixed array (circular buffer)
class CircularQueue:
    def __init__(self, k: int):
        self.queue = deque(maxlen=k)

    def enqueue(self, value: int) -> bool:
        if len(self.queue) == self.queue.maxlen:
            return False
        self.queue.append(value)
        return True

    def dequeue(self) -> int:
        return self.queue.popleft() if self.queue else -1
```

### Bounded deque (maxlen)

```python
from collections import deque

# Fixed-size buffer
recent = deque(maxlen=3)
for i in range(5):
    recent.append(i)
    print(list(recent))

# Output:
# [0]
# [0, 1]
# [0, 1, 2]
# [1, 2, 3]  <- 0 was evicted
# [2, 3, 4]  <- 1 was evicted
```

---

## OrderedDict

A dictionary that remembers insertion order (less needed since Python 3.7+).

### Basic Usage

```python
from collections import OrderedDict

od = OrderedDict()
od['a'] = 1
od['b'] = 2
od['c'] = 3

# Move to end
od.move_to_end('a')  # Now order is b, c, a
od.move_to_end('c', last=False)  # Move to beginning

# Pop from end
od.popitem(last=True)   # Removes and returns ('a', 1)
od.popitem(last=False)  # Removes from beginning
```

### LRU Cache with OrderedDict

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

---

## namedtuple

Create simple classes without defining a full class.

```python
from collections import namedtuple

# Define a Point type
Point = namedtuple('Point', ['x', 'y'])

p = Point(3, 4)
print(p.x, p.y)  # 3 4
print(p[0], p[1])  # Also works: 3 4

# Useful for graph problems
Edge = namedtuple('Edge', ['weight', 'src', 'dest'])
edges = [Edge(5, 'a', 'b'), Edge(3, 'b', 'c')]
edges.sort()  # Sorts by weight first
```

---

## Complexity Summary

| Container | Access | Search | Insert | Delete |
|-----------|--------|--------|--------|--------|
| Counter | O(1) | O(1) | O(1) | O(1) |
| defaultdict | O(1) | O(1) | O(1) | O(1) |
| deque (ends) | O(n) | O(n) | O(1) | O(1) |
| OrderedDict | O(1) | O(1) | O(1) | O(1) |

---

## When to Use Each

| Scenario | Container |
|----------|-----------|
| Count frequencies | Counter |
| Build graph | defaultdict(list) |
| BFS queue | deque |
| Sliding window | deque |
| LRU Cache | OrderedDict |
| Group by key | defaultdict(list) |

---

## Practice Problems

| # | Problem | Container |
|---|---------|-----------|
| 1 | Valid Anagram | Counter |
| 2 | Top K Frequent Elements | Counter |
| 3 | Group Anagrams | defaultdict |
| 4 | Sliding Window Maximum | deque |
| 5 | LRU Cache | OrderedDict |
| 6 | Number of Recent Calls | deque |

---

## Related Sections

- [Heapq Module](./02-heapq-module.md) - Priority queues
- [Common Gotchas](./05-common-gotchas.md) - Pitfalls with mutable defaults
