# Solutions: 0/1 Knapsack Patterns

## 1. 0/1 Knapsack (Basic)
**Problem:** Maximize value within capacity $W$ using each item at most once.

### Optimal Python Solution
```python
def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    # State: dp[w] = max value for capacity w
    # Key: Iterate backwards through capacity to ensure 0/1 property
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
```

### Complexity Analysis
- **Time:** $O(n \times W)$
- **Space:** $O(W)$

---

## 2. Partition Equal Subset Sum
**Problem:** Can array be partitioned into two subsets with equal sum?

### Optimal Python Solution
```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2: return False
    target = total // 2

    # Subset Sum Problem
    dp = [False] * (target + 1)
    dp[0] = True
    for n in nums:
        for i in range(target, n - 1, -1):
            dp[i] = dp[i] or dp[i - n]
    return dp[target]
```

### Complexity Analysis
- **Time:** $O(n \times \text{sum})$
- **Space:** $O(\text{sum})$

---

## 3. Target Sum
**Problem:** Ways to assign +/- to get target.

### Optimal Python Solution
```python
def find_target_sum_ways(nums: list[int], target: int) -> int:
    # P - N = target, P + N = sum => 2P = target + sum
    total = sum(nums)
    if (total + target) % 2 or abs(target) > total: return 0
    p = (total + target) // 2

    dp = [0] * (p + 1)
    dp[0] = 1
    for n in nums:
        for i in range(p, n - 1, -1):
            dp[i] += dp[i - n]
    return dp[p]
```

### Complexity Analysis
- **Time:** $O(n \times \text{sum})$
- **Space:** $O(\text{sum})$

---

## 4. Last Stone Weight II
**Problem:** Minimize remaining weight after smashing stones.

### Optimal Python Solution
```python
def last_stone_weight_ii(stones: list[int]) -> int:
    # Insight: Minimize difference between two groups
    # Maximize one group's sum up to total // 2
    total = sum(stones)
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for s in stones:
        for i in range(target, s - 1, -1):
            dp[i] = dp[i] or dp[i - s]

    for i in range(target, -1, -1):
        if dp[i]:
            return total - 2 * i
    return 0

---

## 5. Ones and Zeroes
**Problem:** Maximize number of strings you can form given `m` zeros and `n` ones.

### Optimal Python Solution
```python
def find_max_form(strs: list[str], m: int, n: int) -> int:
    # State: dp[i][j] = max strings using i zeros and j ones
    # 2D Knapsack (Two constraints)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for s in strs:
        zeros = s.count('0')
        ones = len(s) - zeros

        # Backward iteration for 0/1 knapsack property
        for i in range(m, zeros - 1, -1):
            for j in range(n, ones - 1, -1):
                dp[i][j] = max(dp[i][j], 1 + dp[i - zeros][j - ones])

    return dp[m][n]
```

### Explanation
1.  **Multiple Constraints**: Unlike standard knapsack with one capacity, this has two (zeros and ones).
2.  **State**: `dp[i][j]` stores the maximum number of strings achievable with `i` zeros and `j` ones available.
3.  **Iteration**: For each string, we calculate its "cost" (zeros and ones) and update the DP table backwards to ensure we only use each string once.

### Complexity Analysis
- **Time:** $O(L \times m \times n)$ - Where $L$ is the number of strings.
- **Space:** $O(m \times n)$ - To store the 2D capacity table.
```

### Complexity Analysis
- **Time:** $O(n \times \text{sum})$
- **Space:** $O(\text{sum})$
