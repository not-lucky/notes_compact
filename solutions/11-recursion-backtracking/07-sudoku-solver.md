# Sudoku Solver - Solutions

This document provides optimal solutions and detailed explanations for the practice problems related to Sudoku Solver.

---

## 1. Valid Sudoku

### Problem Statement

Determine if a `9 x 9` Sudoku board is valid. Only the filled cells need to be validated according to the following rules:

1. Each row must contain the digits `1-9` without repetition.
2. Each column must contain the digits `1-9` without repetition.
3. Each of the nine `3 x 3` sub-boxes of the grid must contain the digits `1-9` without repetition.

### Optimal Python Solution (Single Pass)

```python
def isValidSudoku(board: list[list[str]]) -> bool:
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == ".":
                continue

            # Box index formula: (r // 3) * 3 + (c // 3)
            box_idx = (r // 3) * 3 + (c // 3)

            if val in rows[r] or val in cols[c] or val in boxes[box_idx]:
                return False

            rows[r].add(val)
            cols[c].add(val)
            boxes[box_idx].add(val)

    return True
```

### Complexity Analysis

- **Time Complexity:** $O(1)$ - Fixed board size ($9 \times 9 = 81$ cells).
- **Space Complexity:** $O(1)$ - Fixed number of sets and elements.

---

## 2. Sudoku Solver

### Problem Statement

Write a program to solve a Sudoku puzzle by filling the empty cells. A sudoku solution must satisfy all of the following rules:

1. Each of the digits `1-9` must occur exactly once in each row.
2. Each of the digits `1-9` must occur exactly once in each column.
3. Each of the digits `1-9` must occur exactly once in each of the 9 `3x3` sub-boxes of the grid.

### Optimal Python Solution (Backtracking with Bitmasks)

Bitmasking significantly improves the constant factor for validity checks.

```python
def solveSudoku(board: list[list[str]]) -> None:
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empty_cells = []

    # Initialize constraints and find empty cells
    for r in range(9):
        for c in range(9):
            if board[r][c] != ".":
                digit = int(board[r][c]) - 1
                mask = 1 << digit
                rows[r] |= mask
                cols[c] |= mask
                boxes[(r // 3) * 3 + (c // 3)] |= mask
            else:
                empty_cells.append((r, c))

    def backtrack(idx):
        if idx == len(empty_cells):
            return True

        r, c = empty_cells[idx]
        box_idx = (r // 3) * 3 + (c // 3)

        # Get bits that are used in row, col, or box
        used = rows[r] | cols[c] | boxes[box_idx]

        # Try each digit 1-9
        for digit in range(9):
            if not (used & (1 << digit)):
                # Place digit
                mask = 1 << digit
                board[r][c] = str(digit + 1)
                rows[r] |= mask
                cols[c] |= mask
                boxes[box_idx] |= mask

                if backtrack(idx + 1):
                    return True

                # Backtrack
                board[r][c] = "."
                rows[r] &= ~mask
                cols[c] &= ~mask
                boxes[box_idx] &= ~mask

        return False

    backtrack(0)
```

### Detailed Explanation

1. **Bitmasking**: Instead of using sets, we use a 9-bit integer for each row, column, and box. If the $i$-th bit is 1, the digit $i+1$ is already used.
2. **Empty Cell List**: Pre-identifying the cells that need filling avoids redundant nested loops inside the recursive calls.
3. **Success Propagation**: The `backtrack` function returns a boolean. If a branch returns `True`, we immediately stop and propagate that `True` up the call stack to preserve the solved board.

### Complexity Analysis

- **Time Complexity:** $O(9^k)$ where $k$ is the number of empty cells. In practice, constraints prune the search space massively.
- **Space Complexity:** $O(k)$ for the recursion stack and the list of empty cells.

---

## 3. Design Sudoku (Puzzle Generator)

### Problem Statement

Design an algorithm to generate a valid Sudoku puzzle with a unique solution.

### Optimal Python Solution (Backtracking + Randomization)

```python
import random

def generateSudoku(difficulty=40):
    board = [["." for _ in range(9)] for _ in range(9)]

    def is_valid(r, c, val):
        for i in range(9):
            if board[r][i] == val or board[i][c] == val:
                return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if board[i][j] == val:
                    return False
        return True

    def fill_board():
        # Standard solver with randomized digit order
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    digits = list("123456789")
                    random.shuffle(digits)
                    for d in digits:
                        if is_valid(r, c, d):
                            board[r][c] = d
                            if fill_board(): return True
                            board[r][c] = "."
                    return False
        return True

    # 1. Generate a complete valid board
    fill_board()

    # 2. Remove cells based on difficulty
    # (Simplified: true uniqueness check requires a counter-solver)
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for i in range(difficulty):
        r, c = cells[i]
        board[r][c] = "."

    return board
```

### Detailed Explanation

1. **Randomized Filling**: We use the same backtracking logic as a solver but shuffle the digits 1-9 before trying them. This ensures we generate a different valid full board every time.
2. **Cell Removal**: To create a puzzle, we remove digits from the full board. A professional generator would check that removing a specific cell doesn't result in multiple possible solutions by running a modified solver that counts all possibilities.
