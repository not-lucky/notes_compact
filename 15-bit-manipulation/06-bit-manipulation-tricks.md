# Bit Manipulation Tricks

> **Prerequisites:** [Binary Basics](./01-binary-basics.md), [Counting Bits](./03-counting-bits.md)

## Interview Context

This section is a compendium of bit manipulation tricks that appear across various interview problems. These techniques are building blocks that combine to solve complex problems elegantly.

---

## Trick 1: Isolate the Rightmost Set Bit

```python
def rightmost_set_bit(n: int) -> int:
    """
    Isolate the rightmost 1 bit.

    Formula: n & (-n)

    Why it works:
    -n = ~n + 1 (two's complement)
    This flips all bits and adds 1, which means:
    - All bits left of rightmost 1 become opposite
    - Rightmost 1 stays 1
    - All bits right of it (were 0, flipped to 1, +1 ripples through) become 0

    Time: O(1)
    """
    return n & (-n)


# Examples
print(bin(rightmost_set_bit(12)))   # 0b100 (12 = 1100, rightmost 1 is at position 2)
print(bin(rightmost_set_bit(10)))   # 0b10  (10 = 1010, rightmost 1 is at position 1)
print(bin(rightmost_set_bit(8)))    # 0b1000 (8 = 1000, only bit is position 3)
```

### Visualization

```
n = 12 = 1100
-n = 0100 (in two's complement for the relevant bits)

  1100
& 0100
------
  0100 = 4 (rightmost set bit isolated)
```

---

## Trick 2: Clear the Rightmost Set Bit

```python
def clear_rightmost_set_bit(n: int) -> int:
    """
    Clear the rightmost 1 bit.

    Formula: n & (n - 1)

    Why it works:
    n - 1 flips the rightmost 1 to 0 and all bits right of it to 1.
    ANDing clears the rightmost 1 while keeping everything else.

    This is Brian Kernighan's trick!

    Time: O(1)
    """
    return n & (n - 1)


# Examples
print(bin(clear_rightmost_set_bit(12)))  # 0b1000 (12=1100 → 8=1000)
print(bin(clear_rightmost_set_bit(10)))  # 0b1000 (10=1010 → 8=1000)
print(bin(clear_rightmost_set_bit(8)))   # 0b0    (8=1000 → 0)
```

---

## Trick 3: Set the Rightmost Clear Bit

```python
def set_rightmost_clear_bit(n: int) -> int:
    """
    Set the rightmost 0 bit to 1.

    Formula: n | (n + 1)

    Why it works:
    n + 1 flips the rightmost 0 to 1 (and ripples carry).
    ORing preserves all 1s and sets the new 1.

    Time: O(1)
    """
    return n | (n + 1)


# Examples
print(bin(set_rightmost_clear_bit(12)))  # 0b1101 (12=1100 → 13=1101)
print(bin(set_rightmost_clear_bit(5)))   # 0b111  (5=101 → 7=111)
```

---

## Trick 4: Turn Off Rightmost Consecutive 1s

```python
def turn_off_rightmost_consecutive_ones(n: int) -> int:
    """
    Turn off all trailing 1s (rightmost consecutive 1s).

    Formula: n & (n + 1)

    Example: 0b1011 → 0b1000 (trailing 11 cleared)

    Time: O(1)
    """
    return n & (n + 1)


# Examples
print(bin(turn_off_rightmost_consecutive_ones(0b1011)))  # 0b1000
print(bin(turn_off_rightmost_consecutive_ones(0b1111)))  # 0b0
print(bin(turn_off_rightmost_consecutive_ones(0b1100)))  # 0b1100 (no trailing 1s)
```

---

## Trick 5: Check if Integer is Power of 2

```python
def is_power_of_two(n: int) -> bool:
    """
    Check if n is a power of 2.

    Formula: n > 0 and (n & (n - 1)) == 0

    Why: Powers of 2 have exactly one set bit.
    Clearing it gives 0.

    Time: O(1)
    """
    return n > 0 and (n & (n - 1)) == 0


# Examples
print(is_power_of_two(8))   # True
print(is_power_of_two(6))   # False
print(is_power_of_two(1))   # True (2^0)
print(is_power_of_two(0))   # False
```

---

## Trick 6: Get/Set/Clear/Toggle Bit at Position

```python
def get_bit(n: int, pos: int) -> int:
    """Get bit at position pos (0-indexed from right)."""
    return (n >> pos) & 1


def set_bit(n: int, pos: int) -> int:
    """Set bit at position pos to 1."""
    return n | (1 << pos)


def clear_bit(n: int, pos: int) -> int:
    """Clear bit at position pos to 0."""
    return n & ~(1 << pos)


def toggle_bit(n: int, pos: int) -> int:
    """Toggle bit at position pos."""
    return n ^ (1 << pos)


# Examples
n = 0b1010  # 10
print(get_bit(n, 1))            # 1
print(get_bit(n, 0))            # 0
print(bin(set_bit(n, 0)))       # 0b1011
print(bin(clear_bit(n, 3)))     # 0b10
print(bin(toggle_bit(n, 2)))    # 0b1110
```

---

## Trick 7: Reverse Bits

```python
def reverseBits(n: int) -> int:
    """
    Reverse all 32 bits of an unsigned integer.

    LeetCode 190

    Time: O(1) - fixed 32 iterations
    Space: O(1)
    """
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


# Optimized: Divide and conquer (swap halves recursively)
def reverseBits_optimized(n: int) -> int:
    """Reverse using parallel swapping."""
    n = ((n & 0xFFFF0000) >> 16) | ((n & 0x0000FFFF) << 16)  # Swap 16-bit halves
    n = ((n & 0xFF00FF00) >> 8)  | ((n & 0x00FF00FF) << 8)   # Swap 8-bit pairs
    n = ((n & 0xF0F0F0F0) >> 4)  | ((n & 0x0F0F0F0F) << 4)   # Swap 4-bit pairs
    n = ((n & 0xCCCCCCCC) >> 2)  | ((n & 0x33333333) << 2)   # Swap 2-bit pairs
    n = ((n & 0xAAAAAAAA) >> 1)  | ((n & 0x55555555) << 1)   # Swap adjacent bits
    return n


# Example
print(reverseBits(0b00000010100101000001111010011100))
# Returns: 964176192 = 0b00111001011110000010100101000000
```

---

## Trick 8: Subsets Using Bitmask

```python
def generate_subsets(nums: list[int]) -> list[list[int]]:
    """
    Generate all subsets using bit manipulation.

    For n elements, iterate from 0 to 2^n - 1.
    Each bit position represents include/exclude.

    LeetCode 78

    Time: O(n × 2^n)
    Space: O(n × 2^n) for output
    """
    n = len(nums)
    result = []

    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):  # If bit i is set
                subset.append(nums[i])
        result.append(subset)

    return result


# Example
print(generate_subsets([1, 2, 3]))
# [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
```

### Bitmask Visualization

```
nums = [1, 2, 3], n = 3

mask = 0 = 000 → []
mask = 1 = 001 → [1]     (bit 0 set)
mask = 2 = 010 → [2]     (bit 1 set)
mask = 3 = 011 → [1, 2]  (bits 0, 1 set)
mask = 4 = 100 → [3]     (bit 2 set)
mask = 5 = 101 → [1, 3]  (bits 0, 2 set)
mask = 6 = 110 → [2, 3]  (bits 1, 2 set)
mask = 7 = 111 → [1,2,3] (all bits set)
```

---

## Trick 9: Count Bits Differing in Position

```python
def different_bit_positions(a: int, b: int) -> list[int]:
    """
    Find all positions where a and b differ.

    Time: O(number of differing bits)
    """
    xor = a ^ b
    positions = []
    pos = 0
    while xor:
        if xor & 1:
            positions.append(pos)
        xor >>= 1
        pos += 1
    return positions


# Example
print(different_bit_positions(5, 9))  # [2, 3] (5=0101, 9=1001)
```

---

## Trick 10: Swap All Even and Odd Bits

```python
def swap_even_odd_bits(n: int) -> int:
    """
    Swap all even position bits with odd position bits.

    Example: 0b10101010 → 0b01010101

    Time: O(1)
    """
    # 0xAAAAAAAA = 10101010... (even positions)
    # 0x55555555 = 01010101... (odd positions)
    even_bits = n & 0xAAAAAAAA
    odd_bits = n & 0x55555555
    return (even_bits >> 1) | (odd_bits << 1)


# Example
print(bin(swap_even_odd_bits(0b10101010)))  # 0b1010101
```

---

## Trick 11: Gray Code

```python
def to_gray(n: int) -> int:
    """
    Convert binary to Gray code.
    Gray code: adjacent values differ by exactly one bit.

    Formula: n ^ (n >> 1)

    Time: O(1)
    """
    return n ^ (n >> 1)


def from_gray(gray: int) -> int:
    """Convert Gray code back to binary."""
    n = gray
    mask = n >> 1
    while mask:
        n ^= mask
        mask >>= 1
    return n


def generate_gray_code(n: int) -> list[int]:
    """
    Generate n-bit Gray code sequence.
    LeetCode 89

    Time: O(2^n)
    """
    return [i ^ (i >> 1) for i in range(1 << n)]


# Example
print([bin(x) for x in generate_gray_code(3)])
# ['0b0', '0b1', '0b11', '0b10', '0b110', '0b111', '0b101', '0b100']
```

---

## Trick 12: Find Position of Only Set Bit

```python
def position_of_only_set_bit(n: int) -> int:
    """
    If n has exactly one set bit, return its position.
    Returns -1 if not exactly one set bit.

    Time: O(log n)
    """
    if n <= 0 or (n & (n - 1)) != 0:
        return -1  # Not exactly one set bit

    position = 0
    while n > 1:
        n >>= 1
        position += 1
    return position


# Using Python built-in
def position_of_only_set_bit_builtin(n: int) -> int:
    if n <= 0 or (n & (n - 1)) != 0:
        return -1
    return n.bit_length() - 1


# Example
print(position_of_only_set_bit(8))   # 3
print(position_of_only_set_bit(16))  # 4
print(position_of_only_set_bit(5))   # -1 (not power of 2)
```

---

## Trick 13: Absolute Value Without Branching

```python
def abs_without_branching(n: int) -> int:
    """
    Get absolute value without using if statement.

    For 32-bit signed integer.

    Note: This is hardware-specific and mainly educational.
    In Python, just use abs(n).

    Time: O(1)
    """
    # For 32-bit signed integer
    mask = n >> 31  # All 1s if negative, all 0s if positive
    return (n + mask) ^ mask


# Example
print(abs_without_branching(-5))  # 5
print(abs_without_branching(5))   # 5
```

---

## Trick 14: Minimum/Maximum Without Branching

```python
def min_without_branching(a: int, b: int) -> int:
    """
    Find minimum without using if or ternary.

    Note: Primarily educational. Use min() in practice.
    """
    return b ^ ((a ^ b) & -(a < b))


def max_without_branching(a: int, b: int) -> int:
    """Find maximum without branching."""
    return a ^ ((a ^ b) & -(a < b))


# Example
print(min_without_branching(3, 5))  # 3
print(max_without_branching(3, 5))  # 5
```

---

## Common Bitmasks Reference

```python
# 32-bit masks
ALL_ONES_32 = 0xFFFFFFFF       # 11111111 11111111 11111111 11111111
EVEN_BITS   = 0xAAAAAAAA       # 10101010 10101010 10101010 10101010
ODD_BITS    = 0x55555555       # 01010101 01010101 01010101 01010101
HIGH_HALF   = 0xFFFF0000       # Upper 16 bits
LOW_HALF    = 0x0000FFFF       # Lower 16 bits

# Useful for extracting bytes
BYTE_0 = 0x000000FF  # Lowest byte
BYTE_1 = 0x0000FF00
BYTE_2 = 0x00FF0000
BYTE_3 = 0xFF000000  # Highest byte
```

---

## Complexity Analysis

| Trick | Time | Space | Common Use |
|-------|------|-------|------------|
| Isolate rightmost 1 | O(1) | O(1) | Loop control, partition |
| Clear rightmost 1 | O(1) | O(1) | Counting bits, power of 2 |
| Get/Set/Clear/Toggle | O(1) | O(1) | Bit manipulation basics |
| Reverse bits | O(1) | O(1) | Networking, cryptography |
| Generate subsets | O(n × 2^n) | O(2^n) | Backtracking alternative |
| Gray code | O(1) | O(1) | Error detection |

---

## Interview Tips

1. **Know the formulas**: n & (n-1), n & (-n), n ^ (n >> 1)
2. **Explain why they work**: Draw out the bit patterns
3. **Recognize when to use bitmasks**: Subsets, flags, state compression
4. **Start with simpler approach**: Then optimize with bit tricks
5. **Practice reading binary**: Quick mental conversion helps

---

## Practice Problems

| # | Problem | Difficulty | Key Trick |
|---|---------|------------|-----------|
| 1 | Reverse Bits | Easy | Bit by bit reversal |
| 2 | Subsets | Medium | Bitmask iteration |
| 3 | Gray Code | Medium | n ^ (n >> 1) |
| 4 | Single Number II | Medium | Bit counting |
| 5 | Maximum XOR | Medium | Trie + XOR |
| 6 | UTF-8 Validation | Medium | Bit pattern matching |

---

## Related Sections

- [Binary Basics](./01-binary-basics.md) - Operator fundamentals
- [Single Number](./02-single-number.md) - XOR applications
- [Power of Two](./04-power-of-two.md) - n & (n-1) applications
- [XOR Tricks](./05-xor-tricks.md) - XOR-specific techniques
