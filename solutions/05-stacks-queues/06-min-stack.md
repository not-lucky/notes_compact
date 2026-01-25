# Min Stack - Practice Solutions

This file provides optimal Python solutions and explanations for the practice problems listed in the Min Stack notes.

## 1. Min Stack
**Problem Statement**: Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

### Examples & Edge Cases
- **Example**: `push(-2), push(0), push(-3), getMin() -> -3, pop(), top() -> 0, getMin() -> -2`
- **Edge Case**: Pop from a stack with one element.
- **Edge Case**: Multiple elements with the same minimum value.

### Optimal Python Solution
```python
class MinStack:
    def __init__(self):
        # Main stack to store all values
        self.stack = []
        # Auxiliary stack to store minimum values
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Only push to min_stack if it's empty or val is new minimum (or equal)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        # If the value being popped is the current minimum, pop it from min_stack too
        if self.stack.pop() == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

### Explanation
We maintain two stacks. The `stack` stores all elements normally. The `min_stack` stores the minimum value seen so far. By using `<=` in the push condition, we handle duplicate minimum values correctly (e.g., pushing `[1, 1, 1]`). When we pop, we check if the element removed was the current minimum; if so, we also pop from `min_stack` to reveal the previous minimum.

### Complexity Analysis
- **Time Complexity**: O(1) for all operations: `push`, `pop`, `top`, `getMin`.
- **Space Complexity**: O(n), where n is the number of elements pushed. In the worst case (strictly decreasing values), `min_stack` stores n elements.

---

## 2. Max Stack
**Problem Statement**: Design a stack that supports `push`, `pop`, `top`, `peekMax`, and `popMax`. `popMax` removes the maximum element from the stack and returns it. If there are multiple maximum elements, only remove the top-most one.

### Optimal Python Solution (O(log n) popMax)
```python
import heapq

class MaxStack:
    def __init__(self):
        self.stack = [] # (value, id)
        self.heap = [] # (-value, -id) for max heap
        self.removed = set() # ids of removed elements
        self.id = 0

    def push(self, x: int) -> None:
        self.stack.append((x, self.id))
        heapq.heappush(self.heap, (-x, -self.id))
        self.id += 1

    def _cleanup(self):
        # Remove elements from stack top that were popped via popMax
        while self.stack and self.stack[-1][1] in self.removed:
            self.stack.pop()
        # Remove elements from heap top that were popped via pop
        while self.heap and -self.heap[0][1] in self.removed:
            heapq.heappop(self.heap)

    def pop(self) -> int:
        self._cleanup()
        val, id = self.stack.pop()
        self.removed.add(id)
        return val

    def top(self) -> int:
        self._cleanup()
        return self.stack[-1][0]

    def peekMax(self) -> int:
        self._cleanup()
        return -self.heap[0][0]

    def popMax(self) -> int:
        self._cleanup()
        val_neg, id_neg = heapq.heappop(self.heap)
        self.removed.add(-id_neg)
        return -val_neg
```

### Explanation
To support `popMax` efficiently, we use a combination of a stack, a max-heap, and lazy deletion. Each element is assigned a unique `id`. When an element is removed (either via `pop` or `popMax`), its `id` is added to a `removed` set. Before any operation, we "clean up" the tops of the stack and heap to ensure they reflect valid, non-removed elements.

---

## 3. Implement Stack using Queues
**Problem Statement**: Implement a last-in-first-out (LIFO) stack using only two queues.

### Optimal Python Solution
```python
from collections import deque

class MyStack:
    def __init__(self):
        self.queue = deque()

    def push(self, x: int) -> None:
        self.queue.append(x)
        # Rotate the queue to put the new element at the front
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())

    def pop(self) -> int:
        return self.queue.popleft()

    def top(self) -> int:
        return self.queue[0]

    def empty(self) -> bool:
        return not self.queue
```

### Complexity Analysis
- **Time Complexity**: `push`: O(n), `pop`: O(1), `top`: O(1).
- **Space Complexity**: O(n).

---

## 4. Design a Stack With Increment Operation
**Problem Statement**: Design a stack that supports `push`, `pop`, and `increment(k, val)`. `increment` adds `val` to the bottom `k` elements of the stack.

### Optimal Python Solution
```python
class CustomStack:
    def __init__(self, maxSize: int):
        self.stack = []
        self.inc = [] # Stores increments to be applied
        self.maxSize = maxSize

    def push(self, x: int) -> None:
        if len(self.stack) < self.maxSize:
            self.stack.append(x)
            self.inc.append(0)

    def pop(self) -> int:
        if not self.stack: return -1
        # Apply increment and pass it down to the element below
        idx = len(self.stack) - 1
        if idx > 0:
            self.inc[idx - 1] += self.inc[idx]

        res = self.stack.pop() + self.inc.pop()
        return res

    def increment(self, k: int, val: int) -> None:
        # We only need to store the increment at the k-th element
        idx = min(k, len(self.stack)) - 1
        if idx >= 0:
            self.inc[idx] += val
```

### Explanation
We use lazy propagation. Instead of incrementing all `k` elements (which would be O(k)), we only store the increment at the `k-th` index. When we pop an element, we add its increment and "pass down" that increment to the next element below it.

---

## 5. Maximum Frequency Stack
**Problem Statement**: Design a stack that returns the most frequent element. If there's a tie, return the one closest to the stack's top.

### Optimal Python Solution
```python
from collections import Counter, defaultdict

class FreqStack:
    def __init__(self):
        self.freq = Counter() # element -> frequency
        self.group = defaultdict(list) # frequency -> list of elements
        self.max_freq = 0

    def push(self, val: int) -> None:
        f = self.freq[val] + 1
        self.freq[val] = f
        if f > self.max_freq:
            self.max_freq = f
        self.group[f].append(val)

    def pop(self) -> int:
        # Get element from the highest frequency group
        val = self.group[self.max_freq].pop()
        self.freq[val] -= 1
        if not self.group[self.max_freq]:
            self.max_freq -= 1
        return val
```
