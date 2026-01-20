# N-Queens Problem

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md), [Backtracking concepts from Subsets](./02-subsets.md)

## Overview

N-Queens is the classic **constraint satisfaction** backtracking problem. You place n queens on an n×n chessboard such that no two queens attack each other. It elegantly demonstrates how backtracking explores possibilities while respecting constraints, making it a favorite interview and teaching problem.

## Building Intuition

**Why does row-by-row placement with constraint checking work?**

Think of it as a systematic search with early rejection of invalid paths.

1. **The Row-by-Row Strategy**: Since each row must have exactly one queen (otherwise they'd attack each other horizontally), we place one queen per row. This reduces the search space from n² positions to n positions per row.

2. **The Key Mental Model**: Imagine filling out a schedule where each row is a time slot and columns are resources. Each slot needs exactly one resource, and certain combinations conflict. You try each possibility, checking for conflicts, and backtrack when stuck.

3. **The Three Attack Vectors**: Queens attack along:
   - **Column**: Only one queen per column (track with a set or array)
   - **Main diagonal (↘)**: Cells where `row - col` is constant
   - **Anti-diagonal (↙)**: Cells where `row + col` is constant

4. **Visual Intuition—Diagonal Math**:
```
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

5. **Why Backtracking is Needed**: Not all partial solutions lead to complete solutions. For n=4, if you place queens at (0,0) and (1,2), there's no valid place for row 2. You must undo (backtrack) and try (1,3) instead.

6. **Pruning via Constraint Checking**: Before placing a queen at (row, col), check if col is taken, if `row-col` diagonal is taken, if `row+col` diagonal is taken. This O(1) check (with sets) prunes entire subtrees instantly.

## When NOT to Use N-Queens Style Backtracking

This constraint satisfaction approach isn't always best:

1. **When n Is Very Large**: N-Queens can be solved for large n, but finding ALL solutions becomes exponential. For n > 15, consider heuristic methods or just finding one solution.

2. **When Constraints Are Different**: N-Queens has specific diagonal constraints. Other constraint satisfaction problems (like graph coloring, scheduling) may need different representations.

3. **When You Only Need One Solution**: For large n, heuristics like minimum conflicts or random restart can find one solution faster than exhaustive backtracking.

4. **When You Need the Count Only**: For counting N-Queens solutions, there are mathematical approaches and optimized algorithms (like Dancing Links) that are faster.

5. **When Symmetry Can Be Exploited**: N-Queens has 8-fold symmetry (rotations and reflections). For counting or finding all solutions, you can solve for 1/8 of the cases and multiply.

**Red Flags for N-Queens Pattern:**
- n > 15 and need ALL solutions → too slow
- Need just one solution → use heuristics
- Just need count → use specialized algorithms
- Problem isn't chess-like → may need different constraint model

**Better Alternatives:**
| Situation | Use Instead |
|-----------|-------------|
| Just need one solution | Min-conflicts heuristic |
| Very large n, all solutions | Dancing Links (DLX) |
| Need count only | Mathematical + DLX |
| Exploit symmetry | Solve 1/8, apply transforms |

---

## Interview Context

N-Queens is a classic constraint satisfaction problem that tests:
1. **Backtracking mastery**: Systematic exploration with constraints
2. **Constraint checking**: Efficient validation of queen placement
3. **State representation**: How to represent the board
4. **Optimization skills**: Pruning invalid paths early

---

## Problem Statement

Place n queens on an n×n chessboard so that no two queens attack each other.

Queens attack horizontally, vertically, and diagonally.

```
n = 4, One solution:

. Q . .
. . . Q
Q . . .
. . Q .

Another solution:

. . Q .
Q . . .
. . . Q
. Q . .
```

---

## The Core Insight

Place queens row by row. For each row, try each column. A placement is valid if no queen attacks the new position.

```
Row 0: Try each column, place queen
Row 1: Try each column that's not attacked
Row 2: Continue...
...
Row n-1: Found a solution!
```

---

## Approach 1: Basic Backtracking

```python
def solve_n_queens(n: int) -> list[list[str]]:
    """
    Find all valid N-Queens configurations.

    Time: O(n!) - n choices for row 0, ~n-1 for row 1, etc.
    Space: O(n) - recursion depth + board state
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
            # Convert board to string representation
            solution = []
            for r in range(n):
                row_str = '.' * board[r] + 'Q' + '.' * (n - board[r] - 1)
                solution.append(row_str)
            result.append(solution)
            return

        for col in range(n):
            if is_valid(board, row, col):
                board[row] = col
                backtrack(row + 1, board, result)
                board[row] = -1  # Backtrack (optional, overwritten anyway)

    result = []
    board = [-1] * n  # board[i] = column of queen in row i
    backtrack(0, board, result)
    return result
```

### Visual Trace for n=4

```
backtrack(0, [-1,-1,-1,-1])
├── col=0: place at (0,0), board=[0,-1,-1,-1]
│   ├── col=0: attacked (same col)
│   ├── col=1: attacked (diagonal)
│   ├── col=2: valid! board=[0,2,-1,-1]
│   │   ├── col=0: attacked (diagonal)
│   │   ├── col=1: attacked (diagonal)
│   │   ├── col=2: attacked (same col)
│   │   └── col=3: attacked (diagonal)
│   │   └── dead end, backtrack
│   └── col=3: valid! board=[0,3,-1,-1]
│       └── ...continues...
├── col=1: place at (0,1), board=[1,-1,-1,-1]
│   └── ...eventually finds solutions
...
```

---

## Approach 2: Optimized with Sets

Use sets to track attacked columns and diagonals in O(1).

```python
def solve_n_queens_optimized(n: int) -> list[list[str]]:
    """
    Optimized N-Queens using sets for O(1) conflict checking.

    Time: O(n!)
    Space: O(n) - sets + recursion
    """

    def backtrack(row: int):
        if row == n:
            solution = ['.' * c + 'Q' + '.' * (n - c - 1) for c in board]
            result.append(solution)
            return

        for col in range(n):
            # Check if position is attacked
            if col in cols:
                continue
            if row - col in diag1:  # Main diagonal (↘)
                continue
            if row + col in diag2:  # Anti-diagonal (↙)
                continue

            # Place queen
            board[row] = col
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(row + 1)

            # Remove queen (backtrack)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    result = []
    board = [0] * n
    cols = set()      # Columns with queens
    diag1 = set()     # Main diagonals (row - col is constant)
    diag2 = set()     # Anti-diagonals (row + col is constant)

    backtrack(0)
    return result
```

### Understanding Diagonals

```
Main diagonal (↘): row - col is constant
    (0,0), (1,1), (2,2): row - col = 0
    (0,1), (1,2), (2,3): row - col = -1
    (1,0), (2,1), (3,2): row - col = 1

Anti-diagonal (↙): row + col is constant
    (0,2), (1,1), (2,0): row + col = 2
    (0,3), (1,2), (2,1), (3,0): row + col = 3

  0 1 2 3
0 . . Q .   (0,2): diag1=0-2=-2, diag2=0+2=2
1 Q . . .   (1,0): diag1=1-0=1, diag2=1+0=1
2 . . . Q   (2,3): diag1=2-3=-1, diag2=2+3=5
3 . Q . .   (3,1): diag1=3-1=2, diag2=3+1=4
```

---

## N-Queens II: Count Solutions Only

If we only need the count, we don't need to build strings.

```python
def total_n_queens(n: int) -> int:
    """
    Count total N-Queens solutions.

    Time: O(n!)
    Space: O(n)
    """

    def backtrack(row: int) -> int:
        if row == n:
            return 1

        count = 0
        for col in range(n):
            if col in cols or row - col in diag1 or row + col in diag2:
                continue

            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            count += backtrack(row + 1)

            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

        return count

    cols, diag1, diag2 = set(), set(), set()
    return backtrack(0)
```

---

## Solution Counts by N

| n | Solutions | Time to Compute |
|---|-----------|-----------------|
| 1 | 1 | Instant |
| 2 | 0 | Instant |
| 3 | 0 | Instant |
| 4 | 2 | Instant |
| 5 | 10 | Instant |
| 6 | 4 | Instant |
| 7 | 40 | Instant |
| 8 | 92 | Fast |
| 9 | 352 | Fast |
| 10 | 724 | ~1 second |
| 12 | 14,200 | ~1 minute |

---

## Using Bitmasks (Advanced)

For maximum performance, use bitmasks instead of sets.

```python
def total_n_queens_bits(n: int) -> int:
    """
    Count solutions using bitmasking for O(1) operations.

    Time: O(n!)
    Space: O(n) - recursion only
    """

    def backtrack(row: int, cols: int, diag1: int, diag2: int) -> int:
        if row == n:
            return 1

        count = 0
        available = ((1 << n) - 1) & ~(cols | diag1 | diag2)

        while available:
            # Get rightmost set bit (next available column)
            pos = available & -available
            available &= available - 1

            count += backtrack(
                row + 1,
                cols | pos,
                (diag1 | pos) << 1,
                (diag2 | pos) >> 1
            )

        return count

    return backtrack(0, 0, 0, 0)
```

---

## Alternative: Return Board Positions

Sometimes we want (row, col) pairs instead of string representation.

```python
def solve_n_queens_positions(n: int) -> list[list[tuple[int, int]]]:
    """Return solutions as list of (row, col) positions."""

    def backtrack(row: int):
        if row == n:
            result.append([(r, board[r]) for r in range(n)])
            return

        for col in range(n):
            if col in cols or row - col in diag1 or row + col in diag2:
                continue

            board[row] = col
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(row + 1)

            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    result = []
    board = [0] * n
    cols, diag1, diag2 = set(), set(), set()
    backtrack(0)
    return result
```

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Basic backtracking | O(n! × n) | O(n) | n for is_valid check |
| With sets | O(n!) | O(n) | O(1) validation |
| With bitmasks | O(n!) | O(n) | Fastest constant factor |
| Count only | O(n!) | O(n) | No string building |

---

## Edge Cases

- [ ] n = 1 → [[["Q"]]]
- [ ] n = 2, 3 → [] (no solution)
- [ ] Large n → performance matters

---

## Common Mistakes

### 1. Forgetting Diagonal Check

```python
# WRONG: only checks column
if prev_col == col:
    return False

# CORRECT: also check diagonals
if abs(prev_row - row) == abs(prev_col - col):
    return False
```

### 2. Wrong Diagonal Formula

```python
# Main diagonal: row - col (constant along ↘)
# Anti-diagonal: row + col (constant along ↙)

# WRONG: mixing them up
diag1.add(row + col)  # This is anti-diagonal!
```

### 3. Not Backtracking Sets

```python
cols.add(col)
backtrack(row + 1)
# WRONG: forgetting to remove
# CORRECT:
cols.remove(col)
```

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | N-Queens | Hard | Classic backtracking |
| 2 | N-Queens II | Hard | Count only |
| 3 | Valid Sudoku | Medium | Similar constraint checking |
| 4 | Robot Room Cleaner | Hard | Backtracking in unknown space |

---

## Interview Tips

1. **Start simple**: Use the basic O(n²) validation first
2. **Explain diagonals**: Show how row ± col works
3. **Optimize if asked**: Move to sets, then bitmasks if needed
4. **Know the counts**: n=8 has 92 solutions
5. **Discuss symmetry**: Mention you could use symmetry to halve work

---

## Key Takeaways

1. N-Queens is the classic constraint satisfaction backtracking problem
2. Place row by row, check column and both diagonals
3. Use sets for O(1) conflict checking
4. Main diagonal: row - col; Anti-diagonal: row + col
5. Bitmasks are fastest but harder to understand

---

## Next: [07-sudoku-solver.md](./07-sudoku-solver.md)

Apply similar constraint satisfaction techniques to solve Sudoku.
