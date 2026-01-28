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

## Building Intuition

**Why Store a Tree as an Array?**

The heap's brilliance is using array indices as implicit pointers. No node objects, no left/right references—just math:

```
Parent of i:     (i - 1) // 2
Left child of i:  2*i + 1
Right child of i: 2*i + 2

For index 3:
- Parent: (3-1)//2 = 1
- Left child: 2*3+1 = 7
- Right child: 2*3+2 = 8

This works because a complete binary tree has NO GAPS.
Level 0: 1 node  (indices 0)
Level 1: 2 nodes (indices 1-2)
Level 2: 4 nodes (indices 3-6)
Level 3: 8 nodes (indices 7-14)
```

**Mental Model: The Tournament Bracket**

Think of a min heap as an ongoing tournament where smaller values win:

```
Round 1 (leaves):    7   4   6   5
                      \ /     \ /
Round 2:              4       5
                       \     /
Finals:                  4 (winner = minimum)
```

Each parent "won" against both children. The root is the ultimate winner (smallest value). When you remove the winner, you run a new tournament from that position down.

**Why Heapify Up vs Heapify Down?**

- **Heapify UP**: New element enters at bottom, might be "too good" (too small for min heap), bubbles up to its rightful place
- **Heapify DOWN**: Element at top might be "not good enough", sinks down as better elements rise

```
Insert 1 into [3, 5, 4, 7, 8]:

  3          3          1     ← 1 bubbles UP
 / \   →    / \    →   / \
5   4      1   4      3   4
/\        / \        / \
7 8 1    7 8 5      7 8 5

Pop from [1, 3, 4, 7, 8, 5]:

  1          5          3     ← 5 sinks DOWN
 / \   →    / \    →   / \
3   4      3   4      5   4
/\ /      /\ /       /\ /
7 8 5    7 8        7 8
         (5 moved)
```

**Why O(n) Build Heap Is Not Intuitive**

Most people think: "n elements × O(log n) per insert = O(n log n)". But building bottom-up is different:

```
Heap of height h has 2^h nodes at bottom level.

Work done at each level:
- Level h (leaves): 2^h nodes × 0 swaps = 0
- Level h-1:        2^(h-1) nodes × 1 swap max
- Level h-2:        2^(h-2) nodes × 2 swaps max
- ...
- Level 0 (root):   1 node × h swaps max

Total = Σ (nodes at level) × (distance to bottom)
      = O(n) by mathematical analysis

KEY INSIGHT: Half the nodes are leaves doing ZERO work!
```

**When to Use Heap vs Sorted Structure**

```
Need                          | Use
------------------------------|----------------
Only min OR max repeatedly    | Heap
Range queries (all in [5,10]) | Sorted array/BST
Find kth element once         | QuickSelect
Find kth repeatedly (dynamic) | Heap or BST
```

---

## When NOT to Use a Heap

**1. You Need to Search for Arbitrary Elements**

Heap has O(n) search—it only orders parent-child, not siblings:

```
Min Heap:
      1
     / \
    5   2    ← 5 and 2 are NOT ordered relative to each other
   / \
  7   6      ← 7 and 6 are NOT ordered either

To find "is 6 in the heap?" → Must check every element
```

Use instead: Hash set O(1), BST O(log n), sorted array O(log n)

**2. You Need Both Min AND Max**

A min heap gives O(1) min but O(n) max (and vice versa). If you need both:

```python
# Bad: two separate heaps get out of sync when removing

# Good: Use a min-max heap (complex) or just sorted structure
```

Use instead: Balanced BST, or two heaps with lazy deletion

**3. You Need the Kth Element (Not Just First)**

Heap only guarantees the root. Getting kth smallest requires k pops:

```python
# To get 5th smallest: pop 5 times = O(k log n)
# Not efficient for large k
```

Use instead: Order statistic tree, sorted array with index access

**4. You Need to Modify Priorities Efficiently**

Standard heap has O(n) to find an element before changing its priority:

```python
# Change priority of "task_x" from 5 to 2?
# Step 1: Find "task_x" → O(n) scan
# Step 2: Update and reheapify → O(log n)
# Total: O(n)
```

Use instead: Indexed heap (heap + hash map), or Fibonacci heap

**5. Data Is Already Sorted**

If input is sorted and you just need min/max:

```python
sorted_arr = [1, 2, 3, 4, 5]
min_val = sorted_arr[0]   # O(1)
max_val = sorted_arr[-1]  # O(1)
# No heap needed!
```

**Red Flags:**

- "Find if X exists in the heap" → Need hash set or BST
- "Get both minimum and maximum" → Need different structure
- "Update priority of specific item" → Need indexed priority queue
- "Get kth smallest without removing" → Need order statistic tree

---

## Core Concept: What is a Heap?

A **heap** is a complete binary tree stored as an array where each parent satisfies the **heap property** with its children.

### Min Heap vs Max Heap

| Type         | Property          | Root Contains   |
| ------------ | ----------------- | --------------- |
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
Array:  [  1,    3,    2,    7,    4  ]
Index:     0     1     2     3     4

Tree:
             1 [idx:0]
           /   \
  [idx:1] 3     2 [idx:2]
         / \
[idx:3] 7   4 [idx:4]

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

| Operation  | Time     | Space | Notes                        |
| ---------- | -------- | ----- | ---------------------------- |
| push       | O(log n) | O(1)  | Heapify up                   |
| pop        | O(log n) | O(1)  | Heapify down                 |
| peek       | O(1)     | O(1)  | Access root                  |
| build_heap | O(n)     | O(1)  | In-place heapify             |
| search     | O(n)     | O(1)  | Must check all (no ordering) |

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

| Operation      | Heap     | Sorted Array | BST (balanced) |
| -------------- | -------- | ------------ | -------------- |
| Find min/max   | O(1)     | O(1)         | O(log n)       |
| Insert         | O(log n) | O(n)         | O(log n)       |
| Delete min/max | O(log n) | O(1) or O(n) | O(log n)       |
| Search         | O(n)     | O(log n)     | O(log n)       |
| Build          | O(n)     | O(n log n)   | O(n log n)     |

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

| #   | Problem                         | Difficulty | Key Concept             |
| --- | ------------------------------- | ---------- | ----------------------- |
| 1   | Last Stone Weight               | Easy       | Basic heap operations   |
| 2   | Kth Largest Element in a Stream | Easy       | Maintain heap of size K |
| 3   | Sort an Array (Heap Sort)       | Medium     | Build heap + extract    |
| 4   | Kth Largest Element in an Array | Medium     | Heap or QuickSelect     |

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
