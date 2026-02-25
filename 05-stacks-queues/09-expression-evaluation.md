# Expression Evaluation

> **Prerequisites:** [01-stack-basics](./01-stack-basics.md), [03-valid-parentheses](./03-valid-parentheses.md)

## Overview

Expression evaluation uses stacks to handle operator precedence and parentheses in mathematical expressions. The key insight is that stacks naturally handle nested structures (parentheses) and can defer operations until we know what comes next (precedence). This is how calculators and compilers work under the hood.

## Building Intuition

**Why do stacks solve expression evaluation?**

Two challenges make expressions tricky:

1. **Operator precedence**: `2 + 3 * 4` = 14, not 20 (multiply before add)
2. **Parentheses**: `(2 + 3) * 4` = 20 (override precedence)

**The Key Insight for Precedence**:

```
We can't evaluate an operator immediately because we don't know
what comes next. In "2 + 3 * 4", we can't compute "2 + 3" right away
because "*" has higher precedence and should happen first.

Solution: Delay low-precedence operations by pushing to a stack.
When we see a high-precedence operator, we evaluate it immediately.
```

**How Delayed Evaluation Works**:

```
Expression: 2 + 3 * 4

Token  Action                   Stack
2      Push 2                   [2]
+      Push + (wait for later)  [2, +] (can't compute yet)
3      Push 3                   [2, +, 3]
*      Higher precedence!       Keep 3, remember we need to multiply
4      Push 4                   [...]
End    Now evaluate:
       - 3 * 4 = 12 (high precedence first)
       - 2 + 12 = 14 (then lower precedence)
```

**The Key Insight for Parentheses**:

```
Parentheses create a "sub-expression" that must be evaluated completely
before continuing the outer expression. This is a nested structure!

Solution: When we see '(', save our current context and start fresh.
When we see ')', finish the sub-expression and restore context.
```

**How Parentheses Work**:

```
Expression: 1 - (2 + 3)

Token  Action                   Stack      Result
1      num = 1                  []         result = 0
-      result += 1*1 = 1        []         result = 1, sign = -1
(      Save context!            [1, -1]    result = 0, sign = 1
2      num = 2                  [1, -1]
+      result += 1*2 = 2        [1, -1]    result = 2, sign = 1
3      num = 3                  [1, -1]
)      result += 1*3 = 5        [1, -1]
       Pop sign: result *= -1   []         result = -5
       Pop old_result: += 1     []         result = -4
```

**Why Postfix (RPN) is Simpler**:

```
Infix:   2 + 3 * 4  (needs precedence rules)
Postfix: 2 3 4 * +  (no precedence needed!)

In postfix, operators come after their operands.
Evaluation: read left-to-right, apply each operator to the top two stack values.

2 3 4 * +
  Stack: [2]
  Stack: [2, 3]
  Stack: [2, 3, 4]
  * : pop 4, 3, push 3*4=12 → [2, 12]
  + : pop 12, 2, push 2+12=14 → [14]
```

## When NOT to Use Stack-Based Evaluation

Stack-based expression evaluation is wrong when:

1. **Expressions Are Simple**: For just `+` and `-` (no precedence issues), you can evaluate left-to-right without a stack.

2. **Expressions Are Parsed Already**: If you have an AST (abstract syntax tree), use recursive evaluation instead of stack manipulation.

3. **You Need Optimization**: For repeated evaluation of the same expression, compiling to bytecode or machine code is faster.

4. **Expressions Have Variables**: For expressions like `a + b * c`, you need a symbol table and more infrastructure.

5. **Custom Operators Exist**: For user-defined operators with custom precedence, parsing becomes more complex than stacks can easily handle.

**Alternative Approaches**:
| Scenario | Better Approach |
|----------|-----------------|
| Simple +/- only | Linear scan |
| Pre-parsed AST | Recursive tree traversal |
| Repeated evaluation | Compile to bytecode |
| Complex expressions | Parser generator (ANTLR, etc.) |

## Interview Context

Expression evaluation is a **classic interview topic** at FANG+ companies because:

1. **Stack mastery**: Tests understanding of operator precedence and stack usage
2. **Parsing skills**: Requires careful character-by-character processing
3. **Multiple variations**: Infix, postfix, prefix, with/without parentheses
4. **Real-world application**: Compilers, calculators, spreadsheet formulas

Interviewers use this to assess your ability to handle complex multi-step algorithms.

---

## Expression Notations

| Notation      | Example     | Evaluation Order       |
| ------------- | ----------- | ---------------------- |
| Infix         | `3 + 4 * 2` | Needs precedence rules |
| Postfix (RPN) | `3 4 2 * +` | Left to right          |
| Prefix        | `+ 3 * 4 2` | Right to left          |

### Why Postfix?

- No parentheses needed
- No operator precedence rules
- Simple left-to-right evaluation
- Used in HP calculators, stack-based VMs

---

## Pattern 1: Evaluate Reverse Polish Notation

```python
from typing import List

def eval_rpn(tokens: List[str]) -> int:
    """
    Evaluate expression in Reverse Polish Notation.

    LeetCode 150: Evaluate Reverse Polish Notation

    Time Complexity: $\Theta(n)$
    Space Complexity: $\Theta(n)$
    """
    stack = []

    for token in tokens:
        if token in '+-*/':
            b = stack.pop()  # Second operand (popped first)
            a = stack.pop()  # First operand

            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            else:  # Division truncates toward zero
                # int(a / b) works in Python to truncate towards zero
                result = int(a / b)

            stack.append(result)
        else:
            stack.append(int(token))

    return stack[0]


# Example
tokens = ["2", "1", "+", "3", "*"]
# ((2 + 1) * 3) = 9
print(eval_rpn(tokens))  # 9

tokens = ["4", "13", "5", "/", "+"]
# 4 + (13 / 5) = 4 + 2 = 6
print(eval_rpn(tokens))  # 6
```

### Step-by-Step Walkthrough

```
tokens = ["2", "1", "+", "3", "*"]

Token   Stack           Action
"2"     [2]             push number
"1"     [2, 1]          push number
"+"     [3]             pop 1, 2; push 2+1=3
"3"     [3, 3]          push number
"*"     [9]             pop 3, 3; push 3*3=9

Result: 9
```

---

## Pattern 2: Basic Calculator (Infix with +, -, parentheses)

```python
def calculate(s: str) -> int:
    """
    Evaluate expression with +, -, and parentheses.

    LeetCode 224: Basic Calculator

    Time Complexity: $\Theta(n)$
    Space Complexity: $\Theta(n)$
    """
    stack = []
    num = 0
    sign = 1  # 1 for positive, -1 for negative
    result = 0

    for char in s:
        if char.isdigit():
            num = num * 10 + int(char)

        elif char == '+':
            result += sign * num
            num = 0
            sign = 1

        elif char == '-':
            result += sign * num
            num = 0
            sign = -1

        elif char == '(':
            # Save current result and sign, start fresh
            stack.append(result)
            stack.append(sign)
            result = 0
            sign = 1

        elif char == ')':
            result += sign * num
            num = 0
            # Apply saved sign and add to saved result
            result *= stack.pop()  # sign before parenthesis
            result += stack.pop()  # result before parenthesis

    # Don't forget the last number
    result += sign * num

    return result


# Examples
print(calculate("1 + 1"))           # 2
print(calculate(" 2-1 + 2 "))       # 3
print(calculate("(1+(4+5+2)-3)+(6+8)"))  # 23
```

### Why Stack for Parentheses?

```
Expression: "1 - (2 + 3)"

Processing:
1. "1": num=1
2. "-": result=1, sign=-1
3. "(": stack=[1, -1], result=0, sign=1
4. "2": num=2
5. "+": result=2, sign=1
6. "3": num=3
7. ")": result=5, then result=5*(-1)+1=-4

The stack saves the "context" before entering parentheses.
```

---

## Pattern 3: Basic Calculator II (Infix with +, -, \*, /)

```python
def calculate_ii(s: str) -> int:
    """
    Evaluate expression with +, -, *, / (no parentheses).

    LeetCode 227: Basic Calculator II

    Time Complexity: $\Theta(n)$
    Space Complexity: $\Theta(n)$
    """
    stack = []
    num = 0
    prev_op = '+'

    for i, char in enumerate(s):
        if char.isdigit():
            num = num * 10 + int(char)

        if char in '+-*/' or i == len(s) - 1:
            if prev_op == '+':
                stack.append(num)
            elif prev_op == '-':
                stack.append(-num)
            elif prev_op == '*':
                stack.append(stack.pop() * num)
            elif prev_op == '/':
                # Integer division truncates toward zero
                top = stack.pop()
                stack.append(int(top / num))

            num = 0
            prev_op = char

    return sum(stack)


# Examples
print(calculate_ii("3+2*2"))     # 7
print(calculate_ii(" 3/2 "))     # 1
print(calculate_ii(" 3+5 / 2 ")) # 5
```

### How It Handles Precedence

```
Expression: "3 + 2 * 2"

Step by step:
char='3': num=3
char='+': prev_op='+', push 3, stack=[3], prev_op='+'
char='2': num=2
char='*': prev_op='+', push 2, stack=[3,2], prev_op='*'
char='2': num=2
end:      prev_op='*', pop 2, push 2*2=4, stack=[3,4]

Result: sum([3,4]) = 7

The trick: delay pushing until we see the next operator.
For * and /, we compute immediately with the top of stack.
```

---

## Pattern 4: Basic Calculator III (Full Expression)

```python
def calculate_iii(s: str) -> int:
    """
    Evaluate expression with +, -, *, / and parentheses.

    LeetCode 772: Basic Calculator III

    Time Complexity: $\Theta(n)$
    Space Complexity: $\Theta(n)$
    """
    def helper(s: List[str]) -> int:
        stack = []
        num = 0
        prev_op = '+'

        while s:
            char = s.pop(0)

            if char.isdigit():
                num = num * 10 + int(char)

            if char == '(':
                num = helper(s)  # Recursively evaluate parentheses

            if char in '+-*/)' or not s:
                if prev_op == '+':
                    stack.append(num)
                elif prev_op == '-':
                    stack.append(-num)
                elif prev_op == '*':
                    stack.append(stack.pop() * num)
                elif prev_op == '/':
                    # Integer division truncates toward zero
                    top = stack.pop()
                    stack.append(int(top / num))

                num = 0
                prev_op = char

            if char == ')':
                break

        return sum(stack)

    # Remove spaces and convert to list for easier processing
    s_list = list(s.replace(' ', ''))
    return helper(s_list)


# Examples
print(calculate_iii("1 + 1"))        # 2
print(calculate_iii("6-4 / 2"))      # 4
print(calculate_iii("2*(5+5*2)/3+(6/2+8)"))  # 21
```

---

## Pattern 5: Infix to Postfix Conversion

```python
def infix_to_postfix(expression: str) -> str:
    """
    Convert infix to postfix (Shunting Yard algorithm).

    Time Complexity: $\Theta(n)$
    Space Complexity: $\Theta(n)$
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    right_associative = {'^'}

    output = []
    operator_stack = []

    i = 0
    while i < len(expression):
        char = expression[i]

        if char.isdigit():
            # Collect multi-digit number
            num = []
            while i < len(expression) and expression[i].isdigit():
                num.append(expression[i])
                i += 1
            output.append(''.join(num))
            continue

        elif char == '(':
            operator_stack.append(char)

        elif char == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Remove '('

        elif char in precedence:
            while (operator_stack and
                   operator_stack[-1] != '(' and
                   operator_stack[-1] in precedence and
                   (precedence[operator_stack[-1]] > precedence[char] or
                    (precedence[operator_stack[-1]] == precedence[char] and
                     char not in right_associative))):
                output.append(operator_stack.pop())
            operator_stack.append(char)

        i += 1

    while operator_stack:
        output.append(operator_stack.pop())

    return ' '.join(output)


# Examples
print(infix_to_postfix("3 + 4 * 2"))       # "3 4 2 * +"
print(infix_to_postfix("(3 + 4) * 2"))     # "3 4 + 2 *"
print(infix_to_postfix("3 + 4 * 2 - 1"))   # "3 4 2 * + 1 -"
```

---

## Pattern 6: Decode String

```python
def decode_string(s: str) -> str:
    """
    Decode string like "3[a2[c]]" → "accaccacc".

    LeetCode 394: Decode String

    Time Complexity: $\Theta(\text{output length})$
    Space Complexity: $\Theta(n)$
    """
    stack = []
    current_string = ""
    current_num = 0

    for char in s:
        if char.isdigit():
            current_num = current_num * 10 + int(char)

        elif char == '[':
            # Save current state
            stack.append((current_string, current_num))
            current_string = ""
            current_num = 0

        elif char == ']':
            # Pop and apply repetition
            prev_string, num = stack.pop()
            current_string = prev_string + current_string * num

        else:
            current_string += char

    return current_string


# Examples
print(decode_string("3[a]2[bc]"))      # "aaabcbc"
print(decode_string("3[a2[c]]"))       # "accaccacc"
print(decode_string("2[abc]3[cd]ef"))  # "abcabccdcdcdef"
```

---

## Operator Precedence Summary

| Operator | Precedence  | Associativity |
| -------- | ----------- | ------------- |
| `^`      | 3 (highest) | Right         |
| `*`, `/` | 2           | Left          |
| `+`, `-` | 1 (lowest)  | Left          |

### Why Associativity Matters

```
Left associative: 8 - 4 - 2 = (8 - 4) - 2 = 2
Right associative: 2 ^ 3 ^ 2 = 2 ^ (3 ^ 2) = 2 ^ 9 = 512
```

---

## Common Mistakes

1. **Last number**: Don't forget to process the final number
2. **Division truncation**: `int(a / b)` truncates toward zero, not floor division (which `//` does)
3. **Negative numbers**: Handle unary minus (e.g., "-5 + 3")
4. **Spaces**: Skip spaces during parsing
5. **Empty string**: Handle empty input

---

## Division Truncation

```python
# Python's // is floor division (toward -∞)
print(7 // 3)    # 2
print(-7 // 3)   # -3 (floor)

# For truncation toward zero (like C/Java):
print(int(7 / 3))    # 2
print(int(-7 / 3))   # -2 (toward zero)
```

---

## Edge Cases

```python
# 1. Single number
calculate("42")  # 42

# 2. Leading/trailing spaces
calculate("  1 + 1  ")  # 2

# 3. Multiple digits
calculate("123 + 456")  # 579

# 4. Nested parentheses
calculate("((1 + 2))")  # 3

# 5. Negative result
calculate("1 - 5")  # -4

# 6. Division
calculate("7 / 3")  # 2 (truncated)
```

---

## Practice Problems

| #   | Problem                          | Difficulty | Key Concept           |
| --- | -------------------------------- | ---------- | --------------------- |
| 1   | Evaluate Reverse Polish Notation | Medium     | RPN evaluation        |
| 2   | Basic Calculator                 | Hard       | + - and ()            |
| 3   | Basic Calculator II              | Medium     | + - \* /              |
| 4   | Basic Calculator III             | Hard       | Full expression       |
| 5   | Decode String                    | Medium     | Nested encoding       |
| 6   | Number of Atoms                  | Hard       | Chemical formula      |
| 7   | Parse Lisp Expression            | Hard       | Nested function calls |

---

## Key Takeaways

1. **Stack for operators**: Hold operators until we can evaluate them
2. **Stack for parentheses**: Save context when entering, restore when leaving
3. **Postfix is simplest**: No precedence rules needed
4. **Process on next operator**: Delay evaluation until we know the next operator
5. **Recursion for nesting**: Treat parenthesized expressions as sub-problems

---

## Next: [10-histogram-problems.md](./10-histogram-problems.md)

Learn the classic monotonic stack application: largest rectangle in histogram.
