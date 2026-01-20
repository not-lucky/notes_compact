# Subsets

## Problem Statement

Given an integer array `nums` of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets.

**Example:**
```
Input: nums = [1, 2, 3]
Output: [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
```

## Building Intuition

### Why This Works

Every subset is the result of making n binary decisions: for each element, either include it or exclude it. With 3 elements, you have 2^3 = 8 possible combinations of include/exclude decisions, which is exactly why there are 2^n subsets. The backtracking approach systematically explores this binary decision tree.

The key insight for the backtracking implementation is the "start" parameter. By only considering elements from index `start` onward, we ensure each subset is generated exactly once and in a canonical order. Without this, you'd generate [1,2] and [2,1] as separate subsets. The `start` parameter says: "once you've decided on element i, only consider elements after i for the rest of this subset."

The iterative approach reveals the same structure differently: for each new element, every existing subset spawns a new subset containing that element. Starting from [[]], adding element 1 gives [[], [1]]. Adding element 2 gives [[], [1], [2], [1,2]]. This doubling at each step is why we get 2^n subsets.

### How to Discover This

For any "generate all combinations" problem, think about what decisions you're making. For subsets: include or exclude each element. For permutations: which element comes next. The backtracking template is: (1) add current state to result, (2) for each remaining choice, make the choice, recurse, and undo the choice. The recursion tree mirrors the decision space.

### Pattern Recognition

This is the **Subset Generation / Power Set** pattern. Recognize it when:
- You need ALL possible subsets/combinations
- Order within subsets doesn't matter (unlike permutations)
- There are no constraints beyond "choose any subset of elements"

## When NOT to Use

- **When you need permutations (order matters)**: Use the permutation pattern instead, which swaps elements rather than using a start index.
- **When there are constraints on valid subsets**: You might need pruning to avoid generating invalid subsets.
- **When you only need to count subsets, not enumerate them**: Just compute 2^n; no need to generate.
- **When the array has duplicates**: Use Subsets II pattern with sorting and skip logic to avoid duplicate subsets.

## Approach

### Method 1: Backtracking
For each element, make a choice: include it or exclude it.

### Method 2: Iterative
Start with empty set, for each number, add it to all existing subsets.

### Method 3: Bit Manipulation
Each subset corresponds to a binary number from 0 to 2^n - 1.

## Implementation

```python
def subsets(nums: list[int]) -> list[list[int]]:
    """
    Generate all subsets using backtracking.

    Time: O(n × 2^n) - generate 2^n subsets, each takes O(n) to copy
    Space: O(n) - recursion depth
    """
    result = []

    def backtrack(start: int, current: list[int]):
        # Add current subset (make a copy)
        result.append(current[:])

        # Try adding each remaining element
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result


def subsets_iterative(nums: list[int]) -> list[list[int]]:
    """
    Generate subsets iteratively.

    Start with [[]], for each num, add num to all existing subsets.

    Time: O(n × 2^n)
    Space: O(1) extra (excluding output)
    """
    result = [[]]

    for num in nums:
        result += [subset + [num] for subset in result]

    return result


def subsets_bit(nums: list[int]) -> list[list[int]]:
    """
    Generate subsets using bit manipulation.

    For n elements, there are 2^n subsets.
    Each subset corresponds to a binary number.

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

## Complexity Analysis

| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n × 2^n) | Generate 2^n subsets, each O(n) to copy |
| Space | O(n) | Recursion depth (excluding output) |

## Visual Walkthrough

```
nums = [1, 2, 3]

Backtracking Tree:
                    []
          /         |         \
        [1]        [2]        [3]
       /   \         |
    [1,2]  [1,3]   [2,3]
      |
   [1,2,3]

Iterative:
Start: [[]]
Add 1: [[], [1]]
Add 2: [[], [1], [2], [1,2]]
Add 3: [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]

Bit Manipulation:
000 → []
001 → [1]
010 → [2]
011 → [1,2]
100 → [3]
101 → [1,3]
110 → [2,3]
111 → [1,2,3]
```

## Edge Cases

1. **Empty array**: Return [[]] (only empty subset)
2. **Single element**: [[], [element]]
3. **Large array**: Exponential output, be careful

## Common Mistakes

1. **Not copying current list**: `result.append(current[:])` not `result.append(current)`
2. **Including duplicates**: Use `start` parameter to avoid
3. **Missing empty set**: Initialize with empty set or add at start

## Variations

### Subsets II (With Duplicates)
```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    """
    Generate subsets with duplicates in input.
    Skip duplicates at same level of recursion.

    Time: O(n × 2^n)
    Space: O(n)
    """
    nums.sort()  # Sort to group duplicates
    result = []

    def backtrack(start: int, current: list[int]):
        result.append(current[:])

        for i in range(start, len(nums)):
            # Skip duplicates at same level
            if i > start and nums[i] == nums[i - 1]:
                continue
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result
```

### Subsets of Size K
```python
def subsets_of_size_k(nums: list[int], k: int) -> list[list[int]]:
    """
    Generate all subsets of exactly size k (combinations).

    Time: O(C(n,k) × k)
    Space: O(k)
    """
    result = []

    def backtrack(start: int, current: list[int]):
        if len(current) == k:
            result.append(current[:])
            return

        # Pruning: need (k - len(current)) more elements
        # So don't start beyond len(nums) - (k - len(current))
        remaining = k - len(current)
        for i in range(start, len(nums) - remaining + 1):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result
```

### Permutations
```python
def permutations(nums: list[int]) -> list[list[int]]:
    """
    Generate all permutations (order matters).

    Time: O(n! × n)
    Space: O(n)
    """
    result = []

    def backtrack(current: list[int], remaining: set):
        if not remaining:
            result.append(current[:])
            return

        for num in list(remaining):
            current.append(num)
            remaining.remove(num)
            backtrack(current, remaining)
            remaining.add(num)
            current.pop()

    backtrack([], set(nums))
    return result


def permutations_swap(nums: list[int]) -> list[list[int]]:
    """
    Permutations using swapping (in-place).
    """
    result = []

    def backtrack(start: int):
        if start == len(nums):
            result.append(nums[:])
            return

        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]

    backtrack(0)
    return result
```

### Combination Sum
```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """
    Find combinations that sum to target (can reuse elements).

    Time: O(2^target) roughly
    Space: O(target)
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
            # Same i because we can reuse
            backtrack(i, current, remaining - candidates[i])
            current.pop()

    backtrack(0, [], target)
    return result
```

## Related Problems

- **Subsets II** - With duplicate elements
- **Permutations** - Order matters
- **Permutations II** - With duplicates
- **Combinations** - Fixed size subsets
- **Combination Sum** - Subsets that sum to target
- **Letter Combinations of a Phone Number** - Different domain
