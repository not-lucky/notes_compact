# Matrix Search

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md)

## Interview Context

Matrix search problems are extremely common in FANG interviews because they test multiple dimensions of problem-solving:

1. **Dimensional thinking**: Can you elegantly map a 2D structure to a 1D sequence?
2. **Property exploitation**: Can you leverage the specific sorted properties (Type 1 vs. Type 2) to eliminate search space efficiently?
3. **Domain reduction**: Can you define a path that guarantees progress towards the target?
4. **Binary Search on Answer**: Can you recognize when the search space is the *range of values* rather than the *indices*?

---

## The Core Distinction: Two Types of "Sorted" Matrices

This is the critical distinction that changes EVERYTHING about your approach. In an interview, **always clarify which type you are dealing with before writing code**.

### TYPE 1: Row-wise AND Column-wise Sorted
Often called "Partially Sorted" or "Monotonic Matrix".
- Each row is sorted left-to-right.
- Each column is sorted top-to-bottom.
- **CRITICAL**: No global order guarantee (e.g., the last element of row $i$ might be larger than the first element of row $i+1$).

```
┌────────────────────────┐
│  1    4    7   11      │  11 > 2, so it's not globally sorted
│  2    5    8   12      │  You CANNOT treat this as a 1D array
│  3    6    9   16      │
│ 10   13   14   17      │
└────────────────────────┘
```

### TYPE 2: Fully Sorted (Row-major Order)
Strictly sorted matrix.
- Each row is sorted.
- The first element of each row is strictly greater than the last element of the previous row.
- **CRITICAL**: It is structurally identical to a sorted 1D array wrapped into 2D.

```
┌────────────────────────┐
│  1    3    5    7      │  7 < 10
│ 10   11   16   20      │  20 < 23
│ 23   30   34   60      │  This is just [1,3,5,7,10,11,16,20,23,30,34,60]
└────────────────────────┘
```

---

## Strategy 1: The 1D Mapping (For Type 2 Fully Sorted)

A Type 2 matrix is just a sorted 1D array displayed in rows. We can run standard binary search by converting 1D indices to 2D coordinates on the fly.

### The Math:
For a matrix of dimensions `m x n` (m rows, n cols):
- The conceptual 1D array has indices from `0` to `(m * n) - 1`.
- Given a 1D index `mid`:
  - `row = mid // n` (integer division by number of columns)
  - `col = mid % n` (modulo by number of columns)

### Implementation (LeetCode 74: Search a 2D Matrix)

```python
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    """
    Search in a fully sorted (Type 2) matrix.
    Treat as 1D array with index conversion.

    Time: O(log(m * n))
    Space: O(1)
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    left, right = 0, (m * n) - 1

    while left <= right:
        mid = left + (right - left) // 2

        # Convert 1D index back to 2D coordinates
        row, col = divmod(mid, n) # Equivalent to: mid // n, mid % n
        val = matrix[row][col]

        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False
```

*Note: You could also do two binary searches (one to find the row, one within the row), but treating it as a 1D array is cleaner and mathematically elegant. Both are $O(\log(m \cdot n))$.*

---

## Strategy 2: The "Staircase" or "Saddle Point" (For Type 1)

For Type 1 (Row/Col sorted), standard binary search fails because flattening it doesn't yield a sorted 1D array.

**The Insight:** We need a starting point where we can make a deterministic binary decision (eliminate a row OR eliminate a column).

If we start at the **Top-Left (0, 0)**:
- Go Right -> Values increase
- Go Down -> Values increase
- *Problem: If target > current, which way do we go? We can't decide!*

If we start at the **Top-Right (0, n-1)**:
- Go Left -> Values decrease (entire column eliminated)
- Go Down -> Values increase (entire row eliminated)
- *Perfect! Every step securely eliminates an entire row or column.*

### Implementation (LeetCode 240: Search a 2D Matrix II)

```python
def searchMatrixII(matrix: list[list[int]], target: int) -> bool:
    """
    Search in a row-sorted AND col-sorted (Type 1) matrix.
    Start at Top-Right and eliminate row or col at each step.

    Time: O(m + n) - in worst case we traverse one full row and col
    Space: O(1)
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])

    # Start at Top-Right corner
    r, c = 0, n - 1

    while r < m and c >= 0:
        if matrix[r][c] == target:
            return True
        elif matrix[r][c] > target:
            # Current is too big, and everything below it is even bigger.
            # So the target cannot be in this column. Move left.
            c -= 1
        else:
            # Current is too small, and everything left of it is even smaller.
            # So the target cannot be in this row. Move down.
            r += 1

    return False
```

*Alternative: Starting at Bottom-Left `(m-1, 0)` also works (Up = decrease, Right = increase). Never start at Top-Left or Bottom-Right.*

---

## Strategy 3: Binary Search on Answer / Value Range

Some matrix problems don't ask you to *find a target*, but rather ask for a property across the matrix, like "Kth smallest element" or "Median".

When you see a Type 1 Matrix (Row/Col sorted) AND you need to find an element based on its rank (Kth, Median):
**Use Binary Search on the Value Range.**

### The Pattern
1. Search space is `[matrix[0][0], matrix[m-1][n-1]]` (min and max values in the matrix).
2. Given a `mid` value, count how many elements in the matrix are $\le$ `mid`.
3. If count < K, `mid` is too small (search right). Else, search left.
4. Counting takes $O(m+n)$ using the Staircase method!

### Implementation (LeetCode 378: Kth Smallest Element in a Sorted Matrix)

```python
def kthSmallest(matrix: list[list[int]], k: int) -> int:
    """
    Find the Kth smallest element in a Type 1 Matrix.
    Uses Binary Search on the value range + Staircase counting.

    Time: O((m+n) * log(MAX_VAL - MIN_VAL))
    Space: O(1)
    """
    m, n = len(matrix), len(matrix[0])

    def count_less_equal(mid_val: int) -> int:
        """Counts how many elements in matrix are <= mid_val in O(m+n) time."""
        count = 0
        r, c = m - 1, 0  # Start Bottom-Left

        while r >= 0 and c < n:
            if matrix[r][c] <= mid_val:
                # If current is <= mid_val, everything above it in this col is also <=
                count += (r + 1)
                c += 1       # Move right to look for more
            else:
                r -= 1       # Move up to find smaller elements
        return count

    # Value range binary search
    left = matrix[0][0]
    right = matrix[m-1][n-1]

    while left < right:
        mid = left + (right - left) // 2

        if count_less_equal(mid) < k:
            left = mid + 1
        else:
            right = mid  # mid could be the answer

    return left
```

*FANG Note: This is a highly desired pattern at Google and Meta. Master the transition between "binary searching indices" and "binary searching the answer space".*

---

## Applications & Variations

### 1. Count Negatives in Sorted Matrix (LeetCode 1351)
Matrix is sorted in non-increasing (descending) order both row-wise and col-wise.
**Approach**: Staircase. Start top-right. If `grid[r][c] < 0`, then everything below it is also `< 0` (since it's sorted descending). Count `m - r` and move left. If `grid[r][c] >= 0`, move down.
**Time**: $O(m+n)$

### 2. Leftmost Column with at Least a One (Premium)
Binary matrix where rows are sorted (0s then 1s).
**Approach**: Staircase from Top-Right. If `1`, record column and move left. If `0`, move down.
**Time**: $O(m+n)$

---

## Complexity Summary

| Problem Type | Best Approach | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Search (Type 2 - Fully Sorted)** | 1D mapping Binary Search | $\mathcal{O}(\log(m \cdot n))$ | $\mathcal{O}(1)$ |
| **Search (Type 1 - Row/Col Sorted)** | Staircase from Corner (Top-R/Bot-L) | $\mathcal{O}(m + n)$ | $\mathcal{O}(1)$ |
| **Kth Smallest / Median** | BS on Value + Staircase Counting | $\mathcal{O}((m+n) \log(\text{Range}))$ | $\mathcal{O}(1)$ |
| **Count conditional elements** | Staircase (if monotonic) | $\mathcal{O}(m + n)$ | $\mathcal{O}(1)$ |

---

## Common Interview Pitfalls

1. **Blindly applying Binary Search to Type 1**
   - Flattening a Type 1 matrix does NOT yield a sorted array. Always verify strict row-major sorting before using 1D mapping.
2. **Starting Staircase from the wrong corner**
   - Top-Left (0,0) and Bottom-Right (m-1, n-1) are traps. Both directions increase or decrease respectively. You MUST start where one direction increases and the other decreases (Top-Right or Bottom-Left).
3. **Using $O(m \log n)$ when $O(m+n)$ is expected**
   - For Type 1 search, binary searching each row takes $O(m \log n)$. This is usually considered suboptimal by interviewers compared to the elegant $O(m+n)$ staircase method.
4. **Getting the DivMod wrong**
   - `row = mid // cols`
   - `col = mid % cols`
   - **Never use `rows` here!** You are slicing the 1D array into chunks of length `cols`.

---

## Edge Cases to Check
- `matrix = []` or `matrix = [[]]` (Empty structures)
- `m = 1` or `n = 1` (1D array disguised as 2D)
- `target` is smaller than `matrix[0][0]` or larger than `matrix[-1][-1]`
- All elements are the same

---

## Next: [08-median-two-arrays.md](./08-median-two-arrays.md)

Finding median of two sorted arrays - a classic hard problem.
