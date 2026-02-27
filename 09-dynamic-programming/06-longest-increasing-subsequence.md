# Longest Increasing Subsequence

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

Longest Increasing Subsequence (LIS) is a fundamental sequence Dynamic Programming problem. The goal is to find the longest strictly increasing subsequence in an array. A subsequence is derived from the array by deleting some or no elements without changing the order of the remaining elements.

## Problem Statement

Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

```
Input: [10, 9, 2, 5, 3, 7, 101, 18]
Output: 4
Explanation: [2, 3, 7, 101] or [2, 3, 7, 18] or [2, 5, 7, 101]
```

## Building Intuition

**Why does LIS have both O(n²) and O(n log n) solutions?**

1. **O(n²) DP Insight**: For each position `i`, we ask: *"What's the longest increasing subsequence ending exactly at `i`?"* To find this, we check all previous positions `j < i`. If `nums[j] < nums[i]`, we can extend the LIS ending at `j`. We take the maximum of these valid extensions (`dp[j] + 1`). This exhaustive pairwise search gives O(n²).
2. **Why We Track "Ending At"**: If we only tracked "LIS in the first `i` elements," we couldn't extend it—we wouldn't know the final value of that LIS, making it impossible to check if `nums[i]` can legally extend it.
3. **The Binary Search Insight (Patience Sorting)**: Instead of tracking lengths, we track *"the smallest ending value for a subsequence of each length."* If we have subsequences of lengths 1, 2, 3 with smallest endings `[2, 5, 8]`, and we encounter `6`, we can:
   - Extend the length-2 sequence (ending in 5) to create a length-3 sequence ending at `6`.
   - Replace the previous length-3 ending (`8 → 6`), which makes future extensions easier because `6` is a more favorable (smaller) tail than `8`.
4. **Why Binary Search Works**: The "smallest endings" array (`tails`) is strictly increasing by definition. Proof: If we have a length-2 sequence ending at X and a length-3 sequence ending at Y, then Y > X. The length-3 sequence must include a valid length-2 prefix. Since we track the *smallest* possible endings, Y must be strictly greater than X.
5. **Mental Model**: Imagine sorting playing cards into piles (Patience Sorting). Each pile represents sequences of a certain length. When a new card comes, place it on the leftmost pile whose top card is `≥` the new card. If no such pile exists, create a new pile to the right. The total number of piles is the LIS length.

---

## When NOT to Use LIS Pattern

1. **Contiguous Required**: If you need the longest increasing **SUBARRAY** (contiguous), use a simple single-pass O(n) approach. Keep a running count that resets to 1 when `nums[i] <= nums[i-1]`.
2. **Multi-Dimensional Non-Nesting**: For problems where sorting doesn't expose a linear structure. However, Box Stacking and Russian Dolls *are* variations of LIS after careful sorting.
3. **Non-Strict Increase**: If elements can be equal (non-decreasing sequence), you must adjust the binary search approach to use `bisect_right` instead of `bisect_left`.
4. **Need All Sequences**: If you must output *all* valid LIS combinations, backtracking/DFS is required, often guided by the DP table.

---

## Solution 1: O(n²) Dynamic Programming

### State and Transitions

Let `dp[i]` be the length of the Longest Increasing Subsequence ending exactly at index `i`.

**Base Case:**
`dp[i] = 1` for all `i`. Every single element is trivially an increasing subsequence of length 1.

**Transitions:**
For a given index `i`, check all previous indices `j` where `0 ≤ j < i`. We can append `nums[i]` to the subsequence ending at `j` if `nums[j] < nums[i]`.
`dp[i] = max(dp[i], dp[j] + 1)` for all `j < i` where `nums[j] < nums[i]`.

**Result:**
The length of the overall LIS is `max(dp)`. The global maximum can end at any index.

### Bottom-Up (Tabulation)

```python
def length_of_lis(nums: list[int]) -> int:
    """
    Bottom-Up Tabulation DP.

    Time Complexity: O(n²)
    Space Complexity: O(n)
    """
    if not nums:
        return 0

    n = len(nums)
    dp = [1] * n  # Base case: LIS ending at i is at least length 1

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)
```

### Visual Walkthrough (O(n²))

```text
nums = [10, 9, 2, 5, 3, 7, 101, 18]
dp initialized to [1, 1, 1, 1, 1, 1, 1, 1]

i=0 (10) : dp[0] = 1
i=1 (9)  : dp[1] = 1  (can't extend from 10)
i=2 (2)  : dp[2] = 1  (can't extend from 10 or 9)
i=3 (5)  : dp[3] = max(1, dp[2]+1) = 2  (extend from 2)
i=4 (3)  : dp[4] = max(1, dp[2]+1) = 2  (extend from 2)
i=5 (7)  : dp[5] = max(1, dp[2]+1, dp[3]+1, dp[4]+1) = 3  (extend from 5 or 3)
i=6 (101): dp[6] = 4  (extend from 7)
i=7 (18) : dp[7] = 4  (extend from 7)

dp = [1, 1, 1, 2, 2, 3, 4, 4]
Answer = max(dp) = 4
```

---

## Solution 2: O(n log n) Binary Search

We maintain a `tails` array where `tails[i]` stores the smallest ending element of an increasing subsequence of length `i + 1`.

### Implementation

```python
import bisect

def length_of_lis_optimized(nums: list[int]) -> int:
    """
    Patience Sorting / Binary Search approach.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    tails = []

    for num in nums:
        # Find the index where 'num' can replace an existing tail,
        # or extend the 'tails' array.
        pos = bisect.bisect_left(tails, num)

        if pos == len(tails):
            tails.append(num)  # num is larger than all tails; extend the longest subsequence
        else:
            tails[pos] = num   # num replaces a larger tail, keeping tails as small as possible

    # The length of the tails array is the length of the LIS
    return len(tails)
```

### Visual Walkthrough (O(n log n))

```text
nums = [10, 9, 2, 5, 3, 7, 101, 18]

num=10  : tails = [10]             (new LIS of len 1)
num=9   : tails = [9]              (9 replaces 10, better tail for len 1)
num=2   : tails = [2]              (2 replaces 9, better tail for len 1)
num=5   : tails = [2, 5]           (5 extends LIS to len 2)
num=3   : tails = [2, 3]           (3 replaces 5, better tail for len 2)
num=7   : tails = [2, 3, 7]        (7 extends LIS to len 3)
num=101 : tails = [2, 3, 7, 101]   (101 extends LIS to len 4)
num=18  : tails = [2, 3, 7, 18]    (18 replaces 101, better tail for len 4)

Result: len(tails) = 4
```

> **CRITICAL NOTE:** The `tails` array does **NOT** represent the actual longest increasing subsequence. It only stores the smallest possible ending values for subsequences of each length. For example, if `nums = [4, 5, 6, 3]`, `tails` becomes `[3, 5, 6]`. The valid LIS is `[4, 5, 6]`, not `[3, 5, 6]`.

---

## Reconstructing the LIS

If an interviewer asks for the actual sequence (not just the length), we must augment the binary search approach to track predecessor indices.

```python
import bisect

def lis_with_path(nums: list[int]) -> list[int]:
    """
    Returns the actual Longest Increasing Subsequence.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if not nums:
        return []

    tails = []
    tails_indices = [] # Stores indices corresponding to the values in 'tails'
    parent = [-1] * len(nums) # parent[i] stores the index of the predecessor of nums[i]

    for i, num in enumerate(nums):
        pos = bisect.bisect_left(tails, num)

        if pos == len(tails):
            tails.append(num)
            tails_indices.append(i)
        else:
            tails[pos] = num
            tails_indices[pos] = i

        # If pos > 0, this element extends a subsequence ending at tails_indices[pos - 1]
        if pos > 0:
            parent[i] = tails_indices[pos - 1]

    # Reconstruct the sequence starting from the last index in tails_indices
    curr_idx = tails_indices[-1]
    lis_path = []

    while curr_idx != -1:
        lis_path.append(nums[curr_idx])
        curr_idx = parent[curr_idx]

    return lis_path[::-1] # Reverse to get the correct order
```

---

## Variations & Related Patterns

### 1. Longest Non-Decreasing Subsequence

Allows equal elements. `[2, 2, 2]` has a non-decreasing length of 3, but strictly increasing length of 1.
**Fix:** Use `bisect_right` instead of `bisect_left`.

### 2. Number of Longest Increasing Subsequences

Instead of tracking just the length, we must also track the *count* of how many ways we can form an LIS up to index `i`.

```python
def find_number_of_lis(nums: list[int]) -> int:
    """
    Time Complexity: O(n²)
    Space Complexity: O(n)
    """
    if not nums:
        return 0

    n = len(nums)
    lengths = [1] * n  # lengths[i] = length of LIS ending at i
    counts = [1] * n   # counts[i] = number of LIS ending at i

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                if lengths[j] + 1 > lengths[i]:
                    # Found a strictly longer LIS, reset count
                    lengths[i] = lengths[j] + 1
                    counts[i] = counts[j]
                elif lengths[j] + 1 == lengths[i]:
                    # Found another way to build the same max length LIS
                    counts[i] += counts[j]

    max_len = max(lengths)
    # Sum the counts for all indices where the LIS length equals the global max_len
    return sum(count for length, count in zip(lengths, counts) if length == max_len)
```

### 3. Russian Doll Envelopes (2D LIS)

Given a list of envelopes `[width, height]`, find the maximum number of envelopes you can nest. Envelope A can fit in B only if `A_width < B_width` and `A_height < B_height`.

**Key Insight:** Sort by width ascending, then by height **descending**. Why?
If widths are equal, sorting height descending prevents us from nesting envelopes of the same width inside each other (since strict increase is required).
After sorting, run standard 1D LIS on the heights.

```python
import bisect

def max_envelopes(envelopes: list[list[int]]) -> int:
    """
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    # Sort width ascending, height descending
    envelopes.sort(key=lambda x: (x[0], -x[1]))

    # Standard O(n log n) LIS on heights
    tails = []
    for _, height in envelopes:
        pos = bisect.bisect_left(tails, height)
        if pos == len(tails):
            tails.append(height)
        else:
            tails[pos] = height

    return len(tails)
```

### 4. Increasing Triplet Subsequence

Find if there exist indices `i < j < k` such that `nums[i] < nums[j] < nums[k]`. This is just LIS bounded to length 3.

```python
def increasing_triplet(nums: list[int]) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    first = second = float('inf')

    for num in nums:
        if num <= first:
            first = num       # Smallest element seen so far
        elif num <= second:
            second = num      # Second smallest, completing a pair
        else:
            return True       # Found an element larger than both

    return False
```

---

## Common Pitfalls & Edge Cases

### Edge Cases
- **Empty Array:** Should return `0`.
- **Single Element:** Should return `1`.
- **Strictly Decreasing Array:** `[5, 4, 3, 2, 1]` should return `1`.
- **All Identical Elements:** `[2, 2, 2, 2]` should return `1` (for strictly increasing).

### Common Mistakes
1. **Initializing DP Table to 0:**
   ```python
   # WRONG
   dp = [0] * n

   # CORRECT - Every single element is an LIS of length 1
   dp = [1] * n
   ```
2. **Returning `tails` as the answer sequence:**
   The `tails` array in the binary search solution tracks smallest possible tails, NOT the actual sequence. If the sequence is required, you must track parent pointers as shown in the "Reconstructing the LIS" section.
3. **Using `bisect_right` for Strictly Increasing:**
   `bisect_right` allows duplicates in the tails array, which means it solves the "Longest Non-Decreasing" variation, not the strict LIS. Use `bisect_left`.

---

## Complexity Summary

| Approach | Time Complexity | Space Complexity | Best For |
| :--- | :--- | :--- | :--- |
| **DP (Tabulation)** | $O(n^2)$ | $O(n)$ | Reconstructing, counting variations |
| **Patience Sort (BS)** | $O(n \log n)$ | $O(n)$ | Finding length efficiently, FANG standard |
| **Segment Tree / BIT** | $O(n \log n)$ | $O(n)$ | Complex variants with element updates |

---

## Next Steps

Learn how to apply 1D concepts to grids and matrices in **[07-2d-dp-basics.md](./07-2d-dp-basics.md)**.
