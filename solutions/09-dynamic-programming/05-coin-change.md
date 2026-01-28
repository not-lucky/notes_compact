# Solutions: Coin Change Patterns

## 1. Coin Change (Min Coins)

**Problem:** Minimum number of coins to make a total amount.

### Optimal Python Solution

```python
def coin_change(coins: list[int], amount: int) -> int:
    # State: dp[i] = min coins for amount i
    # Pattern: Unbounded Knapsack (Forward iteration)
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

### Complexity Analysis

- **Time:** $O(\text{amount} \times |coins|)$
- **Space:** $O(\text{amount})$

---

## 2. Coin Change II (Count Ways)

**Problem:** Number of combinations that make up the amount.

### Optimal Python Solution

```python
def change(amount: int, coins: list[int]) -> int:
    # Key: Outer loop is coins to ensure combinations (order doesn't matter)
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]
```

### Complexity Analysis

- **Time:** $O(\text{amount} \times |coins|)$
- **Space:** $O(\text{amount})$

---

## 3. Perfect Squares

**Problem:** Minimum perfect squares that sum to $n$.

### Optimal Python Solution

````python
def num_squares(n: int) -> int:
    # Same as Coin Change where coins are [1, 4, 9, ...]
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j*j] + 1)
            j += 1
    return dp[n]

```
---

## 4. Combination Sum IV
**Problem:** Count the number of permutations that sum to a target value using elements from an array.

### Optimal Python Solution
```python
def combination_sum_4(nums: list[int], target: int) -> int:
    # State: dp[i] = number of permutations that sum to i
    # Key: Outer loop is 'target' because order matters (permutations)
    dp = [0] * (target + 1)
    dp[0] = 1 # One way to make sum 0 (empty set)

    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                dp[i] += dp[i - num]
    return dp[target]
````

### Explanation

1.  **Permutations vs Combinations**: In "Coin Change II", we find combinations (order doesn't matter), so we iterate through coins first. Here, we find permutations (order matters), so we iterate through the target sum first.
2.  **Logic**: To reach sum `i`, we can take any number `num` from the array and add it to a permutation that sums to `i - num`.
3.  **Efficiency**: Since we iterate through the target once and check each number, the complexity is $O(\text{target} \times |nums|)$.

### Complexity Analysis

- **Time:** $O(\text{target} \times n)$
- **Space:** $O(\text{target})$

````

### Complexity Analysis
- **Time:** $O(n\sqrt{n})$
- **Space:** $O(n)$

---

## 4. Combination Sum IV
**Problem:** Number of permutations that sum to target.

### Optimal Python Solution
```python
def combination_sum_4(nums: list[int], target: int) -> int:
    # Key: Outer loop is target to count permutations (order matters)
    dp = [0] * (target + 1)
    dp[0] = 1

    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                dp[i] += dp[i - num]

    return dp[target]
````

### Complexity Analysis

- **Time:** $O(\text{target} \times |nums|)$
- **Space:** $O(\text{target})$

---

## 5. Integer Break

**Problem:** Break integer $n$ into $k \ge 2$ positive integers, maximize product.

### Optimal Python Solution

````python
def integer_break(n: int) -> int:
    # State: dp[i] = max product for number i
    if n <= 3: return n - 1

    dp = [0] * (n + 1)
    for i in range(1, 4): dp[i] = i

    for i in range(4, n + 1):
        # Try all possible breaks
        for j in range(1, i // 2 + 1):
            dp[i] = max(dp[i], dp[j] * dp[i - j])

    return dp[n]

```
---

## 4. Combination Sum IV
**Problem:** Count the number of permutations that sum to a target value using elements from an array.

### Optimal Python Solution
```python
def combination_sum_4(nums: list[int], target: int) -> int:
    # State: dp[i] = number of permutations that sum to i
    # Key: Outer loop is 'target' because order matters (permutations)
    dp = [0] * (target + 1)
    dp[0] = 1 # One way to make sum 0 (empty set)

    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                dp[i] += dp[i - num]
    return dp[target]
````

### Explanation

1.  **Permutations vs Combinations**: In "Coin Change II", we find combinations (order doesn't matter), so we iterate through coins first. Here, we find permutations (order matters), so we iterate through the target sum first.
2.  **Logic**: To reach sum `i`, we can take any number `num` from the array and add it to a permutation that sums to `i - num`.
3.  **Efficiency**: Since we iterate through the target once and check each number, the complexity is $O(\text{target} \times |nums|)$.

### Complexity Analysis

- **Time:** $O(\text{target} \times n)$
- **Space:** $O(\text{target})$

```

### Complexity Analysis
- **Time:** $O(n^2)$
- **Space:** $O(n)$
```
