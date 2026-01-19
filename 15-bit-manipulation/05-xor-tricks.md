# XOR Tricks

> **Prerequisites:** [Binary Basics](./01-binary-basics.md), [Single Number](./02-single-number.md)

## Interview Context

XOR is the most versatile bitwise operator for interviews. Its unique properties enable elegant solutions to seemingly complex problems. Mastering XOR tricks demonstrates deep understanding of bit manipulation.

---

## XOR Properties Cheat Sheet

```
Essential Properties:
1. a ^ a = 0         (self-cancellation)
2. a ^ 0 = a         (identity)
3. a ^ b = b ^ a     (commutative)
4. (a^b)^c = a^(b^c) (associative)
5. a ^ b ^ a = b     (pair cancellation)
6. a ^ b = c → a = b ^ c (reversibility)

Bit-level: XOR outputs 1 when bits differ

  0 ^ 0 = 0
  0 ^ 1 = 1
  1 ^ 0 = 1
  1 ^ 1 = 0
```

---

## Problem: Missing Number

**LeetCode 268**: Given an array nums containing n distinct numbers in the range [0, n], return the only number in the range that is missing.

### Example

```
Input: nums = [3, 0, 1]
Output: 2

Range [0, 3] → missing 2

Input: nums = [9, 6, 4, 2, 3, 5, 7, 0, 1]
Output: 8
```

### Solution

```python
def missingNumber(nums: list[int]) -> int:
    """
    Find missing number using XOR.

    Key insight: XOR array elements with indices 0 to n.
    Everything pairs up and cancels except the missing number.

    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    result = n  # Start with n (which is not an index)

    for i in range(n):
        result ^= i ^ nums[i]

    return result


# Alternative: Sum formula
def missingNumber_sum(nums: list[int]) -> int:
    """Use arithmetic sum formula."""
    n = len(nums)
    expected = n * (n + 1) // 2
    actual = sum(nums)
    return expected - actual


# Test
print(missingNumber([3, 0, 1]))  # 2
print(missingNumber([0, 1]))    # 2
```

### Why XOR Works

```
nums = [3, 0, 1], n = 3, range = [0, 1, 2, 3]

XOR indices: 0 ^ 1 ^ 2 ^ 3 = (0^0) ^ (1) ^ (2) ^ (3)
XOR nums:    3 ^ 0 ^ 1

Combined:
  (0 ^ 1 ^ 2 ^ 3) ^ (3 ^ 0 ^ 1)
= 0 ^ (1 ^ 1) ^ 2 ^ (3 ^ 3) ^ (0 ^ 0)
= 0 ^ 0 ^ 2 ^ 0 ^ 0
= 2

Everything cancels except 2!
```

---

## Problem: Find the Duplicate Number

**LeetCode 287**: Given an array of n+1 integers where each integer is in [1, n], find the duplicate. Must use O(1) space and not modify the array.

### Solution (Floyd's Cycle Detection)

```python
def findDuplicate(nums: list[int]) -> int:
    """
    Find duplicate using Floyd's cycle detection.

    Note: This isn't pure bit manipulation, but often
    asked alongside bit problems. XOR doesn't work here
    because we don't know how many times duplicate appears.

    Time: O(n)
    Space: O(1)
    """
    # Phase 1: Find intersection point
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

---

## Problem: Find Two Missing Numbers

Given an array of n-2 distinct numbers from range [1, n], find the two missing numbers.

### Example

```
Input: [1, 3, 5, 6], n = 6
Output: [2, 4]

Range: [1, 2, 3, 4, 5, 6]
Missing: 2 and 4
```

### Solution

```python
def findTwoMissing(nums: list[int], n: int) -> list[int]:
    """
    Find two missing numbers from [1, n].

    Similar approach to Single Number III:
    1. XOR all to get a ^ b (the two missing XORed)
    2. Find bit where they differ
    3. Partition and XOR each group

    Time: O(n)
    Space: O(1)
    """
    # XOR all numbers 1 to n with array elements
    xor_all = 0
    for i in range(1, n + 1):
        xor_all ^= i
    for num in nums:
        xor_all ^= num

    # xor_all = missing1 ^ missing2

    # Find rightmost set bit (where they differ)
    diff_bit = xor_all & (-xor_all)

    # Partition
    a, b = 0, 0
    for i in range(1, n + 1):
        if i & diff_bit:
            a ^= i
        else:
            b ^= i
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num

    return [a, b]


# Test
print(findTwoMissing([1, 3, 5, 6], 6))  # [2, 4] or [4, 2]
```

---

## Problem: Sum of Two Integers (Without + Operator)

**LeetCode 371**: Calculate sum of two integers without using + or -.

### Example

```
Input: a = 1, b = 2
Output: 3

Input: a = 2, b = 3
Output: 5
```

### Solution

```python
def getSum(a: int, b: int) -> int:
    """
    Add two integers using bit manipulation.

    Key insight:
    - XOR gives sum without considering carry
    - AND gives carry bits (shifted left)
    - Repeat until no carry

    Note: Python needs masking for negative numbers
    due to arbitrary precision integers.

    Time: O(1) - at most 32 iterations
    Space: O(1)
    """
    # 32-bit mask
    mask = 0xFFFFFFFF
    max_int = 0x7FFFFFFF

    while b != 0:
        # XOR for sum without carry
        # AND << 1 for carry
        a, b = (a ^ b) & mask, ((a & b) << 1) & mask

    # Handle negative result
    return a if a <= max_int else ~(a ^ mask)


# Test
print(getSum(1, 2))    # 3
print(getSum(-1, 1))   # 0
print(getSum(-2, -3))  # -5
```

### Bit Addition Visualization

```
Adding 5 + 3:
  5 = 101
  3 = 011

Step 1:
  sum (no carry) = 5 ^ 3 = 101 ^ 011 = 110
  carry = (5 & 3) << 1 = (001) << 1 = 010

  a = 110 (6), b = 010 (2)

Step 2:
  sum (no carry) = 6 ^ 2 = 110 ^ 010 = 100
  carry = (6 & 2) << 1 = (010) << 1 = 100

  a = 100 (4), b = 100 (4)

Step 3:
  sum (no carry) = 4 ^ 4 = 000
  carry = (4 & 4) << 1 = (100) << 1 = 1000

  a = 000, b = 1000

Step 4:
  sum = 0 ^ 8 = 8
  carry = 0

  a = 8, b = 0 → done!

Result: 8... wait, that's wrong for 5+3=8?

Actually let me recalculate:
5 + 3 = 8... yes that's right! 5 + 3 = 8.
```

---

## Problem: Swap Without Temp

Exchange values of two variables without using a temporary variable.

### Solution

```python
def swap_xor(a: int, b: int) -> tuple[int, int]:
    """
    Swap using XOR.

    a ^= b  →  a = a ^ b
    b ^= a  →  b = b ^ (a ^ b) = a
    a ^= b  →  a = (a ^ b) ^ a = b

    Time: O(1)
    Space: O(1)
    """
    if a != b:  # Avoid zeroing out if same variable
        a ^= b
        b ^= a
        a ^= b
    return a, b


# In Python, prefer: a, b = b, a (clearer and equally efficient)

# Example
x, y = 5, 10
x, y = swap_xor(x, y)
print(x, y)  # 10, 5
```

---

## Problem: Find Different Element

Given an array where all elements are same except one, find the different one.

### Example

```
Input: [2, 2, 2, 5, 2]
Output: 5

Input: [1, 1, 3, 1, 1]
Output: 3
```

### Solution

```python
def findDifferent(nums: list[int]) -> int:
    """
    Find the element that's different from all others.

    Key insight: Can't use simple XOR (majority isn't pairs).
    Check first few elements to identify the common value.

    Time: O(n)
    Space: O(1)
    """
    # The first three elements contain at least 2 copies of common
    if nums[0] == nums[1]:
        common = nums[0]
    elif nums[0] == nums[2]:
        common = nums[0]
    else:
        common = nums[1]

    for num in nums:
        if num != common:
            return num

    return -1  # All same (shouldn't happen per problem)


# XOR won't work directly here because we need pairs for cancellation
# This problem is better solved with simple comparison
```

---

## Problem: Decode XORed Array

**LeetCode 1720**: Given encoded array where `encoded[i] = arr[i] XOR arr[i+1]`, and first element, find original array.

### Example

```
Input: encoded = [1, 2, 3], first = 1
Output: [1, 0, 2, 1]

Because:
  arr[0] = 1 (given)
  arr[0] ^ arr[1] = 1  →  arr[1] = 1 ^ 1 = 0
  arr[1] ^ arr[2] = 2  →  arr[2] = 0 ^ 2 = 2
  arr[2] ^ arr[3] = 3  →  arr[3] = 2 ^ 3 = 1
```

### Solution

```python
def decode(encoded: list[int], first: int) -> list[int]:
    """
    Decode XOR-encoded array.

    Use property: if a ^ b = c, then a = b ^ c

    Time: O(n)
    Space: O(n) for result
    """
    result = [first]
    for val in encoded:
        result.append(result[-1] ^ val)
    return result


# Test
print(decode([1, 2, 3], 1))  # [1, 0, 2, 1]
```

---

## Complexity Analysis

| Problem | Time | Space | Key Technique |
|---------|------|-------|---------------|
| Missing Number | O(n) | O(1) | XOR indices and values |
| Two Missing Numbers | O(n) | O(1) | XOR + partition by diff bit |
| Sum of Two Integers | O(1) | O(1) | XOR + carry with AND |
| Swap | O(1) | O(1) | Triple XOR |
| Decode XORed Array | O(n) | O(n) | Reversibility of XOR |

---

## Common XOR Patterns

### 1. Find Single in Pairs

```python
def find_single(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
```

### 2. Toggle Specific Bit

```python
def toggle_bit(n, pos):
    return n ^ (1 << pos)
```

### 3. Check if Two Numbers Have Opposite Signs

```python
def opposite_signs(a, b):
    return (a ^ b) < 0
```

### 4. XOR of Range [0, n]

```python
def xor_range(n):
    """
    XOR of 0 to n follows a pattern:
    n % 4 == 0 → n
    n % 4 == 1 → 1
    n % 4 == 2 → n + 1
    n % 4 == 3 → 0
    """
    if n % 4 == 0:
        return n
    elif n % 4 == 1:
        return 1
    elif n % 4 == 2:
        return n + 1
    else:
        return 0


# XOR of range [a, b]
def xor_range_ab(a, b):
    return xor_range(b) ^ xor_range(a - 1)
```

---

## Edge Cases

1. **Empty array**: Handle before XOR loop
2. **Single element**: XOR result is that element
3. **All same elements**: XOR gives 0 (not useful for finding unique)
4. **Negative numbers**: XOR works the same on signed integers
5. **Overflow**: Python handles arbitrary precision

---

## Interview Tips

1. **Know the four XOR properties**: Self-cancel, identity, commutative, associative
2. **Draw the XOR table**: Shows you understand the operation
3. **Explain why pairs cancel**: a ^ a = 0
4. **Handle edge cases**: Check for empty arrays, single elements
5. **Compare with alternatives**: XOR gives O(1) space vs hash table O(n)

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Missing Number | Easy | XOR indices and values |
| 2 | Single Number III | Medium | XOR + partition |
| 3 | Sum of Two Integers | Medium | XOR for sum, AND for carry |
| 4 | Decode XORed Array | Easy | XOR reversibility |
| 5 | XOR Queries of a Subarray | Medium | Prefix XOR |
| 6 | Maximum XOR of Two Numbers | Medium | Trie for XOR |

---

## Related Sections

- [Binary Basics](./01-binary-basics.md) - XOR operator fundamentals
- [Single Number](./02-single-number.md) - Classic XOR applications
- [Bit Manipulation Tricks](./06-bit-manipulation-tricks.md) - More techniques
