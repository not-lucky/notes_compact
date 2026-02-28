# Subsets (Power Set)

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md)

## Core Concept

The subsets problem asks you to generate all possible subsets of a given set—this is called the **power set**. It is the foundational backtracking problem because it teaches the core decision-making patterns that apply to many other problems.

## Intuition & Mental Models

There are two primary ways to conceptualize generating subsets. Understanding both is critical for mastering backtracking.

### 1. The "Include/Exclude" Model (Binary Decision)

At each step, we focus on a single element and make a binary choice: **include** it in our current subset, or **exclude** it.

- **State**: The current element index we are considering.
- **Decision**: Yes or No.
- **Tree Depth**: Exactly $N$ (number of elements).
- **Leaves**: All $2^N$ subsets.

```text
                    Start: []
                   /          \
          Include 1?          Exclude 1?
              /                    \
           [1]                      []
          /    \                  /    \
     Include 2?  Exclude 2?  Include 2?  Exclude 2?
        /           \          /           \
      [1,2]        [1]       [2]          []
```

### 2. The "Suffix Selection" Model (Loop-Based)

Instead of a binary choice, we start with an empty subset and iterate through the remaining elements. We can pick *any* element to add next, but to avoid generating duplicates (like `[1,2]` and `[2,1]`), we only pick from the elements that come *after* our last choice.

- **State**: The `start_index` from which we can pick the next element.
- **Decision**: Which element from `nums[start_index:]` should I add next?
- **Tree Depth**: Up to $N$.
- **Nodes**: *Every* node in this tree is a valid subset.

```text
                         []
                    /    |    \
                  [1]   [2]   [3]
                 /  \     \
             [1,2] [1,3] [2,3]
               |
            [1,2,3]
```

This model is often preferred because it naturally extends to combinations and permutations.

## Basic Implementation

We will use the **Suffix Selection** model.

### Code

```python
def subsets(nums: list[int]) -> list[list[int]]:
    result = []

    def backtrack(start_index: int, path: list[int]):
        # Every node in the suffix selection tree is a valid subset.
        # We MUST explicitly copy the path using path[:]
        result.append(path[:])

        # Iterate through all remaining elements to add to our subset
        for i in range(start_index, len(nums)):
            # 1. Choose (Include)
            path.append(nums[i])

            # 2. Explore (Move to the next level)
            backtrack(i + 1, path)

            # 3. Un-choose (Backtrack/Exclude)
            path.pop()

    backtrack(0, [])
    return result
```

## Subsets II: Handling Duplicates

What if the input has duplicates, like `[1, 2, 2]`? The standard algorithm will generate duplicate subsets.

To fix this, we sort the array and skip same-level duplicates.

### Code

```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    # 1. Sort the array so duplicates are adjacent
    nums.sort()
    result = []

    def backtrack(start_index: int, path: list[int]):
        result.append(path[:])

        for i in range(start_index, len(nums)):
            # 2. Pruning: Skip duplicates at the SAME level of the recursive tree
            if i > start_index and nums[i] == nums[i - 1]:
                continue

            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

### Visualizing Pruning

```text
nums = [1, 2, 2] (sorted)

                         []
                    /    |      \
                  [1]   [2]    [2] (pruned: i > start and nums[i] == nums[i-1])
                 /  \     \
             [1,2] [1,2]* [2,2]
               |
            [1,2,2]

* Note: The second [1,2] is pruned because at start_index=1 (after picking 1),
  the loop considers nums[1]=2 (valid) and then nums[2]=2. Since nums[2]==nums[1],
  it is skipped.
```

## Complexity Analysis

- **Time Complexity**: $\mathcal{O}(N \cdot 2^N)$
  - There are $2^N$ possible subsets.
  - For each subset, copying `path[:]` into the result array takes $\mathcal{O}(N)$ time.
- **Auxiliary Space**: $\mathcal{O}(N)$
  - The maximum depth of the call stack is $N$.
  - The `path` array takes $\mathcal{O}(N)$ space.
- **Total Space**: $\mathcal{O}(N \cdot 2^N)$
  - We store $2^N$ subsets, each of up to size $N$, in the `result` array.

## Common Pitfalls

1. **Forgetting to Copy the Path**:
   ```python
   # WRONG: Appends a reference to the mutable list.
   # By the end, result will be a list of empty arrays: [[], [], []]
   result.append(path)

   # CORRECT: Creates a shallow copy of the list at this exact moment in time.
   result.append(path[:])
   ```
2. **Slicing Arrays in Recursive Calls**:
   ```python
   # WRONG: Creates a new array every call, adding O(N) time and space overhead
   backtrack(nums[1:], path)

   # CORRECT: Use an index pointer
   backtrack(start_index + 1, path)
   ```
3. **Using `start_index` vs `i + 1`**:
   Inside the loop, the recursive call must be `backtrack(i + 1, path)`, NOT `backtrack(start_index + 1, path)`. The next level must only consider elements strictly after the one we just picked (`i`).

## When NOT to Use the Subsets Pattern

1. **When Order Matters**: Subsets do not care about order. If `[1,2]` and `[2,1]` are different answers, you need permutations.
2. **When You Need a Specific Size**: If you only need subsets of size $K$, use combinations—it stops exploring when the size exceeds $K$.
3. **When N is Large**: $2^{20} \approx 1,000,000$. For $N > 20$, generating all subsets is too slow. Look for Dynamic Programming or Greedy approaches.

---

## Next: [03-permutations.md](./03-permutations.md)
Learn how to generate all permutations (orderings) of elements.
