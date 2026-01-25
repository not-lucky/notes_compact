# Solutions: House Robber Variants

## 1. House Robber (Linear)
**Problem:** Maximize sum of non-adjacent elements.

### Optimal Python Solution
```python
def rob(nums: list[int]) -> int:
    # State: dp[i] = max money from houses 0..i
    # Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    prev2, prev1 = 0, 0
    for n in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + n)
    return prev1
```

### Complexity Analysis
- **Time:** $O(n)$
- **Space:** $O(1)$

---

## 2. House Robber II (Circular)
**Problem:** Houses are arranged in a circle.

### Optimal Python Solution
```python
def rob_circular(nums: list[int]) -> int:
    if len(nums) == 1: return nums[0]

    def rob_linear(arr):
        p2, p1 = 0, 0
        for x in arr:
            p2, p1 = p1, max(p1, p2 + x)
        return p1

    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

### Complexity Analysis
- **Time:** $O(n)$
- **Space:** $O(1)$

---

## 3. House Robber III (Binary Tree)
**Problem:** Houses form a binary tree. Cannot rob parent and child.

### Optimal Python Solution
```python
def rob_tree(root) -> int:
    # Returns (max if rob current, max if skip current)
    def dfs(node):
        if not node: return (0, 0)

        left = dfs(node.left)
        right = dfs(node.right)

        # Rob this node: must skip children
        rob = node.val + left[1] + right[1]

        # Skip this node: children can be robbed or skipped
        skip = max(left) + max(right)

        return (rob, skip)

    return max(dfs(root))
```

### Complexity Analysis
- **Time:** $O(n)$ - Visit each node once.
- **Space:** $O(h)$ - Recursion stack height.

---

## 4. Delete and Earn
**Problem:** Earn points by picking numbers, but delete all `num-1` and `num+1`.

### Optimal Python Solution
```python
def delete_and_earn(nums: list[int]) -> int:
    # Key Insight: Transform to House Robber on points array
    if not nums: return 0

    max_num = max(nums)
    points = [0] * (max_num + 1)
    for num in nums:
        points[num] += num

    # House Robber on points
    prev2, prev1 = 0, 0
    for p in points:
        prev2, prev1 = prev1, max(prev1, prev2 + p)
    return prev1
```

### Complexity Analysis
- **Time:** $O(n + \text{max\_num})$
- **Space:** $O(\text{max\_num})$

---

## 5. Paint House
**Problem:** $n$ houses, 3 colors. Minimize cost such that no two adjacent houses have same color.

### Optimal Python Solution
```python
def min_cost(costs: list[list[int]]) -> int:
    # State: dp[i][color] = min cost to paint house i with color
    # Recurrence: dp[i][0] = costs[i][0] + min(dp[i-1][1], dp[i-1][2])
    if not costs: return 0

    prev = costs[0][:]
    for i in range(1, len(costs)):
        curr = [0] * 3
        curr[0] = costs[i][0] + min(prev[1], prev[2])
        curr[1] = costs[i][1] + min(prev[0], prev[2])
        curr[2] = costs[i][2] + min(prev[0], prev[1])
        prev = curr

    return min(prev)
```

### Complexity Analysis
- **Time:** $O(n)$
- **Space:** $O(1)$ - Only storing 3 color costs.

---

## 6. Paint House II
**Problem:** $n$ houses, $k$ colors. Minimize cost.

### Optimal Python Solution
```python
def min_cost_ii(costs: list[list[int]]) -> int:
    # Optimization: Keep track of min and second min from previous house
    if not costs: return 0
    n, k = len(costs), len(costs[0])

    prev_min = prev_second_min = 0
    prev_min_idx = -1

    for i in range(n):
        curr_min = curr_second_min = float('inf')
        curr_min_idx = -1

        for j in range(k):
            # If current color is same as previous house min color, use second min
            cost = costs[i][j] + (prev_second_min if j == prev_min_idx else prev_min)

            if cost < curr_min:
                curr_second_min = curr_min
                curr_min = cost
                curr_min_idx = j
            elif cost < curr_second_min:
                curr_second_min = cost

        prev_min, prev_second_min, prev_min_idx = curr_min, curr_second_min, curr_min_idx

    return prev_min
```

### Complexity Analysis
- **Time:** $O(nk)$ - By tracking min/second min, we avoid $O(nk^2)$.
- **Space:** $O(1)$
