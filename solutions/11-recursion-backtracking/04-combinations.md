# Solution: Combinations Practice Problems

## Problem 1: Combinations
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

        # Pruning: only iterate if enough numbers left to reach k
        # remaining_needed = k - len(combo)
        # numbers_left = n - i + 1
        # n - i + 1 >= k - len(combo)  =>  i <= n - k + len(combo) + 1
        for i in range(start, n - (k - len(combo)) + 2):
            combo.append(i)
            backtrack(i + 1, combo)
            combo.pop()

    backtrack(1, [])
    return res
```

---

## Problem 2: Combination Sum III
### Problem Statement
Find all valid combinations of `k` numbers that sum up to `n` such that the following conditions are true:
- Only numbers `1` through `9` are used.
- Each number is used at most once.
Return a list of all possible valid combinations. The list must not contain the same combination twice, and the combinations may be returned in any order.

### Constraints
- `2 <= k <= 9`
- `1 <= n <= 60`

### Example
Input: `k = 3, n = 7`
Output: `[[1,2,4]]`

### Python Implementation
```python
def combinationSum3(k: int, n: int) -> list[list[int]]:
    """
    Time Complexity: O(C(9, k))
    Space Complexity: O(k)
    """
    res = []

    def backtrack(start, combo, target):
        if len(combo) == k:
            if target == 0:
                res.append(combo.copy())
            return

        if target < 0:
            return

        for i in range(start, 10):
            if i > target:
                break
            combo.append(i)
            backtrack(i + 1, combo, target - i)
            combo.pop()

    backtrack(1, [], n)
    return res
```

---

## Problem 3: Factor Combinations
### Problem Statement
Numbers can be regarded as the product of their factors.
For example, `8 = 2 x 2 x 2 = 2 x 4`.
Write a function that takes an integer `n` and return all possible combinations of its factors.

### Constraints
- `n` is always positive.
- Factors should be in the range `(1, n)`.

### Example
Input: `n = 12`
Output: `[[2,6],[2,2,3],[3,4]]`

### Python Implementation
```python
def getFactors(n: int) -> list[list[int]]:
    """
    Time Complexity: O(n^(1/2) * log n)
    Space Complexity: O(log n)
    """
    res = []

    def backtrack(start, target, path):
        if path:
            res.append(path + [target])

        for i in range(start, int(target**0.5) + 1):
            if target % i == 0:
                backtrack(i, target // i, path + [i])

    backtrack(2, n, [])
    return res
```

---

## Problem 4: Combination Iterator
### Problem Statement
Design the `CombinationIterator` class:
- `CombinationIterator(string characters, int combinationLength)` Initializes the object with a string `characters` of sorted distinct lowercase English letters and a number `combinationLength` as arguments.
- `next()` Returns the next combination of length `combinationLength` in lexicographical order.
- `hasNext()` Returns `true` if and only if there exists a next combination.

### Constraints
- `1 <= combinationLength <= characters.length <= 15`
- All the characters of `characters` are unique and sorted.
- At most `10^4` calls will be made to `next` and `hasNext`.

### Example
Input: `["CombinationIterator", "next", "hasNext", "next", "hasNext", "next", "hasNext"]`, `[["abc", 2], [], [], [], [], [], []]`
Output: `[null, "ab", true, "ac", true, "bc", false]`

### Python Implementation
```python
class CombinationIterator:
    def __init__(self, characters: str, combinationLength: int):
        """
        Pre-generates all combinations.
        Space Complexity: O(C(n, k))
        """
        self.combinations = []
        self.generate(characters, combinationLength, 0, [])
        self.index = 0

    def generate(self, s, k, start, path):
        if len(path) == k:
            self.combinations.append("".join(path))
            return

        for i in range(start, len(s)):
            path.append(s[i])
            self.generate(s, k, i + 1, path)
            path.pop()

    def next(self) -> str:
        res = self.combinations[self.index]
        self.index += 1
        return res

    def hasNext(self) -> bool:
        return self.index < len(self.combinations)
```
