# Combinations

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md), [Subsets](./02-subsets.md)

## Overview

Combinations are about choosing k elements from n where **order doesn't matter**. It's the "pick a team" problem: choosing 3 players from 10 is the same regardless of the order you pick them. This pattern appears whenever you need to select a fixed-size group from a larger set.

## Building Intuition

**Why does the "start index + size limit" pattern work?**

Think of combinations as subsets with a constraint: we only want subsets of exactly size k.

1. **The Team Selection Model**: Imagine picking a 3-person team from 10 candidates. You can use the subsets approach (include/exclude each person), but only save teams of exactly 3. The "start index" ensures you don't count {Alice, Bob} and {Bob, Alice} as different teams.

2. **The Key Mental Model**: Line up all candidates in order. For each combination, you're essentially saying "I'll take candidates at positions i, j, k where i < j < k." The ordering constraint (i < j < k) is enforced by the start index.

3. **Why C(n,k) Combinations?**: C(n,k) = n! / (k! × (n-k)!)
   - The numerator n! counts all orderings
   - Dividing by k! removes duplicate orderings of the chosen k
   - Dividing by (n-k)! removes orderings of the unchosen

4. **Visual Intuition—Pruned Subset Tree**:
```
n=4, k=2: Choose 2 from {1,2,3,4}

Start with {} (need 2 more)
├── Add 1 → {1} (need 1 more)
│   ├── Add 2 → {1,2} ✓ size=k, save!
│   ├── Add 3 → {1,3} ✓ save!
│   └── Add 4 → {1,4} ✓ save!
├── Add 2 → {2} (need 1 more)
│   ├── Add 3 → {2,3} ✓ save!
│   └── Add 4 → {2,4} ✓ save!
├── Add 3 → {3} (need 1 more)
│   └── Add 4 → {3,4} ✓ save!
└── Add 4 → {4} (need 1 more)
    └── No more elements! (pruned)
```

5. **The Pruning Insight**: If you need k elements and only have fewer than k remaining, stop early. This "not enough elements" pruning is the key optimization. Without it, you'd explore many dead-end branches.

## When NOT to Use Combinations Pattern

Combinations are powerful but have specific use cases:

1. **When Order Matters**: If picking A then B is different from B then A, use permutations. Combinations treat {A,B} and {B,A} as identical.

2. **When Size Isn't Fixed**: If you need all subset sizes (not just k), use the general subsets pattern. Combinations are specifically for fixed-size selection.

3. **When k Is Close to n/2**: C(n, n/2) is the largest binomial coefficient. For n=20 and k=10, C(20,10) ≈ 184,756. If constraints allow, this might be manageable, but be aware of the growth.

4. **When Elements Can Repeat**: Standard combinations assume each element is chosen at most once. For "combinations with replacement," use a different formula and algorithm.

5. **When You Need Weighted Selection**: If elements have weights or costs and you want the "best" combination, consider DP or greedy approaches rather than enumerating all.

**Red Flags Against Generating All Combinations:**
- n and k are large (C(n,k) > 10^7) → too many combinations
- Problem asks for "optimal" → probably DP or greedy
- Problem asks for count → use math formula directly
- Elements can be chosen multiple times → different problem

**Better Alternatives:**
| Situation | Use Instead |
|-----------|-------------|
| Order matters | Permutations |
| All sizes needed | Subsets |
| Need optimal combination | DP/Greedy |
| Just counting | Math: C(n,k) = n!/(k!(n-k)!) |
| With replacement | Stars and bars / different algorithm |

---

## Interview Context

Combination problems test:
1. **Subset selection**: Choose k elements from n
2. **Order independence**: [1,2] and [2,1] are the same combination
3. **Pruning ability**: Skip when not enough elements remain
4. **Mathematical insight**: Understanding C(n,k) = n! / (k!(n-k)!)

---

## Problem Statement

Given n and k, return all combinations of k numbers from [1, n].

```
Input: n = 4, k = 2
Output: [[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]
```

There are C(n,k) combinations.

---

## The Core Insight

Combinations are like subsets, but we only keep subsets of exactly size k.

```
n = 4, k = 2

                    []
           /    /    \    \
         [1]   [2]   [3]   [4]
        / | \   | \    \
    [1,2][1,3][1,4][2,3][2,4][3,4]  ← only these (size = k)
```

Key difference from subsets: we only save when `len(current) == k`.

---

## Approach 1: Backtracking

```python
def combine(n: int, k: int) -> list[list[int]]:
    """
    Generate all combinations of k numbers from 1 to n.

    Time: O(k × C(n,k)) - C(n,k) combinations, O(k) to copy each
    Space: O(k) - recursion depth
    """
    result = []

    def backtrack(start: int, current: list[int]):
        # Base case: combination complete
        if len(current) == k:
            result.append(current[:])
            return

        # Try each number from start to n
        for i in range(start, n + 1):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()

    backtrack(1, [])
    return result
```

### Visual Trace

```
n = 4, k = 2

backtrack(1, [])
├── i=1: [1] → backtrack(2, [1])
│   ├── i=2: [1,2] → len=2, save [1,2] ✓
│   ├── i=3: [1,3] → len=2, save [1,3] ✓
│   └── i=4: [1,4] → len=2, save [1,4] ✓
├── i=2: [2] → backtrack(3, [2])
│   ├── i=3: [2,3] → len=2, save [2,3] ✓
│   └── i=4: [2,4] → len=2, save [2,4] ✓
├── i=3: [3] → backtrack(4, [3])
│   └── i=4: [3,4] → len=2, save [3,4] ✓
└── i=4: [4] → backtrack(5, [4])
    └── no more elements, can't reach k=2
```

---

## Approach 2: With Pruning

We can skip early if there aren't enough elements left to complete the combination.

```python
def combine_pruned(n: int, k: int) -> list[list[int]]:
    """
    Generate combinations with pruning optimization.

    Pruning: If we need (k - len(current)) more elements,
    we must have at least that many elements remaining.

    Time: O(k × C(n,k)) - but fewer recursive calls
    Space: O(k)
    """
    result = []

    def backtrack(start: int, current: list[int]):
        if len(current) == k:
            result.append(current[:])
            return

        # Pruning: need (k - len(current)) more elements
        # Available: n - start + 1 elements
        need = k - len(current)
        available = n - start + 1

        if available < need:
            return  # Can't possibly complete

        for i in range(start, n + 1):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()

    backtrack(1, [])
    return result
```

### Alternative: Adjust Loop Upper Bound

```python
def combine_pruned_v2(n: int, k: int) -> list[list[int]]:
    """Prune by adjusting loop range."""
    result = []

    def backtrack(start: int, current: list[int]):
        if len(current) == k:
            result.append(current[:])
            return

        # Upper bound: n - (k - len(current)) + 1
        # This ensures enough elements remain
        need = k - len(current)
        for i in range(start, n - need + 2):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()

    backtrack(1, [])
    return result
```

---

## Approach 3: Iterative

Build combinations level by level.

```python
def combine_iterative(n: int, k: int) -> list[list[int]]:
    """
    Generate combinations iteratively.

    Time: O(k × C(n,k))
    Space: O(C(n,k)) for result
    """
    result = [[]]

    for _ in range(k):
        new_result = []
        for combo in result:
            # Get the last element (or 0 if empty)
            start = combo[-1] + 1 if combo else 1
            for num in range(start, n + 1):
                new_result.append(combo + [num])
        result = new_result

    return result
```

---

## Combinations from Array

Instead of [1, n], choose k elements from an array.

```python
def combine_array(nums: list[int], k: int) -> list[list[int]]:
    """
    Choose k elements from nums array.

    Time: O(k × C(n,k))
    Space: O(k)
    """
    result = []

    def backtrack(start: int, current: list[int]):
        if len(current) == k:
            result.append(current[:])
            return

        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result
```

---

## Combinations vs Subsets vs Permutations

| Aspect | Subsets | Combinations | Permutations |
|--------|---------|--------------|--------------|
| Size | All sizes | Exactly k | Exactly n |
| Order | No | No | Yes |
| Count | 2^n | C(n,k) | n! |
| Example | {}, {1}, {1,2} | {1,2}, {1,3} | [1,2], [2,1] |

---

## Mathematical Background

The number of ways to choose k items from n:

```
C(n, k) = n! / (k! × (n-k)!)

Examples:
C(4, 2) = 4! / (2! × 2!) = 24 / 4 = 6
C(5, 3) = 5! / (3! × 2!) = 120 / 12 = 10
C(n, 0) = 1 (empty set)
C(n, n) = 1 (full set)
C(n, 1) = n (choose one)
```

Pascal's Triangle relation:
```
C(n, k) = C(n-1, k-1) + C(n-1, k)
```

---

## Python's itertools

For production code, use the standard library:

```python
from itertools import combinations

# Generate all 2-element combinations from [1,2,3,4]
list(combinations([1, 2, 3, 4], 2))
# [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]

# With replacement (allows repeats)
from itertools import combinations_with_replacement
list(combinations_with_replacement([1, 2, 3], 2))
# [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
```

---

## Common Variations

### 1. Combinations with Duplicates in Input

```python
def combine_with_dup(nums: list[int], k: int) -> list[list[int]]:
    """Handle duplicate elements in input."""
    nums.sort()
    result = []

    def backtrack(start: int, current: list[int]):
        if len(current) == k:
            result.append(current[:])
            return

        for i in range(start, len(nums)):
            # Skip duplicates at same level
            if i > start and nums[i] == nums[i-1]:
                continue
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result
```

### 2. K-Combinations That Sum to Target

```python
def combine_sum_k(nums: list[int], k: int, target: int) -> list[list[int]]:
    """Find k-element combinations that sum to target."""
    nums.sort()
    result = []

    def backtrack(start: int, current: list[int], remaining: int):
        if len(current) == k:
            if remaining == 0:
                result.append(current[:])
            return

        for i in range(start, len(nums)):
            if nums[i] > remaining:
                break  # Pruning: sorted, so all following are too large
            current.append(nums[i])
            backtrack(i + 1, current, remaining - nums[i])
            current.pop()

    backtrack(0, [], target)
    return result
```

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Generate C(n,k) | O(k × C(n,k)) | O(k) | O(k) per combination |
| With pruning | O(k × C(n,k)) | O(k) | Fewer recursive calls |
| Using itertools | O(k × C(n,k)) | O(1) | Iterator, memory efficient |

---

## Edge Cases

- [ ] k = 0 → return [[]]
- [ ] k > n → return []
- [ ] k = n → return [[1,2,...,n]]
- [ ] n = 0, k = 0 → return [[]]

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Combinations | Medium | Basic backtracking |
| 2 | Combination Sum III | Medium | k numbers that sum to n |
| 3 | Factor Combinations | Medium | Prime factorization |
| 4 | Combination Iterator | Medium | Design pattern |

---

## Interview Tips

1. **State the count**: Mention C(n,k) combinations expected
2. **Add pruning**: Show you can optimize with early termination
3. **Clarify constraints**: Ask about duplicates in input
4. **Compare to subsets**: Show understanding of the relationship
5. **Know itertools**: Mention Python's built-in for production

---

## Key Takeaways

1. Combinations = subsets of exactly size k
2. Use `start` parameter to ensure order independence
3. Prune when not enough elements remain to reach k
4. C(n,k) is the expected number of results
5. Related to Pascal's Triangle: C(n,k) = C(n-1,k-1) + C(n-1,k)

---

## Next: [05-combination-sum.md](./05-combination-sum.md)

Learn about combination sum variants with target sums.
