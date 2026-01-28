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
   - `"listen"` → `sorted("listen")` → `"eilnst"`
   - Time: O(k log k) per string

2. **Count Tuple**: Faster for lowercase, fixed alphabet
   - `"listen"` → `(0,0,0,0,1,0,0,0,1,0,0,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0)`
   - Time: O(k) per string

**Mental Model: The Signature as a "Name Tag"**

Imagine a party where everyone wearing the same "name tag" is grouped together:

- Instead of comparing everyone to everyone (O(n²))
- Give each person a name tag based on their letters
- People with matching name tags go to the same table

The hashmap groups by name tag in O(1) per lookup.

**Why Sliding Window for Substring Anagrams**

Naive approach for "find all anagrams of 'abc' in 'cbaebabacd'":

- Check every substring of length 3: O(n × k) where k=3
- Each check sorts or counts: O(k log k) or O(k)

Sliding window optimization:

- Start with first window, compute signature
- Slide right: add new char, remove old char
- Update signature incrementally → O(1) per slide

Total: O(n) instead of O(n × k)

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

```python
def is_anagram(s: str, t: str) -> bool:
    """
    Check if t is an anagram of s.

    Time: O(n)
    Space: O(1) - at most 26 lowercase letters
    """
    if len(s) != len(t):
        return False

    from collections import Counter
    return Counter(s) == Counter(t)


def is_anagram_array(s: str, t: str) -> bool:
    """
    Using array instead of Counter (slightly faster for lowercase letters).
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

```python
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Group strings that are anagrams of each other.

    Time: O(n * k log k) where k = max string length (due to sorting)
    Space: O(n * k)

    Example:
    ["eat", "tea", "tan", "ate", "nat", "bat"]
    → [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    """
    from collections import defaultdict

    groups = defaultdict(list)

    for s in strs:
        # Signature: sorted string
        key = ''.join(sorted(s))
        groups[key].append(s)

    return list(groups.values())


def group_anagrams_count(strs: list[str]) -> list[list[str]]:
    """
    Using character count as signature - O(n * k) time.

    Avoids sorting for better performance on long strings.
    """
    from collections import defaultdict

    groups = defaultdict(list)

    for s in strs:
        # Signature: tuple of character counts
        count = [0] * 26
        for char in s:
            count[ord(char) - ord('a')] += 1
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

```python
def find_anagrams(s: str, p: str) -> list[int]:
    """
    Find all start indices of p's anagrams in s.

    Time: O(n) - sliding window
    Space: O(1) - fixed alphabet size

    Example:
    s = "cbaebabacd", p = "abc" → [0, 6]
    (substrings "cba" at 0 and "bac" at 6 are anagrams of "abc")
    """
    from collections import Counter

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
        if window[left_char] == 0:
            del window[left_char]

        # Check if anagram
        if window == p_count:
            result.append(i - len(p) + 1)

    return result
```

### Optimized Version (Tracking Matches)

```python
def find_anagrams_optimized(s: str, p: str) -> list[int]:
    """
    Track number of matching characters instead of comparing full dicts.

    Time: O(n)
    Space: O(1)
    """
    from collections import Counter

    if len(p) > len(s):
        return []

    p_count = Counter(p)
    window_count = Counter()
    result = []
    matches = 0  # Number of characters with correct frequency

    for i, char in enumerate(s):
        # Add char to window
        window_count[char] += 1
        if window_count[char] == p_count.get(char, 0):
            matches += 1
        elif window_count[char] == p_count.get(char, 0) + 1:
            matches -= 1  # Was matching, now exceeds

        # Remove char leaving window
        if i >= len(p):
            left_char = s[i - len(p)]
            if window_count[left_char] == p_count.get(left_char, 0):
                matches -= 1
            elif window_count[left_char] == p_count.get(left_char, 0) + 1:
                matches += 1  # Will match after decrement

            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]

        # Check for anagram
        if matches == len(p_count):
            result.append(i - len(p) + 1)

    return result
```

---

## Template: Permutation in String

```python
def check_inclusion(s1: str, s2: str) -> bool:
    """
    Check if s2 contains a permutation of s1.

    Time: O(n)
    Space: O(1)

    Example:
    s1 = "ab", s2 = "eidbaooo" → True ("ba" is permutation of "ab")
    """
    from collections import Counter

    if len(s1) > len(s2):
        return False

    s1_count = Counter(s1)
    window = Counter(s2[:len(s1)])

    if window == s1_count:
        return True

    for i in range(len(s1), len(s2)):
        window[s2[i]] += 1

        left_char = s2[i - len(s1)]
        window[left_char] -= 1
        if window[left_char] == 0:
            del window[left_char]

        if window == s1_count:
            return True

    return False
```

---

## Template: Minimum Window Substring

```python
def min_window(s: str, t: str) -> str:
    """
    Find minimum window in s that contains all characters of t.

    Time: O(n + m)
    Space: O(m) where m = len(t)

    Example:
    s = "ADOBECODEBANC", t = "ABC" → "BANC"
    """
    from collections import Counter

    if not s or not t or len(s) < len(t):
        return ""

    t_count = Counter(t)
    required = len(t_count)  # Unique characters to match

    window_count = {}
    formed = 0  # Unique characters with required frequency

    left = 0
    min_len = float('inf')
    result = ""

    for right, char in enumerate(s):
        # Expand window
        window_count[char] = window_count.get(char, 0) + 1

        if char in t_count and window_count[char] == t_count[char]:
            formed += 1

        # Contract window while valid
        while formed == required:
            # Update result
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right + 1]

            # Remove left character
            left_char = s[left]
            window_count[left_char] -= 1

            if left_char in t_count and window_count[left_char] < t_count[left_char]:
                formed -= 1

            left += 1

    return result
```

---

## Template: Longest Substring Without Repeating Characters

```python
def length_of_longest_substring(s: str) -> int:
    """
    Find length of longest substring without repeating characters.

    Time: O(n)
    Space: O(min(n, alphabet_size))

    Example:
    "abcabcbb" → 3 ("abc")
    """
    char_index = {}  # Character → last seen index
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        # If char is in window, shrink from left
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1

        char_index[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

## Template: Longest Repeating Character Replacement

```python
def character_replacement(s: str, k: int) -> int:
    """
    Longest substring where you can replace at most k characters
    to make all characters the same.

    Time: O(n)
    Space: O(1)

    Example:
    s = "AABABBA", k = 1 → 4 ("AABA" or "ABBA" with 1 replacement)
    """
    from collections import defaultdict

    count = defaultdict(int)
    left = 0
    max_freq = 0  # Frequency of most common char in window
    max_len = 0

    for right, char in enumerate(s):
        count[char] += 1
        max_freq = max(max_freq, count[char])

        # Window is valid if: window_size - max_freq <= k
        # (characters to replace <= k)
        window_size = right - left + 1

        if window_size - max_freq > k:
            count[s[left]] -= 1
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len
```

---

## Template: Anagram Substring Count

```python
def count_anagram_substrings(text: str, pattern: str) -> int:
    """
    Count how many substrings of text are anagrams of pattern.

    Time: O(n)
    Space: O(1)
    """
    from collections import Counter

    if len(pattern) > len(text):
        return 0

    pattern_count = Counter(pattern)
    window = Counter(text[:len(pattern)])
    count = 1 if window == pattern_count else 0

    for i in range(len(pattern), len(text)):
        window[text[i]] += 1

        left_char = text[i - len(pattern)]
        window[left_char] -= 1
        if window[left_char] == 0:
            del window[left_char]

        if window == pattern_count:
            count += 1

    return count
```

---

## Signature Strategies

| Strategy              | Key Type    | Time per String | When to Use                    |
| --------------------- | ----------- | --------------- | ------------------------------ |
| Sorted string         | `str`       | O(k log k)      | Short strings, simple code     |
| Character count tuple | `tuple`     | O(k)            | Long strings, lowercase only   |
| Prime product         | `int`       | O(k)            | Unique product (overflow risk) |
| Frozen Counter        | `frozenset` | O(k)            | When Counter comparison needed |

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
4. **Counter comparison is O(1)** for fixed alphabet (26 letters)
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
4. **Counter == Counter is O(alphabet)** - effectively O(1)
5. **Delete zero counts** - ensures Counter equality works
6. **Consider both sorted and count-based** signatures in interviews

---

## Next: [05-subarray-sum-hashmap.md](./05-subarray-sum-hashmap.md)

Learn how to combine prefix sums with hashmaps for O(n) subarray sum problems.
