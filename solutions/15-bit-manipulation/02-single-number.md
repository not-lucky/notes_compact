# Solutions: Single Number

## 1. Single Number

**Problem Statement:**
Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one. You must implement a solution with a linear runtime complexity and use only constant extra space.

**Constraints:**
- `1 <= nums.length <= 3 * 10^4`
- `-3 * 10^4 <= nums[i] <= 3 * 10^4`
- Each element in the array appears twice except for one element which appears only once.

**Example:**
- Input: `nums = [4,1,2,1,2]`
- Output: `4`

**Python Implementation:**
```python
def singleNumber(nums: list[int]) -> int:
    result = 0
    for num in nums:
        result ^= num
    return result
```

## 2. Single Number II

**Problem Statement:**
Given an integer array `nums` where every element appears three times except for one, which appears exactly once. Find the single element and return it. You must implement a solution with a linear runtime complexity and use only constant extra space.

**Constraints:**
- `1 <= nums.length <= 3 * 10^4`
- `-2^31 <= nums[i] <= 2^31 - 1`
- Each element in `nums` appears three times except for one element which appears only once.

**Example:**
- Input: `nums = [2,2,3,2]`
- Output: `3`

**Python Implementation:**
```python
def singleNumber2(nums: list[int]) -> int:
    ones = 0  # Bits seen once
    twos = 0  # Bits seen twice

    for num in nums:
        # ones: bits that have appeared 1 time (mod 3)
        # twos: bits that have appeared 2 times (mod 3)
        ones = (ones ^ num) & ~twos
        twos = (twos ^ num) & ~ones

    return ones
```

## 3. Single Number III

**Problem Statement:**
Given an integer array `nums`, in which exactly two elements appear only once and all the other elements appear exactly twice. Find the two elements that appear only once. You can return the answer in any order. You must write an algorithm that runs in linear runtime complexity and uses only constant extra space.

**Constraints:**
- `2 <= nums.length <= 3 * 10^4`
- `-2^31 <= nums[i] <= 2^31 - 1`
- Each integer in `nums` will appear twice, only two integers will appear once.

**Example:**
- Input: `nums = [1,2,1,3,2,5]`
- Output: `[3,5]`

**Python Implementation:**
```python
def singleNumber3(nums: list[int]) -> list[int]:
    # Step 1: XOR all to get a ^ b
    xor_all = 0
    for num in nums:
        xor_all ^= num

    # Step 2: Find rightmost set bit (where a and b differ)
    diff_bit = xor_all & (-xor_all)

    # Step 3: Partition and XOR each group
    a, b = 0, 0
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num

    return [a, b]
```

## 4. Find the Duplicate Number

**Problem Statement:**
Given an array of integers `nums` containing `n + 1` integers where each integer is in the range `[1, n]` inclusive. There is only one repeated number in `nums`, return this repeated number. You must solve the problem without modifying the array `nums` and uses only constant extra space.

**Constraints:**
- `1 <= n <= 10^5`
- `nums.length == n + 1`
- `1 <= nums[i] <= n`
- All the integers in `nums` appear only once except for precisely one integer which appears two or more times.

**Example:**
- Input: `nums = [1,3,4,2,2]`
- Output: `2`

**Python Implementation:**
```python
def findDuplicate(nums: list[int]) -> int:
    # Phase 1: Find intersection point in cycle
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: Find entrance to cycle (duplicate)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow
```

## 5. Missing Number

**Problem Statement:**
Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.

**Constraints:**
- `n == nums.length`
- `1 <= n <= 10^4`
- `0 <= nums[i] <= n`
- All the numbers of `nums` are unique.

**Example:**
- Input: `nums = [3,0,1]`
- Output: `2`

**Python Implementation:**
```python
def missingNumber(nums: list[int]) -> int:
    n = len(nums)
    result = n
    for i in range(n):
        result ^= i ^ nums[i]
    return result
```
