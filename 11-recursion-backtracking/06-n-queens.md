# N-Queens Problem

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md), [Backtracking concepts from Subsets](./02-subsets.md)

## Core Concept

N-Queens is the classic **constraint satisfaction** backtracking problem. You place $N$ queens on an $N \times N$ chessboard such that no two queens attack each other. It elegantly demonstrates how backtracking explores possibilities while respecting constraints, making it a favorite interview and teaching problem. The essence of this problem is **state mutation and restoration** in a grid representation.

## Intuition & Mental Models

**Why does row-by-row placement with constraint checking work?**

Think of it as a systematic search with early rejection of invalid paths.

1. **The Row-by-Row Strategy (Level):** Since each row must have exactly one queen (otherwise they'd attack each other horizontally), we place one queen per row. This reduces the search space from $N^2$ positions down to $N$ choices per row. The `row` index acts as the depth/level in our recursive tree.

2. **Suffix Selection (Choices):** At each row, our choices are the $N$ columns. We iterate through each column and try to place a queen.

3. **The Three Attack Vectors (State Validation):** Queens attack along:
   - **Column**: Only one queen per column.
   - **Main diagonal ($\searrow$)**: Cells where `row - col` is constant.
   - **Anti-diagonal ($\swarrow$)**: Cells where `row + col` is constant.

4. **Visual Intuition—Diagonal Math:**

```text
    col→  0  1  2  3
row↓
  0      [0][-1][-2][-3]   ← row - col (main diagonal ID)
  1      [1][0][-1][-2]
  2      [2][1][0][-1]
  3      [3][2][1][0]

    col→  0  1  2  3
row↓
  0      [0][1][2][3]      ← row + col (anti-diagonal ID)
  1      [1][2][3][4]
  2      [2][3][4][5]
  3      [3][4][5][6]
```

If two queens have the same diagonal ID, they attack each other.

1. **Pruning via Constraint Checking:** Before placing a queen at `(row, col)`, check if the `col`, `row-col` diagonal, or `row+col` diagonal is taken. This $O(1)$ check (with sets) prunes entire invalid subtrees instantly.

## Visualizations

### Decision Tree with Pruning (N=4)

```text
Level 0: place Q in row 0
                          (0,0)
                       /         \
Level 1:       (1,0) ✗         (1,1) ✗     ... (1,2) ✓     (1,3) ✓
              (same col)     (same diag)         |           |
                                                 |           |
Level 2:                                   (2,0) ✗         ...
                                         (same diag)
```

By eagerly pruning choices that violate constraints, we prevent the tree from growing to an unmanageable $O(N^N)$ size.

## Basic Implementation: State Mutation and Restoration

Instead of passing new board copies, we **mutate** a shared state array and **restore** it after the recursive call. This is the core of backtracking.

```python
def solve_n_queens(n: int) -> list[list[str]]:
    """
    Find all valid N-Queens configurations.
    """
    def is_valid(board: list[int], row: int, col: int) -> bool:
        """Check if placing queen at (row, col) is valid."""
        for prev_row in range(row):
            prev_col = board[prev_row]

            # Same column?
            if prev_col == col:
                return False

            # Same diagonal? (difference in rows = difference in cols)
            if abs(prev_row - row) == abs(prev_col - col):
                return False

        return True

    def backtrack(row: int, board: list[int], result: list[list[str]]):
        if row == n:
            # Valid placement found! Convert board to string representation
            solution = []
            for r in range(n):
                row_str = '.' * board[r] + 'Q' + '.' * (n - board[r] - 1)
                solution.append(row_str)
            result.append(solution)
            return

        for col in range(n):
            if is_valid(board, row, col):
                # 1. Mutate State
                board[row] = col

                # 2. Recurse to next level
                backtrack(row + 1, board, result)

                # 3. Restore State (Backtrack)
                board[row] = -1

    result = []
    # board[i] = column of queen in row i
    # We use a 1D array instead of a 2D matrix for efficiency
    board = [-1] * n
    backtrack(0, board, result)
    return result
```

## Optimized Implementation: O(1) Constraint Checking

Using sets to track attacked columns and diagonals drops the validation step from $O(N)$ to $O(1)$.

```python
def solve_n_queens_optimized(n: int) -> list[list[str]]:
    """
    Optimized N-Queens using sets for O(1) conflict checking.
    """
    def backtrack(row: int):
        if row == n:
            solution = ['.' * c + 'Q' + '.' * (n - c - 1) for c in board]
            result.append(solution)
            return

        for col in range(n):
            # O(1) check if position is attacked
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            # 1. Place queen and mark constraints (Mutate State)
            board[row] = col
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            # 2. Recurse
            backtrack(row + 1)

            # 3. Remove queen and constraints (Restore State)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    result = []
    board = [0] * n
    cols = set()      # Columns with queens
    diag1 = set()     # Main diagonals (row - col)
    diag2 = set()     # Anti-diagonals (row + col)

    backtrack(0)
    return result
```

## Complexity Analysis

- **Time Complexity:** $O(N!)$. For the first row, we have $N$ choices. For the second, $N-1$ choices, and so on. Pruning makes this much faster in practice, but the upper bound is $N!$. Building each valid board string takes $O(N^2)$, making the total time $O(N! + S \cdot N^2)$ where $S$ is the number of solutions.
- **Auxiliary Space:** $O(N)$. The recursion call stack goes up to $N$ frames deep. The `board` array and sets (`cols`, `diag1`, `diag2`) also use $O(N)$ space.
- **Total Space:** $O(S \cdot N^2)$ where $S$ is the number of valid solutions. Each solution requires an $N \times N$ string representation.

## Common Pitfalls

### 1. Forgetting to Restore State (Backtrack)

When using shared sets or matrices, you **must** undo the changes after returning from the recursive call.

```python
# WRONG: Constraints persist across parallel branches
cols.add(col)
backtrack(row + 1)

# CORRECT: Clean up for the next sibling in the loop
cols.add(col)
backtrack(row + 1)
cols.remove(col)
```

### 2. Wrong Diagonal Formula

Mixing up the math for the main and anti-diagonals.

```python
# Main diagonal (↘): row - col (constant along ↘)
# Anti-diagonal (↙): row + col (constant along ↙)

# WRONG: mixing them up
diag1.add(row + col)  # This tracks the anti-diagonal!
```

### 3. Mutating Results by Reference

If you store the array of column indices rather than the constructed strings, you must explicitly copy the array.

```python
# WRONG: Appends a reference to the mutating board list
if row == n:
    result.append(board)

# CORRECT: Append a copy
if row == n:
    result.append(board[:])
```
