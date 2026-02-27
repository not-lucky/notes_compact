# House Robber

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

The House Robber problem is the canonical "take or skip" Dynamic Programming (DP) problem. The goal is to maximize the sum of elements chosen from an array while respecting a constraint: you cannot pick adjacent elements.

It's an essential pattern because it introduces the concept of making decisions that have localized consequences (choosing index `i` only affects your ability to choose `i-1` and `i+1`).

## Problem Statement

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and **it will automatically contact the police if two adjacent houses were broken into on the same night.**

Given an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight **without alerting the police**.

**Example:**
```text
Input: nums = [2, 7, 9, 3, 1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.
(Wait, house 1 is index 0... let's use 0-indexed terms to match the code!)
Rob house 0 (money = 2), rob house 2 (money = 9) and rob house 4 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.
```

---

## 1. House Robber I: Linear Array

### Building Intuition

At any given house `i`, you have exactly two choices:
1. **Rob it**: If you rob house `i`, you cannot have robbed house `i-1`. Therefore, the max money you can have is `nums[i]` plus the maximum money you could have robbed up to house `i-2`.
2. **Skip it**: If you skip house `i`, the maximum money you can have is just the maximum money you could have robbed up to house `i-1`.

**Why Greedy Fails:**
You might think "always rob the higher-value house." But consider `[2, 10, 3, 11]`. A greedy approach might pick 10 (which forces you to skip 2 and 3), leaving you with `10 + 11` wait, you can't pick 11 if you picked 10. Wait, 10 and 11 are adjacent in `[..., 10, 3, 11]`? No, they are separated by 3.
Let's trace: pick 11 (skip 3), pick 10 (skip 2). `10 + 11 = 21`.
Let's try a better example where greedy fails: `[2, 1, 1, 2]`. Greedy picks 2 (index 0) and 2 (index 3). Total 4. Wait, greedy works here.
Let's try: `[100, 1, 1, 100]`. Picks 100 and 100.
Let's try: `[2, 7, 9, 3, 1]`. Greedy picks 9 (skip 7, 3), then picks 2. Total 11. But optimal is `2 + 9 + 1 = 12`. Here greedy (pick max available) fails!

**The Recurrence Relation:**
Let `dp[i]` be the maximum money you can rob from houses `0` to `i`.
$$dp[i] = \max(\text{Rob house } i, \text{Skip house } i)$$
$$dp[i] = \max(nums[i] + dp[i-2], dp[i-1])$$

**Base Cases:**
- `dp[0] = nums[0]` (Only one house, you must rob it)
- `dp[1] = \max(nums[0], nums[1])` (Two houses, rob the one with more money)

### Approach 1: Dynamic Programming (O(n) Space)

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

### Approach 2: Space-Optimized DP (O(1) Space)

Notice that to calculate `dp[i]`, we only ever need `dp[i-1]` and `dp[i-2]`. We don't need the entire array. We can reduce the space complexity to $O(1)$ by using two variables to track the previous two results.

```python
def rob(nums: list[int]) -> int:
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
        # temp is our new dp[i]
        temp = max(n + rob1, rob2)
        rob1 = rob2
        rob2 = temp

    return rob2
```

*Note on the clean logic:* Using `rob1 = 0, rob2 = 0` and iterating over the entire array simplifies the base case handling. For the first house `n`, `temp = max(n + 0, 0) = n`. Then `rob1 = 0, rob2 = n`. For the second house, `temp = max(n2 + 0, n1) = max(n1, n2)`. It naturally handles `len(nums) == 1` and `len(nums) == 2` without explicit `if` checks!

---

## 2. House Robber II: Circular Array

**Problem:** Houses are arranged in a circle. That means the first house is adjacent to the last house.

**Insight:** Because the first and last houses are adjacent, you cannot rob both of them. Therefore, the optimal solution must fall into one of two scenarios:
1. You rob from houses `0` to `n-2` (excluding the last house).
2. You rob from houses `1` to `n-1` (excluding the first house).

The answer is simply the maximum of these two scenarios!

```python
def rob_circular(nums: list[int]) -> int:
    """
    Houses in a circle - first and last are adjacent.

    Time: O(n)
    Space: O(1)
    """
    # Edge cases are important here because slicing nums[1:]
    # when len(nums) == 1 would return an empty array
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    # Helper function using the space-optimized logic from House Robber I
    def rob_linear(houses: list[int]) -> int:
        rob1, rob2 = 0, 0
        for n in houses:
            temp = max(n + rob1, rob2)
            rob1 = rob2
            rob2 = temp
        return rob2

    # Case 1: Exclude the last house
    case1 = rob_linear(nums[:-1])

    # Case 2: Exclude the first house
    case2 = rob_linear(nums[1:])

    return max(case1, case2)
```

---

## 3. House Robber III: Binary Tree

**Problem:** The houses form a binary tree. If two directly-linked houses are broken into on the same night, the police are alerted. (You cannot rob a node and its parent).

**Insight:** This combines Tree Traversal (DFS/Post-order) with DP. For any given node, we want to return two values to its parent:
1. The max money we can get if we **rob** this node.
2. The max money we can get if we **do not rob** this node.

At node `curr`:
- If we **rob** `curr`, we cannot rob its children. Thus, `rob_curr = curr.val + skip_left + skip_right`.
- If we **skip** `curr`, we are free to *either* rob or skip its children, whichever yields more money! Thus, `skip_curr = max(rob_left, skip_left) + max(rob_right, skip_right)`.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def rob_tree(root: TreeNode) -> int:
    """
    Houses form a binary tree.

    Time: O(n) where n is number of nodes
    Space: O(h) where h is height of tree (for recursion stack)
    """
    def dfs(node) -> tuple[int, int]:
        # Returns (max_with_node, max_without_node)
        if not node:
            return (0, 0)

        # Post-order traversal: process children first
        left_with, left_without = dfs(node.left)
        right_with, right_without = dfs(node.right)

        # Choice 1: Rob this node. Cannot rob children.
        with_node = node.val + left_without + right_without

        # Choice 2: Skip this node. Can either rob or skip children.
        # We take the max of (with, without) for each child independently!
        without_node = max(left_with, left_without) + max(right_with, right_without)

        return (with_node, without_node)

    # Return the max of robbing or not robbing the root
    return max(dfs(root))
```

---

## 4. Related Problem: Delete and Earn

**Problem:** Given an array of integers `nums`, you can perform operations. In each operation, you pick any `nums[i]`, earn `nums[i]` points, and must delete **every** element equal to `nums[i] - 1` or `nums[i] + 1`. Maximize your points.

**Insight:** If you take a number `x`, you get points equal to `x * count(x)`. But you are forbidden from taking `x - 1` and `x + 1`. This is exactly House Robber!
1. Group the numbers by frequency/total value.
2. The "houses" are the unique numbers `0` through `max(nums)`.
3. Robbing house `x` means taking `x * count(x)` and skipping houses `x-1` and `x+1`.

```python
import collections

def delete_and_earn(nums: list[int]) -> int:
    """
    Transform array into a House Robber problem.

    Time: O(n + max_val)
    Space: O(max_val)
    """
    if not nums:
        return 0

    # Count how much points we can get for each specific number
    points = collections.Counter()
    max_val = 0
    for num in nums:
        points[num] += num
        max_val = max(max_val, num)

    # Standard House Robber logic
    rob1 = 0
    rob2 = 0

    # We must iterate from 0 up to max_val to handle adjacent values correctly
    for i in range(max_val + 1):
        temp = max(points[i] + rob1, rob2)
        rob1 = rob2
        rob2 = temp

    return rob2
```

*(Note: If `max_val` is huge and `n` is small, you can optimize this by sorting the unique keys of the counter, but the basic logic remains the same: if `keys[i] == keys[i-1] + 1`, apply the robber recurrence; otherwise, you can safely add `keys[i]` points to the total without skipping).*

---

## Reconstruction: Finding Which Houses Were Robbed

Sometimes an interviewer asks: *"What is the maximum profit AND which houses did you rob to get it?"*

To do this, we can't just use $O(1)$ space. We need the full `dp` array, and we trace backwards.

```python
def rob_with_path(nums: list[int]) -> tuple[int, list[int]]:
    if not nums: return 0, []
    if len(nums) == 1: return nums[0], [0]

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
        if i == 1:
            if nums[1] > nums[0]:
                path.append(1)
            else:
                path.append(0)
            break

        # If dp[i] comes from dp[i-1], we skipped house i
        # If dp[i] comes from dp[i-2] + nums[i], we robbed house i
        if dp[i] == dp[i-1]:
            i -= 1 # Move to the house we actually took
        else:
            path.append(i)
            i -= 2 # Skip the adjacent house

    return dp[-1], path[::-1] # Reverse path to be in ascending order
```

---

## Summary & Pattern Recognition

**Recognize the "House Robber" pattern when:**
- You must choose a subset of elements.
- Choosing an element strictly forbids choosing its immediate neighbors (adjacent constraint).
- Goal is to maximize or minimize a sum.

**When NOT to use this exact recurrence:**
- Constraint is "no three consecutive" (you need to track more state: `dp[i] = max(dp[i-1], nums[i]+dp[i-2], nums[i]+nums[i-1]+dp[i-3]...)`).
- Elements can be picked multiple times (this moves into Unbounded Knapsack territory).

## Next: [05-coin-change.md](./05-coin-change.md)

Learn the classic unbounded knapsack pattern with Coin Change.
