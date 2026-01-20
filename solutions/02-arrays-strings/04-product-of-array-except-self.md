# Product of Array Except Self

## Problem Statement

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.

The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

**Constraint:** Must run in O(n) time WITHOUT using division.

**Example:**
```
Input: nums = [1, 2, 3, 4]
Output: [24, 12, 8, 6]

Explanation:
- answer[0] = 2 * 3 * 4 = 24
- answer[1] = 1 * 3 * 4 = 12
- answer[2] = 1 * 2 * 4 = 8
- answer[3] = 1 * 2 * 3 = 6
```

## Building Intuition

### Why This Works

The product of all elements except `nums[i]` can be decomposed into two parts: the product of everything to the left of `i`, and the product of everything to the right of `i`. These two products are independent and can be computed separately.

The prefix product at position `i` captures "the product of all elements before `i`". The suffix product captures "the product of all elements after `i`". Multiplying these together gives exactly what we need: the product of all elements except the one at position `i`.

This decomposition avoids division entirely. Division would be problematic anyway: it fails with zeros and the problem explicitly forbids it. The prefix/suffix approach handles zeros naturally because they just propagate through the products.

### How to Discover This

When you cannot use an operation (here, division), ask: "What information can I precompute that lets me answer the query differently?" The prefix/suffix pattern emerges when the answer at position `i` depends on elements on both sides.

Think of it as splitting the problem: "What do I know about the left side?" and "What do I know about the right side?" If you can answer both in O(1) with precomputation, you can solve the overall problem in O(n).

### Pattern Recognition

This is the **Prefix/Suffix Decomposition** pattern. It appears in:
- Trapping Rain Water (max height from left and right)
- Product of Array Except Self (this problem)
- Range sum/product queries with preprocessing
- Problems where the answer at position `i` depends on aggregates from both directions

## When NOT to Use

- **When division is allowed and there are no zeros**: Simply compute total product, then divide by each element. This is simpler and uses O(1) extra space (just the total).
- **When the operation is not associative**: Prefix/suffix decomposition relies on being able to combine partial results. It does not work for operations like median or mode.
- **When you need a single query, not all positions**: If you only need the product-except-self for one specific index, computing prefix and suffix arrays is overkill.
- **When the array is very large and memory is limited**: The O(1) space version exists (using the output array for prefix, then a running suffix), but if even the output array is too large, you have a fundamental problem.

## Approach

### Why Not Division?
Division approach fails with zeros and the problem explicitly forbids it.

### Optimal: Left and Right Products
For each position, the answer is:
`product of all elements to the left × product of all elements to the right`

**Two-pass approach:**
1. First pass: Build prefix products (left to right)
2. Second pass: Multiply by suffix products (right to left)

```
nums = [1, 2, 3, 4]

Pass 1 (prefix products):
  prefix = [1, 1, 2, 6]  # Each element is product of all to its left

Pass 2 (multiply by suffix):
  suffix from right: 1 → 4 → 12 → 24
  result = [24, 12, 8, 6]  # prefix × suffix at each position
```

## Implementation

```python
def product_except_self(nums: list[int]) -> list[int]:
    """
    Calculate product of array except self without division.

    Time: O(n) - two passes
    Space: O(1) - output array doesn't count as extra space
    """
    n = len(nums)
    result = [1] * n

    # Pass 1: Calculate prefix products
    # result[i] = product of all elements before index i
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    # Pass 2: Multiply by suffix products
    # Multiply result[i] by product of all elements after index i
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result


def product_except_self_with_arrays(nums: list[int]) -> list[int]:
    """
    More explicit version with separate prefix/suffix arrays.
    Easier to understand but uses O(n) extra space.
    """
    n = len(nums)

    # prefix[i] = product of nums[0] to nums[i-1]
    prefix = [1] * n
    for i in range(1, n):
        prefix[i] = prefix[i-1] * nums[i-1]

    # suffix[i] = product of nums[i+1] to nums[n-1]
    suffix = [1] * n
    for i in range(n - 2, -1, -1):
        suffix[i] = suffix[i+1] * nums[i+1]

    # result[i] = prefix[i] * suffix[i]
    return [prefix[i] * suffix[i] for i in range(n)]
```

## Complexity Analysis

| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n) | Two linear passes through array |
| Space | O(1) | Only the output array (doesn't count as extra) |

## Edge Cases

1. **Array with zero**: `[1, 2, 0, 4]` → `[0, 0, 8, 0]`
2. **Multiple zeros**: `[0, 0, 2]` → `[0, 0, 0]`
3. **All ones**: `[1, 1, 1, 1]` → `[1, 1, 1, 1]`
4. **Two elements**: `[3, 4]` → `[4, 3]`
5. **Negative numbers**: `[-1, 2, -3]` → `[-6, 3, -2]`
6. **Single element**: Problem guarantees length ≥ 2

## Common Mistakes

1. **Using division**: Not allowed and fails with zeros
2. **Forgetting to handle zeros**: Algorithm handles this naturally
3. **Off-by-one in prefix/suffix**: Be careful with loop bounds
4. **Not initializing prefix/suffix to 1**: Must start with identity element

## Visual Walkthrough

```
nums = [1, 2, 3, 4]
       ─────────────→ Prefix direction
              ←───────────── Suffix direction

Position 0: prefix=1 (nothing left), suffix=24 (2×3×4) → 24
Position 1: prefix=1 (just 1), suffix=12 (3×4) → 12
Position 2: prefix=2 (1×2), suffix=4 (just 4) → 8
Position 3: prefix=6 (1×2×3), suffix=1 (nothing right) → 6
```

## Variations

### With Division (If Allowed)
```python
def product_except_self_division(nums: list[int]) -> list[int]:
    """Only works if no zeros in array."""
    total = 1
    for num in nums:
        total *= num
    return [total // num for num in nums]
```

### Handle Division with Zeros
```python
def product_except_self_with_zeros(nums: list[int]) -> list[int]:
    """Handle zeros with division approach."""
    zero_count = nums.count(0)

    if zero_count > 1:
        return [0] * len(nums)

    if zero_count == 1:
        product_without_zero = 1
        for num in nums:
            if num != 0:
                product_without_zero *= num
        return [product_without_zero if num == 0 else 0 for num in nums]

    # No zeros
    total = 1
    for num in nums:
        total *= num
    return [total // num for num in nums]
```

## Related Problems

- **Trapping Rain Water** - Similar prefix/suffix approach
- **Maximum Product Subarray** - Track prefix products with sign handling
- **Range Sum Query** - Prefix sum concept
- **Subarray Product Less Than K** - Sliding window with products
