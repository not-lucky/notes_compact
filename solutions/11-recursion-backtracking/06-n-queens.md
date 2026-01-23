# Solution: N-Queens Practice Problems

## Problem 1: N-Queens
### Problem Statement
The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.
Given an integer `n`, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.

### Constraints
- `1 <= n <= 9`

### Example
Input: `n = 4`
Output: `[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]`

### Python Implementation
```python
def solveNQueens(n: int) -> list[list[str]]:
    """
    Time Complexity: O(n!)
    Space Complexity: O(n^2) for board
    """
    res = []
    board = [['.'] * n for _ in range(n)]

    cols = set()
    posDiag = set() # (r + c)
    negDiag = set() # (r - c)

    def backtrack(r):
        if r == n:
            copy = ["".join(row) for row in board]
            res.append(copy)
            return

        for c in range(n):
            if c in cols or (r + c) in posDiag or (r - c) in negDiag:
                continue

            cols.add(c)
            posDiag.add(r + c)
            negDiag.add(r - c)
            board[r][c] = "Q"

            backtrack(r + 1)

            cols.remove(c)
            posDiag.remove(r + c)
            negDiag.remove(r - c)
            board[r][c] = "."

    backtrack(0)
    return res
```

---

## Problem 2: N-Queens II
### Problem Statement
The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.
Given an integer `n`, return the number of distinct solutions to the n-queens puzzle.

### Constraints
- `1 <= n <= 9`

### Example
Input: `n = 4`
Output: `2`

### Python Implementation
```python
def totalNQueens(n: int) -> int:
    """
    Time Complexity: O(n!)
    Space Complexity: O(n)
    """
    cols = set()
    posDiag = set() # (r + c)
    negDiag = set() # (r - c)
    res = 0

    def backtrack(r):
        if r == n:
            nonlocal res
            res += 1
            return

        for c in range(n):
            if c in cols or (r + c) in posDiag or (r - c) in negDiag:
                continue

            cols.add(c)
            posDiag.add(r + c)
            negDiag.add(r - c)

            backtrack(r + 1)

            cols.remove(c)
            posDiag.remove(r + c)
            negDiag.remove(r - c)

    backtrack(0)
    return res
```

---

## Problem 3: Valid Sudoku
### Problem Statement
Determine if a `9 x 9` Sudoku board is valid. Only the filled cells need to be validated according to the following rules:
- Each row must contain the digits `1-9` without repetition.
- Each column must contain the digits `1-9` without repetition.
- Each of the nine `3 x 3` sub-boxes of the grid must contain the digits `1-9` without repetition.

### Constraints
- `board.length == 9`
- `board[i].length == 9`
- `board[i][j]` is a digit `1-9` or `'.'`.

### Example
Input: `board` (standard valid Sudoku)
Output: `true`

### Python Implementation
```python
def isValidSudoku(board: list[list[str]]) -> bool:
    """
    Time Complexity: O(1) - board size is fixed at 81 cells
    Space Complexity: O(1)
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    squares = [set() for _ in range(9)] # (r // 3) * 3 + (c // 3)

    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                continue
            val = board[r][c]
            square_idx = (r // 3) * 3 + (c // 3)

            if (val in rows[r] or
                val in cols[c] or
                val in squares[square_idx]):
                return False

            rows[r].add(val)
            cols[c].add(val)
            squares[square_idx].add(val)

    return True
```
