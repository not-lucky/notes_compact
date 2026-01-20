# Min Stack

## Problem Statement

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the `MinStack` class:
- `push(val)` - pushes element onto stack
- `pop()` - removes element on top of stack
- `top()` - gets the top element
- `getMin()` - retrieves the minimum element

All operations must be O(1) time complexity.

**Example:**
```
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin(); // return -3
minStack.pop();
minStack.top();    // return 0
minStack.getMin(); // return -2
```

## Approach

### Two Stacks
- Main stack: stores all elements
- Min stack: stores minimum at each level

### Single Stack with Pairs
Store (value, current_min) pairs

### Key Insight
When we push, the minimum can only decrease or stay same.
When we pop, we need to know what the minimum was before this push.

## Implementation

```python
class MinStack:
    """
    MinStack using two stacks.

    Time: O(1) for all operations
    Space: O(n) - two stacks
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Push to min_stack if empty or val <= current min
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        val = self.stack.pop()
        # If popped value was the min, also pop from min_stack
        if val == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]


class MinStackPairs:
    """
    MinStack storing (value, current_min) pairs.

    Time: O(1) for all operations
    Space: O(n) - single stack with pairs
    """
    def __init__(self):
        self.stack = []  # Each element is (value, min_so_far)

    def push(self, val: int) -> None:
        current_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


class MinStackSingleValue:
    """
    MinStack with O(1) extra space using encoding trick.
    Stores difference between value and current min.

    Note: May have overflow issues with extreme values.
    """
    def __init__(self):
        self.stack = []
        self.min_val = float('inf')

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append(0)
            self.min_val = val
        else:
            # Store difference from current min
            self.stack.append(val - self.min_val)
            if val < self.min_val:
                self.min_val = val

    def pop(self) -> None:
        top = self.stack.pop()
        if top < 0:
            # This means the popped value was the min
            # Restore previous min
            self.min_val = self.min_val - top
        if not self.stack:
            self.min_val = float('inf')

    def top(self) -> int:
        top = self.stack[-1]
        if top < 0:
            # Actual value is min_val (we stored negative diff)
            return self.min_val
        else:
            return top + self.min_val

    def getMin(self) -> int:
        return self.min_val
```

## Complexity Analysis

| Operation | Time | Space (Two Stacks) | Space (Single Value) |
|-----------|------|-------------------|---------------------|
| push | O(1) | O(1) amortized | O(1) |
| pop | O(1) | O(1) | O(1) |
| top | O(1) | O(1) | O(1) |
| getMin | O(1) | O(1) | O(1) |
| **Total** | O(1) all | O(n) | O(n) |

## Visual Walkthrough

```
Operations: push(-2), push(0), push(-3), getMin, pop, top, getMin

Two Stacks Approach:
┌─────────────────────────────────────────────────┐
│ Step      │ Stack     │ Min Stack │ getMin     │
├───────────┼───────────┼───────────┼────────────┤
│ push(-2)  │ [-2]      │ [-2]      │            │
│ push(0)   │ [-2,0]    │ [-2]      │            │
│ push(-3)  │ [-2,0,-3] │ [-2,-3]   │            │
│ getMin()  │           │           │ -3         │
│ pop()     │ [-2,0]    │ [-2]      │            │
│ top()     │           │           │ 0          │
│ getMin()  │           │           │ -2         │
└─────────────────────────────────────────────────┘
```

## Edge Cases

1. **Single element**: Min is that element
2. **Duplicate minimums**: Handle with <= comparison
3. **Pop minimum**: Min stack must also pop
4. **Empty stack**: Undefined behavior (assume valid calls)
5. **Large values**: Watch for overflow in single-value approach

## Common Mistakes

1. **Not handling duplicate mins**: Use `<=` not `<` when pushing to min stack
2. **Wrong order of operations**: Pop from both stacks when values match
3. **Empty min stack**: Always push first element to min stack
4. **Returning wrong stack's top**: `top()` should return from main stack

## Variations

### Max Stack (with popMax)
```python
import heapq
from sortedcontainers import SortedList

class MaxStack:
    """
    Stack with popMax operation.
    Uses sorted list for O(log n) popMax.
    """
    def __init__(self):
        self.stack = []  # (value, id)
        self.sorted = SortedList()  # (value, id)
        self.removed = set()  # ids that were removed
        self.id = 0

    def push(self, x: int) -> None:
        self.stack.append((x, self.id))
        self.sorted.add((x, self.id))
        self.id += 1

    def pop(self) -> int:
        while self.stack[-1][1] in self.removed:
            self.stack.pop()
        val, idx = self.stack.pop()
        self.removed.add(idx)
        return val

    def top(self) -> int:
        while self.stack[-1][1] in self.removed:
            self.stack.pop()
        return self.stack[-1][0]

    def peekMax(self) -> int:
        while self.sorted[-1][1] in self.removed:
            self.sorted.pop()
        return self.sorted[-1][0]

    def popMax(self) -> int:
        while self.sorted[-1][1] in self.removed:
            self.sorted.pop()
        val, idx = self.sorted.pop()
        self.removed.add(idx)
        return val
```

### Implement Queue using Stacks
```python
class MyQueue:
    """
    Queue using two stacks.

    Time: O(1) amortized for all operations
    """
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def pop(self) -> int:
        self._transfer()
        return self.out_stack.pop()

    def peek(self) -> int:
        self._transfer()
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack

    def _transfer(self) -> None:
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
```

### Design Circular Queue
```python
class MyCircularQueue:
    """
    Fixed-size circular queue using array.
    """
    def __init__(self, k: int):
        self.queue = [0] * k
        self.size = k
        self.front = 0
        self.rear = -1
        self.count = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = value
        self.count += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.front = (self.front + 1) % self.size
        self.count -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.queue[self.front]

    def Rear(self) -> int:
        return -1 if self.isEmpty() else self.queue[self.rear]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == self.size
```

## Related Problems

- **Max Stack** - Similar with popMax operation
- **Implement Queue using Stacks** - Stack to queue conversion
- **Implement Stack using Queues** - Queue to stack conversion
- **Design Circular Queue** - Fixed-size queue
- **Stock Span Problem** - Uses stack for tracking
