# 10. Letter Combinations of a Phone Number

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md), [Combinations](./04-combinations.md)

## Core Concept

This problem requires generating all possible letter combinations that a given sequence of digits could represent on a standard telephone keypad. It is a pure **Cartesian product** problem—you are combining choices from independent groups.

## Intuition & Mental Models

Unlike constraint-satisfaction backtracking problems (like N-Queens or Generate Parentheses) where choices restrict future branches, here there are **no constraints** between choices. Picking 'a' for the first digit doesn't restrict what you can pick for the second.

We use the **Suffix Selection** mental model:

- The `level` of the tree corresponds to the current digit we are evaluating (driven by an `index` pointer).
- The `branches` represent iterating through every possible letter for that specific digit.

## Visualizing the Call Stack

```text
digits = "23"

Level 0 (idx 0):             ""
                          /  |  \
                         /   |   \
Level 1 (idx 1):        a    b    c     (mapped from '2')
                       /|\  /|\  /|\
Level 2 (idx 2):      d e f d e f d e f (mapped from '3')

Results: "ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"
```

## Basic Implementation (String Concatenation)

While creating new strings at every level works and implicitly handles backtracking state, it is an anti-pattern for strict performance because string concatenation in Python is $O(N)$. However, because $N$ is at most 4 for a single phone digit mapping, and max digits length is typically small (e.g. $N \le 4$), this is acceptable in many interviews.

```python
def letter_combinations(digits: str) -> list[str]:
    if not digits:
        return []

    phone_map = {
        '2': "abc", '3': "def", '4': "ghi", '5': "jkl",
        '6': "mno", '7': "pqrs", '8': "tuv", '9': "wxyz"
    }

    result = []

    def backtrack(idx: int, current_str: str):
        # Base case: reached the end of the input digits
        if idx == len(digits):
            result.append(current_str)
            return

        # Get the letters that the current digit maps to
        current_digit = digits[idx]
        possible_letters = phone_map[current_digit]

        # Iterate through all choices (Suffix Selection pattern)
        for letter in possible_letters:
            # current_str + letter creates a NEW string (implicit backtracking)
            backtrack(idx + 1, current_str + letter)

    backtrack(0, "")
    return result
```

## Optimized Implementation (List Mutation)

To be rigorous about performance and demonstrate senior-level understanding of Python's memory model, we use a single shared list and explicitly append and pop.

```python
def letter_combinations_optimized(digits: str) -> list[str]:
    if not digits:
        return []

    phone_map = {
        '2': "abc", '3': "def", '4': "ghi", '5': "jkl",
        '6': "mno", '7': "pqrs", '8': "tuv", '9': "wxyz"
    }

    result = []

    def backtrack(idx: int, path: list[str]):
        if idx == len(digits):
            # Join once at the leaf node
            result.append("".join(path))
            return

        possible_letters = phone_map[digits[idx]]

        for letter in possible_letters:
            path.append(letter)       # Make choice
            backtrack(idx + 1, path)  # Recurse
            path.pop()                # Undo choice (Backtrack)

    backtrack(0, [])
    return result
```

## Complexity Analysis

Let $N$ be the length of the `digits` string.

- **Time Complexity:** $O(N \cdot 4^N)$
  - In the worst case (e.g., input "7979"), each digit maps to 4 letters, creating $4^N$ leaf nodes.
  - At each leaf node, we perform an $O(N)$ operation to copy/join the path array into a string.
- **Space Complexity:**
  - **Auxiliary Space (Call Stack):** $O(N)$ depth of the recursion tree.
  - **Total Space:** $O(N \cdot 4^N)$ to store all combinations in the result list.

## Common Pitfalls

1. **Failing to handle empty input:**
   - If `digits` is `""`, a blind backtracking implementation might return `[""]`. The problem typically expects `[]` for an empty input string.
2. **Missing `pop()`:**
   - When using the optimized list approach, failing to `path.pop()` will result in accumulated letters from dead-end branches spilling over into valid ones.
3. **Hardcoding mappings incorrectly:**
   - Remember that `7` maps to 4 letters (`pqrs`) and `9` maps to 4 letters (`wxyz`). Assuming all map to 3 letters throws off exact time complexity analysis.
4. **Using $O(N)$ Slicing:**
   - Avoid passing sliced strings like `digits[1:]` in the recursive call. Always use an index pointer (`idx`). Passing `digits[1:]` adds a hidden $O(N)$ string copy at every recursive step, degrading time complexity.
