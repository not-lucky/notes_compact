# Solution: Queue Basics Practice Problems

## Problem 1: Design Circular Queue
### Problem Statement
Design your implementation of the circular queue. The circular queue is a linear data structure in which the operations are performed based on FIFO (First In First Out) principle and the last position is connected back to the first position to make a circle. It is also called "Ring Buffer".

Implement the `MyCircularQueue` class:
- `MyCircularQueue(k)` Initializes the object with the size of the queue to be `k`.
- `Front()` Gets the front item from the queue. If the queue is empty, return -1.
- `Rear()` Gets the last item from the queue. If the queue is empty, return -1.
- `enQueue(value)` Inserts an element into the circular queue. Return true if the operation is successful.
- `deQueue()` Deletes an element from the circular queue. Return true if the operation is successful.
- `isEmpty()` Checks whether the circular queue is empty or not.
- `isFull()` Checks whether the circular queue is full or not.

### Constraints
- `1 <= k <= 1000`
- `0 <= value <= 1000`
- At most `3000` calls will be made to `enQueue`, `deQueue`, `Front`, `Rear`, `isEmpty`, and `isFull`.

### Example
Input: `["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "Rear", "isFull", "deQueue", "enQueue", "Rear"]`, `[[3], [1], [2], [3], [4], [], [], [], [4], []]`
Output: `[null, true, true, true, false, 3, true, true, true, 4]`

### Python Implementation
```python
class MyCircularQueue:
    def __init__(self, k: int):
        self.queue = [None] * k
        self.capacity = k
        self.size = 0
        self.front = 0
        self.rear = -1

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = value
        self.size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.queue[self.front]

    def Rear(self) -> int:
        return -1 if self.isEmpty() else self.queue[self.rear]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity
```

---

## Problem 2: Number of Recent Calls
### Problem Statement
You have a `RecentCounter` class which counts the number of recent requests within a certain time frame.

Implement the `RecentCounter` class:
- `RecentCounter()` Initializes the counter with zero recent requests.
- `ping(int t)` Adds a new request at time `t`, where `t` represents some time in milliseconds, and returns the number of requests that has happened in the past 3000 milliseconds (including the new request). Specifically, return the number of requests that have happened in the inclusive range `[t - 3000, t]`.

It is guaranteed that every call to `ping` uses a strictly increasing value of `t`.

### Constraints
- `1 <= t <= 10^9`
- Each test case will call `ping` with strictly increasing values of `t`.
- At most `10^4` calls will be made to `ping`.

### Example
Input: `["RecentCounter", "ping", "ping", "ping", "ping"]`, `[[], [1], [100], [3001], [3002]]`
Output: `[null, 1, 2, 3, 3]`

### Python Implementation
```python
from collections import deque

class RecentCounter:
    def __init__(self):
        self.requests = deque()

    def ping(self, t: int) -> int:
        self.requests.append(t)
        while self.requests[0] < t - 3000:
            self.requests.popleft()
        return len(self.requests)
```

---

## Problem 3: Moving Average from Data Stream
### Problem Statement
Given a stream of integers and a window size, calculate the moving average of all integers in the sliding window.

Implement the `MovingAverage` class:
- `MovingAverage(size)` Initializes the object with the size of the window `size`.
- `next(val)` Returns the moving average of the last `size` values of the stream.

### Constraints
- `1 <= size <= 1000`
- `-10^5 <= val <= 10^5`
- At most `10^4` calls will be made to `next`.

### Example
Input: `["MovingAverage", "next", "next", "next", "next"]`, `[[3], [1], [10], [3], [5]]`
Output: `[null, 1.0, 5.5, 4.66667, 6.0]`

### Python Implementation
```python
from collections import deque

class MovingAverage:
    def __init__(self, size: int):
        self.size = size
        self.queue = deque()
        self.sum = 0

    def next(self, val: int) -> float:
        self.sum += val
        self.queue.append(val)
        if len(self.queue) > self.size:
            self.sum -= self.queue.popleft()
        return self.sum / len(self.queue)
```

---

## Problem 4: Implement Queue using Stacks
### Problem Statement
Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (`push`, `peek`, `pop`, and `empty`).

Implement the `MyQueue` class:
- `void push(int x)` Pushes element x to the back of the queue.
- `int pop()` Removes the element from the front of the queue and returns it.
- `int peek()` Returns the element at the front of the queue.
- `boolean empty()` Returns `true` if the queue is empty, `false` otherwise.

Notes:
- You must use only standard operations of a stack, which means only `push to top`, `peek/pop from top`, `size`, and `is empty` operations are valid.
- Depending on your language, the stack may not be supported natively. You may simulate a stack using a list or deque (double-ended queue) as long as you use only a stack's standard operations.

### Constraints
- `1 <= x <= 9`
- At most `100` calls will be made to `push`, `pop`, `peek`, and `empty`.
- All the calls to `pop` and `peek` are valid.

### Example
Input: `["MyQueue", "push", "push", "peek", "pop", "empty"]`, `[[], [1], [2], [], [], []]`
Output: `[null, null, null, 1, 1, false]`

### Python Implementation
```python
class MyQueue:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def pop(self) -> int:
        self.peek()
        return self.out_stack.pop()

    def peek(self) -> int:
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack
```
