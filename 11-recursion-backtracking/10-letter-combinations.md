# Letter Combinations of a Phone Number

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md), [Combinations](./04-combinations.md)

## Interview Context

This classic problem tests:
1. **Mapping understanding**: Digit to letters mapping
2. **Cartesian product**: Generate all combinations across groups
3. **Clean backtracking**: Simple state management
4. **Iterative alternative**: Can be solved without recursion

---

## Problem Statement

Given a string of digits 2-9, return all letter combinations the number could represent (like phone keypads).

```
Keypad mapping:
2 → abc    5 → jkl    8 → tuv
3 → def    6 → mno    9 → wxyz
4 → ghi    7 → pqrs

Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Input: digits = "2"
Output: ["a","b","c"]
```

---

## The Core Insight

For each digit, try all its letters. Build combinations by exploring all paths.

```
digits = "23"

                  ""
          /       |       \
         a        b        c        (digit 2: abc)
       / | \    / | \    / | \
      d  e  f  d  e  f  d  e  f    (digit 3: def)

Result: ad, ae, af, bd, be, bf, cd, ce, cf
```

This is a Cartesian product of letter sets.

---

## Approach 1: Backtracking (Recommended)

```python
def letter_combinations(digits: str) -> list[str]:
    """
    Generate all letter combinations for phone digits.

    Time: O(4^n × n) - worst case 4 letters per digit, n digits
    Space: O(n) - recursion depth
    """
    if not digits:
        return []

    phone_map = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    result = []

    def backtrack(index: int, current: str):
        # Base case: used all digits
        if index == len(digits):
            result.append(current)
            return

        # Get letters for current digit
        letters = phone_map[digits[index]]

        # Try each letter
        for letter in letters:
            backtrack(index + 1, current + letter)

    backtrack(0, '')
    return result
```

### Visual Trace

```
digits = "23"

backtrack(0, "")
├── letter 'a': backtrack(1, "a")
│   ├── letter 'd': backtrack(2, "ad") → save "ad"
│   ├── letter 'e': backtrack(2, "ae") → save "ae"
│   └── letter 'f': backtrack(2, "af") → save "af"
├── letter 'b': backtrack(1, "b")
│   ├── letter 'd': backtrack(2, "bd") → save "bd"
│   ├── letter 'e': backtrack(2, "be") → save "be"
│   └── letter 'f': backtrack(2, "bf") → save "bf"
└── letter 'c': backtrack(1, "c")
    ├── letter 'd': backtrack(2, "cd") → save "cd"
    ├── letter 'e': backtrack(2, "ce") → save "ce"
    └── letter 'f': backtrack(2, "cf") → save "cf"
```

---

## Approach 2: Using List (More Efficient)

```python
def letter_combinations_v2(digits: str) -> list[str]:
    """Using list for efficient string building."""
    if not digits:
        return []

    phone_map = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    result = []

    def backtrack(index: int, current: list[str]):
        if index == len(digits):
            result.append(''.join(current))
            return

        for letter in phone_map[digits[index]]:
            current.append(letter)
            backtrack(index + 1, current)
            current.pop()  # Backtrack

    backtrack(0, [])
    return result
```

---

## Approach 3: Iterative (BFS-like)

Build combinations level by level.

```python
def letter_combinations_iterative(digits: str) -> list[str]:
    """
    Generate combinations iteratively.

    Time: O(4^n × n)
    Space: O(4^n) - storing all combinations
    """
    if not digits:
        return []

    phone_map = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    result = ['']  # Start with empty string

    for digit in digits:
        letters = phone_map[digit]
        # Extend each existing combination with each letter
        result = [combo + letter for combo in result for letter in letters]

    return result
```

### Visual Trace

```
digits = "23"

Start: result = ['']

Process '2' (abc):
  '' + 'a' = 'a'
  '' + 'b' = 'b'
  '' + 'c' = 'c'
  result = ['a', 'b', 'c']

Process '3' (def):
  'a' + 'd' = 'ad', 'a' + 'e' = 'ae', 'a' + 'f' = 'af'
  'b' + 'd' = 'bd', 'b' + 'e' = 'be', 'b' + 'f' = 'bf'
  'c' + 'd' = 'cd', 'c' + 'e' = 'ce', 'c' + 'f' = 'cf'
  result = ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
```

---

## Approach 4: Using itertools

Python's itertools provides a clean solution.

```python
from itertools import product

def letter_combinations_product(digits: str) -> list[str]:
    """Using itertools.product for Cartesian product."""
    if not digits:
        return []

    phone_map = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    letter_groups = [phone_map[d] for d in digits]
    return [''.join(combo) for combo in product(*letter_groups)]
```

---

## Handling Edge Cases

### Empty Input

```python
if not digits:
    return []
```

### Digits with 0 or 1

Traditional phone keypads:
- 0 → usually space or nothing
- 1 → usually nothing

```python
phone_map = {
    '0': ' ',    # or ''
    '1': '',     # no letters
    '2': 'abc', ...
}

# Skip digits with no letters
if not letters:
    backtrack(index + 1, current)
```

---

## Related: T9 Predictive Text

Find words that match a digit sequence.

```python
def find_words_t9(digits: str, dictionary: set[str]) -> list[str]:
    """Find dictionary words matching digit sequence."""
    combinations = letter_combinations(digits)
    return [combo for combo in combinations if combo in dictionary]
```

For efficiency, use a Trie:

```python
def find_words_t9_trie(digits: str, trie_root) -> list[str]:
    """Find words using Trie for efficiency."""
    phone_map = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    result = []

    def dfs(index: int, node, path: list[str]):
        if index == len(digits):
            if node.is_word:
                result.append(''.join(path))
            return

        for letter in phone_map[digits[index]]:
            if letter in node.children:
                path.append(letter)
                dfs(index + 1, node.children[letter], path)
                path.pop()

    dfs(0, trie_root, [])
    return result
```

---

## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Backtracking | O(4^n × n) | O(n) | n = number of digits |
| Iterative | O(4^n × n) | O(4^n) | Stores all in memory |
| itertools | O(4^n × n) | O(4^n) | Same as iterative |

Why 4^n? Worst case is all 7s or 9s (4 letters each).

---

## Edge Cases

- [ ] Empty string → return []
- [ ] Single digit → return list of its letters
- [ ] Contains 0 or 1 → handle appropriately

---

## Common Mistakes

### 1. Forgetting Empty Check

```python
# WRONG: returns [''] instead of []
if not digits:
    return []  # Don't forget this!
```

### 2. Wrong Recursion Index

```python
# WRONG: using same index
backtrack(index, current + letter)

# CORRECT: increment index
backtrack(index + 1, current + letter)
```

### 3. Hardcoding Wrong Mapping

```python
# Make sure 7 has 4 letters (pqrs) not 3
# Make sure 9 has 4 letters (wxyz) not 3
'7': 'pqrs',  # Not 'prs'!
'9': 'wxyz',  # Not 'wxy'!
```

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Letter Combinations of Phone Number | Medium | Basic backtracking |
| 2 | Letter Case Permutation | Medium | Similar structure |
| 3 | Generate All Binary Strings | Easy | Same pattern |
| 4 | All Paths from Source to Target | Medium | Graph variant |

---

## Interview Tips

1. **Draw the keypad**: Show you know the mapping
2. **Mention both approaches**: Recursive and iterative
3. **Handle edge cases first**: Empty input check
4. **Know the complexity**: O(4^n) not O(3^n)
5. **Mention itertools**: Shows Python knowledge

---

## Key Takeaways

1. This is Cartesian product of letter groups
2. Both recursive and iterative solutions are valid
3. 7 and 9 have 4 letters (pqrs, wxyz)
4. Time complexity is O(4^n × n) worst case
5. Empty input returns empty list, not [""]

---

## Summary: Backtracking Patterns

This chapter covered the main backtracking patterns:

| Pattern | Example Problems | Key Technique |
|---------|------------------|---------------|
| Subsets | Power set, Subsets II | Include/exclude each element |
| Permutations | All orderings | Track used elements |
| Combinations | Choose k from n | Start index to avoid duplicates |
| Constraint Satisfaction | N-Queens, Sudoku | Validate before placing |
| Grid Search | Word Search | Mark visited, backtrack |
| Sequence Generation | Parentheses, Phone | Build valid sequences |

Master these patterns and you'll handle most backtracking problems in interviews!
