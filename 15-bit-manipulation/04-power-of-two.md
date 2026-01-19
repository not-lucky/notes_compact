# Power of Two

> **Prerequisites:** [Binary Basics](./01-binary-basics.md), [Counting Bits](./03-counting-bits.md)

## Interview Context

Power of two checks are common interview questions because they have an elegant O(1) bit manipulation solution. These problems test whether you understand binary representation and can recognize patterns.

---

## Pattern: Power of Two Properties

Powers of two have a unique property: they have exactly one set bit.

```
Power of 2    Binary      Property
1             0001        Single 1 bit
2             0010        Single 1 bit
4             0100        Single 1 bit
8             1000        Single 1 bit
16            10000       Single 1 bit

Not power of 2:
3 = 0011      (two 1s)
5 = 0101      (two 1s)
6 = 0110      (two 1s)

Key insight: n & (n-1) clears the rightmost 1 bit.
For power of 2, clearing the only 1 gives 0!
```

---

## Problem: Power of Two

**LeetCode 231**: Given an integer n, return true if it is a power of two.

### Example

```
Input: n = 1 → Output: true  (2⁰ = 1)
Input: n = 16 → Output: true (2⁴ = 16)
Input: n = 3 → Output: false
Input: n = 0 → Output: false
Input: n = -16 → Output: false
```

### Solution

```python
def isPowerOfTwo(n: int) -> bool:
    """
    Check if n is a power of 2.

    Key insight: Power of 2 has exactly one set bit.
    n & (n-1) clears the rightmost set bit.
    If result is 0, there was only one set bit.

    Time: O(1)
    Space: O(1)
    """
    return n > 0 and (n & (n - 1)) == 0


# Alternative: Check if only one bit is set
def isPowerOfTwo_alt(n: int) -> bool:
    """Use popcount to check if exactly one bit is set."""
    return n > 0 and bin(n).count('1') == 1


# Test
print(isPowerOfTwo(1))    # True (2^0)
print(isPowerOfTwo(16))   # True (2^4)
print(isPowerOfTwo(3))    # False
print(isPowerOfTwo(0))    # False
print(isPowerOfTwo(-16))  # False
```

### Why n & (n-1) Works

```
n = 8 = 1000:
  n - 1 = 0111
  n & (n-1) = 1000 & 0111 = 0000 ✓ (Power of 2)

n = 6 = 0110:
  n - 1 = 0101
  n & (n-1) = 0110 & 0101 = 0100 ✗ (Not power of 2)

n = 16 = 10000:
  n - 1 = 01111
  n & (n-1) = 10000 & 01111 = 00000 ✓ (Power of 2)

The trick: n-1 flips all bits from rightmost 1 to the right.
If n is power of 2, all bits become 0 after AND.
```

---

## Problem: Power of Four

**LeetCode 342**: Given an integer n, return true if it is a power of four.

### Example

```
Input: n = 16 → Output: true  (4² = 16)
Input: n = 5 → Output: false
Input: n = 1 → Output: true  (4⁰ = 1)
Input: n = 2 → Output: false (power of 2 but not 4)
```

### Solution

```python
def isPowerOfFour(n: int) -> bool:
    """
    Check if n is a power of 4.

    Conditions:
    1. n > 0
    2. n is power of 2 (single set bit)
    3. The set bit is at an even position (0, 2, 4, ...)

    The mask 0x55555555 = 01010101... has 1s at even positions.

    Time: O(1)
    Space: O(1)
    """
    # 0x55555555 = 01010101 01010101 01010101 01010101
    # This mask has 1s at positions 0, 2, 4, 6, ... (even positions)
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0


# Alternative using modulo
def isPowerOfFour_mod(n: int) -> bool:
    """
    Power of 4 minus 1 is always divisible by 3.
    4^k - 1 = (4-1)(4^(k-1) + 4^(k-2) + ... + 1) = 3 × something
    """
    return n > 0 and (n & (n - 1)) == 0 and (n - 1) % 3 == 0


# Test
print(isPowerOfFour(1))   # True (4^0)
print(isPowerOfFour(16))  # True (4^2)
print(isPowerOfFour(2))   # False (2^1, not power of 4)
print(isPowerOfFour(8))   # False (2^3, not power of 4)
print(isPowerOfFour(64))  # True (4^3)
```

### Powers of Four in Binary

```
Powers of 4:
  4⁰ = 1  = 0001      (bit at position 0)
  4¹ = 4  = 0100      (bit at position 2)
  4² = 16 = 10000     (bit at position 4)
  4³ = 64 = 1000000   (bit at position 6)

Pattern: Single 1 bit at EVEN positions (0, 2, 4, 6, ...)

Powers of 2 but NOT 4:
  2¹ = 2  = 0010      (bit at position 1 - ODD)
  2³ = 8  = 1000      (bit at position 3 - ODD)
  2⁵ = 32 = 100000    (bit at position 5 - ODD)

Mask 0x55555555:
  Binary: 01010101 01010101 01010101 01010101
  Has 1s at all EVEN positions

If (n & mask) != 0, the single bit is at an even position.
```

---

## Problem: Power of Three

**LeetCode 326**: Given an integer n, return true if it is a power of three.

### Example

```
Input: n = 27 → Output: true (3³)
Input: n = 0 → Output: false
Input: n = 9 → Output: true (3²)
Input: n = 45 → Output: false
```

### Solution

```python
def isPowerOfThree(n: int) -> bool:
    """
    Check if n is a power of 3.

    Note: No simple bit trick for 3 (not power of 2).
    Use the fact that 3^19 = 1162261467 is the largest
    power of 3 that fits in a 32-bit signed integer.

    If n is a power of 3, then 3^19 % n == 0.

    Time: O(1)
    Space: O(1)
    """
    return n > 0 and 1162261467 % n == 0


# Alternative: Loop
def isPowerOfThree_loop(n: int) -> bool:
    """Check by repeatedly dividing by 3."""
    if n <= 0:
        return False
    while n % 3 == 0:
        n //= 3
    return n == 1


# Test
print(isPowerOfThree(1))   # True (3^0)
print(isPowerOfThree(9))   # True (3^2)
print(isPowerOfThree(27))  # True (3^3)
print(isPowerOfThree(45))  # False
```

### Why the Modulo Trick Works

```
3^19 = 1162261467 (largest power of 3 in 32-bit signed int)

Powers of 3: 1, 3, 9, 27, 81, 243, 729, ...

All powers of 3 divide 3^19 evenly:
  3^19 % 3^0 = 0 ✓
  3^19 % 3^1 = 0 ✓
  3^19 % 3^5 = 0 ✓

Non-powers of 3 don't divide evenly:
  3^19 % 2 ≠ 0 ✗
  3^19 % 6 ≠ 0 ✗
  3^19 % 45 ≠ 0 ✗

Only powers of 3 (prime factorization contains only 3s)
can divide a pure power of 3 evenly.
```

---

## Problem: Bitwise AND of Numbers Range

**LeetCode 201**: Given two integers left and right, return the bitwise AND of all numbers in [left, right].

### Example

```
Input: left = 5, right = 7
Output: 4

5 = 101
6 = 110
7 = 111
5 & 6 & 7 = 100 = 4
```

### Solution

```python
def rangeBitwiseAnd(left: int, right: int) -> int:
    """
    Find common prefix of left and right.

    Key insight: When we AND a range, any bit that changes
    within the range will become 0. We only keep the
    common prefix bits that stay constant.

    Time: O(log n)
    Space: O(1)
    """
    shift = 0
    while left < right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift


# Alternative: Clear rightmost differing bits
def rangeBitwiseAnd_v2(left: int, right: int) -> int:
    """Keep clearing rightmost bit of right until right <= left."""
    while right > left:
        right &= right - 1
    return right


# Test
print(rangeBitwiseAnd(5, 7))    # 4
print(rangeBitwiseAnd(0, 0))    # 0
print(rangeBitwiseAnd(1, 2147483647))  # 0
```

### Why Common Prefix Works

```
Range [5, 7]:
  5 = 101
  6 = 110
  7 = 111

Notice: The leftmost bit (position 2) is always 1.
But positions 0 and 1 change values.

Any bit that "flips" during the range becomes 0 in the AND.

Algorithm:
  left=5=101, right=7=111, shift=0
  left < right, so:
    left>>1 = 10, right>>1 = 11, shift=1
  left < right, so:
    left>>1 = 1, right>>1 = 1, shift=2
  left == right, stop!
  return 1 << 2 = 100 = 4

The common prefix is 1, and we shift it back.
```

---

## Complexity Analysis

| Problem | Time | Space | Technique |
|---------|------|-------|-----------|
| Power of Two | O(1) | O(1) | n & (n-1) == 0 |
| Power of Four | O(1) | O(1) | Power of 2 + mask check |
| Power of Three | O(1) | O(1) | Modulo by max power |
| Range Bitwise AND | O(log n) | O(1) | Find common prefix |

---

## Common Variations

### 1. Next Power of Two

```python
def next_power_of_two(n: int) -> int:
    """
    Find smallest power of 2 >= n.

    Time: O(log n)
    Space: O(1)
    """
    if n <= 0:
        return 1
    if n & (n - 1) == 0:
        return n  # Already power of 2

    # Fill all bits to the right of highest set bit
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    return n + 1


print(next_power_of_two(5))   # 8
print(next_power_of_two(8))   # 8
print(next_power_of_two(17))  # 32
```

### 2. Previous Power of Two

```python
def prev_power_of_two(n: int) -> int:
    """
    Find largest power of 2 <= n.

    Time: O(log n)
    Space: O(1)
    """
    if n <= 0:
        return 0
    if n & (n - 1) == 0:
        return n  # Already power of 2

    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    return (n + 1) >> 1


print(prev_power_of_two(5))   # 4
print(prev_power_of_two(8))   # 8
print(prev_power_of_two(17))  # 16
```

### 3. Log Base 2

```python
def log2_floor(n: int) -> int:
    """
    Floor of log base 2 (position of highest set bit).

    Time: O(1) with bit_length()
    """
    return n.bit_length() - 1 if n > 0 else -1


def log2_ceil(n: int) -> int:
    """Ceiling of log base 2."""
    if n <= 0:
        return -1
    floor = log2_floor(n)
    return floor if n == (1 << floor) else floor + 1


print(log2_floor(8))   # 3
print(log2_floor(10))  # 3
print(log2_ceil(8))    # 3
print(log2_ceil(10))   # 4
```

---

## Edge Cases

1. **Zero**: Not a power of any positive integer
2. **One**: Power of every base (n⁰ = 1)
3. **Negative numbers**: Not powers of positive bases
4. **Large numbers**: Watch for overflow in some languages
5. **Range where left == right**: Result is left (or right)

---

## Interview Tips

1. **Know the n & (n-1) trick**: This is essential for power of 2
2. **Explain the binary insight**: Show understanding, not just memorization
3. **Handle edge cases first**: Check n > 0 before bit operations
4. **Power of 4 mask**: Knowing 0x55555555 is impressive
5. **Power of 3**: Explain why bit tricks don't apply (3 isn't power of 2)

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Power of Two | Easy | n & (n-1) |
| 2 | Power of Three | Easy | Modulo by max power |
| 3 | Power of Four | Easy | Mask for even positions |
| 4 | Bitwise AND of Numbers Range | Medium | Common prefix |
| 5 | Find Highest Set Bit | Easy | bit_length() |

---

## Related Sections

- [Binary Basics](./01-binary-basics.md) - Bitwise operators
- [Counting Bits](./03-counting-bits.md) - Related techniques
- [Bit Manipulation Tricks](./06-bit-manipulation-tricks.md) - More tricks
