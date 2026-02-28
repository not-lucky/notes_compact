# Sudoku Solver

> **Prerequisites:** [N-Queens](./06-n-queens.md), understanding of constraint satisfaction

## Core Concept

Sudoku Solver applies constraint satisfaction backtracking to a familiar puzzle. Unlike N-Queens (which has one constraint type), Sudoku has **three simultaneous constraints**: row, column, and $3 \times 3$ box. This makes it an excellent advanced backtracking problem that teaches multi-dimensional constraint tracking, **2D matrix state mutation**, and early pruning via heuristics.

## Intuition & Mental Models

**Why does cell-by-cell placement with triple constraint checking work?**

Think of Sudoku as filling slots while respecting multiple "clubs" each cell belongs to.

1. **The Three-Club Model**: Every cell belongs to exactly one row-club, one column-club, and one box-club. Each club requires digits 1-9 with no repeats. Your job is to find an assignment where every club is happy.

2. **Suffix Selection**: At each empty cell, our choices are the digits '1' through '9'. We iterate through each digit and try to place it if it satisfies all three clubs.

3. **Why Box Index = `(row // 3) * 3 + col // 3`**:

```text
The 9 boxes are numbered 0-8:
┌───┬───┬───┐
│ 0 │ 1 │ 2 │   row 0-2
├───┼───┼───┤
│ 3 │ 4 │ 5 │   row 3-5
├───┼───┼───┤
│ 6 │ 7 │ 8 │   row 6-8
└───┴───┴───┘
 col col col
 0-2 3-5 6-8

For cell (5,7):
- row // 3 = 5 // 3 = 1 (middle row of boxes)
- col // 3 = 7 // 3 = 2 (right column of boxes)
- box = 1 * 3 + 2 = 5 ✓
```

1. **MRV (Minimum Remaining Values)**: Instead of filling cells left-to-right, pick the cell with fewest valid options. If a cell has only one valid digit, fill it first. If a cell has zero valid digits, backtrack immediately. This drastically prunes the search tree.

## Visualizations

### Constraint Intersection Bounding Box

```text
For cell (4,5) represented by 'X':

Row 4 constraint: [8 . . | . 6 . | . . 3]  ← Can't use 8, 6, 3
                       ↓
Column 5 constraint:   .
                       5     ← Can't use 5, 3, 9 (etc.)
                       .
                       .
                       .     ← Cell (4,5) is here
                       3
                       .
                       9
                       .

Box 4 constraint:     . 6 .
                      8 X 3   ← X is (4,5), can't use 8, 6, 3
                      . 2 .

Valid choices = {1-9} - {row 4 used} - {col 5 used} - {box 4 used}
```

## Basic Implementation: State Mutation and Restoration

Instead of copying the 2D matrix, we **mutate** it in place, try a digit, and **restore** the state if it doesn't lead to a solution.

```python
def solve_sudoku(board: list[list[str]]) -> None:
    """
    Solve Sudoku in-place using backtracking.
    """
    def is_valid(row: int, col: int, digit: str) -> bool:
        # Check row
        if digit in board[row]:
            return False

        # Check column
        for r in range(9):
            if board[r][col] == digit:
                return False

        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == digit:
                    return False

        return True

    def backtrack() -> bool:
        # Find the next empty cell (Suffix Selection)
        for row in range(9):
            for col in range(9):
                if board[row][col] == '.':
                    # Try digits 1-9
                    for digit in '123456789':
                        if is_valid(row, col, digit):
                            # 1. Mutate State (Place the digit)
                            board[row][col] = digit

                            # 2. Recurse (Does this lead to a solution?)
                            if backtrack():
                                return True

                            # 3. Restore State (Undo placing the digit)
                            board[row][col] = '.'

                    # If no digit works, this path is dead. Backtrack!
                    return False

        # If we loop through the whole board and find no '.', we are done.
        return True

    backtrack()
```

## Optimized Implementation: O(1) Checks and Pruning

Pre-compute and maintain sets for $O(1)$ validity checking, and keep track of empty cells to avoid scanning the board repeatedly.

```python
def solve_sudoku_optimized(board: list[list[str]]) -> None:
    """
    Optimized Sudoku solver using sets and an array of empty cells.
    """
    # 1. Initialize constraint sets
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    empty_cells = []

    # 2. Populate initial constraints and find empty cells
    for r in range(9):
        for c in range(9):
            if board[r][c] != '.':
                digit = board[r][c]
                rows[r].add(digit)
                cols[c].add(digit)
                boxes[(r // 3) * 3 + c // 3].add(digit)
            else:
                empty_cells.append((r, c))

    def backtrack(idx: int) -> bool:
        # Base case: All empty cells filled
        if idx == len(empty_cells):
            return True

        r, c = empty_cells[idx]
        box_idx = (r // 3) * 3 + c // 3

        for digit in '123456789':
            # O(1) constraint check
            if digit in rows[r] or digit in cols[c] or digit in boxes[box_idx]:
                continue

            # 1. Mutate State (Place digit and update sets)
            board[r][c] = digit
            rows[r].add(digit)
            cols[c].add(digit)
            boxes[box_idx].add(digit)

            # 2. Recurse to next empty cell
            if backtrack(idx + 1):
                return True

            # 3. Restore State (Backtrack!)
            board[r][c] = '.'
            rows[r].remove(digit)
            cols[c].remove(digit)
            boxes[box_idx].remove(digit)

        return False

    backtrack(0)
```

## Complexity Analysis

- **Time Complexity:** $O(9^M)$, where $M$ is the number of empty cells (max 81). For each empty cell, there are up to 9 choices. Pruning makes it extremely fast in practice, but the upper bound is exponential.
- **Auxiliary Space:** $O(M)$ for the recursion depth and the `empty_cells` array, plus $O(81)$ space for the constraint sets, yielding an overall $O(81)$ strictly.
- **Total Space:** $O(1)$ modification space since the 2D grid is mutated **in-place** directly.

## Common Pitfalls

### 1. Wrong Box Index Formula

Mixing up the math for finding the current $3 \times 3$ box.

```python
# WRONG: integer division order matters
box_idx = r // 3 + c // 3 * 3

# CORRECT
box_idx = (r // 3) * 3 + c // 3
```

### 2. Forgetting to Return False on Failure

When backtracking, if you exhaust all 9 options for a cell without success, you must return `False` so the parent caller knows to explore a different branch.

```python
# WRONG: Implicitly returning None!
for digit in '123456789':
    if is_valid(row, col, digit):
        board[row][col] = digit
        if backtrack():
            return True
        board[row][col] = '.'

# CORRECT: Tell the parent this path is a dead end.
for digit in '123456789':
    if is_valid(row, col, digit):
        board[row][col] = digit
        if backtrack():
            return True
        board[row][col] = '.'
return False
```

### 3. Creating New Board Copies

Instead of mutating the board, some candidates attempt to create copies of the entire 2D matrix on every recursive call.

```python
# WRONG: Deep copying the board on every step ruins performance
new_board = copy.deepcopy(board)
new_board[row][col] = digit
if backtrack(new_board):
    return True
```

Backtracking is powerful precisely because we reuse a single memory representation and carefully mutate/restore it.
