# Valid Anagram

## Problem Statement

Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

An anagram is a word formed by rearranging the letters of another word, using all the original letters exactly once.

**Example:**
```
Input: s = "anagram", t = "nagaram"
Output: true

Input: s = "rat", t = "car"
Output: false
```

## Approach

### Method 1: Hash Map / Counter
Count character frequencies in both strings and compare.

### Method 2: Sorting
Sort both strings and compare.

### Method 3: Single Counter
Increment for `s`, decrement for `t`, check all zeros.

## Implementation

```python
def is_anagram(s: str, t: str) -> bool:
    """
    Check if t is anagram of s using Counter.

    Time: O(n) - counting and comparing
    Space: O(k) - k is character set size (26 for lowercase)
    """
    if len(s) != len(t):
        return False

    from collections import Counter
    return Counter(s) == Counter(t)


def is_anagram_single_map(s: str, t: str) -> bool:
    """
    Single counter: increment for s, decrement for t.

    Time: O(n)
    Space: O(k)
    """
    if len(s) != len(t):
        return False

    count = {}

    for c in s:
        count[c] = count.get(c, 0) + 1

    for c in t:
        if c not in count:
            return False
        count[c] -= 1
        if count[c] == 0:
            del count[c]

    return len(count) == 0


def is_anagram_array(s: str, t: str) -> bool:
    """
    Using array for lowercase letters (fastest).

    Time: O(n)
    Space: O(26) = O(1)
    """
    if len(s) != len(t):
        return False

    count = [0] * 26

    for i in range(len(s)):
        count[ord(s[i]) - ord('a')] += 1
        count[ord(t[i]) - ord('a')] -= 1

    return all(c == 0 for c in count)


def is_anagram_sorting(s: str, t: str) -> bool:
    """
    Sort and compare.

    Time: O(n log n)
    Space: O(n) - sorted copies
    """
    return sorted(s) == sorted(t)
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Counter | O(n) | O(k) | k = unique chars |
| Single Map | O(n) | O(k) | Early termination |
| Array | O(n) | O(1) | Only lowercase letters |
| Sorting | O(n log n) | O(n) | Simplest code |

## Edge Cases

1. **Empty strings**: Both empty → True
2. **Different lengths**: Immediately False
3. **Single character**: `"a"`, `"a"` → True
4. **Same string**: Always True
5. **Unicode characters**: Use hash map, not array
6. **Case sensitivity**: Problem assumes lowercase; clarify in interview

## Common Mistakes

1. **Not checking length first**: Quick optimization
2. **Using wrong index for array**: `ord(c) - ord('a')` for lowercase
3. **Case sensitivity**: Clarify with interviewer
4. **Unicode support**: Array approach only works for limited charset

## Variations

### Group Anagrams
```python
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Group strings that are anagrams of each other.

    Time: O(n × k log k) where k is max string length
    Space: O(n × k)
    """
    from collections import defaultdict

    groups = defaultdict(list)

    for s in strs:
        # Use sorted string as key
        key = tuple(sorted(s))
        groups[key].append(s)

    return list(groups.values())


def group_anagrams_count(strs: list[str]) -> list[list[str]]:
    """
    Using character count as key (faster for long strings).

    Time: O(n × k) where k is max string length
    Space: O(n × k)
    """
    from collections import defaultdict

    groups = defaultdict(list)

    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(s)

    return list(groups.values())
```

### Find All Anagrams in a String
```python
def find_anagrams(s: str, p: str) -> list[int]:
    """
    Find all start indices of p's anagrams in s.

    Time: O(n) - sliding window
    Space: O(k) - character count
    """
    if len(p) > len(s):
        return []

    from collections import Counter

    p_count = Counter(p)
    s_count = Counter()
    result = []

    for i, char in enumerate(s):
        s_count[char] += 1

        # Remove character going out of window
        if i >= len(p):
            left_char = s[i - len(p)]
            s_count[left_char] -= 1
            if s_count[left_char] == 0:
                del s_count[left_char]

        # Check if window matches
        if s_count == p_count:
            result.append(i - len(p) + 1)

    return result
```

### Permutation in String
```python
def check_inclusion(s1: str, s2: str) -> bool:
    """
    Check if s2 contains any permutation of s1.
    Same as finding any anagram of s1 in s2.

    Time: O(n)
    Space: O(k)
    """
    return len(find_anagrams(s2, s1)) > 0


def check_inclusion_optimized(s1: str, s2: str) -> bool:
    """
    Optimized: stop at first match.
    """
    if len(s1) > len(s2):
        return False

    s1_count = [0] * 26
    s2_count = [0] * 26

    for c in s1:
        s1_count[ord(c) - ord('a')] += 1

    for i, c in enumerate(s2):
        s2_count[ord(c) - ord('a')] += 1

        if i >= len(s1):
            left_idx = ord(s2[i - len(s1)]) - ord('a')
            s2_count[left_idx] -= 1

        if s1_count == s2_count:
            return True

    return False
```

### Minimum Window Substring (Related)
```python
def min_window(s: str, t: str) -> str:
    """
    Find minimum window in s containing all chars of t.

    Time: O(n)
    Space: O(k)
    """
    from collections import Counter

    if not t or not s:
        return ""

    t_count = Counter(t)
    required = len(t_count)

    left = 0
    formed = 0
    window_counts = {}

    result = float('inf'), None, None

    for right, char in enumerate(s):
        window_counts[char] = window_counts.get(char, 0) + 1

        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1

        while formed == required:
            if right - left + 1 < result[0]:
                result = right - left + 1, left, right

            left_char = s[left]
            window_counts[left_char] -= 1

            if left_char in t_count and window_counts[left_char] < t_count[left_char]:
                formed -= 1

            left += 1

    return "" if result[0] == float('inf') else s[result[1]:result[2] + 1]
```

## Related Problems

- **Group Anagrams** - Group all anagrams together
- **Find All Anagrams in a String** - Find anagram indices
- **Permutation in String** - Check if permutation exists
- **Minimum Window Substring** - Find window containing all chars
- **Sort Characters By Frequency** - Related counting problem
