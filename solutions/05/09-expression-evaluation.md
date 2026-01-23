# Expression Evaluation

## Practice Problems

### 1. Evaluate Reverse Polish Notation
**Difficulty:** Medium
**Key Technique:** Stack for operands

```python
def eval_rpn(tokens: list[str]) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    stack = []
    for t in tokens:
        if t in "+-*/":
            b, a = stack.pop(), stack.pop()
            if t == "+": stack.append(a + b)
            elif t == "-": stack.append(a - b)
            elif t == "*": stack.append(a * b)
            else: stack.append(int(a / b))
        else:
            stack.append(int(t))
    return stack[0]
```

### 2. Basic Calculator ( + - ( ) )
**Difficulty:** Hard
**Key Technique:** Stack to save context (result, sign)

```python
def calculate(s: str) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    stack = []
    res, num, sign = 0, 0, 1
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c in "+-":
            res += sign * num
            num = 0
            sign = 1 if c == "+" else -1
        elif c == "(":
            stack.append(res)
            stack.append(sign)
            res, sign = 0, 1
        elif c == ")":
            res += sign * num
            num = 0
            res *= stack.pop() # sign
            res += stack.pop() # prev res
    return res + sign * num
```

### 3. Basic Calculator II ( + - * / )
**Difficulty:** Medium
**Key Technique:** Stack for deferred + / -

```python
def calculate_ii(s: str) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    stack = []
    num = 0
    op = "+"
    for i, c in enumerate(s):
        if c.isdigit():
            num = num * 10 + int(c)
        if c in "+-*/" or i == len(s) - 1:
            if op == "+": stack.append(num)
            elif op == "-": stack.append(-num)
            elif op == "*": stack.append(stack.pop() * num)
            elif op == "/": stack.append(int(stack.pop() / num))
            num = 0
            op = c
    return sum(stack)
```

### 4. Decode String
**Difficulty:** Medium
**Key Technique:** Stack for (prev_str, repeat_count)

```python
def decode_string(s: str) -> str:
    """
    Time: O(Output Length)
    Space: O(n)
    """
    stack = []
    curr_s = ""
    curr_n = 0
    for c in s:
        if c.isdigit():
            curr_n = curr_n * 10 + int(c)
        elif c == "[":
            stack.append((curr_s, curr_n))
            curr_s, curr_n = "", 0
        elif c == "]":
            prev_s, n = stack.pop()
            curr_s = prev_s + n * curr_s
        else:
            curr_s += c
    return curr_s
```
