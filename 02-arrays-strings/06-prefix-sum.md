# Prefix Sum

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

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

| Use Case | Prefix Sum | Sliding Window |
|----------|------------|----------------|
| Has negative numbers | ✓ Yes | ✗ No |
| Exact sum queries | ✓ Yes | ✓ Yes (for positives) |
| Modification needed | ✗ No (immutable) | N/A |
| Range sum query | ✓ O(1) | ✗ O(n) |
| Minimum/maximum window | ✗ Limited | ✓ Yes |

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

| # | Problem | Difficulty | Key Technique |
|---|---------|------------|---------------|
| 1 | Range Sum Query - Immutable | Easy | Basic prefix sum |
| 2 | Range Sum Query 2D - Immutable | Medium | 2D prefix sum |
| 3 | Subarray Sum Equals K | Medium | Prefix + hashmap |
| 4 | Subarray Sums Divisible by K | Medium | Mod prefix sum |
| 5 | Product of Array Except Self | Medium | Prefix + suffix |
| 6 | Find Pivot Index | Easy | Left = right sum |
| 7 | Continuous Subarray Sum | Medium | Mod prefix sum |
| 8 | Maximum Size Subarray Sum Equals K | Medium | Prefix + hashmap |

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
