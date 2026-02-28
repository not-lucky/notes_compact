# Permutations

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md), [Subsets](./02-subsets.md)

## Core Concept

Permutations are all possible **orderings** of a set of elements. Unlike subsets where order does not matter (`[1,2]` and `[2,1]` are the same subset), in permutations they are distinct results. This pattern appears in scheduling, arrangement, and optimization problems.

## Intuition & Mental Models

### The "Slot-Filling" Model

Think of building a permutation as filling empty slots. At each slot, you choose from the elements you have not used yet.

1. **First Slot**: You can choose any of $N$ elements.
2. **Second Slot**: You choose from the remaining $N-1$ elements.
3. **Third Slot**: You choose from the remaining $N-2$ elements.
4. **Total Arrangements**: $N \times (N-1) \times (N-2) \times \dots \times 1 = N!$

### Permutations vs. Subsets

In **Subsets**, we use the "Suffix Selection" model with a `start_index` to avoid generating `[2,1]` after we have already generated `[1,2]`. We only pick elements that come *after* our last choice.

In **Permutations**, we *want* both `[1,2]` and `[2,1]`. Therefore, we do not use a `start_index`. Instead, every recursive call loops through the **entire array** from index 0, but we use a `used` boolean array (or a hash set) to track which elements are currently in our path.

## Visualizations

### The Permutation Tree

```text
                         []
                    /    |    \
               [1]      [2]     [3]
              /   \    /   \   /   \
          [1,2] [1,3] [2,1] [2,3] [3,1] [3,2]
           |     |     |     |     |     |
        [1,2,3] [1,3,2] [2,1,3] [2,3,1] [3,1,2] [3,2,1]
```

At each step, we look at the array `[1, 2, 3]` and pick any element that isn't already used in the current branch.

## Basic Implementation

### Using a `used` Array

```python
def permute(nums: list[int]) -> list[list[int]]:
    result = []
    used = [False] * len(nums)

    def backtrack(path: list[int]):
        # Base case: We have filled all slots
        if len(path) == len(nums):
            result.append(path[:])  # Explicitly copy the path!
            return

        # Suffix Selection model DOES NOT use a start_index here!
        # We always iterate through the whole array.
        for i in range(len(nums)):
            # Skip elements we've already placed in our current permutation
            if used[i]:
                continue

            # 1. Choose
            used[i] = True
            path.append(nums[i])

            # 2. Explore
            backtrack(path)

            # 3. Un-choose (Backtrack)
            path.pop()
            used[i] = False

    backtrack([])
    return result
```

## Permutations II: Handling Duplicates

If the input array contains duplicates (e.g., `[1, 1, 2]`), the basic permutation algorithm will generate identical sequences (e.g., two distinct `[1, 1, 2]` permutations depending on which `1` was picked first).

To solve this, we sort the array to place duplicates adjacent to one another. Then, we skip a duplicate if it appears at the **same level** of our decision tree.

### Code

```python
def permute_unique(nums: list[int]) -> list[list[int]]:
    # 1. Sort the array so duplicates are adjacent
    nums.sort()
    result = []
    used = [False] * len(nums)

    def backtrack(path: list[int]):
        if len(path) == len(nums):
            result.append(path[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue

            # 2. Pruning: Skip same-level duplicates
            # If nums[i] == nums[i-1], we only use nums[i] if nums[i-1] was already used
            # in the CURRENT branch (meaning we are at a DEEPER level).
            # If used[i-1] is False, it means nums[i-1] was used and then UN-CHOSEN,
            # so we are at the SAME level and should skip.
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue

            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result
```

### Visualizing Pruning

```text
nums = [1, 1, 2] (sorted)

At the first slot (level 0):
- Pick nums[0]=1: valid. Branches down to create [1, 1, 2], etc.
- Pick nums[1]=1: wait. nums[1] == nums[0]. Is nums[0] used?
  No, we just backtracked from it. That means we are at the SAME level.
  Skip it! Otherwise, we'd generate all the [1, ...] permutations again.
- Pick nums[2]=2: valid. Branches down to create [2, 1, 1].
```

## Complexity Analysis

- **Time Complexity**: $\mathcal{O}(N \cdot N!)$
  - There are $N!$ possible permutations.
  - For each permutation, copying `path[:]` takes $\mathcal{O}(N)$ time.
- **Auxiliary Space**: $\mathcal{O}(N)$
  - Call stack depth is exactly $N$.
  - The `used` array and `path` array take $\mathcal{O}(N)$ space.
- **Total Space**: $\mathcal{O}(N \cdot N!)$
  - We store $N!$ lists, each of length $N$, in the `result` array.

## Common Pitfalls

1. **Confusing Subsets and Permutations**: Subsets use a `start_index` parameter in the `backtrack` function to avoid looking backward. Permutations do not use a `start_index`; they loop `for i in range(len(nums))` every time and use a `used` array to skip previously picked elements.
2. **Forgetting the Base Case**: Unlike Subsets (where every node is a valid subset), in Permutations, only the **leaf nodes** (where `len(path) == len(nums)`) are valid results.
3. **The Duplicates Pruning Condition**: For `permute_unique`, the condition is `if i > 0 and nums[i] == nums[i-1] and not used[i-1]`.
   - `i > 0`: Prevents index out of bounds.
   - `nums[i] == nums[i-1]`: Checks if the value is a duplicate.
   - `not used[i-1]`: Crucial part. It ensures we only skip if the previous identical element was just *un-chosen* (meaning we are at the exact same level of the tree). If `used[i-1]` is true, the previous duplicate was chosen at an *earlier/higher* level of the tree, which is allowed.

## When NOT to Use Permutations Pattern

1. **When Order Doesn't Matter**: If `[1,2,3]` and `[3,2,1]` are the same answer, use subsets or combinations. They have exponential ($2^N$) or polynomial complexity, not factorial ($N!$).
2. **When N Is Large**: $10! = 3.6$ million. $12! = 479$ million. For $N > 10$, generating all permutations is usually too slow. Look for DP, Greedy, or Math optimizations.
3. **When Elements Can Be Reused**: If the same element can appear multiple times (e.g., rolling a die 3 times), you're dealing with "Permutations with Repetition" (or Combinatorics with Replacement)—the complexity is $K^N$, not $N!$.

---

## Next: [04-combinations.md](./04-combinations.md)

Learn how to generate combinations (choose K from N).
