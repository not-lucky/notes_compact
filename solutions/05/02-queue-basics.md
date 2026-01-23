# Queue Basics

## Practice Problems

### 1. Design Circular Queue
**Difficulty:** Medium
**Key Technique:** Array + Modulo arithmetic

```python
class MyCircularQueue:
    """
    Time: O(1) for all operations
    Space: O(k)
    """
    def __init__(self, k: int):
        self.q = [0] * k
        self.head = 0
        self.count = 0
        self.capacity = k

    def enQueue(self, value: int) -> bool:
        if self.isFull(): return False
        self.q[(self.head + self.count) % self.capacity] = value
        self.count += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty(): return False
        self.head = (self.head + 1) % self.capacity
        self.count -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.q[self.head]

    def Rear(self) -> int:
        return -1 if self.isEmpty() else self.q[(self.head + self.count - 1) % self.capacity]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == self.capacity
```

### 2. Number of Recent Calls
**Difficulty:** Easy
**Key Technique:** Queue for sliding window

```python
from collections import deque

class RecentCounter:
    """
    Time: O(1) amortized
    Space: O(W) where W is window size
    """
    def __init__(self):
        self.q = deque()

    def ping(self, t: int) -> int:
        self.q.append(t)
        while self.q[0] < t - 3000:
            self.q.popleft()
        return len(self.q)
```

### 3. Implement Stack using Queues
**Difficulty:** Easy
**Key Technique:** One queue + rotation

```python
from collections import deque

class MyStack:
    """
    Time: O(n) push, O(1) pop
    Space: O(n)
    """
    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return not self.q
```

### 4. Implement Queue using Stacks
**Difficulty:** Easy
**Key Technique:** Two stacks (in and out)

```python
class MyQueue:
    """
    Time: O(1) amortized
    Space: O(n)
    """
    def __init__(self):
        self.s1 = [] # in
        self.s2 = [] # out

    def push(self, x: int) -> None:
        self.s1.append(x)

    def pop(self) -> int:
        self.peek()
        return self.s2.pop()

    def peek(self) -> int:
        if not self.s2:
            while self.s1:
                self.s2.append(self.s1.pop())
        return self.s2[-1]

    def empty(self) -> bool:
        return not self.s1 and not self.s2
```
