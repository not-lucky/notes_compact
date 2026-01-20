# Binary Basics

> **Prerequisites:** None (foundational topic)

## Interview Context

Understanding binary representation and bitwise operators is fundamental to all bit manipulation problems. Interviewers expect you to know these basics cold—they're the building blocks for more complex bit manipulation techniques.

---

## Building Intuition

**Why Binary Matters for Programming**

Every piece of data in a computer—numbers, text, images, code—is ultimately stored as binary: sequences of 0s and 1s. Understanding binary isn't just academic; it's the language your computer actually speaks.

**The Positional Number System Insight**

You already understand positional notation from decimal:

```
The number 347 = 3×100 + 4×10 + 7×1
                = 3×10² + 4×10¹ + 7×10⁰
```

Binary works identically, just with base 2 instead of 10:

```
The number 101 (binary) = 1×4 + 0×2 + 1×1
                        = 1×2² + 0×2¹ + 1×2⁰
                        = 5 (decimal)
```

**Why Powers of 2 Appear Everywhere**

This is why you see 2, 4, 8, 16, 32, 64, 128, 256... constantly in computing. Each represents a single bit position:

```
Bit position:  7    6    5    4    3    2    1    0
Value:       128   64   32   16    8    4    2    1

An 8-bit number can represent 0 to 255 (2⁸ - 1)
```

**The AND/OR/XOR Mental Models**

Think of these operators as asking questions about each bit position:

- **AND**: "Are BOTH bits 1?" → Used for masking (extracting specific bits)
- **OR**: "Is AT LEAST ONE bit 1?" → Used for setting bits
- **XOR**: "Are the bits DIFFERENT?" → Used for toggling and finding uniqueness

```
Think of AND as an "intersection" — keeps only what's in both
Think of OR as a "union" — includes everything from either
Think of XOR as a "difference detector" — marks where they disagree
```

**Why XOR is Special**

XOR has a property no other operator has: it's its own inverse.

```
a XOR b XOR b = a

This means: whatever XOR does, applying XOR again undoes it.
This property is the foundation of:
- Finding single elements among pairs
- Simple encryption
- Error detection
```

**Shifts as Multiplication/Division**

Left shift (`<<`) multiplies by 2, right shift (`>>`) divides by 2:

```
5 << 1 = 10  (5 × 2 = 10)
5 << 2 = 20  (5 × 4 = 20)
5 >> 1 = 2   (5 ÷ 2 = 2, floored)

Why? Each position to the left is worth 2× more.
Moving all bits left by 1 = multiplying each position's value by 2.
```

---

## When NOT to Use Bit Manipulation

**1. When Readability Matters More Than Micro-Optimization**

```python
# Bit manipulation version
is_even = (n & 1) == 0

# Readable version
is_even = n % 2 == 0
```

In most code, the second version is better. Save bit manipulation for:
- Hot paths where every nanosecond counts
- Interview problems that specifically require it
- Problems where bit properties are essential (not just optimizations)

**2. Floating Point Numbers**

Bit manipulation works on integers. Floats have a completely different internal representation (sign, exponent, mantissa) and bitwise operators will give nonsensical results:

```python
# This doesn't work as expected
# Floats aren't just "numbers stored in binary"
5.5 & 3  # TypeError in Python
```

**3. When Built-ins Are Clearer**

Python provides excellent built-ins that compile to the same operations:

```python
# Instead of counting bits manually:
count = bin(n).count('1')  # Pythonic
count = n.bit_length()      # For finding highest bit

# Instead of manual floor division by power of 2:
result = n // 4  # Clearer than n >> 2 in most contexts
```

**4. Variable-Width Integers (Python's Arbitrary Precision)**

Python integers can be arbitrarily large, which means:
- `~n` doesn't give you a simple bit flip (no fixed width)
- Two's complement behavior differs from C/Java
- Some tricks that work with 32-bit integers need masking

```python
# In C/Java: ~5 = -6 (with fixed bit width)
# In Python: ~5 = -6 (but the binary representation is conceptually infinite)

# For 32-bit simulation in Python:
result = ~n & 0xFFFFFFFF  # Mask to 32 bits
```

**Red Flags (Don't Use Bit Manipulation):**
- Problem doesn't mention bits, binary, or XOR specifically
- Floating point input
- When a hashmap or set would be clearer
- When the "clever" solution obscures the algorithm

---

## Pattern: Binary Number System

The binary (base-2) number system represents values using only 0 and 1. Each position represents a power of 2.

### Binary to Decimal Conversion

```
Binary:  1 0 1 1 0 1
         ↓ ↓ ↓ ↓ ↓ ↓
Power:  2⁵ 2⁴ 2³ 2² 2¹ 2⁰
Value:  32 16  8  4  2  1

Calculation: 32 + 0 + 8 + 4 + 0 + 1 = 45

So binary 101101 = decimal 45
```

### Decimal to Binary Conversion

```
Method: Repeatedly divide by 2, collect remainders (read bottom to top)

45 ÷ 2 = 22 remainder 1  ↑
22 ÷ 2 = 11 remainder 0  |
11 ÷ 2 = 5  remainder 1  | Read upward: 101101
5  ÷ 2 = 2  remainder 1  |
2  ÷ 2 = 1  remainder 0  |
1  ÷ 2 = 0  remainder 1  ↑

So decimal 45 = binary 101101
```

---

## Bitwise Operators

### AND (`&`)

Returns 1 only if both bits are 1.

```
    1 0 1 1  (11)
  & 1 1 0 1  (13)
  ---------
    1 0 0 1  (9)

Truth table:
  0 & 0 = 0
  0 & 1 = 0
  1 & 0 = 0
  1 & 1 = 1

Use cases:
- Check if bit is set: n & (1 << i)
- Clear bits: n & mask
- Check if number is even: n & 1 == 0
```

### OR (`|`)

Returns 1 if either bit is 1.

```
    1 0 1 1  (11)
  | 1 1 0 1  (13)
  ---------
    1 1 1 1  (15)

Truth table:
  0 | 0 = 0
  0 | 1 = 1
  1 | 0 = 1
  1 | 1 = 1

Use cases:
- Set a bit: n | (1 << i)
- Combine flags: flags | NEW_FLAG
```

### XOR (`^`)

Returns 1 if bits differ.

```
    1 0 1 1  (11)
  ^ 1 1 0 1  (13)
  ---------
    0 1 1 0  (6)

Truth table:
  0 ^ 0 = 0
  0 ^ 1 = 1
  1 ^ 0 = 1
  1 ^ 1 = 0

Key properties:
- a ^ a = 0 (self-cancellation)
- a ^ 0 = a (identity)
- a ^ b = b ^ a (commutative)
- (a ^ b) ^ c = a ^ (b ^ c) (associative)

Use cases:
- Find single number among pairs
- Toggle bits
- Swap without temp variable
```

### NOT (`~`)

Flips all bits (one's complement).

```
    ~ 0 1 0 1  (5)
    ---------
      1 0 1 0  (-6 in two's complement)

Note: In Python, ~n = -(n + 1)
  ~5  = -6
  ~0  = -1
  ~(-1) = 0
```

### Left Shift (`<<`)

Shifts bits left, filling with 0s. Equivalent to multiplying by 2^k.

```
    5 << 1:
    0101 << 1 = 1010 (10)

    5 << 2:
    0101 << 2 = 10100 (20)

    In general: n << k = n × 2^k
```

### Right Shift (`>>`)

Shifts bits right. Equivalent to integer division by 2^k.

```
    20 >> 1:
    10100 >> 1 = 1010 (10)

    20 >> 2:
    10100 >> 2 = 101 (5)

    In general: n >> k = n ÷ 2^k (floor division)

Note: For negative numbers, Python uses arithmetic shift
(sign bit is preserved).
```

---

## Implementation

### Basic Bit Operations

```python
def get_bit(n: int, i: int) -> bool:
    """
    Get the value of bit at position i (0-indexed from right).

    Time: O(1)
    Space: O(1)
    """
    return (n & (1 << i)) != 0


def set_bit(n: int, i: int) -> int:
    """
    Set bit at position i to 1.

    Time: O(1)
    Space: O(1)
    """
    return n | (1 << i)


def clear_bit(n: int, i: int) -> int:
    """
    Clear bit at position i to 0.

    Time: O(1)
    Space: O(1)
    """
    return n & ~(1 << i)


def toggle_bit(n: int, i: int) -> int:
    """
    Toggle bit at position i (0 -> 1 or 1 -> 0).

    Time: O(1)
    Space: O(1)
    """
    return n ^ (1 << i)


def update_bit(n: int, i: int, value: bool) -> int:
    """
    Update bit at position i to given value.

    Time: O(1)
    Space: O(1)
    """
    # Clear the bit first, then set if value is True
    cleared = n & ~(1 << i)
    return cleared | (int(value) << i)


# Examples
n = 0b1010  # 10 in decimal

print(f"n = {n} = {bin(n)}")
print(f"bit 1: {get_bit(n, 1)}")      # True (1010, position 1 is 1)
print(f"bit 2: {get_bit(n, 2)}")      # False (1010, position 2 is 0)
print(f"set bit 0: {bin(set_bit(n, 0))}")     # 0b1011
print(f"clear bit 3: {bin(clear_bit(n, 3))}")  # 0b0010
print(f"toggle bit 1: {bin(toggle_bit(n, 1))}")  # 0b1000
```

### Conversion Utilities

```python
def decimal_to_binary(n: int) -> str:
    """
    Convert decimal to binary string representation.

    Time: O(log n)
    Space: O(log n)
    """
    if n == 0:
        return "0"

    is_negative = n < 0
    n = abs(n)
    result = []

    while n:
        result.append(str(n & 1))
        n >>= 1

    binary = ''.join(reversed(result))
    return f"-{binary}" if is_negative else binary


def binary_to_decimal(s: str) -> int:
    """
    Convert binary string to decimal integer.

    Time: O(n) where n is string length
    Space: O(1)
    """
    result = 0
    for char in s:
        result = (result << 1) | (1 if char == '1' else 0)
    return result


# Python built-ins (often faster in interviews)
n = 45
print(bin(n))        # '0b101101'
print(bin(n)[2:])    # '101101' (without '0b' prefix)
print(int('101101', 2))  # 45
```

---

## Problem: Add Binary

**LeetCode 67**: Given two binary strings `a` and `b`, return their sum as a binary string.

### Example

```
Input: a = "11", b = "1"
Output: "100"

  11
+  1
----
 100

Input: a = "1010", b = "1011"
Output: "10101"

 1010
+1011
-----
10101
```

### Solution

```python
def addBinary(a: str, b: str) -> str:
    """
    Add two binary strings.

    Time: O(max(m, n)) where m, n are string lengths
    Space: O(max(m, n)) for the result
    """
    result = []
    carry = 0
    i, j = len(a) - 1, len(b) - 1

    while i >= 0 or j >= 0 or carry:
        # Get current digits (0 if index out of bounds)
        digit_a = int(a[i]) if i >= 0 else 0
        digit_b = int(b[j]) if j >= 0 else 0

        # Calculate sum and carry
        total = digit_a + digit_b + carry
        result.append(str(total % 2))
        carry = total // 2

        i -= 1
        j -= 1

    return ''.join(reversed(result))


# Alternative: Use Python built-ins (for quick solution)
def addBinary_pythonic(a: str, b: str) -> str:
    return bin(int(a, 2) + int(b, 2))[2:]


# Test
print(addBinary("11", "1"))      # "100"
print(addBinary("1010", "1011"))  # "10101"
```

---

## Problem: Number Complement

**LeetCode 476**: Given a positive integer, return its complement number. The complement flips all bits in the binary representation.

### Example

```
Input: 5
Binary: 101
Complement: 010 = 2
Output: 2

Input: 7
Binary: 111
Complement: 000 = 0
Output: 0
```

### Solution

```python
def findComplement(num: int) -> int:
    """
    Find the complement of a number (flip all bits).

    Key insight: We only flip the significant bits, not all 32 bits.

    Time: O(log n) - need to find bit length
    Space: O(1)
    """
    if num == 0:
        return 1

    # Create a mask with all 1s of the same length as num
    # e.g., if num = 5 (101), mask = 111 (7)
    mask = (1 << num.bit_length()) - 1

    # XOR with mask flips all significant bits
    return num ^ mask


# Alternative: Build mask iteratively
def findComplement_v2(num: int) -> int:
    mask = 1
    while mask <= num:
        mask <<= 1
    return (mask - 1) ^ num


# Test
print(findComplement(5))   # 2 (101 -> 010)
print(findComplement(7))   # 0 (111 -> 000)
print(findComplement(10))  # 5 (1010 -> 0101)
```

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Get bit | O(1) | O(1) | Single AND + shift |
| Set bit | O(1) | O(1) | Single OR + shift |
| Clear bit | O(1) | O(1) | AND with NOT |
| Toggle bit | O(1) | O(1) | Single XOR |
| Decimal ↔ Binary | O(log n) | O(log n) | Process each bit |

---

## Common Variations

### 1. Checking Odd/Even

```python
def is_odd(n: int) -> bool:
    """Check if n is odd using bit manipulation."""
    return (n & 1) == 1

def is_even(n: int) -> bool:
    """Check if n is even using bit manipulation."""
    return (n & 1) == 0

# Why it works:
# Odd numbers always have LSB = 1:  5 = 101, 7 = 111
# Even numbers always have LSB = 0: 4 = 100, 6 = 110
```

### 2. Swap Without Temp Variable

```python
def swap(a: int, b: int) -> tuple[int, int]:
    """Swap two numbers using XOR (no temporary variable)."""
    a ^= b  # a now holds a ^ b
    b ^= a  # b = b ^ (a ^ b) = a
    a ^= b  # a = (a ^ b) ^ a = b
    return a, b

# Example
x, y = 5, 10
x, y = swap(x, y)
print(x, y)  # 10, 5
```

### 3. Sign of Number

```python
def sign(n: int) -> int:
    """Return 1 for positive, -1 for negative, 0 for zero."""
    if n == 0:
        return 0
    # Check if sign bit is set (for negative numbers in two's complement)
    return -1 if n < 0 else 1

# For 32-bit integers specifically:
def is_negative_32bit(n: int) -> bool:
    return (n >> 31) & 1 == 1
```

---

## Edge Cases

1. **Zero**: `bin(0)` = '0b0', many formulas need special handling
2. **Negative numbers**: Python uses arbitrary precision, no fixed bit width
3. **Large numbers**: Python handles arbitrary size integers
4. **Empty strings**: Handle in binary string problems
5. **Leading zeros**: May or may not be significant

---

## Interview Tips

1. **Know operator precedence**: Bitwise operators have lower precedence than comparison
   - `n & 1 == 0` is parsed as `n & (1 == 0)` - WRONG!
   - Use `(n & 1) == 0` instead

2. **Python bit_length()**: Useful built-in for finding number of bits
   - `(5).bit_length()` = 3 (since 5 = 101)

3. **Python bin()**: Quick way to see binary representation
   - `bin(5)` = '0b101'

4. **Mention time/space**: All basic bit operations are O(1)

5. **Draw it out**: Binary visualization helps avoid mistakes

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Add Binary | Easy | Binary addition with carry |
| 2 | Number Complement | Easy | XOR with mask |
| 3 | Reverse Bits | Easy | Bit by bit reconstruction |
| 4 | Convert Binary Number in Linked List | Easy | Binary to decimal |
| 5 | Concatenation of Consecutive Binary Numbers | Medium | Bit shifting |

---

## Related Sections

- [Single Number](./02-single-number.md) - XOR applications
- [Counting Bits](./03-counting-bits.md) - Counting set bits
- [XOR Tricks](./05-xor-tricks.md) - Advanced XOR techniques
