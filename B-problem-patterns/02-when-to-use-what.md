# When to Use What: Data Structure & Algorithm Selection

> **Prerequisites:** [01-pattern-flowchart.md](./01-pattern-flowchart.md)

This guide helps you choose the right data structure and algorithm based on the operations you need to perform and the constraints you're given.

---

## Building Intuition

### Why Data Structure Selection Matters

Every data structure is a trade-off. There's no "best" structure—only the best one for your specific operations. The key insight: **what you do most frequently should be fastest**.

Think of it like choosing a vehicle:

- Need to carry 10 people? → Bus (slow but high capacity)
- Need to go fast with one person? → Sports car
- Need to go off-road? → Truck

Similarly:

- Need frequent lookups by key? → HashMap (O(1) lookup)
- Need to maintain sorted order with insertions? → TreeMap (O(log n) operations)
- Need to get min/max repeatedly? → Heap (O(1) peek, O(log n) operations)

### The Core Trade-offs to Understand

**Time vs Space**: HashMaps give O(1) lookup but consume memory. If you're memory-constrained, you might use binary search on a sorted array instead.

**Preprocessing vs Query**: Prefix sums cost O(n) to build but give O(1) range queries. Worth it if you have many queries; wasteful for one query.

**Static vs Dynamic**: Arrays are great when size is fixed. When you need frequent insertions/deletions, consider linked structures or trees.

### Mental Model: The Operations Checklist

Before choosing a data structure, list your operations:

1. What's the most frequent operation?
2. What's the second most frequent?
3. What operations are rare but still needed?

Then pick the structure that optimizes the frequent operations, even if rare operations are slower.

---

## When NOT to Use This Selection Guide

### Avoid Over-Optimization

1. **For small n (n < 100)**: Constants matter more than asymptotic complexity. A simple array with linear search might beat a HashMap due to cache locality.

2. **When the guide suggests complexity you don't need**: If n ≤ 1000 and you're allowed O(n²), don't spend time implementing a heap when a simple nested loop works.

3. **When problem structure provides natural optimizations**: Sometimes the problem constraints give you shortcuts. "Values are 1 to n" enables cyclic sort without needing any fancy structure.

### Common Selection Mistakes

- **HashMap for everything**: HashMaps are great but have overhead. For 5 elements, an array is faster.
- **Choosing based on familiarity**: Don't pick a heap because you know heaps—pick it because you need O(1) min/max access.
- **Ignoring built-in operations**: Python's `in` on lists is O(n), on sets is O(1). Know your language's guarantees.

---

## Data Structure Selection

### Quick Decision Matrix

| Need to...            | Best Choice        | Time Complexity                  | Notes                             |
| --------------------- | ------------------ | -------------------------------- | --------------------------------- |
| Access by index       | Array/List         | O(1)                             | Use when order matters            |
| Search by value       | HashSet            | O(1) avg                         | Unordered, no duplicates          |
| Search with count     | HashMap            | O(1) avg                         | Key-value pairs                   |
| Maintain sorted order | TreeMap/SortedList | O(log n)                         | Range queries possible            |
| Get min/max quickly   | Heap               | O(1) get, O(log n) insert/remove | Use for K-th element problems     |
| FIFO order            | Queue              | O(1) both ends                   | BFS, level-order                  |
| LIFO order            | Stack              | O(1) push/pop                    | Parentheses, recursion simulation |
| Both ends access      | Deque              | O(1) both ends                   | Sliding window max/min            |
| Range operations      | Prefix Sum         | O(1) query, O(n) build           | Sum queries after preprocessing   |
| Fast union/find       | Union-Find         | O(α(n)) ≈ O(1)                   | Connected components              |
| Prefix matching       | Trie               | O(L) where L = length            | Autocomplete, word search         |

---

## When to Use Each Data Structure

### Arrays / Lists

**Use when:**

- Random access by index is needed
- Order of elements matters
- Iterating through all elements
- Memory efficiency is important

**Avoid when:**

- Frequent insertions/deletions in the middle
- Need fast search by value

```python
# Good use case: tracking positions
positions = [0] * n
for i, val in enumerate(nums):
    positions[val] = i
```

### HashMap (dict)

**Use when:**

- Need O(1) lookup by key
- Counting frequencies
- Mapping relationships (parent, next greater, etc.)
- Caching/memoization

**Avoid when:**

- Need to maintain order (use OrderedDict)
- Need to find min/max (use heap)

```python
# Good use case: two sum
seen = {}
for i, num in enumerate(nums):
    if target - num in seen:
        return [seen[target - num], i]
    seen[num] = i
```

### HashSet (set)

**Use when:**

- Need O(1) membership check
- Removing duplicates
- Set operations (intersection, union)

**Avoid when:**

- Need to track counts (use HashMap)
- Need ordered unique elements (use sorted set)

```python
# Good use case: find duplicate
seen = set()
for num in nums:
    if num in seen:
        return num
    seen.add(num)
```

### Heap (heapq)

**Use when:**

- Need quick access to min or max
- Top-K problems
- Merge K sorted streams
- Priority-based processing

**Avoid when:**

- Need access to arbitrary elements
- Need to delete arbitrary elements efficiently

```python
# Good use case: Kth largest
import heapq
# Min heap of size k → root is kth largest
heap = nums[:k]
heapq.heapify(heap)
for num in nums[k:]:
    if num > heap[0]:
        heapq.heapreplace(heap, num)
return heap[0]
```

### Stack

**Use when:**

- Matching pairs (parentheses, tags)
- Tracking "most recent" state
- Monotonic patterns (next greater/smaller)
- Simulating recursion iteratively
- Undo operations

**Avoid when:**

- Need access to elements in the middle

```python
# Good use case: valid parentheses
stack = []
for char in s:
    if char in '([{':
        stack.append(char)
    elif not stack or not matches(stack.pop(), char):
        return False
return len(stack) == 0
```

### Queue / Deque

**Use when:**

- BFS traversal
- Level-order processing
- Sliding window with max/min
- FIFO order matters

```python
# Good use case: BFS
from collections import deque
queue = deque([start])
visited = {start}
while queue:
    node = queue.popleft()
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)
```

### Monotonic Stack / Deque

**Use when:**

- Next/previous greater/smaller element
- Sliding window maximum/minimum
- Histogram problems (largest rectangle)

```python
# Good use case: next greater element
stack = []  # stores indices
result = [-1] * len(nums)
for i, num in enumerate(nums):
    while stack and nums[stack[-1]] < num:
        result[stack.pop()] = num
    stack.append(i)
```

### Union-Find (Disjoint Set)

**Use when:**

- Grouping elements into sets
- Finding connected components
- Detecting cycles in undirected graphs
- Dynamic connectivity queries

```python
# Good use case: number of connected components
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

### Trie (Prefix Tree)

**Use when:**

- Prefix matching / autocomplete
- Word search in matrix
- Longest common prefix
- Word dictionary with wildcard

```python
# Good use case: word prefix check
class Trie:
    def __init__(self):
        self.children = {}
        self.is_word = False

    def insert(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = Trie()
            node = node.children[char]
        node.is_word = True
```

---

## Algorithm Selection by Problem Type

### Searching

| Constraint               | Algorithm                 | Time                  |
| ------------------------ | ------------------------- | --------------------- |
| Unsorted data            | Linear Search             | O(n)                  |
| Sorted array             | Binary Search             | O(log n)              |
| Search in rotated sorted | Modified Binary Search    | O(log n)              |
| Peak/valley finding      | Binary Search             | O(log n)              |
| 2D sorted matrix         | Binary Search / Staircase | O(m + n) or O(log mn) |

### Sorting

| Constraint             | Algorithm                | Time       | Space |
| ---------------------- | ------------------------ | ---------- | ----- |
| General purpose        | Timsort (Python default) | O(n log n) | O(n)  |
| Nearly sorted          | Insertion Sort           | O(n) best  | O(1)  |
| Limited range (0 to k) | Counting Sort            | O(n + k)   | O(k)  |
| K sorted lists         | K-way Merge (heap)       | O(n log k) | O(k)  |

### Graph Traversal

| Need                             | Algorithm             | Time       |
| -------------------------------- | --------------------- | ---------- |
| Shortest path (unweighted)       | BFS                   | O(V + E)   |
| Shortest path (positive weights) | Dijkstra              | O(E log V) |
| Shortest path (negative weights) | Bellman-Ford          | O(V × E)   |
| All paths / exhaustive           | DFS                   | O(V + E)   |
| Topological order                | Kahn's BFS or DFS     | O(V + E)   |
| Cycle detection (directed)       | DFS with colors       | O(V + E)   |
| Cycle detection (undirected)     | Union-Find or DFS     | O(V + E)   |
| Connected components             | DFS/BFS or Union-Find | O(V + E)   |

### Optimization Problems

| Characteristic                      | Approach                | Example                |
| ----------------------------------- | ----------------------- | ---------------------- |
| Overlapping subproblems             | Dynamic Programming     | Fibonacci, coin change |
| Greedy choice works                 | Greedy                  | Activity selection     |
| Minimize maximum / maximize minimum | Binary Search on Answer | Capacity allocation    |
| All possibilities needed            | Backtracking            | N-Queens, permutations |
| Constraints are inequalities        | Two Pointers            | 3Sum                   |

---

## Constraint-Based Selection

The input size (n) is a strong hint for the expected time complexity:

| n             | Expected Complexity | Typical Patterns             |
| ------------- | ------------------- | ---------------------------- |
| n ≤ 10        | O(n!)               | Brute force, permutations    |
| n ≤ 20        | O(2^n)              | Backtracking, bitmask DP     |
| n ≤ 100       | O(n³)               | Floyd-Warshall, 3D DP        |
| n ≤ 1,000     | O(n²)               | 2D DP, nested loops          |
| n ≤ 10,000    | O(n²) or O(n log n) | Careful with O(n²)           |
| n ≤ 100,000   | O(n log n)          | Sorting, heap, binary search |
| n ≤ 1,000,000 | O(n)                | Single pass, hash table      |
| n ≤ 10^9      | O(log n) or O(1)    | Binary search, math          |

---

## Common Trade-offs

### Time vs Space

| More Space      | Less Time           | Example         |
| --------------- | ------------------- | --------------- |
| HashMap         | O(1) lookup         | Two Sum         |
| Memoization     | Avoid recomputation | DP problems     |
| Prefix Sum      | O(1) range query    | Range Sum Query |
| Parent pointers | Faster LCA          | Tree traversal  |

### Preprocessing vs Query

| Approach     | Preprocess     | Query        | When to Use                  |
| ------------ | -------------- | ------------ | ---------------------------- |
| Prefix Sum   | O(n)           | O(1)         | Many range sum queries       |
| Sorting      | O(n log n)     | O(log n)     | Many search queries          |
| Trie         | O(total chars) | O(query len) | Many prefix queries          |
| Sparse Table | O(n log n)     | O(1)         | Many RMQ queries (immutable) |

---

## Decision Examples

### Example 1: "Find if there's a pair that sums to target"

**Constraints:** n = 10^6

Analysis:

- n is large → need O(n) or O(n log n)
- Two approaches:
  - Sort + Two Pointers: O(n log n)
  - HashSet: O(n)

**Choose:** HashSet for single pass O(n)

### Example 2: "Find the median from a stream of numbers"

**Constraints:** Up to 10^5 operations

Analysis:

- Need dynamic insertions
- Need quick access to middle elements
- Sorted list: O(n) insert, O(1) median
- Two heaps: O(log n) insert, O(1) median

**Choose:** Two Heaps (max-heap for lower half, min-heap for upper half)

### Example 3: "Count connected components in graph"

**Constraints:** n = 10^5 nodes, m = 10^5 edges

Analysis:

- Need to group nodes
- Options:
  - DFS/BFS: O(V + E)
  - Union-Find: O(E × α(V)) ≈ O(E)

**Choose:** Either works. Union-Find if need dynamic queries; DFS/BFS if one-time.

### Example 4: "Find K closest points to origin"

**Constraints:** n = 10^5 points, k = 100

Analysis:

- Need K smallest by distance
- Options:
  - Sort all: O(n log n)
  - Max-heap of size k: O(n log k)
  - QuickSelect: O(n) average

**Choose:** Max-heap for guaranteed O(n log k), or QuickSelect for average O(n)

---

## Quick Reference Cards

### Array/String Problems

```
Subarray with constraint?     → Sliding Window
Find pair/triplet?            → Two Pointers (after sort if needed)
Range sum queries?            → Prefix Sum
Need index and value?         → HashMap
Contiguous max sum?           → Kadane's
```

### Linked List Problems

```
Cycle detection?              → Fast/Slow Pointers
Find middle?                  → Fast/Slow Pointers
Reverse?                      → In-Place Reversal
Merge sorted?                 → Two Pointers or Heap
```

### Tree Problems

```
Level by level?               → BFS
Path problems?                → DFS
LCA?                          → DFS with tracking
BST operations?               → Use BST property
Serialize?                    → Preorder or Level-order
```

### Graph Problems

```
Shortest path (unweighted)?   → BFS
Shortest path (weighted)?     → Dijkstra
Cycle detection?              → DFS colors or Union-Find
Topological order?            → Kahn's or DFS
Components?                   → Union-Find or DFS/BFS
```

---

## Next: [03-template-code.md](./03-template-code.md)
