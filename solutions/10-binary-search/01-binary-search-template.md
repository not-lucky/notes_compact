# Binary Search Template Solutions

## 1. Binary Search
[LeetCode 704](https://leetcode.com/problems/binary-search/)

### Problem Description
Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.

### Solution
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
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 2. Sqrt(x)
[LeetCode 69](https://leetcode.com/problems/sqrtx/)

### Problem Description
Given a non-negative integer `x`, return the square root of `x` rounded down to the nearest integer. The returned integer should be non-negative as well.

### Solution
```python
def mySqrt(x: int) -> int:
    if x < 2:
        return x

    left, right = 1, x // 2
    res = 1

    while left <= right:
        mid = left + (right - left) // 2
        if mid * mid <= x:
            res = mid
            left = mid + 1
        else:
            right = mid - 1

    return res
```
- **Time Complexity**: O(log x)
- **Space Complexity**: O(1)

---

## 3. First Bad Version
[LeetCode 278](https://leetcode.com/problems/first-bad-version/)

### Problem Description
You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.

### Solution
```python
# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

def firstBadVersion(n: int) -> int:
    left, right = 1, n

    while left < right:
        mid = left + (right - left) // 2
        if isBadVersion(mid):
            right = mid
        else:
            left = mid + 1

    return left
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 4. Guess Number Higher or Lower
[LeetCode 374](https://leetcode.com/problems/guess-number-higher-or-lower/)

### Problem Description
We are playing the Guess Game. The game is as follows:
I pick a number from 1 to n. You have to guess which number I picked.
Every time you guess wrong, I will tell you whether the number I picked is higher or lower than your guess.

### Solution
```python
# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num: int) -> int:

def guessNumber(n: int) -> int:
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
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 5. Search Insert Position
[LeetCode 35](https://leetcode.com/problems/search-insert-position/)

### Problem Description
Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

### Solution
```python
def searchInsert(nums: list[int], target: int) -> int:
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
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 6. Valid Perfect Square
[LeetCode 367](https://leetcode.com/problems/valid-perfect-square/)

### Problem Description
Given a positive integer `num`, return `true` if `num` is a perfect square or `false` otherwise.

### Solution
```python
def isPerfectSquare(num: int) -> bool:
    if num < 2:
        return True

    left, right = 2, num // 2

    while left <= right:
        mid = left + (right - left) // 2
        guess_sq = mid * mid
        if guess_sq == num:
            return True
        elif guess_sq < num:
            left = mid + 1
        else:
            right = mid - 1

    return False
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 7. Count Negative Numbers in Sorted Matrix
[LeetCode 1351](https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/)

### Problem Description
Given a `m x n` matrix `grid` which is sorted in non-increasing order both row-wise and column-wise, return the number of negative numbers in `grid`.

### Solution
```python
def countNegatives(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    count = 0
    row, col = 0, n - 1

    while row < m and col >= 0:
        if grid[row][col] < 0:
            # If current element is negative, all elements below it in the same column are also negative
            count += (m - row)
            col -= 1
        else:
            row += 1

    return count
```
- **Time Complexity**: O(m + n)
- **Space Complexity**: O(1)

---

## 8. Find Smallest Letter Greater Than Target
[LeetCode 744](https://leetcode.com/problems/find-smallest-letter-greater-than-target/)

### Problem Description
You are given an array of characters `letters` that is sorted in non-decreasing order, and a character `target`. There are at least two different characters in `letters`. Return the smallest character in `letters` that is lexicographically greater than `target`. If such a character does not exist, return the first character in `letters`.

### Solution
```python
def nextGreatestLetter(letters: list[str], target: str) -> str:
    left, right = 0, len(letters) - 1

    if target >= letters[-1]:
        return letters[0]

    while left < right:
        mid = left + (right - left) // 2
        if letters[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return letters[left]
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 9. Arranging Coins
[LeetCode 441](https://leetcode.com/problems/arranging-coins/)

### Problem Description
You have `n` coins and you want to build a staircase with these coins. The staircase consists of `k` rows where the `i`-th row has exactly `i` coins. The last row of the staircase may be incomplete. Given the integer `n`, return the number of complete rows of the staircase you will build.

### Solution
```python
def arrangeCoins(n: int) -> int:
    left, right = 0, n
    while left <= right:
        k = left + (right - left) // 2
        curr = k * (k + 1) // 2
        if curr == n:
            return k
        if n < curr:
            right = k - 1
        else:
            left = k + 1
    return right
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 10. Fair Candy Swap
[LeetCode 888](https://leetcode.com/problems/fair-candy-swap/)

### Problem Description
Alice and Bob have a different total number of candies. You are given two integer arrays `aliceSizes` and `bobSizes` where `aliceSizes[i]` is the number of candies of the `i`-th box of candy that Alice has and `bobSizes[j]` is the number of candies of the `j`-th box of candy that Bob has. Since they are friends, they would like to exchange one candy box each so that after the exchange, they both have the same total amount of candy. Return an integer array `ans` where `ans[0]` is the number of candies in the box that Alice must exchange, and `ans[1]` is the number of candies in the box that Bob must exchange.

### Solution
```python
import bisect

def fairCandySwap(aliceSizes: list[int], bobSizes: list[int]) -> list[int]:
    sumA, sumB = sum(aliceSizes), sum(bobSizes)
    delta = (sumB - sumA) // 2
    bobSizes.sort()
    for x in aliceSizes:
        # We need y such that sumB - y + x = sumA - x + y
        # sumB - sumA + 2x = 2y
        # y = x + (sumB - sumA) / 2
        target = x + delta
        idx = bisect.bisect_left(bobSizes, target)
        if idx < len(bobSizes) and bobSizes[idx] == target:
            return [x, target]
    return []
```
- **Time Complexity**: O(n log n + m log n) where n is len(bobSizes) and m is len(aliceSizes).
- **Space Complexity**: O(1) or O(n) depending on sort implementation.
