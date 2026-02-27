# DP on Strings

> **Prerequisites:** [08-longest-common-subsequence](./08-longest-common-subsequence.md), [09-edit-distance](./09-edit-distance.md)

## Overview

String DP encompasses problems involving subsequences, interleavings, decodings, and pattern matching across one or more strings. While they share similarities with general DP problems, they often leverage the linear and contiguous nature of strings.

## Building Intuition

**Why do strings need specialized DP patterns?**

1. **Character-by-Character Decisions**: Most string DP processes strings one character at a time, deciding how each character contributes to the answer (e.g., matching it, deleting it, replacing it).

2. **Common State Patterns**:
   - `dp[i]` = answer for prefix `s[0..i-1]` (single string, 1D DP)
   - `dp[i][j]` = answer for prefixes `s1[0..i-1]` and `s2[0..j-1]` (two strings, 2D Sequence Alignment)
   - `dp[i][j]` = answer for substring `s[i..j]` (interval on single string, 2D Interval DP)

3. **Use vs Skip Decision**: Many problems ask "use this character or skip it?" Similar to 0/1 knapsack but applied to characters in a specific sequence.

4. **Counting vs Optimization**: String problems often involve counting (distinct subsequences, valid decodings) rather than just optimization. The recurrence relation usually sums probabilities or counts rather than taking a `max()` or `min()`.

5. **The Interleaving Insight**: Interleaving problems track positions in multiple strings simultaneously, asking "did this character come from `s1` or `s2`?"

6. **Mental Model (Single String)**: Walk through the string character by character. At each step, update your answer based on the current character and the history computed so far.

7. **Mental Model (Two Strings)**: Maintain a 2D grid where cell `(i, j)` represents the "answer for the first `i` chars of `s1` and the first `j` chars of `s2`." Fill it systematically, usually by matching `s1[i-1]` and `s2[j-1]`.

## Interview Context

Advanced string DP problems appear frequently in FANG+ interviews because they test:

1. **Complex state transitions**: You must handle multiple matching and mismatching cases.
2. **Space optimization**: Many 2D string DP problems can be optimized to O(n) space since they only rely on the previous row or column.
3. **Boundary conditions**: Correctly initializing empty strings (`dp[0][0]`, `dp[0][j]`, `dp[i][0]`) is a common stumbling block.

---

## When NOT to Use String DP

1. **Simple String Matching**: For exact matching or finding a pattern without wildcards, use built-in string methods or KMP.
   - *Example*: Finding the first occurrence of "needle" in "haystack".

2. **Suffix-Based Problems**: For suffix arrays, longest repeated substring, or complex substring search, specialized suffix data structures (Tries, Suffix Trees) are better than DP.
   - *Example*: Finding the longest repeated substring. Suffix trees do this in O(n), while DP is O(n²).

3. **Very Long Strings ($n > 10^4$ for $O(n^2)$)**: Many string DPs are $O(n^2)$ or $O(nm)$. For $n = 10^6$, this will Time Limit Exceeded (TLE).
   - *Example*: Comparing two full books for similarity.

4. **Need Rolling Hash or Hashing**: For finding duplicate substrings, Rabin-Karp hashing is often more efficient.

5. **Streaming/Online Processing**: If the string is given character by character and you need immediate answers, batch DP doesn't apply.

---

## Sub-pattern: 1D Prefix DP (Decoding and Formatting)

This sub-pattern involves a 1D state array where `dp[i]` depends on a constant number of previous elements (e.g., `i-1` and `i-2`). This is very similar to the Fibonacci sequence or Climbing Stairs, but applied to string properties.

### Decode Ways

Count the number of ways to decode a string of digits where '1' -> 'A', '2' -> 'B', ..., '26' -> 'Z'.

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

        prev2, prev1 = prev1, curr

    return prev1
```

### Decode Ways II (with Wildcards)

A harder variant where `*` can match any digit from 1-9. This involves more complex branching but the same 1D prefix pattern.

```python
def num_decodings_ii(s: str) -> int:
    """
    Decode with * matching 1-9.

    Time: O(n)
    Space: O(1)
    """
    MOD = 10**9 + 7

    if not s or s[0] == '0':
        return 0

    def single_ways(c: str) -> int:
        if c == '*': return 9
        elif c == '0': return 0
        else: return 1

    def double_ways(c1: str, c2: str) -> int:
        if c1 == '*' and c2 == '*':
            return 15  # '11'-'19' (9 ways) + '21'-'26' (6 ways)
        elif c1 == '*':
            return 2 if c2 <= '6' else 1  # '1x' and possibly '2x'
        elif c2 == '*':
            if c1 == '1': return 9
            elif c1 == '2': return 6
            else: return 0
        else:
            return 1 if 10 <= int(c1 + c2) <= 26 else 0

    prev2, prev1 = 1, single_ways(s[0])

    for i in range(2, len(s) + 1):
        curr = (single_ways(s[i - 1]) * prev1 + double_ways(s[i - 2], s[i - 1]) * prev2) % MOD
        prev2, prev1 = prev1, curr

    return prev1
```

---

## Sub-pattern: 2D Sequence Alignment (Two Strings)

This sub-pattern involves comparing two strings. The state is typically a 2D array `dp[i][j]` representing the solution for prefixes `s1[0..i-1]` and `s2[0..j-1]`.

### Distinct Subsequences

Count the number of distinct subsequences of `s` that equal `t`.

#### Recurrence Relation

Let `dp[i][j]` be the number of distinct subsequences of `s[0..i-1]` that equal `t[0..j-1]`.

If `s[i-1] == t[j-1]`, we have two choices:
1. Use `s[i-1]` to match `t[j-1]`: The problem reduces to matching `s[0..i-2]` with `t[0..j-2]` (`dp[i-1][j-1]`).
2. Don't use `s[i-1]`: The problem reduces to matching `s[0..i-2]` with `t[0..j-1]` (`dp[i-1][j]`).

If `s[i-1] != t[j-1]`, we cannot use `s[i-1]`, so we must drop it: `dp[i-1][j]`.

$$
dp[i][j] =
\begin{cases}
1 & \text{if } j = 0 \text{ (empty } t \text{ matches any } s \text{ by deleting all chars)} \\
0 & \text{if } i = 0 \text{ and } j > 0 \text{ (empty } s \text{ cannot match non-empty } t \text{)} \\
dp[i-1][j] + (dp[i-1][j-1] \text{ if } s[i-1] == t[j-1] \text{ else } 0) & \text{otherwise}
\end{cases}
$$

#### Space-Optimized Implementation

Since `dp[i][j]` only relies on `dp[i-1][j]` and `dp[i-1][j-1]` (the row directly above), we can optimize the space to O(n) by using a single array and updating it backwards.

```python
def num_distinct(s: str, t: str) -> int:
    """
    Count distinct subsequences of s that equal t.

    Time: O(m * n) where m=len(s), n=len(t)
    Space: O(n) using 1D DP array
    """
    m, n = len(s), len(t)
    # dp[j] represents the number of ways to form t[0..j-1]
    dp = [0] * (n + 1)
    dp[0] = 1  # Empty t can be formed in 1 way from any prefix of s

    for i in range(1, m + 1):
        # Iterate backwards to avoid overwriting dp[j-1] which is needed for dp[j]
        # We only need to check up to min(i, n) since a string of length i
        # can't have a subsequence longer than i.
        for j in range(min(i, n), 0, -1):
            if s[i - 1] == t[j - 1]:
                # ways = don't use s[i-1] + use s[i-1]
                dp[j] = dp[j] + dp[j - 1]
            # else: dp[j] remains dp[j] (equivalent to dp[i-1][j])

    return dp[n]
```

#### Visual Walkthrough
`s = "rabbbit"`, `t = "rabbit"`

| | "" | `r` | `a` | `b` | `b` | `i` | `t` |
|---|---|---|---|---|---|---|---|
| **""** | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| **`r`** | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| **`a`** | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| **`b`** | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| **`b`** | 1 | 1 | 1 | 2 | 1 | 0 | 0 |
| **`b`** | 1 | 1 | 1 | 3 | 3 | 0 | 0 |
| **`i`** | 1 | 1 | 1 | 3 | 3 | 3 | 0 |
| **`t`** | 1 | 1 | 1 | 3 | 3 | 3 | 3 ← Answer |

### Interleaving String

Check if `s3` is formed by interleaving `s1` and `s2`.

#### Recurrence Relation

Let `dp[i][j]` be a boolean representing whether `s3[0..i+j-1]` is a valid interleaving of `s1[0..i-1]` and `s2[0..j-1]`.

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

    Time: O(m * n)
    Space: O(n) optimized to 1D array
    """
    m, n = len(s1), len(s2)

    if m + n != len(s3):
        return False

    # dp[j] represents whether s1[0..i-1] and s2[0..j-1] can form s3[0..i+j-1]
    dp = [False] * (n + 1)
    dp[0] = True

    # Initialize the first row (using only characters from s2)
    for j in range(1, n + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]

    # Process remaining rows
    for i in range(1, m + 1):
        # Update first column (using only characters from s1)
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]

        for j in range(1, n + 1):
            match_s1 = dp[j] and s1[i - 1] == s3[i + j - 1]
            match_s2 = dp[j - 1] and s2[j - 1] == s3[i + j - 1]
            dp[j] = match_s1 or match_s2

    return dp[n]
```

---

## Sub-pattern: Recursive Splitting / Scramble

This sub-pattern involves breaking a string into two parts at an arbitrary index, and recursively checking if the parts can form the target string, often allowing operations like swapping. These problems are generally solved top-down with memoization.

### Scramble String

Check if `s2` is a scrambled version of `s1`. A string can be scrambled by recursively partitioning it into two non-empty substrings, and optionally swapping them.

```python
from functools import lru_cache

def is_scramble(s1: str, s2: str) -> bool:
    """
    Check if s2 is a scramble of s1.

    Time: O(n^4) due to states (i1, i2, length) taking O(n^3) and O(n) loop inside.
    Space: O(n^3) for the memoization cache.
    """
    if len(s1) != len(s2): return False

    @lru_cache(maxsize=None)
    def dp(i1: int, i2: int, length: int) -> bool:
        # Base case: identical substrings
        if s1[i1:i1+length] == s2[i2:i2+length]:
            return True

        # Pruning: if character frequencies don't match, they can't be scrambles
        if sorted(s1[i1:i1+length]) != sorted(s2[i2:i2+length]):
            return False

        # Try all possible split points
        for k in range(1, length):
            # Case 1: No swap at this level
            if dp(i1, i2, k) and dp(i1+k, i2+k, length-k):
                return True

            # Case 2: Swap at this level
            if dp(i1, i2+length-k, k) and dp(i1+k, i2, length-k):
                return True

        return False

    return dp(0, 0, len(s1))
```

---

## Sub-pattern: Palindromic Strings (Interval DP)

Palindromic problems often use interval DP where the state is `dp[i][j]`, representing the substring from index `i` to `j`.

The transition generally depends on the outer characters (`s[i]` and `s[j]`) and the inner substring (`dp[i+1][j-1]`). Because computing `dp[i][j]` requires knowing `dp[i+1][j-1]`, we must iterate by the **length** of the substring, starting from length 1 up to $n$.

### Count Different Palindromic Subsequences

Find the number of distinct non-empty palindromic subsequences in `s`.

```python
def count_palindromic_subseq(s: str) -> int:
    """
    Count distinct palindromic subsequences modulo 10^9 + 7.

    Time: O(n^2)
    Space: O(n^2)
    """
    MOD = 10**9 + 7
    n = len(s)

    # dp[i][j] = count of distinct palindromic subseq in s[i..j]
    dp = [[0] * n for _ in range(n)]

    # Base case: strings of length 1
    for i in range(n):
        dp[i][i] = 1

    # Iterate by length of interval
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                left, right = i + 1, j - 1

                # Find the first occurrences of s[i] inside the interval
                while left <= right and s[left] != s[i]:
                    left += 1
                while left <= right and s[right] != s[j]:
                    right -= 1

                if left > right:
                    # Case 1: The character s[i] doesn't exist inside s[i+1..j-1]
                    # Example: "aba" -> "b" contributes forms, plus "a", "aa", and "a_a"
                    dp[i][j] = dp[i + 1][j - 1] * 2 + 2
                elif left == right:
                    # Case 2: The character exists exactly once inside s[i+1..j-1]
                    # Example: "aaa" -> "a" contributes, plus "aa", "aaa", and "a_a"
                    dp[i][j] = dp[i + 1][j - 1] * 2 + 1
                else:
                    # Case 3: The character exists multiple times inside
                    # We must subtract the overcounted inner subsequences
                    dp[i][j] = dp[i + 1][j - 1] * 2 - dp[left + 1][right - 1]
            else:
                # Inclusion-exclusion principle:
                # Count subsequences without left char + without right char - without both
                dp[i][j] = dp[i + 1][j] + dp[i][j - 1] - dp[i + 1][j - 1]

            dp[i][j] %= MOD

    # Python handles negative modulo correctly, but good practice in other languages:
    # return (dp[0][n - 1] + MOD) % MOD
    return dp[0][n - 1]
```

---

## Sub-pattern: State Machine DP on Strings (Parentheses)

These problems often involve a state machine or maintaining the length of a valid prefix/suffix.

### Longest Valid Parentheses

Given a string containing just the characters `'('` and `')'`, find the length of the longest valid (well-formed) parentheses substring.

```python
def longest_valid_parentheses(s: str) -> int:
    """
    Find length of longest valid parentheses substring.

    State: dp[i] = length of the longest valid substring ENDING at index i.

    Time: O(n)
    Space: O(n)
    """
    n = len(s)
    if n == 0:
        return 0
    dp = [0] * n
    max_len = 0

    for i in range(1, n):
        if s[i] == ')':
            if s[i - 1] == '(':
                # Case 1: Simple pair like "...()"
                # The length is 2 plus whatever valid string preceded it
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
            else:
                # Case 2: Nested pair like "...))"
                # If s[i-1] is ')', there might be a matching '(' before the valid string ending at i-1
                prev_valid_len = dp[i - 1]
                match_idx = i - prev_valid_len - 1

                if match_idx >= 0 and s[match_idx] == '(':
                    # Found a matching '(' for our current ')'
                    dp[i] = prev_valid_len + 2

                    # Add any valid string that immediately precedes the matching '('
                    if match_idx - 1 >= 0:
                        dp[i] += dp[match_idx - 1]

            max_len = max(max_len, dp[i])

    return max_len
```

---

## Non-DP String Problems (For Contrast)

Some string matching problems look like DP but are better solved with hashing, tries, or greedy two-pointer approaches. Identifying when NOT to use DP is crucial.

### Palindrome Pairs (Tries / Hash Maps)

Given a list of unique words, find all pairs `(i, j)` such that the concatenation `words[i] + words[j]` is a palindrome. *(Not strictly DP, but often tested in string arrays).*

```python
def palindrome_pairs(words: list[str]) -> list[list[int]]:
    """
    Find pairs (i, j) where words[i] + words[j] is palindrome.
    Uses hash map for O(1) lookups of reversed strings.

    Time: O(n * k^2) where n = number of words, k = max word length
    Space: O(n * k) for the hash map
    """
    def is_palindrome(s: str) -> bool:
        return s == s[::-1]

    word_to_idx = {word: i for i, word in enumerate(words)}
    result = []

    for i, word in enumerate(words):
        k = len(word)
        # Try splitting the word into prefix and suffix
        for j in range(k + 1):
            prefix = word[:j]
            suffix = word[j:]

            # Case 1: If prefix is a palindrome, check if reverse(suffix) exists.
            # E.g., word="llbat", prefix="ll" (palindrome), suffix="bat".
            # If "tab" exists, "tab" + "llbat" = "tabllbat" (palindrome).
            if is_palindrome(prefix):
                rev_suffix = suffix[::-1]
                if rev_suffix in word_to_idx and word_to_idx[rev_suffix] != i:
                    result.append([word_to_idx[rev_suffix], i])

            # Case 2: If suffix is a palindrome, check if reverse(prefix) exists.
            # E.g., word="batll", prefix="bat", suffix="ll" (palindrome).
            # If "tab" exists, "batll" + "tab" = "batlltab" (palindrome).
            # Note: We check j != k to prevent duplicates (empty suffix covered by empty prefix)
            if j != k and is_palindrome(suffix):
                rev_prefix = prefix[::-1]
                if rev_prefix in word_to_idx and word_to_idx[rev_prefix] != i:
                    result.append([i, word_to_idx[rev_prefix]])

    return result
```

### Shortest Way to Form String (Greedy / Two Pointers)

Find the minimum number of subsequences of `source` needed to form `target`.

```python
def shortest_way(source: str, target: str) -> int:
    """
    Minimum subsequences of source to form target.
    A greedy approach works best here, no DP needed.

    Time: O(m * n) in worst case (can be optimized to O(n log m) with binary search on indices)
    Space: O(1) aux space
    """
    # Quick check to ensure all target characters exist in source
    source_set = set(source)
    for c in target:
        if c not in source_set:
            return -1

    count = 0
    i = 0  # Pointer in target

    while i < len(target):
        count += 1
        j = 0  # Reset pointer in source for a new subsequence

        # Greedily match as many characters as possible in one pass of source
        while i < len(target) and j < len(source):
            if source[j] == target[i]:
                i += 1
            j += 1

    return count
```

---

## Common Patterns Summary

| Problem | Key Insight | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Distinct Subsequences** | Match current char + don't match. | $O(mn)$ | $O(n)$ optimized |
| **Interleaving String** | 2D table tracking `s1` vs `s2` usage. | $O(mn)$ | $O(n)$ optimized |
| **Scramble String** | Top-down interval DP with splitting. | $O(n^4)$ | $O(n^3)$ |
| **Decode Ways** | 1D prefix DP. Look back 1 and 2 steps. | $O(n)$ | $O(1)$ optimized |
| **Valid Parentheses** | DP state is length ending at index $i$. | $O(n)$ | $O(n)$ |
| **Palindromic Subseqs** | 2D Interval DP checking `s[i] == s[j]`. | $O(n^2)$ | $O(n^2)$ |

---

## Interview Tips

1. **Draw the DP table**: For 2D problems, draw a matrix. For interval problems, you only fill the upper right triangle.
2. **Handle empty strings**: Initialize an extra row/column for empty prefixes (`dp[0]`).
3. **Space optimize**: 2D Sequence Alignment problems can almost always be space-optimized to $O(\min(n, m))$. Mention this to the interviewer even if you write the $O(nm)$ version first.
4. **Watch for overflow**: When counting combinations or subsequences, ask if the answer needs to be modulo $10^9 + 7$.
5. **State Definition is King**: Clearly state what `dp[i]` or `dp[i][j]` represents before writing code. Is it "ending at $i$" or "using prefix of length $i$"?

---

## Practice Problems

| # | Problem | Difficulty | Pattern |
| :--- | :--- | :--- | :--- |
| 1 | [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) | Hard | 2D Sequence Alignment |
| 2 | [Interleaving String](https://leetcode.com/problems/interleaving-string/) | Medium | 2D Sequence Alignment |
| 3 | [Scramble String](https://leetcode.com/problems/scramble-string/) | Hard | Recursive Partition |
| 4 | [Decode Ways](https://leetcode.com/problems/decode-ways/) | Medium | 1D Prefix DP |
| 5 | [Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses/) | Hard | 1D State Machine |
| 6 | [Palindrome Pairs](https://leetcode.com/problems/palindrome-pairs/) | Hard | Strings / Hash Map |
| 7 | [Count Different Palindromic Subsequences](https://leetcode.com/problems/count-different-palindromic-subsequences/) | Hard | Interval DP |

---

## Key Takeaways

1. **String DP builds on LCS/Edit Distance**: They share the same foundations of comparing `s1[i]` and `s2[j]`.
2. **Interval DP is unique**: Problems like Longest Palindromic Subsequence require iterating by the *length* of the substring.
3. **Space optimization is expected**: In a FANG+ interview, reducing $O(nm)$ space to $O(n)$ or $O(1)$ shows seniority.
4. **Not everything is DP**: Be ready to pivot to Tries, Two Pointers, or Hashing if the DP state seems too complex or $n > 10^4$.

---

## Chapter Complete!

You've now covered all major DP patterns for FANG+ interviews:

| Category | Key Topics |
| :--- | :--- |
| **1D DP** | Fibonacci, House Robber, Climbing Stairs |
| **2D DP** | Grid paths, LCS, Edit Distance |
| **Knapsack** | 0/1, Unbounded, Subset Sum |
| **String DP** | Decodings, Distinct Subsequences, Interleaving |
| **Interval DP** | Palindromes, Matrix Chain, Burst Balloons |
| **State Machine** | Stock Trading Problems |

These patterns cover 90%+ of Dynamic Programming problems in technical interviews.