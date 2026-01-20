# Longest Consecutive Sequence

## Problem Statement

Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

**Example:**
```
Input: nums = [100, 4, 200, 1, 3, 2]
Output: 4
Explanation: The longest consecutive sequence is [1, 2, 3, 4]. Length = 4.
```

## Approach

### Key Insight
Use a hash set for O(1) lookups. For each number, only start counting if it's the beginning of a sequence (i.e., `num - 1` is not in the set).

### Algorithm
1. Put all numbers in a hash set
2. For each number:
   - If `num - 1` exists, skip (not the start of a sequence)
   - If `num - 1` doesn't exist, count consecutive numbers starting from `num`
3. Track maximum length

```
nums = [100, 4, 200, 1, 3, 2]
set = {100, 4, 200, 1, 3, 2}

100: 99 not in set → start sequence → 100 (length 1)
4: 3 in set → skip
200: 199 not in set → start sequence → 200 (length 1)
1: 0 not in set → start sequence → 1,2,3,4 (length 4)
3: 2 in set → skip
2: 1 in set → skip

Maximum: 4
```

## Implementation

```python
def longest_consecutive(nums: list[int]) -> int:
    """
    Find longest consecutive sequence.

    Time: O(n) - each number visited at most twice
    Space: O(n) - hash set
    """
    if not nums:
        return 0

    num_set = set(nums)
    max_length = 0

    for num in num_set:
        # Only start counting from sequence beginning
        if num - 1 not in num_set:
            current = num
            length = 1

            # Count consecutive numbers
            while current + 1 in num_set:
                current += 1
                length += 1

            max_length = max(max_length, length)

    return max_length


def longest_consecutive_union_find(nums: list[int]) -> int:
    """
    Alternative: Union-Find approach.

    Time: O(n × α(n)) ≈ O(n)
    Space: O(n)
    """
    if not nums:
        return 0

    parent = {}
    size = {}

    def find(x):
        if x not in parent:
            parent[x] = x
            size[x] = 1
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            if size[px] < size[py]:
                px, py = py, px
            parent[py] = px
            size[px] += size[py]

    num_set = set(nums)

    for num in num_set:
        find(num)  # Initialize
        if num - 1 in num_set:
            union(num, num - 1)
        if num + 1 in num_set:
            union(num, num + 1)

    return max(size.values()) if size else 0
```

## Complexity Analysis

| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n) | Each number visited at most twice (once for set, once for sequence counting) |
| Space | O(n) | Hash set stores all numbers |

### Why O(n) and not O(n²)?
The inner while loop seems like it could be O(n), making total O(n²). But:
- We only enter the while loop when `num - 1` is not in set
- Each number can only be the "next" element for one sequence start
- Therefore, each number is visited at most twice total

## Edge Cases

1. **Empty array**: Return 0
2. **Single element**: `[5]` → 1
3. **No consecutive**: `[10, 30, 50]` → 1
4. **All consecutive**: `[1, 2, 3, 4]` → 4
5. **Duplicates**: `[1, 2, 2, 3]` → Set handles this, returns 3
6. **Negative numbers**: `[-1, 0, 1]` → 3
7. **Large gaps**: Algorithm handles any gaps

## Common Mistakes

1. **Not using set**: Leads to O(n²) with list lookups
2. **Counting from every number**: Must check `num - 1` first
3. **Iterating over nums instead of set**: Duplicates cause issues
4. **Sorting approach**: Works but is O(n log n), not O(n)

## Why Not Sort?

Sorting would work but violates O(n) requirement:

```python
def longest_consecutive_sort(nums: list[int]) -> int:
    """O(n log n) sorting approach - NOT optimal."""
    if not nums:
        return 0

    nums = sorted(set(nums))  # Remove duplicates, sort
    max_length = 1
    current_length = 1

    for i in range(1, len(nums)):
        if nums[i] == nums[i-1] + 1:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 1

    return max_length
```

## Visual Walkthrough

```
nums = [100, 4, 200, 1, 3, 2]

Step 1: Build set {100, 4, 200, 1, 3, 2}

Step 2: Find sequence starts (num-1 not in set)
  - 100: 99 not in set ✓ (start)
  - 4: 3 in set ✗
  - 200: 199 not in set ✓ (start)
  - 1: 0 not in set ✓ (start)
  - 3: 2 in set ✗
  - 2: 1 in set ✗

Step 3: Count from each start
  - 100 → 101 not in set → length 1
  - 200 → 201 not in set → length 1
  - 1 → 2 → 3 → 4 → 5 not in set → length 4

Result: 4
```

## Variations

### Longest Consecutive Sequence in Binary Tree
```python
def longest_consecutive_tree(root) -> int:
    """
    Find longest path of consecutive values in binary tree.
    """
    def dfs(node, parent_val, length):
        if not node:
            return length

        if node.val == parent_val + 1:
            length += 1
        else:
            length = 1

        return max(length,
                   dfs(node.left, node.val, length),
                   dfs(node.right, node.val, length))

    return dfs(root, float('-inf'), 0)
```

### Binary Tree Longest Consecutive II (Any Direction)
```python
def longest_consecutive_ii(root) -> int:
    """
    Path can go in any direction (increasing or decreasing).
    """
    max_length = 0

    def dfs(node):
        nonlocal max_length
        if not node:
            return 0, 0  # (increasing, decreasing)

        inc = dec = 1

        if node.left:
            left_inc, left_dec = dfs(node.left)
            if node.left.val == node.val + 1:
                inc = max(inc, left_inc + 1)
            elif node.left.val == node.val - 1:
                dec = max(dec, left_dec + 1)

        if node.right:
            right_inc, right_dec = dfs(node.right)
            if node.right.val == node.val + 1:
                inc = max(inc, right_inc + 1)
            elif node.right.val == node.val - 1:
                dec = max(dec, right_dec + 1)

        max_length = max(max_length, inc + dec - 1)
        return inc, dec

    dfs(root)
    return max_length
```

## Related Problems

- **Longest Increasing Subsequence** - Not consecutive, uses DP
- **Longest Consecutive Path in Binary Tree**
- **Number of Connected Components** - Union-Find concept
- **Subarray Sum Equals K** - Hash map technique
