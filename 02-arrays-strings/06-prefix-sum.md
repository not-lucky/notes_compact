# Prefix Sum

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Prefix sum is a preprocessing technique that transforms $\Theta(n)$ range sum queries into $\Theta(1)$ operations. By storing cumulative sums, any range `[i, j]` can be computed as `prefix[j+1] - prefix[i]` in constant time.

## Building Intuition

**Why does subtraction give us range sums?**

The key insight is **telescoping cancellation**. A prefix sum is like a running total:

1. **The Running Total Model**: Imagine a bank account where `prefix[i]` represents your total balance after `i` deposits. The deposits from day 5 to day 10 equal (balance after day 10) minus (balance after day 4).

2. **Mathematical Foundation**:

   ```text
   prefix[j] = arr[0] + arr[1] + ... + arr[j-1]
   prefix[i] = arr[0] + arr[1] + ... + arr[i-1]

   prefix[j] - prefix[i] = arr[i] + arr[i+1] + ... + arr[j-1]
   ```

   The common terms (`arr[0]` to `arr[i-1]`) cancel out!

3. **The Leading Zero Trick**: Adding a 0 at the start (`prefix = [0, ...]`) makes formulas cleaner. Range `[i, j]` = `prefix[j+1] - prefix[i]`. No off-by-one gymnastics.

**Mental Model**: Think of milestones on a highway. Mile marker 50 to mile marker 80 is 30 miles—you subtract the lower marker from the higher one. Prefix sums are just "mile markers" for cumulative values.

**Why Prefix + HashMap Works for "Sum = k"**:

```text
If prefix[j] - prefix[i] = k, then prefix[i] = prefix[j] - k

At position j, we ask: "Have we seen prefix[j] - k before?"
If yes, there's a subarray ending at j with sum k.
The hashmap stores how many times each prefix sum has appeared.
```

## When NOT to Use Prefix Sum

Prefix sums have specific use cases:

1. **Array Modifications Between Queries**: Prefix sum assumes immutable data. If the array changes frequently, updates cost $\Theta(n)$ to rebuild. Use a segment tree ($\Theta(\log n)$ update) or Fenwick tree instead.

2. **Non-Sum Aggregates**: Prefix sum works for sum (and XOR, by extension). For min/max queries, use sparse tables or segment trees. For product, prefix products have overflow issues and division-by-zero pitfalls.

3. **Very Few Queries**: If you only need 1-2 range sums, computing them directly is $\Theta(\text{range\_size})$, while building prefix sum is $\Theta(n)$. Prefix sum pays off when queries are many.

4. **Multi-Dimensional with Updates**: 2D prefix sums exist but are harder to update. For dynamic 2D, consider 2D Fenwick trees.

5. **When Subarray Endpoints Don't Align Simply**: Some problems need subarrays with specific properties where endpoints depend on values, not just indices.

**Red Flags:**

- "Update element, then query" → Segment tree or Fenwick tree
- "Range minimum/maximum" → Sparse table or segment tree
- "Only one or two queries needed" → Direct computation may be simpler

---

## Interview Context

Prefix sum is a preprocessing technique that enables $\Theta(1)$ range sum queries. It appears in:

- Range sum problems
- Subarray sum problems (with hashmap)
- 2D matrix sum queries
- Running totals and cumulative calculations

Understanding prefix sum unlocks efficient solutions for many medium/hard problems.

---

## Core Concept

Prefix sum array stores cumulative sums:

```text
Original:    [1, 2, 3, 4, 5]
Prefix sum:  [1, 3, 6, 10, 15]

prefix[i] = arr[0] + arr[1] + ... + arr[i]

Range sum [i, j] = prefix[j] - prefix[i-1]
(or prefix[j] - prefix[i] + arr[i])
```

### With Leading Zero (More Convenient)

```text
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

    Time: \Theta(n) - We iterate through the array exactly once.
    Space: \Theta(n) - We allocate a new dynamic array of size n+1.

    Example:
    arr = [1, 2, 3, 4, 5]
    → prefix = [0, 1, 3, 6, 10, 15]
    """
    n = len(arr)
    # Python lists are dynamic arrays, but preallocating the size is more efficient
    # than calling .append() n times.
    prefix = [0] * (n + 1)

    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]

    return prefix

def range_sum(prefix: list[int], left: int, right: int) -> int:
    """
    Get sum of arr[left:right+1] in \Theta(1).

    Range sum from index left to right (inclusive)
    = prefix[right + 1] - prefix[left]
    """
    return prefix[right + 1] - prefix[left]
```

### Visual Explanation

```text
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

### Problem: Range Sum Query - Immutable
**Problem Statement:** Given an integer array `nums`, handle multiple queries where each query asks for the sum of the elements of `nums` between indices `left` and `right` inclusive.

**Why it works:**
By precalculating a prefix sum array where `prefix[i]` is the sum of `nums[0...i-1]`, we can compute any range sum `nums[L...R]` in $\Theta(1)$.
1. `Sum(L, R) = Sum(0, R) - Sum(0, L-1)`.
2. Using the prefix array, this is `prefix[R+1] - prefix[L]`.
This shifts the cost from query time ($\Theta(n)$) to initialization time ($\Theta(n)$), making it ideal for many sum queries on a static array.

```python
class NumArray:
    """
    LeetCode 303: Range Sum Query - Immutable

    Time: \Theta(n) to build, \Theta(1) per query.
    Space: \Theta(n) for the prefix array. No recursion used, so call stack space is \Theta(1).
    """
    def __init__(self, nums: list[int]):
        self.prefix = [0]
        for num in nums:
            # Python lists are dynamic arrays, so append is amortized O(1).
            # Building the array of size n takes \Theta(n) total time.
            self.prefix.append(self.prefix[-1] + num)

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]
```

---

## Template: Subarray Sum Equals K

### Problem: Subarray Sum Equals K
**Problem Statement:** Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals to `k`.

**Mental Model:** Think of a hiking trail with elevation markers. You want to find a segment of the trail where the net elevation change is exactly `k`. As you walk, you note your current elevation. To see if a valid segment ends here, you check your notebook (hash map) to see if you previously were at an elevation of `current - k`. If you were, the hike from that point to here has an elevation change of exactly `k`.

**Why it works:**
We use a hash map to store the frequency of all prefix sums seen so far.
1. As we iterate, we calculate the current `prefix_sum`.
2. A subarray ending at the current index has sum `k` if there exists a previous prefix sum `P` such that `prefix_sum - P = k`.
3. This is equivalent to checking if `prefix_sum - k` is in our hash map.
This converts an $\Theta(n^2)$ subarray search into an expected $\Theta(n)$ hash map lookup process.

```python
def subarray_sum(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum equal to k.

    Key insight: If prefix[j] - prefix[i] = k,
    then subarray [i+1, j] has sum k.

    Time: Expected \Theta(n), Worst-case O(n^2).
          - We iterate through the array once: \Theta(n).
          - Hash map lookups and insertions are amortized O(1), but O(n) in the worst
            case due to hash collisions.
    Space: O(n) - Hash map can store up to n distinct prefix sums.

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

```text
We want subarray [i, j] where sum = k
sum[i, j] = prefix[j] - prefix[i-1] = k
→ prefix[j] - k = prefix[i-1]

At each j, we ask: "How many prefix sums equal prefix[j] - k?"
This tells us how many valid subarrays end at j.

HashMap stores how many times each prefix sum has appeared.
```

---

## Template: Subarray Sum Divisible by K

### Problem: Subarray Sums Divisible by K
**Problem Statement:** Given an integer array `nums` and an integer `k`, return the number of non-empty subarrays that have a sum divisible by `k`.

**Why it works:**
If the remainders of two prefix sums divided by `k` are the same, their difference must be divisible by `k`.
1. `(P_j - P_i) % k == 0` if `P_j % k == P_i % k`.
2. We store the frequency of prefix sum remainders in a hash map.
3. For each new prefix sum, its remainder `r` tells us how many previous subarrays can be subtracted to form a sum divisible by `k`.

```python
def subarrays_div_by_k(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum divisible by k.

    Key insight: If prefix[j] % k == prefix[i] % k,
    then (prefix[j] - prefix[i]) % k == 0

    Time: Expected \Theta(n), Worst-case O(n^2).
          Iteration is \Theta(n). Hash map operations are amortized O(1), worst-case O(n).
    Space: O(k) - Hash map stores up to k distinct remainders.

    Example:
    nums = [4, 5, 0, -2, -3, 1], k = 5 → 7
    """
    count = 0
    prefix_sum = 0
    mod_count = {0: 1}

    for num in nums:
        prefix_sum += num
        mod = prefix_sum % k

        # Handle negative mod (in Python, % with negative numbers already works as needed,
        # but in other languages like C++/Java you would need: mod = (mod % k + k) % k)
        # However, making it explicit helps cross-language understanding:
        if mod < 0:
            mod += k

        if mod in mod_count:
            count += mod_count[mod]

        mod_count[mod] = mod_count.get(mod, 0) + 1

    return count
```

---

## Template: 2D Prefix Sum (Range Sum Query 2D)

### Problem: Range Sum Query 2D - Immutable
**Problem Statement:** Given a 2D matrix `matrix`, handle multiple queries where each query asks for the sum of the elements of the rectangle defined by its upper left corner `(row1, col1)` and lower right corner `(row2, col2)`.

**Why it works:**
We precalculate `prefix[i][j]` as the sum of all elements in the rectangle from `(0,0)` to `(i-1, j-1)`.
1. To calculate the sum of any region `(r1, c1)` to `(r2, c2)`, we use the principle of inclusion-exclusion.
2. `Sum = TotalRectangle - TopRectangle - LeftRectangle + OverlapCorner`.
3. In terms of prefix sums: `prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]`.
This provides $\Theta(1)$ query time for any rectangular region.

```python
class NumMatrix:
    """
    LeetCode 304: Range Sum Query 2D - Immutable

    Time: \Theta(m \cdot n) to build, \Theta(1) per query.
    Space: \Theta(m \cdot n) to store the 2D prefix array.
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
        if not self.prefix:
            return 0

        return (
            self.prefix[r2 + 1][c2 + 1]
            - self.prefix[r1][c2 + 1]
            - self.prefix[r2 + 1][c1]
            + self.prefix[r1][c1]
        )
```

### Visual: 2D Prefix Sum Query

```text
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

### Problem: Product of Array Except Self
**Problem Statement:** Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`, without using the division operator.

**Why it works:**
The product of all elements except `nums[i]` is the product of everything to its left multiplied by everything to its right.
1. We make one pass to calculate "prefix products" (cumulative product of elements before `i`).
2. We make a second pass (backwards) to multiply these by "suffix products" (cumulative product of elements after `i`).
This effectively computes the result in $\Theta(n)$ time and $\Theta(1)$ extra space (excluding output).

```python
def product_except_self(nums: list[int]) -> list[int]:
    """
    For each index, product of all elements except self.
    Without using division.

    Time: \Theta(n) - Two passes over the array.
    Space: \Theta(1) extra space (excluding the output array).

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

```text
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

### Problem: Find Pivot Index
**Problem Statement:** Given an array of integers `nums`, calculate the pivot index where the sum of all the numbers strictly to the left of the index is equal to the sum of all the numbers strictly to the right of the index.

**Why it works:**
The total sum `S` of the array is `left_sum + nums[i] + right_sum`.
1. If `left_sum == right_sum`, then `S = 2 * left_sum + nums[i]`.
2. This simplifies to `right_sum = total - left_sum - nums[i]`.
3. We can track `left_sum` as we iterate and check this condition in $\Theta(n)$ time.

```python
def pivot_index(nums: list[int]) -> int:
    """
    Find index where left sum equals right sum.

    Time: \Theta(n) - One pass for sum(), one pass to find pivot.
    Space: \Theta(1) - Only scalar variables used.

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
| Range sum query        | ✓ $\Theta(1)$    | ✗ $O(n)$              |
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
[k, k, k, k] → range [i,j] = k * (j - i + 1)

# Large numbers (overflow)
# In Python, integers have arbitrary precision so they won't overflow,
# but in C++/Java you may need to use long/long long or modular arithmetic.
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

1. **Prefix sum enables $\Theta(1)$ range queries** after $\Theta(n)$ preprocessing
2. **Use leading zero** for cleaner range calculations
3. **Combine with hashmap** for subarray sum problems
4. **For 2D**, use the inclusion-exclusion principle
5. **Product variant** uses prefix and suffix products
6. **Works with negative numbers** (unlike sliding window)

---

## Next: [07-difference-array.md](./07-difference-array.md)

Learn difference arrays for efficient range update operations.
