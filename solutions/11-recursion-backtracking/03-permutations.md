# Solution: Permutations Practice Problems

## Problem 1: Permutations
### Problem Statement
Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in any order.

### Constraints
- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- All the integers of `nums` are unique.

### Example
Input: `nums = [1,2,3]`
Output: `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`

### Python Implementation
```python
def permute(nums: list[int]) -> list[list[int]]:
    """
    Time Complexity: O(n * n!)
    Space Complexity: O(n)
    """
    res = []

    def backtrack(current, unused):
        if not unused:
            res.append(current.copy())
            return

        for i in range(len(unused)):
            current.append(unused[i])
            backtrack(current, unused[:i] + unused[i+1:])
            current.pop()

    backtrack([], nums)
    return res
```

---

## Problem 2: Permutations II
### Problem Statement
Given a collection of numbers, `nums`, that might contain duplicates, return all possible unique permutations in any order.

### Constraints
- `1 <= nums.length <= 8`
- `-10 <= nums[i] <= 10`

### Example
Input: `nums = [1,1,2]`
Output: `[[1,1,2],[1,2,1],[2,1,1]]`

### Python Implementation
```python
def permuteUnique(nums: list[int]) -> list[list[int]]:
    """
    Time Complexity: O(n * n!)
    Space Complexity: O(n)
    """
    res = []
    perm = []
    count = {n: 0 for n in nums}
    for n in nums:
        count[n] += 1

    def backtrack():
        if len(perm) == len(nums):
            res.append(perm.copy())
            return

        for n in count:
            if count[n] > 0:
                perm.append(n)
                count[n] -= 1

                backtrack()

                count[n] += 1
                perm.pop()

    backtrack()
    return res
```

---

## Problem 3: Next Permutation
### Problem Statement
A permutation of an array of integers is an arrangement of its members into a sequence or linear order.
The next permutation of an array of integers is the next lexicographically greater permutation of its integer.
Given an array of integers `nums`, find the next permutation of `nums`.
The replacement must be in place and use only constant extra memory.

### Constraints
- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 100`

### Example
Input: `nums = [1,2,3]`
Output: `[1,3,2]`

### Python Implementation
```python
def nextPermutation(nums: list[int]) -> None:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    # 1. Find pivot (first decreasing from right)
    pivot = -1
    for i in range(len(nums) - 2, -1, -1):
        if nums[i] < nums[i + 1]:
            pivot = i
            break

    if pivot == -1:
        nums.reverse()
        return

    # 2. Find successor to pivot
    successor = -1
    for i in range(len(nums) - 1, pivot, -1):
        if nums[i] > nums[pivot]:
            successor = i
            break

    # 3. Swap pivot and successor
    nums[pivot], nums[successor] = nums[successor], nums[pivot]

    # 4. Reverse suffix
    nums[pivot + 1:] = reversed(nums[pivot + 1:])
```

---

## Problem 4: Permutation Sequence
### Problem Statement
The set `[1, 2, 3, ..., n]` contains a total of `n!` unique permutations.
By listing and labeling all of the permutations in order, we get the following sequence for `n = 3`:
1. "123"
2. "132"
3. "213"
4. "231"
5. "312"
6. "321"
Given `n` and `k`, return the `k`th permutation sequence.

### Constraints
- `1 <= n <= 9`
- `1 <= k <= n!`

### Example
Input: `n = 3, k = 3`
Output: `"213"`

### Python Implementation
```python
import math

def getPermutation(n: int, k: int) -> str:
    """
    Time Complexity: O(n^2)
    Space Complexity: O(n)
    """
    numbers = [str(i) for i in range(1, n + 1)]
    res = ""
    k -= 1 # 0-indexed

    while n > 0:
        n -= 1
        fact = math.factorial(n)
        index = k // fact
        res += numbers.pop(index)
        k %= fact

    return res
```
