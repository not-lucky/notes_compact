# Sparse Table

## Overview

Sparse Table is a data structure that answers Range Minimum Query (RMQ) on a static array in $O(1)$ time after $O(N \log N)$ preprocessing. It works for any idempotent operation (an operation $f$ where $f(x, x) = x$), such as `min`, `max`, and `gcd`.

## Core Logic

The Sparse Table stores the result of the operation for all intervals of length $2^k$.
- `st[i][j]` stores the value for the range starting at `i` with length $2^j$: `[i, i + 2^j - 1]`.

For a query $[L, R]$, we find the largest power of 2, $k$, such that $2^k \le R - L + 1$. The result is then `f(st[L][k], st[R - 2^k + 1][k])`.

---

## Implementation Template

```python
import math

class SparseTable:
    def __init__(self, data):
        n = len(data)
        k = n.bit_length() # max power of 2
        self.st = [[0] * k for _ in range(n)]

        for i in range(n):
            self.st[i][0] = data[i]

        for j in range(1, k):
            for i in range(n - (1 << j) + 1):
                self.st[i][j] = min(self.st[i][j-1],
                                    self.st[i + (1 << (j-1))][j-1])

    def query(self, L, R):
        if L > R: return float('inf')
        j = (R - L + 1).bit_length() - 1
        return min(self.st[L][j], self.st[R - (1 << j) + 1][j])
```

---

## Complexity Analysis

| Operation | Complexity | Note |
| :--- | :--- | :--- |
| **Preprocessing**| $O(N \log N)$| Fills the $N \times \log N$ table. |
| **Query** | $O(1)$ | Direct table lookup. |
| **Space** | $O(N \log N)$| Size of the 2D table. |

---

## Sparse Table vs. Others

| Feature | Sparse Table | Segment Tree | Fenwick Tree |
| :--- | :--- | :--- | :--- |
| **Preprocessing**| $O(N \log N)$ | $O(N)$ | $O(N)$ |
| **Query** | $O(1)$ | $O(\log N)$ | $O(\log N)$ |
| **Updates** | **No** (Static) | $O(\log N)$ | $O(\log N)$ |
| **Best for** | RMQ on static arrays | Dynamic range queries | Prefix sums |

## Summary Checklist

- [ ] Is the array static (no updates)?
- [ ] Is the operation idempotent (min, max, gcd)?
- [ ] Are query times critical ($O(1)$ required)?
