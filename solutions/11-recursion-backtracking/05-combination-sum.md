# Solution: Combination Sum Practice Problems

## Problem 1: Combination Sum
### Problem Statement
Given an array of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of `candidates` where the chosen numbers sum to `target`. You may return the combinations in any order.

The same number may be chosen from `candidates` an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

### Constraints
- `1 <= candidates.length <= 30`
- `2 <= candidates[i] <= 40`
- All elements of `candidates` are distinct.
- `1 <= target <= 40`

### Example
Input: `candidates = [2,3,6,7], target = 7`
Output: `[[2,2,3],[7]]`

### Python Implementation
```python
def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
    """
    Time Complexity: O(n^(T/M)) where T=target, M=min_candidate
    Space Complexity: O(T/M)
    """
    res = []
    candidates.sort() # Sorting helps with pruning

    def backtrack(start, current_sum, path):
        if current_sum == target:
            res.append(path[:])
            return

        for i in range(start, len(candidates)):
            if current_sum + candidates[i] > target:
                break # Pruning

            path.append(candidates[i])
            # Reuse candidates[i] by passing i as start
            backtrack(i, current_sum + candidates[i], path)
            path.pop()

    backtrack(0, 0, [])
    return res
```

---

## Problem 2: Combination Sum II
### Problem Statement
Given a collection of candidate numbers (`candidates`) and a target number (`target`), find all unique combinations in `candidates` where the candidate numbers sum to `target`.
Each number in `candidates` may only be used once in the combination.

### Constraints
- `1 <= candidates.length <= 100`
- `1 <= candidates[i] <= 50`
- `1 <= target <= 30`

### Example
Input: `candidates = [10,1,2,7,6,1,5], target = 8`
Output: `[[1,1,6],[1,2,5],[1,7],[2,6]]`

### Python Implementation
```python
def combinationSum2(candidates: list[int], target: int) -> list[list[int]]:
    """
    Time Complexity: O(2^n)
    Space Complexity: O(n)
    """
    res = []
    candidates.sort()

    def backtrack(start, current_sum, path):
        if current_sum == target:
            res.append(path[:])
            return

        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i-1]:
                continue # Skip duplicates at same level

            if current_sum + candidates[i] > target:
                break # Pruning

            path.append(candidates[i])
            backtrack(i + 1, current_sum + candidates[i], path)
            path.pop()

    backtrack(0, 0, [])
    return res
```

---

## Problem 3: Combination Sum III
### Problem Statement
Find all valid combinations of `k` numbers that sum up to `n` such that only numbers `1` through `9` are used and each number is used at most once.

### Constraints
- `2 <= k <= 9`
- `1 <= n <= 60`

### Example
Input: `k = 3, n = 7`
Output: `[[1,2,4]]`

### Python Implementation
```python
def combinationSum3(k: int, n: int) -> list[list[int]]:
    """
    Time Complexity: O(C(9, k))
    Space Complexity: O(k)
    """
    res = []

    def backtrack(start, current_sum, path):
        if len(path) == k:
            if current_sum == n:
                res.append(path[:])
            return

        for i in range(start, 10):
            if current_sum + i > n:
                break
            path.append(i)
            backtrack(i + 1, current_sum + i, path)
            path.pop()

    backtrack(1, 0, [])
    return res
```

---

## Problem 4: Combination Sum IV
### Problem Statement
Given an array of distinct integers `nums` and a target integer `target`, return the number of possible combinations that add up to `target`.
Note that different sequences are counted as different combinations.

### Constraints
- `1 <= nums.length <= 200`
- `1 <= nums[i] <= 1000`
- All the elements of `nums` are unique.
- `1 <= target <= 1000`

### Example
Input: `nums = [1,2,3], target = 4`
Output: `7`
Explanation: (1, 1, 1, 1), (1, 1, 2), (1, 2, 1), (1, 3), (2, 1, 1), (2, 2), (3, 1)

### Python Implementation
```python
def combinationSum4(nums: list[int], target: int) -> int:
    """
    This is actually a Dynamic Programming problem.
    Time Complexity: O(target * n)
    Space Complexity: O(target)
    """
    dp = [0] * (target + 1)
    dp[0] = 1 # One way to make 0: empty set

    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                dp[i] += dp[i - num]

    return dp[target]
```
