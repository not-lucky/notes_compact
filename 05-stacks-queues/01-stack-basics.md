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

**Mental Model**: Imagine a narrow pipe where you can only add or remove balls from one end. This constraint forces LIFO ordering. The "cost" of this constraint is that you can't access middle elements. The "benefit" is that push/pop are O(1) and you automatically get LIFO ordering without any bookkeeping.

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
| `push(x)`          | Add element to top                  | O(1)\*          |
| `pop()`            | Remove and return top element       | O(1)            |
| `peek()` / `top()` | Return top element without removing | O(1)            |
| `isEmpty()`        | Check if stack is empty             | O(1)            |
| `size()`           | Return number of elements           | O(1)            |

\*Amortized for dynamic arrays

---

## Python Implementation

### Using Python List (Recommended)

```python
# Python list as stack - most common in interviews
stack = []

# Push
stack.append(1)
stack.append(2)
stack.append(3)
# stack = [1, 2, 3]

# Peek (view top without removing)
if stack:
    top = stack[-1]  # 3

# Pop (remove and return top)
if stack:
    val = stack.pop()  # 3
# stack = [1, 2]

# Check if empty
is_empty = len(stack) == 0  # False

# Size
size = len(stack)  # 2
```

### Stack Class Implementation

```python
class Stack:
    """
    Stack implementation using Python list.

    All operations are O(1) amortized.
    """
    def __init__(self):
        self._items = []

    def push(self, item) -> None:
        """Add item to top of stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return top item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
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

# deque can also be used as stack (append/pop from right)
stack = deque()

stack.append(1)       # Push
val = stack.pop()     # Pop
top = stack[-1]       # Peek (if not empty)
is_empty = len(stack) == 0
```

---

## Common Stack Patterns in Interviews

### Pattern 1: Matching/Balancing

```python
def is_valid_parentheses(s: str) -> bool:
    """
    Check if parentheses are valid.

    Time: O(n)
    Space: O(n)
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

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
    """
    Reverse string using stack.

    Time: O(n)
    Space: O(n)
    """
    stack = list(s)  # Push all characters
    result = []

    while stack:
        result.append(stack.pop())  # Pop in reverse order

    return ''.join(result)
```

### Pattern 3: Undo/History

```python
class TextEditor:
    """Simple text editor with undo."""

    def __init__(self):
        self.text = ""
        self.history = []  # Stack of previous states

    def write(self, chars: str) -> None:
        self.history.append(self.text)  # Save current state
        self.text += chars

    def delete(self, k: int) -> None:
        self.history.append(self.text)
        self.text = self.text[:-k] if k <= len(self.text) else ""

    def undo(self) -> None:
        if self.history:
            self.text = self.history.pop()
```

### Pattern 4: Iterative DFS

```python
def dfs_iterative(graph: dict, start: str) -> list:
    """
    Iterative DFS using explicit stack.

    Time: O(V + E)
    Space: O(V)
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
| push      | O(1)\*     | O(1)              |
| pop       | O(1)       | O(1)              |
| peek      | O(1)       | O(1)              |
| isEmpty   | O(1)       | O(1)              |
| Space     | O(n)       | O(n)              |

\*Amortized - occasional O(n) when resizing

### Why Python List Works Well

- `append()` and `pop()` operate at the end - O(1) amortized
- Dynamic resizing handled automatically
- Simple and clean syntax

---

## Common Variations

### 1. Stack with Maximum

Track maximum element efficiently (covered in [06-min-stack.md](./06-min-stack.md)).

### 2. Two Stacks in One Array

```python
class TwoStacks:
    """Two stacks using single array."""

    def __init__(self, capacity: int):
        self.arr = [None] * capacity
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

    def pop1(self) -> int:
        if self.top1 >= 0:
            x = self.arr[self.top1]
            self.top1 -= 1
            return x
        return None  # Empty

    def pop2(self) -> int:
        if self.top2 < len(self.arr):
            x = self.arr[self.top2]
            self.top2 += 1
            return x
        return None  # Empty
```

### 3. Stack Using Linked List

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedStack:
    """Stack using linked list - O(1) guaranteed (no resizing)."""

    def __init__(self):
        self.head = None
        self._size = 0

    def push(self, val: int) -> None:
        new_node = ListNode(val, self.head)
        self.head = new_node
        self._size += 1

    def pop(self) -> int:
        if not self.head:
            raise IndexError("pop from empty stack")
        val = self.head.val
        self.head = self.head.next
        self._size -= 1
        return val

    def peek(self) -> int:
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
stack = []
# → Check before pop/peek to avoid IndexError

# 2. Single element
stack = [1]
stack.pop()  # Now empty
# → Check if empty after operation

# 3. Pop from empty
stack = []
if stack:  # Always check first
    stack.pop()

# 4. Peek from empty
stack = []
top = stack[-1] if stack else None  # Safe peek
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
2. **O(1) operations**: push, pop, peek all constant time
3. **Python list**: Use `append()` and `pop()` - simple and efficient
4. **Check before access**: Always verify stack is not empty
5. **Recognize patterns**: Matching, reversal, history, DFS all use stacks

---

## Next: [02-queue-basics.md](./02-queue-basics.md)

Learn about queues, their FIFO ordering, and when to choose queues over stacks.
