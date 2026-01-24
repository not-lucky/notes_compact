# Practice Problems - Binary Search Template

## 1. Binary Search (LeetCode 704)

### Problem Statement
Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.

### Constraints
- `1 <= nums.length <= 10^4`
- `-10^4 < nums[i], target < 10^4`
- All the integers in `nums` are unique.
- `nums` is sorted in ascending order.

### Example
**Input:** `nums = [-1,0,3,5,9,12], target = 9`
**Output:** `4`

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
Given a non-negative integer `x`, compute and return the square root of `x`. Since the return type is an integer, the decimal digits are truncated, and only the integer part of the result is returned.

### Constraints
- `0 <= x <= 2^31 - 1`

### Example
**Input:** `x = 8`
**Output:** `2` (The square root of 8 is 2.82842..., and since the decimal part is truncated, 2 is returned.)

### Python Block
```python
def my_sqrt(x: int) -> int:
    if x < 2:
        return x

    left, right = 2, x // 2

    while left <= right:
        mid = left + (right - left) // 2
        num = mid * mid
        if num == x:
            return mid
        elif num < x:
            left = mid + 1
        else:
            right = mid - 1

    return right
```

## 3. First Bad Version (LeetCode 278)

### Problem Statement
You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.

Suppose you have `n` versions `[1, 2, ..., n]` and you want to find out the first bad one, which causes all the following ones to be bad.

You are given an API `bool isBadVersion(version)` which returns whether `version` is bad. Implement a function to find the first bad version. You should minimize the number of calls to the API.

### Constraints
- `1 <= bad <= n <= 2^31 - 1`

### Example
**Input:** `n = 5, bad = 4`
**Output:** `4`

### Python Block
```python
# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

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
    # This is a placeholder for the actual API
    pass
```

## 4. Guess Number Higher or Lower (LeetCode 374)

### Problem Statement
We are playing the Guess Game. The game is as follows:
I pick a number from `1` to `n`. You have to guess which number I picked.
Every time you guess wrong, I will tell you whether the number I picked is higher or lower than your guess.

You call a pre-defined API `int guess(int num)`, which returns three possible results:
- `-1`: Your guess is higher than the number I picked (i.e. `num > pick`).
- `1`: Your guess is lower than the number I picked (i.e. `num < pick`).
- `0`: your guess is equal to the number I picked (i.e. `num == pick`).

Return the number that I picked.

### Constraints
- `1 <= n <= 2^31 - 1`
- `1 <= pick <= n`

### Example
**Input:** `n = 10, pick = 6`
**Output:** `6`

### Python Block
```python
# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num: int) -> int:

def guess_number(n: int) -> int:
    left, right = 1, n

    while left <= right:
        mid = left + (right - left) // 2
        res = guess(mid)
        if res == 0:
            return mid
        elif res == -1:
            right = mid - 1
        else:
            left = mid + 1

    return -1

def guess(num: int) -> int:
    # This is a placeholder for the actual API
    pass
```

## 5. Search Insert Position (LeetCode 35)

### Problem Statement
Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

You must write an algorithm with `O(log n)` runtime complexity.

### Constraints
- `1 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` contains distinct values sorted in ascending order.
- `-10^4 <= target <= 10^4`

### Example
**Input:** `nums = [1,3,5,6], target = 5`
**Output:** `2`

### Python Block
```python
def search_insert(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return left
```

## 6. Valid Perfect Square (LeetCode 367)

### Problem Statement
Given a positive integer `num`, return `true` if `num` is a perfect square or `false` otherwise.
A perfect square is an integer that is the square of an integer. In other words, it is the product of some integer with itself.

You must not use any built-in library function, such as `sqrt`.

### Constraints
- `1 <= num <= 2^31 - 1`

### Example
**Input:** `num = 16`
**Output:** `true`

### Python Block
```python
def is_perfect_square(num: int) -> bool:
    if num < 2:
        return True

    left, right = 2, num // 2

    while left <= right:
        mid = left + (right - left) // 2
        guess = mid * mid
        if guess == num:
            return True
        elif guess < num:
            left = mid + 1
        else:
            right = mid - 1

    return False
```

## 7. Count Negative Numbers in Sorted Matrix (LeetCode 1351)

### Problem Statement
Given a `m x n` matrix `grid` which is sorted in non-increasing order both row-wise and column-wise, return the number of negative numbers in `grid`.

### Constraints
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 100`
- `-100 <= grid[i][j] <= 100`

### Example
**Input:** `grid = [[4,3,2,-1],[3,2,1,-1],[1,1,-1,-2],[-1,-1,-2,-3]]`
**Output:** `8`

### Python Block
```python
def count_negatives(grid: list[list[int]]) -> int:
    count = 0
    m, n = len(grid), len(grid[0])
    row, col = 0, n - 1

    while row < m and col >= 0:
        if grid[row][col] < 0:
            count += (m - row)
            col -= 1
        else:
            row += 1

    return count
```
