# Valid Parentheses - Practice Solutions

This file provides optimal Python solutions and explanations for the practice problems listed in the Valid Parentheses notes.

## 1. Valid Parentheses

**Problem Statement**: Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

### Examples & Edge Cases

- **Example 1**: `"()"` -> `True`
- **Example 2**: `"()[]{}"` -> `True`
- **Example 3**: `"(]"` -> `False`
- **Edge Case**: `s = ""` -> `True` (Empty string)
- **Edge Case**: `s = "((("` -> `False` (Unclosed brackets)

### Optimal Python Solution

```python
def isValid(s: str) -> bool:
    # Map closing brackets to their corresponding opening brackets
    mapping = {")": "(", "}": "{", "]": "["}
    stack = []

    for char in s:
        if char in mapping:
            # If current is closing, pop from stack (or use dummy '#' if empty)
            top = stack.pop() if stack else '#'
            if top != mapping[char]:
                return False
        else:
            # If opening, push onto stack
            stack.append(char)

    # Valid if stack is empty (all matched)
    return not stack
```

### Explanation

We use a stack to process the string. Opening brackets are stored to be matched later. When a closing bracket appears, it must match the most recently pushed opening bracket (the top of the stack). This LIFO behavior perfectly matches the nested structure of valid parentheses.

### Complexity Analysis

- **Time Complexity**: O(n), where n is the length of the string. We perform a single pass through the input string, and every stack operation (push/pop) is O(1).
- **Space Complexity**: O(n), as in the worst case (e.g., a string consisting only of opening brackets), the stack will store all n characters.

---

## 2. Generate Parentheses

**Problem Statement**: Given `n` pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

### Optimal Python Solution

```python
def generateParenthesis(n: int) -> list[str]:
    result = []

    def backtrack(S = [], left = 0, right = 0):
        if len(S) == 2 * n:
            result.append("".join(S))
            return

        # If we can still add an opening bracket
        if left < n:
            S.append("(")
            backtrack(S, left + 1, right)
            S.pop() # Backtrack

        # If we can add a closing bracket (must have matching open)
        if right < left:
            S.append(")")
            backtrack(S, left, right + 1)
            S.pop() # Backtrack

    backtrack()
    return result
```

### Explanation

This problem uses backtracking. The key constraints for a valid partial string are: 1) Number of '(' must be ≤ `n`. 2) Number of ')' must be ≤ number of '('. By following these rules, we explore all valid paths.

### Complexity Analysis

- **Time Complexity**: O(4^n / √n). This is proportional to the n-th Catalan number, which represents the number of valid parenthetical expressions of length 2n.
- **Space Complexity**: O(n), for the recursion stack and the list used to build each valid string.

---

## 3. Longest Valid Parentheses

**Problem Statement**: Given a string containing just the characters '(' and ')', return the length of the longest valid (well-formed) parentheses substring.

### Optimal Python Solution

```python
def longestValidParentheses(s: str) -> int:
    # Stack stores indices of '('
    # Initialize with -1 to handle full valid strings like "()" (1 - (-1) = 2)
    stack = [-1]
    max_len = 0

    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                # If stack is empty, push current index as new base
                stack.append(i)
            else:
                # Current length is current index minus the last unmatched index
                max_len = max(max_len, i - stack[-1])

    return max_len
```

### Complexity Analysis

- **Time Complexity**: O(n), where n is the length of the string. We traverse the string once, and each index is pushed or popped from the stack at most once.
- **Space Complexity**: O(n), to store the indices in the stack in the worst case.

---

## 4. Remove Invalid Parentheses

**Problem Statement**: Remove the minimum number of invalid parentheses to make the input string valid. Return all possible results.

### Optimal Python Solution

````python
def removeInvalidParentheses(s: str) -> list[str]:
    def is_valid(string):
        count = 0
        for char in string:
            if char == '(': count += 1
            elif char == ')': count -= 1
            if count < 0: return False
        return count == 0

    # BFS approach
    level = {s}
    while True:
        valid = list(filter(is_valid, level))
        if valid:
            return valid

        # Build next level by removing one bracket at a time
        new_level = set()
        for string in level:
            for i in range(len(string)):
                if string[i] in '()':
                    new_level.add(string[:i] + string[i+1:])
```
### Complexity Analysis
- **Time Complexity**: O(n * 2^n), where n is the length of the string. In each BFS level, we potentially explore all possible single-character removals.
- **Space Complexity**: O(n * 2^n), to store the strings in the current and next levels of BFS.

---

## 5. Minimum Remove to Make Valid Parentheses
**Problem Statement**: Given a string `s`, remove the minimum number of parentheses ( '(' or ')', in any positions ) so that the resulting parentheses string is valid.

### Optimal Python Solution
```python
def minRemoveToMakeValid(s: str) -> str:
    s_list = list(s)
    stack = [] # Stores indices of '('

    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                stack.pop()
            else:
                # This ')' is invalid, mark it for removal
                s_list[i] = ""

    # Remaining indices in stack are unmatched '('
```
### Complexity Analysis
- **Time Complexity**: O(n), where n is the length of the string. We perform one pass to identify invalid indices and one pass to join the characters.
- **Space Complexity**: O(n), to store the stack of indices and the list representation of the string.

---

## 6. Valid Parenthesis String
**Problem Statement**: Given a string `s` containing '(', ')' and '*', return true if `s` is valid. '*' can be '(', ')' or empty.

### Optimal Python Solution
```python
def checkValidString(s: str) -> bool:
    # low: min possible open brackets, high: max possible open brackets
    low = high = 0
    for char in s:
        low += 1 if char == '(' else -1
        high += 1 if char != ')' else -1
        if high < 0: return False
        low = max(low, 0)
```
### Complexity Analysis
- **Time Complexity**: O(n), as we iterate through the string once and perform constant time updates to `low` and `high`.
- **Space Complexity**: O(1), as we only use two integer variables.

---

## 7. Score of Parentheses
**Problem Statement**: Calculate score: `()` has score 1, `AB` has score `A + B`, `(A)` has score `2 * A`.

### Optimal Python Solution
```python
def scoreOfParentheses(s: str) -> int:
    stack = [0] # Current scores at each depth
    for char in s:
        if char == '(':
            stack.append(0)
        else:
            v = stack.pop()
            stack[-1] += max(2 * v, 1)
```
### Complexity Analysis
- **Time Complexity**: O(n), where n is the length of the string. We visit each character once and perform O(1) stack operations.
- **Space Complexity**: O(n), for the stack which tracks scores at different nesting depths.
````
