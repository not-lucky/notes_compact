# Solution: Min Stack Practice Problems

## Problem 1: Min Stack
### Problem Statement
Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the `MinStack` class:
- `MinStack()` initializes the stack object.
- `void push(int val)` pushes the element `val` onto the stack.
- `void pop()` removes the element on the top of the stack.
- `int top()` gets the top element of the stack.
- `int getMin()` retrieves the minimum element in the stack.

You must implement a solution with `O(1)` time complexity for each function.

### Constraints
- `-2^31 <= val <= 2^31 - 1`
- Methods `pop`, `top` and `getMin` operations will always be called on non-empty stacks.
- At most `3 * 10^4` calls will be made to `push`, `pop`, `top`, and `getMin`.

### Example
Input: `["MinStack","push","push","push","getMin","pop","top","getMin"]`, `[[],[-2],[0],[-3],[],[],[],[]]`
Output: `[null,null,null,null,-3,null,0,-2]`

### Python Implementation
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        if self.stack.pop() == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

---

## Problem 2: Max Stack
### Problem Statement
Design a stack that supports push, pop, top, peekMax, and popMax.

- `push(x)`: Push element `x` onto stack.
- `pop()`: Remove the element on the top of the stack and return it.
- `top()`: Get the element on the top.
- `peekMax()`: Retrieve the maximum element in the stack.
- `popMax()`: Retrieve the maximum element in the stack, and remove it. If you find more than one maximum elements, only remove the top-most one.

### Constraints
- `-10^7 <= x <= 10^7`
- At most `10^4` calls will be made to `push`, `pop`, `top`, `peekMax`, and `popMax`.
- There will be at least one element in the stack when `pop`, `top`, `peekMax`, or `popMax` is called.

### Example
Input: `["MaxStack", "push", "push", "push", "top", "popMax", "top", "peekMax", "pop", "top"]`, `[[], [5], [1], [5], [], [], [], [], [], []]`
Output: `[null, null, null, null, 5, 5, 1, 5, 1, 5]`

### Python Implementation
```python
class MaxStack:
    def __init__(self):
        self.stack = []

    def push(self, x: int) -> None:
        self.stack.append(x)

    def pop(self) -> int:
        return self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def peekMax(self) -> int:
        return max(self.stack)

    def popMax(self) -> int:
        m = max(self.stack)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i] == m:
                return self.stack.pop(i)
```

Note: A more efficient implementation of `popMax` would use a combination of a doubly linked list and a TreeMap/PriorityQueue for $O(\log n)$ operations. The above is a simple $O(n)$ version.

---

## Problem 3: Maximum Frequency Stack
### Problem Statement
Design a stack-like data structure to push elements to the stack and pop the most frequent element from the stack.

Implement the `FreqStack` class:
- `FreqStack()` constructs an empty frequency stack.
- `void push(int val)` pushes an integer `val` onto the top of the stack.
- `int pop()` removes and returns the most frequent element in the stack.
  - If there is a tie for the most frequent element, the element closest to the stack's top is removed and returned.

### Constraints
- `0 <= val <= 10^9`
- At most `2 * 10^4` calls will be made to `push` and `pop`.
- It is guaranteed that there will be at least one element in the stack before calling `pop`.

### Example
Input: `["FreqStack", "push", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop"]`, `[[], [5], [7], [5], [7], [4], [5], [], [], [], []]`
Output: `[null, null, null, null, null, null, null, 5, 7, 5, 4]`

### Python Implementation
```python
from collections import Counter

class FreqStack:
    def __init__(self):
        self.freq = Counter()
        self.group = {} # frequency -> stack of elements
        self.max_freq = 0

    def push(self, val: int) -> None:
        f = self.freq[val] + 1
        self.freq[val] = f
        if f > self.max_freq:
            self.max_freq = f

        if f not in self.group:
            self.group[f] = []
        self.group[f].append(val)

    def pop(self) -> int:
        val = self.group[self.max_freq].pop()
        self.freq[val] -= 1
        if not self.group[self.max_freq]:
            self.max_freq -= 1
        return val
```
