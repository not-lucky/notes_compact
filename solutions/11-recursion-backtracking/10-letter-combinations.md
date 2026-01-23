# Solution: Letter Combinations of a Phone Number Practice Problems

## Problem 1: Letter Combinations of a Phone Number
### Problem Statement
Given a string containing digits from `2-9` inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.

A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.
`2:abc, 3:def, 4:ghi, 5:jkl, 6:mno, 7:pqrs, 8:tuv, 9:wxyz`

### Constraints
- `0 <= digits.length <= 4`
- `digits[i]` is a digit in the range `['2', '9']`.

### Example
Input: `digits = "23"`
Output: `["ad","ae","af","bd","be","bf","cd","ce","cf"]`

### Python Implementation
```python
def letterCombinations(digits: str) -> list[str]:
    """
    Time Complexity: O(n * 4^n)
    Space Complexity: O(n)
    """
    if not digits:
        return []

    digitToChar = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
    }
    res = []

    def backtrack(i, curStr):
        if len(curStr) == len(digits):
            res.append(curStr)
            return

        for c in digitToChar[digits[i]]:
            backtrack(i + 1, curStr + c)

    backtrack(0, "")
    return res
```

---

## Problem 2: Letter Case Permutation
### Problem Statement
Given a string `s`, you can transform every letter individually to be lowercase or uppercase to create another string.
Return a list of all possible strings we could create. Return the output in any order.

### Constraints
- `1 <= s.length <= 12`
- `s` consists of lowercase English letters, uppercase English letters, and digits.

### Example
Input: `s = "a1b2"`
Output: `["a1b2","a1B2","A1b2","A1B2"]`

### Python Implementation
```python
def letterCasePermutation(s: str) -> list[str]:
    """
    Time Complexity: O(n * 2^n)
    Space Complexity: O(n * 2^n)
    """
    res = []

    def backtrack(i, current):
        if i == len(s):
            res.append(current)
            return

        if s[i].isalpha():
            # Lowercase decision
            backtrack(i + 1, current + s[i].lower())
            # Uppercase decision
            backtrack(i + 1, current + s[i].upper())
        else:
            # Digit - only one decision
            backtrack(i + 1, current + s[i])

    backtrack(0, "")
    return res
```

---

## Problem 3: Generate All Binary Strings
### Problem Statement
Given an integer `n`, return all possible binary strings of length `n`.

### Constraints
- `1 <= n <= 20`

### Example
Input: `n = 2`
Output: `["00", "01", "10", "11"]`

### Python Implementation
```python
def generateBinaryStrings(n: int) -> list[str]:
    """
    Time Complexity: O(2^n)
    Space Complexity: O(n)
    """
    res = []

    def backtrack(cur):
        if len(cur) == n:
            res.append(cur)
            return

        backtrack(cur + "0")
        backtrack(cur + "1")

    backtrack("")
    return res
```
