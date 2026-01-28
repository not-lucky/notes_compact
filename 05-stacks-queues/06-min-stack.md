# Min Stack

> **Prerequisites:** [01-stack-basics](./01-stack-basics.md)

## Overview

The Min Stack problem asks you to design a stack that supports push, pop, top, and retrieving the minimum element—all in O(1) time. The key insight is that we can trade space for time by tracking the minimum at each "level" of the stack, since the minimum only changes when we push or pop.

## Building Intuition

**Why is tracking the minimum hard?**

In a normal stack, finding the minimum requires scanning all elements—O(n). The challenge is maintaining O(1) access to the minimum as elements come and go.

**The Key Insight**:

```
The minimum of a stack only depends on what's currently in the stack.
If we know the minimum when there are k elements, and we pop one,
the minimum of the remaining k-1 elements is what it was before we
pushed that element.

We can "remember" the minimum at each stack level!
```

**Why an Auxiliary Stack Works**:

Imagine we push elements 3, 2, 5, 1:

```
Main stack:    Min stack:
[3]            [3]         ← min is 3
[3,2]          [3,2]       ← min is 2
[3,2,5]        [3,2,2]     ← min is still 2 (5 didn't change it)
[3,2,5,1]      [3,2,2,1]   ← min is 1

If we pop 1:
[3,2,5]        [3,2,2]     ← min is back to 2 (from min_stack top)
```

The min_stack tracks "what was the minimum at this stack height?" When we pop, both stacks shrink together, and the min_stack top is always the current minimum.

**Why NOT Just Track a Single Min Variable?**

Single variable fails on pop:

```
Push 3: min = 3
Push 2: min = 2
Push 1: min = 1
Pop 1:  min = ??? (we forgot that 2 was the previous min!)
```

By tracking min at each level, we never "forget" previous minimums.

**Space Optimization Intuition**:

If we push 5, 4, 3, 2, 1, each is a new minimum → min_stack = [5,4,3,2,1].
But if we push 1, 2, 3, 4, 5, only 1 is ever a minimum → min_stack = [1,1,1,1,1].

The optimized version only pushes to min_stack when the value is ≤ current min, saving space when values are mostly increasing.

## When NOT to Use This Pattern

The auxiliary stack pattern is wrong when:

1. **Need Other Statistics**: If you need median, mode, or percentiles (not just min/max), you need different structures like balanced BSTs or multiple heaps.

2. **Memory is Critical**: The auxiliary stack doubles memory usage. In memory-constrained environments, the mathematical encoding trick (storing differences) uses O(1) extra space.

3. **Need to Pop Specific Values**: If you need `popMin()` or `popMax()` (remove the min/max element wherever it is), you need sorted structures like balanced BSTs with lazy deletion.

4. **Queue Instead of Stack**: For a min queue, you need a monotonic deque instead, since FIFO ordering changes which elements can be removed.

5. **Multiple Data Structures Share Min**: If multiple containers need a shared minimum, consider a global priority queue instead.

**Alternatives by Use Case**:
| Need | Structure |
|------|-----------|
| Min/Max of stack | Auxiliary stack |
| Min/Max of queue | Monotonic deque |
| PopMin/PopMax | Sorted list or heap |
| Median | Two heaps |
| kth smallest | Balanced BST or order statistic tree |

## Interview Context

The Min Stack problem is a **classic design question** at FANG+ companies because:

1. **Data structure design**: Tests ability to augment standard structures
2. **Space-time tradeoffs**: Multiple valid solutions with different tradeoffs
3. **Invariant maintenance**: Keep min updated through push/pop operations
4. **Follow-up potential**: "What about getMax?", "What about constant space?"

Interviewers use this to assess your understanding of auxiliary data structures and design thinking.

---

## The Problem

Design a stack that supports:

- `push(x)` — Push element x onto stack
- `pop()` — Remove top element
- `top()` — Get top element
- `getMin()` — Retrieve minimum element

**Constraint**: All operations must be O(1) time complexity.

```
Example:
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   // Returns -3
minStack.pop();
minStack.getMin();   // Returns -2
minStack.top();      // Returns 0
```

---

## Approach Comparison

| Approach                | push | pop  | getMin  | Space  |
| ----------------------- | ---- | ---- | ------- | ------ |
| Brute force (scan)      | O(1) | O(1) | O(n) ❌ | O(n)   |
| Two stacks              | O(1) | O(1) | O(1) ✓  | O(n)   |
| Single stack with pairs | O(1) | O(1) | O(1) ✓  | O(n)   |
| Single stack optimized  | O(1) | O(1) | O(1) ✓  | O(n)\* |

\*Better space in practice for many duplicates

---

## Solution 1: Two Stacks (Clearest)

```python
class MinStack:
    """
    Min stack using auxiliary stack to track minimums.

    Time: O(1) for all operations
    Space: O(n) for main stack + O(n) for min stack
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []  # Parallel stack tracking min at each level

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Push current min (or val if stack was empty)
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]


# Walkthrough
# push(-2): stack=[-2], min_stack=[-2]
# push(0):  stack=[-2,0], min_stack=[-2,-2]
# push(-3): stack=[-2,0,-3], min_stack=[-2,-2,-3]
# getMin(): min_stack[-1] = -3
# pop():    stack=[-2,0], min_stack=[-2,-2]
# getMin(): min_stack[-1] = -2
```

---

## Solution 2: Single Stack with Pairs

```python
class MinStack:
    """
    Store (value, current_min) pairs in single stack.

    Time: O(1) for all operations
    Space: O(n) - 2 values per element
    """
    def __init__(self):
        self.stack = []  # List of (value, min_at_this_level)

    def push(self, val: int) -> None:
        if self.stack:
            current_min = min(val, self.stack[-1][1])
        else:
            current_min = val
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
```

---

## Solution 3: Optimized Min Stack (Store Min Only When Changes)

```python
class MinStack:
    """
    Only push to min_stack when min changes.

    Time: O(1) for all operations
    Space: O(n) worst case, but often better
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Only push if val is new minimum (or equal)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        val = self.stack.pop()
        # Only pop from min_stack if we're removing the current min
        if val == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]


# Note: We use <= instead of < to handle duplicates
# push(1): stack=[1], min_stack=[1]
# push(1): stack=[1,1], min_stack=[1,1]  (need both!)
# pop():   stack=[1], min_stack=[1]      (correct min remains)
```

---

## Solution 4: Space-Optimized (Mathematical Trick)

```python
class MinStack:
    """
    O(1) extra space using mathematical encoding.

    Stores difference between value and min.

    Time: O(1) for all operations
    Space: O(n) for stack, O(1) extra
    """
    def __init__(self):
        self.stack = []
        self.min_val = None

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append(0)
            self.min_val = val
        else:
            # Store difference from current min
            diff = val - self.min_val
            self.stack.append(diff)
            if diff < 0:
                self.min_val = val  # New minimum

    def pop(self) -> None:
        diff = self.stack.pop()
        if diff < 0:
            # We're popping the min, recover previous min
            self.min_val = self.min_val - diff
        if not self.stack:
            self.min_val = None

    def top(self) -> int:
        diff = self.stack[-1]
        if diff < 0:
            return self.min_val  # Top is current min
        return self.min_val + diff

    def getMin(self) -> int:
        return self.min_val


# How it works:
# If we store diff = val - min:
#   - If diff >= 0: val >= min, so val = min + diff
#   - If diff < 0: val < min, so val becomes new min
#     Previous min = new_min - diff (since diff = new_min - old_min)
```

---

## Max Stack

Same idea, just track maximum instead.

```python
class MaxStack:
    """
    Stack with O(1) getMax.
    """
    def __init__(self):
        self.stack = []
        self.max_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if self.max_stack:
            self.max_stack.append(max(val, self.max_stack[-1]))
        else:
            self.max_stack.append(val)

    def pop(self) -> int:
        self.max_stack.pop()
        return self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMax(self) -> int:
        return self.max_stack[-1]
```

---

## Max Stack with popMax (Harder)

```python
from sortedcontainers import SortedList

class MaxStackWithPopMax:
    """
    Stack supporting popMax operation.

    LeetCode 716: Max Stack

    Uses doubly linked list + sorted structure.

    Time: O(log n) for push, pop, popMax
    Space: O(n)
    """
    def __init__(self):
        self.stack = []  # List of (value, id)
        self.sorted_vals = SortedList()  # (value, id) sorted
        self.counter = 0
        self.deleted = set()  # Lazy deletion

    def push(self, x: int) -> None:
        self.stack.append((x, self.counter))
        self.sorted_vals.add((x, self.counter))
        self.counter += 1

    def _clean_top(self):
        """Remove deleted items from stack top."""
        while self.stack and self.stack[-1][1] in self.deleted:
            self.stack.pop()

    def pop(self) -> int:
        self._clean_top()
        val, idx = self.stack.pop()
        self.deleted.add(idx)
        return val

    def top(self) -> int:
        self._clean_top()
        return self.stack[-1][0]

    def peekMax(self) -> int:
        while self.sorted_vals and self.sorted_vals[-1][1] in self.deleted:
            self.sorted_vals.pop()
        return self.sorted_vals[-1][0]

    def popMax(self) -> int:
        while self.sorted_vals[-1][1] in self.deleted:
            self.sorted_vals.pop()
        val, idx = self.sorted_vals.pop()
        self.deleted.add(idx)
        return val
```

---

## Min Queue

Same concept applied to queue.

```python
from collections import deque

class MinQueue:
    """
    Queue with O(1) getMin using monotonic deque.

    Time: O(1) amortized for all operations
    Space: O(n)
    """
    def __init__(self):
        self.queue = deque()
        self.min_deque = deque()  # Monotonic increasing

    def enqueue(self, val: int) -> None:
        self.queue.append(val)
        # Maintain monotonic increasing
        while self.min_deque and self.min_deque[-1] > val:
            self.min_deque.pop()
        self.min_deque.append(val)

    def dequeue(self) -> int:
        val = self.queue.popleft()
        if val == self.min_deque[0]:
            self.min_deque.popleft()
        return val

    def front(self) -> int:
        return self.queue[0]

    def getMin(self) -> int:
        return self.min_deque[0]
```

---

## Complexity Summary

| Operation | Two Stacks | Pairs | Optimized | Math Trick |
| --------- | ---------- | ----- | --------- | ---------- |
| push      | O(1)       | O(1)  | O(1)      | O(1)       |
| pop       | O(1)       | O(1)  | O(1)      | O(1)       |
| top       | O(1)       | O(1)  | O(1)      | O(1)       |
| getMin    | O(1)       | O(1)  | O(1)      | O(1)       |
| Space     | 2n         | 2n    | n to 2n   | n + O(1)   |

---

## Visual Comparison

```
Two Stacks Approach:

push(-2):  stack: [-2]           min_stack: [-2]
push(0):   stack: [-2, 0]        min_stack: [-2, -2]
push(-3):  stack: [-2, 0, -3]    min_stack: [-2, -2, -3]
                         ↑                            ↑
                        top                          min


Single Stack with Pairs:

push(-2):  stack: [(-2, -2)]
push(0):   stack: [(-2, -2), (0, -2)]
push(-3):  stack: [(-2, -2), (0, -2), (-3, -3)]
                                        ↑     ↑
                                       val   min
```

---

## Edge Cases

```python
# 1. Single element
ms = MinStack()
ms.push(5)
ms.getMin()  # 5
ms.pop()
# Now empty - calling getMin() would error

# 2. All same values
ms = MinStack()
ms.push(1)
ms.push(1)
ms.push(1)
ms.pop()
ms.getMin()  # Still 1

# 3. Strictly decreasing sequence
ms.push(3)  # min = 3
ms.push(2)  # min = 2
ms.push(1)  # min = 1
# Optimized version: min_stack = [3, 2, 1]

# 4. Strictly increasing sequence
ms.push(1)  # min = 1
ms.push(2)  # min = 1
ms.push(3)  # min = 1
# Optimized version: min_stack = [1] (space saved!)
```

---

## Interview Tips

1. **Start with two stacks**: Clearest to explain and implement
2. **Mention optimization**: Shows awareness of space-time tradeoffs
3. **Handle duplicates**: Critical for the optimized version
4. **Discuss the math trick**: Shows deep understanding (if asked about O(1) space)

---

## Practice Problems

| #   | Problem                                 | Difficulty | Key Concept           |
| --- | --------------------------------------- | ---------- | --------------------- |
| 1   | Min Stack                               | Medium     | Core pattern          |
| 2   | Max Stack                               | Hard       | With popMax operation |
| 3   | Implement Stack using Queues            | Easy       | Related design        |
| 4   | Design a Stack With Increment Operation | Medium     | Modified stack        |
| 5   | Maximum Frequency Stack                 | Hard       | Stack + frequency     |

---

## Key Takeaways

1. **Auxiliary stack**: Track min at each level for O(1) getMin
2. **Space optimization**: Only store when min changes
3. **Handle duplicates**: Use `<=` not `<` in optimized version
4. **Math trick**: Encode information in differences for O(1) extra space
5. **Same pattern for max**: Just flip the comparisons

---

## Next: [07-stack-with-queues.md](./07-stack-with-queues.md)

Learn how to implement a stack using only queue operations.
