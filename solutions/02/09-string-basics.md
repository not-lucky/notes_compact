# String Basics

## Practice Problems

### 1. Reverse String
**Difficulty:** Easy
**Key Concept:** Two pointers or slicing

```python
def reverse_string(s: list[str]) -> None:
    """
    Reverses string in-place.
    Time: O(n)
    Space: O(1)
    """
    l, r = 0, len(s) - 1
    while l < r:
        s[l], s[r] = s[r], s[l]
        l += 1; r -= 1
```

### 2. Valid Palindrome
**Difficulty:** Easy
**Key Concept:** Two pointers, isalnum

```python
def is_palindrome(s: str) -> bool:
    """
    Time: O(n)
    Space: O(1)
    """
    l, r = 0, len(s) - 1
    while l < r:
        if not s[l].isalnum(): l += 1
        elif not s[r].isalnum(): r -= 1
        else:
            if s[l].lower() != s[r].lower(): return False
            l += 1; r -= 1
    return True
```

### 3. First Unique Character
**Difficulty:** Easy
**Key Concept:** Frequency count

```python
from collections import Counter

def first_uniq_char(s: str) -> int:
    """
    Time: O(n)
    Space: O(1) (max 26 chars)
    """
    counts = Counter(s)
    for i, char in enumerate(s):
        if counts[char] == 1:
            return i
    return -1
```

### 4. Valid Anagram
**Difficulty:** Easy
**Key Concept:** Character frequency

```python
def is_anagram(s: str, t: str) -> bool:
    """
    Time: O(n)
    Space: O(1)
    """
    if len(s) != len(t): return False
    counts = [0] * 26
    for char in s:
        counts[ord(char) - ord('a')] += 1
    for char in t:
        counts[ord(char) - ord('a')] -= 1
        if counts[ord(char) - ord('a')] < 0: return False
    return True
```

### 5. String to Integer (atoi)
**Difficulty:** Medium
**Key Concept:** Parsing edge cases

```python
def my_atoi(s: str) -> int:
    s = s.strip()
    if not s: return 0

    sign = 1
    if s[0] == '-':
        sign = -1
        s = s[1:]
    elif s[0] == '+':
        s = s[1:]

    res = 0
    for char in s:
        if not char.isdigit(): break
        res = res * 10 + int(char)

    res *= sign
    res = max(-2**31, min(res, 2**31 - 1))
    return res
```

### 6. Longest Common Prefix
**Difficulty:** Easy
**Key Concept:** Character comparison

```python
def longest_common_prefix(strs: list[str]) -> str:
    """
    Time: O(S) where S is sum of all chars
    Space: O(1)
    """
    if not strs: return ""
    for i in range(len(strs[0])):
        char = strs[0][i]
        for s in strs[1:]:
            if i == len(s) or s[i] != char:
                return strs[0][:i]
    return strs[0]
```

### 7. Implement strStr()
**Difficulty:** Easy
**Key Concept:** Substring matching

```python
def str_str(haystack: str, needle: str) -> int:
    """
    Time: O(n * m)
    Space: O(1)
    """
    if not needle: return 0
    n, m = len(haystack), len(needle)
    for i in range(n - m + 1):
        if haystack[i:i+m] == needle:
            return i
    return -1
```

### 8. Reverse Words in a String
**Difficulty:** Medium
**Key Concept:** Split, reverse, join

```python
def reverse_words(s: str) -> str:
    """
    Time: O(n)
    Space: O(n)
    """
    words = s.split()
    return " ".join(reversed(words))
```
