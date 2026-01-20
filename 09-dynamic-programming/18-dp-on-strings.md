# DP on Strings

> **Prerequisites:** [08-longest-common-subsequence](./08-longest-common-subsequence.md), [09-edit-distance](./09-edit-distance.md)

## Overview

String DP encompasses problems involving subsequences, interleavings, decodings, and pattern matching across one or more strings.

## Building Intuition

**Why do strings need specialized DP patterns?**

1. **Character-by-Character Decisions**: Most string DP processes strings one character at a time, deciding how each character contributes to the answer.

2. **Common State Patterns**:
   - dp[i] = answer for prefix s[0..i-1] (single string)
   - dp[i][j] = answer for prefixes s1[0..i-1] and s2[0..j-1] (two strings)
   - dp[i][j] = answer for substring s[i..j] (interval on single string)

3. **Use vs Skip Decision**: Many problems ask "use this character or skip it?" Similar to 0/1 knapsack but for characters.

4. **Counting vs Optimization**: String problems often involve counting (distinct subsequences, decodings) rather than just optimization. The recurrence adds possibilities rather than taking max.

5. **The Interleaving Insight**: Interleaving problems track positions in multiple strings simultaneously, asking "did this character come from s1 or s2?"

6. **Mental Model (Single String)**: Walk through the string character by character. At each step, update your answer based on the current character and what you've computed so far.

7. **Mental Model (Two Strings)**: Maintain a 2D grid where cell (i, j) represents "answer for first i chars of s1 and first j chars of s2." Fill it systematically.

## Interview Context

Advanced string DP problems appear in FANG+ because:

1. **Complex state transitions**: Multiple cases to handle
2. **Pattern matching**: Real-world text processing
3. **Counting problems**: Number of ways to achieve goal
4. **Interleaving/Combination**: String manipulation

---

## When NOT to Use String DP

1. **Simple String Matching**: For exact matching or pattern without wildcards, use built-in string methods or KMP. DP is overkill.

2. **Suffix-Based Problems**: For suffix arrays, longest repeated substring, or substring search, specialized suffix data structures are better than DP.

3. **Very Long Strings (n > 10⁴ for O(n²))**: Many string DPs are O(n²) or O(nm). For n = 10⁶, this times out. Consider approximations or different algorithms.

4. **Need Rolling Hash or Hashing**: For problems like finding duplicate substrings, Rabin-Karp hashing is often more efficient than DP.

5. **Streaming/Online Processing**: If the string is given character by character and you need immediate answers, batch DP doesn't apply.

**Common String DP Categories:**
- Subsequence: LCS, Distinct Subsequences
- Transformation: Edit Distance, One Edit Distance
- Decoding: Decode Ways, Valid Parentheses
- Interleaving: Interleaving String, Scramble String
- Palindrome: LPS, Partition, Count

---

## Distinct Subsequences

Count subsequences of s that equal t.

```python
def num_distinct(s: str, t: str) -> int:
    """
    Count distinct subsequences of s that equal t.

    State: dp[i][j] = ways to form t[0..j-1] from s[0..i-1]
    Recurrence:
        dp[i][j] = dp[i-1][j]  (don't use s[i-1])
        if s[i-1] == t[j-1]: dp[i][j] += dp[i-1][j-1]

    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(s), len(t)
    dp = [0] * (n + 1)
    dp[0] = 1  # Empty t can be formed in 1 way

    for i in range(1, m + 1):
        # Iterate backwards to avoid overwriting
        for j in range(min(i, n), 0, -1):
            if s[i - 1] == t[j - 1]:
                dp[j] += dp[j - 1]

    return dp[n]
```

### Example

```
s = "rabbbit", t = "rabbit"

Ways: 3
r a b b b i t
r a b b - i t  ✓
r a b - b i t  ✓
r a - b b i t  ✓
```

---

## Interleaving String

Check if s3 is formed by interleaving s1 and s2.

```python
def is_interleave(s1: str, s2: str, s3: str) -> bool:
    """
    Is s3 an interleaving of s1 and s2?

    State: dp[i][j] = can form s3[0..i+j-1] from s1[0..i-1] and s2[0..j-1]

    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(s1), len(s2)

    if m + n != len(s3):
        return False

    dp = [False] * (n + 1)
    dp[0] = True

    # Initialize first row
    for j in range(1, n + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]

    for i in range(1, m + 1):
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]

        for j in range(1, n + 1):
            dp[j] = ((dp[j] and s1[i - 1] == s3[i + j - 1]) or
                     (dp[j - 1] and s2[j - 1] == s3[i + j - 1]))

    return dp[n]
```

### Example

```
s1 = "aab", s2 = "axy", s3 = "aaxaby"

     ""  a   x   y
""    T  T   F   F
a     T  T   T   F
a     T  T   T   F
b     F  F   T   T

True: s3 can be formed
```

---

## Scramble String

Check if s2 is a scrambled version of s1.

```python
from functools import lru_cache

def is_scramble(s1: str, s2: str) -> bool:
    """
    Is s2 a scramble of s1?

    Scramble: recursively swap children of binary tree nodes.

    Time: O(n⁴)
    Space: O(n³)
    """
    if len(s1) != len(s2):
        return False

    if s1 == s2:
        return True

    @lru_cache(maxsize=None)
    def dp(i1: int, i2: int, length: int) -> bool:
        if s1[i1:i1+length] == s2[i2:i2+length]:
            return True

        # Check if same characters
        if sorted(s1[i1:i1+length]) != sorted(s2[i2:i2+length]):
            return False

        for k in range(1, length):
            # Not swapped
            if dp(i1, i2, k) and dp(i1+k, i2+k, length-k):
                return True
            # Swapped
            if dp(i1, i2+length-k, k) and dp(i1+k, i2, length-k):
                return True

        return False

    return dp(0, 0, len(s1))
```

---

## Decode Ways

```python
def num_decodings(s: str) -> int:
    """
    Count ways to decode '1'-'26' to 'A'-'Z'.

    Time: O(n)
    Space: O(1)
    """
    if not s or s[0] == '0':
        return 0

    n = len(s)
    prev2, prev1 = 1, 1  # dp[0], dp[1]

    for i in range(2, n + 1):
        curr = 0

        # Single digit (1-9)
        if s[i - 1] != '0':
            curr += prev1

        # Two digits (10-26)
        two_digit = int(s[i - 2:i])
        if 10 <= two_digit <= 26:
            curr += prev2

        prev2, prev1 = prev1, curr

    return prev1
```

---

## Decode Ways II

With `*` matching 1-9.

```python
def num_decodings_ii(s: str) -> int:
    """
    Decode with * matching 1-9.

    Time: O(n)
    Space: O(1)
    """
    MOD = 10**9 + 7

    if not s:
        return 0

    def single_ways(c: str) -> int:
        if c == '*':
            return 9  # 1-9
        elif c == '0':
            return 0
        else:
            return 1

    def double_ways(c1: str, c2: str) -> int:
        if c1 == '*' and c2 == '*':
            return 15  # 11-19 (9) + 21-26 (6)
        elif c1 == '*':
            if c2 <= '6':
                return 2  # 1X or 2X
            else:
                return 1  # only 1X
        elif c2 == '*':
            if c1 == '1':
                return 9  # 11-19
            elif c1 == '2':
                return 6  # 21-26
            else:
                return 0
        else:
            num = int(c1 + c2)
            return 1 if 10 <= num <= 26 else 0

    prev2, prev1 = 1, single_ways(s[0])

    for i in range(2, len(s) + 1):
        curr = (single_ways(s[i - 1]) * prev1 +
                double_ways(s[i - 2], s[i - 1]) * prev2) % MOD
        prev2, prev1 = prev1, curr

    return prev1
```

---

## Longest Valid Parentheses

```python
def longest_valid_parentheses(s: str) -> int:
    """
    Length of longest valid parentheses substring.

    State: dp[i] = length of valid substring ending at i

    Time: O(n)
    Space: O(n)
    """
    n = len(s)
    dp = [0] * n
    max_len = 0

    for i in range(1, n):
        if s[i] == ')':
            if s[i - 1] == '(':
                # "...()"
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
            elif i - dp[i - 1] - 1 >= 0 and s[i - dp[i - 1] - 1] == '(':
                # "...))"
                dp[i] = dp[i - 1] + 2
                if i - dp[i - 1] - 2 >= 0:
                    dp[i] += dp[i - dp[i - 1] - 2]

            max_len = max(max_len, dp[i])

    return max_len
```

---

## Palindrome Pairs

```python
def palindrome_pairs(words: list[str]) -> list[list[int]]:
    """
    Find pairs (i, j) where words[i] + words[j] is palindrome.

    Time: O(n × k²) where k = max word length
    Space: O(n × k)
    """
    def is_palindrome(s: str) -> bool:
        return s == s[::-1]

    word_to_idx = {word: i for i, word in enumerate(words)}
    result = []

    for i, word in enumerate(words):
        for j in range(len(word) + 1):
            prefix = word[:j]
            suffix = word[j:]

            # If prefix is palindrome, check if reverse of suffix exists
            if is_palindrome(prefix):
                rev_suffix = suffix[::-1]
                if rev_suffix in word_to_idx and word_to_idx[rev_suffix] != i:
                    result.append([word_to_idx[rev_suffix], i])

            # If suffix is palindrome, check if reverse of prefix exists
            if j != len(word) and is_palindrome(suffix):
                rev_prefix = prefix[::-1]
                if rev_prefix in word_to_idx and word_to_idx[rev_prefix] != i:
                    result.append([i, word_to_idx[rev_prefix]])

    return result
```

---

## Count Different Palindromic Subsequences

```python
def count_palindromic_subseq(s: str) -> int:
    """
    Count distinct palindromic subsequences.

    Time: O(n²)
    Space: O(n²)
    """
    MOD = 10**9 + 7
    n = len(s)

    # dp[i][j] = count of distinct palindromic subseq in s[i..j]
    dp = [[0] * n for _ in range(n)]

    # Single characters
    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                left, right = i + 1, j - 1

                # Find matching characters inside
                while left <= right and s[left] != s[i]:
                    left += 1
                while left <= right and s[right] != s[j]:
                    right -= 1

                if left > right:
                    # No matching char inside
                    dp[i][j] = dp[i + 1][j - 1] * 2 + 2
                elif left == right:
                    # One matching char
                    dp[i][j] = dp[i + 1][j - 1] * 2 + 1
                else:
                    # Multiple matching chars
                    dp[i][j] = dp[i + 1][j - 1] * 2 - dp[left + 1][right - 1]
            else:
                dp[i][j] = dp[i + 1][j] + dp[i][j - 1] - dp[i + 1][j - 1]

            dp[i][j] = dp[i][j] % MOD

    return dp[0][n - 1] % MOD
```

---

## Shortest Way to Form String

```python
def shortest_way(source: str, target: str) -> int:
    """
    Minimum subsequences of source to form target.

    Time: O(m × n)
    Space: O(1)
    """
    source_set = set(source)

    # Check if possible
    for c in target:
        if c not in source_set:
            return -1

    count = 0
    i = 0  # Position in target

    while i < len(target):
        count += 1
        j = 0  # Position in source

        while i < len(target) and j < len(source):
            if source[j] == target[i]:
                i += 1
            j += 1

    return count
```

---

## Common Patterns Summary

| Problem | Key Insight | Complexity |
|---------|-------------|------------|
| Distinct Subsequences | Count matches, add don't-use | O(mn) |
| Interleaving | Two pointers in 2D | O(mn) |
| Scramble String | Recursive with memo | O(n⁴) |
| Decode Ways | Fibonacci-like | O(n) |
| Valid Parentheses | Track ending valid length | O(n) |

---

## Interview Tips

1. **Draw the DP table**: Helps visualize transitions
2. **Handle edge cases**: Empty strings, single chars
3. **Space optimize**: Usually 2D → 1D possible
4. **Watch for overflow**: Use modulo when counting
5. **Know the patterns**: LCS, edit distance foundations

---

## Practice Problems

| # | Problem | Difficulty | Pattern |
|---|---------|------------|---------|
| 1 | Distinct Subsequences | Hard | Counting matches |
| 2 | Interleaving String | Medium | Two-string merge |
| 3 | Scramble String | Hard | Recursive partition |
| 4 | Decode Ways | Medium | Fibonacci variant |
| 5 | Longest Valid Parentheses | Hard | Bracket matching |
| 6 | Palindrome Pairs | Hard | String manipulation |

---

## Key Takeaways

1. **String DP builds on LCS/Edit Distance**: Same foundations
2. **State often represents prefixes**: s1[0..i], s2[0..j]
3. **Space optimization common**: Usually need only previous row
4. **Counting needs modulo**: Prevent overflow
5. **Complex problems = multiple cases**: Handle each systematically

---

## Chapter Complete!

You've now covered all major DP patterns for FANG+ interviews:

| Category | Key Topics |
|----------|------------|
| 1D DP | Fibonacci, House Robber, Climbing Stairs |
| 2D DP | Grid paths, LCS, Edit Distance |
| Knapsack | 0/1, Unbounded, Subset Sum |
| String DP | Palindromes, Word Break, Regex |
| Interval DP | Matrix Chain, Burst Balloons |
| State Machine | Stock Problems |

These patterns cover 90%+ of DP problems in technical interviews.
