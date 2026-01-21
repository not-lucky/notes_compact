# Fenwick Tree (Binary Indexed Tree)

> **Prerequisites:** [15-bit-manipulation](../15-bit-manipulation/README.md)

## Overview

A Fenwick Tree, also known as a Binary Indexed Tree (BIT), is a data structure that provides efficient methods for calculation and manipulation of the prefix sums of an array of values.

Compared to a Segment Tree, a BIT is:
-   **Easier to implement**: Much shorter code.
-   **More space-efficient**: Uses $O(N)$ space exactly.
-   **More limited**: Primarily handles prefix sums and point updates.

## Key Logic: The Lowbit

The core of BIT is the `lowbit` operation: `i & -i`. This extracts the value of the least significant bit of `i`.
-   To move to the parent (for updates): `i += i & -i`
-   To move to the previous prefix (for queries): `i -= i & -i`

---

## Implementation Template

```python
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i, delta):
        """Adds delta to element at index i (1-indexed)."""
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        """Returns the prefix sum of elements from 1 to i (1-indexed)."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def query_range(self, l, r):
        """Returns sum of elements in range [l, r]."""
        return self.query(r) - self.query(l - 1)
```

---

## Complexity Analysis

| Operation | Complexity | Note |
| :--- | :--- | :--- |
| **Update** | $O(\log N)$ | Traverses bits of the index. |
| **Query** | $O(\log N)$ | Traverses bits of the index. |
| **Space** | $O(N)$ | Exactly $N+1$ integers. |

---

## Common Use Cases

1.  **Prefix Sums**: Standard use case.
2.  **Inversion Counting**: Count how many pairs $(i, j)$ exist such that $i < j$ and $arr[i] > arr[j]$.
3.  **Range Updates & Point Queries**: By storing differences between adjacent elements in the BIT.
4.  **2D Fenwick Tree**: For sum queries on a 2D grid.

## Summary Checklist

- [ ] Are indices 1-indexed? (Crucial for `i & -i`).
- [ ] Is the operation invertible (for range queries)? If not, use Segment Tree.
- [ ] Memory constraints tight? BIT is better than Segment Tree.
