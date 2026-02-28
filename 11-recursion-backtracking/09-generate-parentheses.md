# 09. Generate Parentheses

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md)

## Core Concept

Generate Parentheses is a classic **sequence generation** backtracking problem. Given $n$ pairs of parentheses, you must generate all valid (well-formed) combinations. It is elegant because the constraint is simple—balance—yet it produces non-trivial results.

## Intuition & Mental Models

**Why does tracking open/close counts work?**

Think of it as maintaining a balance while building a sequence.

1. **The Balance Model**: Imagine parentheses as a bank account. `(` is a deposit (+1), `)` is a withdrawal (-1). The rules:
   - You can deposit anytime (as long as you haven't hit the max limit of $n$ deposits).
   - You can only withdraw if your balance is strictly positive (meaning you have unclosed opens).
   - At the end, the balance must be zero.

2. **The Decision Model**: At each position in the string, you make a binary decision:
   - **Branch 1 (Add `(`)**: Valid if `open_count < n`.
   - **Branch 2 (Add `)`)**: Valid if `close_count < open_count`.

3. **Why This Guarantees Validity**:
   - We never add `)` without a matching `(`.
   - We use exactly $n$ of each.
   - At every prefix, `opens ≥ closes` (balance never goes negative).

## Visualizing the Call Stack

```text
n=2, tracking (current_string, open_count, close_count)

                             "" (0,0)
                            /
                           ( (1,0)
                         /         \
                       (( (2,0)     () (1,1)
                       |             \
                      (() (2,1)       ()( (2,1)
                       |                \
                     (()) (2,2) ✓      ()() (2,2) ✓
```

*Note: We never even branch into invalid states like `)(` because of our strict constraints.*

## Basic Implementation (String Concatenation)

In Python, strings are immutable. `current + '('` creates a *brand new string* in $O(N)$ time. This means implicit backtracking happens automatically because the parent call's `current` string is untouched by the child.

```python
def generate_parenthesis(n: int) -> list[str]:
    result = []

    def backtrack(current: str, open_count: int, close_count: int):
        # Base case: string has reached max length 2n
        if len(current) == 2 * n:
            result.append(current)
            return

        # Decision 1: Add an open parenthesis
        if open_count < n:
            # String concatenation creates a new string; no explicit pop() needed
            backtrack(current + '(', open_count + 1, close_count)

        # Decision 2: Add a close parenthesis
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)

    backtrack("", 0, 0)
    return result
```

## Optimized Implementation (List Mutation)

For maximum performance, we should avoid creating a new string at every single node in the tree. Instead, we use a single shared list, push to it, recurse, and then explicitly `pop()` to restore state. This is true backtracking.

```python
def generate_parenthesis_optimized(n: int) -> list[str]:
    result = []

    # Path is a shared list across all recursive calls
    def backtrack(path: list[str], open_count: int, close_count: int):
        if len(path) == 2 * n:
            # Join once at the leaf node ($O(N)$) instead of at every step
            result.append("".join(path))
            return

        if open_count < n:
            path.append('(')  # Make choice
            backtrack(path, open_count + 1, close_count)
            path.pop()        # Undo choice (Backtrack)

        if close_count < open_count:
            path.append(')')  # Make choice
            backtrack(path, open_count, close_count + 1)
            path.pop()        # Undo choice (Backtrack)

    backtrack([], 0, 0)
    return result
```

## Complexity Analysis

- **Time Complexity:** $O\left(\frac{4^n}{\sqrt{n}}\right)$
  - This is bounded by the $n$-th Catalan number. At each leaf node, we do an $O(n)$ operation to join/copy the string, making the strict time complexity $O\left(n \cdot \text{Catalan}_n\right)$.
- **Space Complexity:**
  - **Auxiliary Space (Call Stack):** $O(n)$ maximum depth of the recursion tree (specifically $2n$ levels).
  - **Total Space:** $O\left(n \cdot \frac{4^n}{\sqrt{n}}\right)$ to store all the resulting valid strings in the output array.

## Common Pitfalls

1. **Checking `close < n` instead of `close < open`:**
   - If you only check `close < n`, you will generate invalid sequences like `())(`. You can *only* add a closing bracket if there is currently an unmatched open bracket.
2. **Forgetting to `.pop()` when using lists:**
   - If you use the optimized list approach, you *must* explicitly `pop()` after the recursive call returns. Otherwise, brackets from failed branches will leak into future branches.
3. **Using `result.append(path)` instead of joining:**
   - If you append the mutable list directly, all answers in your result array will reflect the final state of `path` (which becomes empty). Always append a snapshot: `"".join(path)` or `path[:]`.
