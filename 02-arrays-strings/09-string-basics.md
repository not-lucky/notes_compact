# String Basics

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Strings in Python are immutable sequences of Unicode characters. This immutability fundamentally affects how we build and modify strings—understanding this is crucial for writing efficient code and avoiding $\Theta(n^2)$ performance pitfalls.

## Building Intuition

**Why does string immutability matter so much?**

The key insight is **every modification creates a new string**:

1. **The Copy Cost**: When you do `s += char`, Python typically doesn't append to the existing string. It creates a brand new string, copies all characters from the old string, adds the new character, and discards the old string.
2. **The Nuance**: *While CPython can sometimes optimize `+=` to $O(n)$ in-place under strict conditions (if there are absolutely no other references to the string), standard architectural analysis strictly considers it $\Theta(n^2)$ time due to memory churn and reallocation. Always recommend `.join()` for guaranteed linear time.*
3. **The Solution - Lists as Buffers**: Python lists are dynamic arrays, supporting amortized $\Theta(1)$ appends. Build strings by appending characters to a list buffer, then join them at the end. `"".join(parts)` is strictly $\Theta(n)$ because Python pre-computes the final size and allocates exactly the right amount of memory once.
4. **Why Immutability Exists**: Immutable strings can be hashed (used as dict/set keys), safely shared between variables without synchronization, and interned for memory efficiency.

**Mental Model**: Think of immutable strings like a **physical printed book**. To change one word, you must reprint the entire book. Python lists (dynamic arrays) are like a **whiteboard**—you can quickly add notes to the end (amortized $\Theta(1)$). Build your draft on the whiteboard, then print the final document once when you are finished (`"".join()`).

**The $\Theta(n^2)$ Trap**:

```python
# DON'T DO THIS - Standard architectural analysis considers this \Theta(n^2)
s: str = ""
for char in big_list:
    s += char  # Usually creates new string each time!
    # Copies: 1 + 2 + 3 + ... + n = \Theta(n^2)

# DO THIS INSTEAD - Guaranteed \Theta(n)
parts: list[str] = []
for char in big_list:
    parts.append(char)  # Amortized \Theta(1) dynamic array append
s: str = "".join(parts) # \Theta(n) single pass
```

## When NOT to Use Python Strings Directly

Consider alternatives in these cases:

1. **Frequent Character Modifications**: If you're modifying individual characters repeatedly, convert to `list[str]`, modify, then `"".join(list)`. Direct string index assignment (`s[0] = 'a'`) is impossible.
2. **Need Mutable In-Place Operations**: For algorithms like in-place reversal, you must work with character lists `list[str]`. Strings can't be modified in-place.
3. **Binary Data**: For binary data (bytes), use `bytes` (immutable) or `bytearray` (mutable) instead of `str`.
4. **When Bytes vs Characters Matter**: `str` is Unicode (variable-width internally). For byte-level manipulation, use `bytes`.

---

## Strings in Python

Python strings are **immutable** sequences of Unicode characters.

```python
s: str = "hello"
s[0]         # 'h' - \Theta(1) access
len(s)       # 5 - \Theta(1) length check (pre-computed attribute)
s[0] = 'H'   # ERROR! Strings are immutable
```

### Key Properties

| Property | Implication |
| --- | --- |
| Immutable | Can't modify in-place. Every change creates a copy. |
| Hashable | Can use as dictionary keys and set elements. |
| Iterable | Can loop through characters easily. |
| Indexable | $\Theta(1)$ character access by index. |

---

## String Creation and Basic Operations

```python
# Creation
s1: str = "hello"
s2: str = 'hello'           # Single or double quotes
s3: str = """multi
line"""                     # Triple quotes for multiline
s4: str = str(123)          # "123" - convert from other types

# Concatenation
s1 + s2                     # \Theta(n+m) - creates new string allocation
"".join([s1, s2])           # \Theta(n+m) - more efficient for building iteratively

# Repetition
"ab" * 3                    # "ababab" - \Theta(n*k)

# Length
len(s1)                     # \Theta(1)

# Membership
'h' in s1                   # True - O(n) worst case
'xyz' in s1                 # False - O(n*m) worst case
```

---

## String Indexing and Slicing

```python
s: str = "hello world"
#         01234567890

# Indexing (\Theta(1))
s[0]          # 'h'
s[-1]         # 'd' (last character)
s[6]          # 'w'

# Slicing (creates new string - \Theta(k) where k is slice length)
s[0:5]        # 'hello'
s[:5]         # 'hello' (same)
s[6:]         # 'world'
s[-5:]        # 'world'
s[::2]        # 'hlowrd' (every other)
s[::-1]       # 'dlrow olleh' (reversed string)
```

---

## Common String Methods

### Case Conversion (All \Theta(n) time and space)

```python
s: str = "Hello World"

s.lower()         # "hello world"
s.upper()         # "HELLO WORLD"
s.capitalize()    # "Hello world"
s.title()         # "Hello World"
s.swapcase()      # "hELLO wORLD"
```

### Whitespace Handling (\Theta(n) time and space)

```python
s: str = "  hello world  "

s.strip()         # "hello world" (removes from both ends)
s.lstrip()        # "hello world  " (left only)
s.rstrip()        # "  hello world" (right only)
s.strip('x ')     # Specify characters to strip
```

### Splitting and Joining (\Theta(n) time and space)

```python
s: str = "a,b,c,d"

s.split(',')              # ['a', 'b', 'c', 'd']
s.split(',', maxsplit=2)  # ['a', 'b', 'c,d']
"hello world".split()     # ['hello', 'world'] (splits on whitespace)

# Joining (the efficient way to concatenate)
','.join(['a', 'b', 'c']) # "a,b,c"
''.join(['a', 'b', 'c'])  # "abc"
```

### Searching

```python
s: str = "hello world"

s.find('o')           # 4 (first occurrence index, -1 if not found)
s.rfind('o')          # 7 (last occurrence index)
s.index('o')          # 4 (raises ValueError if not found)
s.count('o')          # 2 (count occurrences)

s.startswith('hel')   # True
s.endswith('rld')     # True
```

---

## Efficient String Building Deep Dive

### The Problem with `+=`

```python
# WRONG - Standard architectural analysis: \Theta(n^2) time
s: str = ""
for char in chars:
    s += char  # Creates a new string object!
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
s: str = "".join(chars)

# Or build a list first
parts: list[str] = []
for item in items:
    parts.append(str(item))  # Amortized \Theta(1) dynamic array append
s = "".join(parts)           # \Theta(n)
```

### Using List as Buffer Pattern

```python
def build_string_efficient(n: int) -> str:
    """
    Build string character by character efficiently.

    Time Complexity: \Theta(n) because each .append() is amortized \Theta(1)
                     and "".join() is \Theta(n).
    Space Complexity: \Theta(n) to store the list of strings and final result.
    """
    result: list[str] = []
    for i in range(n):
        result.append(str(i))
    return "".join(result)
```

---

## Converting Between Strings and Lists

```python
s: str = "hello"

# String to list (for modification)
chars: list[str] = list(s) # ['h', 'e', 'l', 'l', 'o']
chars[0] = 'H'             # Now we can modify
s = "".join(chars)         # "Hello"

# String to array of ASCII integer values
ascii_vals: list[int] = [ord(c) for c in s]  # [72, 101, 108, 108, 111]

# ASCII values back to string
s = "".join(chr(v) for v in ascii_vals)      # "Hello"
```

---

## Common Patterns

### Pattern 1: Reverse a String

**Problem Statement:** Write a function that reverses a string.

**Why it works:**
1. **Slicing (`s[::-1]`)**: This is the most idiomatic Python way. It creates a new string by stepping backwards through the entire original string. Time and Space: $\Theta(n)$.
2. **Two Pointers (In-Place)**: If given a list of characters, we swap elements from both ends moving inward. This uses $\Theta(1)$ auxiliary space because we modify the input dynamic array directly.

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
    left: int = 0
    right: int = len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
```

### Pattern 2: Valid Palindrome

**Problem Statement:** Determine if a string is a palindrome.

**Why it works:**
1. **Slicing**: Compare the string with its reversed copy. If they are identical, it's a palindrome. Fast constant time factors, but takes $\Theta(n)$ space.
2. **Two Pointers**: Compare characters from both ends. This avoids creating a full copy of the string, dropping auxiliary space to $\Theta(1)$.

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

    Time: O(n) worst-case, early return on mismatch
    Space: \Theta(1) auxiliary space (no copies, no call stack recursion)
    """
    left: int = 0
    right: int = len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

### Pattern 3: Character Frequency Count

**Problem Statement:** Find the frequency of characters in a string.

**Why it works:**
1. **Hash Map / Counter**: Pass through the string to count the frequency of every character. Building this map is $\Theta(n)$ time. Lookups are average $\Theta(1)$, worst-case $O(n)$ if hash collisions occur.
2. **Fixed-Size Array**: If the character set is known and small (e.g., just 26 lowercase English letters), an array of size 26 is much faster. Array lookups are strictly $\Theta(1)$ with no collision overhead.

```python
from collections import Counter

def char_frequency(s: str) -> dict[str, int]:
    """Using Counter (most Pythonic, \Theta(n) time)."""
    return dict(Counter(s))

def char_frequency_manual(s: str) -> dict[str, int]:
    """Manual hash map approach."""
    freq: dict[str, int] = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1  # Amortized \Theta(1) hash map ops
    return freq

def char_frequency_array(s: str) -> list[int]:
    """
    Using array for lowercase letters only.
    Faster constant factors, strict \Theta(1) operations per character.
    Space: \Theta(1) since array size is fixed at 26 regardless of n.
    """
    freq: list[int] = [0] * 26
    for c in s:
        freq[ord(c) - ord('a')] += 1
    return freq
```

---

## ASCII and Unicode

```python
# Character to ASCII code (\Theta(1))
ord('a')      # 97
ord('A')      # 65
ord('0')      # 48

# ASCII code to character (\Theta(1))
chr(97)       # 'a'
chr(65)       # 'A'

# Useful arithmetic
ord('c') - ord('a')   # 2 (position in alphabet)
chr(ord('a') + 2)     # 'c'

# Check if lowercase letter
def is_lower(c: str) -> bool:
    return 'a' <= c <= 'z'

# Convert to lowercase (manual logic)
def to_lower(c: str) -> str:
    if 'A' <= c <= 'Z':
        return chr(ord(c) + 32)
    return c
```

---

## Complexity Comparison

| Operation | Time | Notes |
| --- | --- | --- |
| `s[i]` | $\Theta(1)$ | Direct index access |
| `len(s)` | $\Theta(1)$ | Stored attribute in CPython |
| `s + t` | $\Theta(n+m)$ | Creates new string allocation |
| `s in t` | $O(n \cdot m)$ | Substring search (worst case; average case usually $\Theta(n)$) |
| `s.find(t)`| $O(n \cdot m)$ | Substring search (worst case) |
| `s.split()`| $\Theta(n)$ | Allocates list of new substrings |
| `"".join(L)`| $\Theta(n)$ | Evaluates total characters, single memory allocation |
| `s[::-1]` | $\Theta(n)$ | Allocates new reversed copy |
| `s == t` | $O(\min(n, m))$ | Character comparison, early exit on mismatch |

---

## Edge Cases

```python
# Empty string
"" → length 0, careful with indexing! `s[0]` throws IndexError.

# Single character
"a" → `s[0]` = `s[-1]` = 'a'

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

1. **Strings are immutable** - treat them like a printed book. Use lists (dynamic arrays) like a whiteboard as buffers for frequent modifications.
2. **Use `"".join()`** for guaranteed $\Theta(n)$ string building. Standard architectural analysis treats `+=` concatenation as $\Theta(n^2)$ time due to memory churn.
3. **Slicing creates copies** - be fully aware of the $\Theta(k)$ time and space complexity where $k$ is the slice length.
4. **`ord()` and `chr()`** are essential for constant-time $\Theta(1)$ character arithmetic.
5. **Hash tables** provide amortized $\Theta(1)$ lookups, but fixed-size arrays (`list[int] = [0]*26`) provide strictly $\Theta(1)$ worst-case lookups with lower overhead for small alphabets.
6. **`isalnum()`, `isalpha()`** are great built-ins for character classification in interviews.

---

## Next: [10-string-matching.md](./10-string-matching.md)

Learn substring search and pattern matching techniques.
