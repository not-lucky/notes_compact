# Permutations

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md), [Subsets](./02-subsets.md)

## Interview Context

Permutation problems test:
1. **Order matters**: Unlike subsets, [1,2] ≠ [2,1]
2. **Element tracking**: Knowing which elements are already used
3. **Duplicate handling**: Avoiding duplicate permutations
4. **Factorial complexity**: Understanding O(n!) growth

---

## Problem Statement

Given an array of unique integers, return all possible permutations.

```
Input: nums = [1, 2, 3]
Output: [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

There are n! permutations (n choices for first position, n-1 for second, etc.).

---

## The Core Insight

At each position, choose from **remaining unused elements**:

```
                         []
                    /    |    \
               [1]      [2]     [3]
              /   \    /   \   /   \
          [1,2] [1,3] [2,1] [2,3] [3,1] [3,2]
           |     |     |     |     |     |
        [1,2,3] [1,3,2] [2,1,3] [2,3,1] [3,1,2] [3,2,1]
```

---

## Approach 1: Backtracking with Used Array

```python
def permute(nums: list[int]) -> list[list[int]]:
    """
    Generate all permutations using backtracking.

    Time: O(n × n!) - n! permutations, O(n) to copy each
    Space: O(n) - recursion depth + used array
    """
    result = []
    used = [False] * len(nums)

    def backtrack(current: list[int]):
        # Base case: permutation complete
        if len(current) == len(nums):
            result.append(current[:])
            return

        # Try each unused element
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

### Visual Trace

```
nums = [1, 2, 3]

backtrack([])
├── i=0: use 1 → backtrack([1])
│   ├── i=1: use 2 → backtrack([1,2])
│   │   └── i=2: use 3 → backtrack([1,2,3]) ✓
│   └── i=2: use 3 → backtrack([1,3])
│       └── i=1: use 2 → backtrack([1,3,2]) ✓
├── i=1: use 2 → backtrack([2])
│   ├── i=0: use 1 → backtrack([2,1])
│   │   └── i=2: use 3 → backtrack([2,1,3]) ✓
│   └── i=2: use 3 → backtrack([2,3])
│       └── i=0: use 1 → backtrack([2,3,1]) ✓
└── i=2: use 3 → backtrack([3])
    ├── i=0: use 1 → backtrack([3,1])
    │   └── i=1: use 2 → backtrack([3,1,2]) ✓
    └── i=1: use 2 → backtrack([3,2])
        └── i=0: use 1 → backtrack([3,2,1]) ✓
```

---

## Approach 2: Swapping (In-Place)

Instead of tracking used elements, swap elements into position.

```python
def permute_swap(nums: list[int]) -> list[list[int]]:
    """
    Generate permutations by swapping elements in place.

    Time: O(n × n!)
    Space: O(n) - recursion depth only
    """
    result = []

    def backtrack(start: int):
        # Base case: all positions filled
        if start == len(nums):
            result.append(nums[:])
            return

        # Try each element in current position
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]  # Swap
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]  # Swap back

    backtrack(0)
    return result
```

### Visual Trace

```
nums = [1, 2, 3]

backtrack(0)
├── swap(0,0): [1,2,3] → backtrack(1)
│   ├── swap(1,1): [1,2,3] → backtrack(2)
│   │   └── swap(2,2): [1,2,3] ✓
│   └── swap(1,2): [1,3,2] → backtrack(2)
│       └── [1,3,2] ✓
├── swap(0,1): [2,1,3] → backtrack(1)
│   ├── swap(1,1): [2,1,3] → backtrack(2)
│   │   └── [2,1,3] ✓
│   └── swap(1,2): [2,3,1] → backtrack(2)
│       └── [2,3,1] ✓
└── swap(0,2): [3,2,1] → backtrack(1)
    ├── swap(1,1): [3,2,1] → backtrack(2)
    │   └── [3,2,1] ✓
    └── swap(1,2): [3,1,2] → backtrack(2)
        └── [3,1,2] ✓
```

---

## Permutations II: With Duplicates

When input contains duplicates, avoid duplicate permutations.

```
Input: nums = [1, 1, 2]
Output: [[1,1,2], [1,2,1], [2,1,1]]
NOT: [[1,1,2], [1,1,2], [1,2,1], [1,2,1], [2,1,1], [2,1,1]]
```

### Solution: Sort + Skip Same-Level Duplicates

```python
def permute_unique(nums: list[int]) -> list[list[int]]:
    """
    Generate unique permutations with duplicates.

    Time: O(n × n!)
    Space: O(n)
    """
    nums.sort()  # Sort to group duplicates
    result = []
    used = [False] * len(nums)

    def backtrack(current: list[int]):
        if len(current) == len(nums):
            result.append(current[:])
            return

        for i in range(len(nums)):
            # Skip if already used
            if used[i]:
                continue

            # Skip duplicate: same value, previous not used (same level)
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

### Why `not used[i-1]`?

```
nums = [1, 1, 2] (indices: 0, 1, 2)

At first position, we can use:
- nums[0]=1 (first 1) ✓
- nums[1]=1 (second 1) ✗ if nums[0] not used yet

Why? If we haven't used the first 1 yet, using the second 1
would create a duplicate path. We only use the second 1 when
the first 1 is already in our permutation.

Valid: use 1(0), then 1(1), then 2 → [1,1,2]
Invalid: use 1(1) first → would duplicate 1(0) first
```

---

## Next Permutation

Find the lexicographically next permutation.

```python
def next_permutation(nums: list[int]) -> None:
    """
    Rearrange to next lexicographically greater permutation.
    Modify in-place.

    Time: O(n)
    Space: O(1)

    Algorithm:
    1. Find largest i where nums[i] < nums[i+1]
    2. Find largest j where nums[j] > nums[i]
    3. Swap nums[i] and nums[j]
    4. Reverse nums[i+1:]
    """
    n = len(nums)

    # Step 1: Find first decreasing element from right
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:
        # Step 2: Find smallest element larger than nums[i]
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        # Step 3: Swap
        nums[i], nums[j] = nums[j], nums[i]

    # Step 4: Reverse the suffix
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
```

### Visual Example

```
nums = [1, 2, 3] → [1, 3, 2]
nums = [1, 3, 2] → [2, 1, 3]
nums = [3, 2, 1] → [1, 2, 3] (wrap around)

Step by step for [1, 2, 3]:
1. Find i: 2 > 3? No. 2 < 3? Yes! i = 1 (nums[1] = 2)
2. Find j: nums[j] > 2? nums[2] = 3 > 2. j = 2
3. Swap: [1, 3, 2]
4. Reverse after i: nothing to reverse
Result: [1, 3, 2]
```

---

## Permutation Sequence (Kth Permutation)

Find the kth permutation without generating all.

```python
def get_permutation(n: int, k: int) -> str:
    """
    Return the kth permutation of [1, 2, ..., n].

    Time: O(n²)
    Space: O(n)
    """
    import math

    # Build factorial lookup and numbers list
    numbers = list(range(1, n + 1))
    k -= 1  # Convert to 0-indexed
    result = []

    for i in range(n, 0, -1):
        # There are (i-1)! permutations for each first digit
        factorial = math.factorial(i - 1)
        index = k // factorial
        result.append(str(numbers[index]))
        numbers.pop(index)
        k %= factorial

    return ''.join(result)
```

### Visual Example

```
n = 3, k = 3 (0-indexed: k = 2)

Available: [1, 2, 3]
2! = 2 permutations per first digit

k // 2 = 1 → pick numbers[1] = 2
Result so far: "2"
k %= 2 = 0

Available: [1, 3]
1! = 1 permutation per second digit

k // 1 = 0 → pick numbers[0] = 1
Result so far: "21"
k %= 1 = 0

Available: [3]
Pick the last: 3
Result: "213"
```

---

## Approach Comparison

| Approach | Time | Space | Best For |
|----------|------|-------|----------|
| Used array | O(n × n!) | O(n) | Most readable |
| Swapping | O(n × n!) | O(n) | In-place modification |
| With duplicates | O(n × n!) | O(n) | Handling duplicates |

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| All permutations | O(n × n!) | O(n) | n! permutations, O(n) each |
| Next permutation | O(n) | O(1) | Single iteration |
| Kth permutation | O(n²) | O(n) | Pop from list is O(n) |

---

## Edge Cases

- [ ] Empty array → return [[]]
- [ ] Single element → return [[elem]]
- [ ] All duplicates → return one permutation
- [ ] n = 0 for kth permutation

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Permutations | Medium | Basic backtracking |
| 2 | Permutations II | Medium | Sort + skip duplicates |
| 3 | Next Permutation | Medium | Find pattern, O(n) |
| 4 | Permutation Sequence | Hard | Math-based, skip counting |
| 5 | Palindrome Permutation II | Medium | Build from half |

---

## Interview Tips

1. **Clarify duplicates**: Ask if input can have duplicate elements
2. **Know both approaches**: Used array is clearer; swapping is more elegant
3. **State complexity**: n! is massive—mention it grows faster than 2^n
4. **Next permutation is O(n)**: Don't generate all permutations for it
5. **Watch for in-place**: Some problems ask to modify input

---

## Key Takeaways

1. Permutations differ from subsets: order matters, all elements used
2. Track used elements with boolean array or swapping
3. Handle duplicates by sorting and skipping at same level
4. n! grows extremely fast: 10! = 3.6 million
5. Next permutation is a pattern recognition problem, not backtracking

---

## Next: [04-combinations.md](./04-combinations.md)

Learn how to generate combinations (choose k from n).
