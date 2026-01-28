# Prefix Sum

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Prefix sum is a preprocessing technique that transforms O(n) range sum queries into O(1) operations. By storing cumulative sums, any range [i, j] can be computed as prefix[j+1] - prefix[i] in constant time.

## Building Intuition

**Why does subtraction give us range sums?**

The key insight is **telescoping cancellation**. A prefix sum is like a running total:

1. **The Running Total Model**: Imagine a bank account where prefix[i] represents your total balance after i deposits. The deposits from day 5 to day 10 equal (balance after day 10) minus (balance after day 4).

2. **Mathematical Foundation**:

   ```
   prefix[j] = arr[0] + arr[1] + ... + arr[j-1]
   prefix[i] = arr[0] + arr[1] + ... + arr[i-1]

   prefix[j] - prefix[i] = arr[i] + arr[i+1] + ... + arr[j-1]
   ```

   The common terms (arr[0] to arr[i-1]) cancel out!

3. **The Leading Zero Trick**: Adding a 0 at the start (`prefix = [0, ...]`) makes formulas cleaner. Range [i, j] = prefix[j+1] - prefix[i]. No off-by-one gymnastics.

**Mental Model**: Think of milestones on a highway. Mile marker 50 to mile marker 80 is 30 miles—you subtract the lower marker from the higher one. Prefix sums are just "mile markers" for cumulative values.

**Why Prefix + HashMap Works for "Sum = k"**:

```
If prefix[j] - prefix[i] = k, then prefix[i] = prefix[j] - k

At position j, we ask: "Have we seen prefix[j] - k before?"
If yes, there's a subarray ending at j with sum k.
The hashmap stores how many times each prefix sum has appeared.
```

## When NOT to Use Prefix Sum

Prefix sums have specific use cases:

1. **Array Modifications Between Queries**: Prefix sum assumes immutable data. If the array changes frequently, updates cost O(n) to rebuild. Use a segment tree (O(log n) update) or Fenwick tree instead.

2. **Non-Sum Aggregates**: Prefix sum works for sum (and XOR, by extension). For min/max queries, use sparse tables or segment trees. For product, prefix products have overflow issues and division-by-zero pitfalls.

3. **Very Few Queries**: If you only need 1-2 range sums, computing them directly is O(range_size), while building prefix sum is O(n). Prefix sum pays off when queries are many.

4. **Multi-Dimensional with Updates**: 2D prefix sums exist but are harder to update. For dynamic 2D, consider 2D Fenwick trees.

5. **When Subarray Endpoints Don't Align Simply**: Some problems need subarrays with specific properties where endpoints depend on values, not just indices.

**Red Flags:**

- "Update element, then query" → Segment tree or Fenwick tree
- "Range minimum/maximum" → Sparse table or segment tree
- "Only one or two queries needed" → Direct computation may be simpler

---

## Interview Context

Prefix sum is a preprocessing technique that enables O(1) range sum queries. It appears in:

- Range sum problems
- Subarray sum problems (with hashmap)
- 2D matrix sum queries
- Running totals and cumulative calculations

Understanding prefix sum unlocks efficient solutions for many medium/hard problems.

---

## Core Concept

Prefix sum array stores cumulative sums:

```
Original:    [1, 2, 3, 4, 5]
Prefix sum:  [1, 3, 6, 10, 15]

prefix[i] = arr[0] + arr[1] + ... + arr[i]

Range sum [i, j] = prefix[j] - prefix[i-1]
(or prefix[j] - prefix[i] + arr[i])
```

### With Leading Zero (More Convenient)

```
Original:    [1, 2, 3, 4, 5]
Prefix sum:  [0, 1, 3, 6, 10, 15]
              ↑
              dummy (makes range queries cleaner)

Range sum [i, j] = prefix[j+1] - prefix[i]
```

---

## Template: Build Prefix Sum

```python
def build_prefix_sum(arr: list[int]) -> list[int]:
    """
    Build prefix sum array with leading zero.

    Time: O(n)
    Space: O(n)

    Example:
    arr = [1, 2, 3, 4, 5]
    → prefix = [0, 1, 3, 6, 10, 15]
    """
    n = len(arr)
    prefix = [0] * (n + 1)

    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]

    return prefix


def range_sum(prefix: list[int], left: int, right: int) -> int:
    """
    Get sum of arr[left:right+1] in O(1).

    Range sum from index left to right (inclusive)
    = prefix[right + 1] - prefix[left]
    """
    return prefix[right + 1] - prefix[left]
```

### Visual Explanation

```
arr    = [1, 2, 3, 4, 5]
         0  1  2  3  4  (indices)

prefix = [0, 1, 3, 6, 10, 15]
          0  1  2  3  4   5   (indices)

Range sum [1, 3] (arr[1] + arr[2] + arr[3])
= 2 + 3 + 4 = 9
= prefix[4] - prefix[1] = 10 - 1 = 9 ✓
```

---

## Template: Range Sum Query (Immutable)

```python
class NumArray:
    """
    LeetCode 303: Range Sum Query - Immutable

    Time: O(n) to build, O(1) per query
    Space: O(n)
    """
    def __init__(self, nums: list[int]):
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]
```

---

## Template: Subarray Sum Equals K

```python
def subarray_sum(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum equal to k.

    Key insight: If prefix[j] - prefix[i] = k,
    then subarray [i+1, j] has sum k.

    Time: O(n)
    Space: O(n)

    Example:
    nums = [1, 1, 1], k = 2 → 2
    nums = [1, 2, 3], k = 3 → 2 ([1,2] and [3])
    """
    count = 0
    prefix_sum = 0
    prefix_count = {0: 1}  # prefix_sum → count

    for num in nums:
        prefix_sum += num

        # If (prefix_sum - k) exists, found subarrays ending here
        if prefix_sum - k in prefix_count:
            count += prefix_count[prefix_sum - k]

        # Record current prefix sum
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return count
```

### Why This Works

```
We want subarray [i, j] where sum = k
sum[i, j] = prefix[j] - prefix[i-1] = k
→ prefix[j] - k = prefix[i-1]

At each j, we ask: "How many prefix sums equal prefix[j] - k?"
This tells us how many valid subarrays end at j.

HashMap stores how many times each prefix sum has appeared.
```

---

## Template: Subarray Sum Divisible by K

```python
def subarrays_div_by_k(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum divisible by k.

    Key insight: If prefix[j] % k == prefix[i] % k,
    then (prefix[j] - prefix[i]) % k == 0

    Time: O(n)
    Space: O(k)

    Example:
    nums = [4, 5, 0, -2, -3, 1], k = 5 → 7
    """
    count = 0
    prefix_sum = 0
    mod_count = {0: 1}

    for num in nums:
        prefix_sum += num
        mod = prefix_sum % k

        # Handle negative mod
        if mod < 0:
            mod += k

        if mod in mod_count:
            count += mod_count[mod]

        mod_count[mod] = mod_count.get(mod, 0) + 1

    return count
```

---

## Template: 2D Prefix Sum (Range Sum Query 2D)

```python
class NumMatrix:
    """
    LeetCode 304: Range Sum Query 2D - Immutable

    Time: O(m*n) to build, O(1) per query
    Space: O(m*n)
    """
    def __init__(self, matrix: list[list[int]]):
        if not matrix or not matrix[0]:
            self.prefix = []
            return

        m, n = len(matrix), len(matrix[0])
        # prefix[i][j] = sum of rectangle from (0,0) to (i-1,j-1)
        self.prefix = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m):
            for j in range(n):
                self.prefix[i + 1][j + 1] = (
                    matrix[i][j]
                    + self.prefix[i][j + 1]
                    + self.prefix[i + 1][j]
                    - self.prefix[i][j]
                )

    def sumRegion(self, r1: int, c1: int, r2: int, c2: int) -> int:
        """
        Sum of rectangle from (r1,c1) to (r2,c2) inclusive.
        """
        return (
            self.prefix[r2 + 1][c2 + 1]
            - self.prefix[r1][c2 + 1]
            - self.prefix[r2 + 1][c1]
            + self.prefix[r1][c1]
        )
```

### Visual: 2D Prefix Sum Query

```
Query rectangle: (r1,c1) to (r2,c2)

┌─────────────────────────┐
│                         │
│   ┌─────┬───────────┐   │
│   │  A  │     B     │   │
│   ├─────┼───────────┤   │
│   │  C  │  QUERY    │   │
│   │     │  REGION   │   │
│   └─────┴───────────┘   │
│                         │
└─────────────────────────┘

Answer = Total - A - B - C + overlap
       = prefix[r2+1][c2+1]
         - prefix[r1][c2+1]    (remove top)
         - prefix[r2+1][c1]    (remove left)
         + prefix[r1][c1]      (add back corner, subtracted twice)
```

---

## Template: Product of Array Except Self

```python
def product_except_self(nums: list[int]) -> list[int]:
    """
    For each index, product of all elements except self.
    Without using division.

    Time: O(n)
    Space: O(1) excluding output

    Uses prefix and suffix products.

    Example:
    [1, 2, 3, 4] → [24, 12, 8, 6]
    """
    n = len(nums)
    result = [1] * n

    # First pass: prefix products (product of all left elements)
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    # Second pass: suffix products (multiply by all right elements)
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result
```

### Visual Trace

```
nums = [1, 2, 3, 4]

After prefix pass:
result = [1, 1, 2, 6]
          ↑  ↑  ↑  ↑
          1  1  1×2 1×2×3

After suffix pass:
result = [24, 12, 8, 6]
          ↑    ↑   ↑  ↑
       1×24  1×12 2×4 6×1
```

---

## Template: Pivot Index

```python
def pivot_index(nums: list[int]) -> int:
    """
    Find index where left sum equals right sum.

    Time: O(n)
    Space: O(1)

    Example:
    [1, 7, 3, 6, 5, 6] → 3 (left sum = 11, right sum = 11)
    """
    total = sum(nums)
    left_sum = 0

    for i, num in enumerate(nums):
        # Right sum = total - left_sum - current
        right_sum = total - left_sum - num

        if left_sum == right_sum:
            return i

        left_sum += num

    return -1
```

---

## Prefix Sum vs Sliding Window

| Use Case               | Prefix Sum       | Sliding Window        |
| ---------------------- | ---------------- | --------------------- |
| Has negative numbers   | ✓ Yes            | ✗ No                  |
| Exact sum queries      | ✓ Yes            | ✓ Yes (for positives) |
| Modification needed    | ✗ No (immutable) | N/A                   |
| Range sum query        | ✓ O(1)           | ✗ O(n)                |
| Minimum/maximum window | ✗ Limited        | ✓ Yes                 |

---

## Edge Cases

```python
# Empty array
[] → handle specially

# Single element
[5] → prefix = [0, 5]

# All zeros
[0, 0, 0] → all range sums = 0

# All same values
[k, k, k, k] → range [i,j] = k × (j - i + 1)

# Large numbers (overflow)
Consider using modular arithmetic if needed
```

---

## Practice Problems

| #   | Problem                            | Difficulty | Key Technique    |
| --- | ---------------------------------- | ---------- | ---------------- |
| 1   | Range Sum Query - Immutable        | Easy       | Basic prefix sum |
| 2   | Range Sum Query 2D - Immutable     | Medium     | 2D prefix sum    |
| 3   | Subarray Sum Equals K              | Medium     | Prefix + hashmap |
| 4   | Subarray Sums Divisible by K       | Medium     | Mod prefix sum   |
| 5   | Product of Array Except Self       | Medium     | Prefix + suffix  |
| 6   | Find Pivot Index                   | Easy       | Left = right sum |
| 7   | Continuous Subarray Sum            | Medium     | Mod prefix sum   |
| 8   | Maximum Size Subarray Sum Equals K | Medium     | Prefix + hashmap |

---

## Key Takeaways

1. **Prefix sum enables O(1) range queries** after O(n) preprocessing
2. **Use leading zero** for cleaner range calculations
3. **Combine with hashmap** for subarray sum problems
4. **For 2D**, inclusion-exclusion principle
5. **Product variant** uses prefix and suffix products
6. **Works with negative numbers** (unlike sliding window)

---

## Next: [07-difference-array.md](./07-difference-array.md)

Learn difference arrays for efficient range update operations.
