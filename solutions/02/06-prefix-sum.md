# Prefix Sum

## Practice Problems

### 1. Range Sum Query - Immutable
**Difficulty:** Easy
**Key Technique:** Basic prefix sum

```python
class NumArray:
    def __init__(self, nums: list[int]):
        self.prefix = [0] * (len(nums) + 1)
        for i in range(len(nums)):
            self.prefix[i + 1] = self.prefix[i] + nums[i]

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]
```

### 2. Range Sum Query 2D - Immutable
**Difficulty:** Medium
**Key Technique:** 2D prefix sum

```python
class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        if not matrix or not matrix[0]: return
        R, C = len(matrix), len(matrix[0])
        self.prefix = [[0] * (C + 1) for _ in range(R + 1)]
        for r in range(R):
            for c in range(C):
                self.prefix[r+1][c+1] = matrix[r][c] + self.prefix[r][c+1] + \
                                       self.prefix[r+1][c] - self.prefix[r][c]

    def sumRegion(self, r1: int, c1: int, r2: int, c2: int) -> int:
        return self.prefix[r2+1][c2+1] - self.prefix[r1][c2+1] - \
               self.prefix[r2+1][c1] + self.prefix[r1][c1]
```

### 3. Subarray Sum Equals K
**Difficulty:** Medium
**Key Technique:** Prefix + hashmap

```python
def subarray_sum(nums: list[int], k: int) -> int:
    counts = {0: 1}
    curr_sum = 0
    res = 0
    for num in nums:
        curr_sum += num
        if curr_sum - k in counts:
            res += counts[curr_sum - k]
        counts[curr_sum] = counts.get(curr_sum, 0) + 1
    return res
```

### 4. Subarray Sums Divisible by K
**Difficulty:** Medium
**Key Technique:** Mod prefix sum

```python
def subarrays_div_by_k(nums: list[int], k: int) -> int:
    counts = {0: 1}
    curr_sum = 0
    res = 0
    for num in nums:
        curr_sum += num
        mod = curr_sum % k
        if mod in counts:
            res += counts[mod]
        counts[mod] = counts.get(mod, 0) + 1
    return res
```

### 5. Product of Array Except Self
**Difficulty:** Medium
**Key Technique:** Prefix + suffix

```python
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [1] * n
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
    return res
```

### 6. Find Pivot Index
**Difficulty:** Easy
**Key Technique:** Left = right sum

```python
def pivot_index(nums: list[int]) -> int:
    total = sum(nums)
    left_sum = 0
    for i, num in enumerate(nums):
        if left_sum == total - left_sum - num:
            return i
        left_sum += num
    return -1
```

### 7. Continuous Subarray Sum
**Difficulty:** Medium
**Key Technique:** Mod prefix sum

```python
def check_subarray_sum(nums: list[int], k: int) -> bool:
    seen = {0: -1}
    curr_sum = 0
    for i, num in enumerate(nums):
        curr_sum += num
        mod = curr_sum % k
        if mod in seen:
            if i - seen[mod] > 1: return True
        else:
            seen[mod] = i
    return False
```

### 8. Maximum Size Subarray Sum Equals K
**Difficulty:** Medium
**Key Technique:** Prefix + hashmap

```python
def max_subarray_len(nums: list[int], k: int) -> int:
    seen = {0: -1}
    curr_sum = 0
    res = 0
    for i, num in enumerate(nums):
        curr_sum += num
        if curr_sum - k in seen:
            res = max(res, i - seen[curr_sum - k])
        if curr_sum not in seen:
            seen[curr_sum] = i
    return res
```
