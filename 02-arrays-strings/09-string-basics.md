# String Basics

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

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
s[0]         # 'h' - O(1) access
len(s)       # 5 - O(1)
s[0] = 'H'   # ERROR! Strings are immutable
```

### Key Properties

| Property | Implication |
|----------|-------------|
| Immutable | Can't modify in-place |
| Hashable | Can use as dict keys/set elements |
| Iterable | Can loop through characters |
| Indexable | O(1) character access |

---

## String Creation and Basic Operations

```python
# Creation
s = "hello"
s = 'hello'           # Single or double quotes
s = """multi
line"""                # Triple quotes for multiline
s = str(123)          # "123" - convert from other types

# Concatenation
s1 + s2               # O(n+m) - creates new string
"".join([s1, s2])     # O(n+m) - more efficient for many strings

# Repetition
"ab" * 3              # "ababab"

# Length
len(s)                # O(1)

# Membership
'h' in s              # True - O(n)
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

# Slicing (creates new string - O(k) where k is slice length)
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

### The Problem with +=

```python
# WRONG - O(n²) total time
s = ""
for char in chars:
    s += char  # Creates new string each time!
```

Why O(n²)? Each `+=` copies the entire string:
- Iteration 1: copy 1 char
- Iteration 2: copy 2 chars
- ...
- Iteration n: copy n chars
- Total: 1 + 2 + ... + n = O(n²)

### The Solution: Join

```python
# RIGHT - O(n) total time
s = "".join(chars)

# Or build a list first
parts = []
for item in items:
    parts.append(process(item))
s = "".join(parts)
```

### Using List as Buffer

```python
def build_string_efficient(n: int) -> str:
    """
    Build string character by character efficiently.

    Time: O(n)
    Space: O(n)
    """
    result = []
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

```python
def reverse_string(s: str) -> str:
    """
    Time: O(n)
    Space: O(n)
    """
    return s[::-1]

def reverse_string_inplace(chars: list[str]) -> None:
    """
    For list of characters (in-place).

    Time: O(n)
    Space: O(1)
    """
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
```

### Check if Palindrome

```python
def is_palindrome(s: str) -> bool:
    """
    Time: O(n)
    Space: O(n) for s[::-1], or O(1) with two pointers
    """
    return s == s[::-1]

def is_palindrome_two_pointers(s: str) -> bool:
    """
    Space-efficient version.

    Time: O(n)
    Space: O(1)
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

```python
from collections import Counter

def char_frequency(s: str) -> dict:
    """Using Counter (most Pythonic)."""
    return Counter(s)

def char_frequency_manual(s: str) -> dict:
    """Manual approach."""
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    return freq

def char_frequency_array(s: str) -> list[int]:
    """Using array for lowercase letters only (faster)."""
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
|-----------|------|-------|
| `s[i]` | O(1) | Index access |
| `len(s)` | O(1) | Stored attribute |
| `s + t` | O(n+m) | Creates new string |
| `s in t` | O(n*m) | Substring search |
| `s.find(t)` | O(n*m) | Substring search |
| `s.split()` | O(n) | Creates list of strings |
| `"".join(list)` | O(n) | Total characters |
| `s[::-1]` | O(n) | Creates reversed copy |
| `s == t` | O(n) | Character comparison |

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

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Reverse String | Easy | Two pointers or slicing |
| 2 | Valid Palindrome | Easy | Two pointers, isalnum |
| 3 | First Unique Character | Easy | Frequency count |
| 4 | Valid Anagram | Easy | Character frequency |
| 5 | String to Integer (atoi) | Medium | Parsing edge cases |
| 6 | Longest Common Prefix | Easy | Character comparison |
| 7 | Implement strStr() | Easy | Substring matching |
| 8 | Reverse Words in a String | Medium | Split, reverse, join |

---

## Key Takeaways

1. **Strings are immutable** - use list for modifications
2. **Use join()** for efficient string building
3. **Slicing creates copies** - be aware of space complexity
4. **ord() and chr()** for character arithmetic
5. **Counter** for frequency counting
6. **isalnum(), isalpha()** for character classification

---

## Next: [10-string-matching.md](./10-string-matching.md)

Learn substring search and pattern matching techniques.
