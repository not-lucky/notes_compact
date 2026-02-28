# Chapter 11: Recursion & Backtracking

## Overview

Recursion is a problem-solving technique where a function solves a problem by calling itself with simpler inputs. Backtracking extends recursion by **exploring possibilities and undoing choices** when they do not lead to valid solutions. Together, they are essential tools for solving constraint satisfaction problems, generating combinations, and systematically searching through complex solution spaces.

## Mental Models

A backtracking problem is simply a Depth-First Search (DFS) on an implicit tree. The tree isn't stored in memory—it's defined dynamically by your choices.

Two primary mental models dictate how you map a problem to a recursive tree:

### 1. Include/Exclude (Binary Choices)

At each step, you make a binary decision about a single element: do I include it, or do I exclude it?

- **Tree Structure:** Every node has exactly 2 branches (Yes or No).
- **Depth (Level):** Corresponds to the index of the element being considered.
- **Best for:** Subsets, 0/1 Knapsack equivalents.

### 2. Suffix Selection (Iterating Through Choices)

At each step, you use a `for` loop to try every valid remaining option for the *current position*.

- **Tree Structure:** A node can have $N$ branches (one for each valid choice).
- **Depth (Level):** Corresponds to the size of the partial solution being built.
- **Best for:** Permutations, Combinations, N-Queens.

## Complexity & Strict Definitions

To analyze backtracking correctly in interviews, distinguish between:

1. **Auxiliary Space:** The memory consumed by the recursive call stack. This is directly proportional to the **max depth of the recursion tree**.
2. **Total Space:** The memory needed to store all final answers in your `result` array.
3. **Index Pointers over Slicing:** Never pass `array[1:]` or `string[1:]` in recursive calls, as this creates hidden $O(N)$ operations at every node. Always pass the reference to the original array/string and a `start_index` pointer.

## Chapter Contents

| #   | Topic                                                | Key Concepts                                   |
| --- | ---------------------------------------------------- | ---------------------------------------------- |
| 01  | [Recursion Basics](./01-recursion-basics.md)         | Call stack, base cases, recursion vs iteration |
| 02  | [Subsets](./02-subsets.md)                           | Include/exclude model, power sets              |
| 03  | [Permutations](./03-permutations.md)                 | Suffix selection, state tracking (visited)     |
| 04  | [Combinations](./04-combinations.md)                 | Suffix selection with a monotonic `start_idx`  |
| 05  | [Combination Sum](./05-combination-sum.md)           | Subsets with duplicates and infinite reuse     |
| 06  | [N-Queens](./06-n-queens.md)                         | 2D grid constraint propagation                 |
| 07  | [Sudoku Solver](./07-sudoku-solver.md)               | 2D grid backtracking with early exit pruning   |
| 08  | [Word Search](./08-word-search.md)                   | 2D matrix pathfinding and restoring visited    |
| 09  | [Generate Parentheses](./09-generate-parentheses.md) | Balanced sequence string generation            |
| 10  | [Letter Combinations](./10-letter-combinations.md)   | Pure Cartesian product mappings                |

---

## The Backtracking Blueprint

Every optimal backtracking solution mutates a shared state variable (usually a list) and explicitly restores it after returning from the recursive call.

```python
def solve_backtracking(nums: list[int]) -> list[list[int]]:
    result = []

    def backtrack(start_idx: int, current_path: list[int]):
        # 1. Base Case: Add a COPY of the path to results
        if is_solution(current_path):
            result.append(current_path[:])
            return

        # 2. Iterate through possible choices (Suffix Selection Model)
        for i in range(start_idx, len(nums)):

            # 3. Pruning: Skip invalid choices or duplicates
            if not is_valid(nums[i]):
                continue

            # 4. Make the choice
            current_path.append(nums[i])

            # 5. Explore further down the tree
            backtrack(i + 1, current_path)  # Pass i+1, NOT nums[i+1:]

            # 6. Undo the choice (Backtrack)
            current_path.pop()

    backtrack(0, [])
    return result
```

## Common Mistakes

1. **Not passing index pointers:** Passing slices `nums[i:]` instead of an index `i` degrades time complexity due to hidden $O(N)$ copies.
2. **Forgetting to append a copy:** `result.append(path)` stores a reference. Since `path` is mutated and eventually popped back to empty, `result` will just be a list of empty arrays. Always use `result.append(path[:])`.
3. **Missing the `.pop()`:** If you append to the shared list but forget to pop it off after `backtrack()` returns, state will leak across branches.

---

## Quick Reference: Time & Space Complexities

| Problem                       | Time Complexity           | Auxiliary Space (Stack) | Total Output Space                  |
| ----------------------------- | ------------------------- | ----------------------- | ----------------------------------- |
| Subsets                       | $O(N \cdot 2^N)$          | $O(N)$                  | $O(N \cdot 2^N)$                    |
| Permutations                  | $O(N \cdot N!)$           | $O(N)$                  | $O(N \cdot N!)$                     |
| Combinations ($N$ choose $K$) | $O(K \cdot \binom{N}{K})$ | $O(K)$                  | $O(K \cdot \binom{N}{K})$           |
| N-Queens                      | $O(N!)$                   | $O(N)$                  | $O(N^3)$ (for grid representations) |
| Phone Letters                 | $O(N \cdot 4^N)$          | $O(N)$                  | $O(N \cdot 4^N)$                    |

*Note: The multiplier (like $N$ or $K$) often comes from the cost of copying the `path` array at the base case.*
