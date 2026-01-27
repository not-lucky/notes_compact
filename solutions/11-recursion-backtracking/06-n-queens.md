# N-Queens Problem - Solutions

This document provides optimal solutions and detailed explanations for the practice problems related to N-Queens.

---

## 1. N-Queens

### Problem Statement
The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other. Given an integer `n`, return all distinct solutions to the n-queens puzzle. You may return the answer in any order. Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.

### Examples & Edge Cases
- **Input:** n = 4 → **Output:** [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
- **Input:** n = 1 → **Output:** [["Q"]]
- **Edge Case:** n = 2 or n = 3 (no solutions).

### Optimal Python Solution (Backtracking with Sets)
```python
def solveNQueens(n: int) -> list[list[str]]:
    res = []
    board = [['.' for _ in range(n)] for _ in range(n)]

    # Sets to keep track of columns and diagonals already occupied
    cols = set()
    pos_diag = set() # (r + c)
    neg_diag = set() # (r - c)

    def backtrack(r: int):
        if r == n:
            copy = ["".join(row) for row in board]
            res.append(copy)
            return

        for c in range(n):
            if c in cols or (r + c) in pos_diag or (r - c) in neg_diag:
                continue

            # Place queen
            cols.add(c)
            pos_diag.add(r + c)
            neg_diag.add(r - c)
            board[r][c] = 'Q'

            backtrack(r + 1)

            # Remove queen (backtrack)
            cols.remove(c)
            pos_diag.remove(r + c)
            neg_diag.remove(r - c)
            board[r][c] = '.'

    backtrack(0)
    return res
```

### Detailed Explanation
1. **Systematic Search**: We place queens row by row. This ensures we don't need to check horizontal attacks.
2. **Diagonal Math**:
   - For any cell on a **positive diagonal** (bottom-left to top-right), the sum of its coordinates `r + c` is constant.
   - For any cell on a **negative diagonal** (top-left to bottom-right), the difference of its coordinates `r - c` is constant.
3. **Efficiency**: Using `set()` allows $O(1)$ time complexity for checking if a placement is valid.

### Complexity Analysis
- **Time Complexity:** $O(N!)$ - In the first row, we have $N$ choices, in the second $\approx N-2$, and so on.
- **Space Complexity:** $O(N^2)$ - To store the board, and $O(N)$ for the recursion stack and sets.

---

## 2. N-Queens II

### Problem Statement
The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other. Given an integer `n`, return the number of distinct solutions to the n-queens puzzle.

### Optimal Python Solution (Backtracking with Bitmasks)
Bitmasking is often preferred for "count-only" problems as it's significantly faster.

```python
def totalNQueens(n: int) -> int:
    def backtrack(row, cols, diags, anti_diags):
        if row == n:
            return 1

        count = 0
        # Determine available positions using bitwise operations
        # A '0' bit means the position is available
        occupied = cols | diags | anti_diags
        # Mask ensures we only look at first n bits
        available = (~occupied) & ((1 << n) - 1)

        while available:
            # Get the lowest set bit (next position to try)
            position = available & -available
            # Clear that bit from available
            available &= available - 1

            count += backtrack(
                row + 1,
                cols | position,
                (diags | position) << 1,
                (anti_diags | position) >> 1
            )
        return count

    return backtrack(0, 0, 0, 0)
```

### Detailed Explanation
1. **Bit Representation**: Each bit in the integers `cols`, `diags`, and `anti_diags` represents an attack zone.
2. **Shifting Diagonals**: When moving to the next row:
   - The attack zone of a diagonal shifts left (`<< 1`).
   - The attack zone of an anti-diagonal shifts right (`>> 1`).
3. **Low-bit Trick**: `available & -available` isolates the rightmost `1` bit, giving us the next valid column to try in the current row.

### Complexity Analysis
- **Time Complexity:** $O(N!)$
- **Space Complexity:** $O(N)$ - Recursion stack.

---

## 3. Valid Sudoku

### Problem Statement
Determine if a `9 x 9` Sudoku board is valid. Only the filled cells need to be validated according to the following rules:
1. Each row must contain the digits 1-9 without repetition.
2. Each column must contain the digits 1-9 without repetition.
3. Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.

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

            # Calculate box index
            box_idx = (r // 3) * 3 + (c // 3)

            if val in rows[r] or val in cols[c] or val in boxes[box_idx]:
                return False

            rows[r].add(val)
            cols[c].add(val)
            boxes[box_idx].add(val)

    return True
```

### Complexity Analysis
- **Time Complexity:** $O(1)$ - Since the board is always $9 \times 9$, we perform exactly 81 iterations.
- **Space Complexity:** $O(1)$ - Constant space for the sets.

---

## 4. Robot Room Cleaner

### Problem Statement
You are given a robot in a room that is represented as a grid. Each cell in the grid can be either empty or blocked. The robot has 4 functions: `move()`, `turnLeft()`, `turnRight()`, and `clean()`. Design an algorithm to clean the entire room using these functions.

### Optimal Python Solution (Backtracking with Spiral Search)
```python
def cleanRoom(robot):
    # (row, col), direction (0: up, 1: right, 2: down, 3: left)
    visited = set()
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def go_back():
        robot.turnRight()
        robot.turnRight()
        robot.move()
        robot.turnRight()
        robot.turnRight()

    def backtrack(r, c, d):
        visited.add((r, c))
        robot.clean()

        # Try all 4 directions starting from current heading d
        for i in range(4):
            new_d = (d + i) % 4
            dr, dc = directions[new_d]
            nr, nc = r + dr, c + dc

            if (nr, nc) not in visited and robot.move():
                backtrack(nr, nc, new_d)
                go_back() # Backtrack physically

            robot.turnRight()

    backtrack(0, 0, 0)
```

### Detailed Explanation
1. **Abstract Coordinates**: We don't know the map, so we use the starting point as `(0,0)`.
2. **DFS**: We explore as far as possible in one direction, then turn and explore others.
3. **Physical Backtracking**: Unlike standard DFS where we just return from a function, here we must tell the robot to physically move back to the previous cell and restore its original orientation.
