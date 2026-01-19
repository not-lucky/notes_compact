# Combination Sum

> **Prerequisites:** [Combinations](./04-combinations.md), [Subsets](./02-subsets.md)

## Interview Context

Combination sum problems test:
1. **Target-based search**: Find elements that sum to a target
2. **Reuse decisions**: Can elements be used multiple times?
3. **Duplicate handling**: Input duplicates vs output duplicates
4. **Pruning skills**: Early termination when sum exceeds target

---

## Problem Variants Overview

| Variant | Reuse Elements? | Input Duplicates? | Key Difference |
|---------|-----------------|-------------------|----------------|
| Combination Sum | Yes | No | Unlimited reuse |
| Combination Sum II | No | Yes | Each element once |
| Combination Sum III | No | No | k numbers from 1-9 |
| Combination Sum IV | Yes | No | Count only (DP) |

---

## Combination Sum I: Unlimited Reuse

Find all unique combinations where candidates sum to target. Each number can be used unlimited times.

```
Input: candidates = [2, 3, 6, 7], target = 7
Output: [[2, 2, 3], [7]]
```

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """
    Find combinations that sum to target (unlimited reuse).

    Time: O(n^(target/min)) - worst case, very deep recursion
    Space: O(target/min) - recursion depth
    """
    result = []

    def backtrack(start: int, current: list[int], remaining: int):
        if remaining == 0:
            result.append(current[:])
            return
        if remaining < 0:
            return

        for i in range(start, len(candidates)):
            current.append(candidates[i])
            # NOT i+1: same element can be reused
            backtrack(i, current, remaining - candidates[i])
            current.pop()

    backtrack(0, [], target)
    return result
```

### Visual Trace

```
candidates = [2, 3, 6, 7], target = 7

backtrack(0, [], 7)
├── add 2 → backtrack(0, [2], 5)
│   ├── add 2 → backtrack(0, [2,2], 3)
│   │   ├── add 2 → backtrack(0, [2,2,2], 1)
│   │   │   └── add 2 → remaining = -1, return
│   │   └── add 3 → backtrack(1, [2,2,3], 0) ✓ save [2,2,3]
│   └── add 3 → backtrack(1, [2,3], 2)
│       └── remaining never reaches 0
├── add 3 → backtrack(1, [3], 4)
│   └── ...no solution
├── add 6 → backtrack(2, [6], 1)
│   └── ...no solution
└── add 7 → backtrack(3, [7], 0) ✓ save [7]
```

### With Sorting for Better Pruning

```python
def combination_sum_optimized(candidates: list[int], target: int) -> list[list[int]]:
    """Optimized with sorting and early termination."""
    candidates.sort()  # Sort for pruning
    result = []

    def backtrack(start: int, current: list[int], remaining: int):
        if remaining == 0:
            result.append(current[:])
            return

        for i in range(start, len(candidates)):
            # Early termination: if current candidate > remaining, all following are too
            if candidates[i] > remaining:
                break

            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i])
            current.pop()

    backtrack(0, [], target)
    return result
```

---

## Combination Sum II: No Reuse, Has Duplicates

Each number can only be used once. Input may contain duplicates.

```
Input: candidates = [10, 1, 2, 7, 6, 1, 5], target = 8
Output: [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
```

```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    """
    Find combinations that sum to target (no reuse, handle duplicates).

    Time: O(2^n) - each element included or not
    Space: O(n) - recursion depth
    """
    candidates.sort()  # Must sort to handle duplicates
    result = []

    def backtrack(start: int, current: list[int], remaining: int):
        if remaining == 0:
            result.append(current[:])
            return

        for i in range(start, len(candidates)):
            # Skip duplicates at same level
            if i > start and candidates[i] == candidates[i-1]:
                continue

            # Pruning: sorted, so if current > remaining, stop
            if candidates[i] > remaining:
                break

            current.append(candidates[i])
            backtrack(i + 1, current, remaining - candidates[i])  # i+1: no reuse
            current.pop()

    backtrack(0, [], target)
    return result
```

### Why Skip Duplicates?

```
candidates = [1, 1, 6], target = 8

Without skipping:
- Start with first 1: [1] → [1,1,6] ✓
- Start with second 1: [1] → [1,1,6] ← DUPLICATE!

With skipping:
- i=0: use first 1, continue
- i=1: i > start AND candidates[1] == candidates[0], SKIP
```

---

## Combination Sum III: k Numbers from 1-9

Find k numbers from [1-9] that sum to n.

```
Input: k = 3, n = 7
Output: [[1, 2, 4]]
```

```python
def combination_sum3(k: int, n: int) -> list[list[int]]:
    """
    Find k numbers from 1-9 that sum to n.

    Time: O(C(9,k) × k)
    Space: O(k)
    """
    result = []

    def backtrack(start: int, current: list[int], remaining: int):
        if len(current) == k:
            if remaining == 0:
                result.append(current[:])
            return

        for i in range(start, 10):  # 1 to 9
            if i > remaining:
                break  # Pruning

            current.append(i)
            backtrack(i + 1, current, remaining - i)
            current.pop()

    backtrack(1, [], n)
    return result
```

---

## Combination Sum IV: Count Only (DP Approach)

Count the number of combinations (order matters, so actually permutations).

```
Input: nums = [1, 2, 3], target = 4
Output: 7
Explanation: (1,1,1,1), (1,1,2), (1,2,1), (1,3), (2,1,1), (2,2), (3,1)
```

This is actually DP, not backtracking:

```python
def combination_sum4(nums: list[int], target: int) -> int:
    """
    Count combinations (order matters).

    Time: O(target × n)
    Space: O(target)
    """
    dp = [0] * (target + 1)
    dp[0] = 1  # One way to make 0: use nothing

    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                dp[i] += dp[i - num]

    return dp[target]
```

---

## Pattern Comparison

```python
# Combination Sum I: reuse allowed
backtrack(i, current, remaining - candidates[i])  # Keep i

# Combination Sum II: no reuse
backtrack(i + 1, current, remaining - candidates[i])  # Move to i+1

# Key difference in loop:
for i in range(start, len(candidates)):
    # For II with duplicates:
    if i > start and candidates[i] == candidates[i-1]:
        continue  # Skip duplicate
```

---

## Advanced: Target Sum with Negative Numbers

When candidates can be negative, we can't prune by `candidates[i] > remaining`.

```python
def combination_sum_with_neg(candidates: list[int], target: int) -> list[list[int]]:
    """Handle negative numbers - no early termination."""
    result = []
    candidates.sort()  # Still sort for consistent ordering

    def backtrack(start: int, current: list[int], remaining: int, max_depth: int):
        if max_depth == 0:
            return  # Prevent infinite recursion

        if remaining == 0 and current:
            result.append(current[:])
            return

        for i in range(start, len(candidates)):
            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i], max_depth - 1)
            current.pop()

    backtrack(0, [], target, 20)  # Limit depth
    return result
```

---

## Complexity Analysis

| Variant | Time | Space | Notes |
|---------|------|-------|-------|
| Sum I (reuse) | O(n^(t/m)) | O(t/m) | t=target, m=min candidate |
| Sum II (no reuse) | O(2^n) | O(n) | Each element in/out |
| Sum III (1-9) | O(C(9,k) × k) | O(k) | At most C(9,k) combos |
| Sum IV (count) | O(t × n) | O(t) | DP approach |

---

## Common Mistakes

### 1. Wrong Recursion Index

```python
# Combination Sum I (reuse allowed)
backtrack(i, ...)       # Stay at i

# Combination Sum II (no reuse)
backtrack(i + 1, ...)   # Move past i
```

### 2. Forgetting to Sort

```python
# For Combination Sum II, MUST sort first
candidates.sort()  # Required for duplicate skipping
```

### 3. Wrong Duplicate Skip Condition

```python
# WRONG: skips too much
if candidates[i] == candidates[i-1]:
    continue

# CORRECT: only skip at same level
if i > start and candidates[i] == candidates[i-1]:
    continue
```

---

## Edge Cases

- [ ] Target = 0 → depends on problem (usually [[]])
- [ ] Empty candidates → return []
- [ ] No valid combination → return []
- [ ] Single candidate = target → return [[candidate]]
- [ ] All candidates > target → return []

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Combination Sum | Medium | Unlimited reuse |
| 2 | Combination Sum II | Medium | No reuse, duplicates |
| 3 | Combination Sum III | Medium | k from 1-9 |
| 4 | Combination Sum IV | Medium | DP, order matters |
| 5 | Target Sum | Medium | +/- choices |
| 6 | Coin Change 2 | Medium | Count combinations |

---

## Interview Tips

1. **Clarify reuse**: Ask if elements can be used multiple times
2. **Clarify duplicates**: Ask if input has duplicate values
3. **Sort for pruning**: Always mention sorting helps with early termination
4. **Know all variants**: Be prepared for any combination sum variant
5. **DP when counting**: If only count needed, DP is usually better

---

## Key Takeaways

1. Reuse allowed → stay at index i; no reuse → move to i+1
2. Input duplicates → sort and skip at same level
3. Always sort for better pruning
4. Combination Sum IV is DP (order matters = permutations)
5. Handle edge cases: target=0, empty input, no solution

---

## Next: [06-n-queens.md](./06-n-queens.md)

Learn about the classic N-Queens constraint satisfaction problem.
