# Solution: Valid Parentheses Practice Problems

## Problem 1: Valid Parentheses
### Problem Statement
Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

### Constraints
- `1 <= s.length <= 10^4`
- `s` consists of parentheses only `'()[]{}'`.

### Example
Input: `s = "()[]{}"`
Output: `true`

### Python Implementation
```python
def isValid(s: str) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)

    return not stack
```

---

## Problem 2: Generate Parentheses
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
    Time Complexity: O(4^n / sqrt(n)) - Catalan number
    Space Complexity: O(n) for recursion stack
    """
    result = []
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return

        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)

    backtrack("", 0, 0)
    return result
```

---

## Problem 3: Longest Valid Parentheses
### Problem Statement
Given a string containing just the characters `'('` and `')'`, return the length of the longest valid (well-formed) parentheses substring.

### Constraints
- `0 <= s.length <= 3 * 10^4`
- `s[i]` is `'('`, or `')'`.

### Example
Input: `s = "(()"`
Output: `2`

### Python Implementation
```python
def longestValidParentheses(s: str) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    stack = [-1]
    max_len = 0
    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                max_len = max(max_len, i - stack[-1])
    return max_len
```

---

## Problem 4: Minimum Remove to Make Valid Parentheses
### Problem Statement
Given a string `s` of `'('`, `')'` and lowercase English characters.

Your task is to remove the minimum number of parentheses ( `'('` or `')'`, in any positions ) so that the resulting parentheses string is valid and return any valid string.

### Constraints
- `1 <= s.length <= 10^5`
- `s[i]` is either `'('` , `')'` or lowercase English letter.

### Example
Input: `s = "lee(t(c)o)de)"`
Output: `"lee(t(c)o)de"`

### Python Implementation
```python
def minRemoveToMakeValid(s: str) -> str:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    stack = [] # indices of '('
    to_remove = set()
    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                stack.pop()
            else:
                to_remove.add(i)

    to_remove.update(stack)

    res = []
    for i, char in enumerate(s):
        if i not in to_remove:
            res.append(char)

    return "".join(res)
```
