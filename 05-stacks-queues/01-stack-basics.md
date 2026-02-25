# Stack Basics

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

## Overview

A stack is a linear data structure that follows the Last-In-First-Out (LIFO) principle. Think of it as a vertical container where you can only access the top element. This simple constraint makes stacks surprisingly powerful for solving problems involving nested structures, undo operations, and depth-first traversal.

## Building Intuition

**Why does LIFO ordering matter?**

Think about how you naturally handle nested activities in real life:

1. **Reading email chains**: You start with the latest reply (most recent), then work backward to understand context. The last message you received is the first you read—that's LIFO.

2. **Putting on and taking off clothes**: You put on your shirt, then jacket. To undress, you remove the jacket first, then the shirt. The last item on is the first item off.

3. **Navigating web pages**: You click through pages A → B → C. The back button returns to C's predecessor (B), not the original page (A). Your browser history is a stack.

**The Core Insight**:

```
When processing nested or reversible structures, the most recent
incomplete item must be resolved before returning to earlier items.
```

**Why this matters for algorithms**: Many problems have this "most recent first" property:

- **Matching brackets**: The most recently opened bracket must close first
- **Function calls**: The most recently called function must return first
- **Undo systems**: The most recent action is undone first
- **DFS traversal**: The most recently discovered path is explored first

**Mental Model**: Imagine a narrow pipe where you can only add or remove balls from one end. This constraint forces LIFO ordering. The "cost" of this constraint is that you can't access middle elements. The "benefit" is that push/pop are $\mathcal{O}(1)$ and you automatically get LIFO ordering without any bookkeeping.

## When NOT to Use Stacks

Stacks are the wrong choice when:

1. **Random Access Needed**: If you frequently need to access elements by position (not just the top), use an array or list instead. Stacks only expose the top element.

2. **FIFO Order Required**: If you need first-in-first-out ordering (like a waiting line), use a queue instead. Example: task schedulers that process oldest tasks first.

3. **Multiple Accesses Per Element**: If you need to peek at multiple elements simultaneously (like comparing top-3 items), a stack's single-element access is limiting.

4. **Frequent Middle Operations**: If you need to insert or remove from the middle, a linked list or deque is more appropriate.

5. **Size Matters More Than Order**: If you just need to track min/max/size without ordering, use simpler counters or heaps.

**Red Flags in Interviews**:

- "Process elements in arrival order" → Use queue
- "Access the kth element" → Use array/list
- "Find median of elements" → Use heaps
- "Need both ends" → Use deque

## Interview Context

Stacks are fundamental because:

1. **LIFO principle**: Last-In-First-Out ordering is essential for many algorithms
2. **Function call management**: Recursion uses the call stack internally
3. **Parsing applications**: Expression evaluation, syntax checking, undo operations
4. **DFS foundation**: Depth-first search can be implemented with explicit stack

Interviewers use stacks to test your understanding of order-dependent processing and ability to simulate recursive algorithms iteratively.

---

## Core Concept: What is a Stack?

A stack is a linear data structure that follows **LIFO (Last-In-First-Out)** principle. The last element added is the first to be removed.

```
Stack operations:

    push(1)     push(2)     push(3)     pop()       pop()

    ┌───┐       ┌───┐       ┌───┐       ┌───┐       ┌───┐
    │   │       │   │       │ 3 │ ←top  │   │       │   │
    ├───┤       ├───┤       ├───┤       ├───┤       ├───┤
    │   │       │ 2 │ ←top  │ 2 │       │ 2 │ ←top  │   │
    ├───┤       ├───┤       ├───┤       ├───┤       ├───┤
    │ 1 │ ←top  │ 1 │       │ 1 │       │ 1 │       │ 1 │ ←top
    └───┘       └───┘       └───┘       └───┘       └───┘
```

### Real-World Analogies

- **Stack of plates**: Take from top, add to top
- **Browser back button**: Most recent page first
- **Undo in editors**: Last action reversed first
- **Function calls**: Most recent call returns first

---

## Stack Operations

### Core Operations

| Operation          | Description                         | Time Complexity |
| ------------------ | ----------------------------------- | --------------- |
| `push(x)`          | Add element to top                  | $\mathcal{O}(1)$*       |
| `pop()`            | Remove and return top element       | $\mathcal{O}(1)$        |
| `peek()` / `top()` | Return top element without removing | $\mathcal{O}(1)$        |
| `isEmpty()`        | Check if stack is empty             | $\mathcal{O}(1)$        |
| `size()`           | Return number of elements           | $\mathcal{O}(1)$        |

\*Amortized for dynamic arrays

---

## Python Implementation

### Using Python List (Recommended)

```python
# Python list as stack - most common in interviews
stack_list: list[int] = []

# Push
stack_list.append(1)
stack_list.append(2)
stack_list.append(3)
# stack_list = [1, 2, 3]

# Peek (view top without removing)
if stack_list:
    top = stack_list[-1]  # 3

# Pop (remove and return top)
if stack_list:
    val = stack_list.pop()  # 3
# stack_list = [1, 2]

# Check if empty
is_empty = len(stack_list) == 0  # False

# Size
size = len(stack_list)  # 2
```

### Stack Class Implementation

```python
from typing import Any

class Stack:
    r"""
    Stack implementation using Python list.

    All operations are $\mathcal{O}(1)$ amortized.
    """
    def __init__(self):
        self._items: list[Any] = []

    def push(self, item: Any) -> None:
        """Add item to top of stack."""
        self._items.append(item)

    def pop(self) -> Any:
        """Remove and return top item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        """Return top item without removing. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if stack is empty."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return number of items in stack."""
        return len(self._items)

    def __len__(self) -> int:
        return self.size()

    def __repr__(self) -> str:
        return f"Stack({self._items})"


# Usage
stack = Stack()
stack.push(1)
stack.push(2)
print(stack.peek())  # 2
print(stack.pop())   # 2
print(stack.size())  # 1
```

### Using collections.deque

```python
from collections import deque
from typing import Deque

# deque can also be used as stack (append/pop from right)
# Unlike lists, deque operations are strictly $\mathcal{O}(1)$ non-amortized,
# because deque is implemented as a doubly linked list in Python.
stack_deque: Deque[int] = deque()

stack_deque.append(1)       # Push
val = stack_deque.pop()     # Pop
top = stack_deque[-1]       # Peek (if not empty)
is_empty = len(stack_deque) == 0
```

---

## Common Stack Patterns in Interviews

### Pattern 1: Matching/Balancing

```python
def is_valid_parentheses(s: str) -> bool:
    r"""
    Check if parentheses are valid.

    Time: $\mathcal{O}(n)$
    Space: $\mathcal{O}(n)$
    """
    stack: list[str] = []
    mapping = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in mapping:
            # Closing bracket - check match
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            # Opening bracket - push
            stack.append(char)

    return len(stack) == 0
```

### Pattern 2: Reverse Order

```python
def reverse_string(s: str) -> str:
    r"""
    Reverse string using stack.

    Time: $\mathcal{O}(n)$
    Space: $\mathcal{O}(n)$
    """
    stack = list(s)  # Push all characters
    result: list[str] = []

    while stack:
        result.append(stack.pop())  # Pop in reverse order

    return "".join(result)
```

### Pattern 3: Undo/History

```python
class TextEditor:
    """Simple text editor with undo."""

    def __init__(self):
        self.text = ""
        self.history: list[str] = []  # Stack of previous states

    def write(self, chars: str) -> None:
        self.history.append(self.text)  # Save current state
        self.text += chars  # Note: string concatenation is O(n). A real editor uses more complex structures.

    def delete(self, k: int) -> None:
        self.history.append(self.text)
        self.text = self.text[:-k] if k <= len(self.text) else ""

    def undo(self) -> None:
        if self.history:
            self.text = self.history.pop()
```

### Pattern 4: Iterative DFS

```python
def dfs_iterative(graph: dict[str, list[str]], start: str) -> list[str]:
    r"""
    Iterative DFS using explicit stack.

    Time: $\mathcal{O}(V + E)$
    Space: $\mathcal{O}(V)$
    """
    visited = set()
    result = []
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            # Add neighbors in reverse order for left-to-right processing
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)

    return result
```

---

## Complexity Analysis

| Operation | List-based | Linked List-based |
| --------- | ---------- | ----------------- |
| push      | $\mathcal{O}(1)$* | $\mathcal{O}(1)$         |
| pop       | $\mathcal{O}(1)$  | $\mathcal{O}(1)$         |
| peek      | $\mathcal{O}(1)$  | $\mathcal{O}(1)$         |
| isEmpty   | $\mathcal{O}(1)$  | $\mathcal{O}(1)$         |
| Space     | $\mathcal{O}(n)$  | $\mathcal{O}(n)$         |

\*Amortized - occasional $\mathcal{O}(n)$ when resizing

### Why Python List Works Well

- `append()` and `pop()` operate at the end - $\mathcal{O}(1)$ amortized
- Dynamic resizing handled automatically
- Simple and clean syntax

---

## Common Variations

### 1. Stack with Maximum

Track maximum element efficiently (covered in [06-min-stack.md](./06-min-stack.md)).

### 2. Two Stacks in One Array

```python
from typing import Optional

class TwoStacks:
    """Two stacks using a single array."""

    def __init__(self, capacity: int):
        self.arr: list[Optional[int]] = [None] * capacity
        self.top1 = -1
        self.top2 = capacity

    def push1(self, x: int) -> bool:
        if self.top1 + 1 < self.top2:
            self.top1 += 1
            self.arr[self.top1] = x
            return True
        return False  # Full

    def push2(self, x: int) -> bool:
        if self.top1 + 1 < self.top2:
            self.top2 -= 1
            self.arr[self.top2] = x
            return True
        return False  # Full

    def pop1(self) -> Optional[int]:
        if self.top1 >= 0:
            x = self.arr[self.top1]
            self.top1 -= 1
            return x
        return None  # Empty

    def pop2(self) -> Optional[int]:
        if self.top2 < len(self.arr):
            x = self.arr[self.top2]
            self.top2 += 1
            return x
        return None  # Empty
```

### 3. Stack Using Linked List

```python
from typing import Optional, Any

class ListNode:
    def __init__(self, val: Any = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next

class LinkedStack:
    r"""Stack using linked list - $\mathcal{O}(1)$ guaranteed (no resizing)."""

    def __init__(self):
        self.head: Optional[ListNode] = None
        self._size = 0

    def push(self, val: Any) -> None:
        new_node = ListNode(val, self.head)
        self.head = new_node
        self._size += 1

    def pop(self) -> Any:
        if not self.head:
            raise IndexError("pop from empty stack")
        val = self.head.val
        self.head = self.head.next
        self._size -= 1
        return val

    def peek(self) -> Any:
        if not self.head:
            raise IndexError("peek from empty stack")
        return self.head.val

    def is_empty(self) -> bool:
        return self.head is None

    def size(self) -> int:
        return self._size
```

---

## Edge Cases

```python
# 1. Empty stack
stack: list[int] = []
# → Check before pop/peek to avoid IndexError

# 2. Single element
stack_single = [1]
stack_single.pop()  # Now empty
# → Check if empty before next operation

# 3. Pop from empty
stack_empty: list[int] = []
if stack_empty:  # Always check first
    stack_empty.pop()

# 4. Peek from empty
stack_peek: list[int] = []
top = stack_peek[-1] if stack_peek else None  # Safe peek
```

---

## Interview Tips

1. **Always check for empty** before `pop()` or `peek()`
2. **Use Python list** unless asked for linked list implementation
3. **Consider space-time tradeoffs** when using auxiliary stacks
4. **Recognize stack problems**: matching, reversal, undo, DFS, parsing

---

## Practice Problems

| #   | Problem                          | Difficulty | Key Concept          |
| --- | -------------------------------- | ---------- | -------------------- |
| 1   | Valid Parentheses                | Easy       | Stack matching       |
| 2   | Baseball Game                    | Easy       | Stack operations     |
| 3   | Backspace String Compare         | Easy       | Stack for processing |
| 4   | Remove All Adjacent Duplicates   | Easy       | Stack cleanup        |
| 5   | Daily Temperatures               | Medium     | Monotonic stack      |
| 6   | Min Stack                        | Medium     | Auxiliary stack      |
| 7   | Evaluate Reverse Polish Notation | Medium     | Operator stack       |

---

## Key Takeaways

1. **LIFO**: Last-In-First-Out principle is fundamental
2. **$\mathcal{O}(1)$ operations**: push, pop, peek all constant time
3. **Python list**: Use `append()` and `pop()` - simple and efficient
4. **Check before access**: Always verify stack is not empty
5. **Recognize patterns**: Matching, reversal, history, DFS all use stacks

---

## Next: [02-queue-basics.md](./02-queue-basics.md)

Learn about queues, their FIFO ordering, and when to choose queues over stacks.
