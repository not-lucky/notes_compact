# Solution: Generate Parentheses Practice Problems

## Problem 1: Generate Parentheses
### Problem Statement
Given `n` pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

### Constraints
- `1 <= n <= 8`

### Example
Input: `n = 3`
Output: `["((()))","(()())","(())()","()(())","()()()"]`

### Python Implementation
```python
def generateParenthesis(n: int) -> list[str]:
    """
    Time Complexity: O(4^n / sqrt(n)) - Catalan Number
    Space Complexity: O(n)
    """
    stack = []
    res = []

    def backtrack(openN, closedN):
        if openN == closedN == n:
            res.append("".join(stack))
            return

        if openN < n:
            stack.append("(")
            backtrack(openN + 1, closedN)
            stack.pop()

        if closedN < openN:
            stack.append(")")
            backtrack(openN, closedN + 1)
            stack.pop()

    backtrack(0, 0)
    return res
```

---

## Problem 2: Remove Invalid Parentheses
### Problem Statement
Given a string `s` that contains parentheses and letters, remove the minimum number of invalid parentheses to make the input string valid. Return all possible results. You may return the answer in any order.

### Constraints
- `1 <= s.length <= 25`
- `s` consists of lowercase English letters and parentheses `'('` and `')'`.

### Example
Input: `s = "()())()"`
Output: `["(())()","()()()"]`

### Python Implementation
```python
def removeInvalidParentheses(s: str) -> list[str]:
    """
    Using BFS to find shortest path to valid string.
    Time Complexity: O(2^n)
    Space Complexity: O(2^n)
    """
    def isValid(string):
        count = 0
        for char in string:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
                if count < 0:
                    return False
        return count == 0

    level = {s}
    while True:
        valid = list(filter(isValid, level))
        if valid:
            return valid
        next_level = set()
        for string in level:
            for i in range(len(string)):
                if string[i] in '()':
                    next_level.add(string[:i] + string[i+1:])
        level = next_level
        if not level:
            return [""]
```
