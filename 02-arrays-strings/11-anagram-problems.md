# Anagram Problems

> **Prerequisites:** [09-string-basics.md](./09-string-basics.md)

## Overview

Anagram problems test your ability to efficiently compare character frequencies. The core insight is that anagrams have identical character counts—once you internalize this, many variations become straightforward applications of hash maps and sliding windows.

## Building Intuition

**Why does character frequency completely define anagrams?**

The key insight is **order-independent equality**:

1. **The Multiset View**: An anagram is a rearrangement. "listen" and "silent" both contain: {e:1, i:1, l:1, n:1, s:1, t:1}. Two words are anagrams if and only if their character multisets are identical.

2. **Hash Map as Canonical Form**: By counting characters, we reduce strings to their "essence." Sorting does the same thing but costs O(n log n); counting costs O(n).

3. **The Sliding Window Connection**: Finding anagrams of pattern P in text T means finding windows where character counts match P. This is a fixed-size sliding window problem with O(1) comparison per window.

**Mental Model**: Think of each string as a bag of lettered tiles (like Scrabble). Two bags are anagrams if they contain exactly the same tiles. You don't care about the order—just count each tile type.

**Why Counting Beats Sorting**:
```
Approach 1: Sort both strings, compare
  Time: O(n log n + m log m)
  Space: O(n + m) for sorted copies

Approach 2: Count characters, compare counts
  Time: O(n + m)
  Space: O(26) = O(1) for lowercase letters

For single anagram check: both work
For finding anagrams in text: counting + sliding window is O(n)
```

**The Count Array Trick**:
```python
# Instead of two hash maps, use one and increment/decrement
count = [0] * 26
for c in s: count[ord(c) - ord('a')] += 1  # Add s's characters
for c in t: count[ord(c) - ord('a')] -= 1  # Remove t's characters

# If all zeros, s and t are anagrams
all(x == 0 for x in count)  # True means anagram
```

## When NOT to Use Anagram Techniques

Anagram patterns have limitations:

1. **Order Matters**: Anagram techniques ignore order. If the problem requires order (e.g., "is s a rotation of t?"), use string concatenation or different techniques.

2. **Approximate Matching**: "Almost anagrams" (differ by at most k characters) require more complex counting or DP.

3. **Non-Character Properties**: If you need to match by word frequency (not character), adapt the technique for word-level counting.

4. **Large Alphabets**: The array trick assumes small alphabet (26 letters). For Unicode or large character sets, use hash maps instead.

5. **Counting Isn't Enough**: Some problems look like anagrams but have additional constraints (e.g., "rearrange into palindrome"—need to check odd-count characters).

**Red Flags:**
- "Rearrange to form X" → May need to check feasibility beyond simple anagram check
- "Approximately equal" → Different technique (edit distance or similar)
- "Subsequence" (not substring/rearrangement) → DP, not anagram counting

---

## Interview Context

Anagram problems test your ability to:

- Use hash tables effectively
- Understand character frequency counting
- Apply sliding window techniques
- Recognize when sorting helps

These problems are very common at FANG+ (especially "Group Anagrams" and "Find All Anagrams").

---

## What is an Anagram?

Two strings are anagrams if they contain the same characters with the same frequencies.

```
"listen" and "silent" → Anagrams ✓
"rat" and "tar" → Anagrams ✓
"hello" and "world" → Not anagrams ✗
```

---

## Template: Valid Anagram

### Problem: Valid Anagram
**Problem Statement:** Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

**Why it works:**
Two strings are anagrams if they have the exact same characters with the same frequencies.
1. We use a frequency map (or a fixed-size array for limited alphabets) to count the occurrences of each character.
2. If the character counts match exactly, the strings are anagrams.
3. This approach is O(n) which is better than sorting (O(n log n)).

```python
def is_anagram(s: str, t: str) -> bool:
    """
    Check if two strings are anagrams.

    Time: O(n)
    Space: O(1) - at most 26 characters for lowercase

    Example:
    "anagram", "nagaram" → True
    "rat", "car" → False
    """
    if len(s) != len(t):
        return False

    from collections import Counter
    return Counter(s) == Counter(t)
```

### Using Array (Faster for Lowercase Letters)

```python
def is_anagram_array(s: str, t: str) -> bool:
    """
    Using array for lowercase letters only.

    Time: O(n)
    Space: O(26) = O(1)
    """
    if len(s) != len(t):
        return False

    count = [0] * 26

    for c in s:
        count[ord(c) - ord('a')] += 1

    for c in t:
        count[ord(c) - ord('a')] -= 1
        if count[ord(c) - ord('a')] < 0:
            return False

    return True
```

### Using Sorting

```python
def is_anagram_sort(s: str, t: str) -> bool:
    """
    Sort and compare.

    Time: O(n log n)
    Space: O(n) - for sorted strings
    """
    return sorted(s) == sorted(t)
```

---

## Template: Group Anagrams

### Problem: Group Anagrams
**Problem Statement:** Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

**Why it works:**
To group anagrams, we need a "canonical" representation of an anagram class that can be used as a hash map key.
1. **Sorting**: Sorting the string (e.g., "eat" → "aet") is a common canonical form.
2. **Frequency Count**: A tuple of character counts (e.g., `(1, 0, ..., 1, ...)` for 'a' and 't') is also a valid key and faster than sorting for long strings.
3. We store the original strings in a hash map where the keys are these canonical forms.

```python
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Group words that are anagrams of each other.

    Time: O(n × k log k) where n = number of strings, k = max string length
    Space: O(n × k)

    Example:
    ["eat", "tea", "tan", "ate", "nat", "bat"]
    → [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    """
    from collections import defaultdict

    groups = defaultdict(list)

    for s in strs:
        # Use sorted string as key
        key = tuple(sorted(s))
        groups[key].append(s)

    return list(groups.values())
```

### Using Character Count as Key

```python
def group_anagrams_count(strs: list[str]) -> list[list[str]]:
    """
    Using character count tuple as key.

    Time: O(n × k) - no sorting!
    Space: O(n × k)
    """
    from collections import defaultdict

    groups = defaultdict(list)

    for s in strs:
        # Count characters and use as key
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        key = tuple(count)
        groups[key].append(s)

    return list(groups.values())
```

---

## Template: Find All Anagrams in a String

### Problem: Find All Anagrams in a String
**Problem Statement:** Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s`.

**Why it works:**
Since the length of an anagram is fixed, we use a fixed-size sliding window of length `len(p)`.
1. We maintain a frequency map for the current window in `s`.
2. As the window moves, we update the map in O(1).
3. We compare the window map to `p`'s map to find matches.
This ensures we find all anagram occurrences in a single O(n) pass.

```python
def find_anagrams(s: str, p: str) -> list[int]:
    """
    Find all start indices of p's anagrams in s.

    Time: O(n) where n = len(s)
    Space: O(1) - constant 26 characters

    Example:
    s = "cbaebabacd", p = "abc"
    → [0, 6]  (substrings "cba" and "bac")
    """
    if len(p) > len(s):
        return []

    result = []
    p_count = [0] * 26
    window_count = [0] * 26

    # Build pattern count
    for c in p:
        p_count[ord(c) - ord('a')] += 1

    k = len(p)

    for i in range(len(s)):
        # Add character to window
        window_count[ord(s[i]) - ord('a')] += 1

        # Remove character leaving window
        if i >= k:
            window_count[ord(s[i - k]) - ord('a')] -= 1

        # Check if window is anagram
        if i >= k - 1 and window_count == p_count:
            result.append(i - k + 1)

    return result
```

### Optimized: Track Matches Instead of Full Comparison

```python
def find_anagrams_optimized(s: str, p: str) -> list[int]:
    """
    Track number of matching character counts.

    Time: O(n)
    Space: O(1)
    """
    if len(p) > len(s):
        return []

    from collections import Counter

    p_count = Counter(p)
    window_count = Counter()

    result = []
    matches = 0  # Number of characters with matching counts
    k = len(p)

    for i in range(len(s)):
        # Add character
        c = s[i]
        if c in p_count:
            if window_count[c] == p_count[c]:
                matches -= 1
            window_count[c] += 1
            if window_count[c] == p_count[c]:
                matches += 1

        # Remove character leaving window
        if i >= k:
            c = s[i - k]
            if c in p_count:
                if window_count[c] == p_count[c]:
                    matches -= 1
                window_count[c] -= 1
                if window_count[c] == p_count[c]:
                    matches += 1

        # Check if all characters match
        if matches == len(p_count):
            result.append(i - k + 1)

    return result
```

---

## Template: Permutation in String

### Problem: Permutation in String
**Problem Statement:** Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise.

**Why it works:**
A permutation of a string is simply an anagram of it.
1. The problem is identical to finding if there's *at least one* anagram of `s1` in `s2`.
2. We use the sliding window frequency count technique.
3. If any window's character count matches `s1`, we return `true`.

```python
def check_inclusion(s1: str, s2: str) -> bool:
    """
    Check if s1's permutation is a substring of s2.
    (Same as checking if any anagram of s1 exists in s2)

    Time: O(n)
    Space: O(1)

    Example:
    s1 = "ab", s2 = "eidbaooo" → True ("ba" is substring)
    s1 = "ab", s2 = "eidboaoo" → False
    """
    if len(s1) > len(s2):
        return False

    s1_count = [0] * 26
    window_count = [0] * 26

    for c in s1:
        s1_count[ord(c) - ord('a')] += 1

    k = len(s1)

    for i in range(len(s2)):
        window_count[ord(s2[i]) - ord('a')] += 1

        if i >= k:
            window_count[ord(s2[i - k]) - ord('a')] -= 1

        if window_count == s1_count:
            return True

    return False
```

---

## Template: Minimum Window Containing Anagram

```python
def min_window_anagram(s: str, p: str) -> str:
    """
    Find minimum window in s that contains an anagram of p.
    (This is essentially same as p itself when found)

    Note: For this problem, window must be exactly len(p).
    """
    anagram_indices = find_anagrams(s, p)
    if anagram_indices:
        return s[anagram_indices[0]:anagram_indices[0] + len(p)]
    return ""
```

---

## Template: Anagram Substring Count

```python
def count_anagram_substrings(s: str, p: str) -> int:
    """
    Count how many substrings of s are anagrams of p.

    Time: O(n)
    Space: O(1)
    """
    return len(find_anagrams(s, p))
```

---

## Template: Scramble String Check

### Problem: Scramble String
**Problem Statement:** Given two strings `s1` and `s2` of the same length, determine if `s2` is a scrambled string of `s1`.

**Why it works:**
Scrambling involves recursively splitting the string and optionally swapping the two halves.
1. Two strings can only be scrambles if they are anagrams.
2. We use recursion with memoization to check all possible split points.
3. For each split, we check if the halves match (without swap) or match after a swap.
Anagram checking is used here as an "early exit" optimization for the recursion.

```python
def is_scramble(s1: str, s2: str) -> bool:
    """
    Check if s2 is a scrambled version of s1.
    (Can recursively swap non-empty substrings)

    This is more complex than anagram - uses DP/memoization.

    Time: O(n⁴)
    Space: O(n³)
    """
    from functools import lru_cache

    if len(s1) != len(s2):
        return False

    @lru_cache(maxsize=None)
    def helper(str1: str, str2: str) -> bool:
        if str1 == str2:
            return True
        if sorted(str1) != sorted(str2):
            return False

        n = len(str1)
        for i in range(1, n):
            # No swap: left with left, right with right
            if helper(str1[:i], str2[:i]) and helper(str1[i:], str2[i:]):
                return True
            # Swap: left with right, right with left
            if helper(str1[:i], str2[n-i:]) and helper(str1[i:], str2[:n-i]):
                return True

        return False

    return helper(s1, s2)
```

---

## Common Patterns Summary

| Problem Type | Technique | Key |
|--------------|-----------|-----|
| Check if anagram | Counter/Array | Compare counts |
| Group anagrams | HashMap | Sorted string or count tuple as key |
| Find anagram in string | Sliding window | Fixed size window |
| Multiple anagram search | Sliding window | Track matches |

---

## Edge Cases

```python
# Empty strings
"", "" → True (both are empty anagrams)
"a", "" → False (different lengths)

# Single character
"a", "a" → True
"a", "b" → False

# Same string
"hello", "hello" → True

# Different lengths
Any strings with different lengths → False

# Unicode/special characters
Handle based on problem constraints
Usually limited to lowercase a-z in interviews
```

---

## Practice Problems

| # | Problem | Difficulty | Key Technique |
|---|---------|------------|---------------|
| 1 | Valid Anagram | Easy | Character count |
| 2 | Group Anagrams | Medium | HashMap with key |
| 3 | Find All Anagrams in a String | Medium | Sliding window |
| 4 | Permutation in String | Medium | Sliding window |
| 5 | Minimum Number of Steps to Make Anagram | Medium | Count difference |
| 6 | Smallest Range Covering K Lists | Hard | Uses anagram concepts |
| 7 | Scramble String | Hard | DP with memoization |

---

## Key Takeaways

1. **Character count is the essence** of anagram checking
2. **Use array `[0]*26`** for lowercase letters (faster than dict)
3. **Sorted string or count tuple** as key for grouping
4. **Sliding window** for finding anagrams in text
5. **Track match count** for optimization over full comparison

---

## Next: [12-palindrome-strings.md](./12-palindrome-strings.md)

Learn palindrome checking, expansion, and construction techniques.
