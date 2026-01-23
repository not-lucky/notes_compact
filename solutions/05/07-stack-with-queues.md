# Implement Stack Using Queues

## Practice Problems

### 1. Implement Stack using Queues (Push Costly)
**Difficulty:** Easy
**Key Technique:** One queue + Rotation

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

### 2. Implement Stack using Queues (Pop Costly)
**Difficulty:** Easy
**Key Technique:** Two queues

```python
from collections import deque

class MyStackPopCostly:
    """
    Time: O(1) push, O(n) pop
    Space: O(n)
    """
    def __init__(self):
        self.q1 = deque()
        self.q2 = deque()

    def push(self, x: int) -> None:
        self.q1.append(x)

    def pop(self) -> int:
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())
        res = self.q1.popleft()
        self.q1, self.q2 = self.q2, self.q1
        return res

    def top(self) -> int:
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())
        res = self.q1[0]
        self.q2.append(self.q1.popleft())
        self.q1, self.q2 = self.q2, self.q1
        return res

    def empty(self) -> bool:
        return not self.q1
```
