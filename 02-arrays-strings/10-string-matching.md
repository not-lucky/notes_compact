# String Matching

> **Prerequisites:** [09-string-basics.md](./09-string-basics.md)

## Overview

String matching (pattern search) finds occurrences of a pattern P in text T. While brute force is $\Theta(n \cdot m)$, techniques like Rabin-Karp (rolling hash) and KMP (prefix function) achieve $\Theta(n + m)$. Understanding when each applies is key to interview success.

## Building Intuition

**Why is brute force $\Theta(n \cdot m)$ and how do we beat it?**

The key insight is **avoiding redundant comparisons**:

1. **Brute Force Waste**: When a mismatch occurs at position i+j, brute force starts over at i+1. But we've already compared characters at i+1, i+2, etc. Can we reuse this work?

2. **Rabin-Karp Insight**: Instead of comparing characters one by one, compute a hash of the current window. If hashes don't match, no need to compare (O(1) rejection). If hashes match, verify character-by-character (handles collisions). Rolling hash updates in O(1) as the window slides.

3. **KMP Insight**: When mismatch occurs, how far can we skip? If we've matched "ABAB" and the pattern is "ABABAC", the "AB" at the end of what we matched is also a prefix of the pattern. We can resume matching from there instead of starting over.

**Mental Model - Rabin-Karp**: Think of hashing as a "fingerprint." Comparing fingerprints is fast (one number comparison), while comparing full documents is slow. The rolling hash is like sliding a fingerprint scanner across the text—each slide updates the fingerprint incrementally.

**Mental Model - KMP (Failure Function)**: The LPS array (Longest Proper Prefix which is also Suffix) tells us: "If we fail at position j, where can we resume without rechecking earlier characters?" It's like having bookmarks in the pattern that tell us where to jump back.

**Why We Skip Ahead Safely**:

```
Text:    A B A B A B C ...
Pattern: A B A B A C
                   ↑ mismatch at position 5

We've matched "ABABA". The pattern is "ABABAC".
Longest prefix of "ABABA" that's also a suffix: "ABA" (length 3)

We can resume matching the pattern from position 3 (after "ABA")
because we know those characters already match!

Text:    A B A B A B C ...
Pattern:     A B A B A C
                 ↑ resume here (position 3 in pattern)
```

## When NOT to Use Advanced String Matching

Sometimes simpler approaches work better:

1. **Short Strings**: For small inputs (n, m < 1000), brute force is fast and clear. KMP's constant factors may not pay off.

2. **Built-in Is Available**: In interviews, `text.find(pattern)` is often acceptable. Modern languages have optimized implementations (often Boyer-Moore variants).

3. **Single Search in Short Text**: Building KMP's failure function is O(m). For one search in short text, brute force may be faster.

4. **Multiple Different Patterns**: If searching for many patterns simultaneously, consider Aho-Corasick (automaton-based) instead of repeated KMP.

5. **Approximate Matching**: For fuzzy matching (edit distance ≤ k), use DP-based approaches, not exact match algorithms.

**Red Flags:**

- "Find multiple patterns" → Aho-Corasick or suffix structures
- "Approximate match" or "at most k differences" → Edit distance DP
- "Replace all occurrences" → Python's `str.replace()` is fine for interviews

---

## Interview Context

String matching (finding a pattern in text) appears in interviews as:

- Direct pattern matching problems
- Foundation for more complex problems (regex, wildcard)
- Testing algorithmic thinking (brute force → optimization)

For interviews, focus on:

1. Brute force (know the complexity)
2. Rabin-Karp (rolling hash concept)
3. Understanding when to use built-in functions

KMP is rarely expected but good to mention.

---

## Problem Definition

Given:

- Text `T` of length `n`
- Pattern `P` of length `m`

Find all occurrences of `P` in `T`.

```
T = "ABABDABACDABABCABAB"
P = "ABABC"
         ↑
    Found at index 10
```

---

## Approach 1: Brute Force

### Problem: Implement strStr()
**Problem Statement:** Given two strings `needle` and `haystack`, return the index of the first occurrence of `needle` in `haystack`, or `-1` if `needle` is not part of `haystack`.

**Why it works:**
The brute force approach checks every possible starting position in the `haystack`.
1. For each index `i`, we compare the substring `haystack[i:i+len(needle)]` with `needle`.
2. While simple, its worst-case complexity is $\Theta(n \cdot m)$ where N is haystack length and M is needle length.
Modern built-in functions often use more advanced variants, but brute force is the foundational logic.

```python
def brute_force_search(text: str, pattern: str) -> list[int]:
    """
    Check pattern at every position in text.

    Time: $\Theta((n - m + 1) \cdot m) = \Theta(n \cdot m)$
    Space: $O(n)$ for the output list (or $O(1)$ auxiliary space)
    """
    n, m = len(text), len(pattern)
    occurrences = []

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            occurrences.append(i)

    return occurrences
```

### Pythonic Version

```python
def brute_force_pythonic(text: str, pattern: str) -> list[int]:
    """
    Using list comprehensions (lists are dynamic arrays with amortized $O(1)$ append) (still $\Theta(n \cdot m)$ due to slice comparison).
    Space: $O(n)$ for the output list (or $O(1)$ auxiliary space)
    """
    n, m = len(text), len(pattern)
    return [i for i in range(n - m + 1) if text[i:i + m] == pattern]
```

### Built-in Methods

```python
# Find first occurrence
idx = text.find(pattern)    # Returns -1 if not found
idx = text.index(pattern)   # Raises ValueError if not found

# Find all occurrences
def find_all(text: str, pattern: str) -> list[int]:
    """Find all occurrences using built-in methods."""
    indices = []
    start = 0
    while True:
        idx = text.find(pattern, start)
        if idx == -1:
            break
        indices.append(idx)
        start = idx + 1
    return indices
```

---

## Approach 2: Rabin-Karp (Rolling Hash)

### Problem: Substring Search using Hashing
**Problem Statement:** Find all occurrences of a pattern in a text efficiently by comparing hashes instead of characters.

**Why it works:**
Comparing two strings of length `M` takes O(M). Comparing two numbers takes O(1).
1. We compute a hash for the pattern and for the first window of the text.
2. As we slide the window, we update the hash in O(1) by removing the old character and adding the new one (rolling hash).
3. If hashes match, we perform a character-by-character comparison to confirm (to handle collisions).
This results in an average time complexity of $\Theta(n + m)$.

Use hashing to quickly compare pattern with text windows.

```python
def rabin_karp(text: str, pattern: str) -> list[int]:
    """
    Use rolling hash for O(1) window comparison.

    Time: $\Theta(n + m)$ average, O(n \cdot m) worst case (due to hash collisions)
    Space: $O(n)$ for the output list (or $O(1)$ auxiliary space)
    """
    if len(pattern) > len(text):
        return []

    n, m = len(text), len(pattern)
    base = 256      # Number of characters in alphabet
    mod = 10**9 + 7 # Large prime to avoid overflow

    # Compute base^(m-1) % mod
    h = pow(base, m - 1, mod)

    # Compute initial hashes
    pattern_hash = 0
    window_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        window_hash = (window_hash * base + ord(text[i])) % mod

    occurrences = []

    for i in range(n - m + 1):
        # Check if hashes match
        if pattern_hash == window_hash:
            # Verify character by character (handle collisions)
            if text[i:i + m] == pattern:
                occurrences.append(i)

        # Roll the hash: remove leftmost, add rightmost
        if i < n - m:
            window_hash = (window_hash - ord(text[i]) * h) % mod
            window_hash = (window_hash * base + ord(text[i + m])) % mod
            window_hash = (window_hash + mod) % mod  # Handle negative

    return occurrences
```

### Rolling Hash Visualization

```
Text: "ABCDE", Pattern: "BCD"

Initial window hash (ABC):
hash = ord('A') × 256² + ord('B') × 256 + ord('C')

Roll to next window (BCD):
new_hash = (hash - ord('A') × 256²) × 256 + ord('D')

This is O(1) instead of O(m) to compute!
```

---

## Approach 3: KMP (Knuth-Morris-Pratt)

### Problem: Efficient Substring Search
**Problem Statement:** Find all occurrences of a pattern in a text in guaranteed $\Theta(n + m)$ time.

**Why it works:**
KMP avoids backtracking in the text by using a "failure function" (LPS array) precalculated from the pattern.
1. The LPS array tells us the length of the longest proper prefix of `P[0...i]` that is also a suffix of `P[0...i]`.
2. When a mismatch occurs, we know some portion of the pattern already matches the text.
3. We "jump" the pattern forward to the next possible match based on the LPS, ensuring we never re-compare characters in the text that we've already matched.

Uses a prefix function to avoid redundant comparisons.

```python
def kmp_search(text: str, pattern: str) -> list[int]:
    """
    KMP algorithm using failure function.

    Time: $\Theta(n + m)$
    Space: $O(m)$ for the LPS (failure function) array, plus $O(n)$ for the output list
    """
    if not pattern:
        return [0]

    # Build failure function (longest proper prefix suffix)
    def build_lps(pattern: str) -> list[int]:
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        return lps

    lps = build_lps(pattern)
    occurrences = []

    n, m = len(text), len(pattern)
    i = j = 0

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            occurrences.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return occurrences
```

### LPS (Failure Function) Explanation

```
Pattern: "ABABAC"
LPS:     [0, 0, 1, 2, 3, 0]

lps[i] = length of longest proper prefix of pattern[0:i+1]
         that is also a suffix

"ABABA" → longest prefix-suffix is "ABA" (length 3)

When mismatch at position j, jump to lps[j-1] instead of 0.
```

---

## When to Use Which

| Algorithm   | Time       | Space | Use When                                      |
| ----------- | ---------- | ----- | --------------------------------------------- |
| Brute Force | $\Theta(n \cdot m)$      | O(1)  | Short strings, simple cases                   |
| Built-in    | $\Theta(n \cdot m)$\*    | O(1)  | Production code, interview shortcuts          |
| Rabin-Karp  | $\Theta(n + m)$ avg | O(1)  | Multiple pattern search, plagiarism detection |
| KMP         | $\Theta(n + m)$     | O(m)  | Guaranteed linear, streaming text             |

\*Python's `find()` uses optimized algorithms internally.

---

## Template: Find and Replace

```python
def find_replace(text: str, pattern: str, replacement: str) -> str:
    """
    Replace all occurrences of pattern with replacement.

    Time: $\Theta(n \cdot m)$ for finding, $\Theta(n)$ for replacement
    Space: $O(n)$ for the result list
    """
    # Using built-in (preferred in interviews)
    return text.replace(pattern, replacement)

def find_replace_manual(text: str, pattern: str, replacement: str) -> str:
    """Manual implementation."""
    result = []
    i = 0
    n, m = len(text), len(pattern)

    while i < n:
        if text[i:i + m] == pattern:
            result.append(replacement)
            i += m
        else:
            result.append(text[i])
            i += 1

    return "".join(result)  # O(n) join is efficient compared to += string concatenation (which is often $O(n^2)$ due to memory churn)
```

---

## Template: Wildcard Matching

### Problem: Wildcard Matching
**Problem Statement:** Implement wildcard pattern matching with support for `'?'` and `'*'`. `'?'` matches any single character. `'*'` matches any sequence of characters (including the empty sequence).

**Why it works:**
We use 2D Dynamic Programming where `dp[i][j]` is true if the first `i` characters of the string match the first `j` characters of the pattern.
1. If `p[j-1] == '?'` or characters match, `dp[i][j] = dp[i-1][j-1]`.
2. If `p[j-1] == '*'`, it can either match empty (`dp[i][j-1]`) or one or more characters (`dp[i-1][j]`).
The DP table systematically builds up the solution by combining these sub-problems.

```python
def is_match(s: str, p: str) -> bool:
    """
    Wildcard pattern matching:
    '?' matches any single character
    '*' matches any sequence (including empty)

    Time: $\Theta(m \cdot n)$
    Space: $\Theta(m \cdot n)$ for the DP table
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Handle patterns like "*", "**", etc.
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # '*' matches empty (dp[i][j-1]) or one+ chars (dp[i-1][j])
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif p[j - 1] == '?' or s[i - 1] == p[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]
```

---

## Template: Regex Matching (Simplified)

### Problem: Regular Expression Matching
**Problem Statement:** Implement regular expression matching with support for `'.'` and `'*'`. `'.'` matches any single character. `'*'` matches zero or more of the preceding element.

**Why it works:**
This is more complex than wildcard matching because `'*'` depends on the *preceding* character.
1. If `p[j-1] == '*'`, we check:
   a. Zero occurrences of the preceding char: `dp[i][j-2]`.
   b. One or more occurrences: if the preceding char matches `s[i-1]`, we can stay in the same state `dp[i-1][j]`.
The state transition for `'*'` is the "killer feature" of this DP approach.

```python
def is_match_regex(s: str, p: str) -> bool:
    """
    Simple regex with '.' and '*'.
    '.' matches any single character
    '*' means zero or more of the preceding element

    Time: $\Theta(m \cdot n)$
    Space: $\Theta(m \cdot n)$ for the DP table
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Handle patterns like "a*", "a*b*"
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # Zero occurrences
                dp[i][j] = dp[i][j - 2]
                # One or more occurrences
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]
```

---

## Edge Cases

```python
# Empty pattern
"" in "hello" → True (at every position)

# Empty text
"abc" in "" → False

# Pattern longer than text
Immediately return []

# Single character
One comparison

# All same characters
"aaa" in "aaaaaaa" → multiple overlapping matches

# Substring at start/end
"abc" in "abcdef" → 0
"abc" in "defabc" → 3
```

---

## Practice Problems

| #   | Problem                     | Difficulty | Pattern               |
| --- | --------------------------- | ---------- | --------------------- |
| 1   | Implement strStr()          | Easy       | Brute force or KMP    |
| 2   | Repeated Substring Pattern  | Easy       | Pattern matching      |
| 3   | Wildcard Matching           | Hard       | DP                    |
| 4   | Regular Expression Matching | Hard       | DP                    |
| 5   | Shortest Palindrome         | Hard       | KMP prefix function   |
| 6   | Longest Happy Prefix        | Hard       | KMP LPS               |
| 7   | Find All Anagrams           | Medium     | Sliding window + hash |

---

## Key Takeaways

1. **Brute force is $\Theta(n \cdot m)$** - acceptable for interviews if explained
2. **Built-in methods are fine** - Python's find() is optimized
3. **Rabin-Karp** - rolling hash, good for multiple patterns
4. **KMP** - guaranteed $\Theta(n + m)$, know the concept
5. **Wildcard/Regex** - DP approach with careful state transitions

---

## Next: [11-anagram-problems.md](./11-anagram-problems.md)

Learn techniques for anagram-related problems.
