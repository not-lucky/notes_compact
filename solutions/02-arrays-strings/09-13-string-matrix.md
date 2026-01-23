# Solution: String and Matrix Patterns

## Problem 1: Longest Palindromic Substring
Given a string `s`, return the longest palindromic substring in `s`.

### Python Implementation
```python
def longest_palindrome(s: str) -> str:
    """
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    if not s: return ""

    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l+1:r]

    res = ""
    for i in range(len(s)):
        # Odd
        p1 = expand(i, i)
        if len(p1) > len(res): res = p1
        # Even
        p2 = expand(i, i+1)
        if len(p2) > len(res): res = p2
    return res
```

---

## Problem 2: Group Anagrams
Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

### Python Implementation
```python
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Time Complexity: O(n * k log k)
    Space Complexity: O(n * k)
    """
    from collections import defaultdict
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    return list(groups.values())
```

---

## Problem 3: Spiral Matrix
Given an `m x n` matrix, return all elements of the matrix in spiral order.

### Python Implementation
```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    """
    Time Complexity: O(m * n)
    Space Complexity: O(1) (excluding result)
    """
    if not matrix: return []
    res = []
    top, bottom = 0, len(matrix)-1
    left, right = 0, len(matrix[0])-1

    while top <= bottom and left <= right:
        # Right
        for i in range(left, right + 1):
            res.append(matrix[top][i])
        top += 1
        # Down
        for i in range(top, bottom + 1):
            res.append(matrix[i][right])
        right -= 1
        # Left
        if top <= bottom:
            for i in range(right, left - 1, -1):
                res.append(matrix[bottom][i])
            bottom -= 1
        # Up
        if left <= right:
            for i in range(bottom, top - 1, -1):
                res.append(matrix[i][left])
            left += 1
    return res
```
