# Valid Parentheses

> **Prerequisites:** [01-stack-basics](./01-stack-basics.md)

## Overview

The valid parentheses problem asks whether a string of brackets is properly nested and matched. It's the quintessential stack problem—demonstrating why LIFO ordering naturally solves nested structure validation. Every closing bracket must match the most recently opened unmatched bracket.

## Building Intuition

**Why does a stack solve bracket matching?**

Think about how you naturally check brackets in your head:

1. **When you see an opening bracket**: You "remember" it needs a match. You're adding a mental note.

2. **When you see a closing bracket**: You check if it matches your "most recent unmatched opening." If it does, you can forget that opening bracket.

3. **Why "most recent"?**: Because of nesting! In `([])`, when you see `]`, you must match the `[` that opened most recently—not the `(` that opened first.

**The Core Insight**:

```
Nested structures have an "inside-out" property: the innermost
pair must close before outer pairs. This is exactly LIFO ordering.
```

**Visual proof of why stack works**:

```
Expression: ( [ { } ] )
            ↑
            Open '(' - push, wait for match
              ↑
              Open '[' - push, wait for match
                ↑
                Open '{' - push, wait for match
                  ↑
                  Close '}' - must match top ('{') ✓
                    ↑
                    Close ']' - must match top ('[') ✓
                      ↑
                      Close ')' - must match top ('(') ✓

The closing order is exactly reverse of opening order. That's LIFO.
```

**Why NOT a queue or counter?**: A simple counter (count + for open, - for close) fails because it doesn't track types. `([)]` has balanced counts but wrong order. A queue fails because `)][(` would incorrectly match `[` with `]` when we need LIFO matching.

**Mental Model**: Imagine stacking plates with colors. You stack red, then blue, then green. When removing, you must remove green first, then blue, then red. If someone hands you a blue lid, it doesn't fit the green plate on top—invalid!

## When NOT to Use This Pattern

The stack-based parentheses pattern is wrong when:

1. **Order Doesn't Matter**: If you just need to count if there are equal opens and closes (not caring about nesting), simple counters work. Example: "Do we have same number of `(` and `)`?" doesn't need a stack.

2. **Wildcards Allow Flexibility**: For problems like "valid parenthesis string with `*`" (where `*` can be anything), the stack approach becomes complex. Greedy range tracking often works better.

3. **Single Bracket Type**: For just `()`, you don't need a stack at all—just count balance and ensure it never goes negative.

4. **Non-Nested Matching**: If brackets don't need to nest properly (like HTML tags that can overlap), stack matching doesn't apply.

**Simpler Alternative for Single Type**:

```python
# No stack needed for just '(' and ')'
def is_valid_simple(s: str) -> bool:
    """
    Check if a string of simple parentheses is valid.

    Time: $\mathcal{O}(N)$ - single pass
    Space: $\mathcal{O}(1)$ - constant extra space
    """
    balance = 0
    for c in s:
        if c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
            if balance < 0:  # More closes than opens so far
                return False
    return balance == 0
```

## Interview Context

The valid parentheses problem is one of the most common interview questions because:

1. **Classic stack application**: Perfect demonstration of LIFO matching
2. **Edge case rich**: Tests attention to detail with empty strings, single chars, etc.
3. **Foundation for harder problems**: Expression parsing, HTML validation, nested structures
4. **Quick to code**: Easy to explain, implement, and verify in 10-15 minutes

Interviewers use this to assess your understanding of stacks and ability to handle edge cases cleanly.

---

## The Problem

Given a string containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['`, and `']'`, determine if the input string is valid.

A string is valid if:

1. Open brackets are closed by the same type of brackets
2. Open brackets are closed in the correct order
3. Every close bracket has a corresponding open bracket

```
Examples:
"()"        → true
"()[]{}"    → true
"(]"        → false
"([)]"      → false  (wrong order)
"([{}])"    → true   (nested correctly)
```

---

## Visual Pattern

```
Valid: "([{}])"

Step by step:
  char    stack         action
  '('     ['(']         push
  '['     ['(', '[']    push
  '{'     ['(', '[', '{'] push
  '}'     ['(', '[']    pop (matches '{')
  ']'     ['(']         pop (matches '[')
  ')'     []            pop (matches '(')
  end     []            ✓ empty = valid

Invalid: "([)]"

  char    stack         action
  '('     ['(']         push
  '['     ['(', '[']    push
  ')'     -             ✗ ')' doesn't match '[' at top
```

---

## Core Solution

```python
def is_valid(s: str) -> bool:
    """
    Check if parentheses are valid.

    Time: $\mathcal{O}(N)$ - single pass through string
    Space: $\mathcal{O}(N)$ - stack can hold all opening brackets
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping:
            # Closing bracket: check if it matches the top
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            # Opening bracket: push onto stack
            stack.append(char)

    # Valid only if all brackets matched
    return len(stack) == 0
```

### Why This Works

1. **Opening brackets**: Push onto stack (waiting for match)
2. **Closing brackets**: Must match most recent unmatched opening bracket (stack top)
3. **End check**: All opening brackets must have been matched (stack empty)

---

## Alternative Implementation

```python
def is_valid_v2(s: str) -> bool:
    """
    Alternative using set for opening brackets.

    Time: $\mathcal{O}(N)$
    Space: $\mathcal{O}(N)$
    """
    stack = []
    opening = {'(', '[', '{'}
    pairs = {'(': ')', '[': ']', '{': '}'}

    for char in s:
        if char in opening:
            stack.append(char)
        else:
            # char is closing bracket
            if not stack:
                return False
            if pairs[stack[-1]] != char:
                return False
            stack.pop()

    return len(stack) == 0
```

---

## Common Variations

### Variation 1: Remove Invalid Parentheses

```python
def min_remove_to_make_valid(s: str) -> str:
    """
    Remove minimum parentheses to make string valid.

    LeetCode 1249: Minimum Remove to Make Valid Parentheses

    Time: $\mathcal{O}(N)$
    Space: $\mathcal{O}(N)$
    """
    # Track indices of invalid parentheses
    indices_to_remove = set()
    stack = []  # Stack of indices of '('

    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                stack.pop()  # Matched
            else:
                indices_to_remove.add(i)  # Unmatched ')'

    # Any remaining '(' are unmatched
    indices_to_remove.update(stack)

    return ''.join(c for i, c in enumerate(s) if i not in indices_to_remove)


# Examples
print(min_remove_to_make_valid("lee(t(c)o)de)"))  # "lee(t(c)o)de"
print(min_remove_to_make_valid("a)b(c)d"))        # "ab(c)d"
print(min_remove_to_make_valid("))(("))           # ""
```

### Variation 2: Longest Valid Parentheses

```python
def longest_valid_parentheses(s: str) -> int:
    """
    Find length of longest valid parentheses substring.

    LeetCode 32: Longest Valid Parentheses

    Time: $\mathcal{O}(N)$
    Space: $\mathcal{O}(N)$
    """
    # Stack stores indices; start with -1 as base
    stack = [-1]
    max_length = 0

    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        else:  # ')'
            stack.pop()
            if not stack:
                # No matching '(', push current as new base
                stack.append(i)
            else:
                # Valid match, calculate length
                max_length = max(max_length, i - stack[-1])

    return max_length


# Examples
print(longest_valid_parentheses("(()"))     # 2
print(longest_valid_parentheses(")()())"))  # 4
print(longest_valid_parentheses("()(())"))  # 6
```

### Variation 3: Score of Parentheses

```python
def score_of_parentheses(s: str) -> int:
    """
    Calculate score: () = 1, AB = A + B, (A) = 2 * A.

    LeetCode 856: Score of Parentheses

    Time: $\mathcal{O}(N)$
    Space: $\mathcal{O}(N)$
    """
    stack = [0]  # Stack of scores at each depth

    for char in s:
        if char == '(':
            stack.append(0)  # New depth starts with 0
        else:
            # Pop inner score and compute
            inner = stack.pop()
            # () = 1, (A) = 2*A
            score = max(1, 2 * inner)
            stack[-1] += score  # Add to outer scope

    return stack[0]


# Examples
print(score_of_parentheses("()"))      # 1
print(score_of_parentheses("(())"))    # 2
print(score_of_parentheses("()()"))    # 2
print(score_of_parentheses("(()(()))"))  # 6
```

### Variation 4: Generate All Valid Combinations

```python
def generate_parentheses(n: int) -> list[str]:
    """
    Generate all valid combinations of n pairs.

    LeetCode 22: Generate Parentheses

    Time: $\mathcal{O}(4^N / \sqrt{N})$ - Catalan number bound
    Space: $\mathcal{O}(N)$ for recursion stack
    """
    result = []

    def backtrack(current: str, open_count: int, close_count: int):
        if len(current) == 2 * n:
            result.append(current)
            return

        # Can add '(' if we haven't used all n
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)

        # Can add ')' only if there are unmatched '('
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)

    backtrack("", 0, 0)
    return result


# Example
print(generate_parentheses(3))
# ['((()))', '(()())', '(())()', '()(())', '()()()']
```

### Variation 5: Check Valid String with Wildcards

```python
def check_valid_string(s: str) -> bool:
    """
    Check validity where '*' can be '(', ')', or empty.

    LeetCode 678: Valid Parenthesis String

    Time: $\mathcal{O}(N)$
    Space: $\mathcal{O}(1)$
    """
    # Track range of possible open count
    low = 0   # Minimum possible open '(' count
    high = 0  # Maximum possible open '(' count

    for char in s:
        if char == '(':
            low += 1
            high += 1
        elif char == ')':
            low -= 1
            high -= 1
        else:  # '*'
            low -= 1   # '*' as ')'
            high += 1  # '*' as '('

        if high < 0:
            return False  # Too many ')'

        low = max(low, 0)  # low can't be negative

    return low == 0


# Examples
print(check_valid_string("(*)"))   # True
print(check_valid_string("(*))"))  # True
print(check_valid_string("*("))    # False
```

---

## Complexity Analysis

| Approach                  | Time | Space | Notes                            |
| ------------------------- | ---- | ----- | -------------------------------- |
| Stack-based               | $\mathcal{O}(N)$ | $\mathcal{O}(N)$  | Standard approach                |
| Count-based (single type) | $\mathcal{O}(N)$ | $\mathcal{O}(1)$  | Only works for one bracket type  |
| Two-pass counter          | $\mathcal{O}(N)$ | $\mathcal{O}(1)$  | Alternative for one bracket type |

---

## Edge Cases

```python
# 1. Empty string
is_valid("")  # True (vacuously valid)

# 2. Single character
is_valid("(")  # False
is_valid(")")  # False

# 3. Odd length (quick check)
if len(s) % 2 == 1:
    return False  # Can't be valid

# 4. Wrong order but equal counts
is_valid(")(")  # False
is_valid("([)]")  # False

# 5. Only one type
is_valid("(((()))))")  # False (extra ')')

# 6. Long nested
is_valid("(" * 5000 + ")" * 5000)  # True
```

---

## Optimizations

### Early Termination

```python
def is_valid_optimized(s: str) -> bool:
    """
    Optimized with early termination.

    Time: $\mathcal{O}(N)$
    Space: $\mathcal{O}(N)$
    """
    # Quick length check
    if len(s) % 2 == 1:
        return False

    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            # Early termination: more than n/2 opens means invalid
            if len(stack) > len(s) // 2:
                return False
            stack.append(char)

    return len(stack) == 0
```

---

## Interview Tips

1. **Start with brute force explanation**: "Match each closing with nearest unmatched opening"
2. **Explain why stack works**: LIFO matches nested structure
3. **Use a mapping**: Cleaner than multiple if-else
4. **Handle edge cases upfront**: Empty string, odd length
5. **Test with examples**: Walk through at least one valid and one invalid

---

## Practice Problems

| #   | Problem                      | Difficulty | Key Concept          |
| --- | ---------------------------- | ---------- | -------------------- |
| 1   | Valid Parentheses            | Easy       | Basic stack matching |
| 2   | Generate Parentheses         | Medium     | Backtracking         |
| 3   | Longest Valid Parentheses    | Hard       | Stack with indices   |
| 4   | Remove Invalid Parentheses   | Hard       | BFS or backtracking  |
| 5   | Minimum Remove to Make Valid | Medium     | Track indices        |
| 6   | Valid Parenthesis String     | Medium     | Two-pointer/range    |
| 7   | Score of Parentheses         | Medium     | Nested scoring       |

---

## Key Takeaways

1. **Stack is perfect**: LIFO ordering matches nested bracket structure
2. **Mapping simplifies code**: `{')': '(', ...}` is cleaner than if-else chains
3. **Check at end**: Stack must be empty for all brackets to match
4. **Indices for variations**: Store positions instead of characters for removal problems
5. **Odd length shortcut**: Odd-length strings can never be valid

---

## Next: [04-monotonic-stack.md](./04-monotonic-stack.md)

Learn the powerful monotonic stack pattern for "next greater element" problems.
