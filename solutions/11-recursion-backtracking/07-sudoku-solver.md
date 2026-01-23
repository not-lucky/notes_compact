# Solution: Sudoku Solver Practice Problems

## Problem 1: Sudoku Solver
### Problem Statement
Write a program to solve a Sudoku puzzle by filling the empty cells.
A sudoku solution must satisfy all of the following rules:
- Each of the digits `1-9` must occur exactly once in each row.
- Each of the digits `1-9` must occur exactly once in each column.
- Each of the digits `1-9` must occur exactly once in each of the 9 `3x3` sub-boxes of the grid.

The `'.'` character indicates empty cells.

### Constraints
- `board.length == 9`
- `board[i].length == 9`
- `board[i][j]` is a digit or `'.'`.
- It is guaranteed that the input board has only one solution.

### Example
Input: `board` (standard unsolved Sudoku)
Output: `board` (solved Sudoku)

### Python Implementation
```python
def solveSudoku(board: list[list[str]]) -> None:
    """
    Do not return anything, modify board in-place instead.
    Time Complexity: O(9^(n*n)) worst case
    Space Complexity: O(n*n)
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    squares = [set() for _ in range(9)]

    # 1. Initialize sets with current board values
    for r in range(9):
        for c in range(9):
            if board[r][c] != ".":
                val = board[r][c]
                rows[r].add(val)
                cols[c].add(val)
                squares[(r // 3) * 3 + (c // 3)].add(val)

    # 2. Define backtracking function
    def backtrack(r, c):
        # If at the end of a row, move to the next row
        if c == 9:
            return backtrack(r + 1, 0)
        # If all rows processed, board is solved
        if r == 9:
            return True

        # Skip filled cells
        if board[r][c] != ".":
            return backtrack(r, c + 1)

        # Try digits 1-9
        for val in "123456789":
            square_idx = (r // 3) * 3 + (c // 3)
            if (val not in rows[r] and
                val not in cols[c] and
                val not in squares[square_idx]):

                # Make choice
                board[r][c] = val
                rows[r].add(val)
                cols[c].add(val)
                squares[square_idx].add(val)

                if backtrack(r, c + 1):
                    return True

                # Undo choice
                board[r][c] = "."
                rows[r].remove(val)
                cols[c].remove(val)
                squares[square_idx].remove(val)

        return False

    backtrack(0, 0)
```
