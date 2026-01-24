# Practice Problems - Binary Search Overview

## 1. Binary Search (LeetCode 704)

### Problem Statement
Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.

### Python Block
```python
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## 2. Sqrt(x) (LeetCode 69)

### Problem Statement
Given a non-negative integer `x`, compute and return the square root of `x`.

### Python Block
```python
def my_sqrt(x: int) -> int:
    if x < 2: return x
    left, right = 2, x // 2
    while left <= right:
        mid = left + (right - left) // 2
        num = mid * mid
        if num == x: return mid
        elif num < x: left = mid + 1
        else: right = mid - 1
    return right
```

## 3. First Bad Version (LeetCode 278)

### Problem Statement
Find the first bad version in `n` versions given `isBadVersion(version)` API.

### Python Block
```python
def first_bad_version(n: int) -> int:
    left, right = 1, n
    while left < right:
        mid = left + (right - left) // 2
        if is_bad_version(mid):
            right = mid
        else:
            left = mid + 1
    return left

def is_bad_version(version: int) -> bool:
    pass
```

## 4. Guess Number Higher or Lower (LeetCode 374)

### Problem Statement
Guess the number picked by the game.

### Python Block
```python
def guess_number(n: int) -> int:
    left, right = 1, n
    while left <= right:
        mid = left + (right - left) // 2
        res = guess(mid)
        if res == 0: return mid
        elif res == -1: right = mid - 1
        else: left = mid + 1
    return -1

def guess(num: int) -> int:
    pass
```

## 5. Search Insert Position (LeetCode 35)

### Problem Statement
Return the index if the target is found, or the index where it would be if it were inserted in order.

### Python Block
```python
def search_insert(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target: return mid
        elif nums[mid] < target: left = mid + 1
        else: right = mid - 1
    return left
```

## 6. Valid Perfect Square (LeetCode 367)

### Problem Statement
Return `true` if `num` is a perfect square.

### Python Block
```python
def is_perfect_square(num: int) -> bool:
    if num < 2: return True
    left, right = 2, num // 2
    while left <= right:
        mid = left + (right - left) // 2
        guess = mid * mid
        if guess == num: return True
        elif guess < num: left = mid + 1
        else: right = mid - 1
    return False
```

## 7. Count Negative Numbers in Sorted Matrix (LeetCode 1351)

### Problem Statement
Return the number of negative numbers in a row/col sorted matrix.

### Python Block
```python
def count_negatives(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    count = 0
    row, col = 0, n - 1
    while row < m and col >= 0:
        if grid[row][col] < 0:
            count += (m - row)
            col -= 1
        else:
            row += 1
    return count
```
