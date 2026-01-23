# Min Stack

## Practice Problems

### 1. Min Stack (Two Stacks)
**Difficulty:** Medium
**Key Technique:** Auxiliary stack for current minimum

```python
class MinStack:
    """
    Time: O(1) for all operations
    Space: O(n)
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        if self.stack.pop() == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

### 2. Max Stack (Two Stacks)
**Difficulty:** Medium
**Key Technique:** Auxiliary stack for current maximum

```python
class MaxStack:
    """
    Time: O(1)
    Space: O(n)
    """
    def __init__(self):
        self.stack = []
        self.max_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.max_stack or val >= self.max_stack[-1]:
            self.max_stack.append(val)

    def pop(self) -> int:
        if self.stack.pop() == self.max_stack[-1]:
            self.max_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMax(self) -> int:
        return self.max_stack[-1]
```

### 3. Min Stack (Difference Encoding)
**Difficulty:** Hard
**Key Technique:** Mathematical encoding for O(1) extra space

```python
class MinStackEncoded:
    """
    Time: O(1)
    Space: O(1) extra (O(n) total for stack)
    """
    def __init__(self):
        self.stack = []
        self.min_val = None

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append(0)
            self.min_val = val
        else:
            self.stack.append(val - self.min_val)
            if val < self.min_val:
                self.min_val = val

    def pop(self) -> None:
        diff = self.stack.pop()
        if diff < 0:
            self.min_val = self.min_val - diff
        if not self.stack:
            self.min_val = None

    def top(self) -> int:
        diff = self.stack[-1]
        if diff < 0:
            return self.min_val
        return self.min_val + diff

    def getMin(self) -> int:
        return self.min_val
```
