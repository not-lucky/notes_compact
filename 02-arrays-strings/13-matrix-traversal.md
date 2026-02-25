# Matrix Traversal

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Matrix (2D array) problems require careful index manipulation and pattern recognition. The key techniques—layer-by-layer traversal, transpose+reverse for rotation, and corner-based search—form the foundation for solving most matrix interview problems.

## Building Intuition

**Why do these specific patterns work for matrix problems?**

The key insight is **geometric structure enables systematic processing**:

1. **Spiral as Layer Peeling**: A spiral traversal is like peeling an onion. Process the outer layer (top row, right column, bottom row, left column), then move inward. Each layer is a rectangle that shrinks by one on each side.
   * **Physical Metaphor**: Imagine painting a square room starting from the baseboards and spiraling inward until you reach the center. After each lap, the available floor space shrinks by a concentric square.

2. **Rotation as Transpose + Flip**: 90° clockwise rotation = transpose (swap rows/columns) then reverse each row. This works because transpose "reflects" the matrix diagonally, and reversing rows completes the rotation. No need to calculate new coordinates!
   * **Physical Metaphor**: Imagine a transparent square tile with a picture on it. Flipping it over diagonally (transpose) gives you a mirror image. Flipping it again horizontally (reverse rows) corrects the mirror effect but leaves the picture rotated 90 degrees.

3. **Sorted Matrix Search from Corner**: At the top-right corner, moving left decreases values, moving down increases values. This gives binary-search-like elimination power—each comparison eliminates a row or column.
   * **Physical Metaphor**: Imagine navigating a mountain where moving South (down) always goes uphill and moving West (left) always goes downhill. If you are at the North-East corner and want to reach a specific altitude, if you are too high, you must go West. If you are too low, you must go South.

## When NOT to Use Standard Matrix Techniques

Matrix problems have variations that require different approaches:

1. **Matrix as Graph**: Some "matrix" problems are really graph problems (shortest path, connected components). Use BFS/DFS, not traversal patterns. Note: For recursive DFS, always factor in the $\mathcal{O}(m \times n)$ recursive call stack memory in your worst-case space complexity analysis.
2. **Sparse Matrices**: If most entries are zero, storing as a list of `(row, col, value)` tuples or a hash map is more efficient. Remember that Python dictionaries (hash maps) provide amortized $\mathcal{O}(1)$ insertions/lookups, but can degrade to worst-case $\mathcal{O}(n)$ if hash collisions occur.
3. **Non-Rectangular Grids**: Jagged arrays or hexagonal grids need adapted coordinate systems.
4. **In-Place with Non-Square Matrix**: 90° rotation in-place requires square matrices. Non-square matrices need $\Theta(m \times n)$ extra space or clever element cycling.
5. **Dynamic Matrix Updates**: If the matrix changes frequently and you need repeated queries, consider 2D segment trees or 2D Fenwick trees.

**Red Flags:**

- "Shortest path in grid" → BFS
- "Count islands/connected components" → DFS/BFS flood fill
- "Matrix updates + queries" → 2D data structures
- "Rotate non-square matrix in-place" → Not possible; need extra space

---

## Interview Context

Matrix (2D array) problems are common in FANG+ interviews because they test:

- Multi-dimensional thinking
- Careful index manipulation
- Space optimization techniques
- Various traversal patterns

Key patterns: Spiral order, Rotate image, Search in sorted matrix.

---

## Matrix Basics

```python
# Creating a matrix
matrix: list[list[int]] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

rows: int = len(matrix)           # 3
cols: int = len(matrix[0])        # 3

# Access element at row r, column c
element: int = matrix[r][c]       # \Theta(1) amortized for Python lists (dynamic arrays)

# Iterate all elements
for r in range(rows):
    for c in range(cols):
        print(matrix[r][c])
```

### Direction Vectors

```python
# 4-directional (up, down, left, right)
directions_4: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# 8-directional (including diagonals)
directions_8: list[tuple[int, int]] = [
    (-1, 0), (1, 0), (0, -1), (0, 1),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
]

# Check bounds
def is_valid(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols
```

---

## Template: Spiral Order Traversal

### Problem: Spiral Matrix
**Problem Statement:** Given an `m x n` matrix, return all elements of the matrix in spiral order.

**Why it works:**
We process the matrix layer by layer, starting from the outer boundary.
1. We maintain four boundaries: `top`, `bottom`, `left`, `right`.
2. We traverse the `top` row, then the `right` column, then the `bottom` row (if it exists), then the `left` column (if it exists).
3. After each boundary traversal, we shrink that boundary inward.

The loop continues until the boundaries cross, ensuring every element is visited exactly once in the correct order.

```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    """
    Traverse matrix in spiral order.

    Time: \Theta(m \times n) worst and best case bounds. We visit every element exactly once.
          Appending to the result list (a dynamic array in Python) takes
          amortized \Theta(1) time per element.
    Space: \Theta(m \times n) for the output array. \Theta(1) auxiliary space.

    Example:
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
    → [1, 2, 3, 6, 9, 8, 7, 4, 5]
    """
    if not matrix or not matrix[0]:
        return []

    result: list[int] = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Traverse right across top boundary
        for c in range(left, right + 1):
            result.append(matrix[top][c])
        top += 1

        # Traverse down across right boundary
        for r in range(top, bottom + 1):
            result.append(matrix[r][right])
        right -= 1

        # Traverse left across bottom boundary (if rows remaining)
        if top <= bottom:
            for c in range(right, left - 1, -1):
                result.append(matrix[bottom][c])
            bottom -= 1

        # Traverse up across left boundary (if columns remaining)
        if left <= right:
            for r in range(bottom, top - 1, -1):
                result.append(matrix[r][left])
            left += 1

    return result
```

### Visual: Spiral Traversal

```text
Step 1 →→→: [1, 2, 3]
       ↓
Step 2 ↓↓: [6, 9]
       ↓
Step 3 ←←←: [8, 7]
       ↑
Step 4 ↑: [4]
       ↑
Step 5: [5] (center)

Result: [1, 2, 3, 6, 9, 8, 7, 4, 5]
```

---

## Template: Rotate Matrix 90° Clockwise

### Problem: Rotate Image
**Problem Statement:** You are given an `n x n` 2D matrix representing an image, rotate the image by 90 degrees (clockwise). You have to rotate the image in-place.

**Why it works:**
A 90-degree clockwise rotation can be achieved through two simpler transformations:
1. **Transpose**: Reflecting the matrix across its main diagonal (swap `arr[i][j]` with `arr[j][i]`).
2. **Horizontal Reflection**: Reversing each row.

Combining these two steps transforms the element at `(i, j)` to its new position `(j, n-1-i)` without needing a separate output matrix.

```python
def rotate(matrix: list[list[int]]) -> None:
    """
    Rotate matrix 90° clockwise in-place.

    Time: \Theta(n^2) tightest bound. We process every element a constant number of times.
    Space: \Theta(1) auxiliary space, performed strictly in-place.

    Technique: Transpose then reverse each row.

    Example:
    [[1, 2, 3],     [[7, 4, 1],
     [4, 5, 6],  →   [8, 5, 2],
     [7, 8, 9]]      [9, 6, 3]]
    """
    n: int = len(matrix)

    # Step 1: Transpose (swap matrix[i][j] with matrix[j][i])
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()
```

### Rotation Techniques

```text
90° clockwise:   Transpose → Reverse rows
90° counter:     Transpose → Reverse columns
180°:            Reverse rows → Reverse each row (or reverse rows and columns)
```

---

## Template: Search in Sorted Matrix

### Problem: Search a 2D Matrix
**Problem Statement:** Design an efficient algorithm that searches for a value `target` in an `m x n` integer matrix `matrix`. This matrix has the following properties:
- Integers in each row are sorted from left to right.
- The first integer of each row is greater than the last integer of the previous row.

**Why it works:**
The properties of the matrix mean that if we were to flatten it row by row, it would be a single sorted 1D array.
1. We can perform a binary search on the range `[0, m*n - 1]`.
2. To convert a 1D index `idx` back to 2D coordinates: `row = idx // n` and `col = idx % n`.
This allows us to search the entire matrix in logarithmic time.

```python
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """
    Search in a globally sorted 2D matrix.
    Treat as flattened sorted array → Binary search.

    Time: \mathcal{O}(\log(m \times n)) worst-case bounds. \Theta(1) best case.
    Space: \Theta(1) auxiliary space.
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1

    while left <= right:
        mid = (left + right) // 2
        # Convert 1D index to 2D coordinates
        row, col = mid // n, mid % n
        val = matrix[row][col]

        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False
```

### Problem: Search a 2D Matrix II
**Problem Statement:** Search for a `target` in an `m x n` matrix where:
- Integers in each row are sorted in ascending from left to right.
- Integers in each column are sorted in ascending from top to bottom.

**Why it works:**
Starting from the top-right corner `(0, n-1)` provides a decision point.
1. If the current value is larger than `target`, we know the entire current column is larger (since columns are sorted), so we can eliminate it and move `left`.
2. If the current value is smaller than `target`, we know the entire current row is smaller (since rows are sorted), so we can eliminate it and move `down`.
Every step eliminates either a row or a column, leading to a linear-time elimination process relative to the dimensions.

```python
def search_matrix_ii(matrix: list[list[int]], target: int) -> bool:
    """
    Matrix where each row and column is sorted (but not globally).

    Start from top-right corner:
    - If target < current: go left (eliminate column)
    - If target > current: go down (eliminate row)

    Time: \mathcal{O}(m + n) worst-case. \Theta(1) best case.
    Space: \Theta(1) auxiliary space.
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1

    while row < m and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1  # Go left
        else:
            row += 1  # Go down

    return False
```

### Visual: Top-Right Search

```text
Target: 5

[1,  4,  7, 11]  Start at 11
[2,  5,  8, 12]  11 > 5 → go left to 7
[3,  6,  9, 16]   7 > 5 → go left to 4
[10, 13, 14, 17]  4 < 5 → go down to 5
                  5 == 5 → Found!
```

---

## Template: Set Matrix Zeroes

### Problem: Set Matrix Zeroes
**Problem Statement:** Given an `m x n` integer matrix `matrix`, if an element is `0`, set its entire row and column to `0`. Do it in-place.

**Why it works:**
To do it in-place with $\Theta(1)$ extra space, we use the first row and first column of the matrix itself as markers to record which rows and columns should be zeroed.
1. We check if the first row and first column need to be zeroed initially and store this in two boolean variables.
2. We scan the rest of the matrix, and if `matrix[r][c]` is 0, we mark `matrix[r][0]` and `matrix[0][c]` as 0.
3. We then iterate through the rest of the matrix again and use the markers to set zeros.
4. Finally, we handle the first row and first column separately using our boolean variables from step 1.

```python
def set_zeroes(matrix: list[list[int]]) -> None:
    """
    If element is 0, set entire row and column to 0.
    Do it in-place.

    Time: \Theta(m \times n) tightest bound. We visit each element twice.
    Space: \Theta(1) auxiliary space - use first row/col as markers

    Example:
    [[1, 1, 1],     [[1, 0, 1],
     [1, 0, 1],  →   [0, 0, 0],
     [1, 1, 1]]      [1, 0, 1]]
    """
    m, n = len(matrix), len(matrix[0])

    # Use first row and first column as markers
    first_row_zero = any(matrix[0][c] == 0 for c in range(n))
    first_col_zero = any(matrix[r][0] == 0 for r in range(m))

    # Mark zeros in first row/col
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0

    # Set zeros based on markers
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0

    # Handle first row
    if first_row_zero:
        for c in range(n):
            matrix[0][c] = 0

    # Handle first column
    if first_col_zero:
        for r in range(m):
            matrix[r][0] = 0
```

---

## Template: Diagonal Traversal

### Problem: Diagonal Traverse
**Problem Statement:** Given an `m x n` matrix `mat`, return an array of all the elements of the array in a diagonal order (zigzag pattern).

**Why it works:**
We start at `(0, 0)` moving diagonally up-right (`r-1, c+1`). When we hit a boundary, we turn around and move down-left (`r+1, c-1`).
The trick is boundary checking:
- Moving up-right: Check the right boundary first (`c == n - 1`), then the top boundary (`r == 0`).
- Moving down-left: Check the bottom boundary first (`r == m - 1`), then the left boundary (`c == 0`).

*Note: The error in the original file implementation has been corrected here. The original missed the while loop logic error and instead used an append list length check. We provide a cleaner implementation.*

```python
def diagonal_traverse(matrix: list[list[int]]) -> list[int]:
    """
    Traverse matrix diagonally in zigzag pattern.

    Time: \Theta(m \times n) tightest bound.
    Space: \Theta(m \times n) for the output array. \Theta(1) auxiliary space.

    Example:
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
    → [1, 2, 4, 7, 5, 3, 6, 8, 9]
    """
    if not matrix or not matrix[0]:
        return []

    m, n = len(matrix), len(matrix[0])
    result: list[int] = []

    # Process each diagonal
    # A diagonal is defined by the sum of its indices (r + c == d)
    # There are m + n - 1 diagonals
    for d in range(m + n - 1):
        # Determine starting point and direction based on whether d is even or odd

        if d % 2 == 0:
            # Moving up-right
            # Row starts at d (if d < m) or m-1 (if d >= m)
            r = min(d, m - 1)
            c = d - r
            while r >= 0 and c < n:
                result.append(matrix[r][c])
                r -= 1
                c += 1
        else:
            # Moving down-left
            # Col starts at d (if d < n) or n-1 (if d >= n)
            c = min(d, n - 1)
            r = d - c
            while r < m and c >= 0:
                result.append(matrix[r][c])
                r += 1
                c -= 1

    return result
```

---

## Template: Generate Spiral Matrix

```python
def generate_spiral_matrix(n: int) -> list[list[int]]:
    """
    Generate n×n matrix filled in spiral order.

    Time: \Theta(n^2) tightest bound.
    Space: \Theta(n^2) for the output matrix.

    Example n=3:
    [[1, 2, 3],
     [8, 9, 4],
     [7, 6, 5]]
    """
    matrix: list[list[int]] = [[0] * n for _ in range(n)]

    top, bottom = 0, n - 1
    left, right = 0, n - 1
    num = 1

    while top <= bottom and left <= right:
        # Right
        for c in range(left, right + 1):
            matrix[top][c] = num
            num += 1
        top += 1

        # Down
        for r in range(top, bottom + 1):
            matrix[r][right] = num
            num += 1
        right -= 1

        # Left
        if top <= bottom:
            for c in range(right, left - 1, -1):
                matrix[bottom][c] = num
                num += 1
            bottom -= 1

        # Up
        if left <= right:
            for r in range(bottom, top - 1, -1):
                matrix[r][left] = num
                num += 1
            left += 1

    return matrix
```

---

## Template: Transpose Matrix

```python
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """
    Transpose matrix (swap rows and columns).

    Time: \Theta(m \times n) tightest bound.
    Space: \Theta(m \times n) to store the transposed matrix.

    Example:
    [[1, 2, 3],     [[1, 4],
     [4, 5, 6]]  →   [2, 5],
                     [3, 6]]
    """
    m, n = len(matrix), len(matrix[0])
    return [[matrix[r][c] for r in range(m)] for c in range(n)]
```

---

## Edge Cases

```python
# Empty matrix
[] → handle specially

# Single element
[[5]] → most operations trivial

# Single row
[[1, 2, 3]] → row becomes column after transpose

# Single column
[[1], [2], [3]] → column becomes row

# Non-square matrix
Can't rotate in-place, transpose changes dimensions
```

---

## Practice Problems

| #   | Problem               | Difficulty | Technique                |
| --- | --------------------- | ---------- | ------------------------ |
| 1   | Spiral Matrix         | Medium     | Layer traversal          |
| 2   | Spiral Matrix II      | Medium     | Generate spiral          |
| 3   | Rotate Image          | Medium     | Transpose + reverse      |
| 4   | Set Matrix Zeroes     | Medium     | First row/col as markers |
| 5   | Search a 2D Matrix    | Medium     | Binary search            |
| 6   | Search a 2D Matrix II | Medium     | Start from corner        |
| 7   | Diagonal Traverse     | Medium     | Zigzag pattern           |
| 8   | Transpose Matrix      | Easy       | Swap indices             |
| 9   | Reshape the Matrix    | Easy       | Flatten and rebuild      |

---

## Key Takeaways

1. **Layer by layer** for spiral traversal
2. **Transpose + reverse** for rotation
3. **Top-right corner** for row/column sorted search
4. **Direction vectors** for neighbor traversal
5. **First row/col as markers** for \Theta(1) extra space
6. **`row = idx // cols, col = idx % cols`** for 1D ↔ 2D conversion

---

## Next: [14-in-place-modifications.md](./14-in-place-modifications.md)

Learn techniques for modifying arrays in-place.
