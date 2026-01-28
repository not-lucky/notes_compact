# Subsets (Power Set) - Solutions

This document provides optimal solutions and detailed explanations for the practice problems related to Subsets.

---

## 1. Subsets

### Problem Statement

Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.

### Examples & Edge Cases

- **Input:** nums = [1,2,3] → **Output:** `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`
- **Input:** nums = [0] → **Output:** `[[],[0]]`
- **Edge Case:** Empty array → [[]]

### Optimal Python Solution (Backtracking)

```python
def subsets(nums: list[int]) -> list[list[int]]:
    result = []

    def backtrack(start: int, current: list[int]):
        # Every state in the decision tree is a valid subset
        result.append(current[:])

        for i in range(start, len(nums)):
            current.append(nums[i])      # Include nums[i]
            backtrack(i + 1, current)    # Move to next element
            current.pop()                # Backtrack: exclude nums[i]

    backtrack(0, [])
    return result
```

### Detailed Explanation

1. **Decision Tree**: At each step, we decide whether to include an element or not. However, the `for` loop approach naturally handles the "starting point" of subsets.
2. **Backtracking**: We maintain a `current` list. We append it to `result` at every step because every prefix of a path in the decision tree represents a valid subset.
3. **Start Index**: The `start` parameter ensures we only look forward in the array, preventing duplicate combinations like `[1,2]` and `[2,1]`.

### Complexity Analysis

- **Time Complexity:** $O(n \cdot 2^n)$ - There are $2^n$ subsets, and each subset takes $O(n)$ to copy into the result list.
- **Space Complexity:** $O(n)$ - The recursion stack depth is at most $n$.

---

## 2. Subsets II

### Problem Statement

Given an integer array `nums` that may contain duplicates, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.

### Examples & Edge Cases

- **Input:** nums = [1,2,2] → **Output:** [[],[1],[1,2],[1,2,2],[2],[2,2]]
- **Edge Case:** All elements are the same: [2,2,2].

### Optimal Python Solution (Backtracking with Sorting)

```python
def subsetsWithDup(nums: list[int]) -> list[list[int]]:
    nums.sort() # Sort to group duplicates
    result = []

    def backtrack(start: int, current: list[int]):
        result.append(current[:])

        for i in range(start, len(nums)):
            # If current element is same as previous, and we are at the same level
            # of recursion (not just following a branch), skip it.
            if i > start and nums[i] == nums[i-1]:
                continue

            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result
```

### Detailed Explanation

1. **Sorting**: Sorting is crucial because it brings duplicates together.
2. **Duplicate Skipping**: Inside the loop, `if i > start and nums[i] == nums[i-1]` checks if the current element is a duplicate of the previous one _at the same level of the recursion tree_. If we just popped a `2` and the next element is also `2`, we skip it to avoid generating the same subset again.

### Complexity Analysis

- **Time Complexity:** $O(n \cdot 2^n)$ - Sorting is $O(n \log n)$, but the power set generation dominates.
- **Space Complexity:** $O(n)$ - For the recursion stack and `current` list.

---

## 3. Letter Case Permutation

### Problem Statement

Given a string `s`, you can transform every letter individually to be lowercase or uppercase to create another string. Return a list of all possible strings we could create.

### Examples & Edge Cases

- **Input:** s = "a1b2" → **Output:** ["a1b2","a1B2","A1b2","A1B2"]
- **Input:** s = "3z4" → **Output:** ["3z4","3Z4"]
- **Edge Case:** String with no letters: "123".

### Optimal Python Solution (Backtracking)

```python
def letterCasePermutation(s: str) -> list[str]:
    result = []

    def backtrack(index: int, path: list[str]):
        if index == len(s):
            result.append("".join(path))
            return

        char = s[index]

        if char.isalpha():
            # Choice 1: Lowercase
            path.append(char.lower())
            backtrack(index + 1, path)
            path.pop()

            # Choice 2: Uppercase
            path.append(char.upper())
            backtrack(index + 1, path)
            path.pop()
        else:
            # Only one choice for digits/symbols
            path.append(char)
            backtrack(index + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

### Detailed Explanation

1. **Binary Decision**: For every character, if it's a letter, we have two branches in our recursion: one where we use the lowercase version and one where we use the uppercase version.
2. **Base Case**: When `index == len(s)`, we have processed all characters and can add the current path to our results.

### Complexity Analysis

- **Time Complexity:** $O(n \cdot 2^k)$ - Where $k$ is the number of letters in the string. $2^k$ total permutations, each taking $O(n)$ to build.
- **Space Complexity:** $O(n)$ - Recursion depth equals string length.

---

## 4. Find All Subsets of Length K

### Problem Statement

Given an array `nums` and an integer `k`, return all possible subsets of length exactly `k`.

### Examples & Edge Cases

- **Input:** nums = [1,2,3,4], k = 2 → **Output:** [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
- **Edge Case:** k = 0 (result: [[]]), k > len(nums) (result: []).

### Optimal Python Solution (Backtracking with Pruning)

```python
def combine(nums: list[int], k: int) -> list[list[int]]:
    result = []
    n = len(nums)

    def backtrack(start: int, current: list[int]):
        # Base Case: Found a subset of length k
        if len(current) == k:
            result.append(current[:])
            return

        # Optimization (Pruning):
        # If the number of remaining elements plus elements already in current
        # is less than k, we can't possibly reach length k.
        # Elements needed: k - len(current)
        # Elements available: n - i
        for i in range(start, n):
            if (n - i) < (k - len(current)):
                break

            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result
```

### Detailed Explanation

1. **Target Length**: This is a variation of the general subsets problem where we only care about paths of length `k`.
2. **Pruning**: The `if (n - i) < (k - len(current))` condition is a powerful optimization. It stops the loop if there aren't enough items left in the array to reach the target size `k`.

### Complexity Analysis

- **Time Complexity:** $O(k \cdot \binom{n}{k})$ - $\binom{n}{k}$ is the number of combinations.
- **Space Complexity:** $O(k)$ - For the recursion stack.
