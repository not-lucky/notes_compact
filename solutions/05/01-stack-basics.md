# Stack Basics

## Practice Problems

### 1. Valid Parentheses
**Difficulty:** Easy
**Key Technique:** Stack for matching

```python
def is_valid(s: str) -> bool:
    """
    Time: O(n)
    Space: O(n)
    """
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    return not stack
```

### 2. Min Stack
**Difficulty:** Medium
**Key Technique:** Auxiliary stack for minimums

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

### 3. Evaluate Reverse Polish Notation
**Difficulty:** Medium
**Key Technique:** Stack for operands

```python
def eval_rpn(tokens: list[str]) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    stack = []
    for t in tokens:
        if t in "+-*/":
            b, a = stack.pop(), stack.pop()
            if t == "+": stack.append(a + b)
            elif t == "-": stack.append(a - b)
            elif t == "*": stack.append(a * b)
            else: stack.append(int(a / b)) # Truncate toward zero
        else:
            stack.append(int(t))
    return stack[0]
```

### 4. Remove All Adjacent Duplicates In String
**Difficulty:** Easy
**Key Technique:** Stack for processing

```python
def remove_duplicates(s: str) -> str:
    """
    Time: O(n)
    Space: O(n)
    """
    stack = []
    for char in s:
        if stack and stack[-1] == char:
            stack.pop()
        else:
            stack.append(char)
    return "".join(stack)
```
