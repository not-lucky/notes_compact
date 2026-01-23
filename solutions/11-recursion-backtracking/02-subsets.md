# Solution: Subsets (Power Set) Practice Problems

## Problem 1: Subsets
### Problem Statement
Given an integer array `nums` of unique elements, return all possible subsets (the power set).
The solution set must not contain duplicate subsets. Return the solution in any order.

### Constraints
- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
- All the numbers of `nums` are unique.

### Example
Input: `nums = [1,2,3]`
Output: `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`

### Python Implementation
```python
def subsets(nums: list[int]) -> list[list[int]]:
    """
    Time Complexity: O(n * 2^n)
    Space Complexity: O(n)
    """
    res = []
    subset = []

    def backtrack(i):
        if i >= len(nums):
            res.append(subset.copy())
            return

        # Decision to include nums[i]
        subset.append(nums[i])
        backtrack(i + 1)

        # Decision NOT to include nums[i]
        subset.pop()
        backtrack(i + 1)

    backtrack(0)
    return res
```

---

## Problem 2: Subsets II
### Problem Statement
Given an integer array `nums` that may contain duplicates, return all possible subsets (the power set).
The solution set must not contain duplicate subsets. Return the solution in any order.

### Constraints
- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`

### Example
Input: `nums = [1,2,2]`
Output: `[[],[1],[1,2],[1,2,2],[2],[2,2]]`

### Python Implementation
```python
def subsetsWithDup(nums: list[int]) -> list[list[int]]:
    """
    Time Complexity: O(n * 2^n)
    Space Complexity: O(n)
    """
    res = []
    nums.sort()

    def backtrack(i, subset):
        if i == len(nums):
            res.append(subset.copy())
            return

        # All subsets that include nums[i]
        subset.append(nums[i])
        backtrack(i + 1, subset)
        subset.pop()

        # All subsets that don't include nums[i]
        while i + 1 < len(nums) and nums[i] == nums[i + 1]:
            i += 1
        backtrack(i + 1, subset)

    backtrack(0, [])
    return res
```

---

## Problem 3: Letter Case Permutation
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

## Problem 4: Combinations (Subsets of length K)
### Problem Statement
Given two integers `n` and `k`, return all possible combinations of `k` numbers chosen from the range `[1, n]`.
You may return the answer in any order.

### Constraints
- `1 <= n <= 20`
- `1 <= k <= n`

### Example
Input: `n = 4, k = 2`
Output: `[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]`

### Python Implementation
```python
def combine(n: int, k: int) -> list[list[int]]:
    """
    Time Complexity: O(k * C(n, k))
    Space Complexity: O(k)
    """
    res = []

    def backtrack(start, combo):
        if len(combo) == k:
            res.append(combo.copy())
            return

        for i in range(start, n + 1):
            combo.append(i)
            backtrack(i + 1, combo)
            combo.pop()

    backtrack(1, [])
    return res
```
