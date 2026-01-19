# Matrix Traversal

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

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
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

rows = len(matrix)           # 3
cols = len(matrix[0])        # 3

# Access element at row r, column c
element = matrix[r][c]       # O(1)

# Iterate all elements
for r in range(rows):
    for c in range(cols):
        print(matrix[r][c])
```

### Direction Vectors

```python
# 4-directional (up, down, left, right)
directions_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# 8-directional (including diagonals)
directions_8 = [
    (-1, 0), (1, 0), (0, -1), (0, 1),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
]

# Check bounds
def is_valid(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols
```

---

## Template: Spiral Order Traversal

```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    """
    Traverse matrix in spiral order.

    Time: O(m × n)
    Space: O(1) excluding output

    Example:
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
    → [1, 2, 3, 6, 9, 8, 7, 4, 5]
    """
    if not matrix or not matrix[0]:
        return []

    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Traverse right
        for c in range(left, right + 1):
            result.append(matrix[top][c])
        top += 1

        # Traverse down
        for r in range(top, bottom + 1):
            result.append(matrix[r][right])
        right -= 1

        # Traverse left (if rows remaining)
        if top <= bottom:
            for c in range(right, left - 1, -1):
                result.append(matrix[bottom][c])
            bottom -= 1

        # Traverse up (if columns remaining)
        if left <= right:
            for r in range(bottom, top - 1, -1):
                result.append(matrix[r][left])
            left += 1

    return result
```

### Visual: Spiral Traversal

```
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

```python
def rotate(matrix: list[list[int]]) -> None:
    """
    Rotate matrix 90° clockwise in-place.

    Time: O(n²)
    Space: O(1)

    Technique: Transpose then reverse each row.

    Example:
    [[1, 2, 3],     [[7, 4, 1],
     [4, 5, 6],  →   [8, 5, 2],
     [7, 8, 9]]      [9, 6, 3]]
    """
    n = len(matrix)

    # Step 1: Transpose (swap matrix[i][j] with matrix[j][i])
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()
```

### Rotation Techniques

```
90° clockwise:   Transpose → Reverse rows
90° counter:     Transpose → Reverse columns
180°:            Reverse rows → Reverse each row
```

---

## Template: Search in Sorted Matrix

### Search a 2D Matrix (Row and Column Sorted)

```python
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """
    Matrix where each row is sorted, and first element of each row
    is greater than last element of previous row.

    Treat as flattened sorted array → Binary search.

    Time: O(log(m × n))
    Space: O(1)
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

### Search a 2D Matrix II (Each Row/Column Sorted)

```python
def search_matrix_ii(matrix: list[list[int]], target: int) -> bool:
    """
    Matrix where each row and column is sorted (but not globally).

    Start from top-right corner:
    - If target < current: go left
    - If target > current: go down

    Time: O(m + n)
    Space: O(1)
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

```
Target: 5

[1, 4, 7, 11]  Start at 11
[2, 5, 8, 12]  11 > 5 → go left
[3, 6, 9, 16]  7 > 5 → go left
               4 < 5 → go down
               5 == 5 → Found!
```

---

## Template: Set Matrix Zeroes

```python
def set_zeroes(matrix: list[list[int]]) -> None:
    """
    If element is 0, set entire row and column to 0.
    Do it in-place.

    Time: O(m × n)
    Space: O(1) - use first row/col as markers

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

```python
def diagonal_traverse(matrix: list[list[int]]) -> list[int]:
    """
    Traverse matrix diagonally in zigzag pattern.

    Time: O(m × n)
    Space: O(1) excluding output

    Example:
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
    → [1, 2, 4, 7, 5, 3, 6, 8, 9]
    """
    if not matrix or not matrix[0]:
        return []

    m, n = len(matrix), len(matrix[0])
    result = []
    r, c = 0, 0
    going_up = True

    while len(result) < m * n:
        result.append(matrix[r][c])

        if going_up:
            if c == n - 1:  # Hit right boundary
                r += 1
                going_up = False
            elif r == 0:    # Hit top boundary
                c += 1
                going_up = False
            else:
                r -= 1
                c += 1
        else:
            if r == m - 1:  # Hit bottom boundary
                c += 1
                going_up = True
            elif c == 0:    # Hit left boundary
                r += 1
                going_up = True
            else:
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

    Time: O(n²)
    Space: O(n²)

    Example n=3:
    [[1, 2, 3],
     [8, 9, 4],
     [7, 6, 5]]
    """
    matrix = [[0] * n for _ in range(n)]

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

    Time: O(m × n)
    Space: O(m × n)

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

| # | Problem | Difficulty | Technique |
|---|---------|------------|-----------|
| 1 | Spiral Matrix | Medium | Layer traversal |
| 2 | Spiral Matrix II | Medium | Generate spiral |
| 3 | Rotate Image | Medium | Transpose + reverse |
| 4 | Set Matrix Zeroes | Medium | First row/col as markers |
| 5 | Search a 2D Matrix | Medium | Binary search |
| 6 | Search a 2D Matrix II | Medium | Start from corner |
| 7 | Diagonal Traverse | Medium | Zigzag pattern |
| 8 | Transpose Matrix | Easy | Swap indices |
| 9 | Reshape the Matrix | Easy | Flatten and rebuild |

---

## Key Takeaways

1. **Layer by layer** for spiral traversal
2. **Transpose + reverse** for rotation
3. **Top-right corner** for row/column sorted search
4. **Direction vectors** for neighbor traversal
5. **First row/col as markers** for O(1) space
6. **`row = idx // cols, col = idx % cols`** for 1D ↔ 2D conversion

---

## Next: [14-in-place-modifications.md](./14-in-place-modifications.md)

Learn techniques for modifying arrays in-place.
