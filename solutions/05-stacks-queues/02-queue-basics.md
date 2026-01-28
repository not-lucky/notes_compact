# Queue Basics - Practice Solutions

This file provides optimal Python solutions and explanations for the practice problems listed in the Queue Basics notes.

## 1. Design Circular Queue

**Problem Statement**: Design your implementation of the circular queue. The circular queue is a linear data structure in which the operations are performed based on FIFO (First In First Out) principle and the last position is connected back to the first position to make a circle.

### Optimal Python Solution

```python
class MyCircularQueue:
    def __init__(self, k: int):
        self.queue = [0] * k
        self.head = 0
        self.count = 0
        self.capacity = k

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        # Calculate next rear position using modulo
        rear = (self.head + self.count) % self.capacity
        self.queue[rear] = value
        self.count += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        # Move head forward using modulo
        self.head = (self.head + 1) % self.capacity
        self.count -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.queue[self.head]

    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        # Calculate rear position
        rear = (self.head + self.count - 1) % self.capacity
        return self.queue[rear]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == self.capacity
```

### Explanation

A circular queue uses a fixed-size array and modulo arithmetic to wrap the rear and head pointers back to the beginning. We use `count` to easily track the number of elements and differentiate between empty and full states.

### Complexity Analysis

- **Time Complexity**: O(1) for all operations because we use direct index access and simple arithmetic.
- **Space Complexity**: O(k), where k is the capacity of the queue, to pre-allocate the array.

---

## 2. Number of Recent Calls

**Problem Statement**: You have a `RecentCounter` class which counts the number of recent requests within a certain time frame (3000ms).

### Optimal Python Solution

```python
from collections import deque

class RecentCounter:
    def __init__(self):
        self.requests = deque()

    def ping(self, t: int) -> int:
        # Add new request time
        self.requests.append(t)
        # Remove requests that are outside the [t-3000, t] window
        while self.requests[0] < t - 3000:
            self.requests.popleft()
        return len(self.requests)
```

### Explanation

We use a queue to store timestamps. Since timestamps are strictly increasing, any request older than `t - 3000` will never be relevant for future pings. We use `popleft()` on the deque to efficiently remove old requests from the front.

### Complexity Analysis

- **Time Complexity**: O(1) amortized. Each timestamp is appended once and popped at most once across all ping calls, making the total work linear with respect to the number of pings.
- **Space Complexity**: O(W), where W is the maximum number of requests in a 3000ms window.

---

## 3. Moving Average from Data Stream

**Problem Statement**: Given a stream of integers and a window size, calculate the moving average of all integers in the sliding window.

### Optimal Python Solution

```python
from collections import deque

class MovingAverage:
    def __init__(self, size: int):
        self.size = size
        self.queue = deque()
        self.current_sum = 0

    def next(self, val: int) -> float:
        # Add new value to window
        self.queue.append(val)
        self.current_sum += val

        # If window size exceeded, remove oldest
        if len(self.queue) > self.size:
            oldest = self.queue.popleft()
            self.current_sum -= oldest

        return self.current_sum / len(self.queue)
```

### Explanation

We maintain a window of size `size` using a queue. By keeping a running `current_sum`, we can calculate the average in constant time instead of re-summing the entire queue.

### Complexity Analysis

- **Time Complexity**: O(1) for each `next()` call because we perform a constant number of deque and addition operations.
- **Space Complexity**: O(size), to store the elements currently in the window.

---

## 4. Implement Queue using Stacks

**Problem Statement**: Implement a first-in-first-out (FIFO) queue using only two stacks.

### Optimal Python Solution

```python
class MyQueue:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def pop(self) -> int:
        self._move()
        return self.out_stack.pop()

    def peek(self) -> int:
        self._move()
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack

    def _move(self):
        # Transfer elements only if out_stack is empty
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
```

### Explanation

We use two stacks: `in_stack` for additions and `out_stack` for removals. By transferring all elements from `in_stack` to `out_stack` when `out_stack` is empty, we reverse the LIFO order twice, which results in FIFO order.

### Complexity Analysis

- **Time Complexity**: O(1) amortized for `pop` and `peek`. While one operation might move n elements, each element is moved exactly once across its lifetime. `push` is O(1).
- **Space Complexity**: O(n), where n is the number of elements stored.

---

## 5. Design Circular Deque

**Problem Statement**: Design your implementation of the circular double-ended queue (deque).

### Optimal Python Solution

```python
class MyCircularDeque:
    def __init__(self, k: int):
        self.k = k
        self.q = [0] * k
        self.size = 0
        self.front = 0
        self.rear = k - 1

    def insertFront(self, value: int) -> bool:
        if self.isFull(): return False
        self.front = (self.front - 1) % self.k
        self.q[self.front] = value
        self.size += 1
        return True

    def insertLast(self, value: int) -> bool:
        if self.isFull(): return False
        self.rear = (self.rear + 1) % self.k
        self.q[self.rear] = value
        self.size += 1
        return True

    def deleteFront(self) -> bool:
        if self.isEmpty(): return False
        self.front = (self.front + 1) % self.k
        self.size -= 1
        return True

    def deleteLast(self) -> bool:
        if self.isEmpty(): return False
        self.rear = (self.rear - 1) % self.k
        self.size -= 1
        return True

    def getFront(self) -> int:
        return -1 if self.isEmpty() else self.q[self.front]

    def getRear(self) -> int:
        return -1 if self.isEmpty() else self.q[self.rear]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.k
```

### Explanation

Similar to the circular queue, but with the ability to add and remove from both ends. We adjust pointers using modulo arithmetic to ensure they wrap around.

---

## 6. Binary Tree Level Order Traversal

**Problem Statement**: Given the `root` of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

### Optimal Python Solution

```python
from collections import deque

def levelOrder(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)

            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)

        result.append(current_level)

    return result
```

### Explanation

We use a queue to perform Breadth-First Search (BFS). For each level, we record the queue size to process exactly the nodes currently on that level before moving to the next.

### Complexity Analysis

- **Time Complexity**: O(n), where n is the number of nodes in the tree. We visit each node exactly once.
- **Space Complexity**: O(w), where w is the maximum width of the tree (number of nodes in the largest level) which is at most n/2.

---

## 7. Rotting Oranges

**Problem Statement**: You are given a grid where each cell is empty, has a fresh orange, or a rotten orange. Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten. Return the minimum time until no fresh oranges remain.

### Optimal Python Solution

```python
from collections import deque

def orangesRotting(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh_count = 0

    # 1. Initialize queue with all rotten oranges
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh_count += 1

    if fresh_count == 0: return 0

    minutes = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # 2. Multi-source BFS
    while queue and fresh_count > 0:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh_count -= 1
                    queue.append((nr, nc))

    return minutes if fresh_count == 0 else -1
```

### Explanation

This is a multi-source BFS problem. We start by adding all rotten oranges to the queue. Each "level" of BFS represents one minute passing. Fresh oranges become rotten and are added to the queue for the next minute.

### Complexity Analysis

- **Time Complexity**: O(R \* C), where R and C are rows and columns. In the worst case, we visit every cell in the grid.
- **Space Complexity**: O(R \* C), for the queue in the case where all oranges are rotten initially.
