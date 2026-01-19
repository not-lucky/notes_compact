# Heap Basics

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md), [06-trees/01-tree-basics](../06-trees/01-tree-basics.md)

## Interview Context

Heaps are fundamental because:

1. **Optimal for priority operations**: O(log n) insert/remove, O(1) peek
2. **Foundation for many patterns**: Top-K, merge K sorted, scheduling
3. **Memory efficient**: Stored as array, no pointer overhead
4. **Interview frequency**: Heap understanding is prerequisite for medium/hard problems

Interviewers expect you to know heap properties and operations, even if you use library functions.

---

## Core Concept: What is a Heap?

A **heap** is a complete binary tree stored as an array where each parent satisfies the **heap property** with its children.

### Min Heap vs Max Heap

| Type | Property | Root Contains |
|------|----------|---------------|
| **Min Heap** | Parent ≤ Children | Minimum element |
| **Max Heap** | Parent ≥ Children | Maximum element |

```
Min Heap:                    Max Heap:
      1                           9
     / \                         / \
    3   2                       7   8
   / \                         / \
  7   4                       3   5

Array: [1, 3, 2, 7, 4]       Array: [9, 7, 8, 3, 5]
```

---

## Array Representation

A heap is stored as an array where:
- **Root** is at index 0
- For node at index `i`:
  - **Left child**: `2*i + 1`
  - **Right child**: `2*i + 2`
  - **Parent**: `(i - 1) // 2`

```
Array:  [1,  3,  2,  7,  4]
Index:   0   1   2   3   4

Tree:
         1 (i=0)
        / \
   (i=1) 3   2 (i=2)
        / \
  (i=3) 7   4 (i=4)

Parent of index 3: (3-1)//2 = 1 → value 3 ✓
Left child of index 1: 2*1+1 = 3 → value 7 ✓
Right child of index 1: 2*1+2 = 4 → value 4 ✓
```

---

## Complete Binary Tree Property

A heap is always a **complete binary tree**:
- All levels fully filled except possibly the last
- Last level filled from left to right

This guarantees:
- Height is always O(log n)
- No gaps in array representation
- Efficient memory usage

```
Complete (valid):        Not complete (invalid):
      1                        1
     / \                      / \
    3   2                    3   2
   / \                        \
  7   4                        4
```

---

## Core Operations

### 1. Heapify Up (Bubble Up / Sift Up)

Used after inserting a new element at the end.

```python
def heapify_up(heap: list, index: int) -> None:
    """
    Move element up until heap property is satisfied.
    Used after insertion at the end.

    Time: O(log n) - at most height of tree
    Space: O(1)
    """
    while index > 0:
        parent = (index - 1) // 2
        if heap[index] < heap[parent]:  # Min heap: child < parent
            heap[index], heap[parent] = heap[parent], heap[index]
            index = parent
        else:
            break
```

### 2. Heapify Down (Bubble Down / Sift Down)

Used after removing root or during heap construction.

```python
def heapify_down(heap: list, index: int, size: int) -> None:
    """
    Move element down until heap property is satisfied.
    Used after removing root.

    Time: O(log n)
    Space: O(1)
    """
    while True:
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < size and heap[left] < heap[smallest]:
            smallest = left
        if right < size and heap[right] < heap[smallest]:
            smallest = right

        if smallest != index:
            heap[index], heap[smallest] = heap[smallest], heap[index]
            index = smallest
        else:
            break
```

### 3. Push (Insert)

```python
def heap_push(heap: list, val: int) -> None:
    """
    Insert element into heap.

    Time: O(log n)
    Space: O(1)
    """
    heap.append(val)              # Add to end
    heapify_up(heap, len(heap) - 1)  # Bubble up
```

### 4. Pop (Extract Min/Max)

```python
def heap_pop(heap: list) -> int:
    """
    Remove and return root element.

    Time: O(log n)
    Space: O(1)
    """
    if not heap:
        raise IndexError("pop from empty heap")

    root = heap[0]
    heap[0] = heap[-1]            # Move last to root
    heap.pop()                     # Remove last
    if heap:
        heapify_down(heap, 0, len(heap))  # Bubble down

    return root
```

### 5. Build Heap (Heapify)

```python
def build_heap(arr: list) -> None:
    """
    Convert array to heap in-place.

    Time: O(n) - NOT O(n log n)!
    Space: O(1)

    Why O(n)? Nodes near bottom (most nodes) do little work.
    """
    n = len(arr)
    # Start from last non-leaf node
    for i in range(n // 2 - 1, -1, -1):
        heapify_down(arr, i, n)
```

**Why Build Heap is O(n), not O(n log n)?**

Most nodes are near the bottom and do little work:
- n/2 nodes at leaves: 0 swaps
- n/4 nodes at level 1: at most 1 swap
- n/8 nodes at level 2: at most 2 swaps
- Sum: n/4 + 2(n/8) + 3(n/16) + ... = O(n)

---

## Complete Min Heap Implementation

```python
class MinHeap:
    """
    Min heap implementation for interview understanding.
    In practice, use Python's heapq module.
    """
    def __init__(self):
        self.heap = []

    def push(self, val: int) -> None:
        """Add element to heap. Time: O(log n)"""
        self.heap.append(val)
        self._heapify_up(len(self.heap) - 1)

    def pop(self) -> int:
        """Remove and return minimum. Time: O(log n)"""
        if not self.heap:
            raise IndexError("pop from empty heap")

        root = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._heapify_down(0)
        return root

    def peek(self) -> int:
        """Return minimum without removing. Time: O(1)"""
        if not self.heap:
            raise IndexError("peek from empty heap")
        return self.heap[0]

    def __len__(self) -> int:
        return len(self.heap)

    def _heapify_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index] < self.heap[parent]:
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
                index = parent
            else:
                break

    def _heapify_down(self, index: int) -> None:
        size = len(self.heap)
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < size and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < size and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break
```

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| push | O(log n) | O(1) | Heapify up |
| pop | O(log n) | O(1) | Heapify down |
| peek | O(1) | O(1) | Access root |
| build_heap | O(n) | O(1) | In-place heapify |
| search | O(n) | O(1) | Must check all (no ordering) |

---

## Common Variations

### Max Heap (Negate Values)

Python's heapq is min heap only. For max heap, negate values:

```python
import heapq

# Max heap simulation
max_heap = []
heapq.heappush(max_heap, -5)  # Push -5 to get max behavior
heapq.heappush(max_heap, -3)
heapq.heappush(max_heap, -7)

max_val = -heapq.heappop(max_heap)  # Returns 7 (largest)
```

### Heap with Custom Comparator

For complex objects, use tuples or wrapper classes:

```python
import heapq

# Priority queue with (priority, item)
pq = []
heapq.heappush(pq, (2, "task B"))
heapq.heappush(pq, (1, "task A"))
heapq.heappush(pq, (3, "task C"))

priority, task = heapq.heappop(pq)  # (1, "task A")
```

---

## Edge Cases

```python
# 1. Empty heap
heap = []
# → pop/peek should raise exception

# 2. Single element
heap = [5]
# → pop returns 5, heap becomes empty

# 3. All same values
heap = [3, 3, 3, 3]
# → Still valid heap, any order of same values works

# 4. Already sorted (ascending)
heap = [1, 2, 3, 4, 5]
# → Already a valid min heap

# 5. Reverse sorted (descending)
heap = [5, 4, 3, 2, 1]
# → Requires O(n) heapify to become min heap
```

---

## Heap vs Other Data Structures

| Operation | Heap | Sorted Array | BST (balanced) |
|-----------|------|--------------|----------------|
| Find min/max | O(1) | O(1) | O(log n) |
| Insert | O(log n) | O(n) | O(log n) |
| Delete min/max | O(log n) | O(1) or O(n) | O(log n) |
| Search | O(n) | O(log n) | O(log n) |
| Build | O(n) | O(n log n) | O(n log n) |

**Use heap when**: You only need min/max, not arbitrary search.

---

## Interview Tips

1. **Know the formulas**: Parent = (i-1)//2, Left = 2i+1, Right = 2i+2
2. **Understand O(n) heapify**: Interviewers often ask why it's not O(n log n)
3. **Use library in practice**: Implement only if asked, use heapq otherwise
4. **Min vs Max**: Default is min heap; negate for max heap
5. **Complete binary tree**: This is why height is always O(log n)

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Last Stone Weight | Easy | Basic heap operations |
| 2 | Kth Largest Element in a Stream | Easy | Maintain heap of size K |
| 3 | Sort an Array (Heap Sort) | Medium | Build heap + extract |
| 4 | Kth Largest Element in an Array | Medium | Heap or QuickSelect |

---

## Key Takeaways

1. **Heap = Complete binary tree + Heap property** stored as array
2. **Min heap**: Parent ≤ children, root is minimum
3. **Max heap**: Parent ≥ children, root is maximum
4. **Build heap is O(n)**, not O(n log n) — common interview question
5. **Use heapq in Python**: Don't implement from scratch unless asked

---

## Next: [02-python-heapq.md](./02-python-heapq.md)

Learn Python's heapq module and common usage patterns.
