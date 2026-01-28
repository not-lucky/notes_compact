# Matrix Search

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md)

## Interview Context

Matrix search problems test:

1. **Dimensional thinking**: Treating 2D as 1D or using properties
2. **Multiple approaches**: Different strategies for different matrix types
3. **Edge case handling**: Boundaries, empty matrices
4. **Optimization awareness**: O(m+n) vs O(log(mn)) tradeoffs

---

## Building Intuition

**Two Types of "Sorted" Matrices**

This is the critical distinction that changes EVERYTHING:

```
TYPE 1: Row-wise and Column-wise Sorted (Not Globally Sorted)
┌────────────────────────┐
│  1    4    7   11     │  Each row is sorted left→right
│  2    5    8   12     │  Each column is sorted top→bottom
│  3    6    9   16     │  BUT: 11 > 2, 11 > 3 (no global order)
│ 10   13   14   17     │
└────────────────────────┘

TYPE 2: Fully Sorted (Row-major Order)
┌────────────────────────┐
│  1    3    5    7     │  Each row is sorted
│ 10   11   16   20     │  AND: row[i].last < row[i+1].first
│ 23   30   34   60     │  It's really a 1D sorted array in 2D form
└────────────────────────┘
```

**Type 2: The "Fake 2D" Array**

A Type 2 matrix is just a sorted 1D array displayed in rows:

```
1D view: [1, 3, 5, 7, 10, 11, 16, 20, 23, 30, 34, 60]

2D view:  1   3   5   7
         10  11  16  20
         23  30  34  60

Index conversion:
- 1D index 7 → 2D position (row=1, col=3) = matrix[1][3] = 20
- row = index // num_cols
- col = index % num_cols
```

**Type 1: The Staircase Insight**

For Type 1, you can't use simple 1D conversion. Instead, use the **staircase pattern** from a corner:

```
Start at TOP-RIGHT (or bottom-left):
┌────────────────────────┐
│  1    4    7   [11] ← START HERE
│  2    5    8   12     │
│  3    6    9   16     │
│ 10   13   14   17     │
└────────────────────────┘

Looking for 5:
- At 11: 11 > 5, go LEFT (eliminate column)
- At 7: 7 > 5, go LEFT
- At 4: 4 < 5, go DOWN (eliminate row)
- At 5: FOUND!
```

**Why Top-Right (or Bottom-Left)?**

From top-right:

- Go LEFT → values decrease (eliminate that column)
- Go DOWN → values increase (eliminate that row)

You can make a decision at every step! Each move eliminates a row OR column.

From top-left (BAD):

- Go RIGHT → values increase
- Go DOWN → values increase
- BOTH directions increase! Can't decide which way to go.

**Mental Model: The Ladder**

Imagine you're on a ladder leaning against a wall:

- Going LEFT means stepping down the ladder (smaller values)
- Going DOWN means climbing up the wall (larger values)
- You can always adjust your position to reach your target

---

## When NOT to Use These Approaches

**1. Type 1 Methods on Type 2 Matrix (and Vice Versa)**

- Type 2 allows O(log(mn)) binary search
- Type 1 only allows O(m+n) staircase
- Using staircase on Type 2 wastes efficiency
- Using 1D binary search on Type 1 gives wrong results

**2. Unsorted Matrix**

If rows/columns aren't sorted, no efficient search exists:

```
┌──────────────┐
│ 5   2   8    │
│ 1   9   3    │  No pattern → must check all elements O(mn)
│ 4   7   6    │
└──────────────┘
```

**3. When You Need Multiple Elements**

- "Find all elements satisfying X" → likely O(mn)
- These methods find ONE element

**4. Non-Square Matrices with Extreme Dimensions**

For m×n where m >> n (or vice versa):

- Staircase is O(m+n) which is basically O(m)
- Binary search per row might be better: O(m·log(n))
- Compare based on actual dimensions

**Red Flags:**

- "Find all occurrences" → Can't avoid O(mn)
- Matrix isn't sorted at all → Linear scan
- Matrix has complex sorting (diagonals, etc.) → Different approach

---

## Types of Sorted Matrices

### Type 1: Row and Column Sorted

Each row is sorted, each column is sorted, but no global order:

```
[1,  4,  7,  11]
[2,  5,  8,  12]
[3,  6,  9,  16]
[10, 13, 14, 17]
```

### Type 2: Fully Sorted (Row-major)

Rows are sorted, and first element of each row > last element of previous row:

```
[1,  3,  5,  7]
[10, 11, 16, 20]
[23, 30, 34, 60]
```

This is essentially a sorted 1D array in 2D form.

---

## Search a 2D Matrix (Type 2)

LeetCode 74: Search a 2D Matrix

### Approach 1: Treat as 1D Array

```python
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """
    Search in row-major sorted matrix.
    Treat as 1D array with index conversion.

    Time: O(log(m*n))
    Space: O(1)
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1

    while left <= right:
        mid = left + (right - left) // 2
        # Convert 1D index to 2D
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

### Approach 2: Two Binary Searches

```python
def search_matrix_v2(matrix: list[list[int]], target: int) -> bool:
    """
    First find the row, then search within it.

    Time: O(log m + log n) = O(log(m*n))
    Space: O(1)
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])

    # Binary search for the correct row
    top, bottom = 0, m - 1
    while top <= bottom:
        mid_row = top + (bottom - top) // 2

        if matrix[mid_row][0] > target:
            bottom = mid_row - 1
        elif matrix[mid_row][-1] < target:
            top = mid_row + 1
        else:
            # Target could be in this row
            break
    else:
        return False  # No valid row found

    # Binary search within the row
    row = top + (bottom - top) // 2
    left, right = 0, n - 1

    while left <= right:
        mid = left + (right - left) // 2

        if matrix[row][mid] == target:
            return True
        elif matrix[row][mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return False
```

---

## Search a 2D Matrix II (Type 1)

LeetCode 240: Search a 2D Matrix II

### Approach: Start from Corner

Start from top-right (or bottom-left) corner:

- If current > target: move left
- If current < target: move down

```python
def search_matrix_2(matrix: list[list[int]], target: int) -> bool:
    """
    Search in row-sorted and column-sorted matrix.
    Start from top-right corner.

    Time: O(m + n)
    Space: O(1)
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1  # Top-right corner

    while row < m and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1  # Eliminate this column
        else:
            row += 1  # Eliminate this row

    return False
```

### Why This Works

```
[1,  4,  7,  11]
[2,  5,  8,  12]
[3,  6,  9,  16]
[10, 13, 14, 17]

Looking for 5, start at 11:
11 > 5: move left to 7
7 > 5: move left to 4
4 < 5: move down to 5
Found!
```

At each step, we eliminate either a row or a column.

---

## Visual Comparison

```
Type 2 (Fully Sorted):          Type 1 (Row/Col Sorted):
┌─────────────────────┐         ┌─────────────────────┐
│ 1   3   5   7      │         │ 1   4   7   11     │
│ 10  11  16  20     │         │ 2   5   8   12     │
│ 23  30  34  60     │         │ 3   6   9   16     │
└─────────────────────┘         │ 10  13  14  17     │
                                └─────────────────────┘
Binary search: O(log mn)        Staircase: O(m + n)
```

---

## Count Negatives in Sorted Matrix

LeetCode 1351: Count Negative Numbers in a Sorted Matrix

```python
def count_negatives(grid: list[list[int]]) -> int:
    """
    Count negatives in matrix sorted in non-increasing order.

    Time: O(m + n)
    Space: O(1)
    """
    m, n = len(grid), len(grid[0])
    count = 0
    row, col = 0, n - 1  # Start top-right

    while row < m and col >= 0:
        if grid[row][col] < 0:
            # All elements below in this column are negative
            count += (m - row)
            col -= 1
        else:
            row += 1

    return count
```

---

## Kth Smallest in Sorted Matrix

LeetCode 378: Kth Smallest Element in a Sorted Matrix

### Approach: Binary Search on Value

```python
def kth_smallest(matrix: list[list[int]], k: int) -> int:
    """
    Find kth smallest element in row/col sorted matrix.

    Time: O(n * log(max - min))
    Space: O(1)
    """
    n = len(matrix)

    def count_less_or_equal(mid: int) -> int:
        """Count elements <= mid."""
        count = 0
        row, col = n - 1, 0  # Start bottom-left

        while row >= 0 and col < n:
            if matrix[row][col] <= mid:
                count += row + 1  # All elements above are also <=
                col += 1
            else:
                row -= 1

        return count

    left, right = matrix[0][0], matrix[n-1][n-1]

    while left < right:
        mid = left + (right - left) // 2

        if count_less_or_equal(mid) < k:
            left = mid + 1
        else:
            right = mid

    return left
```

### Why Binary Search on Value?

- Binary search directly on positions doesn't work (not sorted that way)
- But we can binary search on the answer value
- For each candidate value, count how many elements are ≤ it
- Find the smallest value with at least k elements ≤ it

---

## Median in Row-Wise Sorted Matrix

```python
def find_median(matrix: list[list[int]]) -> int:
    """
    Find median of row-wise sorted matrix.
    Assume odd total elements.

    Time: O(m * log n * log(max - min))
    Space: O(1)
    """
    import bisect

    m, n = len(matrix), len(matrix[0])
    target = (m * n + 1) // 2

    def count_less_or_equal(val: int) -> int:
        count = 0
        for row in matrix:
            count += bisect.bisect_right(row, val)
        return count

    # Find min and max in matrix
    low = min(row[0] for row in matrix)
    high = max(row[-1] for row in matrix)

    while low < high:
        mid = low + (high - low) // 2

        if count_less_or_equal(mid) < target:
            low = mid + 1
        else:
            high = mid

    return low
```

---

## Row with Maximum Ones

```python
def row_with_max_ones(matrix: list[list[int]]) -> int:
    """
    Find row with maximum 1s in binary matrix (rows sorted).

    Time: O(m + n)
    Space: O(1)
    """
    m, n = len(matrix), len(matrix[0])
    max_row = -1
    col = n - 1  # Start from rightmost column

    for row in range(m):
        # Move left while seeing 1s
        while col >= 0 and matrix[row][col] == 1:
            col -= 1
            max_row = row

    return max_row
```

---

## Complexity Summary

| Problem                        | Approach               | Time            | Space |
| ------------------------------ | ---------------------- | --------------- | ----- |
| Search Type 2 (fully sorted)   | 1D binary search       | O(log mn)       | O(1)  |
| Search Type 1 (row/col sorted) | Staircase              | O(m + n)        | O(1)  |
| Count negatives                | Staircase              | O(m + n)        | O(1)  |
| Kth smallest                   | Binary search on value | O(n log(range)) | O(1)  |
| Row with max ones              | Staircase              | O(m + n)        | O(1)  |

---

## Choosing the Right Approach

```
Is the matrix fully sorted (row-major order)?
    │
    ├── Yes → Treat as 1D array, O(log mn)
    │
    └── No → Is it row and column sorted?
              │
              ├── Yes → Staircase from corner, O(m + n)
              │
              └── Partially sorted → Binary search on value
```

---

## Common Mistakes

### 1. Wrong Index Conversion

```python
# Wrong: mixing up row and column
row, col = mid % n, mid // n

# Correct
row, col = mid // n, mid % n
```

### 2. Wrong Corner for Staircase

```python
# Wrong: starting from top-left (both directions increase)
row, col = 0, 0

# Correct: top-right or bottom-left
row, col = 0, n - 1  # or (m - 1, 0)
```

### 3. Out of Bounds

```python
# Always check bounds
while row < m and col >= 0:  # Not just while True
```

---

## Edge Cases Checklist

- [ ] Empty matrix
- [ ] Single row / single column
- [ ] Single element
- [ ] Target smaller than all elements
- [ ] Target larger than all elements
- [ ] Target not present

---

## Practice Problems

| #   | Problem                                 | Difficulty | Key Insight            |
| --- | --------------------------------------- | ---------- | ---------------------- |
| 1   | Search a 2D Matrix                      | Medium     | Treat as 1D            |
| 2   | Search a 2D Matrix II                   | Medium     | Staircase from corner  |
| 3   | Kth Smallest Element in Sorted Matrix   | Medium     | Binary search on value |
| 4   | Count Negative Numbers in Sorted Matrix | Easy       | Staircase counting     |
| 5   | Median of Row Wise Sorted Matrix        | Hard       | Binary search on value |
| 6   | Row with Maximum Ones                   | Easy       | Staircase              |

---

## Interview Tips

1. **Clarify matrix type**: Fully sorted vs row/col sorted
2. **Mention both approaches**: For fully sorted, mention 1D trick
3. **Draw the matrix**: Visualize the search path
4. **Handle edge cases**: Empty, single element, not found
5. **Know complexities**: O(log mn) vs O(m+n)

---

## Key Takeaways

1. **Two types of sorted matrices**: Different approaches for each
2. **1D trick for fully sorted**: Convert indices
3. **Staircase for row/col sorted**: O(m+n) from corner
4. **Binary search on value**: For kth smallest problems
5. **Corner choice matters**: Top-right or bottom-left only

---

## Next: [08-median-two-arrays.md](./08-median-two-arrays.md)

Finding median of two sorted arrays - a classic hard problem.
