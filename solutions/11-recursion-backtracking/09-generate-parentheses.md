# Generate Parentheses - Solutions

This document provides optimal solutions and detailed explanations for the practice problems related to Generate Parentheses.

---

## 1. Generate Parentheses

### Problem Statement

Given `n` pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

### Examples & Edge Cases

- **Input:** n = 3 → **Output:** ["((()))","(()())","(())()","()(())","()()()"]
- **Input:** n = 1 → **Output:** ["()"]
- **Edge Case:** n = 0 → [""]

### Optimal Python Solution (Backtracking)

```python
def generateParenthesis(n: int) -> list[str]:
    res = []

    def backtrack(current: str, open_count: int, close_count: int):
        # Base case: used all parentheses
        if len(current) == 2 * n:
            res.append(current)
            return

        # Choice 1: Add an open parenthesis
        if open_count < n:
            backtrack(current + "(", open_count + 1, close_count)

        # Choice 2: Add a closing parenthesis (only if it matches an open one)
        if close_count < open_count:
            backtrack(current + ")", open_count, close_count + 1)

    backtrack("", 0, 0)
    return res
```

### Detailed Explanation

1. **The Validity Invariant**: To ensure a sequence is well-formed:
   - We can never have more than `n` open parentheses.
   - At any point while building the string, the number of closing parentheses cannot exceed the number of open ones.
2. **Backtracking**: We start with an empty string and recursively try adding `(` then `)`. If we reach length `2n`, we have a valid sequence.
3. **Efficiency**: This approach _only_ generates valid sequences, exploring exactly $C_n$ paths (the $n$-th Catalan number).

### Complexity Analysis

- **Time Complexity:** $O(\frac{4^n}{\sqrt{n}})$ - This is the bound for the $n$-th Catalan number.
- **Space Complexity:** $O(n)$ - The maximum depth of the recursion stack is $2n$.

---

## 2. Valid Parentheses

### Problem Statement

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

### Optimal Python Solution (Stack)

```python
def isValid(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in mapping:
            # If closing bracket, check if it matches the top of stack
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            # If opening bracket, push to stack
            stack.append(char)

    return not stack
```

### Complexity Analysis

- **Time Complexity:** $O(n)$ - Single pass through the string.
- **Space Complexity:** $O(n)$ - Worst case stack size.

---

## 3. Minimum Add to Make Valid

### Problem Statement

Return the minimum number of parentheses we must add to make the string valid.

### Optimal Python Solution

```python
def minAddToMakeValid(s: str) -> int:
    # Track balance
    open_needed = 0
    close_needed = 0

    for char in s:
        if char == '(':
            open_needed += 1
        else:
            if open_needed > 0:
                open_needed -= 1
            else:
                close_needed += 1

    return open_needed + close_needed
```

---

## 4. Longest Valid Parentheses

### Problem Statement

Given a string containing just the characters `'('` and `')'`, find the length of the longest valid (well-formed) parentheses substring.

### Optimal Python Solution (Stack or DP)

```python
def longestValidParentheses(s: str) -> int:
    stack = [-1] # Initialize with -1 to handle full valid strings
    max_len = 0

    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i) # Anchor for next valid sequence
            else:
                max_len = max(max_len, i - stack[-1])

    return max_len
```

---

## 5. Remove Invalid Parentheses

### Problem Statement

Remove the minimum number of invalid parentheses to make the input string valid. Return all possible results.

### Optimal Python Solution (BFS)

BFS is ideal here because it finds the "minimum removals" level by level.

```python
from collections import deque

def removeInvalidParentheses(s: str) -> list[str]:
    def is_valid(s):
        count = 0
        for char in s:
            if char == '(': count += 1
            elif char == ')': count -= 1
            if count < 0: return False
        return count == 0

    queue = deque([s])
    visited = {s}
    found = False
    res = []

    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            curr = queue.popleft()
            if is_valid(curr):
                res.append(curr)
                found = True

            if found: continue # If found at this level, don't generate next level

            for i in range(len(curr)):
                if curr[i] not in "()": continue
                next_s = curr[:i] + curr[i+1:]
                if next_s not in visited:
                    visited.add(next_s)
                    queue.append(next_s)

        if found: break # Return immediately after finishing the level where solutions were found
    return res
```
