# Single Number Solutions

## 1. Single Number

**Problem Statement**: Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one. You must implement a solution with a linear runtime complexity and use only constant extra space.

### Examples & Edge Cases

- **Example 1**: `nums = [2, 2, 1]` → `1`
- **Example 2**: `nums = [4, 1, 2, 1, 2]` → `4`
- **Edge Cases**:
  - Single element array: `[1]` → `1`.
  - Negative numbers: `[-1, -1, -2]` → `-2`.

### Optimal Python Solution

```python
def singleNumber(nums: list[int]) -> int:
    """
    Finds the element that appears once using the XOR property.
    Property: a ^ a = 0 and a ^ 0 = a
    """
    result = 0
    for num in nums:
        # XORing all numbers cancels out duplicates
        result ^= num
    return result
```

### Explanation

We leverage the property of the XOR bitwise operator. XOR of a number with itself is 0 (`a ^ a = 0`), and XOR of a number with 0 is the number itself (`a ^ 0 = a`). Since all numbers except one appear twice, if we XOR all elements in the array, the pairs will cancel each other out (become 0), leaving only the single number.

### Complexity Analysis

- **Time Complexity**: O(N) where N is the number of elements in the array. We traverse the array once.
- **Space Complexity**: O(1) as we only use one variable to store the XOR sum.

---

## 2. Single Number II

**Problem Statement**: Given an integer array `nums` where every element appears three times except for one, which appears exactly once. Find the single element and return it. You must implement a solution with a linear runtime complexity and use only constant extra space.

### Examples & Edge Cases

- **Example 1**: `nums = [2, 2, 3, 2]` → `3`
- **Example 2**: `nums = [0, 1, 0, 1, 0, 1, 99]` → `99`
- **Edge Cases**:
  - Negative numbers: Need to handle Python's 32-bit integer simulation.

### Optimal Python Solution

```python
def singleNumber(nums: list[int]) -> int:
    """
    Finds the element that appears once when others appear three times.
    Logic: Track bits seen once and bits seen twice using bitmasks.
    """
    ones = 0  # Bits that appeared once
    twos = 0  # Bits that appeared twice

    for num in nums:
        # Add to 'ones' if not already in 'twos'
        ones = (ones ^ num) & ~twos
        # Add to 'twos' if it was in 'ones'
        twos = (twos ^ num) & ~ones

    return ones
```

### Explanation

We use two bitmasks, `ones` and `twos`. `ones` keeps track of bits that have appeared an odd number of times (conceptually mod 3). `twos` keeps track of bits that have appeared twice. When a bit appears for the third time, it is removed from both `ones` and `twos`. Specifically, `ones = (ones ^ num) & ~twos` ensures a bit is set in `ones` only if it's not already in `twos`. The same logic applies to `twos`.

Note: This state machine approach works correctly for negative numbers in Python without explicit 32-bit masking because it handles the bits consistently. If using a bit-counting approach (looping 32 times), explicit masking with `0xFFFFFFFF` and sign reconstruction would be required.

### Complexity Analysis

- **Time Complexity**: O(N) where N is the length of `nums`.
- **Space Complexity**: O(1) as we use only two variables.

---

## 3. Single Number III

**Problem Statement**: Given an integer array `nums`, in which exactly two elements appear only once and all the other elements appear exactly twice. Find the two elements that appear only once. You can return the answer in any order. Must run in O(n) time and O(1) space.

### Examples & Edge Cases

- **Example**: `nums = [1, 2, 1, 3, 2, 5]` → `[3, 5]`
- **Edge Cases**:
  - Smallest possible array: `[a, b]`.

### Optimal Python Solution

```python
def singleNumber(nums: list[int]) -> list[int]:
    """
    Finds two unique numbers in an array where others appear twice.
    """
    # 1. XOR all numbers to get x ^ y
    xor_all = 0
    for num in nums:
        xor_all ^= num

    # 2. Find a bit where x and y differ (rightmost set bit)
    diff_bit = xor_all & -xor_all

    # 3. Partition numbers into two groups based on this bit
    a, b = 0, 0
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num

    return [a, b]
```

### Explanation

First, we XOR all numbers, which gives us `x ^ y` (where `x` and `y` are the two unique numbers). Since `x != y`, at least one bit in `x ^ y` must be 1. We isolate the rightmost set bit using `xor_all & -xor_all`. We then partition all numbers into two groups: those that have this bit set and those that don't. Each group will contain one of the unique numbers and some pairs of other numbers. XORing each group separately cancels the pairs, leaving the two unique numbers.

### Complexity Analysis

- **Time Complexity**: O(N) as we make two passes over the array.
- **Space Complexity**: O(1) as we use only a few variables.

---

## 4. Find the Duplicate Number

**Problem Statement**: Given an array of integers `nums` containing `n + 1` integers where each integer is in the range `[1, n]` inclusive. There is only one repeated number in `nums`, return this repeated number. You must solve the problem without modifying the array `nums` and uses only constant extra space.

### Examples & Edge Cases

- **Example**: `nums = [1, 3, 4, 2, 2]` → `2`
- **Edge Cases**:
  - Duplicate appears more than twice: `[2, 2, 2, 2, 2]`.

### Optimal Python Solution

```python
def findDuplicate(nums: list[int]) -> int:
    """
    Finds duplicate using Floyd's Cycle-Finding Algorithm (Tortoise and Hare).
    The array is treated as a linked list where nums[i] points to index nums[i].
    """
    # Phase 1: Find the intersection point of the two runners
    slow = nums[0]
    fast = nums[0]

    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: Find the entrance to the cycle
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow
```

### Explanation

Although this is a bit manipulation chapter, this problem is often grouped here. The optimal O(1) space solution uses Floyd's Cycle-Finding Algorithm. We treat the array as a functional mapping where `index -> nums[index]`. Since there's a duplicate, multiple indices point to the same value, creating a "cycle" in the sequence. The entrance to the cycle is the duplicate number.

### Complexity Analysis

- **Time Complexity**: O(N).
- **Space Complexity**: O(1).

---

## 5. Missing Number

**Problem Statement**: Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.

### Examples & Edge Cases

- **Example 1**: `nums = [3, 0, 1]` → `2`
- **Example 2**: `nums = [0, 1]` → `2`
- **Edge Cases**:
  - Missing number is 0 or n.

### Optimal Python Solution

```python
def missingNumber(nums: list[int]) -> int:
    """
    Finds the missing number using XOR properties.
    XORing all numbers from 0 to n with all numbers in the array.
    """
    missing = len(nums)
    for i, num in enumerate(nums):
        # XOR index and value to cancel out everything but the missing one
        missing ^= i ^ num
    return missing
```

### Explanation

We use the XOR property `a ^ a = 0`. If we XOR all the indices from `0` to `n` and all the values in the array, every number that is present in the array will appear twice (once as an index and once as a value) and thus cancel out. The only number that appears only once is the missing number.

### Complexity Analysis

- **Time Complexity**: O(N) as we iterate through the array once.
- **Space Complexity**: O(1).
