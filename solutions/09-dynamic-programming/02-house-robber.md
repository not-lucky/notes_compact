# House Robber

## Problem Statement

You are a robber planning to rob houses along a street. Each house has a certain amount of money stashed. The constraint is that adjacent houses have connected security systems - if two adjacent houses are robbed on the same night, the police will be alerted.

Given an array `nums` representing the amount of money at each house, return the maximum amount you can rob without alerting the police.

**Example:**
```
Input: nums = [1, 2, 3, 1]
Output: 4
Explanation: Rob house 1 (money = 1) and house 3 (money = 3).

Input: nums = [2, 7, 9, 3, 1]
Output: 12
Explanation: Rob houses 1, 3, and 5 (2 + 9 + 1 = 12).
```

## Approach

### Key Insight
For each house, you have two choices:
1. **Rob it**: Add its value to the max from houses before the previous one
2. **Skip it**: Take the max from the previous house

`dp[i] = max(dp[i-1], dp[i-2] + nums[i])`

### Optimization
Only need the last two values, not the entire array.

## Implementation

```python
def rob(nums: list[int]) -> int:
    """
    Find maximum robbery amount using optimized DP.

    Time: O(n)
    Space: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2 = 0  # max if we're 2 houses back
    prev1 = 0  # max if we're 1 house back

    for num in nums:
        current = max(prev1, prev2 + num)
        prev2 = prev1
        prev1 = current

    return prev1


def rob_dp_array(nums: list[int]) -> int:
    """
    DP with array (more intuitive).

    Time: O(n)
    Space: O(n)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])

    for i in range(2, n):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    return dp[-1]


def rob_memo(nums: list[int]) -> int:
    """
    Top-down with memoization.

    Time: O(n)
    Space: O(n)
    """
    memo = {}

    def helper(i: int) -> int:
        if i < 0:
            return 0
        if i in memo:
            return memo[i]

        memo[i] = max(helper(i - 1), helper(i - 2) + nums[i])
        return memo[i]

    return helper(len(nums) - 1)
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Optimized DP | O(n) | O(1) | Best for interviews |
| DP Array | O(n) | O(n) | More intuitive |
| Memoization | O(n) | O(n) | Top-down approach |

## Visual Walkthrough

```
nums = [2, 7, 9, 3, 1]

Step-by-step:
i=0: prev2=0, prev1=0
     current = max(0, 0+2) = 2
     prev2=0, prev1=2

i=1: prev2=0, prev1=2
     current = max(2, 0+7) = 7
     prev2=2, prev1=7

i=2: prev2=2, prev1=7
     current = max(7, 2+9) = 11
     prev2=7, prev1=11

i=3: prev2=7, prev1=11
     current = max(11, 7+3) = 11
     prev2=11, prev1=11

i=4: prev2=11, prev1=11
     current = max(11, 11+1) = 12
     prev2=11, prev1=12

Result: 12
```

## Edge Cases

1. **Empty array**: Return 0
2. **Single house**: Return that value
3. **Two houses**: Return max of the two
4. **All same values**: Every other house optimal
5. **Zero values**: Skip them in optimal solution

## Common Mistakes

1. **Not handling n=1 or n=2**: Special cases
2. **Wrong recurrence**: Must be `max(skip, take)` not `max(take, skip+current)`
3. **Off-by-one with indices**: Careful with starting conditions
4. **Forgetting the "+nums[i]"**: Adding current house value

## Variations

### House Robber II (Circular)
```python
def rob_circular(nums: list[int]) -> int:
    """
    Houses arranged in circle (first and last are adjacent).

    Solution: Take max of:
    1. Rob houses 0 to n-2 (exclude last)
    2. Rob houses 1 to n-1 (exclude first)

    Time: O(n)
    Space: O(1)
    """
    if len(nums) == 1:
        return nums[0]

    def rob_range(start: int, end: int) -> int:
        prev2 = prev1 = 0
        for i in range(start, end):
            current = max(prev1, prev2 + nums[i])
            prev2 = prev1
            prev1 = current
        return prev1

    return max(rob_range(0, len(nums) - 1),
               rob_range(1, len(nums)))
```

### House Robber III (Binary Tree)
```python
def rob_tree(root) -> int:
    """
    Houses form a binary tree.

    At each node, either:
    1. Rob this node + grandchildren
    2. Skip this node, rob children

    Time: O(n)
    Space: O(h)
    """
    def dfs(node):
        """Return (rob_this_node, skip_this_node)."""
        if not node:
            return 0, 0

        left_rob, left_skip = dfs(node.left)
        right_rob, right_skip = dfs(node.right)

        # Rob this node: can't rob children, take grandchildren values
        rob = node.val + left_skip + right_skip

        # Skip this node: take max from each child subtree
        skip = max(left_rob, left_skip) + max(right_rob, right_skip)

        return rob, skip

    return max(dfs(root))
```

### Paint House (Similar Pattern)
```python
def min_cost_paint_houses(costs: list[list[int]]) -> int:
    """
    costs[i][j] = cost to paint house i with color j (0, 1, 2).
    No two adjacent houses can be same color.

    Time: O(n)
    Space: O(1)
    """
    if not costs:
        return 0

    # prev[j] = min cost to paint up to previous house with color j
    prev = costs[0][:]

    for i in range(1, len(costs)):
        curr = [0, 0, 0]
        curr[0] = costs[i][0] + min(prev[1], prev[2])
        curr[1] = costs[i][1] + min(prev[0], prev[2])
        curr[2] = costs[i][2] + min(prev[0], prev[1])
        prev = curr

    return min(prev)
```

### Delete and Earn
```python
def delete_and_earn(nums: list[int]) -> int:
    """
    Pick a number x, earn x points, delete all x-1 and x+1.

    Transform to house robber: bucket by value.
    Picking value x means can't pick x-1 or x+1.

    Time: O(n + max(nums))
    Space: O(max(nums))
    """
    if not nums:
        return 0

    max_num = max(nums)
    points = [0] * (max_num + 1)

    for num in nums:
        points[num] += num

    # Now it's house robber on points array
    prev2 = prev1 = 0
    for point in points:
        current = max(prev1, prev2 + point)
        prev2 = prev1
        prev1 = current

    return prev1
```

## Related Problems

- **House Robber II** - Circular houses
- **House Robber III** - Tree structure
- **Delete and Earn** - Transform to house robber
- **Paint House** - Similar DP pattern
- **Maximum Sum Non-Adjacent** - Same problem, different name
- **Climbing Stairs** - Same recurrence structure
