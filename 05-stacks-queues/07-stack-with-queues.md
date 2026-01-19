# Implement Stack Using Queues

> **Prerequisites:** [01-stack-basics](./01-stack-basics.md), [02-queue-basics](./02-queue-basics.md)

## Interview Context

This problem is a **classic design question** at FANG+ companies because:

1. **Constraint thinking**: Implement LIFO using only FIFO operations
2. **Tradeoff analysis**: Multiple valid solutions with different complexity tradeoffs
3. **Data structure mastery**: Tests deep understanding of stack and queue behavior
4. **Real-world relevance**: Sometimes you only have queue primitives available

Interviewers use this to assess your ability to think creatively within constraints.

---

## The Problem

Implement a stack using only queue operations:
- `push(x)` — Push element x onto stack
- `pop()` — Remove and return the top element
- `top()` — Get the top element
- `empty()` — Return whether the stack is empty

**Constraint**: Only use `enqueue`, `dequeue`, `front`, `empty`, `size` operations.

---

## Approach Comparison

| Approach | push | pop | top | Space |
|----------|------|-----|-----|-------|
| Two queues (push costly) | O(n) | O(1) | O(1) | O(n) |
| Two queues (pop costly) | O(1) | O(n) | O(n) | O(n) |
| One queue | O(n) | O(1) | O(1) | O(n) |

---

## Solution 1: Two Queues (Push Costly)

```python
from collections import deque

class MyStack:
    """
    Stack using two queues, costly push.

    Idea: After push, rotate elements so new element is at front.

    Time: push O(n), pop O(1), top O(1)
    Space: O(n)
    """
    def __init__(self):
        self.q1 = deque()  # Main queue
        self.q2 = deque()  # Helper queue

    def push(self, x: int) -> None:
        # Add to empty q2
        self.q2.append(x)

        # Move all elements from q1 to q2 (behind x)
        while self.q1:
            self.q2.append(self.q1.popleft())

        # Swap q1 and q2
        self.q1, self.q2 = self.q2, self.q1

    def pop(self) -> int:
        return self.q1.popleft()

    def top(self) -> int:
        return self.q1[0]

    def empty(self) -> bool:
        return len(self.q1) == 0


# Walkthrough:
# push(1): q2=[1], q1=[], swap → q1=[1], q2=[]
# push(2): q2=[2], move 1 → q2=[2,1], swap → q1=[2,1], q2=[]
# push(3): q2=[3], move 2,1 → q2=[3,2,1], swap → q1=[3,2,1], q2=[]
# pop(): return q1.popleft() = 3, q1=[2,1]
# top(): q1[0] = 2
```

### Visual Representation

```
push(1):
  q2: [1]          q1: []
  swap
  q1: [1]          q2: []

push(2):
  q2: [2]          q1: [1]
  move q1→q2
  q2: [2, 1]       q1: []
  swap
  q1: [2, 1]       q2: []
       ↑
     front (stack top)

pop():
  return 2
  q1: [1]
```

---

## Solution 2: Two Queues (Pop Costly)

```python
from collections import deque

class MyStack:
    """
    Stack using two queues, costly pop.

    Idea: Push is O(1). For pop, move n-1 elements, dequeue last.

    Time: push O(1), pop O(n), top O(n)
    Space: O(n)
    """
    def __init__(self):
        self.q1 = deque()
        self.q2 = deque()

    def push(self, x: int) -> None:
        self.q1.append(x)

    def pop(self) -> int:
        # Move n-1 elements to q2
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())

        # Last element is the "top" of stack
        result = self.q1.popleft()

        # Swap queues
        self.q1, self.q2 = self.q2, self.q1

        return result

    def top(self) -> int:
        # Move n-1 elements to q2
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())

        # Last element is top
        result = self.q1[0]

        # Move it too, then swap
        self.q2.append(self.q1.popleft())
        self.q1, self.q2 = self.q2, self.q1

        return result

    def empty(self) -> bool:
        return len(self.q1) == 0


# Walkthrough:
# push(1), push(2), push(3): q1=[1,2,3], q2=[]
# pop():
#   move 1,2 to q2 → q1=[3], q2=[1,2]
#   result = 3
#   swap → q1=[1,2], q2=[]
#   return 3
```

---

## Solution 3: Single Queue (Most Elegant)

```python
from collections import deque

class MyStack:
    """
    Stack using single queue.

    Idea: After push, rotate queue so new element is at front.

    Time: push O(n), pop O(1), top O(1)
    Space: O(n)
    """
    def __init__(self):
        self.queue = deque()

    def push(self, x: int) -> None:
        self.queue.append(x)

        # Rotate: move all previous elements behind x
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())

    def pop(self) -> int:
        return self.queue.popleft()

    def top(self) -> int:
        return self.queue[0]

    def empty(self) -> bool:
        return len(self.queue) == 0


# Walkthrough:
# push(1): queue=[1], rotate 0 times → [1]
# push(2): queue=[1,2], rotate 1 time:
#          [2,1]  (moved 1 to back)
# push(3): queue=[2,1,3], rotate 2 times:
#          [1,3,2]  (moved 2)
#          [3,2,1]  (moved 1)
# pop(): return 3, queue=[2,1]
# top(): return 2
```

### Visual Representation

```
push(1):
  queue: [1]
  no rotation needed

push(2):
  queue: [1, 2]
  rotate 1 time:
    dequeue 1, enqueue 1 → [2, 1]
                            ↑
                          front (stack top)

push(3):
  queue: [2, 1, 3]
  rotate 2 times:
    dequeue 2, enqueue 2 → [1, 3, 2]
    dequeue 1, enqueue 1 → [3, 2, 1]
                            ↑
                          front (stack top)
```

---

## Alternative: Pop-Costly Single Queue

```python
from collections import deque

class MyStack:
    """
    Single queue, pop-costly version.

    Time: push O(1), pop O(n), top O(n)
    Space: O(n)
    """
    def __init__(self):
        self.queue = deque()

    def push(self, x: int) -> None:
        self.queue.append(x)

    def pop(self) -> int:
        # Rotate n-1 elements, then dequeue
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())
        return self.queue.popleft()

    def top(self) -> int:
        # Rotate n-1 elements
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())

        result = self.queue[0]

        # Complete the rotation (move last element too)
        self.queue.append(self.queue.popleft())

        return result

    def empty(self) -> bool:
        return len(self.queue) == 0
```

---

## Amortized Analysis

For the push-costly approach with n operations:

```
Operations: push(1), push(2), push(3), pop(), pop(), pop()

push(1): 1 operation
push(2): 2 operations (1 rotation)
push(3): 3 operations (2 rotations)
pop():   1 operation
pop():   1 operation
pop():   1 operation

Total: 1+2+3+1+1+1 = 9 operations for 6 calls
Average: 1.5 operations per call

For n push followed by n pop:
Push cost: 1+2+3+...+n = O(n²)
Pop cost: n × O(1) = O(n)
Total: O(n²) for 2n operations
Amortized: O(n) per push, O(1) per pop
```

---

## When to Use Which Approach

| Scenario | Best Approach |
|----------|---------------|
| Many pushes, few pops | Pop-costly |
| Many pops, few pushes | Push-costly |
| Balanced operations | Either works |
| Minimize code complexity | Single queue push-costly |

---

## Edge Cases

```python
# 1. Empty stack
s = MyStack()
print(s.empty())  # True

# 2. Single element
s.push(1)
print(s.top())    # 1
print(s.pop())    # 1
print(s.empty())  # True

# 3. Multiple push-pop cycles
s.push(1)
s.push(2)
s.pop()           # 2
s.push(3)
s.top()           # 3
s.pop()           # 3
s.pop()           # 1
```

---

## Follow-up Questions

### Q: Can you do better than O(n)?
A: No, without additional data structures. We need O(n) to reverse FIFO to LIFO ordering at some point.

### Q: What if you have limited queue size?
A: Use circular queue implementation to prevent overflow.

### Q: How about making top() O(1) in pop-costly version?
A: Cache the last pushed element:

```python
class MyStack:
    def __init__(self):
        self.queue = deque()
        self._top = None

    def push(self, x: int) -> None:
        self.queue.append(x)
        self._top = x

    def top(self) -> int:
        return self._top

    def pop(self) -> int:
        for _ in range(len(self.queue) - 1):
            self._top = self.queue.popleft()  # Update top
            self.queue.append(self._top)
        return self.queue.popleft()
```

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Implement Stack using Queues | Easy | Core problem |
| 2 | Implement Queue using Stacks | Easy | Reverse direction |
| 3 | Design Circular Queue | Medium | Related structure |
| 4 | Design Front Middle Back Queue | Medium | Multiple operations |

---

## Key Takeaways

1. **Single queue is cleanest**: Rotation after push gives O(n) push, O(1) pop
2. **Tradeoff exists**: Push-costly vs pop-costly depends on usage pattern
3. **Rotation is key**: Moving n-1 elements reverses the order
4. **Cache for optimization**: Store top element for O(1) top() in pop-costly

---

## Next: [08-queue-with-stacks.md](./08-queue-with-stacks.md)

Learn the reverse problem: implementing a queue using stacks.
