# Anagram Grouping

> **Prerequisites:** [03-frequency-counting.md](./03-frequency-counting.md)

## Interview Context

Anagram problems test your ability to create **canonical representations** of strings that identify groups. They appear as:

- Direct anagram checks and grouping
- Substring anagram finding (sliding window)
- Permutation matching problems

The key insight: anagrams share the same **sorted string** or **character frequency signature**.

**Interview frequency**: High. Group Anagrams is a FAANG favorite.

---

## Building Intuition

**The Core Insight: Canonical Representation**

The key question: "How do we identify that two strings are anagrams?"

Answer: Transform them into the same **canonical form** (signature).

```
"listen" → signature → "eilnst" (sorted)
"silent" → signature → "eilnst" (sorted)

Same signature = Same anagram group!
```

**Two Signature Strategies**

1. **Sorted String**: Simple, works for any characters
   - `"listen"` → `"".join(sorted("listen"))` → `"eilnst"`
   - Time: $O(k \log k)$ per string of length $k$

2. **Count Tuple**: Faster for fixed alphabet (e.g., lowercase English)
   - `"listen"` → `(0,0,0,0,1,0,0,0,1,0,0,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0)`
   - Time: $O(k)$ per string of length $k$

**Mental Model: The Signature as a "Name Tag"**

Imagine a party where everyone wearing the same "name tag" is grouped together:

- Instead of comparing everyone to everyone (O(n²))
- Give each person a name tag based on their letters
- People with matching name tags go to the same table

The hashmap groups by name tag in $O(1)$ amortized per lookup/insertion.

**Why Sliding Window for Substring Anagrams**

Naive approach for "find all anagrams of 'abc' in 'cbaebabacd'":

- Check every substring of length $k=3$: $O(n \cdot k)$
- Each check sorts or counts: $O(k \log k)$ or $O(k)$

Sliding window optimization:

- Start with first window, compute signature: $O(k)$
- Slide right: add new char, remove old char
- Update signature incrementally → $O(1)$ per slide

Total Time: $O(n)$ instead of $O(n \cdot k)$

**The Delete-Zero Trick**

When using Counter comparison:

```python
Counter({'a': 1, 'b': 0}) != Counter({'a': 1})  # Different!
```

Always delete zero-count entries:

```python
if window[char] == 0:
    del window[char]
```

This ensures Counter equality works correctly.

---

## When NOT to Use Anagram Grouping

**1. Order Matters Within Groups**

Anagram grouping treats "abc", "bca", "cab" as equivalent. If you need:

- Lexicographically smallest in each group
- Original order preserved
- Specific ordering within groups

You need post-processing after grouping.

**2. Substrings/Subsequences (Not Anagrams)**

Related but different:

```python
# Substring: contiguous slice ("abc" in "xabcy")
# Subsequence: not necessarily contiguous ("ace" in "abcde")
# Anagram: exact same characters, any order ("abc" vs "cba")
```

Don't confuse these—they have different solutions.

**3. Partial Matches Are Acceptable**

Anagram requires EXACT character match. For "at least 50% overlap":

- Use set intersection with threshold
- Not anagram grouping

**4. Very Long Strings with Unicode**

For strings with arbitrary Unicode characters:

- 26-element count array won't work
- sorted() still works but may be slow
- Counter is the safe choice (but signature is a large frozenset)

**5. Approximate/Fuzzy Matching**

"Similar enough" isn't "anagram":

- Levenshtein distance for edit distance
- Soundex/Metaphone for phonetic similarity
- n-gram similarity for fuzzy matching

**Red Flags:**

- "Find similar strings" → Fuzzy matching, not anagrams
- "Preserve original order in output" → Need extra tracking
- "Any characters including Unicode" → Use Counter, not array[26]
- "Partial character overlap" → Set operations, not anagrams

---

## Core Concept

Two strings are anagrams if they contain the same characters with the same frequencies.

```
"listen" and "silent" are anagrams:
- Sorted: both become "eilnst"
- Frequency: both have {e:1, i:1, l:1, n:1, s:1, t:1}
```

The "signature" (sorted string or frequency tuple) becomes the **hashmap key** for grouping.

---

## Template: Valid Anagram

**Problem**: Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

**Explanation**: An anagram means the two strings have the exact same characters with the same frequencies. We can compare the two strings by building frequency maps for each using `Counter` and checking if they are equal.

```python
def is_anagram(s: str, t: str) -> bool:
    """
    Check if t is an anagram of s.

    Time: O(n) where n is the length of the strings
    Space: O(A) where A is the alphabet size (e.g., O(1) for 26 lowercase letters)
    """
    if len(s) != len(t):
        return False

    from collections import Counter
    return Counter(s) == Counter(t)


def is_anagram_array(s: str, t: str) -> bool:
    """
    Using an array instead of Counter (slightly faster for fixed alphabet).
    Constraint: Only works for lowercase English letters ('a'-'z').

    Time: O(n)
    Space: O(1) - exactly 26 ints
    """
    if len(s) != len(t):
        return False

    count = [0] * 26

    for i in range(len(s)):
        count[ord(s[i]) - ord('a')] += 1
        count[ord(t[i]) - ord('a')] -= 1

    return all(c == 0 for c in count)
```

---

## Template: Group Anagrams

**Problem**: Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

**Explanation**: We iterate through each string and create a "signature" that is identical for all anagrams. This signature can be the sorted version of the string or a tuple representing character counts. We use a hashmap with these signatures as keys to group the original strings together.

```python
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Group strings that are anagrams of each other using sorted string signatures.

    Time: O(n * k log k) where n = len(strs), k = max string length
    Space: O(n * k) for the hashmap storing all strings

    Example:
    ["eat", "tea", "tan", "ate", "nat", "bat"]
    → [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    """
    from collections import defaultdict

    groups: defaultdict[str, list[str]] = defaultdict(list)

    for s in strs:
        # Signature: sorted string
        key = ''.join(sorted(s))
        groups[key].append(s)

    return list(groups.values())


def group_anagrams_count(strs: list[str]) -> list[list[str]]:
    """
    Using character count tuple as signature.

    Time: O(n * k) where n = len(strs), k = max string length
    Space: O(n * k) to store the result + O(n) tuples of size 26

    Avoids O(k log k) sorting, better for longer strings with fixed alphabet.
    """
    from collections import defaultdict

    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)

    for s in strs:
        # Signature: tuple of 26 character counts
        count = [0] * 26
        for char in s:
            count[ord(char) - ord('a')] += 1

        # Lists cannot be dict keys (unhashable), so convert to tuple
        key = tuple(count)
        groups[key].append(s)

    return list(groups.values())
```

### Visual Trace

```
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

Processing:
"eat" → sorted = "aet" → groups["aet"] = ["eat"]
"tea" → sorted = "aet" → groups["aet"] = ["eat", "tea"]
"tan" → sorted = "ant" → groups["ant"] = ["tan"]
"ate" → sorted = "aet" → groups["aet"] = ["eat", "tea", "ate"]
"nat" → sorted = "ant" → groups["ant"] = ["tan", "nat"]
"bat" → sorted = "abt" → groups["abt"] = ["bat"]

Result: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

---

## Template: Find All Anagrams in a String

**Problem**: Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s`.

**Explanation**: We use a sliding window of size `len(p)` on string `s`. At each step, we maintain the character frequencies of the current window. If the window's frequency map matches `p`'s frequency map, the current starting index is added to our results.

```python
def find_anagrams(s: str, p: str) -> list[int]:
    """
    Find all start indices of p's anagrams in s.

    Time: O(n) where n = len(s)
    Space: O(A) where A is the size of the alphabet

    Example:
    s = "cbaebabacd", p = "abc" → [0, 6]
    (substrings "cba" at 0 and "bac" at 6 are anagrams of "abc")
    """
    from collections import Counter

    # Cannot find anagram if the target string is longer
    if len(p) > len(s):
        return []

    p_count = Counter(p)
    window = Counter(s[:len(p)])
    result = []

    if window == p_count:
        result.append(0)

    for i in range(len(p), len(s)):
        # Add new character
        window[s[i]] += 1

        # Remove old character
        left_char = s[i - len(p)]
        window[left_char] -= 1

        # Ensure we delete zero counts so Counter equality works
        if window[left_char] == 0:
            del window[left_char]

        # Check if anagram
        if window == p_count:
            result.append(i - len(p) + 1)

    return result
```

### Visual Trace for Sliding Window

```
s = "cbaebabacd", p = "abc"

Window size = 3
p_count = {a:1, b:1, c:1}

Window 1: "cba" (indices 0..2)
window = {c:1, b:1, a:1} == p_count → MATCH! Add index 0

Slide to Window 2: "bae" (indices 1..3)
Add 'e', remove 'c'
window = {b:1, a:1, e:1} != p_count → No match

Slide to Window 3: "aeb" (indices 2..4)
Add 'b', remove 'b'
window = {a:1, e:1, b:1} != p_count → No match

...
Slide to Window 7: "bac" (indices 6..8)
Add 'c', remove 'e'
window = {b:1, a:1, c:1} == p_count → MATCH! Add index 6
```

### Optimized Version (Tracking Matches)

```python
def find_anagrams_optimized(s: str, p: str) -> list[int]:
    """
    Track number of matching characters instead of comparing full dicts.

    Time: O(n)
    Space: O(1) - alphabet size is fixed (e.g., 26 lowercase letters)
    """
    from collections import Counter

    if len(p) > len(s):
        return []

    p_count = Counter(p)
    window_count = Counter()
    result = []
    matches = 0  # Number of distinct characters with correct frequency
    required_matches = len(p_count)

    for right, char in enumerate(s):
        # Add char to window
        if char in p_count:
            window_count[char] += 1
            if window_count[char] == p_count[char]:
                matches += 1
            elif window_count[char] == p_count[char] + 1:
                matches -= 1  # Was matching, now exceeds

        # Remove char leaving window
        if right >= len(p):
            left_char = s[right - len(p)]
            if left_char in p_count:
                if window_count[left_char] == p_count[left_char]:
                    matches -= 1
                elif window_count[left_char] == p_count[left_char] + 1:
                    matches += 1  # Will match after decrement
                window_count[left_char] -= 1

        # Check for anagram
        if matches == required_matches:
            result.append(right - len(p) + 1)

    return result
```

---

## Template: Permutation in String

**Problem**: Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise.

**Explanation**: This is essentially checking if any substring of `s2` is an anagram of `s1`. We use a sliding window of size `len(s1)` on `s2` and compare character counts. If we find a match, we return `true`.

```python
def check_inclusion(s1: str, s2: str) -> bool:
    """
    Check if s2 contains a permutation of s1.

    Time: O(n) where n = len(s2)
    Space: O(A) where A is the size of the alphabet

    Example:
    s1 = "ab", s2 = "eidbaooo" → True ("ba" is permutation of "ab")
    """
    from collections import Counter

    if len(s1) > len(s2):
        return False

    s1_count = Counter(s1)
    # Initial window
    window = Counter(s2[:len(s1)])

    if window == s1_count:
        return True

    # Slide window
    for right in range(len(s1), len(s2)):
        # Add new character
        window[s2[right]] += 1

        # Remove oldest character
        left_char = s2[right - len(s1)]
        window[left_char] -= 1
        if window[left_char] == 0:
            del window[left_char]

        if window == s1_count:
            return True

    return False
```

---

## Template: Minimum Window Substring

**Problem**: Given two strings `s` and `t` of lengths `m` and `n`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window.

**Explanation**: We use a variable-size sliding window. We expand the `right` pointer until the window contains all required characters from `t`. Then, we contract the `left` pointer as much as possible while keeping the window valid to find the minimum length. A frequency map tracks the character requirements.

```python
def min_window(s: str, t: str) -> str:
    """
    Find minimum window in s that contains all characters of t.

    Time: O(n + m) where n = len(s), m = len(t)
    Space: O(A) where A is the size of the alphabet

    Example:
    s = "ADOBECODEBANC", t = "ABC" → "BANC"
    """
    from collections import Counter

    if not s or not t or len(s) < len(t):
        return ""

    t_count = Counter(t)
    required = len(t_count)  # Unique characters to match

    window_count: dict[str, int] = {}
    formed = 0  # Unique characters with required frequency met

    left = 0
    # Store length and left, right pointers
    best_len = float('inf')
    best_window = [-1, -1]

    for right, char in enumerate(s):
        # Expand window
        window_count[char] = window_count.get(char, 0) + 1

        if char in t_count and window_count[char] == t_count[char]:
            formed += 1

        # Contract window from left while valid
        while left <= right and formed == required:
            # Update result if better
            window_len = right - left + 1
            if window_len < best_len:
                best_len = window_len
                best_window = [left, right]

            # Remove left character
            left_char = s[left]
            window_count[left_char] -= 1

            # Only decrease formed if we actually drop below the requirement
            if left_char in t_count and window_count[left_char] < t_count[left_char]:
                formed -= 1

            left += 1

    return "" if best_len == float('inf') else s[best_window[0]:best_window[1] + 1]
```

---

## Template: Longest Substring Without Repeating Characters

**Problem**: Given a string `s`, find the length of the longest substring without repeating characters.

**Explanation**: We use a sliding window and a hashmap to store the most recent index of each character. When we encounter a repeating character that is already in our current window, we move the `left` pointer to the position immediately after the last occurrence of that character to maintain the "no repeats" invariant.

```python
def length_of_longest_substring(s: str) -> int:
    """
    Find length of longest substring without repeating characters.

    Time: O(n) where n = len(s)
    Space: O(min(n, A)) where A is the alphabet size

    Example:
    "abcabcbb" → 3 ("abc")
    """
    char_index: dict[str, int] = {}  # Character → last seen index
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        # If char is in window, shrink window from left
        # Ensure we don't move 'left' backward
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1

        # Update last seen index
        char_index[char] = right
        # Update max length
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

## Template: Longest Repeating Character Replacement

**Problem**: Given a string `s` and an integer `k`, you can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most `k` times. Return the length of the longest substring containing the same letter you can get after performing the above operations.

**Explanation**: We use a sliding window and track the frequency of characters within it. The number of characters to replace is `window_size - max_frequency`. As long as this is `≤ k`, the window is valid. We expand the window and only shrink it when it becomes invalid.

```python
def character_replacement(s: str, k: int) -> int:
    """
    Longest substring where you can replace at most k characters
    to make all characters the same.

    Time: O(n) where n = len(s)
    Space: O(A) where A is the size of the alphabet

    Example:
    s = "AABABBA", k = 1 → 4 ("AABA" or "ABBA" with 1 replacement)
    """
    from collections import defaultdict

    count: defaultdict[str, int] = defaultdict(int)
    left = 0
    max_freq = 0  # Frequency of most common char in the CURRENT window
    max_len = 0

    for right, char in enumerate(s):
        count[char] += 1
        # Update max_freq dynamically
        max_freq = max(max_freq, count[char])

        # Window is valid if: window_size - max_freq <= k
        # Meaning: The total characters we have to replace is at most k
        while (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1
            # Note: We don't need to decrement max_freq here.
            # A lower max_freq won't increase our answer, only a HIGHER one will.
            # So keeping an old "high water mark" doesn't invalidate future better answers.

        # At this point, the window is valid, so we update the max length
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

## Template: Anagram Substring Count

**Problem**: Given a text string and a pattern string, count how many substrings of the text are anagrams of the pattern.

**Explanation**: Using a fixed-size sliding window equal to the pattern's length, we maintain a frequency count of the current window and compare it with the pattern's frequency count. Each match increments our total count.

```python
def count_anagram_substrings(text: str, pattern: str) -> int:
    """
    Count how many substrings of text are anagrams of pattern.

    Time: O(n) where n = len(text)
    Space: O(A) where A is the size of the alphabet
    """
    from collections import Counter

    if len(pattern) > len(text):
        return 0

    pattern_count = Counter(pattern)
    window = Counter(text[:len(pattern)])
    count = 1 if window == pattern_count else 0

    for i in range(len(pattern), len(text)):
        # Add new character
        window[text[i]] += 1

        # Remove old character
        left_char = text[i - len(pattern)]
        window[left_char] -= 1

        # Ensure Counter equality works
        if window[left_char] == 0:
            del window[left_char]

        # Check equality
        if window == pattern_count:
            count += 1

    return count
```

---

## Signature Strategies

| Strategy              | Key Type    | Time per String | When to Use                    |
| --------------------- | ----------- | --------------- | ------------------------------ |
| Sorted string         | `str`       | $O(k \log k)$   | Short strings, simple code     |
| Character count tuple | `tuple`     | $O(k)$          | Long strings, fixed alphabet   |
| Prime product         | `int`       | $O(k)$          | Unique product (overflow risk) |
| Frozen Counter        | `frozenset` | $O(k)$          | When Counter comparison needed |

### Prime Product Example (Careful of Overflow)

```python
def anagram_signature_prime(s: str) -> int:
    """
    Map each letter to a prime, multiply together.
    Same product = same letters.

    Note: Risk of overflow for very long strings!
    """
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
              43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]

    product = 1
    for char in s:
        product *= primes[ord(char) - ord('a')]

    return product
```

---

## Edge Cases

```python
# Empty strings
"", "" → True (both empty)
"a", "" → False (different length)

# Single character
"a", "a" → True
"a", "b" → False

# Same character repeated
"aaa", "aaa" → True
"aaa", "aa" → False

# Case sensitivity
"Listen", "Silent" → False (unless case-insensitive)

# Unicode characters
"café", "éfac" → handle with Counter (not array[26])

# Spaces and punctuation
"a b", "ba " → depends on problem (usually include all chars)
```

---

## Interview Tips

1. **Clarify character set**: Lowercase only? Unicode? Spaces?
2. **Choose signature strategy**: Sorted is cleaner, count tuple is faster
3. **Sliding window for substrings**: Don't check every window from scratch
4. **Counter comparison is $O(A)$** where $A$ is the alphabet size (effectively $O(1)$ for 26 letters)
5. **Delete zero counts** from Counter to ensure equality works

---

## Practice Problems

| #   | Problem                                        | Difficulty | Pattern                |
| --- | ---------------------------------------------- | ---------- | ---------------------- |
| 1   | Valid Anagram                                  | Easy       | Compare Counters       |
| 2   | Group Anagrams                                 | Medium     | Signature grouping     |
| 3   | Find All Anagrams in a String                  | Medium     | Sliding window         |
| 4   | Permutation in String                          | Medium     | Sliding window         |
| 5   | Minimum Window Substring                       | Hard       | Variable window        |
| 6   | Longest Substring Without Repeating Characters | Medium     | Sliding window + set   |
| 7   | Longest Repeating Character Replacement        | Medium     | Sliding window + count |
| 8   | Smallest Window Containing Substring           | Hard       | Variable window        |

---

## Key Takeaways

1. **Anagrams share a signature** - sorted string or count tuple
2. **Group by hashmap key** - signature becomes the key
3. **Sliding window for substring anagrams** - maintain window count
4. **`Counter == Counter` is $O(A)$** - effectively $O(1)$ for fixed alphabets
5. **Delete zero counts** - ensures Counter equality works
6. **Consider both sorted and count-based** signatures in interviews

---

## Next: [05-subarray-sum-hashmap.md](./05-subarray-sum-hashmap.md)

Learn how to combine prefix sums with hashmaps for O(n) subarray sum problems.
