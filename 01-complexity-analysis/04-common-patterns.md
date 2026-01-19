# Common Operation Complexities

> **Prerequisites:** [01-big-o-notation.md](./01-big-o-notation.md)

## Interview Context

Interviewers expect you to know the complexity of basic operations without thinking. When you use a data structure, you should instantly know the cost.

This knowledge helps you:
- Choose the right data structure for a problem
- Spot inefficiencies in your approach
- Optimize by switching data structures

---

## Python Built-in Types

### List (Dynamic Array)

| Operation | Average Case | Worst Case | Notes |
|-----------|--------------|------------|-------|
| Access `a[i]` | O(1) | O(1) | Direct indexing |
| Search `x in a` | O(n) | O(n) | Linear scan |
| Append `a.append(x)` | O(1)* | O(n) | Amortized O(1) |
| Insert at index `a.insert(i, x)` | O(n) | O(n) | Shift elements |
| Delete by index `del a[i]` | O(n) | O(n) | Shift elements |
| Delete by value `a.remove(x)` | O(n) | O(n) | Search + shift |
| Pop last `a.pop()` | O(1) | O(1) | Just decrement size |
| Pop at index `a.pop(i)` | O(n) | O(n) | Shift elements |
| Slice `a[i:j]` | O(j-i) | O(n) | Creates copy |
| Extend `a.extend(b)` | O(len(b)) | O(len(b)) | Append each |
| Sort `a.sort()` | O(n log n) | O(n log n) | Timsort |
| Reverse `a.reverse()` | O(n) | O(n) | In-place swap |
| Copy `a.copy()` | O(n) | O(n) | Shallow copy |
| Length `len(a)` | O(1) | O(1) | Stored value |

```python
# Gotcha: These are O(n), not O(1)!
arr.insert(0, x)     # O(n) - shifts all elements
arr.pop(0)           # O(n) - shifts all elements
x in arr             # O(n) - linear search
```

### String (Immutable)

| Operation | Time | Notes |
|-----------|------|-------|
| Access `s[i]` | O(1) | Direct indexing |
| Search `x in s` | O(n) | Linear scan |
| Concatenate `s + t` | O(n+m) | Creates new string |
| Slice `s[i:j]` | O(j-i) | Creates new string |
| Length `len(s)` | O(1) | Stored value |
| Join `''.join(list)` | O(total length) | Efficient building |
| Replace `s.replace(a, b)` | O(n) | Creates new string |
| Split `s.split()` | O(n) | Creates list of strings |

```python
# Gotcha: String concatenation in a loop is O(n²)!
s = ""
for c in chars:       # n iterations
    s += c            # Each creates new string of growing size
# Total: 1 + 2 + 3 + ... + n = O(n²)

# Better: O(n)
s = "".join(chars)
```

### Dictionary (Hash Map)

| Operation | Average Case | Worst Case | Notes |
|-----------|--------------|------------|-------|
| Get `d[key]` | O(1) | O(n) | Hash collision |
| Set `d[key] = val` | O(1) | O(n) | Hash collision |
| Delete `del d[key]` | O(1) | O(n) | Hash collision |
| Search `key in d` | O(1) | O(n) | Hash collision |
| Keys `d.keys()` | O(1) | O(1) | Returns view |
| Values `d.values()` | O(1) | O(1) | Returns view |
| Items `d.items()` | O(1) | O(1) | Returns view |
| Iteration | O(n) | O(n) | Visit all items |
| Length `len(d)` | O(1) | O(1) | Stored value |
| Copy `d.copy()` | O(n) | O(n) | Shallow copy |

```python
# Gotcha: Iteration over views is O(n)
for key in d.keys():    # O(n) total, not O(1)
    pass

# The O(1) is for creating the view, not iterating
```

### Set (Hash Set)

| Operation | Average Case | Worst Case | Notes |
|-----------|--------------|------------|-------|
| Add `s.add(x)` | O(1) | O(n) | Hash collision |
| Remove `s.remove(x)` | O(1) | O(n) | Hash collision |
| Discard `s.discard(x)` | O(1) | O(n) | No error if missing |
| Search `x in s` | O(1) | O(n) | Hash collision |
| Union `s \| t` | O(len(s)+len(t)) | - | New set |
| Intersection `s & t` | O(min(len(s), len(t))) | - | New set |
| Difference `s - t` | O(len(s)) | - | New set |
| Length `len(s)` | O(1) | O(1) | Stored value |

```python
# Convert list to set for O(1) lookup
arr = [1, 2, 3, 4, 5]
if x in arr:  # O(n)
    pass

s = set(arr)  # O(n) once
if x in s:    # O(1)
    pass
```

### Deque (Double-ended Queue)

| Operation | Time | Notes |
|-----------|------|-------|
| Append right `d.append(x)` | O(1) | |
| Append left `d.appendleft(x)` | O(1) | Unlike list! |
| Pop right `d.pop()` | O(1) | |
| Pop left `d.popleft()` | O(1) | Unlike list! |
| Access `d[i]` | O(n) | Unlike list! |
| Search `x in d` | O(n) | |
| Length `len(d)` | O(1) | |

```python
from collections import deque

# Use deque when you need O(1) operations at both ends
queue = deque()
queue.append(1)      # O(1)
queue.popleft()      # O(1) - vs O(n) for list

# Don't use deque for random access
value = queue[i]     # O(n) - vs O(1) for list
```

### Heap (via heapq)

| Operation | Time | Notes |
|-----------|------|-------|
| Push `heappush(h, x)` | O(log n) | Maintain heap property |
| Pop min `heappop(h)` | O(log n) | Remove and return smallest |
| Peek min `h[0]` | O(1) | Just access |
| Heapify `heapify(arr)` | O(n) | Convert list to heap |
| Push+Pop `heappushpop(h, x)` | O(log n) | More efficient than separate |
| Pop+Push `heapreplace(h, x)` | O(log n) | Pop then push |

```python
import heapq

# Heapify is O(n), not O(n log n)!
arr = [5, 3, 8, 1, 2]
heapq.heapify(arr)  # O(n) - often asked in interviews
```

---

## Data Structure Comparison

### When to Use What

| Need | Best Choice | Alternative |
|------|-------------|-------------|
| O(1) lookup by key | dict | - |
| O(1) membership test | set | frozenset |
| O(1) access by index | list | - |
| O(1) add/remove both ends | deque | - |
| O(log n) min/max | heap | - |
| Sorted data + O(log n) search | sorted list + bisect | - |
| FIFO queue | deque | - |
| LIFO stack | list | - |

### Time Complexity Comparison Table

| Operation | List | Dict/Set | Deque | Heap |
|-----------|------|----------|-------|------|
| Access by index | O(1) | - | O(n) | - |
| Access by key | - | O(1) | - | - |
| Search | O(n) | O(1) | O(n) | O(n) |
| Insert/Delete at end | O(1)* | - | O(1) | O(log n) |
| Insert/Delete at start | O(n) | - | O(1) | - |
| Insert/Delete middle | O(n) | - | O(n) | - |
| Get min/max | O(n) | O(n) | O(n) | O(1)/O(log n) |

---

## Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Python sort (Timsort) | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |
| Bucket sort | O(n+k) | O(n+k) | O(n²) | O(n) | Yes |

*k = range of values*

```python
# Python's built-in sort is almost always the right choice
arr.sort()            # In-place, O(n log n)
sorted_arr = sorted(arr)  # New list, O(n log n)

# With key function - still O(n log n)
arr.sort(key=lambda x: x[0])
```

---

## Tree Operations

### Binary Search Tree (BST)

| Operation | Average | Worst (Unbalanced) |
|-----------|---------|-------------------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Min/Max | O(log n) | O(n) |
| In-order traversal | O(n) | O(n) |

### Balanced BST (AVL, Red-Black)

| Operation | Time |
|-----------|------|
| Search | O(log n) |
| Insert | O(log n) |
| Delete | O(log n) |
| Min/Max | O(log n) |

### Heap (Binary)

| Operation | Time |
|-----------|------|
| Find min/max | O(1) |
| Insert | O(log n) |
| Delete min/max | O(log n) |
| Build heap | O(n) |

---

## Graph Operations

| Operation | Adjacency List | Adjacency Matrix |
|-----------|---------------|------------------|
| Space | O(V + E) | O(V²) |
| Add vertex | O(1) | O(V²) |
| Add edge | O(1) | O(1) |
| Remove edge | O(E) | O(1) |
| Check edge exists | O(V) | O(1) |
| Get neighbors | O(degree) | O(V) |
| BFS/DFS | O(V + E) | O(V²) |

*V = vertices, E = edges*

```python
# Adjacency list - preferred for sparse graphs
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A'],
    'D': ['B']
}

# Adjacency matrix - better for dense graphs or frequent edge checks
matrix = [
    [0, 1, 1, 0],  # A -> B, C
    [1, 0, 0, 1],  # B -> A, D
    [1, 0, 0, 0],  # C -> A
    [0, 1, 0, 0]   # D -> B
]
```

---

## Interview Quick Reference Card

### Must-Know Complexities

```
Array/List:
  Access:   O(1)
  Search:   O(n)
  Insert:   O(n)
  Append:   O(1)*

Hash Table:
  All ops:  O(1) average

Heap:
  Find min: O(1)
  Insert:   O(log n)
  Delete:   O(log n)

Balanced BST:
  All ops:  O(log n)

Sorting:
  Best:     O(n log n)
```

### Red Flags in Your Solution

| If you're doing... | Watch out for... |
|-------------------|------------------|
| `x in list` in a loop | O(n²) total |
| `list.insert(0, x)` | O(n) each |
| `string += char` in a loop | O(n²) total |
| Nested loops | O(n²) or worse |
| Recursion without memoization | Possibly exponential |

---

## Practice Problems

| # | Problem | Difficulty | Focus |
|---|---------|------------|-------|
| 1 | Choose best data structure for scenario | Easy | Data structure selection |
| 2 | Identify hidden O(n) operations | Easy | List/string gotchas |
| 3 | Optimize using hash table | Medium | Trade space for time |
| 4 | Compare adjacency list vs matrix | Medium | Graph representation |
| 5 | Analyze algorithm using multiple data structures | Medium | Combined analysis |

---

## Key Takeaways

1. **Hash tables give O(1) average** for lookup, insert, delete
2. **Lists are O(n) for insert/delete** except at the end
3. **Heaps are O(log n) for insert/delete**, O(1) for peek
4. **Deques are O(1) at both ends**, but O(n) for random access
5. **String concatenation in loops is O(n²)** - use join instead
6. **`x in list` is O(n)** - convert to set for O(1)
7. **Heapify is O(n)**, not O(n log n)

---

## Next: [05-interview-tips.md](./05-interview-tips.md)

How to effectively communicate complexity analysis during your interview.
