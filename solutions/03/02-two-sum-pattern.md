# Two Sum Pattern

## Practice Problems

### 1. Two Sum
**Difficulty:** Easy
**Key Technique:** HashMap (Complement)

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find indices of two numbers that add up to target.

    Time: O(n)
    Space: O(n)
    """
    seen = {} # val -> index
    for i, n in enumerate(nums):
        diff = target - n
        if diff in seen:
            return [seen[diff], i]
        seen[n] = i
    return []
```

### 2. Two Sum II - Input Array Is Sorted
**Difficulty:** Medium
**Key Technique:** Two pointers

```python
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    """
    Find two numbers in sorted array that sum to target.
    Returns 1-indexed positions.

    Time: O(n)
    Space: O(1)
    """
    l, r = 0, len(numbers) - 1
    while l < r:
        curr = numbers[l] + numbers[r]
        if curr == target:
            return [l + 1, r + 1]
        if curr < target:
            l += 1
        else:
            r -= 1
    return []
```

### 3. 3Sum
**Difficulty:** Medium
**Key Technique:** Sort + Fix one + Two pointers

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    """
    Find all unique triplets that sum to zero.

    Time: O(n^2)
    Space: O(n) for sorting or O(1)
    """
    res = []
    nums.sort()
    for i in range(len(nums)-2):
        if i > 0 and nums[i] == nums[i-1]:
            continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l+1]:
                    l += 1
                while l < r and nums[r] == nums[r-1]:
                    r -= 1
                l += 1; r -= 1
    return res
```

### 4. 3Sum Closest
**Difficulty:** Medium
**Key Technique:** Sort + Fix one + Two pointers + track min diff

```python
def three_sum_closest(nums: list[int], target: int) -> int:
    """
    Find sum of three integers closest to target.

    Time: O(n^2)
    Space: O(n) or O(1)
    """
    nums.sort()
    res = nums[0] + nums[1] + nums[2]
    for i in range(len(nums)-2):
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if abs(s - target) < abs(res - target):
                res = s
            if s < target:
                l += 1
            elif s > target:
                r -= 1
            else:
                return target
    return res
```

### 5. 4Sum
**Difficulty:** Medium
**Key Technique:** Sort + Fix two + Two pointers

```python
def four_sum(nums: list[int], target: int) -> list[list[int]]:
    """
    Find all unique quadruplets that sum to target.

    Time: O(n^3)
    Space: O(n) or O(1)
    """
    nums.sort()
    res = []
    n = len(nums)
    for i in range(n-3):
        if i > 0 and nums[i] == nums[i-1]: continue
        for j in range(i+1, n-2):
            if j > i + 1 and nums[j] == nums[j-1]: continue
            l, r = j + 1, n - 1
            while l < r:
                s = nums[i] + nums[j] + nums[l] + nums[r]
                if s < target: l += 1
                elif s > target: r -= 1
                else:
                    res.append([nums[i], nums[j], nums[l], nums[r]])
                    while l < r and nums[l] == nums[l+1]: l += 1
                    while l < r and nums[r] == nums[r-1]: r -= 1
                    l += 1; r -= 1
    return res
```
