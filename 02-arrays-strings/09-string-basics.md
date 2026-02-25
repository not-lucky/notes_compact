# String Basics

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Strings in Python are immutable sequences of Unicode characters. This immutability fundamentally affects how we build and modify strings—understanding this is crucial for writing efficient code and avoiding $\Theta(n^2)$ pitfalls.

## Building Intuition

**Why does string immutability matter so much?**

The key insight is **every modification creates a new string**:

1. **The Copy Cost**: When you do `s += char`, Python typically doesn't append to the existing string. It creates a brand new string, copies all characters from the old string, adds the new character, and discards the old string. *Note: While CPython can sometimes optimize `+=` to $O(n)$ in-place under strict conditions (if there are no other references to the string), standard architectural analysis considers it $\Theta(n^2)$ time due to memory churn and reallocation.*

2. **The Solution - Lists as Buffers**: Python lists are dynamic arrays, which means they support amortized $O(1)$ appends. Build strings by appending to a list of characters (or substrings), then join at the end. `"".join(parts)` is $\Theta(n)$ because Python pre-computes the final size and allocates exactly the right amount of memory once.

3. **Why Immutability Exists**: Immutable strings can be hashed (used as dict keys), shared safely between variables, and interned for memory efficiency. These benefits come at the cost of modification overhead.

**Mental Model**: Think of immutable strings like a physical printed book. To change one word, you must reprint the entire book. Python lists (dynamic arrays) are like a whiteboard—you can quickly add notes to the end (amortized $O(1)$). Build your draft on the whiteboard, then print the final document once when done (`"".join()`).

**The $\Theta(n^2)$ Trap**:

```python
# DON'T DO THIS - Often $\Theta(n^2)$
s = ""
for char in big_list:
    s += char  # Usually creates new string each time!
    # Copies: 1 + 2 + 3 + ... + n = \Theta(n^2)

# DO THIS INSTEAD - \Theta(n)
parts = []
for char in big_list:
    parts.append(char)  # Amortized O(1) dynamic array append
s = "".join(parts)      # \Theta(n) single pass
```

## When NOT to Use Python Strings Directly

Consider alternatives in these cases:

1. **Frequent Character Modifications**: If you're modifying individual characters repeatedly, convert to `list(s)`, modify, then `"".join(list)`. Direct string index assignment is impossible.

2. **Very Large Strings with Many Concatenations**: Even with proper join technique, if you're building massive strings in a memory-constrained environment, consider streaming output instead.

3. **Need Mutable In-Place Operations**: For algorithms like in-place reversal, you must work with character lists. Strings can't be modified in-place.

4. **Binary Data**: For binary data (bytes), use `bytes` or `bytearray` (mutable) instead of `str`.

5. **When Bytes vs Characters Matter**: `str` is Unicode (variable-width internally). For byte-level manipulation, use `bytes`.

**Red Flags:**

- "Modify string in-place" → Must use `list(s)`, then `"".join()`
- "Append in a loop" → Use list + join, not `+=`
- "Binary/byte manipulation" → Use `bytes` or `bytearray`

---

## Interview Context

String manipulation is tested extensively because:

- Strings are fundamental in real applications
- Tests attention to detail (immutability, encoding)
- Many edge cases to handle
- Foundation for pattern matching and parsing

Understanding Python string specifics saves time in interviews.

---

## Strings in Python

Python strings are **immutable** sequences of Unicode characters.

```python
s = "hello"
s[0]         # 'h' - \Theta(1) access
len(s)       # 5 - \Theta(1)
s[0] = 'H'   # ERROR! Strings are immutable
```

### Key Properties

| Property | Implication |
| --- | --- |
| Immutable | Can't modify in-place |
| Hashable | Can use as dict keys/set elements |
| Iterable | Can loop through characters |
| Indexable | $\Theta(1)$ character access |

---

## String Creation and Basic Operations

```python
# Creation
s = "hello"
s = 'hello'           # Single or double quotes
s = """multi
line"""               # Triple quotes for multiline
s = str(123)          # "123" - convert from other types

# Concatenation
s1 + s2               # \Theta(n+m) - creates new string allocation
"".join([s1, s2])     # \Theta(n+m) - more efficient for building iteratively

# Repetition
"ab" * 3              # "ababab"

# Length
len(s)                # \Theta(1)

# Membership
'h' in s              # True - O(n) worst case
'xyz' in s            # False - O(n*m) worst case
```

---

## String Indexing and Slicing

```python
s = "hello world"
#    01234567890
#             10

# Indexing
s[0]          # 'h'
s[-1]         # 'd' (last character)
s[6]          # 'w'

# Slicing (creates new string - \Theta(k) where k is slice length)
s[0:5]        # 'hello'
s[:5]         # 'hello' (same)
s[6:]         # 'world'
s[-5:]        # 'world'
s[::2]        # 'hlowrd' (every other)
s[::-1]       # 'dlrow olleh' (reversed)
```

---

## Common String Methods

### Case Conversion

```python
s = "Hello World"

s.lower()         # "hello world"
s.upper()         # "HELLO WORLD"
s.capitalize()    # "Hello world"
s.title()         # "Hello World"
s.swapcase()      # "hELLO wORLD"
```

### Whitespace Handling

```python
s = "  hello world  "

s.strip()         # "hello world" (both ends)
s.lstrip()        # "hello world  " (left only)
s.rstrip()        # "  hello world" (right only)
s.strip('x ')     # Specify characters to strip
```

### Splitting and Joining

```python
s = "a,b,c,d"

s.split(',')              # ['a', 'b', 'c', 'd']
s.split(',', maxsplit=2)  # ['a', 'b', 'c,d']
"hello world".split()     # ['hello', 'world'] (whitespace)

# Joining (the efficient way to concatenate)
','.join(['a', 'b', 'c'])  # "a,b,c"
''.join(['a', 'b', 'c'])   # "abc"
```

### Searching

```python
s = "hello world"

s.find('o')       # 4 (first occurrence, -1 if not found)
s.rfind('o')      # 7 (last occurrence)
s.index('o')      # 4 (raises ValueError if not found)
s.count('o')      # 2

s.startswith('hel')   # True
s.endswith('rld')     # True
```

### Replacing

```python
s = "hello world"

s.replace('l', 'L')       # "heLLo worLd" (all occurrences)
s.replace('l', 'L', 1)    # "heLlo world" (first only)
```

### Character Classification

```python
s.isalpha()       # All alphabetic?
s.isdigit()       # All digits?
s.isalnum()       # All alphanumeric?
s.isspace()       # All whitespace?
s.islower()       # All lowercase?
s.isupper()       # All uppercase?
```

---

## Efficient String Building

### The Problem with `+=`

```python
# WRONG - Generally $\Theta(n^2)$ total time
s = ""
for char in chars:
    s += char  # Typically creates a new string object!
```

Why $\Theta(n^2)$? Each `+=` (without CPython optimization) copies the entire string into a new allocation:

- Iteration 1: copy 1 char
- Iteration 2: copy 2 chars
- ...
- Iteration n: copy n chars
- Total operations: $1 + 2 + \dots + n = \frac{n(n+1)}{2} = \Theta(n^2)$

### The Solution: `"".join()`

```python
# RIGHT - \Theta(n) total time
s = "".join(chars)

# Or build a list first
parts = []
for item in items:
    parts.append(process(item))  # Amortized O(1) dynamic array append
s = "".join(parts)               # \Theta(n)
```

### Using List as Buffer

```python
def build_string_efficient(n: int) -> str:
    """
    Build string character by character efficiently.

    Time: \Theta(n) because each .append() is amortized O(1) and join is \Theta(n)
    Space: \Theta(n) to store the list of strings and final result
    """
    result: list[str] = []
    for i in range(n):
        result.append(str(i))
    return "".join(result)
```

---

## Converting Between Strings and Lists

```python
s = "hello"

# String to list (for modification)
chars = list(s)       # ['h', 'e', 'l', 'l', 'o']
chars[0] = 'H'        # Can modify
s = "".join(chars)    # "Hello"

# String to array of ASCII values
ascii_vals = [ord(c) for c in s]  # [104, 101, 108, 108, 111]

# ASCII values to string
s = "".join(chr(v) for v in ascii_vals)  # "hello"
```

---

## Common Patterns

### Reverse a String

### Problem: Reverse String
**Problem Statement:** Write a function that reverses a string.

**Why it works:**
1. **Slicing (`s[::-1]`)**: This is the most idiomatic Python way. It creates a new string by stepping backwards through the entire original string.
2. **Two Pointers**: If given a list of characters, we swap elements from both ends moving inward. This uses $\Theta(1)$ extra space because we modify the input dynamic array directly.

```python
def reverse_string(s: str) -> str:
    """
    Time: \Theta(n)
    Space: \Theta(n) for the new string
    """
    return s[::-1]

def reverse_string_inplace(chars: list[str]) -> None:
    """
    For list of characters (in-place).

    Time: \Theta(n)
    Space: \Theta(1) auxiliary space
    """
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
```

### Check if Palindrome

### Problem: Valid Palindrome
**Problem Statement:** Determine if a string is a palindrome, considering only alphanumeric characters and ignoring cases.

**Why it works:**
1. **Slicing**: Compare the string with its reversed copy. If they are identical, it's a palindrome.
2. **Two Pointers**: Compare characters from both ends. This avoids creating a full copy of the string, dropping auxiliary space to $\Theta(1)$ (excluding pre-processing, like filtering non-alphanumeric chars). If implemented recursively, call stack space would be $\Theta(n)$.

```python
def is_palindrome(s: str) -> bool:
    """
    Time: \Theta(n) string reversal and comparison
    Space: \Theta(n) auxiliary memory for reversed copy
    """
    return s == s[::-1]

def is_palindrome_two_pointers(s: str) -> bool:
    """
    Space-efficient version using iterative two pointers.

    Time: \Theta(n) best-case early return, \Theta(n) overall
    Space: \Theta(1) auxiliary space (no string copies, no call stack recursion)
    """
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

### Character Frequency Count

### Problem: First Unique Character in a String
**Problem Statement:** Given a string `s`, find the first non-repeating character in it and return its index. If it does not exist, return `-1`.

**Why it works:**
1. **Hash Map / Counter**: First, pass through the string to count the frequency of every character. Building this frequency map is amortized $\Theta(n)$ time (average case hash map insertion is amortized $O(1)$, worst-case $O(n)$ if many hash collisions occur).
2. **Second Pass**: Iterate through the string again checking the frequency map. The first character with a count of `1` is the answer. Lookups are average $O(1)$, worst-case $O(n)$.

```python
from collections import Counter
from typing import Optional

def char_frequency(s: str) -> dict[str, int]:
    """Using Counter (most Pythonic)."""
    return dict(Counter(s))

def char_frequency_manual(s: str) -> dict[str, int]:
    """Manual approach."""
    freq: dict[str, int] = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1  # Amortized O(1) hash map ops
    return freq

def char_frequency_array(s: str) -> list[int]:
    """Using array for lowercase letters only (faster constant factors, \Theta(1) operations)."""
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('a')] += 1
    return freq
```

---

## ASCII and Unicode

```python
# Character to ASCII code
ord('a')      # 97
ord('A')      # 65
ord('0')      # 48

# ASCII code to character
chr(97)       # 'a'
chr(65)       # 'A'

# Useful arithmetic
ord('c') - ord('a')   # 2 (position in alphabet)
chr(ord('a') + 2)     # 'c'

# Check if lowercase letter
def is_lower(c: str) -> bool:
    return 'a' <= c <= 'z'

# Convert to lowercase (manual)
def to_lower(c: str) -> str:
    if 'A' <= c <= 'Z':
        return chr(ord(c) + 32)
    return c
```

---

## Complexity Comparison

| Operation | Time | Notes |
| --- | --- | --- |
| `s[i]` | $\Theta(1)$ | Index access |
| `len(s)` | $\Theta(1)$ | Stored attribute |
| `s + t` | $\Theta(n+m)$ | Creates new string allocation |
| `s in t` | $O(n \cdot m)$ | Substring search (worst case, CPython's Boyers-Moore implementation usually $O(n)$) |
| `s.find(t)`| $O(n \cdot m)$ | Substring search |
| `s.split()`| $\Theta(n)$ | Allocates list of new substrings |
| `"".join(L)`| $\Theta(n)$ | Evaluates total characters, single allocation |
| `s[::-1]` | $\Theta(n)$ | Allocates new reversed copy |
| `s == t` | $O(\min(n, m))$ | Character comparison, early exit on mismatch |

---

## Edge Cases

```python
# Empty string
"" → length 0, careful with indexing

# Single character
"a" → s[0] = s[-1] = 'a'

# Unicode
"café" → len is 4, not 5
"🎉" → len is 1 (single code point)

# Whitespace
"  " → not empty, len is 2
"".strip() → still ""

# Case sensitivity
"Hello" != "hello"
```

---

## Practice Problems

| #   | Problem                   | Difficulty | Key Concept             |
| --- | ------------------------- | ---------- | ----------------------- |
| 1   | Reverse String            | Easy       | Two pointers or slicing |
| 2   | Valid Palindrome          | Easy       | Two pointers, isalnum   |
| 3   | First Unique Character    | Easy       | Frequency count         |
| 4   | Valid Anagram             | Easy       | Character frequency     |
| 5   | String to Integer (atoi)  | Medium     | Parsing edge cases      |
| 6   | Longest Common Prefix     | Easy       | Character comparison    |
| 7   | Implement strStr()        | Easy       | Substring matching      |
| 8   | Reverse Words in a String | Medium     | Split, reverse, join    |

---

## Key Takeaways

1. **Strings are immutable** - use lists (dynamic arrays) as buffers for modifications.
2. **Use `"".join()`** for efficient $\Theta(n)$ string building instead of $\Theta(n^2)$ `+=` concatenation.
3. **Slicing creates copies** - be aware of the $\Theta(k)$ time and space complexity.
4. **ord() and chr()** for character arithmetic.
5. **Counter** for frequency counting (amortized $\Theta(n)$ time to build).
6. **isalnum(), isalpha()** for character classification.

---

## Next: [10-string-matching.md](./10-string-matching.md)

Learn substring search and pattern matching techniques.
