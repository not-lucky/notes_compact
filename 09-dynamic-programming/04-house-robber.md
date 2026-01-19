# House Robber

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Interview Context

House Robber is a FANG+ classic because:

1. **Clean DP introduction**: Simple state transition
2. **Multiple variants**: Tests adaptability
3. **Space optimization**: Natural O(1) optimization
4. **Common pattern**: Take/skip decision appears everywhere

---

## Problem Statement

You're robbing houses along a street. Adjacent houses have connected alarms. Maximize loot without triggering alarms (can't rob adjacent houses).

```
Input: [2, 7, 9, 3, 1]
Output: 12 (rob houses 0, 2, 4: 2 + 9 + 1 = 12)
       OR (rob houses 1, 3: 7 + 3 = 10) - less optimal
```

---

## House Robber I: Linear Array

### Approach

At each house, two choices:
1. **Rob it**: Add value + best from 2 houses back
2. **Skip it**: Take best from previous house

```python
def rob(nums: list[int]) -> int:
    """
    Maximum sum of non-adjacent elements.

    State: dp[i] = max money from houses 0..i
    Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    Time: O(n)
    Space: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        curr = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = curr

    return prev1
```

### Visual Walkthrough

```
nums = [2, 7, 9, 3, 1]

i=0: dp[0] = 2 (only option)
i=1: dp[1] = max(2, 7) = 7 (rob house 1)
i=2: dp[2] = max(7, 2+9) = 11 (rob houses 0, 2)
i=3: dp[3] = max(11, 7+3) = 11 (skip house 3)
i=4: dp[4] = max(11, 11+1) = 12 (rob houses 0, 2, 4)

Answer: 12
```

---

## House Robber II: Circular Array

Houses form a circle - first and last are adjacent.

### Key Insight

Can't rob both first and last. So:
1. Rob houses 0 to n-2 (exclude last)
2. Rob houses 1 to n-1 (exclude first)
3. Take maximum

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
    if len(nums) == 2:
        return max(nums)

    def rob_linear(houses: list[int]) -> int:
        prev2, prev1 = 0, 0
        for money in houses:
            curr = max(prev1, prev2 + money)
            prev2 = prev1
            prev1 = curr
        return prev1

    # Case 1: Rob houses 0 to n-2
    case1 = rob_linear(nums[:-1])

    # Case 2: Rob houses 1 to n-1
    case2 = rob_linear(nums[1:])

    return max(case1, case2)
```

### Why This Works

```
Circle: [2, 3, 2]
        ↑_____↓ (connected)

If we rob house 0, we can't rob house 2 (last)
If we rob house 2, we can't rob house 0 (first)

Case 1: [2, 3] → max = 3
Case 2: [3, 2] → max = 3
Answer: 3
```

---

## House Robber III: Binary Tree

Houses form a binary tree. Can't rob parent and child directly.

```python
def rob_tree(root) -> int:
    """
    Houses form a binary tree.

    State: For each node, track (rob_it, skip_it)

    Time: O(n)
    Space: O(h) for recursion stack
    """
    def dfs(node) -> tuple[int, int]:
        """
        Returns (max if rob this node, max if skip this node)
        """
        if not node:
            return (0, 0)

        left = dfs(node.left)
        right = dfs(node.right)

        # If rob this node, can't rob children
        rob = node.val + left[1] + right[1]

        # If skip this node, take best from each child
        skip = max(left) + max(right)

        return (rob, skip)

    return max(dfs(root))
```

### Visual Example

```
      3
     / \
    2   3
     \   \
      3   1

DFS from leaves:
- Node 3 (left leaf): (3, 0)
- Node 1 (right leaf): (1, 0)
- Node 2: rob=2+0=2, skip=max(3,0)=3 → (2, 3)
- Node 3 (right child): rob=3+0=3, skip=max(1,0)=1 → (3, 1)
- Node 3 (root): rob=3+3+1=7, skip=max(2,3)+max(3,1)=3+3=6 → (7, 6)

Answer: max(7, 6) = 7
```

---

## Related: Delete and Earn

Transform to House Robber.

```python
def delete_and_earn(nums: list[int]) -> int:
    """
    Pick num, earn num points, delete all num-1 and num+1.

    Insight: Group by value, then House Robber!

    Time: O(n + max_num)
    Space: O(max_num)
    """
    if not nums:
        return 0

    max_num = max(nums)
    points = [0] * (max_num + 1)

    # Sum points for each value
    for num in nums:
        points[num] += num

    # House Robber on points array
    prev2, prev1 = 0, 0

    for i in range(max_num + 1):
        curr = max(prev1, prev2 + points[i])
        prev2 = prev1
        prev1 = curr

    return prev1
```

### Why It Works

```
nums = [2, 2, 3, 3, 3, 4]

points = [0, 0, 4, 9, 4]
          ^  ^  ^  ^  ^
          0  1  2  3  4

If we take 3s (value 9), we delete all 2s and 4s
Same as House Robber: can't take adjacent indices!

House Robber on points:
i=0: dp = 0
i=1: dp = 0
i=2: dp = max(0, 0+4) = 4
i=3: dp = max(4, 0+9) = 9
i=4: dp = max(9, 4+4) = 9

Answer: 9 (take all the 3s)
```

---

## Related: Paint House

n houses, 3 colors, minimize cost. Adjacent can't be same color.

```python
def min_cost(costs: list[list[int]]) -> int:
    """
    costs[i] = [red_cost, blue_cost, green_cost] for house i.

    State: dp[i][c] = min cost for houses 0..i with house i painted color c

    Time: O(n)
    Space: O(1)
    """
    if not costs:
        return 0

    # Previous house costs for each color
    prev = costs[0][:]

    for i in range(1, len(costs)):
        curr = [0, 0, 0]
        curr[0] = costs[i][0] + min(prev[1], prev[2])
        curr[1] = costs[i][1] + min(prev[0], prev[2])
        curr[2] = costs[i][2] + min(prev[0], prev[1])
        prev = curr

    return min(prev)
```

---

## Alternative Formulations

### Include/Exclude Tracking

```python
def rob_with_tracking(nums: list[int]) -> tuple[int, list[int]]:
    """
    Return max money and which houses to rob.
    """
    n = len(nums)
    if n == 0:
        return 0, []
    if n == 1:
        return nums[0], [0]

    dp = [0] * n
    parent = [-1] * n  # Track decisions

    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    parent[1] = -1 if nums[1] > nums[0] else 0

    for i in range(2, n):
        if dp[i - 1] > dp[i - 2] + nums[i]:
            dp[i] = dp[i - 1]
            parent[i] = parent[i - 1]
        else:
            dp[i] = dp[i - 2] + nums[i]
            parent[i] = i

    # Reconstruct path
    houses = []
    i = n - 1
    while i >= 0:
        if parent[i] == i or (i == 0 and dp[0] == nums[0]):
            houses.append(i)
            i -= 2
        else:
            i -= 1

    return dp[-1], houses[::-1]
```

---

## Edge Cases

```python
# 1. Empty array
nums = []
# Return 0

# 2. Single house
nums = [5]
# Return 5

# 3. Two houses
nums = [5, 10]
# Return 10

# 4. All same value
nums = [5, 5, 5, 5]
# Return 10 (houses 0, 2 or 1, 3)

# 5. Decreasing values
nums = [10, 5, 3, 1]
# Return 13 (houses 0, 2)
```

---

## Common Mistakes

```python
# WRONG: Not handling single element
def rob(nums):
    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])  # IndexError if len=1
    ...

# CORRECT:
if len(nums) == 1:
    return nums[0]


# WRONG: Wrong update order
for i in range(2, n):
    prev2 = prev1
    prev1 = max(prev1, prev2 + nums[i])  # prev2 already updated!

# CORRECT:
for i in range(2, n):
    curr = max(prev1, prev2 + nums[i])
    prev2 = prev1
    prev1 = curr


# WRONG: Circular - not excluding endpoints correctly
def rob_circular(nums):
    return max(rob(nums[1:]), rob(nums[:n-1]))  # Wrong for n=2
```

---

## Complexity Analysis

| Variant | Time | Space |
|---------|------|-------|
| Linear | O(n) | O(1) |
| Circular | O(n) | O(1) |
| Tree | O(n) | O(h) |
| Delete and Earn | O(n + max) | O(max) |
| Paint House | O(n × k²) | O(k) |

---

## Interview Tips

1. **Start with recurrence**: "At each house, I can rob or skip"
2. **Identify dependencies**: "Current depends on i-1 and i-2"
3. **Optimize space**: "Only need last two values"
4. **Handle variants**: "Circular means exclude one end"
5. **Watch edge cases**: Empty, single, two elements

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | House Robber | Medium | Basic take/skip |
| 2 | House Robber II | Medium | Circular = two linear |
| 3 | House Robber III | Medium | Tree DP with states |
| 4 | Delete and Earn | Medium | Transform to HR |
| 5 | Paint House | Medium | Multi-state DP |
| 6 | Paint House II | Hard | K colors optimization |

---

## Key Takeaways

1. **Core pattern**: `dp[i] = max(skip, take)`
2. **Space optimization**: Only O(1) needed
3. **Circular handling**: Run twice, exclude one end each time
4. **Tree version**: Return tuple (rob, skip) from each node
5. **Transform problems**: Recognize House Robber in disguise

---

## Next: [05-coin-change.md](./05-coin-change.md)

Learn the classic unbounded knapsack pattern with Coin Change.
