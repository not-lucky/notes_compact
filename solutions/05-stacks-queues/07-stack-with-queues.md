# Implement Stack Using Queues - Practice Solutions

This file provides optimal Python solutions and explanations for the practice problems listed in the Implement Stack Using Queues notes.

## 1. Implement Stack using Queues (Single Queue)

**Problem Statement**: Implement a last-in-first-out (LIFO) stack using only one queue.

### Optimal Python Solution

```python
from collections import deque

class MyStack:
    def __init__(self):
        # We use a single deque to simulate a stack
        self.queue = deque()

    def push(self, x: int) -> None:
        """
        Push element x onto stack.
        Complexity: O(n)
        """
        self.queue.append(x)
        # Rotate the queue so that the newly added element is at the front
        # This makes the queue 'look' like a stack (LIFO)
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())

    def pop(self) -> int:
        """
        Removes the element on top of the stack and returns it.
        Complexity: O(1)
        """
        return self.queue.popleft()

    def top(self) -> int:
        """
        Get the top element.
        Complexity: O(1)
        """
        return self.queue[0]

    def empty(self) -> bool:
        """
        Returns whether the stack is empty.
        Complexity: O(1)
        """
        return not self.queue
```

### Explanation

To implement a stack (LIFO) with a queue (FIFO), we must ensure that the most recently added element is always at the front of the queue. We achieve this by rotating the queue after every `push` operation. When we add an element to the back, we move all previous elements to the back behind it. This takes O(n) time for `push` but allows O(1) `pop` and `top`.

### Complexity Analysis

- **Time Complexity**:
  - `push`: O(n), where n is the number of elements in the stack.
  - `pop`, `top`, `empty`: O(1).
- **Space Complexity**: O(n), to store the elements.

---

## 2. Implement Queue using Stacks

**Problem Statement**: Implement a first-in-first-out (FIFO) queue using only two stacks.

### Optimal Python Solution

```python
class MyQueue:
    def __init__(self):
        self.s1 = [] # For push
        self.s2 = [] # For pop/peek

    def push(self, x: int) -> None:
        """Complexity: O(1)"""
        self.s1.append(x)

    def pop(self) -> int:
        """Complexity: O(1) Amortized"""
        self._move()
        return self.s2.pop()

    def peek(self) -> int:
        """Complexity: O(1) Amortized"""
        self._move()
        return self.s2[-1]

    def empty(self) -> bool:
        """Complexity: O(1)"""
        return not self.s1 and not self.s2

    def _move(self):
        """Move elements from s1 to s2 only when s2 is empty."""
        if not self.s2:
            while self.s1:
                self.s2.append(self.s1.pop())
```

### Explanation

By using two stacks, we can reverse the order of elements twice to achieve FIFO. The elements are pushed into `s1`. When a `pop` or `peek` is requested, we move everything from `s1` to `s2` (reversing the order). Subsequent pops from `s2` will be in FIFO order. We only transfer elements when `s2` is empty to maintain efficiency.

### Complexity Analysis

- **Time Complexity**:
  - `push`: O(1).
  - `pop`, `peek`: O(1) amortized. While a single transfer takes O(n), each element is moved at most twice across its lifetime.
- **Space Complexity**: O(n).

---

## 3. Design Circular Queue

**Problem Statement**: Design your implementation of the circular queue using a fixed-size array.

### Optimal Python Solution

```python
class MyCircularQueue:
    def __init__(self, k: int):
        self.queue = [0] * k
        self.head = 0
        self.count = 0
        self.capacity = k

    def enQueue(self, value: int) -> bool:
        if self.count == self.capacity: return False
        # (head + count) gives the current rear position
        self.queue[(self.head + self.count) % self.capacity] = value
        self.count += 1
        return True

    def deQueue(self) -> bool:
        if self.count == 0: return False
        self.head = (self.head + 1) % self.capacity
        self.count -= 1
        return True

    def Front(self) -> int:
        return -1 if self.count == 0 else self.queue[self.head]

    def Rear(self) -> int:
        if self.count == 0: return -1
        return self.queue[(self.head + self.count - 1) % self.capacity]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == self.capacity
```

---

## 4. Design Front Middle Back Queue

**Problem Statement**: Design a queue that supports `pushFront`, `pushMiddle`, `pushBack`, `popFront`, `popMiddle`, and `popBack`.

### Optimal Python Solution

```python
from collections import deque

class FrontMiddleBackQueue:
    def __init__(self):
        # We split the queue into two halves to keep middle operations efficient
        self.left = deque()
        self.right = deque()

    def _balance(self):
        # Keep left size equal to or one less than right size
        if len(self.left) > len(self.right):
            self.right.appendleft(self.left.pop())
        if len(self.right) > len(self.left) + 1:
            self.left.append(self.right.popleft())

    def pushFront(self, val: int) -> None:
        self.left.appendleft(val)
        self._balance()

    def pushMiddle(self, val: int) -> None:
        if len(self.left) == len(self.right):
            self.right.appendleft(val)
        else:
            self.left.append(val)
        self._balance()

    def pushBack(self, val: int) -> None:
        self.right.append(val)
        self._balance()

    def popFront(self) -> int:
        if not self.right: return -1
        if not self.left: return self.right.popleft()
        res = self.left.popleft()
        self._balance()
        return res

    def popMiddle(self) -> int:
        if not self.right: return -1
        if len(self.left) == len(self.right):
            res = self.left.pop()
        else:
            res = self.right.popleft()
        self._balance()
        return res

    def popBack(self) -> int:
        if not self.right: return -1
        res = self.right.pop()
        self._balance()
        return res
```

### Explanation

By maintaining two deques (`left` and `right`) and keeping them balanced (size difference ≤ 1), we can perform middle insertions and deletions in O(1) time. The middle of the entire structure is essentially the junction between the two deques.
