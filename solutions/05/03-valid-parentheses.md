# Valid Parentheses

## Practice Problems

### 1. Valid Parentheses
**Difficulty:** Easy
**Key Technique:** Stack + Mapping

```python
def is_valid(s: str) -> bool:
    """
    Time: O(n)
    Space: O(n)
    """
    stack = []
    map = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in map:
            if not stack or stack.pop() != map[char]:
                return False
        else:
            stack.append(char)
    return not stack
```

### 2. Minimum Remove to Make Valid Parentheses
**Difficulty:** Medium
**Key Technique:** Stack of indices

```python
def min_remove_to_make_valid(s: str) -> str:
    """
    Time: O(n)
    Space: O(n)
    """
    stack = [] # indices of '('
    to_remove = set()
    for i, c in enumerate(s):
        if c == '(':
            stack.append(i)
        elif c == ')':
            if stack:
                stack.pop()
            else:
                to_remove.add(i)
    to_remove.update(stack)
    return "".join(c for i, c in enumerate(s) if i not in to_remove)
```

### 3. Generate Parentheses
**Difficulty:** Medium
**Key Technique:** Backtracking

```python
def generate_parenthesis(n: int) -> list[str]:
    """
    Time: O(4^n / sqrt(n)) - Catalan number
    Space: O(n)
    """
    res = []
    def backtrack(curr, o, c):
        if len(curr) == 2 * n:
            res.append(curr)
            return
        if o < n:
            backtrack(curr + "(", o + 1, c)
        if c < o:
            backtrack(curr + ")", o, c + 1)
    backtrack("", 0, 0)
    return res
```

### 4. Longest Valid Parentheses
**Difficulty:** Hard
**Key Technique:** Stack with base index

```python
def longest_valid_parentheses(s: str) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    stack = [-1]
    res = 0
    for i, c in enumerate(s):
        if c == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                res = max(res, i - stack[-1])
    return res
```
