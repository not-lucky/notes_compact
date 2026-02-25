# Anagram Problems

> **Prerequisites:** [09-string-basics.md](./09-string-basics.md)

## Overview

Anagram problems test your ability to efficiently compare character frequencies. The core insight is that anagrams have identical character counts—once you internalize this, many variations become straightforward applications of hash maps and sliding windows.

## Building Intuition

**Why does character frequency completely define anagrams?**

The key insight is **order-independent equality**:

1. **The Multiset View**: An anagram is a rearrangement. "listen" and "silent" both contain: `{e:1, i:1, l:1, n:1, s:1, t:1}`. Two words are anagrams if and only if their character multisets are identical.
2. **Hash Map as Canonical Form**: By counting characters, we reduce strings to their "essence." Sorting does the same thing but costs $\Theta(n \log n)$; counting costs $\Theta(n)$.
3. **The Sliding Window Connection**: Finding anagrams of a pattern $P$ in text $T$ means finding windows where character counts match $P$. This is a fixed-size sliding window problem with $\Theta(1)$ comparison per window (since the alphabet size is constant).

**Mental Model**: Think of each string as a bag of lettered tiles (like Scrabble). Two bags are anagrams if they contain exactly the same tiles. You don't care about the order the tiles were pulled out—just count each tile type. When you need a "canonical" representation (like a key in a hash map), sorting the tiles is like organizing them alphabetically before putting them on a shelf, whereas counting them is like filling out an inventory sheet.

**Why Counting Beats Sorting**:

```text
Approach 1: Sort both strings, compare
  Time: Θ(n log n + m log m) (tightest bound for general comparison sorting)
  Space: Θ(n + m) for sorted copies (strings are immutable in Python)

Approach 2: Count characters, compare counts
  Time: Θ(n + m)
  Space: Θ(k) where k is alphabet size. For lowercase English letters, Θ(26) = Θ(1)
```

**The Count Array Trick**:

For small, fixed alphabets (like lowercase English letters), a fixed-size array is faster than a hash map and avoids hash collision edge cases.

```python
# Instead of two hash maps, use one list (dynamic array) and increment/decrement
count = [0] * 26
for c in s: count[ord(c) - ord('a')] += 1  # Add s's characters
for c in t: count[ord(c) - ord('a')] -= 1  # Remove t's characters

# If all zeros, s and t are anagrams
is_anagram = all(x == 0 for x in count)
```

## When NOT to Use Anagram Techniques

Anagram patterns have limitations:

1. **Order Matters**: Anagram techniques ignore order. If the problem requires order (e.g., "is s a rotation of t?"), use string concatenation or other techniques.
2. **Approximate Matching**: "Almost anagrams" (differ by at most $k$ characters) require more complex counting or dynamic programming.
3. **Non-Character Properties**: If you need to match by word frequency (not character), adapt the technique for word-level counting (using actual hash maps since the "alphabet" of words is unbounded).
4. **Large Alphabets**: The array trick assumes a small alphabet (26 letters). For full Unicode or large character sets, use hash maps instead, noting that hash map operations are amortized $\Theta(1)$ but $\Theta(n)$ worst-case.
5. **Counting Isn't Enough**: Some problems look like anagrams but have additional constraints (e.g., "rearrange into palindrome"—you need to check for at most one odd-count character, not just identical counts).

**Red Flags:**

- "Rearrange to form X" → May need to check feasibility beyond a simple anagram check.
- "Approximately equal" → Different technique (edit distance or similar).
- "Subsequence" (not substring/rearrangement) → Dynamic Programming or two pointers, not anagram counting.

---

## Interview Context

Anagram problems test your ability to:

- Use hash tables effectively (and understand their amortized vs. worst-case bounds).
- Understand character frequency counting.
- Apply sliding window techniques.
- Recognize when sorting helps vs. when counting is optimal.

These problems are very common at FANG+ (especially "Group Anagrams" and "Find All Anagrams").

---

## What is an Anagram?

Two strings are anagrams if they contain the exact same characters with the same frequencies.

```text
"listen" and "silent" → Anagrams ✓
"rat" and "tar"       → Anagrams ✓
"hello" and "world"   → Not anagrams ✗
```

---

## Template: Valid Anagram

### Problem: Valid Anagram
**Problem Statement:** Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise.

**Why it works:**
Two strings are anagrams if they have the exact same characters with the same frequencies.
1. We use a frequency map (or a fixed-size array for limited alphabets) to count the occurrences of each character.
2. If the character counts match exactly, the strings are anagrams.
3. This approach is $\Theta(n)$ time, which is strictly better than the $\Theta(n \log n)$ required for sorting.

```python
from collections import Counter

def is_anagram(s: str, t: str) -> bool:
    """
    Check if two strings are anagrams using Python's Counter.

    Time: Θ(n + m) where n, m are string lengths. Counter creation takes linear time.
          Comparison is Θ(k) where k is the number of unique characters.
    Space: Θ(k) where k is the number of unique characters.
           For ASCII, this is bounded by Θ(128) = Θ(1).
           Note: Counter operations are amortized Θ(1) due to underlying hash map.
    """
    if len(s) != len(t):
        return False

    # Counter compares dict keys and values
    return Counter(s) == Counter(t)
```

### Using Array (Faster for Lowercase Letters)

When the character set is restricted (e.g., only lowercase English letters), a fixed-size array avoids the overhead of hashing entirely. It is strictly $\Theta(1)$ for updates, whereas a hash map is *amortized* $\Theta(1)$ and worst-case $\Theta(n)$ on collisions.

```python
def is_anagram_array(s: str, t: str) -> bool:
    """
    Using array for lowercase letters only.

    Time: Θ(n) where n is len(s)
    Space: Θ(26) = Θ(1)
    """
    if len(s) != len(t):
        return False

    # Python lists are dynamic arrays. Initializing with [0] * 26 is Θ(1)
    count: list[int] = [0] * 26

    for c in s:
        count[ord(c) - ord('a')] += 1

    for c in t:
        idx = ord(c) - ord('a')
        count[idx] -= 1
        # Early exit if a character count goes negative
        if count[idx] < 0:
            return False

    # If lengths are equal and no count went negative, all must be zero
    return True
```

### Using Sorting

```python
def is_anagram_sort(s: str, t: str) -> bool:
    """
    Sort and compare.

    Time: Θ(n log n)
    Space: Θ(n) - sorted() creates a new list in Python
    """
    return sorted(s) == sorted(t)
```

---

## Template: Group Anagrams

### Problem: Group Anagrams
**Problem Statement:** Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

**Why it works:**
To group anagrams, we need a "canonical" representation of an anagram class that can be used as a hash map key.
1. **Sorting**: Sorting the string (e.g., `"eat"` → `"aet"`) is a common canonical form. It acts as our "inventory sheet."
2. **Frequency Count**: A tuple of character counts (e.g., `(1, 0, ..., 1, ...)` for 'a' and 't') is also a valid key and faster than sorting for long strings. Tuples are required because Python dict keys must be hashable (immutable).
3. We store the original strings in a hash map where the keys are these canonical forms.

```python
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Group words that are anagrams of each other.

    Time: Θ(n × k log k) where n = number of strings, k = max string length.
          Sorting each string takes Θ(k log k).
    Space: Θ(n × k) to store the result and the hash map.
           Note: Hash map insertion is amortized Θ(1).
    """
    groups: dict[tuple[str, ...], list[str]] = defaultdict(list)

    for s in strs:
        # Use sorted string (converted to tuple) as the canonical key
        key = tuple(sorted(s))
        groups[key].append(s)

    return list(groups.values())
```

### Using Character Count as Key

```python
from collections import defaultdict

def group_anagrams_count(strs: list[str]) -> list[list[str]]:
    """
    Using character count tuple as key.

    Time: Θ(n × k) - no sorting! We process each character of each string once.
    Space: Θ(n × k) to store the grouped strings. The keys are bounded to length 26.
    """
    groups: dict[tuple[int, ...], list[str]] = defaultdict(list)

    for s in strs:
        # Count characters and use as key
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1

        # Lists are unhashable, must convert to tuple for dict key
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
1. We maintain a frequency map (or array) for the current window in `s`.
2. As the window moves, we update the map in $\Theta(1)$ by adding the new character and removing the old one.
3. We compare the window map to `p`'s map to find matches. Array equality in Python (`list1 == list2`) compares elements pairwise, which takes $\Theta(26) = \Theta(1)$ for a fixed alphabet.
This ensures we find all anagram occurrences in a single $\Theta(n)$ pass.

```python
def find_anagrams(s: str, p: str) -> list[int]:
    """
    Find all start indices of p's anagrams in s.

    Time: Θ(n) where n = len(s)
          Comparing two arrays of size 26 is Θ(1).
    Space: Θ(1) - constant 26 characters for the arrays.
           (Excluding the result array which could be O(n)).
    """
    if len(p) > len(s):
        return []

    result: list[int] = []
    p_count = [0] * 26
    window_count = [0] * 26

    # Build pattern count
    for c in p:
        p_count[ord(c) - ord('a')] += 1

    k = len(p)

    for i in range(len(s)):
        # Add new character to window
        window_count[ord(s[i]) - ord('a')] += 1

        # Remove character that falls out of the window
        if i >= k:
            window_count[ord(s[i - k]) - ord('a')] -= 1

        # Check if window is an anagram (array comparison is Θ(26) -> Θ(1))
        if i >= k - 1 and window_count == p_count:
            result.append(i - k + 1)

    return result
```

### Optimized: Track Matches Instead of Full Comparison

Instead of comparing the full 26-element array every step, we can track the number of characters whose counts match perfectly.

```python
from collections import Counter

def find_anagrams_optimized(s: str, p: str) -> list[int]:
    """
    Track number of matching character counts.

    Time: Θ(n)
    Space: Θ(k) where k is unique characters in p (bounded by Θ(1) for fixed alphabet)
    """
    if len(p) > len(s):
        return []

    p_count = Counter(p)
    window_count: Counter[str] = Counter()

    result: list[int] = []
    matches = 0  # Number of characters with perfectly matching frequencies
    required_matches = len(p_count)
    k = len(p)

    for i in range(len(s)):
        # Add character
        c = s[i]
        if c in p_count:
            if window_count[c] == p_count[c]:
                matches -= 1 # It was matching, now it won't be
            window_count[c] += 1
            if window_count[c] == p_count[c]:
                matches += 1 # Now it matches

        # Remove character leaving window
        if i >= k:
            c_remove = s[i - k]
            if c_remove in p_count:
                if window_count[c_remove] == p_count[c_remove]:
                    matches -= 1
                window_count[c_remove] -= 1
                if window_count[c_remove] == p_count[c_remove]:
                    matches += 1

        # If all characters have matching frequencies, it's an anagram
        if matches == required_matches:
            result.append(i - k + 1)

    return result
```

---

## Template: Permutation in String

### Problem: Permutation in String
**Problem Statement:** Given two strings `s1` and `s2`, return `True` if `s2` contains a permutation of `s1`, or `False` otherwise.

**Why it works:**
A permutation of a string is simply an anagram of it.
1. The problem is identical to finding if there's *at least one* anagram of `s1` in `s2`.
2. We use the sliding window frequency count technique.
3. If any window's character count matches `s1`, we return `True`.

```python
def check_inclusion(s1: str, s2: str) -> bool:
    """
    Check if s1's permutation is a substring of s2.
    (Same as checking if any anagram of s1 exists in s2)

    Time: Θ(n) where n = len(s2)
    Space: Θ(1)
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
    (This is essentially the same as p itself when found)

    Note: For this specific constraint, the window must be exactly len(p).
    If the problem is "minimum window containing all characters of p",
    that is a variable-length sliding window problem, not a pure anagram problem.
    """
    anagram_indices = find_anagrams(s, p)
    if anagram_indices:
        return s[anagram_indices[0]:anagram_indices[0] + len(p)]
    return ""
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

**Python String Concatenation/Slicing Note**: String slicing creates *new* strings in Python, taking $\Theta(k)$ time where $k$ is the slice length.

```python
from functools import lru_cache

def is_scramble(s1: str, s2: str) -> bool:
    """
    Check if s2 is a scrambled version of s1.
    (Can recursively swap non-empty substrings)

    Time: O(n⁴) without anagram check optimization, realistically much faster with it.
          The memoization table has O(n²) states, and each state tries O(n) splits.
          String slicing takes O(n) per split.
    Space: O(n³) for the memoization cache (O(n²) states, storing strings of length O(n)).
           The recursion call stack adds an additional O(n) depth.
    """
    if len(s1) != len(s2):
        return False

    @lru_cache(maxsize=None)
    def helper(str1: str, str2: str) -> bool:
        if str1 == str2:
            return True

        # Early exit: if they aren't anagrams, they can't be scrambles.
        # This prunes massive branches of the recursion tree.
        if sorted(str1) != sorted(str2):
            return False

        n = len(str1)
        # Try splitting at every possible index
        for i in range(1, n):
            # Option 1: No swap (left matches left, right matches right)
            if helper(str1[:i], str2[:i]) and helper(str1[i:], str2[i:]):
                return True

            # Option 2: Swap (left matches right, right matches left)
            if helper(str1[:i], str2[n-i:]) and helper(str1[i:], str2[:n-i]):
                return True

        return False

    return helper(s1, s2)
```

---

## Common Patterns Summary

| Problem Type | Technique | Key Idea |
| :--- | :--- | :--- |
| Check if anagram | Array / Counter | Compare character counts; $\Theta(1)$ space for fixed alphabet. |
| Group anagrams | HashMap | Canonical representation (sorted string or count tuple) as dict key. |
| Find anagram in string | Fixed Sliding Window | Maintain window frequency map, compare with pattern map. |
| Multiple anagram search | Sliding Window Tracking | Track `matches` variable to avoid full array comparison every step. |

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
# Any strings with different lengths → False (always check length first!)

# Unicode/special characters
# Cannot use [0] * 26 array trick. Must use dict/Counter or larger array.
# Note that hash map operations become amortized Θ(1), worst-case Θ(n).
```

---

## Practice Problems

| # | Problem | Difficulty | Key Technique |
| :--- | :--- | :--- | :--- |
| 1 | Valid Anagram | Easy | Character count / Array mapping |
| 2 | Group Anagrams | Medium | HashMap with count tuple / sorted string key |
| 3 | Find All Anagrams in a String | Medium | Fixed-size sliding window |
| 4 | Permutation in String | Medium | Fixed-size sliding window |
| 5 | Minimum Number of Steps to Make Anagram | Medium | Count difference between frequency maps |
| 6 | Smallest Range Covering K Lists | Hard | Uses similar counting frequency concepts |
| 7 | Scramble String | Hard | DP / Recursion + Memoization with anagram pruning |

---

## Key Takeaways

1. **Character count is the essence** of anagram checking. Think of words as bags of Scrabble tiles.
2. **Use a fixed array `[0]*26`** for lowercase English letters (faster than dict, strict $\Theta(1)$ updates).
3. **Use a count tuple** or **sorted string** as the key for grouping anagrams. (Tuples are hashable in Python).
4. **Fixed-size sliding window** is the go-to pattern for finding anagrams within a larger text.
5. Always address **amortized vs. worst-case** when discussing hash maps in interviews.

---

## Next: [12-palindrome-strings.md](./12-palindrome-strings.md)

Learn palindrome checking, expansion, and construction techniques.