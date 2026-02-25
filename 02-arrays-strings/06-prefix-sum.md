# Prefix Sum

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Prefix sum is a preprocessing technique that transforms $\Theta(n)$ range sum queries into $\Theta(1)$ operations. By storing cumulative sums, any range `[i, j]` can be computed as `prefix[j+1] - prefix[i]` in constant time.

## Building Intuition

**Why does subtraction give us range sums?**

The key insight is **telescoping cancellation**. A prefix sum is like a running total.

**The Conveyor Belt Metaphor**: Imagine you are a factory inspector monitoring items on a conveyor belt. Every hour, a packer records the *total* number of items that have passed by since the shift started.
If the shift started at 8:00 AM:
- At 1:00 PM, the log says "500 items total".
- At 4:00 PM, the log says "850 items total".
How many items passed by between 1:00 PM and 4:00 PM? You just subtract: `850 - 500 = 350 items`. You don't need to count every individual hour between 1:00 and 4:00! This is exactly how a prefix sum works.

**Mathematical Foundation**:

```text
prefix[j] = arr[0] + arr[1] + ... + arr[j-1]
prefix[i] = arr[0] + arr[1] + ... + arr[i-1]

prefix[j] - prefix[i] = arr[i] + arr[i+1] + ... + arr[j-1]
```

The common terms (`arr[0]` to `arr[i-1]`) cancel out completely.

**The Leading Zero Trick**: Adding a 0 at the start (`prefix = [0, ...]`) makes formulas cleaner. The sum of the range `[i, j]` becomes `prefix[j+1] - prefix[i]`. This avoids messy off-by-one errors and special handling for `i=0`.

## When NOT to Use Prefix Sum

Prefix sums have specific constraints:

1. **Array Modifications Between Queries**: Prefix sum assumes immutable data. If the array changes frequently, updating the prefix array costs $\Theta(n)$ per change. Use a segment tree ($\Theta(\log n)$ update) or Fenwick tree instead.
2. **Non-Reversible Operations**: Prefix sum relies on an inverse operation (like subtraction for addition, or division for multiplication). It works for sum and XOR. It does **not** work for min/max queries because you cannot "subtract" a minimum. Use sparse tables or segment trees for min/max.
3. **Very Few Queries**: If you only need 1 or 2 range sums, computing them directly is $\Theta(\text{range\_size})$. Building the prefix array takes $\Theta(n)$. Prefix sum only pays off when you have many queries.

**Red Flags:**
- "Update element, then query" → Segment tree / Fenwick tree
- "Range minimum/maximum" → Sparse table / Segment tree
- "Only one query" → Direct iteration

---

## Core Concept

A prefix sum array stores cumulative sums:

```text
Original:    [1, 2, 3, 4, 5]
Prefix sum:  [0, 1, 3, 6, 10, 15]
              ↑
              Leading zero makes range queries cleaner

Range sum [i, j] = prefix[j+1] - prefix[i]
```

### Visual Explanation

```text
arr    = [1, 2, 3, 4, 5]
         0  1  2  3  4  (indices)

prefix = [0, 1, 3, 6, 10, 15]
          0  1  2  3  4   5   (indices)

Range sum [1, 3] (which is arr[1] + arr[2] + arr[3])
= 2 + 3 + 4 = 9

Using prefix array:
= prefix[3+1] - prefix[1] = 10 - 1 = 9 ✓
```

---

## Template: Build Prefix Sum

```python
def build_prefix_sum(arr: list[int]) -> list[int]:
    """
    Build prefix sum array with a leading zero.

    Time Complexity: \Theta(n) - We iterate through the array exactly once.
    Space Complexity: \Theta(n) - We allocate a new array of size n+1.

    Example:
        arr = [1, 2, 3, 4, 5]
        -> prefix = [0, 1, 3, 6, 10, 15]
    """
    n = len(arr)
    # Preallocating the size is more efficient than calling .append() n times.
    prefix = [0] * (n + 1)

    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]

    return prefix

def range_sum(prefix: list[int], left: int, right: int) -> int:
    """
    Get sum of arr[left...right] inclusive in \Theta(1) time.
    """
    return prefix[right + 1] - prefix[left]
```

---

## Application: Range Sum Query (Immutable)

### Problem Statement
Given an integer array `nums`, handle multiple queries asking for the sum of elements between indices `left` and `right` inclusive.

**Why it works:**
By precalculating a prefix sum array where `prefix[i]` is the sum of `nums[0...i-1]`, we can compute any range sum `nums[left...right]` as `prefix[right+1] - prefix[left]` in exactly $\Theta(1)$ time. This shifts the cost from query time to initialization time.

```python
class NumArray:
    """
    LeetCode 303: Range Sum Query - Immutable

    Time Complexity:
        __init__: \Theta(n) to build the prefix array.
        sumRange: \Theta(1) per query.
    Space Complexity: \Theta(n) to store the prefix array.
    """
    def __init__(self, nums: list[int]):
        self.prefix = [0] * (len(nums) + 1)
        for i in range(len(nums)):
            self.prefix[i + 1] = self.prefix[i] + nums[i]

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]
```

---

## Application: Subarray Sum Equals K

### Problem Statement
Given an integer array `nums` and an integer `k`, return the total number of subarrays whose sum equals `k`.

**The Ledger Metaphor:**
Imagine a ledger tracking a company's total profit over time. You want to find periods where exactly $10,000 was made. If the total profit today is $50,000, you check your records to see how many past days ended with exactly $40,000 in total profit. Every such day marks the start of a period where exactly $10,000 was earned.

**Why it works:**
We use a hash map to store the frequency of all prefix sums seen so far.
1. As we iterate, we calculate the current `prefix_sum`.
2. A subarray ending at the current index has sum `k` if there exists a previous prefix sum `P` such that `prefix_sum - P = k`.
3. This is equivalent to checking if `prefix_sum - k` is in our hash map.

```text
We want subarray [i, j] where sum = k
sum[i, j] = prefix[j] - prefix[i-1] = k
→ prefix[i-1] = prefix[j] - k

At each j, we ask the hash map: "How many times have we seen (prefix[j] - k)?"
```

```python
def subarray_sum(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum equal to k.

    Time Complexity: \Theta(n) expected, O(n^2) worst-case. We iterate once. Hash map
                     lookups are amortized \Theta(1), but O(n) worst-case due to collisions.
    Space Complexity: O(n) bounds the number of distinct prefix sums in the hash map.
    """
    count = 0
    prefix_sum = 0
    # Base case: A prefix sum of 0 has been seen exactly once (the empty prefix).
    prefix_count = {0: 1}

    for num in nums:
        prefix_sum += num

        # If (prefix_sum - k) exists, we found valid subarrays ending here.
        target = prefix_sum - k
        if target in prefix_count:
            count += prefix_count[target]

        # Record current prefix sum
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return count
```

---

## Application: Subarray Sum Divisible by K

### Problem Statement
Given an integer array `nums` and an integer `k`, return the number of non-empty subarrays that have a sum divisible by `k`.

**Why it works:**
If the remainders of two prefix sums divided by `k` are identical, their difference must be a multiple of `k`.
For example, if `P1 = 17` and `P2 = 5`, and `k = 4`.
`17 % 4 = 1` and `5 % 4 = 1`.
Their difference is `17 - 5 = 12`, which is divisible by 4.

```python
def subarrays_div_by_k(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum divisible by k.

    Time Complexity: \Theta(n) expected. Iteration is \Theta(n).
    Space Complexity: \Theta(k) - Hash map stores at most k distinct remainders (0 to k-1).
    """
    count = 0
    prefix_sum = 0
    mod_count = {0: 1}  # Base case: Remainder 0 seen once.

    for num in nums:
        prefix_sum += num
        mod = prefix_sum % k

        # In languages like C++/Java, modulo of negative numbers can be negative.
        # Python handles this mathematically correctly (e.g., -2 % 5 = 3),
        # but to be universally safe across languages:
        if mod < 0:
            mod += k

        if mod in mod_count:
            count += mod_count[mod]

        mod_count[mod] = mod_count.get(mod, 0) + 1

    return count
```

---

## Application: 2D Prefix Sum (Range Sum Query 2D)

### Problem Statement
Given a 2D matrix, handle multiple queries asking for the sum of elements inside a rectangle defined by its upper-left corner `(r1, c1)` and lower-right corner `(r2, c2)`.

**Why it works:**
We precalculate `prefix[i][j]` as the sum of all elements in the rectangle from `(0,0)` to `(i-1, j-1)`.
Using the **Principle of Inclusion-Exclusion**:
To get the area of the query rectangle, we take the massive rectangle starting from `(0,0)` to `(r2,c2)`. Then we subtract the top rectangle and the left rectangle. Since we subtracted the top-left corner twice, we add it back once.

```text
Answer = Total - Top - Left + Overlap
       = prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]
```

```python
class NumMatrix:
    """
    LeetCode 304: Range Sum Query 2D - Immutable

    Time Complexity: \Theta(m \cdot n) to build, \Theta(1) per query.
    Space Complexity: \Theta(m \cdot n) to store the 2D prefix array.
    """
    def __init__(self, matrix: list[list[int]]):
        if not matrix or not matrix[0]:
            self.prefix = []
            return

        rows, cols = len(matrix), len(matrix[0])
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]

        for r in range(rows):
            for c in range(cols):
                self.prefix[r + 1][c + 1] = (
                    matrix[r][c]
                    + self.prefix[r][c + 1]  # Top rectangle
                    + self.prefix[r + 1][c]  # Left rectangle
                    - self.prefix[r][c]      # Subtract overlap (top-left corner)
                )

    def sumRegion(self, r1: int, c1: int, r2: int, c2: int) -> int:
        if not self.prefix:
            return 0

        return (
            self.prefix[r2 + 1][c2 + 1]
            - self.prefix[r1][c2 + 1]
            - self.prefix[r2 + 1][c1]
            + self.prefix[r1][c1]
        )
```

---

## Application: Product of Array Except Self

### Problem Statement
Given an integer array `nums`, return an array `answer` where `answer[i]` is the product of all elements of `nums` except `nums[i]`, **without using division**.

**Why it works:**
The product of all elements except `nums[i]` is exactly the product of everything to its **left** multiplied by everything to its **right**. We can calculate prefix products and suffix products in two sweeps.

```python
def product_except_self(nums: list[int]) -> list[int]:
    """
    For each index, product of all elements except self, without division.

    Time Complexity: \Theta(n) - Two passes over the array.
    Space Complexity: \Theta(1) auxiliary space (excluding the output array).
    """
    n = len(nums)
    result = [1] * n

    # First pass: calculate prefix products (product of elements to the left)
    prefix_product = 1
    for i in range(n):
        result[i] = prefix_product
        prefix_product *= nums[i]

    # Second pass: multiply by suffix products (product of elements to the right)
    suffix_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix_product
        suffix_product *= nums[i]

    return result
```

---

## Application: Pivot Index

### Problem Statement
Find the pivot index where the sum of all numbers to the left equals the sum of all numbers to the right.

**Why it works:**
The total sum is `left_sum + nums[i] + right_sum`. Therefore, `right_sum = total_sum - left_sum - nums[i]`. We can calculate `total_sum` upfront, then iterate while tracking `left_sum`.

```python
def pivot_index(nums: list[int]) -> int:
    """
    Find index where left sum equals right sum.

    Time Complexity: \Theta(n) - One pass for sum(), one pass to find pivot.
    Space Complexity: \Theta(1) - Only scalar variables used.
    """
    total = sum(nums)
    left_sum = 0

    for i, num in enumerate(nums):
        right_sum = total - left_sum - num

        if left_sum == right_sum:
            return i

        left_sum += num

    return -1
```

---

## Prefix Sum vs Sliding Window

| Scenario | Prefix Sum | Sliding Window |
| :--- | :--- | :--- |
| **Contains negative numbers** | ✓ Works flawlessly | ✗ Fails (window logic breaks) |
| **Exact sum queries** | ✓ Excellent (with Hash Map) | ✓ Good (if all positive) |
| **Data modification** | ✗ Fails (immutable assumption) | N/A |
| **Range sum queries** | ✓ $\Theta(1)$ per query | ✗ O(n) per query |
| **Min/Max subarray length** | ✗ Hard to optimize | ✓ Excellent |

---

## Key Takeaways

1. **Prefix sum enables $\Theta(1)$ range queries** after an initial $\Theta(n)$ preprocessing step.
2. **Always use a leading zero** to avoid off-by-one errors and cleanly handle queries starting at index 0.
3. **Combine with Hash Maps** to solve "subarray sums equal to K" or "subarray sums divisible by K" problems.
4. **Use Inclusion-Exclusion** for 2D matrix sum queries.
5. **Prefix/Suffix arrays** (like Product Except Self) follow the exact same logic: precalculate running values from left-to-right and right-to-left.
6. **Handles Negative Numbers** naturally, unlike the sliding window technique.

---

## Next: [07-difference-array.md](./07-difference-array.md)

Learn difference arrays, the inverse of prefix sums, for efficient range update operations.