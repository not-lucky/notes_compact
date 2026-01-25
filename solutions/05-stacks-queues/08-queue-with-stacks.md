# Implement Queue Using Stacks - Practice Solutions

This file provides optimal Python solutions and explanations for the practice problems listed in the Implement Queue Using Stacks notes.

## 1. Implement Queue using Stacks (Amortized O(1))
**Problem Statement**: Implement a first-in-first-out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (`push`, `peek`, `pop`, and `empty`).

### Examples & Edge Cases
- **Example**: `push(1), push(2), peek() -> 1, pop() -> 1, empty() -> False`
- **Edge Case**: `pop()` or `peek()` called on an empty queue (handled by constraints in most problems).
- **Edge Case**: Interleaved `push` and `pop` operations.

### Optimal Python Solution
```python
class MyQueue:
    def __init__(self):
        # s1: Input stack - used for push operations
        self.s1 = []
        # s2: Output stack - used for pop and peek operations
        self.s2 = []

    def push(self, x: int) -> None:
        """
        Push element x to the back of queue.
        Complexity: O(1)
        """
        self.s1.append(x)

    def pop(self) -> int:
        """
        Removes the element from in front of queue and returns it.
        Complexity: O(1) Amortized
        """
        self._transfer()
        return self.s2.pop()

    def peek(self) -> int:
        """
        Get the front element.
        Complexity: O(1) Amortized
        """
        self._transfer()
        return self.s2[-1]

    def empty(self) -> bool:
        """
        Returns whether the queue is empty.
        Complexity: O(1)
        """
        return not self.s1 and not self.s2

    def _transfer(self):
        """
        Helper method to transfer elements from s1 to s2.
        We only transfer when s2 is empty to maintain FIFO order.
        """
        if not self.s2:
            while self.s1:
                self.s2.append(self.s1.pop())
```

### Explanation
We use two stacks to reverse the "Last-In-First-Out" order twice, which results in "First-In-First-Out" order.
1. New elements are always pushed onto `s1`.
2. To `pop` or `peek` the front of the queue, we need the oldest element.
3. If `s2` is empty, we transfer all elements from `s1` to `s2`. This flips the order such that the oldest element in `s1` (bottom) becomes the newest element in `s2` (top).
4. If `s2` is not empty, we simply pop/peek from `s2`.

### Complexity Analysis
- **Time Complexity**:
    - `push`: O(1).
    - `pop`: O(1) amortized. While a single `pop` might trigger an O(n) transfer, each element is moved from `s1` to `s2` exactly once. Across n operations, the total work is O(n), giving O(1) per operation.
    - `peek`: O(1) amortized.
    - `empty`: O(1).
- **Space Complexity**: O(n), to store the elements in the stacks.

---

## 2. Implement Stack using Queues
**Problem Statement**: Implement a last-in-first-out (LIFO) stack using only two queues.

### Optimal Python Solution
```python
from collections import deque

class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        """
        Complexity: O(n)
        """
        self.q.append(x)
        # Reorder queue: move all elements except the new one to the back
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        """
        Complexity: O(1)
        """
        return self.q.popleft()

    def top(self) -> int:
        """
        Complexity: O(1)
        """
        return self.q[0]

    def empty(self) -> bool:
        return not self.q
```

### Complexity Analysis
- **Time Complexity**: `push` is O(n), `pop` and `top` are O(1).
- **Space Complexity**: O(n).

---

## 3. Design Circular Deque
**Problem Statement**: Design your implementation of the circular double-ended queue (deque).

### Optimal Python Solution
```python
class MyCircularDeque:
    def __init__(self, k: int):
        self.capacity = k
        self.q = [0] * k
        self.size = 0
        self.front = 0
        self.rear = k - 1

    def insertFront(self, value: int) -> bool:
        if self.isFull(): return False
        self.front = (self.front - 1) % self.capacity
        self.q[self.front] = value
        self.size += 1
        return True

    def insertLast(self, value: int) -> bool:
        if self.isFull(): return False
        self.rear = (self.rear + 1) % self.capacity
        self.q[self.rear] = value
        self.size += 1
        return True

    def deleteFront(self) -> bool:
        if self.isEmpty(): return False
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return True

    def deleteLast(self) -> bool:
        if self.isEmpty(): return False
        self.rear = (self.rear - 1) % self.capacity
        self.size -= 1
        return True

    def getFront(self) -> int:
        return -1 if self.isEmpty() else self.q[self.front]

    def getRear(self) -> int:
        return -1 if self.isEmpty() else self.q[self.rear]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity
```

---

## 4. Design Hit Counter
**Problem Statement**: Design a hit counter which counts the number of hits received in the past 5 minutes (300 seconds).

### Optimal Python Solution
```python
from collections import deque

class HitCounter:
    def __init__(self):
        # Stores timestamps of hits
        self.hits = deque()

    def hit(self, timestamp: int) -> None:
        self.hits.append(timestamp)

    def getHits(self, timestamp: int) -> int:
        # Remove hits that occurred more than 300 seconds ago
        while self.hits and self.hits[0] <= timestamp - 300:
            self.hits.popleft()
        return len(self.hits)
```

### Complexity Analysis
- **Time Complexity**: `hit` is O(1), `getHits` is O(1) amortized.
- **Space Complexity**: O(n), where n is the number of hits in the 300s window.
