# Chapter 11: Recursion & Backtracking

## Overview

Recursion is a problem-solving technique where a function solves a problem by calling itself with simpler inputs. Backtracking extends recursion by **exploring possibilities and undoing choices** when they don't lead to solutions. Together, they're essential tools for solving constraint satisfaction problems, generating combinations, and searching through solution spaces.

## Building Intuition

**Why are recursion and backtracking so powerful?**

1. **The Power of Self-Similarity**: Many problems have structure that repeats at different scales. A binary tree is made of smaller binary trees. A maze is solved by solving smaller sub-mazes. When you recognize this self-similarity, recursion becomes natural.

2. **The Explore-Backtrack Pattern**: Think of backtracking as navigating a maze:
   - At each intersection (choice point), pick a path
   - Walk until you hit a dead end or find the goal
   - If dead end, return to the last intersection and try a different path
   - Repeat until you've found all solutions or exhausted all paths

3. **Why "Make Choice, Explore, Undo" Works**: By systematically trying every possibility and undoing choices that don't work, you guarantee finding all solutions without missing any. The key insight: **undoing is what makes exploration reusable**.

4. **Visual Intuition—The Decision Tree**:

```
Every backtracking problem is a tree traversal:

                [Start]
               /   |   \
          Choice1 Choice2 Choice3
            /        |        \
        [State1] [State2]  [State3]
           ✓        ✗          ...
         (valid)  (dead end→backtrack)

You're doing DFS on a tree of possible states.
```

5. **When It "Clicks"**: Backtracking clicks when you realize you're searching an implicit tree. The tree isn't stored in memory—it's defined by your choices. Each recursive call goes down one level; each return goes back up.

## When NOT to Use Backtracking

Backtracking is powerful but not always optimal:

1. **When Greedy Works**: If locally optimal choices lead to globally optimal solutions, greedy is O(n) vs backtracking's exponential. Example: activity selection.

2. **When DP Applies**: If subproblems overlap significantly and you only need optimal value (not all solutions), DP is polynomial vs backtracking's exponential.

3. **When BFS Finds It Faster**: For shortest path or minimum steps, BFS guarantees finding the shortest solution first. DFS/backtracking might explore long paths first.

4. **When Constraints Propagate Well**: Some constraint satisfaction problems (like Sudoku) benefit more from constraint propagation than brute backtracking.

5. **When n Is Large**: Backtracking is often O(2^n), O(n!), or worse. For n > 20, reconsider the approach.

**Red Flags Against Backtracking:**

- Problem asks for minimum/maximum → probably DP
- Only need one solution → BFS or greedy may be faster
- n > 20 in constraints → exponential won't work
- No "generate all" or "find all" in problem → likely not backtracking

---

## Why Recursion & Backtracking Matter

1. **Interview frequency**: Backtracking problems appear in ~25% of coding interviews
2. **Pattern recognition**: Many problems reduce to "generate all X" or "find all valid Y"
3. **Skill indicator**: Shows ability to think systematically about solution spaces
4. **Foundation for DP**: Understanding recursion is essential for dynamic programming

---

## The Core Insight

**Recursion** breaks a problem into smaller subproblems of the same type:

```
solve(problem) = combine(solve(smaller_problem_1), solve(smaller_problem_2), ...)
```

**Backtracking** explores all possibilities by making choices and undoing them:

```
for each choice:
    make choice
    if valid: explore further
    undo choice (backtrack)
```

---

## Recursion vs Backtracking

| Aspect    | Recursion            | Backtracking                |
| --------- | -------------------- | --------------------------- |
| Goal      | Compute result       | Find all solutions          |
| Structure | Divide and conquer   | Explore and undo            |
| State     | Usually return value | Usually modify shared state |
| Example   | Factorial, Fibonacci | N-Queens, Subsets           |

---

## Backtracking Patterns Overview

| Pattern                 | Problems               | Key Insight                  |
| ----------------------- | ---------------------- | ---------------------------- |
| Subsets                 | All subsets, power set | Include/exclude each element |
| Permutations            | All orderings          | Use remaining elements       |
| Combinations            | Choose k from n        | Order doesn't matter         |
| Constraint Satisfaction | N-Queens, Sudoku       | Place and validate           |
| Path Finding            | Word search, maze      | Explore grid with backtrack  |

---

## Chapter Contents

| #   | Topic                                                | Key Concepts                                 |
| --- | ---------------------------------------------------- | -------------------------------------------- |
| 01  | [Recursion Basics](./01-recursion-basics.md)         | Call stack, base cases, thinking recursively |
| 02  | [Subsets](./02-subsets.md)                           | Generate all subsets, power set              |
| 03  | [Permutations](./03-permutations.md)                 | Generate all orderings                       |
| 04  | [Combinations](./04-combinations.md)                 | Choose k elements from n                     |
| 05  | [Combination Sum](./05-combination-sum.md)           | Sum variants, duplicates                     |
| 06  | [N-Queens](./06-n-queens.md)                         | Classic constraint satisfaction              |
| 07  | [Sudoku Solver](./07-sudoku-solver.md)               | 9x9 constraint propagation                   |
| 08  | [Word Search](./08-word-search.md)                   | Grid-based path finding                      |
| 09  | [Generate Parentheses](./09-generate-parentheses.md) | Valid sequence generation                    |
| 10  | [Letter Combinations](./10-letter-combinations.md)   | Phone keypad combinations                    |

---

## The Backtracking Template

```python
def backtrack(state, choices, result):
    """
    Generic backtracking template.

    Args:
        state: Current partial solution
        choices: Available choices at this point
        result: Collection of all valid solutions
    """
    # Base case: found a valid solution
    if is_solution(state):
        result.append(state.copy())  # Save copy of state
        return

    # Try each choice
    for choice in choices:
        # Pruning: skip invalid choices early
        if not is_valid(state, choice):
            continue

        # Make choice
        state.add(choice)

        # Explore further
        backtrack(state, remaining_choices, result)

        # Undo choice (backtrack)
        state.remove(choice)
```

---

## Common Mistakes

1. **Forgetting to backtrack**: Always undo your choice after exploring
2. **Not copying state**: When saving solutions, copy the state (lists are mutable)
3. **Wrong pruning**: Pruning too aggressively misses solutions; too little wastes time
4. **Infinite recursion**: Ensure progress toward base case
5. **Duplicate solutions**: Handle duplicates by sorting and skipping

---

## Time Complexity

| Problem Type | Time      | Space | Why                           |
| ------------ | --------- | ----- | ----------------------------- |
| Subsets      | O(2^n)    | O(n)  | 2 choices per element         |
| Permutations | O(n!)     | O(n)  | n choices, then n-1, etc.     |
| Combinations | O(C(n,k)) | O(k)  | Binomial coefficient          |
| N-Queens     | O(n!)     | O(n)  | Worst case, all placements    |
| Sudoku       | O(9^81)   | O(1)  | Worst case, but pruning helps |

---

## Common Interview Problems by Company

| Company   | Favorite Backtracking Problems                        |
| --------- | ----------------------------------------------------- |
| Google    | Word Search II, N-Queens, Generate Parentheses        |
| Meta      | Subsets, Permutations, Letter Combinations            |
| Amazon    | Combination Sum, Word Search, Palindrome Partitioning |
| Microsoft | Sudoku Solver, N-Queens, Restore IP Addresses         |
| Apple     | Combinations, Generate Parentheses, Subsets II        |

---

## Quick Reference: When to Use Backtracking

```
Does the problem ask for "all" solutions or "generate all"?
    │
    ├── Yes → Likely backtracking
    │         │
    │         ├── Order matters? → Permutations pattern
    │         │
    │         ├── Order doesn't matter? → Subsets/Combinations pattern
    │         │
    │         └── Constraints to satisfy? → Constraint satisfaction
    │
    └── No → Consider DP or greedy first
              │
              └── But can I use backtracking to verify? → Sometimes useful
```

---

## Recursion vs Iteration

While most backtracking uses recursion, know that:

```python
# Recursive (cleaner, but uses call stack)
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Iterative (explicit stack, saves call stack space)
def factorial_iter(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

For interviews, recursive solutions are usually preferred for clarity unless:

- Recursion depth exceeds stack limit (Python default: ~1000)
- Interviewer specifically asks for iterative

---

## Start: [01-recursion-basics.md](./01-recursion-basics.md)

Begin with mastering recursion fundamentals before diving into backtracking.
