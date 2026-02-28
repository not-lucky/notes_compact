# Combination Sum

> **Prerequisites:** [Combinations](./04-combinations.md), [Subsets](./02-subsets.md)

## Core Concept

Combination Sum problems ask you to find subsets of numbers that add up to a specific `target` value. This is a critical pattern because it combines standard backtracking with **constraint satisfaction**.

While standard subsets or combinations branch unconditionally, combination sum algorithms are **Target-Driven**. At each step, we decide whether to add an item to our combination and subtract its value from a running `remaining_target`. When `remaining_target == 0`, we have found a valid combination.

## Intuition & Mental Models

We can conceptualize this as a **Budget Problem**. You have a budget (`target`), and a list of items with costs (`candidates`). You want to spend *exactly* your budget. If you overspend (`remaining_target < 0`), you must immediately return the item and try a cheaper one.

The core of the Combination Sum algorithm involves two models:

1. **State:** `(start_index, current_path, remaining_target)`
2. **Action:**
   - **Base Case 1:** `remaining_target == 0` (Perfect! Save `current_path[:]`).
   - **Base Case 2:** `remaining_target < 0` (Overspent! Backtrack).

### Visualizing Target-Driven Pruning

The true power of this pattern is **Sorting + Early Termination**. If candidates are sorted, and the *current* candidate exceeds the `remaining_target`, we don't just skip that candidate—we can `break` entirely, because *all subsequent candidates will be even larger*.

**The Spending Tree (`target=7, candidates=[2,3,6,7]`)**:

```text
State: (start_idx, remaining_target)

                           (0, 7)
                 /           |          \
           (0, 5)          (1, 4)      (2, 1)
           /    \           |             |
      (0, 3)    (1, 2)    (1, 1)       ✗ (6 > 1, break)
      /    \       |        |
  (0, 1)  (1, 0) ✗ (3>2) ✗ (3>1)
   /        ✓
✗ (2>1)
```

*Notice the pruning logic: Once `remaining` is 1, candidate `2` is too big. Since the array `[2,3,6,7]` is sorted, we immediately `break` because `3, 6, 7` will also be too big.*

### Reuse vs. No-Reuse

The biggest differentiator in Combination Sum problems is whether candidates can be used multiple times:

- **Unlimited Reuse (Sum I)**: When recurring, pass the *same* `i` index down: `backtrack(i, path, remain - c)`.
- **Single Use (Sum II)**: When recurring, pass `i + 1`: `backtrack(i + 1, path, remain - c)`.

## Basic Implementation: Combination Sum I (Unlimited Reuse)

In Combination Sum I, candidates are distinct, and each candidate can be used an **unlimited** number of times.

```python
def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
    result = []
    # Sorting is critical for the pruning optimization
    candidates.sort()

    def backtrack(start: int, path: list[int], remaining: int):
        # Base cases
        if remaining == 0:
            result.append(path[:])  # Found a valid combo
            return
        if remaining < 0:
            return  # Dead end

        # Loop-based suffix selection
        for i in range(start, len(candidates)):
            # Pruning optimization: since candidates are sorted,
            # if candidates[i] is too big, all candidates after it are too.
            if candidates[i] > remaining:
                break

            path.append(candidates[i])
            # Unlimited Reuse: pass 'i', not 'i + 1'
            backtrack(i, path, remaining - candidates[i])
            path.pop()  # Backtrack

    backtrack(0, [], target)
    return result
```

## Optimized Implementation: Combination Sum II (No Reuse, with Duplicates)

In Combination Sum II, the `candidates` array may contain duplicates (e.g., `[10, 1, 2, 7, 6, 1, 5]`), and each element in the array can only be used **once**.

To prevent generating identical combinations (e.g., two identical `[1, 2, 5]` lists), we must sort the array and skip duplicates at the *same tree level*.

```python
def combinationSum2(candidates: list[int], target: int) -> list[list[int]]:
    result = []
    # Sort: Groups duplicates and enables early pruning
    candidates.sort()

    def backtrack(start: int, path: list[int], remaining: int):
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            # 1. Deduplication logic
            # Skip candidates identical to the previous one AT THIS LEVEL
            if i > start and candidates[i] == candidates[i - 1]:
                continue

            # 2. Pruning logic
            if candidates[i] > remaining:
                break

            path.append(candidates[i])
            # 3. No Reuse logic: Pass i + 1
            backtrack(i + 1, path, remaining - candidates[i])
            path.pop()

    backtrack(0, [], target)
    return result
```

### Visualizing Duplicate Skipping (Sum II)

Given `candidates = [1, 1, 6], target = 8`:

```text
State: (start, path)
                          (0, [])
               /             |             \
            (1, [1])      (2, [1])       (3, [6])
            /                |              |
      (2, [1,1])         ✗ (duplicate,    ✗ (6 > 8-6)
         |               i=1, start=0)
      (3, [1,1,6])
         ✓ (target=8)
```

*If we didn't skip the second `1` at the root level, we would generate `[1, 6]` twice.*

## Complexity Analysis

Let $n$ be the number of candidates, $T$ be the target, and $M$ be the minimum candidate value.

### Combination Sum I (Unlimited Reuse)

- **Time Complexity**: Loose upper bound $\mathcal{O}(N^{\frac{T}{M}})$. The maximum depth of the recursion tree is $\frac{T}{M}$ (if we repeatedly pick the smallest element). At each level, we have at most $N$ choices. Pruning significantly reduces this.
- **Space/Memory Complexity**: $\mathcal{O}(\frac{T}{M})$. The call stack and the `path` list can grow up to $\frac{T}{M}$ deep. (This is Auxiliary Space, excluding the output array).

### Combination Sum II (No Reuse)

- **Time Complexity**: Loose upper bound $\mathcal{O}(2^n)$. Each element is either included or excluded. Sorting takes $\mathcal{O}(n \log n)$. Pruning and duplicate skipping drastically reduce the actual branching factor.
- **Space/Memory Complexity**: $\mathcal{O}(n)$. The call stack and `path` list can grow up to $n$ deep (if we select every element).

## Common Pitfalls

1. **Passing Sliced Arrays**: Do NOT use `backtrack(candidates[i+1:])` or similar $O(N)$ slicing operations. This generates massive memory overhead and destroys the time complexity. Always pass a `start` index pointer.
2. **Incorrect Duplicate Logic**: A common mistake is using `if candidates[i] == candidates[i-1]: continue` without the `i > start` check. This aggressively prunes valid vertical branches where the same number is used across different levels (e.g., `[1, 1, 6]`). The `i > start` condition correctly restricts the skipping to horizontal siblings.
3. **Forgetting to Sort**: Duplicate skipping (`candidates[i] == candidates[i-1]`) and early termination (`candidates[i] > remaining`) completely fail if the input array is not sorted first.
4. **Mutating State Variables Incorrectly**: Ensure you subtract directly in the recursive call (`remaining - candidates[i]`) rather than mutating `remaining -= candidates[i]` before the call. If you mutate it before, you must carefully restore it (`remaining += candidates[i]`) afterward. Passing it inline is cleaner and less error-prone.
