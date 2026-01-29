# Permutations - Solutions

This document provides optimal solutions and detailed explanations for the practice problems related to Permutations.

---

## 1. Permutations

### Problem Statement

Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in any order.

### Examples & Edge Cases

- **Input:** nums = [1,2,3] → **Output:** [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
- **Input:** nums = [0,1] → **Output:** [[0,1],[1,0]]
- **Edge Case:** Single element array → [[1]]

### Optimal Python Solution (Backtracking with Used Set)

```python
def permute(nums: list[int]) -> list[list[int]]:
    result = []
    used = [False] * len(nums)

    def backtrack(current: list[int]):
        if len(current) == len(nums):
            result.append(current[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue

            used[i] = True
            current.append(nums[i])
            backtrack(current)
            current.pop()
            used[i] = False

    backtrack([])
    return result
```

### Detailed Explanation

1. **Decision Tree**: At each position in our permutation, we can pick any number that hasn't been used yet.
2. **State Tracking**: We use a `used` boolean array (or a set) to track which indices have already been included in the current path.
3. **Base Case**: Once the `current` list length matches the input `nums` length, we have a complete permutation.

### Complexity Analysis

- **Time Complexity:** $O(n \cdot n!)$ - There are $n!$ permutations, and copying each takes $O(n)$.
- **Space Complexity:** $O(n)$ - For the recursion stack and the `used` array.

---

## 2. Permutations II

### Problem Statement

Given a collection of numbers, `nums`, that might contain duplicates, return all possible unique permutations in any order.

### Examples & Edge Cases

- **Input:** nums = [1,1,2] → **Output:** [[1,1,2],[1,2,1],[2,1,1]]
- **Edge Case:** All elements are the same: [1,1,1] → [[1,1,1]].

### Optimal Python Solution (Backtracking with Sorting)

```python
def permuteUnique(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    used = [False] * len(nums)

    def backtrack(current: list[int]):
        if len(current) == len(nums):
            result.append(current[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue

            # Key Duplicate Prevention:
            # If nums[i] == nums[i-1] AND nums[i-1] was NOT used in this branch,
            # it means we are trying to start a duplicate path at the same level.
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue

            used[i] = True
            current.append(nums[i])
            backtrack(current)
            current.pop()
            used[i] = False

    backtrack([])
    return result
```

### Detailed Explanation

1. **Sorting**: Crucial to group duplicates.
2. **The "not used[i-1]" Trick**: When we encounter a duplicate `nums[i] == nums[i-1]`, we only allow `nums[i]` to be used if `nums[i-1]` is _already_ used. If `nums[i-1]` is NOT used, it means we just finished exploring all branches starting with `nums[i-1]` and are about to start the exact same set of branches with `nums[i]`. We skip to avoid duplicates.

### Complexity Analysis

- **Time Complexity:** $O(n \cdot n!)$ - Still factorial in the worst case.
- **Space Complexity:** $O(n)$ - For recursion stack and tracking.

---

## 3. Next Permutation

### Problem Statement

Implement next permutation, which rearranges numbers into the lexicographically next greater permutation of numbers. If such an arrangement is not possible, it must rearrange it as the lowest possible order (i.e., sorted in ascending order). The replacement must be in place.

### Examples & Edge Cases

- **Input:** [1,2,3] → **Output:** [1,3,2]
- **Input:** [3,2,1] → **Output:** [1,2,3]
- **Input:** [1,1,5] → **Output:** [1,5,1]

### Optimal Python Solution (Pattern Recognition)

```python
def nextPermutation(nums: list[int]) -> None:
    n = len(nums)
    # 1. Find the first pair nums[i] < nums[i+1] from the right
    i = n - 2
    while i >= 0 and nums[i] >= nums[i+1]:
        i -= 1

    if i >= 0:
        # 2. Find the smallest number larger than nums[i] to its right
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        # 3. Swap them
        nums[i], nums[j] = nums[j], nums[i]

    # 4. Reverse the suffix to get the smallest possible tail
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
```

### Detailed Explanation

1. **Find Pivot**: Scanning from right, find the first number that is smaller than its successor. This number needs to be increased to get the next permutation.
2. **Find Successor**: Find the smallest number to the right of the pivot that is still larger than the pivot.
3. **Swap**: Swapping these two makes the prefix lexicographically larger.
4. **Minimize Suffix**: After swapping, the suffix is still in descending order. Reversing it makes it ascending (the smallest possible arrangement for those numbers), giving us the _immediate_ next permutation.

### Complexity Analysis

- **Time Complexity:** $O(n)$ - Three linear passes at most.
- **Space Complexity:** $O(1)$ - In-place modification.

---

## 4. Permutation Sequence (Kth Permutation)

### Problem Statement

The set `[1, 2, 3, ..., n]` contains a total of `n!` unique permutations. By listing and labeling all of the permutations in order, we get the sequence for `n = 3`: `123, 132, 213, 231, 312, 321`. Given `n` and `k`, return the `kth` permutation sequence.

### Examples & Edge Cases

- **Input:** n = 3, k = 3 → **Output:** "213"
- **Input:** n = 4, k = 9 → **Output:** "2314"

### Optimal Python Solution (Factorial Number System)

```python
import math

def getPermutation(n: int, k: int) -> str:
    numbers = [str(i) for i in range(1, n + 1)]
    k -= 1 # 0-indexed
    res = []

    for i in range(n, 0, -1):
        # Number of permutations for each choice of the current digit
        # is (i-1)!
        fact = math.factorial(i - 1)
        index = k // fact
        res.append(numbers.pop(index))
        k %= fact

    return "".join(res)
```

### Detailed Explanation

1. **Block Logic**: For `n=3`, there are `2! = 2` permutations starting with '1', two starting with '2', and two starting with '3'.
2. **Indexing**: If `k=3` (0-indexed `k=2`), we know it must be in the second block (starting with '2') because $2 // 2! = 1$ (index 1 in `['1','2','3']`).
3. **Refining**: Once we pick a digit, we update `k` using modulo and repeat the process for the remaining digits.

### Complexity Analysis

- **Time Complexity:** $O(n^2)$ - We iterate $n$ times, and `pop(index)` from a list is $O(n)$.
- **Space Complexity:** $O(n)$ - To store the list of numbers and the result.

---

## 5. Palindrome Permutation II

### Problem Statement

Given a string `s`, return all the palindromic permutations (without duplicates) of it. Return an empty list if no palindromic permutation can be formed.

### Examples & Edge Cases

- **Input:** "aabb" → **Output:** ["abba", "baab"]
- **Input:** "abc" → **Output:** []

### Optimal Python Solution (Backtracking on Half-String)

```python
from collections import Counter

def generatePalindromes(s: str) -> list[str]:
    count = Counter(s)
    odd_chars = [c for c, freq in count.items() if freq % 2 != 0]

    # A palindrome can have at most one character with an odd frequency
    if len(odd_chars) > 1:
        return []

    mid = odd_chars[0] if odd_chars else ""
    # We only need to permute half of the characters
    half_chars = []
    for c, freq in count.items():
        half_chars.extend([c] * (freq // 2))

    res = []
    used = [False] * len(half_chars)

    def backtrack(current: list[str]):
        if len(current) == len(half_chars):
            s_half = "".join(current)
            res.append(s_half + mid + s_half[::-1])
            return

        for i in range(len(half_chars)):
            if used[i]: continue
            if i > 0 and half_chars[i] == half_chars[i-1] and not used[i-1]:
                continue

            used[i] = True
            current.append(half_chars[i])
            backtrack(current)
            current.pop()
            used[i] = False

    half_chars.sort()
    backtrack([])
    return res
```

### Detailed Explanation

1. **Feasibility Check**: A palindrome can only be formed if at most one character appears an odd number of times.
2. **Construction**: The middle character (if any) is fixed. We only need to generate all unique permutations of the _half_ set of characters and then mirror them.
3. **Efficiency**: Permuting half the characters is significantly faster than permuting the full string ($O((n/2)!)$ vs $O(n!)$).

### Complexity Analysis

- **Time Complexity:** $O((n/2) \cdot (n/2)!)$ - Generating permutations of the half-string.
- **Space Complexity:** $O(n)$ - For the character counts and recursion stack.
