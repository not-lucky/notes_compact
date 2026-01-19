# Generate Parentheses

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md)

## Interview Context

Generate Parentheses tests:
1. **Valid sequence understanding**: When can we add '(' or ')'?
2. **Counting constraints**: Track open and close counts
3. **Tree visualization**: See the decision tree clearly
4. **Clean backtracking**: Simple state management

---

## Problem Statement

Given n pairs of parentheses, generate all valid combinations.

```
Input: n = 3
Output: ["((()))", "(()())", "(())()", "()(())", "()()()"]

Input: n = 2
Output: ["(())", "()()"]
```

---

## The Core Insight

At each position, we can add:
- `(` if we have remaining open parentheses (open < n)
- `)` if it would balance an open (close < open)

```
n = 2

                ""
              /    \
            (        X (can't start with ))
           / \
         ((   ()
         |   / \
       (()  ()(  X
         |    |
       (()) ()()

Valid: "(())", "()()"
```

---

## Approach 1: Backtracking (Recommended)

```python
def generate_parenthesis(n: int) -> list[str]:
    """
    Generate all valid parentheses combinations.

    Time: O(4^n / √n) - Catalan number
    Space: O(n) - recursion depth
    """
    result = []

    def backtrack(current: str, open_count: int, close_count: int):
        # Base case: used all parentheses
        if len(current) == 2 * n:
            result.append(current)
            return

        # Add open parenthesis if available
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)

        # Add close parenthesis if it balances an open
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)

    backtrack('', 0, 0)
    return result
```

### Visual Trace for n=2

```
backtrack("", 0, 0)
├── open < n: backtrack("(", 1, 0)
│   ├── open < n: backtrack("((", 2, 0)
│   │   └── close < open: backtrack("(()", 2, 1)
│   │       └── close < open: backtrack("(())", 2, 2) ✓
│   └── close < open: backtrack("()", 1, 1)
│       └── open < n: backtrack("()(", 2, 1)
│           └── close < open: backtrack("()()", 2, 2) ✓

Result: ["(())", "()()"]
```

---

## Approach 2: Using List (More Efficient)

String concatenation creates new strings. Using a list is faster.

```python
def generate_parenthesis_v2(n: int) -> list[str]:
    """Generate parentheses using list for efficiency."""
    result = []

    def backtrack(current: list[str], open_count: int, close_count: int):
        if len(current) == 2 * n:
            result.append(''.join(current))
            return

        if open_count < n:
            current.append('(')
            backtrack(current, open_count + 1, close_count)
            current.pop()  # Backtrack

        if close_count < open_count:
            current.append(')')
            backtrack(current, open_count, close_count + 1)
            current.pop()  # Backtrack

    backtrack([], 0, 0)
    return result
```

---

## Approach 3: Iterative (Build Level by Level)

```python
def generate_parenthesis_iterative(n: int) -> list[str]:
    """Generate parentheses iteratively."""
    # State: (current_string, open_count, close_count)
    queue = [('', 0, 0)]
    result = []

    while queue:
        current, open_count, close_count = queue.pop(0)

        if len(current) == 2 * n:
            result.append(current)
            continue

        if open_count < n:
            queue.append((current + '(', open_count + 1, close_count))

        if close_count < open_count:
            queue.append((current + ')', open_count, close_count + 1))

    return result
```

---

## Why This Works: Validity Invariant

The key insight is maintaining the invariant:
- At any point, `close_count ≤ open_count ≤ n`

This guarantees:
1. We never have more `)` than `(` at any prefix
2. We use exactly n of each

```
Valid:   ( ( ) ( ) )
counts:  1 2 1 2 1 0  (open - close is always ≥ 0)

Invalid: ( ) ) ( ) (
counts:  1 0 -1  ← negative means invalid!
```

---

## Catalan Numbers

The number of valid parentheses combinations is the nth Catalan number:

```
C(n) = (2n)! / ((n+1)! × n!)

n=1: 1     "( )"
n=2: 2     "( ( ) )", "( ) ( )"
n=3: 5
n=4: 14
n=5: 42
n=6: 132
```

Catalan numbers also count:
- Number of binary trees with n nodes
- Number of ways to triangulate a polygon
- Number of paths in a grid that don't cross the diagonal

---

## Related: Valid Parentheses Check

Check if a given string has valid parentheses.

```python
def is_valid(s: str) -> bool:
    """
    Check if parentheses string is valid.

    Time: O(n)
    Space: O(1)
    """
    balance = 0

    for char in s:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
            if balance < 0:
                return False

    return balance == 0
```

---

## Related: Minimum Add to Make Valid

Find minimum parentheses to add for validity.

```python
def min_add_to_make_valid(s: str) -> int:
    """
    Minimum parentheses to add for validity.

    Time: O(n)
    Space: O(1)
    """
    open_needed = 0  # Unmatched '('
    close_needed = 0  # Unmatched ')'

    for char in s:
        if char == '(':
            open_needed += 1
        elif char == ')':
            if open_needed > 0:
                open_needed -= 1
            else:
                close_needed += 1

    return open_needed + close_needed
```

---

## Related: Generate with Multiple Types

Generate valid combinations with multiple bracket types.

```python
def generate_multi_parenthesis(n: int) -> list[str]:
    """
    Generate valid combinations with (), [], {}.

    This is much more complex - needs stack-based validation.
    """
    # For interview, usually just () is asked
    # Mention this as a follow-up complexity
    pass
```

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Generate all | O(4^n / √n) | O(n) | Catalan number results |
| Check valid | O(n) | O(1) | Single pass |
| Min to add | O(n) | O(1) | Single pass |

---

## Edge Cases

- [ ] n = 0 → return [""] or []
- [ ] n = 1 → return ["()"]

---

## Common Mistakes

### 1. Wrong Condition for Close

```python
# WRONG: allows invalid sequences
if close_count < n:
    backtrack(current + ')', ...)

# CORRECT: must have open to match
if close_count < open_count:
    backtrack(current + ')', ...)
```

### 2. Not Backtracking with List

```python
current.append('(')
backtrack(current, ...)
# WRONG: forgetting to pop
# CORRECT:
current.pop()
```

### 3. Wrong Base Case

```python
# WRONG: checking only one count
if open_count == n:
    result.append(current)

# CORRECT: check total length
if len(current) == 2 * n:
    result.append(current)
```

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Generate Parentheses | Medium | Basic backtracking |
| 2 | Valid Parentheses | Easy | Stack matching |
| 3 | Minimum Add to Make Valid | Medium | Count unmatched |
| 4 | Longest Valid Parentheses | Hard | DP or stack |
| 5 | Remove Invalid Parentheses | Hard | BFS or backtracking |

---

## Interview Tips

1. **Start with conditions**: Explain when we can add ( or )
2. **Draw the tree**: Visualize the decision tree
3. **Mention Catalan**: Shows mathematical insight
4. **Use list for efficiency**: String concat is O(n) each
5. **Know related problems**: Valid check, min add

---

## Key Takeaways

1. Add `(` if open_count < n
2. Add `)` if close_count < open_count
3. Result count is the Catalan number C(n)
4. Use list + join for efficient string building
5. Maintain invariant: close ≤ open ≤ n at all times

---

## Next: [10-letter-combinations.md](./10-letter-combinations.md)

Learn to generate letter combinations from phone keypad.
