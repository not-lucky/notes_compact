# Combination Sum - Solutions

This document provides optimal solutions and detailed explanations for the practice problems related to Combination Sum.

---

## 1. Combination Sum (Unlimited Reuse)

### Problem Statement
Given an array of distinct integers `candidates` and a `target` integer, return a list of all unique combinations where the chosen numbers sum to `target`. You may return the combinations in any order. The same number may be chosen from `candidates` an unlimited number of times.

### Examples & Edge Cases
- **Input:** candidates = [2,3,6,7], target = 7 → **Output:** [[2,2,3],[7]]
- **Edge Case:** Target smaller than all candidates → [].

### Optimal Python Solution (Backtracking with Pruning)
```python
def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort() # Sort for pruning
    res = []

    def backtrack(start: int, current: list[int], remaining: int):
        if remaining == 0:
            res.append(current[:])
            return

        for i in range(start, len(candidates)):
            # Pruning: if current number is > remaining, no future number will work
            if candidates[i] > remaining:
                break

            current.append(candidates[i])
            # Pass 'i' instead of 'i+1' to allow reuse of the same element
            backtrack(i, current, remaining - candidates[i])
            current.pop()

    backtrack(0, [], target)
    return res
```

### Detailed Explanation
1. **Decision Tree**: At each step, we can either use the current number again or move to the next number.
2. **Reuse**: By passing the current index `i` to the next `backtrack` call, we allow the algorithm to pick the same number multiple times.
3. **Pruning**: Sorting the candidates allows us to `break` the loop early if `candidates[i]` exceeds the `remaining` target.

### Complexity Analysis
- **Time Complexity:** $O(N^{\frac{T}{M} + 1})$ - Where $N$ is number of candidates, $T$ is target, $M$ is minimum candidate value.
- **Space Complexity:** $O(\frac{T}{M})$ - Maximum depth of the recursion stack.

---

## 2. Combination Sum II (No Reuse, Duplicates in Input)

### Problem Statement
Given a collection of candidate numbers `candidates` and a `target` number, find all unique combinations where the candidate numbers sum to `target`. Each number in `candidates` may only be used once in the combination. Note: The solution set must not contain duplicate combinations.

### Examples & Edge Cases
- **Input:** [10,1,2,7,6,1,5], target = 8 → **Output:** [[1,1,6],[1,2,5],[1,7],[2,6]]

### Optimal Python Solution (Backtracking with Duplicate Skipping)
```python
def combinationSum2(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()
    res = []

    def backtrack(start: int, current: list[int], remaining: int):
        if remaining == 0:
            res.append(current[:])
            return

        for i in range(start, len(candidates)):
            # Duplicate Skipping:
            if i > start and candidates[i] == candidates[i-1]:
                continue

            # Pruning:
            if candidates[i] > remaining:
                break

            current.append(candidates[i])
            # Pass 'i+1' to ensure each element is used only once
            backtrack(i + 1, current, remaining - candidates[i])
            current.pop()

    backtrack(0, [], target)
    return res
```

### Detailed Explanation
1. **No Reuse**: We pass `i + 1` to the recursive call to ensure we don't pick the exact same index again.
2. **Duplicate Handling**: Because the input can have identical values (e.g., two `1`s), we sort and use `if i > start and candidates[i] == candidates[i-1]: continue` to ensure we don't start the same combination twice at the same recursion depth.

### Complexity Analysis
- **Time Complexity:** $O(2^N)$ - In the worst case, every element is either in or out.
- **Space Complexity:** $O(N)$ - Recursion stack depth.

---

## 3. Combination Sum III (k numbers from 1-9)

### Problem Statement
Find all valid combinations of `k` numbers that sum up to `n` such that only numbers `1` through `9` are used and each number is used at most once.

### Examples & Edge Cases
- **Input:** k = 3, n = 7 → **Output:** [[1,2,4]]

### Optimal Python Solution (Backtracking)
```python
def combinationSum3(k: int, n: int) -> list[list[int]]:
    res = []

    def backtrack(start: int, current: list[int], remaining: int):
        if len(current) == k:
            if remaining == 0:
                res.append(current[:])
            return

        for i in range(start, 10):
            if i > remaining:
                break

            current.append(i)
            backtrack(i + 1, current, remaining - i)
            current.pop()

    backtrack(1, [], n)
    return res
```

### Detailed Explanation
This is a standard combinations problem with an added sum constraint. We restrict our search space to numbers 1 through 9 and the combination length to `k`.

### Complexity Analysis
- **Time Complexity:** $O(\binom{9}{k} \cdot k)$
- **Space Complexity:** $O(k)$

---

## 4. Combination Sum IV (Order Matters - DP)

### Problem Statement
Given an array of distinct integers `nums` and a `target` integer `target`, return the number of possible combinations that add up to `target`. Note that different sequences are counted as different combinations (e.g., [1,2] and [2,1] are different).

### Examples & Edge Cases
- **Input:** nums = [1,2,3], target = 4 → **Output:** 7

### Optimal Python Solution (Dynamic Programming)
```python
def combinationSum4(nums: list[int], target: int) -> int:
    # dp[i] will store the number of ways to reach sum i
    dp = [0] * (target + 1)
    dp[0] = 1 # One way to reach 0: use no numbers

    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                dp[i] += dp[i - num]

    return dp[target]
```

### Detailed Explanation
1. **Permutations vs Combinations**: Because order matters, this is closer to finding permutations with repetition.
2. **DP Transition**: To reach sum `i`, we can take any number `num` from our list. The number of ways to reach `i` is the sum of ways to reach `i - num` for all `num` in `nums`.

### Complexity Analysis
- **Time Complexity:** $O(T \cdot N)$ - Where $T$ is target and $N$ is number of candidates.
- **Space Complexity:** $O(T)$ - To store the DP table.

---

## 5. Target Sum (+/- Choices)

### Problem Statement
You are given an integer array `nums` and an integer `target`. You want to build an expression out of nums by adding one of the symbols '+' and '-' before each integer and then concatenate all the integers. Return the number of different expressions that you can build, which evaluates to `target`.

### Optimal Python Solution (DP with Space Optimization)
```python
def findTargetSumWays(nums: list[int], target: int) -> int:
    # Let P be sum of numbers with '+' and N be sum of numbers with '-'
    # P + N = sum(nums)
    # P - N = target
    # 2P = sum(nums) + target => P = (sum(nums) + target) / 2
    # So we just need to find combinations that sum to P.
    s = sum(nums)
    if (s + target) % 2 != 0 or abs(target) > s:
        return 0

    subset_target = (s + target) // 2
    dp = [0] * (subset_target + 1)
    dp[0] = 1

    for num in nums:
        for i in range(subset_target, num - 1, -1):
            dp[i] += dp[i - num]

    return dp[subset_target]
```

### Detailed Explanation
1. **Mathematical Reduction**: The problem is equivalent to finding a subset of numbers that sum to a specific value $(sum + target) // 2$.
2. **0/1 Knapsack Variation**: We use a 1D DP array to count the number of ways to form each sum, processing elements one by one.

---

## 6. Coin Change 2 (Count Combinations)

### Problem Statement
You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money. Return the number of combinations that make up that amount. You have an infinite number of each kind of coin.

### Optimal Python Solution (DP)
```python
def change(amount: int, coins: list[int]) -> int:
    # Standard Unbounded Knapsack problem for combinations
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]
```

### Detailed Explanation
To avoid counting permutations (like `1+2` and `2+1`) and only count combinations, we process one coin at a time. This ensures that a smaller coin is always added before a larger coin in any sequence, effectively fixing the order.
