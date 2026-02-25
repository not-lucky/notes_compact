# Queue Basics

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md), [01-stack-basics](./01-stack-basics.md)

## Overview

A queue is a linear data structure that follows the First-In-First-Out (FIFO) principle. Think of it as a horizontal pipe where elements enter at one end and exit at the other. This ordering makes queues essential for fair scheduling, level-by-level traversal, and any scenario where "first come, first served" matters.

## Building Intuition

**Why does FIFO ordering matter?**

FIFO is the natural ordering for fairness and breadth exploration:

1. **Waiting in line**: The person who arrived first gets served first. Jumping ahead breaks fairness. Every real-world queue—grocery stores, customer support, DMV—uses FIFO.

2. **Printing documents**: If you send document A, then B, then C to a printer, you expect them to print in that order. LIFO would be chaos.

3. **Exploring a maze level-by-level**: When finding the shortest path, you want to explore all options 1 step away before any options 2 steps away. FIFO naturally gives this breadth-first behavior.

**The Core Insight**:

```
When all waiting items have equal priority, the oldest
waiting item should be processed first. This is fairness.
```

**Stack vs Queue Mental Model**:

```
Stack (LIFO): Like a vertical tube—add and remove from the same end
             Most recent item is always accessible
             Natural for: "most recent first", nested structures

Queue (FIFO): Like a horizontal pipe—add at one end, remove at other
              Oldest item is always accessible
              Natural for: fairness, level-by-level, shortest paths
```

**Why BFS Uses Queues**: In breadth-first search, you want to explore all nodes at distance k before any nodes at distance k+1. When you discover a neighbor, you add it to the queue (it waits its turn). When you process a node, you take from the front (oldest waiting). This ensures distance-ordered exploration.

**The Hidden Guarantee**: With a queue, if you add items A, B, C, you're guaranteed to process them as A, B, C. This ordering guarantee is why queues are essential for simulation, message passing, and task scheduling.

## When NOT to Use Queues

Queues are the wrong choice when:

1. **Most Recent First**: If the newest item has higher priority (like undo operations), use a stack instead. Example: browser back button needs LIFO.

2. **Priority-Based Processing**: If items have different priorities (not just arrival order), use a priority queue (heap) instead. Example: emergency room triage.

3. **Random Access Needed**: If you need to access or modify items in the middle, use a list or deque. Queues only expose front and back.

4. **Both Ends Matter**: If you frequently need to add/remove from both ends, use a deque (double-ended queue) instead.

5. **Need to Find or Search**: If you need to check if an item exists or find its position, queues don't support efficient search—use a set or map.

**Red Flags in Interviews**:

- "Process most recent first" → Use stack
- "Higher priority items should be processed first" → Use heap
- "Find if element exists in the structure" → Use set/map
- "Access elements by index" → Use array/list

## Interview Context

Queues are fundamental because:

1. **FIFO principle**: First-In-First-Out ordering is essential for fair processing
2. **BFS foundation**: Breadth-first search uses queues for level-order traversal
3. **Scheduling**: Task queues, message queues, print spoolers all use FIFO
4. **Rate limiting**: Request queues, sliding window rate limiters

Interviewers use queues to test your understanding of order-dependent processing and level-by-level traversal patterns.

---

## Core Concept: What is a Queue?

A queue is a linear data structure that follows **FIFO (First-In-First-Out)** principle. The first element added is the first to be removed.

```
Queue operations:

enqueue(1)  enqueue(2)  enqueue(3)  dequeue()   dequeue()

 front→rear  front→rear  front→rear  front→rear  front→rear
┌───┐       ┌───┬───┐   ┌───┬───┬───┐ ┌───┬───┐   ┌───┐
│ 1 │       │ 1 │ 2 │   │ 1 │ 2 │ 3 │ │ 2 │ 3 │   │ 3 │
└───┘       └───┴───┘   └───┴───┴───┘ └───┴───┘   └───┘
  ↑           ↑           ↑             ↑           ↑
returns 1   returns 2
```

### Real-World Analogies

- **Line at a store**: First in line gets served first
- **Printer queue**: Documents print in order received
- **Customer support**: Tickets handled in submission order
- **Message queues**: Messages processed in arrival order

---

## Queue vs Stack Comparison

| Aspect   | Stack (LIFO)       | Queue (FIFO)               |
| -------- | ------------------ | -------------------------- |
| Order    | Last-In-First-Out  | First-In-First-Out         |
| Add      | push (to top)      | enqueue (to rear)          |
| Remove   | pop (from top)     | dequeue (from front)       |
| Use case | DFS, undo, parsing | BFS, scheduling, buffering |
| Analogy  | Stack of plates    | Line of people             |

---

## Queue Operations

### Core Operations

| Operation            | Description                           | Time Complexity |
| -------------------- | ------------------------------------- | --------------- |
| `enqueue(x)`         | Add element to rear                   | $\Theta(1)$            |
| `dequeue()`          | Remove and return front element       | $\Theta(1)$*          |
| `front()` / `peek()` | Return front element without removing | $\Theta(1)$            |
| `isEmpty()`          | Check if queue is empty               | $\Theta(1)$            |
| `size()`             | Return number of elements             | $\Theta(1)$            |

*$\Theta(1)$ with deque, $\Theta(n)$ with list

---

## Python Implementation

### Using collections.deque (Recommended)

```python
from collections import deque

# deque for O(1) operations on both ends
queue = deque()

# Enqueue (add to rear)
queue.append(1)
queue.append(2)
queue.append(3)
# queue = deque([1, 2, 3])

# Peek (view front without removing)
if queue:
    front = queue[0]  # 1

# Dequeue (remove and return front)
if queue:
    val = queue.popleft()  # 1
# queue = deque([2, 3])

# Check if empty
is_empty = len(queue) == 0  # False

# Size
size = len(queue)  # 2
```

### ⚠️ Why Not Use List for Queues?

```python
# BAD - $\Theta(n)$ dequeue
queue = [1, 2, 3]
val = queue.pop(0)  # $\Theta(n)$ - shifts all elements!

# GOOD - $\Theta(1)$ dequeue
from collections import deque
queue = deque([1, 2, 3])
val = queue.popleft()  # $\Theta(1)$
```

### Queue Class Implementation

```python
from collections import deque

class Queue:
    """
    Queue implementation using deque.

    All operations are $\Theta(1)$.
    """
    def __init__(self):
        self._items = deque()
        self._size = 0

    def enqueue(self, item) -> None:
        """Add item to rear of queue."""
        self._items.append(item)
        self._size += 1

    def dequeue(self):
        """Remove and return front item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        self._size -= 1
        return self._items.popleft()

    def front(self):
        """Return front item without removing. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._items[0]

    def rear(self):
        """Return rear item without removing."""
        if self.is_empty():
            raise IndexError("rear from empty queue")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if queue is empty."""
        return self._size == 0

    def size(self) -> int:
        """Return number of items in queue."""
        return self._size

    def __len__(self) -> int:
        return self.size()

    def __repr__(self) -> str:
        return f"Queue({list(self._items)})"


# Usage
queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
print(queue.front())    # 1
print(queue.dequeue())  # 1
print(queue.size())     # 1
```

---

## Circular Queue

A circular queue (ring buffer) uses fixed-size array efficiently by wrapping around.

```
Circular Queue visualization:

    front = 2, rear = 1
         ┌───┐
         │ 5 │ ← rear (next insert here)
    ┌────┴───┴────┐
    │      ↓      │
  ┌─┴─┐         ┌─┴─┐
  │ 4 │         │   │
  └─┬─┘         └─┬─┘
    │             │
  ┌─┴─┐         ┌─┴─┐
  │ 3 │ ← front │   │
  └─┬─┘         └─┬─┘
    │      ↑      │
    └────┬───┬────┘
         │   │
         └───┘
```

### Circular Queue Implementation

```python
class CircularQueue:
    """
    Fixed-size circular queue.

    Time Complexity: $\Theta(1)$ for all operations
    Space Complexity: $\Theta(k)$ where k is capacity
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        # Using a list of ints. Can be initialized with zeros.
        self.queue = [0] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def enqueue(self, val: int) -> bool:
        """Add element. Returns False if full."""
        if self.is_full():
            return False

        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = val
        self.size += 1
        return True

    def dequeue(self) -> int:
        """Remove and return front. Returns -1 if empty."""
        if self.is_empty():
            return -1

        val = self.queue[self.front]
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return val

    def get_front(self) -> int:
        """Return front element. Returns -1 if empty."""
        if self.is_empty():
            return -1
        return self.queue[self.front]

    def get_rear(self) -> int:
        """Return rear element. Returns -1 if empty."""
        if self.is_empty():
            return -1
        return self.queue[self.rear]

    def is_empty(self) -> bool:
        return self.size == 0

    def is_full(self) -> bool:
        return self.size == self.capacity


# LeetCode 622: Design Circular Queue
# Usage:
cq = CircularQueue(3)
cq.enqueue(1)  # True
cq.enqueue(2)  # True
cq.enqueue(3)  # True
cq.enqueue(4)  # False (full)
cq.get_rear()  # 3
cq.is_full()   # True
cq.dequeue()   # 1
cq.enqueue(4)  # True (wrapped around)
cq.get_rear()  # 4
```

---

## Common Queue Patterns in Interviews

### Pattern 1: BFS (Level-Order Traversal)

```python
from collections import deque

def bfs(graph: dict[str, list[str]], start: str) -> list[str]:
    """
    Breadth-first search using queue.

    Time Complexity: $\mathcal{O}(V + E)$
    Space Complexity: $\mathcal{O}(V)$
    """
    visited = {start}
    result = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result
```

### Pattern 2: Level-by-Level Processing

```python
from collections import deque

from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

def level_order_traversal(root: Optional[TreeNode]) -> list[list[int]]:
    """
    Binary tree level order traversal.

    Time Complexity: $\Theta(n)$
    Space Complexity: $\Theta(n)$
    """
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result
```

### Pattern 3: Moving Average (Sliding Window)

```python
from collections import deque

class MovingAverage:
    """
    Calculate moving average of last size elements.

    Time Complexity: $\Theta(1)$ per next() call
    Space Complexity: $\Theta(size)$
    """
    def __init__(self, size: int):
        self.size = size
        self.queue = deque()
        self.total = 0

    def next(self, val: int) -> float:
        self.queue.append(val)
        self.total += val

        if len(self.queue) > self.size:
            self.total -= self.queue.popleft()

        return self.total / len(self.queue)


# Usage
ma = MovingAverage(3)
print(ma.next(1))  # 1.0
print(ma.next(10)) # 5.5 = (1+10)/2
print(ma.next(3))  # 4.67 = (1+10+3)/3
print(ma.next(5))  # 6.0 = (10+3+5)/3
```

### Pattern 4: Recent Counter (Rate Limiting)

```python
from collections import deque

class RecentCounter:
    """
    Count requests in the last 3000 milliseconds.

    Time Complexity: $\mathcal{O}(1)$ amortized
    Space Complexity: $\mathcal{O}(w)$ where w is the number of requests in window
    """
    def __init__(self):
        self.requests = deque()

    def ping(self, t: int) -> int:
        self.requests.append(t)

        # Remove requests outside the 3000ms window
        while self.requests[0] < t - 3000:
            self.requests.popleft()

        return len(self.requests)


# Usage
rc = RecentCounter()
print(rc.ping(1))      # 1
print(rc.ping(100))    # 2
print(rc.ping(3001))   # 3
print(rc.ping(3002))   # 3 (request at t=1 expired)
```

---

## Deque: Double-Ended Queue

A deque allows insertion and deletion at both ends in $\Theta(1)$ time.

```python
from collections import deque

dq = deque()

# Add to both ends
dq.append(1)      # Add to right: [1]
dq.appendleft(0)  # Add to left: [0, 1]
dq.append(2)      # [0, 1, 2]

# Remove from both ends
val = dq.pop()       # Remove from right: 2, dq = [0, 1]
val = dq.popleft()   # Remove from left: 0, dq = [1]

# Peek both ends
if dq:
    front = dq[0]
    rear = dq[-1]
```

### Deque Applications

- **Sliding window maximum**: Maintain monotonic deque
- **Palindrome check**: Compare from both ends
- **Work stealing**: Take from own end, steal from other end

---

## Complexity Summary

| Implementation | enqueue | dequeue | front | Space |
| -------------- | ------- | ------- | ----- | ----- |
| List (bad)     | $\Theta(1)$    | $\Theta(n)$ ⚠️ | $\Theta(1)$  | $\Theta(n)$  |
| deque          | $\Theta(1)$    | $\Theta(1)$    | $\Theta(1)$  | $\Theta(n)$  |
| Circular array | $\Theta(1)$    | $\Theta(1)$    | $\Theta(1)$  | $\Theta(k)$  |
| Linked list    | $\Theta(1)$*  | $\Theta(1)$    | $\Theta(1)$  | $\Theta(n)$  |

*With tail pointer

---

## Queue Using Linked List

```python
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next

class LinkedQueue:
    """Queue using linked list with $\Theta(1)$ operations."""

    def __init__(self):
        self.front: Optional[ListNode] = None
        self.rear: Optional[ListNode] = None
        self._size = 0

    def enqueue(self, val: int) -> None:
        new_node = ListNode(val)
        if self.rear:
            self.rear.next = new_node
        self.rear = new_node
        if not self.front:
            self.front = new_node
        self._size += 1

    def dequeue(self) -> int:
        if not self.front:
            raise IndexError("dequeue from empty queue")
        val = self.front.val
        self.front = self.front.next
        if not self.front:
            self.rear = None
        self._size -= 1
        return val

    def peek(self) -> int:
        if not self.front:
            raise IndexError("peek from empty queue")
        return self.front.val

    def is_empty(self) -> bool:
        return self.front is None

    def size(self) -> int:
        return self._size
```

---

## Edge Cases

```python
from collections import deque

# 1. Empty queue
queue = deque()
# → Check before dequeue/peek

# 2. Single element
queue = deque([1])
queue.popleft()  # Now empty

# 3. Dequeue from empty
queue = deque()
if queue:  # Always check first
    queue.popleft()

# 4. Circular queue wrap-around
# → Ensure proper modulo arithmetic
```

---

## Interview Tips

1. **Use `deque`** for $\Theta(1)$ operations in Python
2. **Never use `list.pop(0)`** - it's $\Theta(n)$
3. **BFS = Queue, DFS = Stack** - this pattern is fundamental
4. **Circular queue for fixed capacity** - more space efficient
5. **Level-by-level processing**: Track level size before processing

---

## Practice Problems

| #   | Problem                           | Difficulty | Key Concept         |
| --- | --------------------------------- | ---------- | ------------------- |
| 1   | Design Circular Queue             | Medium     | Circular array      |
| 2   | Number of Recent Calls            | Easy       | Sliding window      |
| 3   | Moving Average from Data Stream   | Easy       | Queue + running sum |
| 4   | Implement Queue using Stacks      | Easy       | Two stacks          |
| 5   | Design Circular Deque             | Medium     | Double-ended        |
| 6   | Binary Tree Level Order Traversal | Medium     | BFS                 |
| 7   | Rotting Oranges                   | Medium     | Multi-source BFS    |

---

## Key Takeaways

1. **FIFO**: First-In-First-Out principle
2. **Use deque**: `collections.deque` for $\Theta(1)$ operations
3. **Never `list.pop(0)`**: It's $\Theta(n)$, use `deque.popleft()`
4. **BFS foundation**: Queue is essential for breadth-first algorithms
5. **Circular queue**: Efficient fixed-size buffer with wrap-around

---

## Next: [03-valid-parentheses.md](./03-valid-parentheses.md)

Learn the classic stack matching pattern for validating nested structures.
