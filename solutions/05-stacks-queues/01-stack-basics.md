# Solution: Stack Basics Practice Problems

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

Input: `s = "(]"`
Output: `false`

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

## Problem 2: Baseball Game
### Problem Statement
You are keeping the scores for a baseball game with strange rules. At the beginning of the game, you start with an empty record.

You are given a list of strings `operations`, where `operations[i]` is the `i`th operation you must apply to the record and is one of the following:
- An integer `x`: Record a new score of `x`.
- `'+'`: Record a new score that is the sum of the previous two scores.
- `'D'`: Record a new score that is double the previous score.
- `'C'`: Invalidate the previous score, removing it from the record.

Return the sum of all the scores on the record after applying all the operations.

### Constraints
- `1 <= operations.length <= 1000`
- `operations[i]` is `"C"`, `"D"`, `"+"`, or a string representing an integer in the range `[-3 * 10^4, 3 * 10^4]`.

### Example
Input: `ops = ["5","2","C","D","+"]`
Output: `30`

### Python Implementation
```python
def calPoints(operations: list[str]) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    stack = []
    for op in operations:
        if op == '+':
            stack.append(stack[-1] + stack[-2])
        elif op == 'D':
            stack.append(2 * stack[-1])
        elif op == 'C':
            stack.pop()
        else:
            stack.append(int(op))
    return sum(stack)
```

---

## Problem 3: Backspace String Compare
### Problem Statement
Given two strings `s` and `t`, return `true` if they are equal when both are typed into empty text editors. `'#'` means a backspace character.

Note that after backspacing an empty text, the text will continue empty.

### Constraints
- `1 <= s.length, t.length <= 200`
- `s` and `t` only contain lowercase letters and `'#'` characters.

### Example
Input: `s = "ab#c", t = "ad#c"`
Output: `true`

### Python Implementation
```python
def backspaceCompare(s: str, t: str) -> bool:
    """
    Time Complexity: O(n + m)
    Space Complexity: O(n + m)
    """
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

---

## Problem 4: Remove All Adjacent Duplicates In String
### Problem Statement
You are given a string `s` consisting of lowercase English letters. A duplicate removal consists of choosing two adjacent and equal letters and removing them.

We repeatedly make duplicate removals on `s` until we no longer can.

Return the final string after all such duplicate removals have been made. It can be proven that the answer is unique.

### Constraints
- `1 <= s.length <= 10^5`
- `s` consists of lowercase English letters.

### Example
Input: `s = "abbaca"`
Output: `"ca"`

### Python Implementation
```python
def removeDuplicates(s: str) -> str:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    stack = []
    for char in s:
        if stack and stack[-1] == char:
            stack.pop()
        else:
            stack.append(char)
    return "".join(stack)
```

---

## Problem 5: Daily Temperatures
### Problem Statement
Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i`th day to get a warmer temperature. If there is no future day for which this is possible, keep `answer[i] == 0` instead.

### Constraints
- `1 <= temperatures.length <= 10^5`
- `30 <= temperatures[i] <= 100`

### Example
Input: `temperatures = [73,74,75,71,69,72,76,73]`
Output: `[1,1,4,2,1,1,0,0]`

### Python Implementation
```python
def dailyTemperatures(temperatures: list[int]) -> list[int]:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    n = len(temperatures)
    ans = [0] * n
    stack = [] # stores indices
    for i in range(n):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            prev_index = stack.pop()
            ans[prev_index] = i - prev_index
        stack.append(i)
    return ans
```

---

## Problem 6: Min Stack
### Problem Statement
Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the `MinStack` class:
- `MinStack()` initializes the stack object.
- `void push(int val)` pushes the element `val` onto the stack.
- `void pop()` removes the element on the top of the stack.
- `int top()` gets the top element of the stack.
- `int getMin()` retrieves the minimum element in the stack.

You must implement a solution with `O(1)` time complexity for each function.

### Constraints
- `-2^31 <= val <= 2^31 - 1`
- Methods `pop`, `top` and `getMin` operations will always be called on non-empty stacks.
- At most `3 * 10^4` calls will be made to `push`, `pop`, `top`, and `getMin`.

### Example
Input: `["MinStack","push","push","push","getMin","pop","top","getMin"]`, `[[],[-2],[0],[-3],[],[],[],[]]`
Output: `[null,null,null,null,-3,null,0,-2]`

### Python Implementation
```python
class MinStack:
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

---

## Problem 7: Evaluate Reverse Polish Notation
### Problem Statement
You are given an array of strings `tokens` that represents an arithmetic expression in a Reverse Polish Notation.

Evaluate the expression. Return an integer that represents the value of the expression.

Note that:
- The valid operators are `'+'`, `'-'`, `'*'`, and `'/'`.
- Each operand may be an integer or another expression.
- The division between two integers always truncates toward zero.
- There will not be any division by zero.
- The input represents a valid arithmetic expression in a reverse polish notation.
- The answer and all the intermediate calculations can be represented in a 32-bit integer.

### Constraints
- `1 <= tokens.length <= 10^4`
- `tokens[i]` is either an operator (`"+"`, `"-"`, `"*"` or `"/"`), or an integer in the range `[-200, 200]`.

### Example
Input: `tokens = ["2","1","+","3","*"]`
Output: `9`

### Python Implementation
```python
def evalRPN(tokens: list[str]) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    stack = []
    for token in tokens:
        if token not in "+-*/":
            stack.append(int(token))
            continue

        num2 = stack.pop()
        num1 = stack.pop()

        if token == '+':
            stack.append(num1 + num2)
        elif token == '-':
            stack.append(num1 - num2)
        elif token == '*':
            stack.append(num1 * num2)
        else:
            stack.append(int(num1 / num2))

    return stack[0]
```
