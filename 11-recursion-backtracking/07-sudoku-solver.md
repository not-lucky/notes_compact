# Sudoku Solver

> **Prerequisites:** [N-Queens](./06-n-queens.md), understanding of constraint satisfaction

## Interview Context

Sudoku solver tests:
1. **Constraint propagation**: Three simultaneous constraints (row, column, box)
2. **Backtracking efficiency**: Knowing when to backtrack early
3. **State management**: Tracking what's valid in each position
4. **Optimization techniques**: Choosing the best cell to fill next

---

## Problem Statement

Fill a 9×9 grid so that each row, column, and 3×3 box contains digits 1-9 exactly once.

```
Input:
5 3 . | . 7 . | . . .
6 . . | 1 9 5 | . . .
. 9 8 | . . . | . 6 .
------+-------+------
8 . . | . 6 . | . . 3
4 . . | 8 . 3 | . . 1
7 . . | . 2 . | . . 6
------+-------+------
. 6 . | . . . | 2 8 .
. . . | 4 1 9 | . . 5
. . . | . 8 . | . 7 9

Output:
5 3 4 | 6 7 8 | 9 1 2
6 7 2 | 1 9 5 | 3 4 8
1 9 8 | 3 4 2 | 5 6 7
------+-------+------
8 5 9 | 7 6 1 | 4 2 3
4 2 6 | 8 5 3 | 7 9 1
7 1 3 | 9 2 4 | 8 5 6
------+-------+------
9 6 1 | 5 3 7 | 2 8 4
2 8 7 | 4 1 9 | 6 3 5
3 4 5 | 2 8 6 | 1 7 9
```

---

## The Core Insight

For each empty cell, try digits 1-9. A digit is valid if it doesn't appear in the same row, column, or 3×3 box.

```
To check (row, col):
1. Check row: board[row][0..8]
2. Check col: board[0..8][col]
3. Check box: 3×3 box containing (row, col)

Box index: (row // 3, col // 3)
For row=4, col=5: box = (1, 1) → middle box
```

---

## Approach 1: Basic Backtracking

```python
def solve_sudoku(board: list[list[str]]) -> None:
    """
    Solve Sudoku in-place.

    Time: O(9^81) worst case, but pruning makes it much faster
    Space: O(81) - recursion depth
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
        # Find first empty cell
        for row in range(9):
            for col in range(9):
                if board[row][col] == '.':
                    # Try digits 1-9
                    for digit in '123456789':
                        if is_valid(row, col, digit):
                            board[row][col] = digit

                            if backtrack():
                                return True

                            board[row][col] = '.'  # Backtrack

                    return False  # No valid digit found

        return True  # All cells filled

    backtrack()
```

---

## Approach 2: Optimized with Sets

Pre-compute and maintain sets for O(1) validity checking.

```python
def solve_sudoku_optimized(board: list[list[str]]) -> None:
    """
    Optimized Sudoku solver using sets.

    Time: Still O(9^empty_cells) worst case
    Space: O(81) for sets
    """

    # Initialize constraint sets
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    empty = []

    # Populate initial constraints
    for r in range(9):
        for c in range(9):
            if board[r][c] != '.':
                digit = board[r][c]
                rows[r].add(digit)
                cols[c].add(digit)
                boxes[(r // 3) * 3 + c // 3].add(digit)
            else:
                empty.append((r, c))

    def backtrack(idx: int) -> bool:
        if idx == len(empty):
            return True

        r, c = empty[idx]
        box_idx = (r // 3) * 3 + c // 3

        for digit in '123456789':
            if digit in rows[r] or digit in cols[c] or digit in boxes[box_idx]:
                continue

            # Place digit
            board[r][c] = digit
            rows[r].add(digit)
            cols[c].add(digit)
            boxes[box_idx].add(digit)

            if backtrack(idx + 1):
                return True

            # Remove digit (backtrack)
            board[r][c] = '.'
            rows[r].remove(digit)
            cols[c].remove(digit)
            boxes[box_idx].remove(digit)

        return False

    backtrack(0)
```

---

## Approach 3: MRV Heuristic (Most Constrained Variable)

Choose the cell with fewest valid options first.

```python
def solve_sudoku_mrv(board: list[list[str]]) -> None:
    """
    Sudoku solver with MRV (Minimum Remaining Values) heuristic.

    Choosing the most constrained cell first prunes more branches.
    """

    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    # Initialize
    for r in range(9):
        for c in range(9):
            if board[r][c] != '.':
                digit = board[r][c]
                rows[r].add(digit)
                cols[c].add(digit)
                boxes[(r // 3) * 3 + c // 3].add(digit)

    def get_candidates(r: int, c: int) -> set:
        """Get valid digits for cell (r, c)."""
        if board[r][c] != '.':
            return set()
        box_idx = (r // 3) * 3 + c // 3
        used = rows[r] | cols[c] | boxes[box_idx]
        return set('123456789') - used

    def find_best_cell() -> tuple[int, int, set] | None:
        """Find empty cell with minimum candidates (MRV)."""
        best = None
        min_candidates = 10

        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    candidates = get_candidates(r, c)
                    if len(candidates) < min_candidates:
                        min_candidates = len(candidates)
                        best = (r, c, candidates)

                    if min_candidates == 0:
                        return best  # Dead end

        return best

    def backtrack() -> bool:
        cell = find_best_cell()
        if cell is None:
            return True  # All filled

        r, c, candidates = cell
        if not candidates:
            return False  # Dead end

        box_idx = (r // 3) * 3 + c // 3

        for digit in candidates:
            board[r][c] = digit
            rows[r].add(digit)
            cols[c].add(digit)
            boxes[box_idx].add(digit)

            if backtrack():
                return True

            board[r][c] = '.'
            rows[r].remove(digit)
            cols[c].remove(digit)
            boxes[box_idx].remove(digit)

        return False

    backtrack()
```

---

## Using Bitmasks (Advanced)

```python
def solve_sudoku_bits(board: list[list[str]]) -> None:
    """
    Sudoku solver using bitmasks for maximum speed.

    Each constraint is a 9-bit integer.
    Bit i is set if digit (i+1) is used.
    """

    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9

    empty = []

    # Initialize
    for r in range(9):
        for c in range(9):
            if board[r][c] != '.':
                bit = 1 << (int(board[r][c]) - 1)
                rows[r] |= bit
                cols[c] |= bit
                boxes[(r // 3) * 3 + c // 3] |= bit
            else:
                empty.append((r, c))

    def backtrack(idx: int) -> bool:
        if idx == len(empty):
            return True

        r, c = empty[idx]
        box_idx = (r // 3) * 3 + c // 3
        used = rows[r] | cols[c] | boxes[box_idx]
        available = ~used & 0x1FF  # 9 bits

        while available:
            bit = available & -available  # Lowest set bit
            available &= available - 1
            digit = bit.bit_length()

            board[r][c] = str(digit)
            rows[r] |= bit
            cols[c] |= bit
            boxes[box_idx] |= bit

            if backtrack(idx + 1):
                return True

            board[r][c] = '.'
            rows[r] ^= bit
            cols[c] ^= bit
            boxes[box_idx] ^= bit

        return False

    backtrack(0)
```

---

## Valid Sudoku (Validation Only)

Check if a board is valid (not necessarily solvable).

```python
def is_valid_sudoku(board: list[list[str]]) -> bool:
    """
    Check if current board state is valid.

    Time: O(81) = O(1)
    Space: O(81) = O(1)
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                continue

            digit = board[r][c]
            box_idx = (r // 3) * 3 + c // 3

            if digit in rows[r] or digit in cols[c] or digit in boxes[box_idx]:
                return False

            rows[r].add(digit)
            cols[c].add(digit)
            boxes[box_idx].add(digit)

    return True
```

---

## Box Index Formula

```
box_idx = (row // 3) * 3 + col // 3

Visual mapping:
Row/Col  0 1 2  3 4 5  6 7 8
   0-2   [0]    [1]    [2]
   3-5   [3]    [4]    [5]
   6-8   [6]    [7]    [8]

Example:
(1, 4) → (1//3)*3 + 4//3 = 0*3 + 1 = 1 (box 1)
(5, 7) → (5//3)*3 + 7//3 = 1*3 + 2 = 5 (box 5)
```

---

## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Basic | O(9^81) | O(81) | Worst case, rarely hit |
| With sets | O(9^empty) | O(81) | O(1) validation |
| MRV heuristic | Better avg | O(81) | Prunes more branches |
| Bitmasks | O(9^empty) | O(27) | Fastest constant |

---

## Edge Cases

- [ ] Already solved → return immediately
- [ ] Invalid initial board → no solution
- [ ] Multiple solutions → return any one
- [ ] All empty → many solutions

---

## Common Mistakes

### 1. Wrong Box Index

```python
# WRONG: integer division order matters
box_idx = r // 3 + c // 3 * 3  # This is wrong!

# CORRECT
box_idx = (r // 3) * 3 + c // 3
```

### 2. Not Backtracking

```python
board[r][c] = digit
if backtrack(...):
    return True
# WRONG: forgetting to reset
# CORRECT:
board[r][c] = '.'
```

### 3. Returning Wrong Value

```python
# WRONG: continuing after valid placement
for digit in '123456789':
    if is_valid(...):
        board[r][c] = digit
        backtrack()  # Should check return value!
        board[r][c] = '.'

# CORRECT
for digit in '123456789':
    if is_valid(...):
        board[r][c] = digit
        if backtrack():
            return True
        board[r][c] = '.'
```

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Valid Sudoku | Medium | Validation only |
| 2 | Sudoku Solver | Hard | Full backtracking |
| 3 | Design Sudoku | Hard | Generate valid puzzles |

---

## Interview Tips

1. **Start with validation**: Show you understand the three constraints
2. **Use sets**: O(1) lookup is expected
3. **Know the box formula**: (row // 3) * 3 + col // 3
4. **Mention optimizations**: MRV, constraint propagation, bitmasks
5. **Handle edge cases**: Already solved, invalid input

---

## Key Takeaways

1. Three simultaneous constraints: row, column, 3×3 box
2. Use sets for O(1) validity checking
3. Box index = (row // 3) * 3 + col // 3
4. MRV heuristic: fill most constrained cell first
5. Must return True/False and backtrack properly

---

## Next: [08-word-search.md](./08-word-search.md)

Apply backtracking to find words in a grid.
