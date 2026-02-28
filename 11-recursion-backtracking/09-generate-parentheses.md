# Generate Parentheses

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md), [Combinations](./04-combinations.md)

## Core Concept

Generate Parentheses is a classic **sequence generation** backtracking problem. Given $N$ pairs of parentheses, you must generate all valid (well-formed) combinations. It elegantly demonstrates how to build combinations while enforcing mathematical constraints on the fly, preventing invalid branches from ever being explored.

## Intuition & Mental Models

**Why does tracking open/close counts work?**

Think of it as maintaining a balance while building a sequence.

1. **The Balance Model**: Imagine parentheses as a bank account. `(` is a deposit (+1), `)` is a withdrawal (-1). The rules:
   - You can deposit anytime (as long as you haven't hit the max limit of $N$ deposits).
   - You can only withdraw if your balance is strictly positive (meaning you have unclosed opens).
   - At the end, the balance must be exactly zero.

2. **The Decision Model**: At each step of building the string, you make a binary choice:
   - **Branch 1 (Add `(`)**: Valid if `open_count < n`.
   - **Branch 2 (Add `)`)**: Valid if `close_count < open_count`.

3. **Why This Guarantees Validity**:
   - We never add `)` without a preceding matching `(`.
   - We use exactly $N$ of each.
   - At every prefix, `opens ≥ closes` (the balance never goes negative).

### Visualizing Valid State Generation

The power of this backtracking approach is that it **never generates invalid states**.

**The Decision Tree (N=2)**:

```text
State: (open_count, close_count, path)

                             (0, 0, "")
                                 |
                             (1, 0, "(")
                           /             \
                  (2, 0, "((")         (1, 1, "()")
                     |                      |
                  (2, 1, "(()")        (2, 1, "()(")
                     |                      |
                  (2, 2, "(())")       (2, 2, "()()")
                     ✓                      ✓
```

*Notice how we never branch into invalid states like `)(` because `close_count < open_count` prevents it.*

## Basic Implementation: String Concatenation

In Python, strings are immutable. Using `current + '('` creates a *brand new string* in $\mathcal{O}(L)$ time (where $L$ is the string length). This implicit state cloning means we don't need to explicitly `pop()` or restore state, as the parent call's `current` string is untouched by the child's mutations.

While elegant and simple to write, creating a new string at every node of the recursive tree has poor performance characteristics.

```python
def generate_parenthesis(n: int) -> list[str]:
    result = []

    def backtrack(current: str, open_count: int, close_count: int):
        # Base case: sequence has reached max length 2n
        if len(current) == 2 * n:
            result.append(current)
            return

        # Decision 1: Add an open parenthesis
        if open_count < n:
            # String concatenation creates a new string; no explicit pop() needed
            backtrack(current + '(', open_count + 1, close_count)

        # Decision 2: Add a close parenthesis
        if close_count < open_count:
            # Safe because open_count > close_count guarantees we have unclosed '('
            backtrack(current + ')', open_count, close_count + 1)

    backtrack("", 0, 0)
    return result
```

## Optimized Implementation: State Mutation and Restoration

For maximum performance, we should avoid creating a new string at every single node in the tree. Instead, we use a single shared list (mutable), push to it, recurse, and then explicitly `pop()` to restore state. This is true backtracking.

```python
def generate_parenthesis_optimized(n: int) -> list[str]:
    result = []

    # path is a shared list across all recursive calls
    def backtrack(open_count: int, close_count: int, path: list[str]):
        # Base case
        if len(path) == 2 * n:
            # Join once at the leaf node (\mathcal{O}(N)) instead of at every step
            result.append("".join(path))
            return

        # 1. Mutate state, recurse, restore state (Backtrack) for '('
        if open_count < n:
            path.append('(')
            backtrack(open_count + 1, close_count, path)
            path.pop()

        # 2. Mutate state, recurse, restore state (Backtrack) for ')'
        if close_count < open_count:
            path.append(')')
            backtrack(open_count, close_count + 1, path)
            path.pop()

    backtrack(0, 0, [])
    return result
```

## Complexity Analysis

Let $N$ be the number of parenthesis pairs. The number of valid combinations is governed by the $N$-th Catalan number, $C_N = \frac{1}{n+1} \binom{2n}{n}$.

- **Time Complexity**: Loose upper bound $\mathcal{O}\left(N \cdot \frac{4^N}{\sqrt{N}}\right)$
  - Generating all valid sequences takes time proportional to the Catalan number, which is bounded asymptotically by $\frac{4^N}{N\sqrt{N}}$.
  - At each leaf node, we perform an $\mathcal{O}(N)$ operation to join the characters into a string.
  - Overall time complexity simplifies to $\mathcal{O}\left(N \cdot \frac{4^N}{\sqrt{N}}\right)$.
- **Space Complexity**:
  - **Auxiliary Space**: $\mathcal{O}(N)$
    - The maximum depth of the call stack is $2N$. The `path` list also takes $\mathcal{O}(N)$ space.
  - **Total Space (including Output)**: $\mathcal{O}\left(N \cdot \frac{4^N}{\sqrt{N}}\right)$
    - We store exactly $C_N$ strings, each of length $2N$, in our output array.

## Common Pitfalls

1. **Checking `close_count < n` instead of `close_count < open_count`**:
   - If you only check `close_count < n`, you will generate invalid sequences like `())(`. You can *only* add a closing bracket if there is currently an unmatched open bracket.
2. **Forgetting to `.pop()` when using mutable lists**:
   - If you use the optimized list approach, you *must* explicitly `pop()` after the recursive call returns. Otherwise, characters from failed or completed branches will leak into future branches, corrupting the shared `path`.
3. **Using `result.append(path)` instead of joining**:
   - If you append the mutable list reference directly, all answers in your result array will reflect the final state of `path` (which ends up empty). Always append a snapshot: `"".join(path)` or `path[:]`.
