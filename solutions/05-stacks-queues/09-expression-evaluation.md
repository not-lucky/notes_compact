# Solution: Expression Evaluation Practice Problems

## Problem 1: Evaluate Reverse Polish Notation
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

---

## Problem 2: Basic Calculator
### Problem Statement
Given a string `s` representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.

Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as `eval()`.

### Constraints
- `1 <= s.length <= 3 * 10^5`
- `s` consists of digits, `'+'`, `'-'`, `'('`, `')'`, and `' '`.
- `s` represents a valid expression.
- `'+'` is not used as a unary operation (i.e., `"+1"` and `"+(2+3)"` is invalid).
- `'-'` could be used as a unary operation (i.e., `"-1"` and `"-(2+3)"` is valid).
- There will be no two consecutive operators in the input.
- Every number and running calculation will fit in a signed 32-bit integer.

### Example
Input: `s = "(1+(4+5+2)-3)+(6+8)"`
Output: `23`

### Python Implementation
```python
def calculate(s: str) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    stack = []
    res = 0
    num = 0
    sign = 1

    for char in s:
        if char.isdigit():
            num = num * 10 + int(char)
        elif char in "+-":
            res += sign * num
            num = 0
            sign = 1 if char == "+" else -1
        elif char == "(":
            stack.append(res)
            stack.append(sign)
            res = 0
            sign = 1
        elif char == ")":
            res += sign * num
            num = 0
            res *= stack.pop() # sign
            res += stack.pop() # prev_res

    return res + sign * num
```

---

## Problem 3: Basic Calculator II
### Problem Statement
Given a string `s` which represents an expression, evaluate this expression and return its value.

The integer division should truncate toward zero.

You may assume that the given expression is always valid. All intermediate results will be in the range of `[-2^31, 2^31 - 1]`.

Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as `eval()`.

### Constraints
- `1 <= s.length <= 3 * 10^5`
- `s` consists of digits, `'+'`, `'-'`, `'*'`, `'/'`, and `' '`.
- `s` represents a valid expression.
- All the integers in the expression are non-negative integers in the range `[0, 2^31 - 1]`.
- The answer is guaranteed to fit in a 32-bit integer.

### Example
Input: `s = " 3+5 / 2 "`
Output: `5`

### Python Implementation
```python
def calculate(s: str) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not s:
        return 0
    stack = []
    num = 0
    op = "+"

    for i, char in enumerate(s):
        if char.isdigit():
            num = num * 10 + int(char)
        if char in "+-*/" or i == len(s) - 1:
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            elif op == "/":
                top = stack.pop()
                stack.append(int(top / num))
            num = 0
            op = char

    return sum(stack)
```

---

## Problem 4: Decode String
### Problem Statement
Given an encoded string, return its decoded string.

The encoding rule is: `k[encoded_string]`, where the `encoded_string` inside the square brackets is being repeated exactly `k` times. Note that `k` is guaranteed to be a positive integer.

You may assume that the input string is always valid; there are no extra white spaces, square brackets are well-formed, etc. Furthermore, you may assume that the original data does not contain any digits and that digits are only for those repeat numbers, `k`. For example, there will not be input like `3a` or `2[4]`.

The test cases are generated so that the length of the output will never exceed `10^5`.

### Constraints
- `1 <= s.length <= 30`
- `s` consists of lowercase English letters, digits, and square brackets `'[]'`.
- `s` is guaranteed to be a valid input.
- All the integers in `s` are in the range `[1, 300]`.

### Example
Input: `s = "3[a2[c]]"`
Output: `"accaccacc"`

### Python Implementation
```python
def decodeString(s: str) -> str:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    stack = []
    curr_str = ""
    curr_num = 0

    for char in s:
        if char.isdigit():
            curr_num = curr_num * 10 + int(char)
        elif char == "[":
            stack.append((curr_str, curr_num))
            curr_str = ""
            curr_num = 0
        elif char == "]":
            prev_str, num = stack.pop()
            curr_str = prev_str + num * curr_str
        else:
            curr_str += char

    return curr_str
```
