# Subsets (Power Set)

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md)

## Overview

The subsets problem asks you to generate all possible subsets of a given set—this is called the **power set**. It's the foundational backtracking problem because it teaches the core "include or exclude" decision pattern that applies to many other problems.

## Building Intuition

**Why does the include/exclude pattern work?**

Think of building a subset as going through a checklist. For each item, you make a binary decision: "Should this item be in my subset?"

1. **The Binary Decision Tree**: For n elements, you make n independent yes/no decisions. Each path through the decision tree represents one unique subset. With n decisions, there are 2^n possible paths—exactly the number of subsets.

2. **The Key Mental Model**: Imagine you're at a buffet with n dishes. For each dish, you decide: take it or leave it. Every possible combination of takes and leaves gives you a different plate (subset). The empty plate (taking nothing) and the full plate (taking everything) are both valid.

3. **Why 2^n Subsets?**: Each element doubles the number of subsets. With 0 elements: 1 subset (empty). Add element A: 2 subsets ({}, {A}). Add element B: 4 subsets ({}, {A}, {B}, {A,B}). Each new element can be added to all existing subsets OR not.

4. **Visual Intuition—The Branching Tree**:

```
                    Start: {}
                   /        \
          Include 1?       Exclude 1?
              /                  \
           {1}                  {}
          /    \              /    \
     Include 2?  Exclude 2?  Include 2?  Exclude 2?
        /           \          /           \
      {1,2}        {1}       {2}          {}
```

Each leaf is a valid subset. The tree has 2^n leaves.

5. **The "Start Index" Trick**: To avoid duplicates like {1,2} and {2,1}, we always process elements in order. By starting from index `start` and only considering elements at `start` or later, we ensure each subset is generated exactly once in a canonical order.

## When NOT to Use Subsets Pattern

The subsets/power set approach isn't always appropriate:

1. **When Only Some Subsets Are Valid**: If most subsets fail validation (like combination sum), consider pruning during generation rather than generating all 2^n subsets and filtering.

2. **When You Need a Specific Size**: If you only need subsets of size k, use the combinations pattern instead—it's more efficient than generating all subsets and filtering.

3. **When n Is Large (n > 20)**: 2^20 = 1 million subsets. For n > 20, you probably need a different approach (DP, greedy, or problem-specific optimization).

4. **When Order Matters**: Subsets don't care about order. If [1,2] and [2,1] are different answers, you need permutations, not subsets.

5. **When You Only Need the Count**: If you just need to count valid subsets, use DP or math—don't generate them all.

**Red Flags Against Subsets Pattern:**

- Problem says "minimum/maximum" → probably DP or greedy
- Problem says "order matters" → probably permutations
- n > 20 in constraints → 2^n won't fit in time limit
- You only need one subset, not all → use greedy or targeted search

**Better Alternatives:**
| Situation | Use Instead |
|-----------|-------------|
| Need subsets of size k | Combinations |
| Order matters | Permutations |
| Count only | DP/Math |
| n is large | Problem-specific optimization |

---

## Interview Context

Subsets problems test:

1. **Backtracking understanding**: Include/exclude decision at each element
2. **Duplicate handling**: Subsets II with duplicate elements
3. **Time/space awareness**: Understanding 2^n complexity
4. **Multiple approaches**: Iterative, recursive, bit manipulation

---

## Problem Statement

Given an array of unique integers, return all possible subsets (the power set).

```
Input: nums = [1, 2, 3]
Output: [[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]
```

The power set has 2^n subsets (each element is either in or out).

---

## The Core Insight

At each element, make a binary decision:

- **Include** the element in the current subset
- **Exclude** the element from the current subset

```
                    []
                   /  \
          Include 1    Exclude 1
               /  \        /  \
          [1]     []
         /  \    /  \
    Include 2  Exclude 2  Include 2  Exclude 2
       /  \      /  \        /  \      /  \
    [1,2]  [1]  [2]   []
    ...    ...  ...   ...
```

---

## Approach 1: Backtracking (Recommended)

```python
def subsets(nums: list[int]) -> list[list[int]]:
    """
    Generate all subsets using backtracking.

    Time: O(n × 2^n) - 2^n subsets, O(n) to copy each
    Space: O(n) - recursion depth
    """
    result = []

    def backtrack(start: int, current: list[int]):
        # Add current subset (every state is valid)
        result.append(current[:])  # Make a copy!

        # Try adding each remaining element
        for i in range(start, len(nums)):
            current.append(nums[i])      # Include
            backtrack(i + 1, current)     # Explore
            current.pop()                 # Exclude (backtrack)

    backtrack(0, [])
    return result
```

### Visual Trace

```
nums = [1, 2, 3]

backtrack(0, [])
├── result = [[]]
├── i=0: add 1 → backtrack(1, [1])
│   ├── result = [[], [1]]
│   ├── i=1: add 2 → backtrack(2, [1,2])
│   │   ├── result = [[], [1], [1,2]]
│   │   ├── i=2: add 3 → backtrack(3, [1,2,3])
│   │   │   └── result = [[], [1], [1,2], [1,2,3]]
│   │   └── pop 3
│   └── pop 2
│   ├── i=2: add 3 → backtrack(3, [1,3])
│   │   └── result = [[], [1], [1,2], [1,2,3], [1,3]]
│   └── pop 3
└── pop 1
├── i=1: add 2 → backtrack(2, [2])
│   ├── result = [..., [2]]
│   ├── i=2: add 3 → backtrack(3, [2,3])
│   │   └── result = [..., [2,3]]
│   └── pop 3
└── pop 2
├── i=2: add 3 → backtrack(3, [3])
│   └── result = [..., [3]]
└── pop 3

Final: [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
```

---

## Approach 2: Iterative (Cascading)

Build subsets by adding each element to existing subsets.

```python
def subsets_iterative(nums: list[int]) -> list[list[int]]:
    """
    Generate subsets iteratively.

    Time: O(n × 2^n)
    Space: O(1) extra (excluding output)
    """
    result = [[]]

    for num in nums:
        # Add num to all existing subsets to create new ones
        result += [subset + [num] for subset in result]

    return result
```

### Visual Trace

```
nums = [1, 2, 3]

Start: result = [[]]

Add 1: result = [[], [1]]
       ([] + [1] = [1])

Add 2: result = [[], [1], [2], [1,2]]
       ([] + [2] = [2], [1] + [2] = [1,2])

Add 3: result = [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
       (add 3 to each existing subset)
```

---

## Approach 3: Bit Manipulation

Each subset corresponds to a binary number from 0 to 2^n - 1.

```python
def subsets_bits(nums: list[int]) -> list[list[int]]:
    """
    Generate subsets using bit manipulation.

    Time: O(n × 2^n)
    Space: O(1) extra
    """
    n = len(nums)
    result = []

    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):  # Check if i-th bit is set
                subset.append(nums[i])
        result.append(subset)

    return result
```

### Visual Trace

```
nums = [1, 2, 3]

mask=0 (000): []
mask=1 (001): [1]
mask=2 (010): [2]
mask=3 (011): [1, 2]
mask=4 (100): [3]
mask=5 (101): [1, 3]
mask=6 (110): [2, 3]
mask=7 (111): [1, 2, 3]
```

---

## Subsets II: With Duplicates

When input contains duplicates, avoid duplicate subsets.

```
Input: nums = [1, 2, 2]
Output: [[], [1], [1,2], [1,2,2], [2], [2,2]]
NOT: [[], [1], [1,2], [1,2], [1,2,2], [2], [2], [2,2]]
```

### Solution: Sort + Skip Duplicates

```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    """
    Generate subsets with duplicate elements.

    Time: O(n × 2^n)
    Space: O(n)
    """
    nums.sort()  # Sort to group duplicates
    result = []

    def backtrack(start: int, current: list[int]):
        result.append(current[:])

        for i in range(start, len(nums)):
            # Skip duplicates: if same as previous and previous wasn't used
            if i > start and nums[i] == nums[i - 1]:
                continue

            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result
```

### Why This Works

```
nums = [1, 2, 2] (sorted)

At start=1, we can choose:
- nums[1]=2 (first 2) → explore subsets with this 2
- nums[2]=2 (second 2) → SKIP! We'd duplicate the work

The key: when we skip nums[i], we're saying "don't start a new branch with this 2"
But we still include it when it's part of a chain (i == start case)
```

---

## Approach Comparison

| Approach         | Time       | Space | Best For                     |
| ---------------- | ---------- | ----- | ---------------------------- |
| Backtracking     | O(n × 2^n) | O(n)  | Most interviews, clear logic |
| Iterative        | O(n × 2^n) | O(1)  | Simple cases                 |
| Bit Manipulation | O(n × 2^n) | O(1)  | When n ≤ 20, clever solution |

---

## Common Mistakes

### 1. Forgetting to Copy

```python
# WRONG: All subsets point to same list
result.append(current)  # current will be modified!

# CORRECT: Copy the list
result.append(current[:])
# or
result.append(list(current))
```

### 2. Wrong Loop Index

```python
# WRONG: Includes same element twice
for i in range(len(nums)):  # Always starts from 0

# CORRECT: Start from where we left off
for i in range(start, len(nums)):
```

### 3. Modifying Input

```python
# Be careful with sort() - it modifies nums
nums.sort()  # Original array is changed!

# If needed, work on a copy
sorted_nums = sorted(nums)  # Original preserved
```

---

## Complexity Analysis

| Operation            | Time       | Space | Notes                      |
| -------------------- | ---------- | ----- | -------------------------- |
| Generate all subsets | O(n × 2^n) | O(n)  | 2^n subsets, O(n) per copy |
| With duplicates      | O(n × 2^n) | O(n)  | Same worst case            |
| Bit manipulation     | O(n × 2^n) | O(1)  | Constant extra space       |

---

## Edge Cases

- [ ] Empty array → return [[]]
- [ ] Single element → return [[], [elem]]
- [ ] All duplicates → return [[], [a], [a,a], ...]
- [ ] Large n → watch for 2^n growth

---

## Practice Problems

| #   | Problem                      | Difficulty | Key Insight            |
| --- | ---------------------------- | ---------- | ---------------------- |
| 1   | Subsets                      | Medium     | Basic backtracking     |
| 2   | Subsets II                   | Medium     | Sort + skip duplicates |
| 3   | Letter Case Permutation      | Medium     | Binary decision tree   |
| 4   | Find All Subsets of Length K | Medium     | Add length constraint  |

---

## Interview Tips

1. **Start with basic subsets**: Show you understand the pattern
2. **Ask about duplicates**: Clarify if input has duplicates
3. **Mention all approaches**: Backtracking, iterative, bit manipulation
4. **State complexity clearly**: O(2^n) subsets is expected
5. **Copy, don't reference**: Always copy mutable objects when saving

---

## Key Takeaways

1. Subsets = include/exclude decision for each element
2. Backtracking is the most versatile approach
3. Handle duplicates by sorting and skipping
4. Always copy lists when adding to result
5. Time is O(n × 2^n) regardless of approach

---

## Next: [03-permutations.md](./03-permutations.md)

Learn how to generate all permutations (orderings) of elements.
