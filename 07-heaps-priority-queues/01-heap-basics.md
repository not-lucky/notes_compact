# Heap Basics

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md), [06-trees/01-tree-basics](../06-trees/01-tree-basics.md)

## Interview Context

Heaps are fundamental data structures that frequently appear in interviews because they are:

1. **Optimal for priority operations**: $O(\log n)$ insert/remove, $O(1)$ peek min/max.
2. **Foundation for many patterns**: Top-K elements, Merge K Sorted Lists, task scheduling algorithms.
3. **Memory efficient**: They are stored as an array with no pointer overhead.
4. **Prerequisites for advanced algorithms**: Dijkstra's shortest path, Prim's minimum spanning tree.

Interviewers expect you to intimately understand heap properties, the underlying array math, and operations, even if you just use library functions (like Python's `heapq`) in practice.

---

## Core Concept: What is a Heap?

A **heap** is a specialized tree-based data structure that satisfies two main properties:

1. **Structural Property (Complete Binary Tree):**
   - All levels of the tree are fully filled except possibly the last level.
   - The last level is filled strictly from left to right.
   - This guarantees the tree's height is always exactly $O(\log n)$ and allows it to be efficiently stored in an array without gaps.

2. **Ordering Property (Heap Property):**
   - In a **Min Heap**, the value of every parent node is less than or equal to the values of its children. The root node is the minimum element.
   - In a **Max Heap**, the value of every parent node is greater than or equal to the values of its children. The root node is the maximum element.

| Type         | Property          | Root Contains   |
| ------------ | ----------------- | --------------- |
| **Min Heap** | Parent $\le$ Children | Minimum element |
| **Max Heap** | Parent $\ge$ Children | Maximum element |

```text
Min Heap:                    Max Heap:
      1                           9
     / \                         / \
    3   2                       7   8
   / \                         / \
  7   4                       3   5

Array: [1, 3, 2, 7, 4]       Array: [9, 7, 8, 3, 5]
```

> **Crucial Distinction:** A heap is a partially ordered data structure. It only guarantees ordering between parents and children. Sibling nodes have no guaranteed relationship to each other (e.g., in the Min Heap above, 3 is the left child and 2 is the right child, but 3 > 2).

---

## Building Intuition

### Why Store a Tree as an Array?

The brilliance of a heap is using array indices as implicit pointers. There are no node objects and no left/right references—just math. Because a complete binary tree has NO GAPS, we can lay out the nodes level by level into a flat array.

```text
Tree Level      Nodes      Array Indices
Level 0:        1 node     [0]
Level 1:        2 nodes    [1, 2]
Level 2:        4 nodes    [3, 4, 5, 6]
Level 3:        8 nodes    [7, ..., 14]
```

**The Math (0-Indexed Array):**

If a node is at index `i`:
- **Parent Index**: `(i - 1) // 2`
- **Left Child Index**: `2*i + 1`
- **Right Child Index**: `2*i + 2`

```text
Array:  [  1,    3,    2,    7,    4  ]
Index:     0     1     2     3     4

Tree mapping:
             1 [idx:0]
           /   \
  [idx:1] 3     2 [idx:2]
         / \
[idx:3] 7   4 [idx:4]

Let's verify for index 1 (value 3):
- Parent: (1 - 1) // 2 = 0       -> value 1  (Correct)
- Left Child: 2*1 + 1 = 3        -> value 7  (Correct)
- Right Child: 2*1 + 2 = 4       -> value 4  (Correct)
```

### Mental Model: The Tournament Bracket

Think of a min heap as an ongoing tournament where smaller values "win" and advance towards the top.

```text
Round 1 (leaves):    7   4   6   5
                      \ /     \ /
Round 2:               4       5
                        \     /
Finals (root):             4 (winner = minimum)
```

Each parent "won" a match against both of its children. The root is the ultimate winner (the smallest value). When you remove the winner (pop), you take an unknown participant (usually the last leaf node), place them at the top, and run a new tournament from that position downwards to find the new winner.

### Why Heapify Up vs Heapify Down?

- **Heapify UP (Bubble Up / Sift Up)**: Used when a *new element* enters at the bottom (end of the array). It might be "too good" (too small for a min heap), so it bubbles UP by swapping with its parent until it finds its rightful place.
- **Heapify DOWN (Bubble Down / Sift Down)**: Used when an element at the top (the root) is removed, and a *leaf element* is placed there. This element is likely "not good enough", so it sinks DOWN by swapping with its smallest child as better elements rise.

---

## Core Operations

### 1. Push (Insert)

To add a new element:
1. Append it to the end of the array (maintaining the complete tree property).
2. **Heapify Up** to restore the heap property.

```python
def heap_push(heap: list[int], val: int) -> None:
    """
    Insert element into heap.
    Time: O(log n) | Space: O(1)
    """
    heap.append(val)
    _heapify_up(heap, len(heap) - 1)

def _heapify_up(heap: list[int], index: int) -> None:
    while index > 0:
        parent = (index - 1) // 2
        # Min heap: if child is smaller than parent, swap them
        if heap[index] < heap[parent]:
            heap[index], heap[parent] = heap[parent], heap[index]
            index = parent  # Move up
        else:
            break  # Heap property satisfied
```

### 2. Pop (Extract Min/Max)

To remove the root (minimum/maximum) element:
1. Save the root element to return later.
2. Remove the *last* element in the array and place it at the root (this destroys the heap property at the root, but keeps the complete tree structure).
3. **Heapify Down** from the root to restore the heap property.

```python
def heap_pop(heap: list[int]) -> int:
    """
    Remove and return root element.
    Time: O(log n) | Space: O(1)
    """
    if not heap:
        raise IndexError("pop from empty heap")

    root = heap[0]
    last = heap.pop()  # Remove last element
    if heap:           # If heap wasn't just 1 element
        heap[0] = last # Move last element to root
        _heapify_down(heap, 0)

    return root

def _heapify_down(heap: list[int], index: int) -> None:
    size = len(heap)
    while True:
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        # Find the smallest among node and its two children
        if left < size and heap[left] < heap[smallest]:
            smallest = left
        if right < size and heap[right] < heap[smallest]:
            smallest = right

        # If smallest is not the current node, swap and continue down
        if smallest != index:
            heap[index], heap[smallest] = heap[smallest], heap[index]
            index = smallest
        else:
            break  # Heap property satisfied
```

---

## The $O(n)$ Build Heap Concept

One of the most frequently asked theoretical interview questions is: **"Why does building a heap from an unsorted array take $O(n)$ time, rather than $O(n \log n)$?"**

If you build a heap by calling `push()` $n$ times, it *is* $O(n \log n)$ because each insert takes up to $O(\log n)$ time.

However, an optimized `build_heap` (often called Floyd's algorithm) works **bottom-up**:

```python
def build_heap(arr: list[int]) -> None:
    """
    Convert an unsorted array into a valid heap in-place.
    Time: O(n) | Space: O(1)
    """
    n = len(arr)
    # Start from the last non-leaf node and heapify down to the root
    for i in range(n // 2 - 1, -1, -1):
        _heapify_down(arr, i)
```

### Why is Build Heap $O(n)$?

The intuition lies in realizing that **most nodes in a tree are near the bottom**, and nodes near the bottom have very little distance to travel when they heapify down.

Consider a complete binary tree of $n$ nodes and height $h \approx \log n$:
- Roughly **half the nodes** ($\approx n/2$) are leaves. They have no children, so calling `heapify_down` on them does $0$ work. (This is why the loop starts at `n // 2 - 1`).
- A quarter of the nodes ($\approx n/4$) are exactly one level above the leaves. They can travel at most $1$ level down.
- An eighth of the nodes ($\approx n/8$) can travel at most $2$ levels down.
- ... Only the **$1$ root node** can travel the maximum $h \approx \log n$ levels down.

Total Work = $\sum (\text{number of nodes at level}) \times (\text{max distance to bottom})$
Total Work = $0(n/2) + 1(n/4) + 2(n/8) + 3(n/16) + \dots + h(1)$

This converges to an infinite geometric series that bounds to **$O(n)$**.

> **Key Insight:** The algorithm does the *most* work (heapify down) on the *fewest* nodes (those near the root), and the *least* work (no heapify down) on the *most* nodes (the leaves).

---

## Complete Min Heap Implementation

While you should almost always use the built-in library (`heapq` in Python), understanding how to build it from scratch demonstrates deep knowledge.

```pythonPrim'
class MinHeap:
    """Min heap implementation for interview understanding."""
    def __init__(self):
        self.heap = []

    def push(self, val: int) -> None:
        """Time: O(log n)"""
        self.heap.append(val)
        self._heapify_up(len(self.heap) - 1)

    def pop(self) -> int:
        """Time: O(log n)"""
        if not self.heap:
            raise IndexError("pop from empty heap")

        root = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._heapify_down(0)
        return root

    def peek(self) -> int:
        """Time: O(1)"""
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

| Operation            | Time Complexity | Space Complexity | Description                               |
| -------------------- | --------------- | ---------------- | ----------------------------------------- |
| **Push**             | $O(\log n)$     | $O(1)$           | Insert at end, heapify up.                |
| **Pop**              | $O(\log n)$     | $O(1)$           | Replace root with last, heapify down.     |
| **Peek**             | $O(1)$          | $O(1)$           | Access array at index 0.                  |
| **Build Heap**       | $O(n)$          | $O(1)$           | In-place heapify array.                   |
| **Search (arbitrary)** | $O(n)$          | $O(1)$           | Must check all elements (no ordering).    |

---

## When NOT to Use a Heap

Heaps are heavily optimized for min/max queries. They are **terrible** for almost everything else. Here are major "anti-patterns" where a heap is the wrong choice:

**1. Searching for Arbitrary Elements ($O(n)$)**
A heap does not order siblings. To check if an element `x` exists, you must scan the entire array.
*Use instead:* Hash Set $O(1)$ or Binary Search Tree $O(\log n)$.

**2. You Need Both Min AND Max Efficiently**
A min heap gives $O(1)$ min, but finding the max requires inspecting all $O(n/2)$ leaf nodes.
*Use instead:* Balanced BST, or a more complex dual-structure (like separate min and max heaps with lazy deletion).

**3. Finding the Kth Element Once ($O(n \log k)$ or $O(k \log n)$)**
If you just need the 5th smallest element in a static list, putting everything in a heap and popping 5 times works, but it's not optimal.
*Use instead:* QuickSelect $O(n)$.
*(Note: If the list is dynamic and you repeatedly need the Kth element, a heap is the right choice).*

**4. Modifying Priorities of Existing Items ($O(n)$)**
Standard heaps cannot efficiently find an item to change its priority. E.g., changing the priority of "task_A" from 5 to 2 requires an $O(n)$ search, followed by an $O(\log n)$ heapify.
*Use instead:* Indexed Priority Queue (a heap augmented with a Hash Map) or Fibonacci Heap.

---

## Common Variations

### Max Heap (Negate Values)

Python's `heapq` is strictly a min heap. To simulate a max heap with numbers, simply **negate the values** before pushing, and negate them again after popping:

```python
import heapq

max_heap = []
heapq.heappush(max_heap, -5)  # Representing 5
heapq.heappush(max_heap, -10) # Representing 10
heapq.heappush(max_heap, -3)  # Representing 3

# Pops -10, negate to get 10
largest = -heapq.heappop(max_heap)
```

### Heap with Custom Objects

When dealing with complex objects (like tasks, nodes, or graphs), store a tuple: `(priority, object)`. Python's `heapq` will sort based on the first element (the priority).

If priorities tie, Python will try to compare the objects themselves. If the objects don't support comparison (e.g., custom classes without `__lt__`), it will crash. **Fix ties** by adding a unique identifier (like an incrementing counter) as the second element: `(priority, insert_order_id, object)`.

```python
import heapq

pq = []
heapq.heappush(pq, (2, 0, "task B")) # (priority, id, task)
heapq.heappush(pq, (1, 1, "task A"))
heapq.heappush(pq, (1, 2, "task C")) # Ties resolved by id

# Pops (1, 1, "task A") -> lowest priority, lowest id
priority, _, task = heapq.heappop(pq)
```

---

## Edge Cases to Consider

- **Empty Heap**: Calling pop or peek on an empty heap should raise an `IndexError`. Handle this explicitly in interviews.
- **Single Element**: Popping from a single-element heap should not trigger `heapify_down`, it just returns the element and leaves the heap empty.
- **Duplicate Values**: Heaps handle duplicate values perfectly well. The structural property prevents any issues.
- **Already Sorted Data**:
  - An ascending array `[1, 2, 3, 4, 5]` is *already* a valid min heap.
  - A descending array `[5, 4, 3, 2, 1]` is a valid max heap, but takes $O(n)$ time to convert to a min heap.

---

## Interview Tips

1. **Know the formulas by heart**: Parent = `(i-1)//2`, Left = `2i+1`, Right = `2i+2`.
2. **Nail the $O(n)$ heapify explanation**: Interviewers will probe this. Mention "half the nodes are leaves doing zero work".
3. **Use the library**: Unless specifically asked to implement one from scratch, ALWAYS say "I'll use Python's built-in `heapq` to maintain a min/max heap".
4. **Spot the pattern**: "Kth largest/smallest", "Top K frequent", "Merge K sorted lists" are immediate giveaways for a Heap.

---

## Practice Problems

| #   | Problem | Difficulty | Key Concept |
| --- | --- | --- | --- |
| 1 | Last Stone Weight | Easy | Basic max heap operations (negate values). |
| 2 | Kth Largest Element in a Stream | Easy | Maintain a min heap of size exactly $K$. |
| 3 | Kth Largest Element in an Array | Medium | Use a heap or implement QuickSelect. |
| 4 | Sort an Array (Heap Sort) | Medium | Build heap $O(n)$, then extract min/max $O(n \log n)$. |

---

## Next Steps

Learn how to use Python's built-in heap library and common usage patterns in:
[02-python-heapq.md](./02-python-heapq.md)
