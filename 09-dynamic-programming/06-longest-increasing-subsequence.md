# Longest Increasing Subsequence

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

LIS is a fundamental sequence DP problem that finds the longest strictly increasing subsequence (not contiguous) in an array.

## Building Intuition

**Why does LIS have both O(n²) and O(n log n) solutions?**

1. **O(n²) DP Insight**: For each position i, we ask: "What's the longest increasing subsequence ending at i?" To find this, we check all previous positions j < i where nums[j] < nums[i], and take the maximum dp[j] + 1. This exhaustive search over all pairs gives O(n²).

2. **Why We Track "Ending At"**: If we only tracked "LIS in first i elements," we couldn't extend—we wouldn't know what value the LIS ends with, so we couldn't determine if nums[i] can extend it.

3. **The Binary Search Insight**: Instead of tracking lengths, we track "the smallest ending value for a subsequence of each length." If we have subsequences of lengths 1, 2, 3 with smallest endings [2, 5, 8], and see 6, we can:
   - Extend length-2 (ending 5) to create length-3 ending at 6
   - Replace the length-3 ending (8 → 6), making future extensions easier

4. **Why Binary Search Works**: The "smallest endings" array is always sorted! Proof: if we have length-2 ending at X and length-3 ending at Y, then Y > X (the length-3 sequence includes a valid length-2 prefix, and we track the smallest, so Y must be at least as large as the smallest length-2 ending).

5. **Mental Model**: Imagine sorting playing cards into piles. Each pile represents sequences of a certain length. When a new card comes, place it on the leftmost pile whose top card is ≥ new card (binary search). The number of piles is the LIS length.

## Interview Context

LIS is a FANG+ essential because:

1. **Classic DP problem**: Appears in countless variations
2. **O(n log n) optimization**: Tests algorithm knowledge
3. **Foundation for harder problems**: Russian Dolls, Envelopes
4. **Multiple approaches**: DP, binary search, patience sorting

---

## When NOT to Use LIS Pattern

1. **Contiguous Required**: If you need longest increasing SUBARRAY (contiguous), not subsequence, use a simpler single-pass O(n) approach.

2. **Multiple Dimensions**: For problems like Russian Dolls (width AND height must increase), sort by one dimension first, then apply LIS on the other.

3. **Non-Strict Increase**: For non-decreasing sequences (≤ instead of <), use `bisect_right` instead of `bisect_left` in the O(n log n) solution.

4. **Need Actual Sequence**: The O(n log n) solution gives LENGTH only. Getting the actual subsequence requires extra bookkeeping (parent pointers).

5. **Counting All LIS**: If you need to count how many LIS exist (not just find one), you need additional DP arrays for counting.

**Recognize LIS Pattern When:**
- Find longest subsequence (not contiguous) with ordering property
- Elements must be strictly/non-strictly increasing/decreasing
- Can reduce multi-dimensional problems to LIS after sorting

---

## Problem Statement

Find the length of the longest strictly increasing subsequence.

```
Input: [10, 9, 2, 5, 3, 7, 101, 18]
Output: 4
Explanation: [2, 3, 7, 101] or [2, 3, 7, 18] or [2, 5, 7, 101]
```

---

## Solution 1: O(n²) DP

```python
def length_of_lis(nums: list[int]) -> int:
    """
    Classic DP approach.

    State: dp[i] = length of LIS ending at index i
    Recurrence: dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]

    Time: O(n²)
    Space: O(n)
    """
    if not nums:
        return 0

    n = len(nums)
    dp = [1] * n  # Every element is LIS of length 1

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)
```

### Visual Walkthrough

```
nums = [10, 9, 2, 5, 3, 7, 101, 18]

i=0: dp[0] = 1  (just 10)
i=1: dp[1] = 1  (just 9, can't extend from 10)
i=2: dp[2] = 1  (just 2)
i=3: dp[3] = 2  (2 → 5, extend from index 2)
i=4: dp[4] = 2  (2 → 3)
i=5: dp[5] = 3  (2 → 3 → 7 or 2 → 5 → 7)
i=6: dp[6] = 4  (2 → 3 → 7 → 101)
i=7: dp[7] = 4  (2 → 3 → 7 → 18)

dp = [1, 1, 1, 2, 2, 3, 4, 4]
Answer: 4
```

---

## Solution 2: O(n log n) with Binary Search

Use a "tails" array where `tails[i]` = smallest ending element of LIS of length i+1.

```python
import bisect

def length_of_lis_optimized(nums: list[int]) -> int:
    """
    Binary search approach.

    Maintain tails array where tails[i] = smallest tail of LIS of length i+1.

    Time: O(n log n)
    Space: O(n)
    """
    tails = []

    for num in nums:
        # Find position where num should go
        pos = bisect.bisect_left(tails, num)

        if pos == len(tails):
            tails.append(num)  # Extend LIS
        else:
            tails[pos] = num  # Replace with smaller value

    return len(tails)
```

### How It Works

```
nums = [10, 9, 2, 5, 3, 7, 101, 18]

num=10: tails = [10]         (new LIS of length 1)
num=9:  tails = [9]          (replace 10 with smaller 9)
num=2:  tails = [2]          (replace 9 with smaller 2)
num=5:  tails = [2, 5]       (extend LIS to length 2)
num=3:  tails = [2, 3]       (replace 5 with smaller 3)
num=7:  tails = [2, 3, 7]    (extend LIS to length 3)
num=101: tails = [2, 3, 7, 101] (extend to length 4)
num=18: tails = [2, 3, 7, 18]   (replace 101 with 18)

len(tails) = 4
```

**Note**: `tails` is NOT the actual LIS, just tracks smallest possible endings!

---

## Reconstructing the LIS

```python
def lis_with_path(nums: list[int]) -> list[int]:
    """
    Return the actual LIS, not just length.

    Time: O(n log n)
    Space: O(n)
    """
    if not nums:
        return []

    n = len(nums)
    tails = []
    indices = []  # indices[i] = index in nums that gave tails[i]
    parent = [-1] * n

    for i, num in enumerate(nums):
        pos = bisect.bisect_left(tails, num)

        if pos == len(tails):
            tails.append(num)
            indices.append(i)
        else:
            tails[pos] = num
            indices[pos] = i

        # Track parent for reconstruction
        if pos > 0:
            parent[i] = indices[pos - 1]

    # Reconstruct LIS
    lis = []
    idx = indices[-1]
    while idx != -1:
        lis.append(nums[idx])
        idx = parent[idx]

    return lis[::-1]
```

---

## Variation: Number of LIS

```python
def find_number_of_lis(nums: list[int]) -> int:
    """
    Count how many LIS of maximum length exist.

    Time: O(n²)
    Space: O(n)
    """
    if not nums:
        return 0

    n = len(nums)
    length = [1] * n  # LIS length ending at i
    count = [1] * n   # Count of LIS ending at i

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]

    max_len = max(length)
    return sum(c for l, c in zip(length, count) if l == max_len)
```

---

## Variation: Longest Non-Decreasing Subsequence

```python
def longest_non_decreasing(nums: list[int]) -> int:
    """
    Allow equal elements (non-decreasing, not strictly increasing).

    Use bisect_right instead of bisect_left.
    """
    tails = []

    for num in nums:
        pos = bisect.bisect_right(tails, num)  # Right for non-decreasing

        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num

    return len(tails)
```

---

## Related: Russian Doll Envelopes

```python
def max_envelopes(envelopes: list[list[int]]) -> int:
    """
    Fit envelopes inside each other (both dimensions strictly larger).

    Key insight: Sort by width ascending, then height descending.
    Then LIS on heights.

    Time: O(n log n)
    Space: O(n)
    """
    # Sort: width ascending, height descending
    envelopes.sort(key=lambda x: (x[0], -x[1]))

    # LIS on heights
    heights = [e[1] for e in envelopes]
    tails = []

    for h in heights:
        pos = bisect.bisect_left(tails, h)
        if pos == len(tails):
            tails.append(h)
        else:
            tails[pos] = h

    return len(tails)
```

### Why Sort Height Descending?

```
Envelopes: [[5,4], [6,4], [6,7], [2,3]]
After sort: [[2,3], [5,4], [6,7], [6,4]]
                                  ^^ Height descending for same width

Heights: [3, 4, 7, 4]
LIS: [3, 4, 7] = length 3

Without descending sort:
[[2,3], [5,4], [6,4], [6,7]]
Heights: [3, 4, 4, 7]
LIS: [3, 4, 4, 7] = length 4 (WRONG! Can't nest [6,4] in [6,7])
```

---

## Related: Increasing Triplet Subsequence

```python
def increasing_triplet(nums: list[int]) -> bool:
    """
    Check if increasing triplet exists.

    Time: O(n)
    Space: O(1)
    """
    first = second = float('inf')

    for num in nums:
        if num <= first:
            first = num
        elif num <= second:
            second = num
        else:
            return True  # Found third element

    return False
```

---

## Edge Cases

```python
# 1. Empty array
nums = []
# Return 0

# 2. Single element
nums = [5]
# Return 1

# 3. Decreasing sequence
nums = [5, 4, 3, 2, 1]
# Return 1

# 4. Already sorted
nums = [1, 2, 3, 4, 5]
# Return 5

# 5. All same elements
nums = [5, 5, 5, 5]
# Return 1 (strictly increasing)
```

---

## Common Mistakes

```python
# WRONG: Not initializing dp to 1
dp = [0] * n
for i in range(n):
    for j in range(i):
        if nums[j] < nums[i]:
            dp[i] = max(dp[i], dp[j] + 1)
# Elements with no smaller predecessor get dp[i] = 0!

# CORRECT:
dp = [1] * n  # Every element is LIS of length 1


# WRONG: Using bisect_right for strictly increasing
pos = bisect.bisect_right(tails, num)  # Wrong for strictly increasing

# CORRECT:
pos = bisect.bisect_left(tails, num)  # Left for strictly increasing


# WRONG: Returning tails as the LIS
return tails  # tails is NOT the actual LIS!
```

---

## Complexity Comparison

| Approach | Time | Space |
|----------|------|-------|
| O(n²) DP | O(n²) | O(n) |
| Binary Search | O(n log n) | O(n) |
| Patience Sorting | O(n log n) | O(n) |

---

## Interview Tips

1. **Start with O(n²)**: Simpler, then optimize
2. **Explain binary search insight**: Why tails array works
3. **Know variants**: Non-decreasing, count, reconstruction
4. **Handle edge cases**: Empty, single element
5. **Mention applications**: Envelopes, scheduling

---

## Practice Problems

| # | Problem | Difficulty | Variant |
|---|---------|------------|---------|
| 1 | LIS | Medium | Classic |
| 2 | Number of LIS | Medium | Count |
| 3 | Increasing Triplet | Medium | k=3 special case |
| 4 | Russian Doll Envelopes | Hard | 2D LIS |
| 5 | Longest Increasing Path | Hard | Grid version |

---

## Key Takeaways

1. **O(n²) baseline**: DP with pairwise comparison
2. **O(n log n) optimal**: Binary search on tails array
3. **tails array trick**: Track smallest ending element for each length
4. **bisect_left vs right**: Left for strictly increasing
5. **2D problems**: Sort one dimension, LIS on other

---

## Next: [07-2d-dp-basics.md](./07-2d-dp-basics.md)

Learn the fundamental 2D DP patterns with grid problems.
