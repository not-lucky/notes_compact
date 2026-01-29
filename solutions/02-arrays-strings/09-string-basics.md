# String Basics - Solutions

## Practice Problems

### 1. Reverse String

**Problem Statement**: Write a function that reverses a string. The input string is given as an array of characters `s`. You must do this by modifying the input array in-place with O(1) extra memory.

**Examples & Edge Cases**:

- Example: `s = ["h","e","l","l","o"]` -> `["o","l","l","e","h"]`
- Edge Case: Single character array.
- Edge Case: Empty array.

**Optimal Python Solution**:

```python
def reverseString(s: list[str]) -> None:
    left, right = 0, len(s) - 1
    while left < right:
        # Swap characters
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
```

**Explanation**:
We use two pointers, one at the beginning and one at the end of the array. We swap the characters at these pointers and move the pointers toward each other until they meet in the middle.

**Complexity Analysis**:

- **Time Complexity**: O(n), where n is the length of the string.
- **Space Complexity**: O(1), as we modify the input array in-place.

---

### 2. Valid Palindrome

**Problem Statement**: A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

**Optimal Python Solution**:

```python
def isPalindrome(s: str) -> bool:
    l, r = 0, len(s) - 1

    while l < r:
        # Skip non-alphanumeric characters
        if not s[l].isalnum():
            l += 1
        elif not s[r].isalnum():
            r -= 1
        else:
            # Compare lowercase characters
            if s[l].lower() != s[r].lower():
                return False
            l += 1
            r -= 1

    return True
```

**Explanation**:
We use two pointers to compare characters from both ends. We use the `.isalnum()` method to skip characters that aren't letters or numbers and `.lower()` to perform a case-insensitive comparison.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 3. First Unique Character in a String

**Problem Statement**: Given a string `s`, find the first non-repeating character in it and return its index. If it does not exist, return -1.

**Optimal Python Solution**:

```python
from collections import Counter

def firstUniqChar(s: str) -> int:
    # Build frequency map
    count = Counter(s)

    # Find the first index with frequency 1
    for i, ch in enumerate(s):
        if count[ch] == 1:
            return i

    return -1
```

**Explanation**:
We first pass through the string to count the frequency of each character using a hash map (or `Counter`). In the second pass, we check each character's frequency in the map. The first character with a count of 1 is our answer.

**Complexity Analysis**:

- **Time Complexity**: O(n), we traverse the string twice.
- **Space Complexity**: O(1) or O(min(n, m)), because the character set is finite (e.g., 26 for lowercase English letters).

---

### 4. Valid Anagram

**Problem Statement**: Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

**Optimal Python Solution**:

```python
def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    # Count character frequencies
    count = {}
    for char in s:
        count[char] = count.get(char, 0) + 1

    for char in t:
        if char not in count or count[char] == 0:
            return False
        count[char] -= 1

    return True
```

**Explanation**:
An anagram must have the same characters with the same frequencies. We count characters in the first string and decrement them for the second. If the counts match perfectly, it's an anagram.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1) (size of alphabet).

---

### 5. String to Integer (atoi)

**Problem Statement**: Implement the `myAtoi(string s)` function, which converts a string to a 32-bit signed integer.

**Optimal Python Solution**:

```python
def myAtoi(s: str) -> int:
    s = s.strip()
    if not s:
        return 0

    sign = 1
    index = 0

    # Check for sign
    if s[0] == '-':
        sign = -1
        index += 1
    elif s[0] == '+':
        index += 1

    res = 0
    while index < len(s) and s[index].isdigit():
        digit = int(s[index])
        res = res * 10 + digit
        index += 1

    # Apply sign and handle 32-bit overflow
    res = sign * res
    INT_MIN, INT_MAX = -2**31, 2**31 - 1
    if res < INT_MIN: return INT_MIN
    if res > INT_MAX: return INT_MAX

    return res
```

**Explanation**:
We follow the algorithm: skip leading whitespace, check for a sign, convert digit characters into an integer, and finally clamp the result to the 32-bit integer range.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 6. Longest Common Prefix

**Problem Statement**: Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string "".

**Optimal Python Solution**:

```python
def longestCommonPrefix(strs: list[str]) -> str:
    if not strs:
        return ""

    # Start with the first string as the prefix
    prefix = strs[0]

    for i in range(1, len(strs)):
        # Shorten prefix until it matches the start of strs[i]
        while not strs[i].startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""

    return prefix
```

**Explanation**:
We assume the first string is the common prefix. Then, for each subsequent string, we prune the prefix from the end until the string starts with it. If the prefix becomes empty, there's no common prefix.

**Complexity Analysis**:

- **Time Complexity**: O(S), where S is the total number of characters in all strings.
- **Space Complexity**: O(1).

---

### 7. Implement strStr()

**Problem Statement**: Given two strings `needle` and `haystack`, return the index of the first occurrence of `needle` in `haystack`, or -1 if `needle` is not part of `haystack`.

**Optimal Python Solution**:

```python
def strStr(haystack: str, needle: str) -> int:
    if not needle:
        return 0

    n, m = len(haystack), len(needle)
    # Only need to check up to n - m + 1
    for i in range(n - m + 1):
        # Slice and compare
        if haystack[i : i + m] == needle:
            return i

    return -1
```

**Explanation**:
We iterate through the `haystack` and check every substring of length `len(needle)` to see if it matches `needle`.

**Complexity Analysis**:

- **Time Complexity**: O((n-m)\*m) in worst case (though Python's string matching is highly optimized).
- **Space Complexity**: O(m) for the slice (or O(1) if character by character comparison is used).

---

### 8. Reverse Words in a String

**Problem Statement**: Given an input string `s`, reverse the order of the words. A word is defined as a sequence of non-space characters. The words in `s` will be separated by at least one space. Return a string of the words in reverse order concatenated by a single space.

**Optimal Python Solution**:

```python
def reverseWords(s: str) -> str:
    # 1. Split into words (automatically handles multiple spaces)
    words = s.split()

    # 2. Reverse the list of words
    words.reverse()

    # 3. Join with a single space
    return " ".join(words)
```

**Explanation**:
Python's `split()` method is very powerful; it handles multiple spaces and leading/trailing whitespace automatically. Once we have a list of words, we reverse the list and join them back together with a single space.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(n) to store the list of words.
