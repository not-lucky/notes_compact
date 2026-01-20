# Single Number

## Problem Statement

Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one.

You must implement a solution with O(1) extra space complexity.

**Example:**
```
Input: nums = [2, 2, 1]
Output: 1

Input: nums = [4, 1, 2, 1, 2]
Output: 4
```

## Approach

### Key Insight: XOR Properties
1. `a ⊕ a = 0` (XOR with itself is 0)
2. `a ⊕ 0 = a` (XOR with 0 is identity)
3. XOR is commutative and associative

So if we XOR all numbers, pairs cancel out, leaving the single number.

```
[4, 1, 2, 1, 2]
4 ⊕ 1 ⊕ 2 ⊕ 1 ⊕ 2
= 4 ⊕ (1 ⊕ 1) ⊕ (2 ⊕ 2)
= 4 ⊕ 0 ⊕ 0
= 4
```

## Implementation

```python
def single_number(nums: list[int]) -> int:
    """
    Find the single number using XOR.

    Time: O(n)
    Space: O(1)
    """
    result = 0
    for num in nums:
        result ^= num
    return result


def single_number_reduce(nums: list[int]) -> int:
    """
    Using functools.reduce.
    """
    from functools import reduce
    from operator import xor
    return reduce(xor, nums)


def single_number_math(nums: list[int]) -> int:
    """
    Using math: 2 × sum(set) - sum(all)

    Time: O(n)
    Space: O(n) - for set
    """
    return 2 * sum(set(nums)) - sum(nums)
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| XOR | O(n) | O(1) | Optimal |
| Set Math | O(n) | O(n) | Uses extra space |
| Hash Map | O(n) | O(n) | Count occurrences |

## Edge Cases

1. **Single element**: Return that element
2. **Three elements**: Two same, one different
3. **Large array**: XOR handles efficiently
4. **Negative numbers**: XOR works the same

## Common Mistakes

1. **Using wrong operator**: Must use XOR (^), not OR (|)
2. **Forgetting to initialize**: Start with 0
3. **Modifying input**: XOR approach doesn't need to

## Variations

### Single Number II (Each appears 3 times)
```python
def single_number_ii(nums: list[int]) -> int:
    """
    Every element appears 3 times except one.

    Approach: Count bits. Each bit position appears 3k times
    for paired elements. The remainder is from single number.

    Time: O(32n) = O(n)
    Space: O(1)
    """
    result = 0

    for i in range(32):
        bit_count = 0
        for num in nums:
            # Count 1s at position i
            if num & (1 << i):
                bit_count += 1

        # If not divisible by 3, single number has this bit
        if bit_count % 3:
            result |= (1 << i)

    # Handle negative numbers (Python's int is unbounded)
    if result >= 2**31:
        result -= 2**32

    return result


def single_number_ii_state_machine(nums: list[int]) -> int:
    """
    Using state machine with ones and twos.

    ones: bits that appeared 1 time (mod 3)
    twos: bits that appeared 2 times (mod 3)

    Time: O(n)
    Space: O(1)
    """
    ones = twos = 0

    for num in nums:
        # Update ones: add new bits, remove if in twos
        ones = (ones ^ num) & ~twos
        # Update twos: add bits leaving ones
        twos = (twos ^ num) & ~ones

    return ones
```

### Single Number III (Two different numbers)
```python
def single_number_iii(nums: list[int]) -> list[int]:
    """
    Two elements appear once, others appear twice.
    Find both single numbers.

    Approach:
    1. XOR all → a ⊕ b (the two singles XORed)
    2. Find a set bit (where a and b differ)
    3. Split into two groups based on that bit
    4. XOR each group separately

    Time: O(n)
    Space: O(1)
    """
    # Step 1: XOR all numbers
    xor_all = 0
    for num in nums:
        xor_all ^= num

    # Step 2: Find rightmost set bit (where a and b differ)
    rightmost_bit = xor_all & (-xor_all)

    # Step 3 & 4: Split and XOR
    a = b = 0
    for num in nums:
        if num & rightmost_bit:
            a ^= num
        else:
            b ^= num

    return [a, b]
```

### Find the Difference
```python
def find_the_difference(s: str, t: str) -> str:
    """
    t is s with one extra character. Find it.

    Time: O(n)
    Space: O(1)
    """
    result = 0
    for c in s:
        result ^= ord(c)
    for c in t:
        result ^= ord(c)
    return chr(result)
```

### Missing Number
```python
def missing_number(nums: list[int]) -> int:
    """
    Array contains n distinct numbers from [0, n].
    One is missing. Find it.

    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    result = n  # Start with n (index never reached)

    for i, num in enumerate(nums):
        result ^= i ^ num

    return result
```

### Find Duplicate Number (Floyd's Cycle)
```python
def find_duplicate(nums: list[int]) -> int:
    """
    Array of n+1 integers in range [1, n].
    Exactly one duplicate. Find it.

    Treat as linked list: nums[i] points to nums[nums[i]]
    Use Floyd's cycle detection.

    Time: O(n)
    Space: O(1)
    """
    # Find cycle
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Find cycle start
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow
```

## XOR Properties Summary

```
a ⊕ 0 = a       (Identity)
a ⊕ a = 0       (Self-inverse)
a ⊕ b = b ⊕ a   (Commutative)
(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)  (Associative)
```

## Related Problems

- **Single Number II** - Elements appear 3 times
- **Single Number III** - Two single elements
- **Find the Difference** - XOR on strings
- **Missing Number** - XOR with indices
- **Find the Duplicate Number** - Floyd's algorithm
- **Maximum XOR of Two Numbers** - Trie-based approach
