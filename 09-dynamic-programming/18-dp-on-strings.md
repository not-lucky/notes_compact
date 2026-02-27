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

## Interview Context

String DP problems are extremely common in FANG+ interviews because they strictly test your ability to model state transitions.

1. **Complex state transitions**: You must rigorously define how to handle matching, mismatching, and boundary cases.
2. **Space optimization**: Almost all 2D string DP problems (comparing two strings) can be optimized to $O(n)$ space since `dp[i][j]` typically only relies on the previous row (`i-1`) or the current row (`i`).
3. **Boundary conditions**: Correctly initializing empty strings (`dp[0][0]`, `dp[0][j]`, `dp[i][0]`) is where most candidates fail.

---

## When NOT to Use String DP

String DP is powerful, but applying it incorrectly will lead to suboptimal solutions or Time Limit Exceeded (TLE) errors.

1. **Simple String Matching**: For exact substring matching (e.g., finding the first occurrence of "needle" in "haystack"), use KMP, Rabin-Karp, or simply `str.find()`. DP is overkill.
2. **Complex Substring / Suffix Queries**: Problems like "Longest Repeated Substring" are better solved with Suffix Arrays or Suffix Trees in $O(n)$ time. DP takes $O(n^2)$, which is too slow for large inputs.
3. **Very Long Strings ($n > 10^4$)**: Most 2D String DPs are $O(n^2)$ or $O(nm)$. If $n = 10^5$, an $O(n^2)$ DP will TLE. Look for greedy approaches, binary search, or linear time algorithms.
4. **Streaming/Online Processing**: If characters arrive one by one and you need immediate answers, batch DP doesn't apply.

---

## Sub-pattern: 1D Prefix DP (Decoding and Formatting)

This sub-pattern involves a 1D state array where `dp[i]` depends on a small, constant number of previous states (e.g., `i-1` and `i-2`). This is mathematically equivalent to the Fibonacci sequence or Climbing Stairs, just applied to string validation.

### Decode Ways

Count the number of ways to decode a string of digits where '1' -> 'A', '2' -> 'B', ..., '26' -> 'Z'.

#### Intuition
At any character `s[i-1]`, we can either:
1. Decode it as a single character (if it's not '0').
2. Combine it with the previous character `s[i-2]` to form a valid double-digit number (10-26).

#### Recurrence Relation
Let `dp[i]` be the number of ways to decode the prefix `s[0..i-1]`.

$$
dp[i] =
\begin{cases}
1 & \text{if } i = 0 \text{ (empty string)} \\
dp[i-1] \cdot [s[i-1] \neq '0'] + dp[i-2] \cdot [10 \le \text{int}(s[i-2..i-1]) \le 26] & \text{if } i > 0
\end{cases}
$$
*(Using Iverson bracket notation `[condition]` which equals 1 if true, 0 if false)*

```python
def num_decodings(s: str) -> int:
    """
    Count ways to decode '1'-'26' to 'A'-'Z'.

    Time Complexity: O(n) where n is len(s)
    Space Complexity: O(1) after space optimization
    """
    if not s or s[0] == '0':
        return 0

    n = len(s)
    # prev2 = dp[i-2], prev1 = dp[i-1]
    prev2, prev1 = 1, 1

    for i in range(2, n + 1):
        curr = 0

        # Case 1: Single digit decoding (1-9)
        if s[i - 1] != '0':
            curr += prev1

        # Case 2: Two digit decoding (10-26)
        two_digit = int(s[i - 2:i])
        if 10 <= two_digit <= 26:
            curr += prev2

        # Shift variables for the next iteration
        prev2, prev1 = prev1, curr

    return prev1
```

---

## Sub-pattern: 2D Sequence Alignment (Two Strings)

This pattern involves comparing two strings character by character. The state is a 2D array `dp[i][j]` representing the solution for prefixes `s1[0..i-1]` and `s2[0..j-1]`.

**Pro-Tip**: Almost all 2D sequence alignment DP problems can be optimized to $O(\min(n, m))$ space.

### Distinct Subsequences

Count the number of distinct subsequences of `s` that equal `t`.

#### Intuition
If the current characters match (`s[i-1] == t[j-1]`), we have a choice:
1. **Use it**: Let `s[i-1]` match `t[j-1]`. The problem reduces to matching `s[0..i-2]` with `t[0..j-2]`.
2. **Skip it**: Don't use `s[i-1]`. Try to form `t[0..j-1]` using only `s[0..i-2]`.

If they don't match (`s[i-1] != t[j-1]`), we are forced to skip `s[i-1]`.

#### Recurrence Relation
Let `dp[i][j]` be the number of distinct subsequences of `s[0..i-1]` that equal `t[0..j-1]`.

$$
dp[i][j] =
\begin{cases}
1 & \text{if } j = 0 \text{ (empty } t \text{ matched by deleting all chars)} \\
0 & \text{if } i = 0 \text{ and } j > 0 \text{ (empty } s \text{ cannot match non-empty } t \text{)} \\
dp[i-1][j] + (dp[i-1][j-1] \text{ if } s[i-1] == t[j-1] \text{ else } 0) & \text{otherwise}
\end{cases}
$$

#### Space-Optimized Implementation
Notice that calculating `dp[i][j]` only requires values from the previous row (`dp[i-1][...]`). Thus, we can condense the matrix into a single 1D array of size `len(t) + 1`.

To avoid overwriting values from `dp[i-1]` before we use them for `dp[i]`, we must iterate `j` backwards.

```python
def num_distinct(s: str, t: str) -> int:
    """
    Count distinct subsequences of s that equal t.

    Time Complexity: O(m * n)
    Space Complexity: O(n) optimized to 1D array
    """
    m, n = len(s), len(t)

    # dp[j] represents the number of ways to form t[0..j-1]
    dp = [0] * (n + 1)
    dp[0] = 1  # Base case: Empty t can be formed 1 way

    for i in range(1, m + 1):
        # Iterate j backwards to prevent using updated dp[j-1] values in the same row i
        # Micro-optimization: A string of length i can't form a subsequence longer than i
        for j in range(min(i, n), 0, -1):
            if s[i - 1] == t[j - 1]:
                # ways = don't use s[i-1] + use s[i-1]
                dp[j] = dp[j] + dp[j - 1]
            # else: dp[j] remains unchanged (conceptually dp[i][j] = dp[i-1][j])

    return dp[n]
```

### Interleaving String

Check if `s3` is formed by interleaving `s1` and `s2`.

#### Intuition
We are constructing `s3` using characters from `s1` and `s2`. At index `i+j-1` of `s3`, the character must match either `s1[i-1]` or `s2[j-1]`.

Let `dp[i][j]` be a boolean: Can `s1[0..i-1]` and `s2[0..j-1]` interleave to form `s3[0..i+j-1]`?

$$
dp[i][j] =
\begin{cases}
True & \text{if } i=0, j=0 \\
(dp[i-1][j] \land s1[i-1] == s3[i+j-1]) \lor (dp[i][j-1] \land s2[j-1] == s3[i+j-1]) & \text{otherwise}
\end{cases}
$$

```python
def is_interleave(s1: str, s2: str, s3: str) -> bool:
    """
    Check if s3 is an interleaving of s1 and s2.

    Time Complexity: O(m * n)
    Space Complexity: O(n) optimized to 1D array
    """
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False

    # dp[j] is True if s1[0..i-1] and s2[0..j-1] form s3[0..i+j-1]
    dp = [False] * (n + 1)
    dp[0] = True

    # Base case: Initialize the 0th row (using ONLY s2 to match s3)
    for j in range(1, n + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]

    for i in range(1, m + 1):
        # Base case for the current row: using ONLY s1 to match s3
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]

        for j in range(1, n + 1):
            # Can we use s1[i-1]?
            match_s1 = dp[j] and s1[i - 1] == s3[i + j - 1]
            # Can we use s2[j-1]?
            match_s2 = dp[j - 1] and s2[j - 1] == s3[i + j - 1]

            dp[j] = match_s1 or match_s2

    return dp[n]
```

---

## Sub-pattern: Interval DP on Strings (Palindromes & Splitting)

When a problem asks about Palindromic properties or allows arbitrary splitting of the string, you generally need Interval DP. The state is `dp[i][j]`, representing the substring `s[i..j]`.

**CRITICAL RULE**: Because `dp[i][j]` (a longer substring) often depends on `dp[i+1][j-1]` (a shorter, nested substring), **you must iterate by substring length**, not just `i` and `j` sequentially.

### Longest Palindromic Subsequence

Before jumping into complex permutations, let's understand the core interval pattern using the Longest Palindromic Subsequence.

#### Intuition
For the interval `s[i..j]`:
- If `s[i] == s[j]`, these two characters form part of our palindrome. We add 2 to the longest palindrome of the inner substring `s[i+1..j-1]`.
- If `s[i] != s[j]`, we can't use both. The best we can do is the maximum of ignoring the left char (`s[i+1..j]`) or ignoring the right char (`s[i..j-1]`).

```python
def longest_palindrome_subseq(s: str) -> int:
    """
    Find the length of the longest palindromic subsequence in s.

    Time Complexity: O(n^2)
    Space Complexity: O(n^2) (Can be optimized to O(n))
    """
    n = len(s)
    dp = [[0] * n for _ in range(n)]

    # Base case: Strings of length 1 are palindromes of length 1
    for i in range(n):
        dp[i][i] = 1

    # DP transition: Iterate over interval lengths
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                # Match: 2 + best inner sequence
                # (If length=2, dp[i+1][j-1] evaluates to dp[i+1][i], which is 0, correctly giving 2)
                dp[i][j] = 2 + (dp[i + 1][j - 1] if length > 2 else 0)
            else:
                # Mismatch: Max of ignoring left vs ignoring right
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]
```

### Count Different Palindromic Subsequences

Find the number of **distinct** non-empty palindromic subsequences in `s`.

#### Intuition
This builds directly on the previous interval DP, but uniqueness makes it brutally difficult. When `s[i] == s[j]`, we must ensure we don't overcount inner palindromes that are already constructed by other identical characters inside the interval.

```python
def count_palindromic_subseq(s: str) -> int:
    """
    Count distinct palindromic subsequences modulo 10^9 + 7.

    Time Complexity: O(n^2)
    Space Complexity: O(n^2)
    """
    MOD = 10**9 + 7
    n = len(s)
    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                left, right = i + 1, j - 1

                # Locate the first occurrences of s[i] inside the interval
                while left <= right and s[left] != s[i]:
                    left += 1
                while left <= right and s[right] != s[j]:
                    right -= 1

                if left > right:
                    # Case 1: s[i] is NOT inside s[i+1..j-1]
                    # Example: "aba" -> inner "b" contributes forms, plus "a", "aa", "aba"
                    dp[i][j] = dp[i + 1][j - 1] * 2 + 2
                elif left == right:
                    # Case 2: s[i] exists exactly ONCE inside s[i+1..j-1]
                    # Example: "aaa" -> inner "a" already contributed, don't double count "a"
                    dp[i][j] = dp[i + 1][j - 1] * 2 + 1
                else:
                    # Case 3: s[i] exists MULTIPLE times inside.
                    # We must subtract the inner subsequences bounded by left/right to prevent duplicates
                    dp[i][j] = dp[i + 1][j - 1] * 2 - dp[left + 1][right - 1]
            else:
                # Inclusion-exclusion principle when bounds don't match
                # Total = (without left) + (without right) - (without both, which was counted twice)
                dp[i][j] = dp[i + 1][j] + dp[i][j - 1] - dp[i + 1][j - 1]

            # In Python, `%` handles negative numbers gracefully.
            dp[i][j] %= MOD

    return dp[0][n - 1]
```

### Scramble String

Check if `s2` is a scrambled version of `s1`. A string is scrambled by recursively partitioning it into two non-empty substrings and optionally swapping them.

#### Intuition
This is Interval DP / Divide and Conquer natively suited for **Top-Down Memoization** due to the $O(n^4)$ time complexity. We split the string at every possible index `k` and check if the unswapped halves match or if the swapped halves match.

Rather than passing indices around which is verbose, slicing `s1` and `s2` directly in Python is cleaner and highly readable, leveraging `@lru_cache`.

```python
from functools import lru_cache

def is_scramble(s1: str, s2: str) -> bool:
    """
    Check if s2 is a scramble of s1.

    Time Complexity: O(n^4) bounds (O(n^3) subproblems * O(n) per subproblem for slicing/iteration)
    Space Complexity: O(n^3) for the memoization cache
    """
    # Quick short-circuit
    if len(s1) != len(s2):
        return False

    @lru_cache(maxsize=None)
    def dp(s1: str, s2: str) -> bool:
        # Base cases
        if s1 == s2:
            return True

        # Pruning: Frequency check. If anagrams don't match, scrambles can't match.
        if sorted(s1) != sorted(s2):
            return False

        n = len(s1)
        # Try all possible split points
        for i in range(1, n):
            # Try Without Swap:
            # Check if left matches left, and right matches right
            if dp(s1[:i], s2[:i]) and dp(s1[i:], s2[i:]):
                return True

            # Try With Swap:
            # Check if left of s1 matches right of s2, and right of s1 matches left of s2
            if dp(s1[:i], s2[-i:]) and dp(s1[i:], s2[:-i]):
                return True

        return False

    return dp(s1, s2)
```

---

## Sub-pattern: State Machine DP on Strings (Parentheses)

These problems often involve a state machine or maintaining the continuous length of a valid prefix/suffix dynamically.

### Longest Valid Parentheses

Given a string containing just `(` and `)`, find the length of the longest valid (well-formed) parentheses substring.

#### Intuition
Let `dp[i]` be the length of the longest valid substring strictly **ending at** index `i`.
- If `s[i] == '('`, it cannot conclude a valid pair. `dp[i] = 0`.
- If `s[i] == ')'`, we look at `s[i-1]`.
  - If `s[i-1] == '('`, they form a simple pair `()`. The length is 2 plus whatever valid sequence immediately preceded the `(` (i.e., `dp[i-2]`).
  - If `s[i-1] == ')'`, it means we have `...))`. We must check if the string immediately preceding the valid substring that ends at `i-1` was a matching `(`.

```python
def longest_valid_parentheses(s: str) -> int:
    """
    Find length of longest continuous valid parentheses substring.

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

            # Case 2: Nested pairing `...))`. Check if there's a matching '('
            elif i - dp[i - 1] - 1 >= 0 and s[i - dp[i - 1] - 1] == '(':
                # Add 2 for the outer `(...)` pair
                dp[i] = dp[i - 1] + 2

                # We must also attach any adjacent valid sequence immediately before our matching '('
                if i - dp[i - 1] - 2 >= 0:
                    dp[i] += dp[i - dp[i - 1] - 2]

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

**Why NOT DP?** While it looks like Sequence Alignment, a greedy approach (matching characters in `target` sequentially against `source` until exhaustion, then restarting `source`) guarantees the optimal answer in $O(m \cdot n)$ space $O(1)$. DP adds unnecessary memory overhead.

---

## Common Patterns Summary

| Problem | Sub-pattern | Key Insight | Time | Space |
| :--- | :--- | :--- | :--- | :--- |
| **Decode Ways** | 1D Prefix | Combine $i-1$ (single digit) and $i-2$ (double digit). | $O(n)$ | $O(1)$ opt |
| **Distinct Subseqs** | 2D Alignment | Match current char + don't match char. | $O(mn)$ | $O(n)$ opt |
| **Interleaving String** | 2D Alignment | State tracks usage of `s1` vs `s2`. | $O(mn)$ | $O(n)$ opt |
| **Longest Palindrome Subseq**| Interval DP | Iterate by length! $i$ and $j$ boundaries. | $O(n^2)$ | $O(n^2)$ |
| **Scramble String** | Div & Conquer | Top-down memoization checking all split points $k$. | $O(n^4)$ | $O(n^3)$ |
| **Valid Parentheses** | State Machine | `dp[i]` represents valid length strictly *ending* at $i$.| $O(n)$ | $O(n)$ |

---

## Interview Tips

1. **Draw the DP table**: For 2D sequence alignment, draw a matrix. If it's interval DP, draw a matrix where you only fill the upper-right triangle!
2. **Handle empty strings rigorously**: `dp[0]` often represents an empty string. `dp[0] = 1` for Counting Distinct Subsequences is a classic "aha" moment.
3. **Space optimize**: 2D Sequence Alignment problems should almost always be space-optimized to $O(n)$ in production code. Mention it to the interviewer.
4. **State Definition is King**: State exactly what `dp` means. "Is `dp[i]` the answer ending exactly at $i$, or the max answer within the prefix up to $i$?"

---

## Practice Problems

| # | Problem | Difficulty | Pattern |
| :--- | :--- | :--- | :--- |
| 1 | [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) | Hard | 2D Sequence Alignment |
| 2 | [Interleaving String](https://leetcode.com/problems/interleaving-string/) | Medium | 2D Sequence Alignment |
| 3 | [Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) | Medium | Interval DP |
| 4 | [Scramble String](https://leetcode.com/problems/scramble-string/) | Hard | Divide & Conquer |
| 5 | [Decode Ways](https://leetcode.com/problems/decode-ways/) | Medium | 1D Prefix DP |
| 6 | [Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses/) | Hard | 1D State Machine |

---

## Chapter Complete!

You've now covered all major DP patterns for FANG+ interviews:

| Category | Key Topics |
| :--- | :--- |
| **1D DP** | Fibonacci, House Robber, Climbing Stairs |
| **2D DP** | Grid paths, LCS, Edit Distance |
| **Knapsack** | 0/1, Unbounded, Subset Sum |
| **Interval DP** | Matrix Chain, Palindromes, Burst Balloons |
| **State Machine** | Stock Trading Problems |
| **String DP** | Decodings, Distinct Subsequences, Interleaving |

These patterns cover 90%+ of Dynamic Programming problems in technical interviews. Master the state definitions, and the recurrences follow naturally.