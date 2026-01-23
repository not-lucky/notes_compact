# Solution: Implement Stack Using Queues Practice Problems

## Problem 1: Implement Stack using Queues
### Problem Statement
Implement a last-in-first-out (LIFO) stack using only two queues. The implemented stack should support all the functions of a normal stack (`push`, `top`, `pop`, and `empty`).

Implement the `MyStack` class:
- `void push(int x)` Pushes element x onto the stack.
- `int pop()` Removes the element on the top of the stack and returns it.
- `int top()` Returns the element on the top of the stack.
- `boolean empty()` Returns `true` if the stack is empty, `false` otherwise.

Notes:
- You must use only standard operations of a queue, which means `push to back`, `peek/pop from front`, `size` and `is empty` operations are valid.
- Depending on your language, the queue may not be supported natively. You may simulate a queue using a list or deque (double-ended queue) as long as you use only a queue's standard operations.

### Constraints
- `1 <= x <= 9`
- At most `100` calls will be made to `push`, `pop`, `top`, and `empty`.
- All the calls to `pop` and `top` are valid.

### Example
Input: `["MyStack", "push", "push", "top", "pop", "empty"]`, `[[], [1], [2], [], [], []]`
Output: `[null, null, null, 2, 2, false]`

### Python Implementation
```python
from collections import deque

class MyStack:
    def __init__(self):
        self.queue = deque()

    def push(self, x: int) -> None:
        self.queue.append(x)
        # Rotate the queue to make the newly added element the front
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())

    def pop(self) -> int:
        return self.queue.popleft()

    def top(self) -> int:
        return self.queue[0]

    def empty(self) -> bool:
        return not self.queue
```

---

## Problem 2: Design Front Middle Back Queue
### Problem Statement
Design a queue that supports `push` and `pop` operations in the front, middle, and back.

Implement the `FrontMiddleBackQueue` class:
- `FrontMiddleBackQueue()` Initializes the queue.
- `void pushFront(int val)` Adds `val` to the front of the queue.
- `void pushMiddle(int val)` Adds `val` to the middle of the queue.
- `void pushBack(int val)` Adds `val` to the back of the queue.
- `int popFront()` Removes the front element of the queue and returns it. If the queue is empty, return -1.
- `int popMiddle()` Removes the middle element of the queue and returns it. If the queue is empty, return -1.
- `int popBack()` Removes the back element of the queue and returns it. If the queue is empty, return -1.

Notice that when there are two middle position choices, the operation is performed on the front-most middle position choice. For example:
- Pushing 6 into `[1, 2, 3, 4, 5]` results in `[1, 2, 6, 3, 4, 5]`.
- Popping the middle from `[1, 2, 3, 4, 5, 6]` results in `[1, 2, 4, 5, 6]` and returns 3.

### Constraints
- `1 <= val <= 10^9`
- At most `1000` calls will be made to `pushFront`, `pushMiddle`, `pushBack`, `popFront`, `popMiddle`, and `popBack`.

### Example
Input: `["FrontMiddleBackQueue", "pushFront", "pushBack", "pushMiddle", "pushMiddle", "popFront", "popMiddle", "popMiddle", "popBack", "popFront"]`, `[[], [1], [2], [3], [4], [], [], [], [], []]`
Output: `[null, null, null, null, null, 1, 3, 4, 2, -1]`

### Python Implementation
```python
from collections import deque

class FrontMiddleBackQueue:
    def __init__(self):
        self.left = deque()
        self.right = deque()

    def pushFront(self, val: int) -> None:
        self.left.appendleft(val)
        self._balance()

    def pushMiddle(self, val: int) -> None:
        if len(self.left) > len(self.right):
            self.right.appendleft(self.left.pop())
        self.left.append(val)

    def pushBack(self, val: int) -> None:
        self.right.append(val)
        self._balance()

    def popFront(self) -> int:
        if not self.left and not self.right:
            return -1
        res = self.left.popleft() if self.left else self.right.popleft()
        self._balance()
        return res

    def popMiddle(self) -> int:
        if not self.left and not self.right:
            return -1
        if len(self.left) == len(self.right):
            res = self.left.pop()
        else:
            res = self.left.pop() if len(self.left) > len(self.right) else self.right.popleft()
        self._balance()
        return res

    def popBack(self) -> int:
        if not self.left and not self.right:
            return -1
        res = self.right.pop() if self.right else self.left.pop()
        self._balance()
        return res

    def _balance(self):
        if len(self.left) > len(self.right) + 1:
            self.right.appendleft(self.left.pop())
        elif len(self.right) > len(self.left):
            self.left.append(self.right.popleft())
```
