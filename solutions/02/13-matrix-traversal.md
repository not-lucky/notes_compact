# Matrix Traversal

## Practice Problems

### 1. Spiral Matrix
**Difficulty:** Medium
**Technique:** Layer traversal

```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    """
    Time: O(m * n)
    Space: O(1)
    """
    if not matrix: return []
    res = []
    T, B, L, R = 0, len(matrix)-1, 0, len(matrix[0])-1
    while T <= B and L <= R:
        for c in range(L, R + 1): res.append(matrix[T][c])
        T += 1
        for r in range(T, B + 1): res.append(matrix[r][R])
        R -= 1
        if T <= B:
            for c in range(R, L - 1, -1): res.append(matrix[B][c])
            B -= 1
        if L <= R:
            for r in range(B, T - 1, -1): res.append(matrix[r][L])
            L += 1
    return res
```

### 2. Spiral Matrix II
**Difficulty:** Medium
**Technique:** Generate spiral

```python
def generate_matrix(n: int) -> list[list[int]]:
    """
    Time: O(n^2)
    Space: O(1) (excluding result)
    """
    res = [[0]*n for _ in range(n)]
    T, B, L, R = 0, n-1, 0, n-1
    val = 1
    while val <= n*n:
        for c in range(L, R + 1):
            res[T][c] = val
            val += 1
        T += 1
        for r in range(T, B + 1):
            res[r][R] = val
            val += 1
        R -= 1
        for c in range(R, L - 1, -1):
            res[B][c] = val
            val += 1
        B -= 1
        for r in range(B, T - 1, -1):
            res[r][L] = val
            val += 1
        L += 1
    return res
```

### 3. Rotate Image
**Difficulty:** Medium
**Technique:** Transpose + reverse

```python
def rotate(matrix: list[list[int]]) -> None:
    """
    Time: O(n^2)
    Space: O(1)
    """
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
```

### 4. Set Matrix Zeroes
**Difficulty:** Medium
**Technique:** First row/col as markers

```python
def set_zeroes(matrix: list[list[int]]) -> None:
    """
    Time: O(m * n)
    Space: O(1)
    """
    R, C = len(matrix), len(matrix[0])
    row_zero = any(matrix[0][c] == 0 for c in range(C))
    col_zero = any(matrix[r][0] == 0 for r in range(R))

    for r in range(1, R):
        for c in range(1, C):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0

    for r in range(1, R):
        for c in range(1, C):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0

    if row_zero:
        for c in range(C): matrix[0][c] = 0
    if col_zero:
        for r in range(R): matrix[r][0] = 0
```

### 5. Search a 2D Matrix
**Difficulty:** Medium
**Technique:** Binary search

```python
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """
    Time: O(log(m * n))
    Space: O(1)
    """
    R, C = len(matrix), len(matrix[0])
    l, r = 0, R * C - 1
    while l <= r:
        m = (l + r) // 2
        val = matrix[m // C][m % C]
        if val == target: return True
        elif val < target: l = m + 1
        else: r = m - 1
    return False
```

### 6. Search a 2D Matrix II
**Difficulty:** Medium
**Technique:** Start from corner

```python
def search_matrix_ii(matrix: list[list[int]], target: int) -> bool:
    """
    Time: O(m + n)
    Space: O(1)
    """
    R, C = len(matrix), len(matrix[0])
    r, c = 0, C - 1
    while r < R and c >= 0:
        if matrix[r][c] == target: return True
        elif matrix[r][c] > target: c -= 1
        else: r += 1
    return False
```

### 7. Diagonal Traverse
**Difficulty:** Medium
**Technique:** Zigzag pattern

```python
def find_diagonal_order(matrix: list[list[int]]) -> list[int]:
    """
    Time: O(m * n)
    Space: O(1)
    """
    if not matrix: return []
    R, C = len(matrix), len(matrix[0])
    res = []
    for d in range(R + C - 1):
        if d % 2 == 0:
            r = min(d, R - 1)
            c = d - r
            while r >= 0 and c < C:
                res.append(matrix[r][c])
                r -= 1; c += 1
        else:
            c = min(d, C - 1)
            r = d - c
            while c >= 0 and r < R:
                res.append(matrix[r][c])
                r += 1; c -= 1
    return res
```

### 8. Transpose Matrix
**Difficulty:** Easy
**Technique:** Swap indices

```python
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """
    Time: O(m * n)
    Space: O(m * n)
    """
    R, C = len(matrix), len(matrix[0])
    res = [[0]*R for _ in range(C)]
    for r in range(R):
        for c in range(C):
            res[c][r] = matrix[r][c]
    return res
```

### 9. Reshape the Matrix
**Difficulty:** Easy
**Technique:** Flatten and rebuild

```python
def matrix_reshape(mat: list[list[int]], r: int, c: int) -> list[list[int]]:
    """
    Time: O(m * n)
    Space: O(m * n)
    """
    R, C = len(mat), len(mat[0])
    if R * C != r * c: return mat
    res = [[0]*c for _ in range(r)]
    for i in range(R * C):
        res[i // c][i % c] = mat[i // C][i % C]
    return res
```
