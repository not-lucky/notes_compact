# String Matching

> **Prerequisites:** [09-string-basics.md](./09-string-basics.md)

## Overview

String matching (pattern search) finds occurrences of a pattern `P` in text `T`. While a naive brute-force approach has a worst-case time complexity of $\Theta(n \cdot m)$, advanced techniques like Rabin-Karp (rolling hash) and KMP (prefix function) can achieve $\Theta(n + m)$. Understanding when each applies is key to interview success.

## Building Intuition

**Why is brute force $\Theta(n \cdot m)$ and how do we beat it?**

The key insight is **avoiding redundant comparisons**.

1. **Brute Force Waste**: Imagine sliding a transparent sheet with the pattern written on it over the text, one letter at a time. If a mismatch occurs at position `i+j`, brute force shifts the sheet exactly one space right to `i+1` and starts checking all over again. But wait—we just compared characters at `i+1`, `i+2`, etc.! Why throw that information away?

2. **Rabin-Karp Insight (The Barcode Scanner)**: Instead of looking at individual letters, imagine having a barcode scanner that reads a "window" of letters and gives you a single number (a hash). Comparing two numbers is lightning fast ($\Theta(1)$) compared to comparing a sequence of letters.
   - If the scanner reads a different number, we slide it over. No need to look closer.
   - If the numbers match, only *then* do we inspect the letters one by one (to handle rare barcode "collisions").
   - Crucially, as we slide the scanner, we can calculate the new barcode mathematically based on the previous barcode, simply by subtracting the old letter that left the window and adding the new letter that entered it. This update is $\Theta(1)$.

3. **KMP Insight (The Smart Jigsaw Puzzle)**: When you're putting together a jigsaw puzzle with a repetitive border (like "ABABAC"), and you realize the 6th piece ("C") is wrong, you don't start the whole border over. You look at the pieces you *did* match ("ABABA"). Since "ABA" is at the start *and* the end of what you just matched, you can keep the last three pieces down and immediately try to fit the 4th piece ("B") again. KMP pre-calculates these "safe jump distances" for the pattern, ensuring we never check the same text character twice.

**Why We Skip Ahead Safely (KMP):**

```text
Text:    A B A B A B C ...
Pattern: A B A B A C
                   ↑ mismatch at position 5

We've matched "ABABA". The pattern is "ABABAC".
Longest prefix of "ABABA" that's also a suffix: "ABA" (length 3)

We can resume matching the pattern from position 3 (after "ABA")
because we know those characters already perfectly match the text!

Text:    A B A B A B C ...
Pattern:     A B A B A C
                 ↑ resume here (position 3 in pattern)
```

## When NOT to Use Advanced String Matching

Sometimes simpler approaches work better:

1. **Short Strings**: For small inputs ($n, m < 1000$), brute force is fast and code is crystal clear. The constant overhead of calculating hashes or KMP prefix arrays may actually be slower.
2. **Built-in Methods**: In interviews, `text.find(pattern)` is often perfectly acceptable. Modern language implementations are highly optimized (often using variants of Boyer-Moore).
3. **Single Search in Short Text**: Building KMP's failure function takes $\Theta(m)$ time. If you only search once in a short text, brute force may finish before KMP finishes setting up.
4. **Multiple Different Patterns**: If searching for a dictionary of words simultaneously, an automaton-based approach like Aho-Corasick or a Trie is better than repeating KMP.
5. **Approximate Matching**: For fuzzy matching (e.g., "allow 1 typo"), you need Dynamic Programming (Edit Distance), not exact match algorithms.

**Red Flags:**
- "Find multiple patterns" → Aho-Corasick or Suffix Trie
- "Approximate match" or "at most k differences" → Edit Distance DP
- "Replace all occurrences" → Python's `str.replace()` is fine

---

## Interview Context

String matching problems appear in interviews as:
- Direct pattern matching (e.g., implement `strStr()`)
- Foundation for complex problems (regex matching, wildcard matching)
- Testing optimization thinking (can you improve on brute force?)

For interviews, focus on:
1. **Brute force**: Know how to code it quickly and state the worst-case $\Theta(n \cdot m)$ complexity.
2. **Rabin-Karp**: Understand the "rolling hash" concept. It is much easier to implement from scratch than KMP.
3. **Built-ins**: Know when it's safe to just use `text.find()`.

*(Note: Implementing KMP flawlessly under 45-minute pressure is rarely expected, but explaining its conceptual advantage is a massive plus.)*

---

## Problem Definition

**Given:**
- Text `T` of length `n`
- Pattern `P` of length `m`

**Find:**
- All starting indices of occurrences of `P` in `T`.

```text
T = "ABABDABACDABABCABAB"
P = "ABABC"
         ↑
    Found at index 10
```

---

## Approach 1: Brute Force

### Problem: Implement `strStr()`
**Problem Statement:** Given two strings `needle` and `haystack`, return the index of the first occurrence of `needle` in `haystack`, or `-1` if `needle` is not part of `haystack`.

**Why it works:**
The transparent sheet metaphor: we slide the pattern over the text, checking every possible starting position.
1. For each index `i` in the text, we compare the substring `text[i:i+len(pattern)]` character-by-character against the pattern.
2. While simple, its worst-case complexity is exactly $\Theta(n \cdot m)$. Imagine `T = "AAAAAA...B"` and `P = "AAAB"`. We match all the way to the end of the pattern before failing and shifting only by 1.

```python
def brute_force_search(text: str, pattern: str) -> list[int]:
    """
    Check pattern at every possible starting position in text.

    Time Complexity:
    - Worst case: $\Theta((n - m + 1) \cdot m)$ which simplifies to $\Theta(n \cdot m)$
    - Best case: $\Theta(n)$ (e.g., first character mismatch always)
    Space Complexity: $\Theta(1)$ auxiliary, $\Theta(k)$ for output list of size k.
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return []

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
    Using list comprehensions and string slicing.
    Note: Slicing creates a new string, so `text[i:i+m] == pattern` takes $\Theta(m)$ time and space.
    Overall Time: $\Theta(n \cdot m)$ worst case.
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return []
    return [i for i in range(n - m + 1) if text[i:i + m] == pattern]
```

### Built-in Methods (Standard in Interviews)

```python
# Find first occurrence
idx = text.find(pattern)    # Returns -1 if not found
idx = text.index(pattern)   # Raises ValueError if not found

def find_all(text: str, pattern: str) -> list[int]:
    """Find all occurrences efficiently using built-in methods."""
    if not pattern:
        return []

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

**Why it works:**
The barcode scanner metaphor. Comparing two strings of length $m$ takes $\Theta(m)$. Comparing two integers takes $\Theta(1)$.
1. Compute a numerical hash for the pattern and for the first $m$-length window of the text.
2. Slide the window one character right. We update the hash mathematically in $\Theta(1)$ by removing the value of the character that left the window and adding the value of the new character.
3. If the integer hashes match, we perform a character-by-character string comparison to confirm (since distinct strings might occasionally have the same hash, a "collision").

```python
def rabin_karp(text: str, pattern: str) -> list[int]:
    """
    Use a rolling hash for $\Theta(1)$ window comparison.

    Time Complexity:
    - Average/Best: $\Theta(n + m)$
    - Worst case: $\Theta(n \cdot m)$ (if there are many hash collisions, or if text consists entirely of matches)
    Space Complexity: $\Theta(1)$ auxiliary.
    """
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []

    base = 256      # Number of characters in alphabet
    mod = 10**9 + 7 # Large prime to minimize collisions

    # h is the positional multiplier for the leftmost character in a window: base^(m-1) % mod
    h = pow(base, m - 1, mod)

    # Compute initial hashes for pattern and the first window in text
    pattern_hash = 0
    window_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        window_hash = (window_hash * base + ord(text[i])) % mod

    occurrences = []

    for i in range(n - m + 1):
        # 1. Check if hashes match
        if pattern_hash == window_hash:
            # 2. Verify character by character to handle potential hash collisions
            if text[i:i + m] == pattern:
                occurrences.append(i)

        # 3. Roll the hash to the next window (remove leftmost, add rightmost)
        if i < n - m:
            # Subtract the leftmost character (multiplying by its positional weight `h`)
            window_hash = (window_hash - ord(text[i]) * h) % mod

            # Shift remaining characters left (multiply by base) and add new character
            window_hash = (window_hash * base + ord(text[i + m])) % mod

            # Ensure the modulo result is positive (Python handles this natively, but good practice for other languages)
            window_hash = (window_hash + mod) % mod

    return occurrences
```

### Rolling Hash Visualization

```text
Text: "ABCDE", Pattern: "BCD", Base: 10 (for simplicity)

Initial window hash ("ABC"):
hash = 'A'*100 + 'B'*10 + 'C'*1

Slide window right to "BCD":
1. Remove 'A':  hash - 'A'*100
2. Shift left:  (hash - 'A'*100) * 10
3. Add 'D':     (hash - 'A'*100) * 10 + 'D'*1

Resulting hash is exactly the numerical representation of "BCD".
We did this in $\Theta(1)$ math operations, rather than scanning the 3 letters again!
```

---

## Approach 3: KMP (Knuth-Morris-Pratt)

### Problem: Guaranteed Linear Time Search

**Why it works:**
KMP uses a "failure function" (LPS array) precalculated from the pattern. The LPS array answers the question: "If I mismatch at this character, what is the longest prefix of my pattern that still matches the text I just successfully read?"
1. Precalculate LPS: `lps[i]` is the length of the longest proper prefix of `P[0...i]` that is also a suffix of `P[0...i]`.
2. As we scan the text, if a mismatch occurs, we jump the pattern forward based on the LPS value, meaning we *never move our text pointer backwards*.

```python
def kmp_search(text: str, pattern: str) -> list[int]:
    """
    KMP algorithm using a precomputed Longest Proper Prefix which is also Suffix (LPS) array.

    Time Complexity: Guaranteed $\Theta(n + m)$ worst case.
    Space Complexity: $\Theta(m)$ for the LPS array.
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return []

    # Helper function to build the LPS array
    def build_lps(p: str) -> list[int]:
        lps = [0] * len(p)
        length = 0 # Length of the previous longest prefix suffix
        i = 1

        while i < len(p):
            if p[i] == p[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    # Fall back to the previous valid prefix
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = build_lps(pattern)
    occurrences = []

    i = 0 # index for text
    j = 0 # index for pattern

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            # Full pattern match found
            occurrences.append(i - j)
            # Use LPS to find the next possible start without backtracking `i`
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            # Mismatch after j matches
            if j != 0:
                # Don't match `lps[0..lps[j-1]]` characters, they will match anyway
                j = lps[j - 1]
            else:
                # First character didn't match, move to next text character
                i += 1

    return occurrences
```

---

## When to Use Which Algorithm

| Algorithm   | Time Complexity      | Space Complexity | Ideal Use Case                               |
| ----------- | -------------------- | ---------------- | -------------------------------------------- |
| Brute Force | $\Theta(n \cdot m)$  | $\Theta(1)$      | Short strings, simple one-off searches       |
| Built-in    | $\Theta(n \cdot m)$* | $\Theta(1)$      | Production code, standard interview use      |
| Rabin-Karp  | $\Theta(n + m)$ avg  | $\Theta(1)$      | Multiple pattern search, plagiarism check    |
| KMP         | $\Theta(n + m)$      | $\Theta(m)$      | Streaming text, guaranteed linear guarantees |

*\* Python's `find()` internally uses highly optimized C-level string search algorithms, usually significantly faster than Python-level loops.*

---

## Template: Find and Replace

In interviews, sometimes you're asked to find a pattern and replace it.

```python
def find_replace(text: str, pattern: str, replacement: str) -> str:
    """
    Preferred interview approach: just use built-ins!
    Time: highly optimized
    Space: $\Theta(N)$ for the new string
    """
    return text.replace(pattern, replacement)

def find_replace_manual(text: str, pattern: str, replacement: str) -> str:
    """
    Manual implementation. Note the use of a list for the result.
    String concatenation via `+=` inside a loop can be $\Theta(N^2)$ in worst cases
    because strings are immutable and must be copied entirely every time.
    Appending to a list and joining at the end is strictly $\Theta(N)$.
    """
    if not pattern:
        return text

    result = []
    i = 0
    n, m = len(text), len(pattern)

    while i < n:
        # Check if window matches pattern
        if text[i:i + m] == pattern:
            result.append(replacement)
            i += m # Skip over the matched pattern
        else:
            result.append(text[i])
            i += 1

    return "".join(result)
```

---

## Advanced: Dynamic Programming String Matching

String matching takes on a new form when wildcards are introduced. We transition from simple pointer matching to 2D Dynamic Programming.

### Problem: Wildcard Matching

**Problem Statement:** Implement wildcard pattern matching with support for `'?'` (matches any single character) and `'*'` (matches any sequence of characters, including the empty sequence).

**Why it works:**
We use a 2D DP table where `dp[i][j]` is `True` if the first `i` characters of the text match the first `j` characters of the pattern.
- The state transition for `*` is the crux: `*` can either represent nothing (so we look at `dp[i][j-1]`), or it can represent the current text character (meaning we "consume" a text character but keep the `*` active for future characters, so we look at `dp[i-1][j]`).

```python
def is_match_wildcard(s: str, p: str) -> bool:
    """
    Time Complexity: $\Theta(m \cdot n)$ where m = len(s), n = len(p)
    Space Complexity: $\Theta(m \cdot n)$ for DP table (can be optimized to $\Theta(n)$)
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]

    # Empty text matches empty pattern
    dp[0][0] = True

    # Initialize first row (empty string `s`)
    # A sequence of '*' at the start of `p` can match an empty `s`
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # '*' acts as empty string (ignore '*') OR '*' consumes `s[i-1]`
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif p[j - 1] == '?' or s[i - 1] == p[j - 1]:
                # Exact match or single wildcard '?'
                dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]
```

### Problem: Regular Expression Matching (Simplified)

**Problem Statement:** Implement regular expression matching with support for `'.'` (matches any single character) and `'*'` (matches **zero or more of the preceding element**).

**Why it works:**
Regex matching is fundamentally harder than Wildcard matching because the `*` is bound to the character immediately preceding it.
- If `p[j-1]` is `*`, the pattern is actually treating the preceding character `p[j-2]` plus the `*` as a single unit.
- This unit can match ZERO occurrences of the preceding char (`dp[i][j-2]`).
- Or, if the preceding character matches the current text character, the unit can match ONE OR MORE occurrences (`dp[i-1][j]`).

```python
def is_match_regex(s: str, p: str) -> bool:
    """
    Time Complexity: $\Theta(m \cdot n)$
    Space Complexity: $\Theta(m \cdot n)$
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Initialize first row (empty string `s`)
    # Patterns like "a*", "a*b*" can match an empty string by evaluating to zero occurrences
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # Option 1: Zero occurrences of preceding char. Ignore `p[j-2]` and `*`.
                dp[i][j] = dp[i][j - 2]

                # Option 2: One or more occurrences.
                # Requires preceding char to match current string char.
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                # Exact match or single wildcard '.'
                dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]
```

---

## Edge Cases to Consider

When solving string matching problems, always check:

- **Empty pattern:** Usually matches at the beginning of any string, or at every position.
- **Empty text:** Handled gracefully if pattern isn't empty (should return `False` or `[]`).
- **Pattern longer than text:** Immediate return `[]` or `False`.
- **Overlapping matches:** Does "aba" in "ababa" occur once or twice? (The algorithms above find both indices: 0 and 2).
- **All identical characters:** `T = "AAAAAAA", P = "AAA"`. Worst case for brute force.

---

## Practice Problems

| #   | Problem | Difficulty | Pattern |
| --- | --- | --- | --- |
| 1   | [Find the Index of the First Occurrence in a String](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) | Easy | Brute Force / KMP |
| 2   | [Repeated Substring Pattern](https://leetcode.com/problems/repeated-substring-pattern/) | Easy | String manipulation |
| 3   | [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/) | Hard | DP |
| 4   | [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) | Hard | DP |
| 5   | [Shortest Palindrome](https://leetcode.com/problems/shortest-palindrome/) | Hard | KMP Prefix Function |
| 6   | [Longest Happy Prefix](https://leetcode.com/problems/longest-happy-prefix/) | Hard | KMP LPS Array |

---

## Key Takeaways

1. **Brute Force is often enough:** For basic interviews, a clean $\Theta(n \cdot m)$ solution using built-ins (`text.find()`) or slicing is often step one.
2. **Rabin-Karp is a Barcode Scanner:** Convert string matching to integer matching via a rolling hash. Understand how to "roll" the hash mathematically in $\Theta(1)$.
3. **KMP is a Smart Jigsaw Puzzle:** It uses a prefix table (LPS) to never re-evaluate a text character it has already seen, guaranteeing $\Theta(n + m)$.
4. **Strings + Wildcards = DP:** When you introduce `*` or `?` modifiers, step away from linear pointers and use a 2D DP table.

---

## Next: [11-anagram-problems.md](./11-anagram-problems.md)

Learn techniques for anagram-related problems.