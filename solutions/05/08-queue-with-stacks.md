# Implement Queue Using Stacks

## Practice Problems

### 1. Implement Queue using Stacks (Amortized O(1))
**Difficulty:** Easy
**Key Technique:** Two stacks (In and Out) with lazy transfer

```python
class MyQueue:
    """
    Time: O(1) push, O(1) amortized pop/peek
    Space: O(n)
    """
    def __init__(self):
        self.s_in = []
        self.s_out = []

    def push(self, x: int) -> None:
        self.s_in.append(x)

    def pop(self) -> int:
        self.peek()
        return self.s_out.pop()

    def peek(self) -> int:
        if not self.s_out:
            while self.s_in:
                self.s_out.append(self.s_in.pop())
        return self.s_out[-1]

    def empty(self) -> bool:
        return not self.s_in and not self.s_out
```

### 2. Implement Queue using Stacks (Push Costly)
**Difficulty:** Easy
**Key Technique:** Two stacks + Full transfer on every push

```python
class MyQueuePushCostly:
    """
    Time: O(n) push, O(1) pop
    Space: O(n)
    """
    def __init__(self):
        self.s1 = []
        self.s2 = []

    def push(self, x: int) -> None:
        while self.s1:
            self.s2.append(self.s1.pop())
        self.s1.append(x)
        while self.s2:
            self.s1.append(self.s2.pop())

    def pop(self) -> int:
        return self.s1.pop()

    def peek(self) -> int:
        return self.s1[-1]

    def empty(self) -> bool:
        return not self.s1
```
