# Stack Basics - Practice Solutions

This file provides optimal Python solutions and explanations for the practice problems listed in the Stack Basics notes.

## 1. Valid Parentheses
**Problem Statement**: Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. A string is valid if open brackets are closed by the same type and in the correct order.

### Examples & Edge Cases
- **Example 1**: `s = "()[]{}"` -> `True`
- **Example 2**: `s = "([)]"` -> `False`
- **Edge Case**: `s = ""` -> `True` (Empty string is valid)
- **Edge Case**: `s = "["` -> `False` (Unclosed bracket)

### Optimal Python Solution
```python
def isValid(s: str) -> bool:
    # Stack to keep track of opening brackets
    stack = []
    # Mapping of closing to opening brackets
    mapping = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in mapping:
            # If it's a closing bracket, check the top of the stack
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            # If it's an opening bracket, push to stack
            stack.append(char)

    # If stack is empty, all brackets were matched
    return not stack
```

### Explanation
We use a stack to store opening brackets as we encounter them. When we see a closing bracket, it must match the most recently opened bracket (the top of the stack). A hash map makes the lookup of corresponding pairs O(1). If the stack is empty at the end, the string is valid.

### Complexity Analysis
- **Time Complexity**: O(n), where n is the length of the string. We traverse the string once, and each stack operation (push/pop) is O(1).
- **Space Complexity**: O(n), as in the worst case (e.g., all opening brackets), we store all characters in the stack.

---

## 2. Baseball Game
**Problem Statement**: You are keeping score for a baseball game with strange rules. Given a list of strings `ops`, where each string is an operation: an integer (record score), "+" (record sum of last two), "D" (record double of last), or "C" (invalidate last). Return the sum of all scores.

### Examples & Edge Cases
- **Example 1**: `ops = ["5","2","C","D","+"]` -> `30`
- **Edge Case**: List with only "C" after one number.
- **Edge Case**: Empty operations list.

### Optimal Python Solution
```python
def calPoints(ops: list[str]) -> int:
    stack = []

    for op in ops:
        if op == "+":
            # Add sum of last two scores
            stack.append(stack[-1] + stack[-2])
        elif op == "D":
            # Add double of last score
            stack.append(2 * stack[-1])
        elif op == "C":
            # Invalidate/Remove last score
            stack.pop()
        else:
            # Record new integer score
            stack.append(int(op))

    return sum(stack)
```

### Explanation
The problem is a natural fit for a stack because all operations depend on the most recent scores recorded. We maintain a stack of valid scores and apply the operations "C", "D", and "+" to the top elements.

### Complexity Analysis
- **Time Complexity**: O(n), where n is the number of operations. We iterate once through the list, and each operation (push, pop, sum) is O(1) or proportional to the number of elements in the stack for the final sum.
- **Space Complexity**: O(n), to store the scores in the stack.

---

## 3. Backspace String Compare
**Problem Statement**: Given two strings `s` and `t`, return if they are equal when both are typed into empty text editors. `#` means a backspace character.

### Examples & Edge Cases
- **Example 1**: `s = "ab#c", t = "ad#c"` -> `True` (Both become "ac")
- **Edge Case**: `s = "a##c", t = "#a#c"` -> `True` (Both become "c")
- **Edge Case**: Backspacing an empty string stays empty.

### Optimal Python Solution
```python
def backspaceCompare(s: str, t: str) -> bool:
    def build(string):
        stack = []
        for char in string:
            if char != '#':
                stack.append(char)
            elif stack:
                stack.pop()
        return "".join(stack)

    return build(s) == build(t)
```

### Explanation
We simulate the typing process using a stack. For every non-`#` character, we push it to the stack. For every `#`, we pop the top element (if the stack is not empty). Comparing the final reconstructed strings gives the answer.

### Complexity Analysis
- **Time Complexity**: O(n + m), where n and m are lengths of `s` and `t`. we process each character in both strings exactly once.
- **Space Complexity**: O(n + m), to store the processed strings in stacks before comparison.

---

## 4. Remove All Adjacent Duplicates In String
**Problem Statement**: You are given a string `s` consisting of lowercase English letters. A duplicate removal consists of choosing two adjacent and equal letters and removing them. Repeatedly make duplicate removals until no more can be made.

### Examples & Edge Cases
- **Example 1**: `s = "abbaca"` -> `"ca"`
- **Edge Case**: `s = "aaaaaaaa"` -> `""` (Empty string)

### Optimal Python Solution
```python
def removeDuplicates(s: str) -> str:
    stack = []

    for char in s:
        # If current char matches top of stack, we found an adjacent duplicate
        if stack and stack[-1] == char:
            stack.pop()
        else:
            stack.append(char)

    return "".join(stack)
```

### Explanation
We use a stack to build the string. For each character, we check if it matches the current "last" character in our processed string (the top of the stack). If it matches, they are adjacent duplicates, so we remove the existing one and skip the current one.

### Complexity Analysis
- **Time Complexity**: O(n), as we perform a single pass through the string, and each character is pushed or popped at most once.
- **Space Complexity**: O(n), for the stack in the worst case (no duplicates found).

---

## 5. Daily Temperatures
**Problem Statement**: Given an array of integers `temperatures`, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i-th` day to get a warmer temperature.

### Examples & Edge Cases
- **Example 1**: `temps = [73, 74, 75, 71, 69, 72, 76, 73]` -> `[1, 1, 4, 2, 1, 1, 0, 0]`
- **Edge Case**: Temperatures are strictly decreasing -> `[0, 0, 0, 0]`.

### Optimal Python Solution
```python
def dailyTemperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    ans = [0] * n
    stack = [] # Stores indices of temperatures

    for i, t in enumerate(temperatures):
        # While current temp is warmer than temp at stack top
        while stack and temperatures[stack[-1]] < t:
            prev_index = stack.pop()
            ans[prev_index] = i - prev_index
        stack.append(i)

    return ans
```

### Explanation
This is a classic Monotonic Stack problem. We maintain a stack of indices where temperatures are decreasing. When we find a temperature warmer than the one at the stack top, we've found the "next warmer day" for that earlier day.

### Complexity Analysis
- **Time Complexity**: O(n), because each index is pushed onto the stack once and popped at most once across the entire iteration.
- **Space Complexity**: O(n), to store the indices in the stack.

---

## 6. Min Stack
**Problem Statement**: Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

### Optimal Python Solution
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Push to min_stack if it's empty or val is new minimum
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

### Explanation
We use an auxiliary stack (`min_stack`) to keep track of the minimum value at every state of the main stack. When we push a value, if it's less than or equal to the current minimum, we push it to the `min_stack`. When we pop, if the value matches the `min_stack` top, we pop from both.

### Complexity Analysis
- **Time Complexity**: O(1) for all operations (push, pop, top, getMin) as we only use O(1) stack operations.
- **Space Complexity**: O(n), to store elements in the stacks.

---

## 7. Evaluate Reverse Polish Notation
**Problem Statement**: Evaluate the value of an arithmetic expression in Reverse Polish Notation (postfix). Valid operators are `+`, `-`, `*`, and `/`.

### Examples & Edge Cases
- **Example 1**: `["2","1","+","3","*"]` -> `((2 + 1) * 3) = 9`
- **Edge Case**: Negative results or division by larger numbers (truncation).

### Optimal Python Solution
```python
def evalRPN(tokens: list[str]) -> int:
    stack = []

    for t in tokens:
        if t not in "+-*/":
            stack.append(int(t))
        else:
            r, l = stack.pop(), stack.pop()
            if t == "+": stack.append(l + r)
            elif t == "-": stack.append(l - r)
            elif t == "*": stack.append(l * r)
            else: stack.append(int(l / r)) # Truncate toward zero

    return stack[0]
```

### Explanation
In RPN, operators follow their operands. We use a stack to store numbers. When we encounter an operator, we pop the last two numbers, apply the operator, and push the result back.

### Complexity Analysis
- **Time Complexity**: O(n), where n is the number of tokens. We process each token once, and all stack/arithmetic operations are O(1).
- **Space Complexity**: O(n), for the stack which can hold up to n operands.
