# Power of Two Solutions

## 1. Power of Two
**Problem Statement**: Given an integer `n`, return `true` if it is a power of two. Otherwise, return `false`. An integer `n` is a power of two if there exists an integer `x` such that `n == 2^x`.

### Examples & Edge Cases
- **Example 1**: `n = 1` → `true` (2^0)
- **Example 2**: `n = 16` → `true` (2^4)
- **Example 3**: `n = 3` → `false`
- **Edge Cases**:
    - `n = 0`: `false`.
    - `n < 0`: `false`.

### Optimal Python Solution
```python
def isPowerOfTwo(n: int) -> bool:
    """
    Checks if n is a power of 2 using bit manipulation.
    A power of 2 has exactly one set bit.
    """
    # n & (n - 1) clears the rightmost set bit.
    # If n is a power of 2, clearing the only bit results in 0.
    return n > 0 and (n & (n - 1)) == 0
```

### Explanation
In binary representation, a power of two is represented as a `1` followed by zero or more `0`s (e.g., `8` is `1000`). This means it has exactly one set bit. The operation `n & (n - 1)` clears the rightmost set bit. If `n` is a power of two, clearing that one bit will result in `0`. We also check `n > 0` because zero and negative numbers are not powers of two.

### Complexity Analysis
- **Time Complexity**: O(1).
- **Space Complexity**: O(1).

---

## 2. Power of Three
**Problem Statement**: Given an integer `n`, return `true` if it is a power of three. Otherwise, return `false`.

### Examples & Edge Cases
- **Example 1**: `n = 27` → `true`
- **Example 2**: `n = 0` → `false`
- **Example 3**: `n = 9` → `true`
- **Edge Cases**:
    - `n = 1`: `true` (3^0).

### Optimal Python Solution
```python
def isPowerOfThree(n: int) -> bool:
    """
    Checks if n is a power of 3.
    Since 3 is prime, any power of 3 will divide the largest
    power of 3 that fits in a 32-bit signed integer.
    """
    # 3^19 = 1162261467 is the largest power of 3 in 32-bit range
    return n > 0 and 1162261467 % n == 0
```

### Explanation
Unlike powers of two, powers of three do not have a simple bit pattern. However, we can use number theory. Since 3 is a prime number, the only divisors of 3^k are 3^j where 0 <= j <= k. The largest power of three that fits into a 32-bit signed integer is 3^19 (1,162,261,467). If `n` is a power of three, it must divide this number.

### Complexity Analysis
- **Time Complexity**: O(1).
- **Space Complexity**: O(1).

---

## 3. Power of Four
**Problem Statement**: Given an integer `n`, return `true` if it is a power of four. Otherwise, return `false`.

### Examples & Edge Cases
- **Example 1**: `n = 16` → `true`
- **Example 2**: `n = 5` → `false`
- **Example 3**: `n = 1` → `true`
- **Edge Cases**:
    - `n = 2`: `false` (it's a power of 2, but not 4).

### Optimal Python Solution
```python
def isPowerOfFour(n: int) -> bool:
    """
    Checks if n is a power of 4.
    Conditions:
    1. n > 0
    2. n is a power of 2 (has only one set bit)
    3. That single bit is at an even position (0, 2, 4...)
    """
    # Mask 0x55555555 (01010101...) has 1s at positions 0, 2, 4, 6...
    is_power_of_two = n > 0 and (n & (n - 1)) == 0
    bit_in_even_pos = (n & 0x55555555) != 0

    return is_power_of_two and bit_in_even_pos
```

### Explanation
A power of four (4^k) is also a power of two (2^(2k)). This means it has exactly one set bit. Additionally, that bit must be at an even position (0, 2, 4, ...). For example, `4^0 = 1` (bit 0), `4^1 = 4` (bit 2), `4^2 = 16` (bit 4). We use the mask `0x55555555` to check if the set bit is in one of these even positions.

### Complexity Analysis
- **Time Complexity**: O(1).
- **Space Complexity**: O(1).

---

## 4. Bitwise AND of Numbers Range
**Problem Statement**: Given two integers `left` and `right` that represent the range `[left, right]`, return the bitwise AND of all numbers in this range, inclusive.

### Examples & Edge Cases
- **Example 1**: `left = 5, right = 7` → `4` (101 & 110 & 111 = 100)
- **Example 2**: `left = 0, right = 0` → `0`
- **Edge Cases**:
    - Large range: `left = 1, right = 2147483647` → `0`.

### Optimal Python Solution
```python
def rangeBitwiseAnd(left: int, right: int) -> int:
    """
    Finds the common prefix of left and right.
    Logic: Shifting both right until they are equal.
    """
    shift = 0
    # Keep shifting right until both numbers are the same
    # This removes all bits that differ in the range
    while left < right:
        left >>= 1
        right >>= 1
        shift += 1

    # Shift back to the original positions
    return left << shift
```

### Explanation
When we perform a bitwise AND on a range of numbers, any bit position that changes from 0 to 1 (or vice versa) within that range will eventually be ANDed with a 0, making that bit 0 in the result. The only bits that remain 1 are the ones in the "common prefix" of the binary representations of `left` and `right`. We find this prefix by shifting both numbers right until they are equal.

### Complexity Analysis
- **Time Complexity**: O(log N) where N is the value of `right`. We shift at most 31 times for a 32-bit integer.
- **Space Complexity**: O(1).

---

## 5. Find Highest Set Bit
**Problem Statement**: Given a positive integer `n`, find the index of its highest set bit (0-indexed from the right).

### Examples & Edge Cases
- **Example 1**: `n = 8` (1000) → `3`
- **Example 2**: `n = 1` (1) → `0`
- **Edge Cases**:
    - Smallest positive integer: `1`.

### Optimal Python Solution
```python
def highestSetBit(n: int) -> int:
    """
    Returns the index of the highest set bit.
    """
    if n <= 0:
        return -1

    # bit_length() returns the number of bits required to represent n
    # The highest bit index is bit_length - 1
    return n.bit_length() - 1
```

### Explanation
The `bit_length()` method in Python returns the number of bits required to represent an integer in binary, excluding the sign and leading zeros. For example, for `8` (binary `1000`), `bit_length()` is `4`. The index of the highest bit is therefore `4 - 1 = 3`.

### Complexity Analysis
- **Time Complexity**: O(1) (Python's `bit_length` is highly optimized).
- **Space Complexity**: O(1).
