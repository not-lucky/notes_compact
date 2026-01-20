# Valid Palindrome

## Problem Statement

A phrase is a palindrome if, after converting all uppercase letters to lowercase and removing all non-alphanumeric characters, it reads the same forward and backward.

Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

**Example:**
```
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Input: s = "race a car"
Output: false
```

## Approach

### Two Pointers
1. Use two pointers from both ends
2. Skip non-alphanumeric characters
3. Compare characters (case-insensitive)
4. Return false if mismatch, true if pointers cross

### Alternative: Clean and Compare
1. Filter string to only alphanumeric, convert to lowercase
2. Compare with reverse

## Implementation

```python
def is_palindrome(s: str) -> bool:
    """
    Check if string is palindrome using two pointers.

    Time: O(n) - single pass
    Space: O(1) - no extra space
    """
    left, right = 0, len(s) - 1

    while left < right:
        # Skip non-alphanumeric from left
        while left < right and not s[left].isalnum():
            left += 1
        # Skip non-alphanumeric from right
        while left < right and not s[right].isalnum():
            right -= 1

        # Compare (case-insensitive)
        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


def is_palindrome_clean(s: str) -> bool:
    """
    Clean string first, then compare with reverse.

    Time: O(n)
    Space: O(n) - creates new string
    """
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def is_palindrome_recursive(s: str, left: int = 0, right: int = None) -> bool:
    """
    Recursive approach (less efficient but demonstrates concept).
    """
    if right is None:
        right = len(s) - 1

    # Skip non-alphanumeric
    while left < right and not s[left].isalnum():
        left += 1
    while left < right and not s[right].isalnum():
        right -= 1

    if left >= right:
        return True

    if s[left].lower() != s[right].lower():
        return False

    return is_palindrome_recursive(s, left + 1, right - 1)
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Two Pointers | O(n) | O(1) | Optimal |
| Clean and Compare | O(n) | O(n) | Creates new string |
| Recursive | O(n) | O(n) | Call stack |

## Edge Cases

1. **Empty string**: `""` → True (vacuously true)
2. **Single character**: `"a"` → True
3. **Only non-alphanumeric**: `".,!"` → True (becomes empty)
4. **Spaces only**: `"   "` → True
5. **Mixed case**: `"Aa"` → True
6. **Numbers**: `"121"` → True
7. **Almost palindrome**: `"ab"` → False

## Common Mistakes

1. **Not skipping non-alphanumeric**: Problem specifically says to ignore
2. **Case sensitivity**: Must convert to same case
3. **Off-by-one with pointers**: Use `left < right`, not `left <= right`
4. **Not checking bounds when skipping**: Pointers might cross

## Variations

### Valid Palindrome II (One Deletion)
```python
def valid_palindrome_ii(s: str) -> bool:
    """
    Check if palindrome after deleting at most one character.

    Time: O(n)
    Space: O(1)
    """
    def is_palindrome_range(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1

    while left < right:
        if s[left] != s[right]:
            # Try skipping either character
            return (is_palindrome_range(left + 1, right) or
                    is_palindrome_range(left, right - 1))
        left += 1
        right -= 1

    return True
```

### Palindrome Number
```python
def is_palindrome_number(x: int) -> bool:
    """
    Check if integer is palindrome without converting to string.
    """
    # Negative numbers are not palindromes
    if x < 0:
        return False

    # Numbers ending in 0 are only palindrome if x == 0
    if x != 0 and x % 10 == 0:
        return False

    reversed_half = 0
    while x > reversed_half:
        reversed_half = reversed_half * 10 + x % 10
        x //= 10

    # For odd length, middle digit doesn't matter
    return x == reversed_half or x == reversed_half // 10
```

### Longest Palindromic Substring
```python
def longest_palindrome(s: str) -> str:
    """
    Find longest palindromic substring.

    Time: O(n²) - expand around each center
    Space: O(1)
    """
    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right  # Return valid palindrome bounds

    if not s:
        return ""

    best_start, best_end = 0, 1

    for i in range(len(s)):
        # Odd length palindrome (center at i)
        start, end = expand(i, i)
        if end - start > best_end - best_start:
            best_start, best_end = start, end

        # Even length palindrome (center between i and i+1)
        start, end = expand(i, i + 1)
        if end - start > best_end - best_start:
            best_start, best_end = start, end

    return s[best_start:best_end]
```

### Palindrome Partitioning
```python
def partition(s: str) -> list[list[str]]:
    """
    Partition string into all possible palindrome substrings.

    Time: O(n × 2^n) - exponential partitions
    Space: O(n) - recursion depth
    """
    def is_palindrome(start: int, end: int) -> bool:
        while start < end:
            if s[start] != s[end]:
                return False
            start += 1
            end -= 1
        return True

    def backtrack(start: int, path: list[str]):
        if start == len(s):
            result.append(path[:])
            return

        for end in range(start, len(s)):
            if is_palindrome(start, end):
                path.append(s[start:end + 1])
                backtrack(end + 1, path)
                path.pop()

    result = []
    backtrack(0, [])
    return result
```

## Related Problems

- **Valid Palindrome II** - Allow one deletion
- **Palindrome Number** - Integer palindrome check
- **Longest Palindromic Substring** - Find longest palindrome
- **Palindrome Partitioning** - Split into palindrome substrings
- **Shortest Palindrome** - Add chars to make palindrome
- **Palindrome Pairs** - Find word pairs forming palindrome
