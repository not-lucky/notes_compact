# DP on Strings

> **Prerequisites:** [08-longest-common-subsequence](./08-longest-common-subsequence.md), [09-edit-distance](./09-edit-distance.md)

## Overview

String Dynamic Programming encompasses problems involving subsequences, interleavings, decodings, and pattern matching across one or more strings. While they share similarities with general DP problems (like 0/1 Knapsack or Interval DP), string problems explicitly leverage the linear, character-by-character nature of text.

## Building Intuition

**Why do strings need specialized DP patterns?**

1. **Character-by-Character Decisions**: Most string DP processes text one character at a time. The core question is usually: "How does this current character contribute to our goal?" (e.g., match it, delete it, replace it, use it as a split point).
2. **Common State Definitions**:
   - `dp[i]` = Answer for prefix `s[0..i-1]`. (1D DP, Single String)
   - `dp[i][j]` = Answer for prefixes `s1[0..i-1]` and `s2[0..j-1]`. (2D DP, Two Strings)
   - `dp[i][j]` = Answer for the substring `s[i..j]`. (Interval DP, Palindromes/Splits)
3. **Use vs. Skip**: Many problems ask "use this character or skip it?" This is conceptually identical to the 0/1 Knapsack problem, but applied sequentially to characters.
4. **Counting vs. Optimization**: String problems frequently involve *counting* (distinct subsequences, valid decodings) rather than optimization (max/min). The recurrence relation usually sums possibilities instead of taking a `max()`.
5. **The Interleaving Insight**: When dealing with multiple strings forming a single result, DP tracks positions in multiple strings simultaneously. "Did this target character come from string A or string B?"

---

## 1. Sub-pattern: 1D Prefix DP (Decoding)

This sub-pattern involves a 1D state array where `dp[i]` depends on a small, constant number of previous states (e.g., `i-1` and `i-2`). This is mathematically equivalent to the Fibonacci sequence or Climbing Stairs, just applied to string validation.

### Decode Ways (LeetCode 91)

Count the number of ways to decode a string of digits where '1' -> 'A', '2' -> 'B', ..., '26' -> 'Z'.

**Intuition:**
At any character `s[i-1]`, we can either:
1. Decode it as a single character (if it's not '0').
2. Combine it with the previous character `s[i-2]` to form a valid double-digit number (10-26).

**Recurrence Relation:**
Let `dp[i]` be the number of ways to decode the prefix `s[0..i-1]`.

$$
dp[i] =
\begin{cases}
1 & \text{if } i = 0 \text{ (empty string)} \\
dp[i-1] \cdot [s[i-1] \neq '0'] + dp[i-2] \cdot [10 \le \text{int}(s[i-2\dots i-1]) \le 26] & \text{if } i > 0
\end{cases}
$$

```python
def num_decodings(s: str) -> int:
    """
    Time Complexity: O(n) where n is len(s)
    Space Complexity: O(1) using space optimization
    """
    if not s or s[0] == '0':
        return 0

    n = len(s)
    # At the start of loop i, prev2 holds dp[i-2], prev1 holds dp[i-1]
    prev2, prev1 = 1, 1

    for i in range(2, n + 1):
        curr_ways = 0

        # Case 1: Single digit decoding (1-9)
        if s[i - 1] != '0':
            curr_ways += prev1

        # Case 2: Two digit decoding (10-26)
        two_digit = int(s[i - 2:i])
        if 10 <= two_digit <= 26:
            curr_ways += prev2

        # Shift variables for the next iteration
        prev2, prev1 = prev1, curr_ways

    return prev1
```

---

## 2. Sub-pattern: 2D Sequence Alignment

This pattern involves comparing two strings character by character. The state is a 2D array `dp[i][j]` representing the solution for prefixes `s1[0..i-1]` and `s2[0..j-1]`.

### Distinct Subsequences (LeetCode 115)

Count the number of distinct subsequences of `s` that equal `t`.

**Intuition:**
If the current characters match (`s[i-1] == t[j-1]`), we have a choice:
1. **Use it**: Let `s[i-1]` match `t[j-1]`. The problem reduces to matching `s[0..i-2]` with `t[0..j-2]`.
2. **Skip it**: Don't use `s[i-1]`. Try to form `t[0..j-1]` using only `s[0..i-2]`.

If they don't match (`s[i-1] != t[j-1]`), we are forced to skip `s[i-1]`.

**Space-Optimized Implementation:**
Calculating `dp[i][j]` only requires values from the previous row (`dp[i-1][...]`). Thus, we can condense the matrix into a single 1D array of size `len(t) + 1`. To avoid overwriting values from `dp[i-1]` before we use them for `dp[i]`, we must iterate `j` backwards.

```python
def num_distinct(s: str, t: str) -> int:
    """
    Time Complexity: O(m * n)
    Space Complexity: O(n) optimized to 1D array
    """
    m, n = len(s), len(t)

    # dp[j] represents the number of ways to form t[0..j-1]
    dp = [0] * (n + 1)
    dp[0] = 1  # Base case: Empty t can be formed 1 way (by deleting all of s)

    for i in range(1, m + 1):
        # Iterate j backwards to prevent using updated dp[j-1] values in the same row i
        for j in range(min(i, n), 0, -1):
            if s[i - 1] == t[j - 1]:
                # dp[j] (new row i) = dp[j] (old row i-1: skip s[i-1]) + dp[j-1] (old row i-1: use s[i-1])
                dp[j] = dp[j] + dp[j - 1]
            # else: dp[j] remains unchanged (conceptually dp[i][j] = dp[i-1][j])

    return dp[n]
```

### Interleaving String (LeetCode 97)

Check if `s3` is formed by interleaving `s1` and `s2`.

**Intuition:**
We are constructing `s3` using characters from `s1` and `s2`. At index `i+j-1` of `s3`, the character must match either `s1[i-1]` or `s2[j-1]`.

Let `dp[i][j]` be a boolean: Can `s1[0..i-1]` and `s2[0..j-1]` interleave to form `s3[0..i+j-1]`?

```python
def is_interleave(s1: str, s2: str, s3: str) -> bool:
    """
    Time Complexity: O(m * n)
    Space Complexity: O(n) optimized to 1D array
    """
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False

    # dp[j] is True if s1[0..i-1] and s2[0..j-1] form s3[0..i+j-1]
    dp = [False] * (n + 1)
    dp[0] = True

    # Base case: Initialize the 0th row (i=0)
    # This represents trying to match s3 using ONLY characters from s2
    for j in range(1, n + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]

    for i in range(1, m + 1):
        # Base case for the current row (j=0): using ONLY characters from s1 to match s3
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]

        for j in range(1, n + 1):
            # Can we use s1[i-1]?
            # Yes, if s1[0..i-2] and s2[0..j-1] matched (dp[j]) AND s1[i-1] matches s3[i+j-1]
            match_s1 = dp[j] and s1[i - 1] == s3[i + j - 1]
            # Can we use s2[j-1]?
            # Yes, if s1[0..i-1] and s2[0..j-2] matched (dp[j-1]) AND s2[j-1] matches s3[i+j-1]
            match_s2 = dp[j - 1] and s2[j - 1] == s3[i + j - 1]

            dp[j] = match_s1 or match_s2

    return dp[n]
```

---

## 3. Sub-pattern: Interval DP on Strings (Splitting)

When a problem allows arbitrary splitting of the string into halves recursively, you generally need Interval DP / Divide and Conquer.

### Scramble String (LeetCode 87)

Check if `s2` is a scrambled version of `s1`. A string is scrambled by recursively partitioning it into two non-empty substrings and optionally swapping them.

**Intuition:**
This is natively suited for **Top-Down Memoization** due to the $O(n^4)$ time complexity. We split the string at every possible index `i` and check if the unswapped halves match or if the swapped halves match.

While passing indices is more standard for DP to avoid $O(n)$ string slicing overhead, passing slices of strings in Python combined with `@lru_cache` is incredibly clean and often fast enough in practice due to underlying string hashing optimizations. We also add an $O(n)$ pruning step using character counts to skip large branches.

```python
from functools import lru_cache
from collections import Counter

class Solution:
    def isScramble(self, s1: str, s2: str) -> bool:
        """
        Time Complexity: O(n^4) bounds (O(n^3) subproblems * O(n) for slicing/Counter)
        Space Complexity: O(n^3) for the memoization cache
        """
        if len(s1) != len(s2):
            return False

        @lru_cache(maxsize=None)
        def dfs(s1: str, s2: str) -> bool:
            # Base cases
            if s1 == s2:
                return True

            # Pruning: Frequency check. If anagrams don't match, scrambles can't match.
            # Counter is O(n), much faster than sorted() which is O(n log n)
            if Counter(s1) != Counter(s2):
                return False

            n = len(s1)
            # Try all possible split points
            for i in range(1, n):
                # Option 1: Try Without Swap
                # Check if left matches left, and right matches right
                if dfs(s1[:i], s2[:i]) and dfs(s1[i:], s2[i:]):
                    return True

                # Option 2: Try With Swap
                # Check if left of s1 matches right of s2, and right of s1 matches left of s2
                if dfs(s1[:i], s2[-i:]) and dfs(s1[i:], s2[:-i]):
                    return True

            return False

        return dfs(s1, s2)
```

---

## 4. Sub-pattern: State Machine DP (Parentheses)

These problems maintain the continuous length of a valid prefix/suffix dynamically.

### Longest Valid Parentheses (LeetCode 32)

Given a string containing just `(` and `)`, find the length of the longest valid (well-formed) parentheses substring.

**Intuition:**
Let `dp[i]` be the length of the longest valid substring strictly **ending at** index `i`.
- If `s[i] == '('`, it cannot conclude a valid pair. `dp[i] = 0`.
- If `s[i] == ')'`, we look at `s[i-1]`.
  - If `s[i-1] == '('`, they form a simple pair `()`. The length is 2 plus whatever valid sequence immediately preceded the `(` (i.e., `dp[i-2]`).
  - If `s[i-1] == ')'`, it means we have `...))`. We must check if the string immediately preceding the valid substring that ends at `i-1` was a matching `(`.

```python
def longest_valid_parentheses(s: str) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    n = len(s)
    if n == 0:
        return 0

    dp = [0] * n
    max_len = 0

    for i in range(1, n):
        if s[i] == ')':
            # Case 1: Simple pairing `...()`
            if s[i - 1] == '(':
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2

            # Case 2: Nested pairing `...))`.
            # Check if there's a matching '(' that corresponds to this closing ')'
            elif s[i - 1] == ')':
                # Skip back over the previous valid sequence to find the potential matching '('
                prev_open_idx = i - dp[i - 1] - 1

                if prev_open_idx >= 0 and s[prev_open_idx] == '(':
                    # Add 2 for the outer `(...)` pair we just found
                    dp[i] = dp[i - 1] + 2

                    # We must also attach any adjacent valid sequence immediately before our matching '('
                    if prev_open_idx - 1 >= 0:
                        dp[i] += dp[prev_open_idx - 1]

            max_len = max(max_len, dp[i])

    return max_len
```

---

## Non-DP String Problems (For Contrast)

Some string matching problems look like DP but are better solved with hashing, tries, or greedy two-pointer approaches. Be highly skeptical if a "DP" solution exceeds $O(n^2)$ time on a string where $n > 5,000$.

### Palindrome Pairs (Tries / Hash Maps)
*Given a list of words, find pairs `(i, j)` where `words[i] + words[j]` is a palindrome.*

**Why NOT DP?** Comparing all pairs is $O(n^2 \cdot k)$. Instead, use a Hash Map. For each word, split it into prefix/suffix. If the prefix is a palindrome, look up the reverse of the suffix in the hash map. Time: $O(n \cdot k^2)$.

### Shortest Way to Form String (Greedy / Two Pointers)
*Minimum number of subsequences of `source` needed to form `target`.*

**Why NOT DP?** While it looks like Sequence Alignment, a greedy approach (matching characters in `target` sequentially against `source` until exhaustion, then restarting `source`) guarantees the optimal answer in $O(m \cdot n)$ with space $O(1)$. DP adds unnecessary memory overhead.

---

## Chapter Complete!

You've now covered all major DP patterns for FANG+ interviews:

| Category | Key Topics |
| :--- | :--- |
| **1D DP** | Fibonacci, House Robber, Climbing Stairs |
| **2D DP** | Grid paths, LCS, Edit Distance |
| **Knapsack** | 0/1, Unbounded, Subset Sum, Coin Change |
| **Interval DP** | Matrix Chain, Palindromes, Burst Balloons |
| **State Machine** | Stock Trading Problems |
| **String DP** | Word Break, Regex, Distinct Subsequences, Interleaving |

These patterns cover 90%+ of Dynamic Programming problems in technical interviews. Master the state definitions, and the recurrences follow naturally.
