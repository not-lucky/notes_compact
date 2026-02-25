# Palindrome Strings

> **Prerequisites:** [09-string-basics.md](./09-string-basics.md)

## Overview

Palindrome problems exploit the symmetry of strings that read the same forwards and backwards. The two key techniques are two-pointer checking and expand-from-center search—together they solve most palindrome interview problems efficiently.

## Building Intuition

**Why do palindromes lend themselves to these specific techniques?**

The key insight is **symmetry enables comparison reduction**:

1. **Two-Pointer Symmetry Check**: A palindrome is symmetric around its center. If outer characters match, the inner substring determines palindrome-ness. We only need to check half the string, reducing unnecessary comparisons.
2. **Expand From Center**: There are only $2n-1$ possible centers ($n$ odd centers at characters, $n-1$ even centers between characters). From each center, expand outward while characters match. This limits our search space significantly.
3. **DP for Substrings**: If `s[i:j]` is a palindrome and `s[i-1] == s[j+1]`, then `s[i-1:j+2]` is also a palindrome. This "if inner is palindrome AND outer chars match" pattern creates overlapping subproblems—perfect for Dynamic Programming.

### Physical Metaphors

- **Two Pointers (Checking): Folding Paper**
  Imagine folding a piece of paper in half. For the text to be a palindrome, the letters on the left half must perfectly align and map to the letters on the right half, all the way to the center crease.

- **Expand From Center (Finding): Ripples in a Pond**
  Imagine dropping a pebble into perfectly still water. The ripples expand outward symmetrically. To find a palindrome, you pick a center (drop a pebble) and let the "ripples" expand outward character by character as long as the symmetry holds.

- **Valid Palindrome II (One Mistake Allowed): The Smeared Mirror**
  You're checking a nearly-perfect mirror. If you find one mismatched reflection (a smudge), you get one chance to wipe either the left or right side. You try wiping the left—if it works, great. If not, try wiping the right.

### Why Expand From Center Works

```text
For each center position, expand outward while s[left] == s[right]

String: "babad"
        01234

Center 0 ('b'): "b" (length 1)
Center 1 ('a'): expand → "bab" (length 3) ← found palindrome
Center 2 ('b'): expand → "aba" (length 3) ← found palindrome
Center 3 ('a'): "a" (length 1)
Center 4 ('d'): "d" (length 1)

Also check even-length centers (between characters):
Center 0.5: s[0]='b' ≠ s[1]='a' → no even palindrome
...

Maximum length: 3, palindromes: "bab" or "aba"
```

## When NOT to Use Standard Palindrome Techniques

These techniques have specific scopes:

1. **Longest Palindromic Subsequence (not Substring)**: Subsequence allows gaps—"bbbab" has LPS "bbbb" (skipping 'a'). This is DP on two indices, not expand-from-center.
2. **Count All Palindromes in Massive String**: $O(n^2)$ expand-from-center may be too slow for $n > 10^6$. Manacher's algorithm achieves $\Theta(n)$ but is rarely expected in interviews.
3. **Construct Palindrome by Modification**: "Minimum insertions to make palindrome" is LCS-based DP, not direct palindrome checking.
4. **Numeric Palindromes**: Integer palindromes (121, 1221) should be checked by reversing the number mathematically (e.g., using modulo and division) or comparing digits—string conversion works but uses extra space and is typically frowned upon as a "shortcut".
5. **Palindrome Partitioning**: "Partition into minimum palindromes" or "all palindrome partitions" needs DP or backtracking, not just checking.

**Red Flags:**

- "Subsequence" (not substring) → 2D DP
- "Minimum insertions/deletions" → LCS-related DP
- "Partition into palindromes" → Backtracking or interval DP
- Constraints $n > 10^5$ for all palindromic substrings → Manacher's algorithm

---

## Interview Context

Palindrome problems are interview favorites because they:

- Test string manipulation skills
- Have multiple solution approaches (two pointers, DP, expand from center)
- Scale from easy to hard difficulty
- Appear in both array and string contexts

Key problems: Valid Palindrome, Longest Palindromic Substring, Palindrome Partitioning.

---

## What is a Palindrome?

A string that reads the same forwards and backwards.

```text
"racecar" → Palindrome ✓
"madam" → Palindrome ✓
"hello" → Not a palindrome ✗
"a" → Palindrome ✓ (single character)
"" → Palindrome ✓ (empty string)
```

---

## Template: Check Palindrome (Two Pointers)

### Problem: Palindrome Check
**Problem Statement:** Determine if a string is a palindrome.

**Why it works:**
A palindrome is symmetric around its center.
1. By comparing the character at the `left` index with the character at the `right` index and moving them inward, we verify the symmetry.
2. If all pairs match until the pointers meet, the string is a palindrome.

```python
def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome.

    Time: O(n) - We check at most n/2 characters. Worst-case tight bound is Θ(n),
                 best case is Θ(1) (mismatch at the very edges).
    Space: Θ(1) - Only two integer pointers.
    """
    left, right = 0, len(s) - 1

    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1

    return True
```

### One-Liner (Less Efficient)

```python
def is_palindrome_slice(s: str) -> bool:
    """
    Time: Θ(n)
    Space: Θ(n) - Creates reversed copy of the string in memory.
    """
    return s == s[::-1]
```

---

## Template: Valid Palindrome (Alphanumeric Only)

### Problem: Valid Palindrome
**Problem Statement:** Check if a string is a palindrome, ignoring non-alphanumeric characters and case.

**Why it works:**
This is the same logic as the basic check but with a "filtering" step.
1. We move pointers as usual but skip any character that isn't `isalnum()`.
2. We use `lower()` to ensure case-insensitive comparison.
This avoids the need for a separate pre-processing step (like creating a new filtered string) that would require $\Theta(n)$ extra space.

```python
def is_palindrome_alphanum(s: str) -> bool:
    """
    Check palindrome ignoring non-alphanumeric characters and case.

    Time: O(n) - Single pass through the string. Worst-case tight bound is Θ(n).
    Space: Θ(1) - Constant extra space used for pointers.

    Example:
    "A man, a plan, a canal: Panama" → True
    "race a car" → False
    """
    left, right = 0, len(s) - 1

    while left < right:
        # Skip non-alphanumeric from left
        while left < right and not s[left].isalnum():
            left += 1

        # Skip non-alphanumeric from right
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

---

## Template: Valid Palindrome II (Remove at Most One)

### Problem: Valid Palindrome II
**Problem Statement:** Given a string `s`, return `True` if `s` can be a palindrome after deleting at most one character from it.

**Why it works:**
1. We start a normal palindrome check from both ends.
2. When we encounter a mismatch `s[left] != s[right]`, we have two options to fix it: remove the `left` character or remove the `right` character.
3. We check if the remaining substring `s[left+1 : right+1]` OR `s[left : right]` is a palindrome.
Since we only get one "skip", this remains an $O(n)$ time complexity solution.

```python
def valid_palindrome_ii(s: str) -> bool:
    """
    Check if string can be a palindrome by removing at most one character.

    Time: O(n) - The helper is called at most twice, checking remaining characters.
                 Worst-case tight bound is Θ(n).
    Space: Θ(1) - Slices are avoided by passing index bounds to the helper.
                  (Using slices would make space Θ(n)).

    Example:
    "aba" → True
    "abca" → True (remove 'c')
    "abc" → False
    """
    def is_palindrome_range(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1

    while left < right:
        if s[left] != s[right]:
            # Try removing either the left character or the right character
            return (is_palindrome_range(left + 1, right) or
                    is_palindrome_range(left, right - 1))
        left += 1
        right -= 1

    return True
```

---

## Template: Longest Palindromic Substring (Expand from Center)

### Problem: Longest Palindromic Substring
**Problem Statement:** Given a string `s`, return the longest palindromic substring in `s`.

**Why it works:**
A palindrome can be centered at a single character (odd length) or between two characters (even length).
1. There are `2n-1` such centers.
2. For each center, we expand outward as long as the characters match.
3. We keep track of the maximum length palindrome found.
This approach uses $\Theta(1)$ extra space, making it better than a Dynamic Programming solution that uses $\Theta(n^2)$ space.

```python
def longest_palindrome(s: str) -> str:
    """
    Find the longest palindromic substring using Expand From Center.

    Time: O(n²) - Expand around 2n-1 centers. Worst-case tight bound is Θ(n²)
                  for strings like "aaaa". Best case is Θ(n) for distinct chars like "abcd".
    Space: Θ(1) - Only keeping track of boundary indices.

    Example:
    "babad" → "bab" or "aba"
    "cbbd" → "bb"
    """
    if not s:
        return ""

    def expand_from_center(left: int, right: int) -> tuple[int, int]:
        """Expand symmetrically and return the valid palindrome boundaries."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # The loop terminates when a mismatch occurs or boundaries are crossed.
        # The valid palindrome is strictly inside (left, right).
        return left + 1, right - 1

    start, end = 0, 0

    for i in range(len(s)):
        # Odd length palindrome (single character center)
        left1, right1 = expand_from_center(i, i)
        if right1 - left1 > end - start:
            start, end = left1, right1

        # Even length palindrome (between two characters)
        left2, right2 = expand_from_center(i, i + 1)
        if right2 - left2 > end - start:
            start, end = left2, right2

    return s[start:end + 1]
```
*(Note: Returning indices from the helper avoids creating $O(n^2)$ substring slices during the process, strictly maintaining $\Theta(1)$ auxiliary space).*

---

## Template: Longest Palindromic Substring (DP)

```python
def longest_palindrome_dp(s: str) -> str:
    """
    Find longest palindromic substring using Dynamic Programming.
    dp[i][j] = True if s[i:j+1] is a palindrome.

    Time: Θ(n²) - We must fill out roughly half the n x n grid.
    Space: Θ(n²) - Storing the 2D boolean grid.

    Note: This is generally considered inferior to Expand From Center due to Θ(n²) space.
    """
    n = len(s)
    if n < 2:
        return s

    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1

    # Base case 1: All single characters are palindromes
    for i in range(n):
        dp[i][i] = True

    # Base case 2: Check for length 2 substrings
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start = i
            max_len = 2

    # DP for lengths >= 3
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            # s[i:j+1] is a palindrome if outer characters match
            # AND the inner substring s[i+1:j] is a palindrome.
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                start = i
                max_len = length

    return s[start:start + max_len]
```

---

## Template: Count Palindromic Substrings

### Problem: Palindromic Substrings
**Problem Statement:** Given a string `s`, return the number of palindromic substrings in it.

**Why it works:**
This uses the same "Expand from Center" technique.
1. Each time we successfully expand from a center, we've found one more palindromic substring.
2. By summing the number of successful expansions from all `2n-1` centers, we get the total count.

```python
def count_substrings(s: str) -> int:
    """
    Count all palindromic substrings.

    Time: O(n²) - Expand around 2n-1 centers. Worst-case tight bound is Θ(n²), best case is Θ(n).
    Space: Θ(1) - Only scalar variables used.

    Example:
    "abc" → 3 ("a", "b", "c")
    "aaa" → 6 ("a"×3, "aa"×2, "aaa"×1)
    """
    count = 0

    def expand(left: int, right: int) -> int:
        """Count valid palindromes expanding from a given center."""
        cnt = 0
        while left >= 0 and right < len(s) and s[left] == s[right]:
            cnt += 1
            left -= 1
            right += 1
        return cnt

    for i in range(len(s)):
        count += expand(i, i)      # Odd length centers
        count += expand(i, i + 1)  # Even length centers

    return count
```

---

## Template: Longest Palindromic Subsequence (DP)

### Problem: Longest Palindromic Subsequence
**Problem Statement:** Given a string `s`, find the longest palindromic subsequence's length in `s`.

**Why it works:**
A subsequence doesn't have to be contiguous.
1. We use DP where `dp[i][j]` is the longest palindromic subsequence in `s[i:j+1]`.
2. If `s[i] == s[j]`, the `LPS` is `2 + LPS of the inner part s[i+1 : j-1]`.
3. If they don't match, the `LPS` is the maximum of `LPS` excluding the left char OR the right char.
The state transitions systematically explore the best palindromic structure within the string.

```python
def longest_palindrome_subseq(s: str) -> int:
    """
    Find length of longest palindromic SUBSEQUENCE (not substring).
    Subsequence doesn't need to be contiguous.

    Time: Θ(n²) - We process every state in the DP table.
    Space: Θ(n²) - 2D DP array. Can be optimized to Θ(n) using 1D row swapping.

    Example:
    "bbbab" → 4 ("bbbb")
    "cbbd" → 2 ("bb")
    """
    n = len(s)
    # dp[i][j] = longest palindromic subsequence in s[i:j+1]
    dp = [[0] * n for _ in range(n)]

    # Single characters are palindromes of length 1
    for i in range(n):
        dp[i][i] = 1

    # Fill by increasing length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]
```

---

## Template: Palindrome Partitioning

### Problem: Palindrome Partitioning
**Problem Statement:** Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of `s`.

**Why it works:**
This is a backtracking problem.
1. At each step, we try all possible prefixes of the current string.
2. If a prefix is a palindrome, we add it to our path and recursively partition the remaining string.
3. If we reach the end of the string, the current path is a valid partitioning.
This finds all ways to split the string into palindromes.

```python
def partition(s: str) -> list[list[str]]:
    """
    Partition s such that every substring is a palindrome.
    Return all possible partitions.

    Time: O(n * 2^n) - In the worst case ("aaaa"), there are 2^(n-1) partitions.
          Constructing each path takes O(n). Worst-case tight bound is Θ(n * 2^n).
    Space: O(n) - Recursive call stack depth is at most n (excluding the output array).

    Example:
    "aab" → [["a", "a", "b"], ["aa", "b"]]
    """
    result = []

    def is_palindrome(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    def backtrack(start: int, path: list[str]) -> None:
        if start == len(s):
            # Reached end of string, valid partition found
            result.append(path[:])
            return

        for end in range(start + 1, len(s) + 1):
            if is_palindrome(start, end - 1):
                path.append(s[start:end])
                backtrack(end, path)
                path.pop()  # Backtrack

    backtrack(0, [])
    return result
```

---

## Template: Minimum Cuts for Palindrome Partitioning

```python
def min_cut(s: str) -> int:
    """
    Find minimum cuts needed to partition a string into valid palindromes.

    Time: Θ(n²) - One pass to build the boolean palindrome DP table,
          and a second nested loop to compute min cuts.
    Space: Θ(n²) - The is_palindrome table requires an n x n boolean matrix.

    Example:
    "aab" → 1 (cut: "aa" | "b")
    """
    n = len(s)

    # is_palindrome[i][j] = True if s[i:j+1] is a palindrome
    is_palindrome = [[False] * n for _ in range(n)]

    # We build the DP table bottom-up and left-to-right to ensure dependencies are met
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_palindrome[i + 1][j - 1]):
                is_palindrome[i][j] = True

    # dp[i] = min cuts for substring s[0:i+1]
    dp = [0] * n

    for i in range(n):
        if is_palindrome[0][i]:
            dp[i] = 0  # No cut needed if the whole prefix is a palindrome
        else:
            dp[i] = i  # Worst case: cut before every character
            for j in range(1, i + 1):
                if is_palindrome[j][i]:
                    dp[i] = min(dp[i], dp[j - 1] + 1)

    return dp[n - 1]
```

---

## Template: Make Palindrome by Inserting Characters

```python
def min_insertions(s: str) -> int:
    """
    Find minimum insertions to make a string into a palindrome.
    Insight: We only need to insert characters for the ones that don't match.
    Minimum Insertions = Total Length - Longest Palindromic Subsequence (LPS).

    Time: Θ(n²) - Building the LPS table requires checking all i,j pairs.
    Space: Θ(n²) - DP table for LPS (optimizable to Θ(n) space using 2 rows).

    Example:
    "zzazz" → 0 (already palindrome)
    "mbadm" → 2 (insert 'b' and 'a' → "mbdadbm")
    """
    n = len(s)
    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    lps = dp[0][n - 1]
    return n - lps
```

---

## Edge Cases

```python
# Empty string
"" → True (palindrome), LPS = 0

# Single character
"a" → True, LPS = 1

# All same characters
"aaaa" → True, LPS = 4

# No palindrome > 1
"abcd" → LPS = 1

# Even vs odd length
"abba" (even), "aba" (odd)
```

---

## Practice Problems

| #   | Problem                         | Difficulty | Technique               |
| --- | ------------------------------- | ---------- | ----------------------- |
| 1   | Valid Palindrome                | Easy       | Two pointers            |
| 2   | Valid Palindrome II             | Easy       | Two pointers + try both |
| 3   | Longest Palindromic Substring   | Medium     | Expand from center      |
| 4   | Palindromic Substrings          | Medium     | Count with expansion    |
| 5   | Longest Palindromic Subsequence | Medium     | DP                      |
| 6   | Palindrome Partitioning         | Medium     | Backtracking            |
| 7   | Palindrome Partitioning II      | Hard       | DP min cuts             |
| 8   | Shortest Palindrome             | Hard       | KMP/hashing             |

---

## Key Takeaways

1. **Two pointers** for basic palindrome check
2. **Expand from center** for finding palindromic substrings
3. **DP[i][j]** for substring/subsequence problems
4. **Odd and even** centers both need checking
5. **LPS** (subsequence) ≠ longest palindromic substring

---

## Next: [13-matrix-traversal.md](./13-matrix-traversal.md)

Learn matrix traversal patterns: spiral, diagonal, and search.
