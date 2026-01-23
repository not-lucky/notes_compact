# Itertools Module

## Practice Problems

### 1. Subsets
**Difficulty:** Medium
**Key Technique:** combinations

```python
from itertools import combinations

def subsets(nums: list[int]) -> list[list[int]]:
    """
    Time: O(n * 2^n)
    Space: O(n * 2^n)
    """
    res = []
    for r in range(len(nums) + 1):
        for combo in combinations(nums, r):
            res.append(list(combo))
    return res
```

### 2. Permutations
**Difficulty:** Medium
**Key Technique:** permutations

```python
from itertools import permutations

def permute(nums: list[int]) -> list[list[int]]:
    """
    Time: O(n * n!)
    Space: O(n * n!)
    """
    return [list(p) for p in permutations(nums)]
```

### 3. Letter Combinations of a Phone Number
**Difficulty:** Medium
**Key Technique:** product

```python
from itertools import product

def letter_combinations(digits: str) -> list[str]:
    """
    Time: O(4^n)
    Space: O(4^n)
    """
    if not digits: return []
    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    letters = [phone[d] for d in digits]
    return [''.join(p) for p in product(*letters)]
```

### 4. Count and Say
**Difficulty:** Medium
**Key Technique:** groupby

```python
from itertools import groupby

def count_and_say(n: int) -> str:
    """
    Time: O(2^n)
    Space: O(2^n)
    """
    res = "1"
    for _ in range(n - 1):
        res = "".join(str(len(list(group))) + key for key, group in groupby(res))
    return res
```
