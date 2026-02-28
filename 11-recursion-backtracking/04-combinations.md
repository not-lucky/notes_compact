# Combinations

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md), [Subsets](./02-subsets.md)

## Core Concept

Combinations represent selecting $k$ elements from a set of $n$ elements where **order does not matter**. Unlike permutations where `[1, 2]` and `[2, 1]` are distinct, in combinations they are identical. This pattern appears whenever you need to select a fixed-size group or "team" from a larger pool of candidates.

Mathematically, the number of combinations is denoted as "n choose k":
$C(n,k) = \frac{n!}{k!(n-k)!}$

## Intuition & Mental Models

Combinations are essentially the **Subsets pattern with a size constraint**. We generate subsets, but we only save the ones that have exactly $k$ elements, and we stop exploring branches that can never reach size $k$.

We use the **Loop-based Suffix Selection** mental model:

1. **Sort/Order**: Imagine all $n$ candidates in a line (e.g., `1, 2, ..., n`).
2. **Select & Constrain**: To ensure we don't pick the same group in a different order, after picking candidate $i$, all subsequent choices must come from the *suffix* of the array (candidates $> i$).
3. **The `start` pointer**: We enforce this suffix rule by passing a `start` pointer to our recursive function.

### Visualizing Suffix Selection & Pruning

The true power in combinations comes from **Pruning**. If we need $k=3$ elements, and our current path has $1$ element, we need $2$ more. If there is only $1$ candidate left in our suffix, it is impossible to complete the combination. We should abort that branch immediately.

**The Loop-based Tree (n=4, k=3):**

```text
State: (start_idx, current_path)

                        (1, [])
              /            |            \
       (2, [1])         (3, [2])       (4, [3])
       /      \            |              |
 (3, [1,2]) (4, [1,3])  (4, [2,3])     ✗ (pruned: need 2 more, 0 avail)
     |          |          |
(4,[1,2,3])(5,[1,3,4]) ✗ (pruned)
     ✓          ✓
```

*Notice how `(4, [3])` is pruned. We need 3 elements, we have 1. We need 2 more, but only candidate `4` is left. Impossible.*

## Basic Implementation: Standard Backtracking

Here is the standard implementation using the `start` index pointer. Notice how we use a shared `path` array, pushing and popping to manage state, and explicitly copying `path[:]` when a valid combination is found.

```python
def combine(n: int, k: int) -> list[list[int]]:
    result = []

    # path: shared state array
    # start: suffix pointer enforcing order
    def backtrack(start: int, path: list[int]):
        # Base case: we hit our target size constraint
        if len(path) == k:
            result.append(path[:])  # CRITICAL: Append a copy, not the reference!
            return

        # Loop-based Suffix Selection
        # We try every candidate from 'start' up to 'n'
        for i in range(start, n + 1):
            path.append(i)         # Choose
            backtrack(i + 1, path) # Explore the suffix (i + 1)
            path.pop()             # Un-choose (backtrack)

    backtrack(1, [])
    return result
```

## Optimized Implementation: Mathematical Pruning

We can optimize the above code by aggressively pruning branches that don't have enough remaining candidates.

If we have `len(path)` elements, we need `need = k - len(path)` more elements.
We are currently evaluating candidate `i`. The available candidates from `i` to `n` inclusive is `n - i + 1`.
If `n - i + 1 < need`, we don't have enough candidates.

We can rewrite this inequality to find the strict upper bound for our `for` loop:
`n - i + 1 >= k - len(path)`
`i <= n - (k - len(path)) + 1`

```python
def combine_pruned(n: int, k: int) -> list[list[int]]:
    result = []

    def backtrack(start: int, path: list[int]):
        if len(path) == k:
            result.append(path[:])
            return

        # Optimization: Restrict the upper bound of the loop.
        # If we need 'need' more elements, we can't start our loop
        # higher than n - need + 1.
        need = k - len(path)
        upper_bound = n - need + 1

        for i in range(start, upper_bound + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result
```

## Variations: Combinations from an Array (with Duplicates)

What if instead of choosing from `1..n`, we choose from an array `nums` that might contain duplicates? E.g., `nums = [1, 2, 2], k = 2`.
Output should be `[[1, 2], [2, 2]]` (we don't want `[1, 2]` twice).

**Rule for Duplicates**: To avoid duplicate combinations, we **sort** the input array. Then, at any specific depth in our recursive tree (within the `for` loop), if the current candidate is identical to the previous candidate, we skip it.

```python
def combine_array_with_duplicates(nums: list[int], k: int) -> list[list[int]]:
    nums.sort()  # Step 1: Sort to place duplicates adjacent
    result = []

    def backtrack(start: int, path: list[int]):
        if len(path) == k:
            result.append(path[:])
            return

        for i in range(start, len(nums)):
            # Step 2: Skip identical elements at the SAME tree level
            # (i > start ensures we only skip if it's not the first element of this loop)
            if i > start and nums[i] == nums[i-1]:
                continue

            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

## Complexity Analysis

Let $n$ be the total number of items to choose from, and $k$ be the combination size.

- **Time Complexity**: $\mathcal{O}(k \cdot C(n, k))$
  - There are $C(n,k) = \frac{n!}{k!(n-k)!}$ valid combinations.
  - For each valid combination, we execute `result.append(path[:])`. Copying an array of size $k$ takes $\mathcal{O}(k)$ time.
  - The pruning ensures we don't spend significant time on dead-end branches.

- **Space/Memory Complexity**:
  - **Auxiliary Space (Call Stack + State)**: $\mathcal{O}(k)$
    - The maximum depth of the recursive call stack is $k$.
    - The shared `path` array takes $\mathcal{O}(k)$ space.
  - **Total Space (including Output)**: $\mathcal{O}(k \cdot C(n, k))$
    - We store $C(n,k)$ arrays, each of size $k$.

## Common Pitfalls

1. **Forgetting to copy the path**: `result.append(path)` stores a *reference* to the shared list. As you continue backtracking, `path` mutates, and your `result` will end up full of empty or incorrect lists (e.g., `[[], [], []]`). **Always do `result.append(path[:])` or `list(path)`**.
2. **$O(N)$ Slicing Anti-pattern**: Do not pass sliced arrays into the recursive function (e.g., `backtrack(candidates[i+1:])`). This creates a new array in memory for every call, ruining space and time complexity. Always pass the original array and an index pointer (`start`).
3. **Incorrect Duplicate Logic**: Writing `if nums[i] == nums[i-1]: continue` without checking `i > start` will skip valid combinations where the same number is used multiple times across *different* levels (e.g., preventing `[2, 2]`). The `i > start` condition correctly restricts the skipping to the *same* horizontal level of the tree.
