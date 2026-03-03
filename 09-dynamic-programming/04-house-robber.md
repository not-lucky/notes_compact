# House Robber

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

The House Robber problem introduces the "take or skip" DP pattern. The goal is to maximize the sum of elements from an array under the constraint: **you cannot pick adjacent elements.**

## Problem Statement

You are a robber planning to rob houses along a street. Adjacent houses have security systems connected. Return the maximum amount of money you can rob without robbing adjacent houses.

---

## 1. House Robber I: Linear Array

### Building Intuition

At any given house `i`, you have exactly two choices:
1. **Rob it**: If you rob house `i`, you cannot have robbed house `i-1`. Therefore, the max money you can have is `nums[i]` plus the maximum money you could have robbed up to house `i-2`.
2. **Skip it**: If you skip house `i`, the maximum money you can have is just the maximum money you could have robbed up to house `i-1`.

**Why Greedy Fails:**
You might think "always pick the largest available house." But consider the array `[2, 7, 9, 3, 1]`.
- A greedy approach picks `9` (forcing you to skip `7` and `3`), then picks `2`, resulting in `11`.
- However, the optimal approach skips `7` and `3` implicitly by picking `2`, `9`, and `1`, yielding `12`.

Greedy fails because taking a locally optimal large number might lock you out of taking multiple slightly smaller numbers that sum to a greater total.

**The Recurrence Relation:**
Let `dp[i]` be the maximum money you can rob from houses `0` to `i`.
$$dp[i] = \max(\text{Rob house } i, \text{Skip house } i)$$
$$dp[i] = \max(nums[i] + dp[i-2], dp[i-1])$$

**Base Cases:**
- `dp[0] = nums[0]` (Only one house, you must rob it)
- `dp[1] = \max(nums[0], nums[1])` (Two houses, rob the one with more money)

### Approach 1: Top-Down Memoization

A great way to solve DP problems is to start top-down using recursion and memoization. We define a recursive function that asks "what is the maximum money we can rob from index `i` onwards?"

```python
def rob_memo(nums: list[int]) -> int:
    """
    Top-Down Recursion with Memoization.
    
    Time: O(n) - each index is evaluated once.
    Space: O(n) - for the recursion stack and memo dictionary.
    """
    memo = {}

    def dfs(i: int) -> int:
        # Base case: out of bounds
        if i >= len(nums):
            return 0
        
        # Return cached result if we've computed it before
        if i in memo:
            return memo[i]

        # Choice 1: Rob current house and skip next
        rob = nums[i] + dfs(i + 2)
        
        # Choice 2: Skip current house and evaluate next
        skip = dfs(i + 1)

        memo[i] = max(rob, skip)
        return memo[i]

    return dfs(0)
```

### Approach 2: Dynamic Programming (Bottom-Up, O(n) Space)

We can translate the top-down approach into a bottom-up iterative approach.

```python
def rob(nums: list[int]) -> int:
    """
    State: dp[i] = max money from houses 0..i
    Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    Time: O(n)
    Space: O(n) for the dp array
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    return dp[-1]
```

### Approach 3: Space-Optimized DP (O(1) Space)

Notice that to calculate `dp[i]`, we only ever need `dp[i-1]` and `dp[i-2]`. We don't need the entire array. We can reduce the space complexity to $O(1)$ by using two variables.

```python
def rob_optimized(nums: list[int]) -> int:
    """
    Space-optimized dynamic programming.

    Time: O(n)
    Space: O(1)
    """
    if not nums:
        return 0

    # rob1 represents dp[i-2]
    # rob2 represents dp[i-1]
    rob1 = 0
    rob2 = 0

    for n in nums:
        # Calculate the max if we rob the current house vs if we skip it
        # and shift variables forward for the next iteration
        temp = max(n + rob1, rob2)
        rob1 = rob2
        rob2 = temp

    return rob2
```

---

## 2. House Robber II: Circular Array

**Problem Statement:** You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are **arranged in a circle**. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent houses were broken into on the same night. Given an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

**Insight:** Because the first and last houses are adjacent, you cannot rob both of them. Therefore, the optimal solution must fall into one of two scenarios:
1. You rob from houses `0` to `n-2` (excluding the last house entirely).
2. You rob from houses `1` to `n-1` (excluding the first house entirely).

The answer is simply the maximum of these two scenarios.

### Approach 1: Top-Down Memoization

```python
def rob_circular_memo(nums: list[int]) -> int:
    """
    Top-Down Memoization for Circular Array.
    
    Time: O(n)
    Space: O(n)
    """
    if not nums: return 0
    if len(nums) == 1: return nums[0]

    def dfs(i: int, end: int, memo: dict) -> int:
        if i > end:
            return 0
        if i in memo:
            return memo[i]
            
        rob = nums[i] + dfs(i + 2, end, memo)
        skip = dfs(i + 1, end, memo)
        
        memo[i] = max(rob, skip)
        return memo[i]

    # Max of (omitting last house) and (omitting first house)
    return max(dfs(0, len(nums) - 2, {}), dfs(1, len(nums) - 1, {}))
```

### Approach 2: Space-Optimized DP

```python
def rob_circular(nums: list[int]) -> int:
    """
    Houses in a circle - first and last are adjacent.

    Time: O(n)
    Space: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    def rob_linear(houses: list[int]) -> int:
        rob1, rob2 = 0, 0
        for n in houses:
            rob1, rob2 = rob2, max(n + rob1, rob2)
        return rob2

    case1 = rob_linear(nums[:-1])
    case2 = rob_linear(nums[1:])

    return max(case1, case2)
```

---

## 3. House Robber III: Binary Tree

**Problem Statement:** The thief has found himself a new place for his thievery again. There is only one entrance to this area, called `root`. Besides the `root`, each house has one and only one parent house. After a tour, the smart thief realized that all houses in this place form a binary tree. It will automatically contact the police if two directly-linked houses were broken into on the same night. Given the `root` of the binary tree, return the maximum amount of money the thief can rob without alerting the police.

### Approach 1: Top-Down Memoization

We can memoize on the node and whether we are allowed to rob it or not (based on if its parent was robbed).

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def rob_tree_memo(root: TreeNode) -> int:
    """
    Top-Down Memoization on a Binary Tree.
    
    Time: O(n)
    Space: O(n) for memoization and call stack
    """
    memo = {}

    def dfs(node: TreeNode, can_rob: bool) -> int:
        if not node:
            return 0
        
        state = (node, can_rob)
        if state in memo:
            return memo[state]
            
        # We always have the option to skip the current node
        skip = dfs(node.left, True) + dfs(node.right, True)
        
        rob = 0
        if can_rob:
            # If we rob this node, we cannot rob its children
            rob = node.val + dfs(node.left, False) + dfs(node.right, False)
            
        memo[state] = max(rob, skip)
        return memo[state]

    return dfs(root, True)
```

### Approach 2: Optimized Tree DP (Post-order Traversal)

**Insight:** For any given node, we want to return two values to its parent:
1. The max money we can get if we **rob** this node.
2. The max money we can get if we **skip** this node.

At node `curr`:
- If we **rob** `curr`, we cannot rob its children. `rob_curr = curr.val + skip_left + skip_right`.
- If we **skip** `curr`, we are free to *either* rob or skip its children, whichever yields more! `skip_curr = max(rob_left, skip_left) + max(rob_right, skip_right)`.

```python
def rob_tree(root: TreeNode) -> int:
    """
    Optimized Tree DP returning (rob, skip) states.

    Time: O(n) where n is number of nodes
    Space: O(h) where h is height of tree (for recursion stack)
    """
    def dfs(node) -> tuple[int, int]:
        # Returns (max_if_robbed, max_if_skipped)
        if not node:
            return (0, 0)

        # Post-order traversal: process children first
        rob_left, skip_left = dfs(node.left)
        rob_right, skip_right = dfs(node.right)

        # Choice 1: Rob this node. Cannot rob children.
        rob_curr = node.val + skip_left + skip_right

        # Choice 2: Skip this node. Can either rob or skip children.
        skip_curr = max(rob_left, skip_left) + max(rob_right, skip_right)

        return (rob_curr, skip_curr)

    return max(dfs(root))
```

---

## 4. Related Problem: Delete and Earn

**Problem Statement:** You are given an integer array `nums`. You want to maximize the number of points you get by performing the following operation any number of times: Pick any `nums[i]` and delete it to earn `nums[i]` points. Afterwards, you must delete every element equal to `nums[i] - 1` and every element equal to `nums[i] + 1`. Return the maximum number of points you can earn by applying the above operation some number of times.

**Insight:** If you take a number `x`, you get points equal to `x * count(x)`. But you are forbidden from taking `x - 1` and `x + 1`. This is exactly House Robber!
1. Group the numbers by frequency/total value.
2. The "houses" are the unique numbers.
3. Robbing house `x` means taking `x * count(x)` and skipping houses `x-1` and `x+1`.

### Approach 1: Top-Down Memoization

```python
import collections

def delete_and_earn_memo(nums: list[int]) -> int:
    """
    Top-Down Memoization for Delete and Earn.
    
    Time: O(n log n) for sorting unique numbers
    Space: O(n) for hash map and memo
    """
    if not nums: return 0
    
    points = collections.Counter()
    for num in nums:
        points[num] += num
        
    unique_nums = sorted(points.keys())
    memo = {}
    
    def dfs(i: int) -> int:
        if i >= len(unique_nums):
            return 0
        if i in memo:
            return memo[i]
            
        curr_val = unique_nums[i]
        curr_points = points[curr_val]
        
        # If we rob this one, we must skip the next one if it's curr_val + 1
        next_idx = i + 1
        if next_idx < len(unique_nums) and unique_nums[next_idx] == curr_val + 1:
            rob = curr_points + dfs(i + 2)
        else:
            rob = curr_points + dfs(i + 1)
            
        skip = dfs(i + 1)
        
        memo[i] = max(rob, skip)
        return memo[i]
        
    return dfs(0)
```

### Approach 2: Space-Optimized DP

```python
import collections

def delete_and_earn(nums: list[int]) -> int:
    """
    Space-Optimized Bottom-Up DP.

    Time: O(n log n) due to sorting unique keys
    Space: O(n) for the hash map
    """
    if not nums:
        return 0

    points = collections.Counter()
    for num in nums:
        points[num] += num

    unique_nums = sorted(points.keys())

    earn1, earn2 = 0, 0

    for i in range(len(unique_nums)):
        curr_val = unique_nums[i]
        curr_points = points[curr_val]

        # If not adjacent, we don't have to skip the previous value
        if i > 0 and unique_nums[i] == unique_nums[i-1] + 1:
            earn1, earn2 = earn2, max(earn1 + curr_points, earn2)
        else:
            earn1, earn2 = earn2, earn2 + curr_points

    return earn2
```

---

## Reconstruction: Finding Which Houses Were Robbed

Sometimes an interviewer asks: *"What is the maximum profit AND which houses did you rob to get it?"*

To do this, we can't just use $O(1)$ space. We need the full `dp` array to track our decisions, and then we trace backward.

```python
def rob_with_path(nums: list[int]) -> tuple[int, list[int]]:
    if not nums:
        return 0, []
    if len(nums) == 1:
        return nums[0], [0]

    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    # Backtrack to find the path
    path = []
    i = len(nums) - 1

    while i >= 0:
        if i == 0:
            path.append(0)
            break

        prev_max = dp[i-2] if i >= 2 else 0

        # If taking current house + dp[i-2] equals optimal dp[i],
        # it was part of an optimal solution to take this house!
        if dp[i] == nums[i] + prev_max:
            path.append(i)
            i -= 2
        else:
            i -= 1

    return dp[-1], path[::-1] # Reverse path to be in ascending order
```

## Progressive Problems

1. **House Robber I** - Standard 1D DP.
2. **House Robber II** - Circular array logic.
3. **House Robber III** - DP on a tree using post-order traversal.
4. **Delete and Earn** - Transforming array values into frequencies.
5. **Maximum Alternating Subsequence Sum** - A variation where the operation alternates (add, subtract). Similar constraints and state transitions.
6. **Solving Questions With Brainpower** - Similar DP skipping logic, but instead of strictly skipping the next `1` element, you skip `brainpower[i]` elements. Good next step after House Robber.
7. **Paint House** - Adds another dimension. Instead of binary (rob/skip), you have multiple choices (red/blue/green), with the constraint that adjacent houses can't have the same color.

---

## Summary & Pattern Recognition

**Recognize the "House Robber" pattern when:**
- You must choose a subset of elements.
- Choosing an element strictly forbids choosing its immediate neighbors (adjacent constraint).
- Goal is to maximize or minimize a sum.

## Next: [05-coin-change.md](./05-coin-change.md)
