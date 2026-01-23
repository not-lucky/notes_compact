# Kadane's Algorithm

## Practice Problems

### 1. Maximum Subarray
**Difficulty:** Medium
**Key Variation:** Basic Kadane

```python
def max_subarray(nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    curr = res = nums[0]
    for i in range(1, len(nums)):
        curr = max(nums[i], curr + nums[i])
        res = max(res, curr)
    return res
```

### 2. Maximum Product Subarray
**Difficulty:** Medium
**Key Variation:** Track min/max

```python
def max_product(nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    res = max_p = min_p = nums[0]
    for i in range(1, len(nums)):
        num = nums[i]
        if num < 0:
            max_p, min_p = min_p, max_p
        max_p = max(num, max_p * num)
        min_p = min(num, min_p * num)
        res = max(res, max_p)
    return res
```

### 3. Maximum Sum Circular Subarray
**Difficulty:** Medium
**Key Variation:** Total - min

```python
def max_subarray_sum_circular(nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    total = sum(nums)

    # Max subarray
    curr_max = res_max = nums[0]
    for i in range(1, len(nums)):
        curr_max = max(nums[i], curr_max + nums[i])
        res_max = max(res_max, curr_max)

    # Min subarray
    curr_min = res_min = nums[0]
    for i in range(1, len(nums)):
        curr_min = min(nums[i], curr_min + nums[i])
        res_min = min(res_min, curr_min)

    if res_max < 0: return res_max
    return max(res_max, total - res_min)
```

### 4. House Robber
**Difficulty:** Medium
**Key Variation:** No adjacent

```python
def rob(nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    prev2, prev1 = 0, 0
    for num in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + num)
    return prev1
```

### 5. House Robber II
**Difficulty:** Medium
**Key Variation:** Circular + no adjacent

```python
def rob_circular(nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    if len(nums) == 1: return nums[0]

    def helper(arr):
        p2, p1 = 0, 0
        for n in arr:
            p2, p1 = p1, max(p1, p2 + n)
        return p1

    return max(helper(nums[1:]), helper(nums[:-1]))
```

### 6. Best Time to Buy and Sell Stock
**Difficulty:** Easy
**Key Variation:** Kadane variation

```python
def max_profit(prices: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    min_price = float('inf')
    res = 0
    for p in prices:
        min_price = min(min_price, p)
        res = max(res, p - min_price)
    return res
```

### 7. Maximum Sum Rectangle (2D)
**Difficulty:** Hard
**Key Variation:** 2D compression

```python
def max_sum_rectangle(matrix: list[list[int]]) -> int:
    R, C = len(matrix), len(matrix[0])
    res = float('-inf')
    for left in range(C):
        temp = [0] * R
        for right in range(left, C):
            for r in range(R):
                temp[r] += matrix[r][right]

            # 1D Kadane
            curr = 0
            curr_max = float('-inf')
            for n in temp:
                curr = max(n, curr + n)
                curr_max = max(curr_max, curr)
            res = max(res, curr_max)
    return res
```

### 8. Maximum Subarray Sum with One Deletion
**Difficulty:** Medium
**Key Variation:** Track with/without deletion

```python
def maximum_sum(arr: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    n = len(arr)
    # no_del: max sum ending at i with no deletions
    # one_del: max sum ending at i with exactly one deletion
    no_del = one_del = res = arr[0]
    for i in range(1, n):
        num = arr[i]
        # one_del either keeps previous deletion and adds num,
        # or starts a deletion at i (takes previous no_del)
        one_del = max(one_del + num, no_del)
        no_del = max(no_del + num, num)
        res = max(res, no_del, one_del)
    return res
```
