# Matrix Traversal - Solutions

## Practice Problems

### 1. Spiral Matrix

**Problem Statement**: Given an `m x n` matrix, return all elements of the matrix in spiral order.

**Examples & Edge Cases**:

- Example: `[[1,2,3],[4,5,6],[7,8,9]]` -> `[1,2,3,6,9,8,7,4,5]`
- Edge Case: Single row or single column matrix.
- Edge Case: Empty matrix.

**Optimal Python Solution**:

```python
def spiralOrder(matrix: list[list[int]]) -> list[int]:
    if not matrix: return []
    res = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # 1. Top row
        for j in range(left, right + 1):
            res.append(matrix[top][j])
        top += 1

        # 2. Right column
        for i in range(top, bottom + 1):
            res.append(matrix[i][right])
        right -= 1

        # 3. Bottom row (if still valid)
        if top <= bottom:
            for j in range(right, left - 1, -1):
                res.append(matrix[bottom][j])
            bottom -= 1

        # 4. Left column (if still valid)
        if left <= right:
            for i in range(bottom, top - 1, -1):
                res.append(matrix[i][left])
            left += 1

    return res
```

**Explanation**:
We maintain four boundaries: `top`, `bottom`, `left`, and `right`. We traverse the outer perimeter, then shrink the boundaries and repeat until all elements are visited. We must check `top <= bottom` and `left <= right` before the backward passes (left and up) to avoid duplicate visits in single-row/column scenarios.

**Complexity Analysis**:

- **Time Complexity**: O(M \* N), where M is rows and N is columns.
- **Space Complexity**: O(1) extra space (excluding output).

---

### 2. Spiral Matrix II

**Problem Statement**: Given a positive integer `n`, generate an `n x n` matrix filled with elements from 1 to `n^2` in spiral order.

**Optimal Python Solution**:

```python
def generateMatrix(n: int) -> list[list[int]]:
    matrix = [[0] * n for _ in range(n)]
    top, bottom = 0, n - 1
    left, right = 0, n - 1
    val = 1

    while val <= n * n:
        for j in range(left, right + 1):
            matrix[top][j] = val
            val += 1
        top += 1

        for i in range(top, bottom + 1):
            matrix[i][right] = val
            val += 1
        right -= 1

        for j in range(right, left - 1, -1):
            matrix[bottom][j] = val
            val += 1
        bottom -= 1

        for i in range(bottom, top - 1, -1):
            matrix[i][left] = val
            val += 1
        left += 1

    return matrix
```

**Complexity Analysis**:

- **Time Complexity**: O(n²).
- **Space Complexity**: O(1) extra space (excluding result).

---

### 3. Rotate Image

**Problem Statement**: You are given an `n x n` 2D matrix representing an image, rotate the image by 90 degrees (clockwise). You have to rotate the image in-place.

**Optimal Python Solution**:

```python
def rotate(matrix: list[list[int]]) -> None:
    n = len(matrix)

    # Step 1: Transpose the matrix
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse each row
    for i in range(n):
        matrix[i].reverse()
```

**Explanation**:
A 90-degree clockwise rotation is mathematically equivalent to transposing the matrix (swapping elements across the diagonal) followed by reversing each row horizontally.

**Complexity Analysis**:

- **Time Complexity**: O(n²).
- **Space Complexity**: O(1).

---

### 4. Set Matrix Zeroes

**Problem Statement**: Given an `m x n` integer matrix `matrix`, if an element is 0, set its entire row and column to 0's. Do it in-place.

**Optimal Python Solution**:

```python
def setZeroes(matrix: list[list[int]]) -> None:
    R, C = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][j] == 0 for j in range(C))
    first_col_zero = any(matrix[i][0] == 0 for i in range(R))

    # Use first row and column as flags for the rest of the matrix
    for i in range(1, R):
        for j in range(1, C):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    # Set zeros based on flags
    for i in range(1, R):
        for j in range(1, C):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    # Finally, handle the first row and column themselves
    if first_row_zero:
        for j in range(C): matrix[0][j] = 0
    if first_col_zero:
        for i in range(R): matrix[i][0] = 0
```

**Complexity Analysis**:

- **Time Complexity**: O(M \* N).
- **Space Complexity**: O(1).

---

### 5. Search a 2D Matrix

**Problem Statement**: Write an efficient algorithm that searches for a value in an `m x n` matrix. Each row is sorted in non-decreasing order and the first integer of each row is greater than the last integer of the previous row.

**Optimal Python Solution**:

```python
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    if not matrix: return False
    M, N = len(matrix), len(matrix[0])
    l, r = 0, M * N - 1

    while l <= r:
        mid = (l + r) // 2
        # Virtual flatten: index 'mid' corresponds to (mid // N, mid % N)
        val = matrix[mid // N][mid % N]
        if val == target:
            return True
        elif val < target:
            l = mid + 1
        else:
            r = mid - 1
    return False
```

**Explanation**:
Since the entire matrix is essentially one long sorted list, we can perform binary search on it. We treat it as a virtual 1D array of size `M * N`.

**Complexity Analysis**:

- **Time Complexity**: O(log(M \* N)).
- **Space Complexity**: O(1).

---

### 6. Search a 2D Matrix II

**Problem Statement**: Search for a value in an `m x n` matrix where each row is sorted in ascending order and each column is sorted in ascending order.

**Optimal Python Solution**:

```python
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    if not matrix: return False
    R, C = len(matrix), len(matrix[0])
    # Start from top-right corner
    r, c = 0, C - 1

    while r < R and c >= 0:
        if matrix[r][c] == target:
            return True
        elif matrix[r][c] > target:
            # All elements below are also larger, move left
            c -= 1
        else:
            # All elements to the left are also smaller, move down
            r += 1
    return False
```

**Complexity Analysis**:

- **Time Complexity**: O(M + N).
- **Space Complexity**: O(1).

---

### 7. Diagonal Traverse

**Problem Statement**: Given an `m x n` matrix, return all elements of the matrix in a diagonal zigzag order.

**Optimal Python Solution**:

```python
def findDiagonalOrder(matrix: list[list[int]]) -> list[int]:
    if not matrix: return []
    R, C = len(matrix), len(matrix[0])
    res = []
    r, c = 0, 0
    direction = 1 # 1 for up-right, -1 for down-left

    while len(res) < R * C:
        res.append(matrix[r][c])

        if direction == 1:
            if c == C - 1: # Hit right edge
                r += 1
                direction = -1
            elif r == 0:   # Hit top edge
                c += 1
                direction = -1
            else:
                r -= 1
                c += 1
        else:
            if r == R - 1: # Hit bottom edge
                c += 1
                direction = 1
            elif c == 0:   # Hit left edge
                r += 1
                direction = 1
            else:
                r += 1
                c -= 1
    return res
```

**Complexity Analysis**:

- **Time Complexity**: O(M \* N).
- **Space Complexity**: O(1).

---

### 8. Transpose Matrix

**Problem Statement**: Given a 2D integer array `matrix`, return the transpose of `matrix`.

**Optimal Python Solution**:

```python
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    R, C = len(matrix), len(matrix[0])
    # New matrix will have dimensions C x R
    res = [[0] * R for _ in range(C)]
    for r in range(R):
        for c in range(C):
            res[c][r] = matrix[r][c]
    return res
```

**Complexity Analysis**:

- **Time Complexity**: O(M \* N).
- **Space Complexity**: O(M \* N) for the result.

---

### 9. Reshape the Matrix

**Problem Statement**: In MATLAB, there is a handy function called `reshape` which can reshape an `m x n` matrix into a new one with a different size `r x c` keeping its original data.

**Optimal Python Solution**:

```python
def matrixReshape(mat: list[list[int]], r: int, c: int) -> list[list[int]]:
    R, C = len(mat), len(mat[0])
    if R * C != r * c:
        return mat

    res = [[0] * c for _ in range(r)]
    for i in range(R * C):
        # Map original index i to (r1, c1) and target index i to (r2, c2)
        res[i // c][i % c] = mat[i // C][i % C]
    return res
```

**Complexity Analysis**:

- **Time Complexity**: O(r \* c).
- **Space Complexity**: O(r \* c).
