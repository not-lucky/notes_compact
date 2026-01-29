# Combinations - Solutions

This document provides optimal solutions and detailed explanations for the practice problems related to Combinations.

---

## 1. Combinations

### Problem Statement

Given two integers `n` and `k`, return all possible combinations of `k` numbers out of the range `[1, n]`. You may return the answer in any order.

### Examples & Edge Cases

- **Input:** n = 4, k = 2 → **Output:** [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
- **Input:** n = 1, k = 1 → **Output:** [[1]]
- **Edge Case:** k = 0 (result: [[]]), k > n (result: []).

### Optimal Python Solution (Backtracking with Pruning)

```python
def combine(n: int, k: int) -> list[list[int]]:
    res = []

    def backtrack(start: int, current: list[int]):
        # Base Case: found a combination of size k
        if len(current) == k:
            res.append(current[:])
            return

        # Pruning:
        # We need (k - len(current)) more elements.
        # If there aren't enough elements left in [start, n], stop.
        # Elements available: n - start + 1
        # Elements needed: k - len(current)
        for i in range(start, n + 1):
            if (n - i + 1) < (k - len(current)):
                break

            current.append(i)
            backtrack(i + 1, current)
            current.pop()

    backtrack(1, [])
    return res
```

### Detailed Explanation

1. **Decision Tree**: At each step, we choose a number `i` from the range `[start, n]`.
2. **Order Independence**: By always picking the next number from `i + 1`, we ensure the combinations are always in ascending order, which prevents duplicates like `[1,2]` and `[2,1]`.
3. **Pruning**: The condition `if (n - i + 1) < (k - len(current)): break` stops the recursion if we've reached a point where it's mathematically impossible to finish the combination.

### Complexity Analysis

- **Time Complexity:** $O(k \cdot \binom{n}{k})$ - $\binom{n}{k}$ is the number of combinations, and each takes $O(k)$ to copy.
- **Space Complexity:** $O(k)$ - The maximum depth of the recursion stack.

---

## 2. Combination Sum III

### Problem Statement

Find all valid combinations of `k` numbers that sum up to `n` such that the following conditions are true:

1. Only numbers `1` through `9` are used.
2. Each number is used at most once.
   Return a list of all possible valid combinations.

### Examples & Edge Cases

- **Input:** k = 3, n = 7 → **Output:** [[1,2,4]]
- **Input:** k = 3, n = 9 → **Output:** [[1,2,6],[1,3,5],[2,3,4]]
- **Edge Case:** n is too small or too large to be formed by k distinct digits.

### Optimal Python Solution (Backtracking)

```python
def combinationSum3(k: int, n: int) -> list[list[int]]:
    res = []

    def backtrack(start: int, current: list[int], target: int):
        # Base Case: used k numbers
        if len(current) == k:
            if target == 0:
                res.append(current[:])
            return

        # Optimization: if target < 0, this branch is invalid
        if target < 0:
            return

        for i in range(start, 10): # Numbers 1-9
            # Pruning: since i increases, if i > target, no future i will work
            if i > target:
                break

            current.append(i)
            backtrack(i + 1, current, target - i)
            current.pop()

    backtrack(1, [], n)
    return res
```

### Detailed Explanation

1. **Double Constraint**: We must satisfy both the count (`len == k`) and the sum (`target == 0`).
2. **Backtracking**: We pick a number, subtract it from the target, and move to the next available number.
3. **Pruning**: Since we process numbers in increasing order, once a number `i` exceeds the remaining `target`, we can stop the loop for the current level.

### Complexity Analysis

- **Time Complexity:** $O(\binom{9}{k} \cdot k)$ - We are choosing `k` numbers from a fixed pool of 9.
- **Space Complexity:** $O(k)$ - Recursion depth.

---

## 3. Factor Combinations

### Problem Statement

Write a function that takes an integer `n` and return all possible combinations of its factors. Numbers should be in the range `[2, n-1]`.

### Examples & Edge Cases

- **Input:** 12 → **Output:** [[2,6],[2,2,3],[3,4]]
- **Input:** 37 → **Output:** [] (Prime number)
- **Input:** 1 → **Output:** []

### Optimal Python Solution (Backtracking)

```python
def getFactors(n: int) -> list[list[int]]:
    res = []

    def backtrack(start: int, target: int, current: list[int]):
        # Find factors starting from 'start' to avoid duplicates
        # We only go up to sqrt(target) to find the first factor of a pair
        i = start
        while i * i <= target:
            if target % i == 0:
                # If i is a factor, [i, target//i] is a valid combination
                res.append(current + [i, target // i])

                # Recursively find factors for the second part of the pair
                current.append(i)
                backtrack(i, target // i, current)
                current.pop()
            i += 1

    backtrack(2, n, [])
    return res
```

### Detailed Explanation

1. **Factor Pairs**: For any factor `i`, there is a corresponding factor `target // i`.
2. **Recursive Decomposition**: After finding a factor `i`, we can either stop (adding the pair `[i, target // i]`) or continue decomposing `target // i` into further factors.
3. **Avoiding Duplicates**: By passing `i` as the `start` for the next recursive call, we ensure that factors are chosen in non-decreasing order (e.g., we get `[2,2,3]` but not `[2,3,2]`).

### Complexity Analysis

- **Time Complexity:** $O(2^{\text{number of factors}})$ - Roughly exponential in terms of the number of divisors.
- **Space Complexity:** $O(\log n)$ - The recursion depth is bounded by the number of factors.

---

## 4. Combination Iterator

### Problem Statement

Design an Iterator class, which has:

- A constructor that takes a string `characters` of sorted distinct lowercase English letters and a number `combinationLength` as arguments.
- A function `next()` that returns the next combination of length `combinationLength` in lexicographical order.
- A function `hasNext()` that returns `true` if and only if there exists a next combination.

### Examples & Edge Cases

- **Input:** "abc", 2 → `next()`: "ab", "ac", "bc"; `hasNext()`: T, T, F.

### Optimal Python Solution (Pre-computation)

```python
class CombinationIterator:
    def __init__(self, characters: str, combinationLength: int):
        self.combinations = []
        self.index = 0

        # Generate all combinations once and store them
        def backtrack(start, current):
            if len(current) == combinationLength:
                self.combinations.append("".join(current))
                return

            for i in range(start, len(characters)):
                current.append(characters[i])
                backtrack(i + 1, current)
                current.pop()

        backtrack(0, [])

    def next(self) -> str:
        res = self.combinations[self.index]
        self.index += 1
        return res

    def hasNext(self) -> bool:
        return self.index < len(self.combinations)
```

### Detailed Explanation

1. **Pre-generation**: Since the number of combinations is usually manageable for interview constraints, generating them all upfront in the constructor is the simplest approach.
2. **Pointer**: Maintain an `index` pointer to keep track of the current position for `next()` calls.
3. **Lexicographical Order**: Because the input `characters` is sorted, the standard backtracking approach naturally generates combinations in lexicographical order.

### Complexity Analysis

- **Time Complexity:** $O(\binom{n}{k})$ for initialization, $O(1)$ for `next` and `hasNext`.
- **Space Complexity:** $O(\binom{n}{k})$ to store all combinations.
