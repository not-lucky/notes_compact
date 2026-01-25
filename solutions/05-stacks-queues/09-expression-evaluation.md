# Expression Evaluation - Practice Solutions

This file provides optimal Python solutions and explanations for the practice problems listed in the Expression Evaluation notes.

## 1. Evaluate Reverse Polish Notation
**Problem Statement**: Evaluate the value of an arithmetic expression in Reverse Polish Notation (postfix). Valid operators are `+`, `-`, `*`, and `/`. Each operand may be an integer or another expression. Division between two integers should truncate toward zero.

### Examples & Edge Cases
- **Example**: `["10","6","9","3","+","-11","*","/","*","17","+","5","+"]` -> `22`
- **Edge Case**: Negative numbers in division (truncation behavior).
- **Edge Case**: Single token expression `["42"]`.

### Optimal Python Solution
```python
def evalRPN(tokens: list[str]) -> int:
    stack = []
    operators = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: int(a / b) # Python's int(/) truncates toward zero
    }

    for token in tokens:
        if token in operators:
            # Pop right operand first, then left
            r = stack.pop()
            l = stack.pop()
            stack.append(operators[token](l, r))
        else:
            # Token is a number
            stack.append(int(token))

    return stack[0]
```

### Explanation
Reverse Polish Notation (postfix) is easily evaluated using a stack. We process tokens from left to right:
1. If the token is a number, push it to the stack.
2. If the token is an operator, pop the top two numbers, apply the operator, and push the result back.
Note: For subtraction and division, the order of operands matters (the first one popped is the right operand).

### Complexity Analysis
- **Time Complexity**: O(n), where n is the number of tokens. We visit each token exactly once.
- **Space Complexity**: O(n), for the stack in the worst case (e.g., all numbers followed by all operators).

---

## 2. Basic Calculator
**Problem Statement**: Implement a basic calculator to evaluate a simple expression string containing non-negative integers, `+`, `-`, `(`, `)`, and spaces.

### Optimal Python Solution
```python
def calculate(s: str) -> int:
    stack = [] # Stores (result, sign) before a parenthesis
    curr_res = 0
    curr_num = 0
    sign = 1 # 1 for '+', -1 for '-'

    for char in s:
        if char.isdigit():
            curr_num = curr_num * 10 + int(char)
        elif char == '+':
            curr_res += sign * curr_num
            curr_num = 0
            sign = 1
        elif char == '-':
            curr_res += sign * curr_num
            curr_num = 0
            sign = -1
        elif char == '(':
            # Push current result and sign to save state
            stack.append(curr_res)
            stack.append(sign)
            # Reset for the sub-expression inside parentheses
            curr_res = 0
            sign = 1
        elif char == ')':
            # Complete the current sub-expression
            curr_res += sign * curr_num
            curr_num = 0
            # Apply the sign and result from before the parentheses
            curr_res *= stack.pop() # sign
            curr_res += stack.pop() # previous result

    return curr_res + (sign * curr_num)
```

### Explanation
We use a stack to handle nested parentheses. When we see an opening parenthesis `(`, we save our current `curr_res` and `sign` and start fresh. When we see a closing parenthesis `)`, we finish the sub-calculation, multiply it by the saved sign, and add it to the saved previous result.

---

## 3. Basic Calculator II
**Problem Statement**: Implement a basic calculator to evaluate a simple expression string containing non-negative integers, `+`, `-`, `*`, `/` and spaces. (No parentheses).

### Optimal Python Solution
```python
def calculate(s: str) -> int:
    if not s: return 0
    stack = []
    num = 0
    op = '+'

    for i, char in enumerate(s):
        if char.isdigit():
            num = num * 10 + int(char)
        if char in '+-*/' or i == len(s) - 1:
            if op == '+':
                stack.append(num)
            elif op == '-':
                stack.append(-num)
            elif op == '*':
                stack.append(stack.pop() * num)
            elif op == '/':
                # Handle truncation toward zero for negative numbers
                stack.append(int(stack.pop() / num))
            num = 0
            op = char

    return sum(stack)
```

### Explanation
Because `*` and `/` have higher precedence than `+` and `-`, we perform them immediately by popping the stack, calculating, and pushing back. `+` and `-` are essentially treated as positive/negative additions to the final sum.

---

## 4. Basic Calculator III
**Problem Statement**: Evaluate a string expression with `+`, `-`, `*`, `/`, `(`, and `)`.

### Optimal Python Solution (Recursive Approach)
```python
def calculate(s: str) -> int:
    def solve(it):
        stack = []
        num = 0
        op = '+'

        while it < len(s):
            char = s[it]
            if char.isdigit():
                num = num * 10 + int(char)
            if char == '(':
                num, it = solve(it + 1)
            if char in '+-*/)' or it == len(s) - 1:
                if op == '+': stack.append(num)
                elif op == '-': stack.append(-num)
                elif op == '*': stack.append(stack.pop() * num)
                elif op == '/': stack.append(int(stack.pop() / num))
                num = 0
                op = char
            if char == ')':
                return sum(stack), it
            it += 1
        return sum(stack)

    return solve(0)
```

---

## 5. Decode String
**Problem Statement**: Decode an encoded string like `3[a2[c]]` to `accaccacc`.

### Optimal Python Solution
```python
def decodeString(s: str) -> str:
    stack = [] # stores (prev_string, repeat_count)
    curr_str = ""
    curr_num = 0

    for char in s:
        if char.isdigit():
            curr_num = curr_num * 10 + int(char)
        elif char == '[':
            stack.append((curr_str, curr_num))
            curr_str = ""
            curr_num = 0
        elif char == ']':
            prev_str, num = stack.pop()
            curr_str = prev_str + num * curr_str
        else:
            curr_str += char

    return curr_str
```

---

## 6. Number of Atoms
**Problem Statement**: Given a chemical formula (e.g., `H2O`, `Mg(OH)2`), return the count of all elements.

### Optimal Python Solution
```python
from collections import Counter
import re

def countOfAtoms(formula: str) -> str:
    stack = [Counter()]
    i = 0
    n = len(formula)

    while i < n:
        if formula[i] == '(':
            stack.append(Counter())
            i += 1
        elif formula[i] == ')':
            i += 1
            # Get multiplier
            i_start = i
            while i < n and formula[i].isdigit(): i += 1
            mult = int(formula[i_start:i] or 1)

            top = stack.pop()
            for elem, count in top.items():
                stack[-1][elem] += count * mult
        else:
            # Get element name
            i_start = i
            i += 1
            while i < n and formula[i].islower(): i += 1
            elem = formula[i_start:i]
            # Get count
            i_start = i
            while i < n and formula[i].isdigit(): i += 1
            count = int(formula[i_start:i] or 1)
            stack[-1][elem] += count

    counts = stack[0]
    res = []
    for elem in sorted(counts.keys()):
        res.append(elem)
        if counts[elem] > 1: res.append(str(counts[elem]))
    return "".join(res)

---

## 7. Parse Lisp Expression
**Problem Statement**: Evaluate a Lisp-like expression.

### Optimal Python Solution
```python
def evaluate(expression: str) -> int:
    scope = [{}]

    def get_val(x):
        if x[0] in '-0123456789': return int(x)
        for s in reversed(scope):
            if x in s: return s[x]

    def parse(s):
        # Helper to split expression into tokens
        res, bal, start = [], 0, 0
        for i, c in enumerate(s):
            if c == '(': bal += 1
            elif c == ')': bal -= 1
            elif c == ' ' and bal == 0:
                res.append(s[start:i])
                start = i + 1
        res.append(s[start:])
        return res

    def solve(expr):
        if not expr.startswith('('): return get_val(expr)

        # Remove outer parentheses
        tokens = parse(expr[1:-1])
        cmd = tokens[0]

        if cmd == 'add':
            return solve(tokens[1]) + solve(tokens[2])
        if cmd == 'mult':
            return solve(tokens[1]) * solve(tokens[2])
        if cmd == 'let':
            scope.append(scope[-1].copy())
            for i in range(1, len(tokens) - 1, 2):
                scope[-1][tokens[i]] = solve(tokens[i+1])
            res = solve(tokens[-1])
            scope.pop()
            return res

    return solve(expression)
```
```
