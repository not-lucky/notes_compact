# Valid Parentheses

## Problem Statement

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

A string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

**Example:**
```
Input: s = "()[]{}"
Output: true

Input: s = "(]"
Output: false

Input: s = "([)]"
Output: false

Input: s = "{[]}"
Output: true
```

## Approach

### Stack-Based Solution
1. Push opening brackets onto stack
2. For closing brackets, check if stack top matches
3. At end, stack should be empty

### Key Insight
The most recent unclosed opening bracket must match the current closing bracket (LIFO order).

## Implementation

```python
def is_valid(s: str) -> bool:
    """
    Check if parentheses are valid using stack.

    Time: O(n) - single pass
    Space: O(n) - stack can hold all characters
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping:  # Closing bracket
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:  # Opening bracket
            stack.append(char)

    return len(stack) == 0


def is_valid_alternative(s: str) -> bool:
    """
    Alternative implementation with explicit matching.
    """
    stack = []
    pairs = {'(': ')', '{': '}', '[': ']'}

    for char in s:
        if char in pairs:  # Opening bracket
            stack.append(char)
        else:  # Closing bracket
            if not stack:
                return False
            if pairs[stack.pop()] != char:
                return False

    return len(stack) == 0


def is_valid_with_counter(s: str) -> bool:
    """
    For single type of bracket, can use counter.
    Does NOT work for mixed brackets (can't detect "[)").

    Only valid for strings with one bracket type.
    """
    count = 0

    for char in s:
        if char == '(':
            count += 1
        elif char == ')':
            count -= 1
            if count < 0:  # More closing than opening
                return False

    return count == 0
```

## Complexity Analysis

| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n) | Single pass through string |
| Space | O(n) | Stack can contain all chars (e.g., "(((((") |

## Visual Walkthrough

```
s = "{[()]}"

Step 1: '{'  → push → stack: ['{']
Step 2: '['  → push → stack: ['{', '[']
Step 3: '('  → push → stack: ['{', '[', '(']
Step 4: ')'  → pop '(' matches → stack: ['{', '[']
Step 5: ']'  → pop '[' matches → stack: ['{']
Step 6: '}'  → pop '{' matches → stack: []

Stack empty → Valid!


s = "([)]"

Step 1: '('  → push → stack: ['(']
Step 2: '['  → push → stack: ['(', '[']
Step 3: ')'  → pop '[' ≠ '(' → Invalid!
```

## Edge Cases

1. **Empty string**: Valid (no brackets to match)
2. **Single character**: Invalid (unmatched)
3. **Only opening**: `"((("` → Invalid (stack not empty)
4. **Only closing**: `")))"` → Invalid (stack empty when popping)
5. **Correct order wrong type**: `"(]"` → Invalid
6. **Interleaved wrong**: `"([)]"` → Invalid
7. **Nested correct**: `"{[()]}"` → Valid

## Common Mistakes

1. **Not checking empty stack before pop**: Causes error
2. **Returning true when any match found**: Must check ALL
3. **Not checking stack is empty at end**: Unmatched opening brackets
4. **Using counter for mixed brackets**: Can't detect type mismatches

## Variations

### Minimum Add to Make Parentheses Valid
```python
def min_add_to_make_valid(s: str) -> int:
    """
    Find minimum '(' or ')' to add to make valid.

    Time: O(n)
    Space: O(1)
    """
    open_needed = 0  # Unmatched '(' needing ')'
    close_needed = 0  # Unmatched ')' needing '('

    for char in s:
        if char == '(':
            open_needed += 1
        elif open_needed > 0:
            open_needed -= 1
        else:
            close_needed += 1

    return open_needed + close_needed
```

### Minimum Remove to Make Valid Parentheses
```python
def min_remove_to_make_valid(s: str) -> str:
    """
    Remove minimum parentheses to make valid.

    Time: O(n)
    Space: O(n)
    """
    s = list(s)
    stack = []  # Indices of unmatched '('

    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                stack.pop()
            else:
                s[i] = ''  # Mark for removal

    # Remove unmatched '('
    for i in stack:
        s[i] = ''

    return ''.join(s)
```

### Longest Valid Parentheses
```python
def longest_valid_parentheses(s: str) -> int:
    """
    Find length of longest valid substring.

    Time: O(n)
    Space: O(n)
    """
    stack = [-1]  # Stack of indices, -1 as base
    max_length = 0

    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)  # New base
            else:
                max_length = max(max_length, i - stack[-1])

    return max_length


def longest_valid_dp(s: str) -> int:
    """
    DP approach.

    dp[i] = length of longest valid ending at i
    """
    if not s:
        return 0

    n = len(s)
    dp = [0] * n

    for i in range(1, n):
        if s[i] == ')':
            if s[i-1] == '(':
                # ...()
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
            elif dp[i-1] > 0:
                # ...))
                j = i - dp[i-1] - 1  # Potential matching '('
                if j >= 0 and s[j] == '(':
                    dp[i] = dp[i-1] + 2 + (dp[j-1] if j >= 1 else 0)

    return max(dp) if dp else 0
```

### Generate Parentheses
```python
def generate_parenthesis(n: int) -> list[str]:
    """
    Generate all valid combinations of n pairs.

    Time: O(4^n / sqrt(n)) - Catalan number
    Space: O(n) - recursion depth
    """
    result = []

    def backtrack(current: str, open_count: int, close_count: int):
        if len(current) == 2 * n:
            result.append(current)
            return

        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)

    backtrack('', 0, 0)
    return result
```

## Related Problems

- **Minimum Add to Make Parentheses Valid** - Count insertions needed
- **Minimum Remove to Make Valid Parentheses** - Remove characters
- **Longest Valid Parentheses** - Longest valid substring
- **Generate Parentheses** - Generate all valid combinations
- **Remove Invalid Parentheses** - BFS for minimum removals
- **Check If Word Is Valid After Substitutions** - Similar stack logic
