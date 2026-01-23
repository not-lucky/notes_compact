# Two Pointers: Opposite Direction

## Practice Problems

### 1. Two Sum II (Sorted)
**Difficulty:** Medium
**Pattern:** Basic opposite

```python
def two_sum_ii(numbers: list[int], target: int) -> list[int]:
    """
    Finds two numbers that sum to target in a sorted array.
    Time: O(n)
    Space: O(1)
    """
    l, r = 0, len(numbers) - 1
    while l < r:
        curr = numbers[l] + numbers[r]
        if curr == target:
            return [l + 1, r + 1]
        elif curr < target:
            l += 1
        else:
            r -= 1
    return []
```

### 2. 3Sum
**Difficulty:** Medium
**Pattern:** Fix one + two pointers

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    """
    Finds all unique triplets that sum to zero.
    Time: O(n^2)
    Space: O(1) or O(n) for sorting
    """
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]: continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0: l += 1
            elif s > 0: r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l+1]: l += 1
                while l < r and nums[r] == nums[r-1]: r -= 1
                l += 1; r -= 1
    return res
```

### 3. 3Sum Closest
**Difficulty:** Medium
**Pattern:** Track closest

```python
def three_sum_closest(nums: list[int], target: int) -> int:
    """
    Finds triplet sum closest to target.
    Time: O(n^2)
    Space: O(1)
    """
    nums.sort()
    closest = float('inf')
    for i in range(len(nums) - 2):
        l, r = i + 1, len(nums) - 1
        while l < r:
            curr = nums[i] + nums[l] + nums[r]
            if abs(target - curr) < abs(target - closest):
                closest = curr
            if curr < target: l += 1
            elif curr > target: r -= 1
            else: return target
    return closest
```

### 4. Container With Most Water
**Difficulty:** Medium
**Pattern:** Max area

```python
def max_area(height: list[int]) -> int:
    """
    Finds maximum area of water a container can hold.
    Time: O(n)
    Space: O(1)
    """
    l, r = 0, len(height) - 1
    res = 0
    while l < r:
        res = max(res, min(height[l], height[r]) * (r - l))
        if height[l] < height[r]: l += 1
        else: r -= 1
    return res
```

### 5. Trapping Rain Water
**Difficulty:** Hard
**Pattern:** Left/right max

```python
def trap(height: list[int]) -> int:
    """
    Calculates total trapped water.
    Time: O(n)
    Space: O(1)
    """
    if not height: return 0
    l, r = 0, len(height) - 1
    l_max, r_max = height[l], height[r]
    res = 0
    while l < r:
        if l_max < r_max:
            l += 1
            l_max = max(l_max, height[l])
            res += l_max - height[l]
        else:
            r -= 1
            r_max = max(r_max, height[r])
            res += r_max - height[r]
    return res
```

### 6. Valid Palindrome
**Difficulty:** Easy
**Pattern:** Skip non-alphanum

```python
def is_palindrome(s: str) -> bool:
    """
    Checks if string is a palindrome.
    Time: O(n)
    Space: O(1)
    """
    l, r = 0, len(s) - 1
    while l < r:
        if not s[l].isalnum(): l += 1
        elif not s[r].isalnum(): r -= 1
        else:
            if s[l].lower() != s[r].lower(): return False
            l += 1; r -= 1
    return True
```

### 7. Sort Colors
**Difficulty:** Medium
**Pattern:** Dutch flag

```python
def sort_colors(nums: list[int]) -> None:
    """
    Sorts 0s, 1s, and 2s in-place.
    Time: O(n)
    Space: O(1)
    """
    l, m, h = 0, 0, len(nums) - 1
    while m <= h:
        if nums[m] == 0:
            nums[l], nums[m] = nums[m], nums[l]
            l += 1; m += 1
        elif nums[m] == 1:
            m += 1
        else:
            nums[m], nums[h] = nums[h], nums[m]
            h -= 1
```

### 8. 4Sum
**Difficulty:** Medium
**Pattern:** Two layers + two pointers

```python
def four_sum(nums: list[int], target: int) -> list[list[int]]:
    """
    Finds all unique quadruplets that sum to target.
    Time: O(n^3)
    Space: O(1)
    """
    nums.sort()
    res = []
    n = len(nums)
    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i-1]: continue
        for j in range(i + 1, n - 2):
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
