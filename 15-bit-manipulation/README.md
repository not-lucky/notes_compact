# Chapter 15: Bit Manipulation

Bit manipulation involves directly working with the binary representation of numbers using bitwise operators. These techniques provide elegant O(1) solutions to many problems and are highly valued in technical interviews for testing low-level understanding.

## Building Intuition

**Why Bits Matter: The Computer's Native Language**

Everything in a computer is ultimately bits. When you manipulate bits directly, you're speaking the computer's native language—no translation needed. This is why bit manipulation is fast: you're doing exactly what the hardware was designed to do.

**The Power of O(1) Operations**

Most bit operations complete in a single CPU cycle, regardless of the value:

```
Checking if 1,000,000,000 is even:
  n % 2         → Division (multiple cycles)
  n & 1         → Single AND instruction (1 cycle)

Same result, vastly different cost at scale.
```

**The Key Mental Shift**

Stop thinking about numbers as values; think about them as **arrays of bits**:

```
The number 13 isn't just "thirteen"
It's the bit array [1, 0, 1, 1] (reading right to left)

Position:  3   2   1   0
Bit:       1   0   1   1
Value:     8 + 0 + 2 + 1 = 13
```

Once you see numbers as bit arrays, operations become intuitive:
- AND = element-wise minimum
- OR = element-wise maximum
- XOR = element-wise difference detector
- Shift = slide the array left/right

**Why XOR is the Star of Bit Manipulation**

XOR has properties no other operator has:
- `a ^ a = 0` (self-cancellation)
- `a ^ 0 = a` (identity)
- It's its own inverse: `a ^ b ^ b = a`

These properties enable finding unique elements, swapping without temp variables, and simple encryption.

**The "Bit Trick" Pattern**

Most bit tricks follow a pattern:
1. Identify a property that's visible in binary representation
2. Find an operation that isolates or transforms that property
3. Use masking (AND/OR) to extract the result

```
Example: Is n a power of 2?
1. Property: Powers of 2 have exactly one 1-bit
2. n & (n-1) clears the rightmost 1-bit
3. If clearing the only bit gives 0, it was a power of 2
```

## When NOT to Use Bit Manipulation

**1. Readability Over Cleverness**

In production code, `n % 2 == 0` is better than `(n & 1) == 0`. Both compile to the same thing, but one is readable by everyone.

**2. Floating Point Numbers**

Bit manipulation is for integers only. Floats have a completely different internal representation (sign, exponent, mantissa).

**3. When a Hashmap is Cleaner**

Not every "find unique element" problem needs XOR. If the constraints allow O(n) space, a Counter might be clearer.

**4. Python's Arbitrary Precision**

Python integers have no fixed bit width. Some C/Java tricks need explicit masking:
```python
# In Python, ~5 has conceptually infinite leading 1s
# Use: (~5) & 0xFFFFFFFF for 32-bit behavior
```

---

## Why Bit Manipulation Matters

1. **Interview frequency**: Appears in ~5-8% of FANG interviews
2. **Efficiency**: O(1) time and space for many operations
3. **Elegance**: Impressive solutions that demonstrate deep understanding
4. **Systems knowledge**: Shows understanding of how computers work

---

## Bitwise Operators Overview

| Operator | Symbol | Description | Example (a=5, b=3) |
|----------|--------|-------------|--------------------|
| AND | `&` | 1 if both bits are 1 | `5 & 3 = 1` (101 & 011 = 001) |
| OR | `\|` | 1 if either bit is 1 | `5 \| 3 = 7` (101 \| 011 = 111) |
| XOR | `^` | 1 if bits differ | `5 ^ 3 = 6` (101 ^ 011 = 110) |
| NOT | `~` | Flip all bits | `~5 = -6` (inverts all bits) |
| Left Shift | `<<` | Shift bits left | `5 << 1 = 10` (101 → 1010) |
| Right Shift | `>>` | Shift bits right | `5 >> 1 = 2` (101 → 10) |

---

## Binary Representation Visualization

```
Decimal 13 in binary (8-bit representation):

Position:   7   6   5   4   3   2   1   0
Power:    128  64  32  16   8   4   2   1
Bits:       0   0   0   0   1   1   0   1

13 = 8 + 4 + 1 = 2³ + 2² + 2⁰

Common values:
  1 = 0001      8 = 1000
  2 = 0010      15 = 1111
  3 = 0011      16 = 10000
  4 = 0100      31 = 11111
  5 = 0101      32 = 100000
  6 = 0110      255 = 11111111
  7 = 0111
```

---

## When to Use Bit Manipulation

### Strong Indicators (Use Bit Manipulation)

1. **"Single number"**: Finding unique element among duplicates
2. **Power of two**: Checking or working with powers of 2
3. **XOR operations**: Pairing, toggling, finding differences
4. **Space constraints**: O(1) space requirement when bits can encode state
5. **Binary properties**: Problems about bits, binary strings
6. **Subset generation**: Each bit represents include/exclude

### Weak Indicators (Consider Alternatives)

1. **Large number ranges**: Hash tables may be clearer
2. **Floating point**: Bit manipulation is for integers
3. **Complex logic**: Sometimes clearer with math/conditions
4. **Negative numbers**: Be careful with sign bit

---

## Core Bit Manipulation Patterns

| Pattern | Technique | Example Use Case |
|---------|-----------|------------------|
| XOR Pairing | `a ^ a = 0` | Find single number |
| Bit Check | `n & (1 << i)` | Check if bit i is set |
| Bit Set | `n \| (1 << i)` | Set bit i to 1 |
| Bit Clear | `n & ~(1 << i)` | Clear bit i to 0 |
| Bit Toggle | `n ^ (1 << i)` | Flip bit i |
| Power of Two | `n & (n-1) == 0` | Check power of 2 |
| Lowest Set Bit | `n & (-n)` | Isolate rightmost 1 |
| Clear Lowest Bit | `n & (n-1)` | Remove rightmost 1 |

---

## Chapter Contents

| # | Topic | Key Concepts |
|---|-------|--------------|
| 01 | [Binary Basics](./01-binary-basics.md) | Binary representation, bitwise operators |
| 02 | [Single Number](./02-single-number.md) | Single number I, II, III variants |
| 03 | [Counting Bits](./03-counting-bits.md) | Count set bits, Hamming distance |
| 04 | [Power of Two](./04-power-of-two.md) | Power of two/four checks |
| 05 | [XOR Tricks](./05-xor-tricks.md) | XOR properties, missing number |
| 06 | [Bit Manipulation Tricks](./06-bit-manipulation-tricks.md) | Common tricks compendium |

---

## Implementation Template: Common Bit Operations

```python
class BitOperations:
    """
    Common bit manipulation operations.

    All operations: O(1) time, O(1) space
    """

    @staticmethod
    def get_bit(n: int, i: int) -> bool:
        """Check if bit at position i is set (1)."""
        return (n & (1 << i)) != 0

    @staticmethod
    def set_bit(n: int, i: int) -> int:
        """Set bit at position i to 1."""
        return n | (1 << i)

    @staticmethod
    def clear_bit(n: int, i: int) -> int:
        """Clear bit at position i to 0."""
        return n & ~(1 << i)

    @staticmethod
    def toggle_bit(n: int, i: int) -> int:
        """Toggle bit at position i."""
        return n ^ (1 << i)

    @staticmethod
    def count_set_bits(n: int) -> int:
        """Count number of 1 bits (Brian Kernighan's algorithm)."""
        count = 0
        while n:
            n &= n - 1  # Clear rightmost set bit
            count += 1
        return count

    @staticmethod
    def is_power_of_two(n: int) -> bool:
        """Check if n is a power of 2."""
        return n > 0 and (n & (n - 1)) == 0

    @staticmethod
    def lowest_set_bit(n: int) -> int:
        """Isolate the rightmost set bit."""
        return n & (-n)


# Example usage
print(BitOperations.get_bit(5, 2))      # True (5 = 101, bit 2 is set)
print(BitOperations.set_bit(5, 1))      # 7 (101 | 010 = 111)
print(BitOperations.clear_bit(5, 2))    # 1 (101 & ~100 = 001)
print(BitOperations.count_set_bits(7))  # 3 (111 has 3 ones)
print(BitOperations.is_power_of_two(8)) # True
```

---

## Common Mistakes

1. **Operator precedence**: Use parentheses! `(n & mask) != 0` not `n & mask != 0`
2. **Sign extension**: Python integers are arbitrary precision; be careful with `~`
3. **Off-by-one in positions**: Bit 0 is rightmost, not leftmost
4. **Forgetting edge cases**: 0, negative numbers, overflow
5. **Mixing logical and bitwise**: `and`/`or` vs `&`/`|`

---

## Time Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Single bitwise op | O(1) | O(1) | AND, OR, XOR, NOT, shifts |
| Count set bits | O(k) | O(1) | k = number of set bits |
| Iterate all bits | O(log n) | O(1) | Or O(32) for 32-bit int |

---

## Space Complexity

```
O(1) for almost all bit manipulation operations

Key insight: We're manipulating existing integers,
not allocating new data structures.

This is why bit manipulation is often requested
when "O(1) space" is required.
```

---

## Classic Interview Problems by Company

| Company | Favorite Bit Manipulation Problems |
|---------|-----------------------------------|
| Google | Single Number III, Hamming Distance, Reverse Bits |
| Meta | Missing Number, Sum of Two Integers, Subsets |
| Amazon | Power of Two, Number of 1 Bits, Counting Bits |
| Microsoft | Single Number, Bitwise AND of Range, Complement |
| Apple | UTF-8 Validation, Maximum XOR, Gray Code |

---

## Bit Manipulation Problem Signals

Look for these keywords/patterns:

```
- "Single/unique element" → XOR
- "Power of two" → n & (n-1)
- "Count bits/ones" → Brian Kernighan or table
- "XOR" mentioned → XOR properties
- "Binary representation" → Bit manipulation
- "O(1) space" constraint → Consider bits
- "Subset generation" → Bitmask iteration
- "Toggle/flip" → XOR
```

---

## Comparison: When Bit Manipulation vs Other Approaches

| Scenario | Use Bit Manipulation | Use Alternative |
|----------|---------------------|-----------------|
| Find unique among pairs | XOR all elements | Hash table (if pairs not guaranteed) |
| Check power of 2 | `n & (n-1) == 0` | Loop (slower) |
| Count 1s in binary | Brian Kernighan | `bin(n).count('1')` (Pythonic) |
| Store boolean flags | Bitmask | Array/set (if clarity needed) |
| Generate subsets | Bitmask `0` to `2^n-1` | Backtracking (if order matters) |

---

## Quick Reference: Essential Formulas

| Goal | Formula | Example |
|------|---------|---------|
| Check bit i | `(n >> i) & 1` | `(5 >> 2) & 1 = 1` |
| Set bit i | `n \| (1 << i)` | `5 \| 2 = 7` |
| Clear bit i | `n & ~(1 << i)` | `7 & ~2 = 5` |
| Toggle bit i | `n ^ (1 << i)` | `5 ^ 2 = 7` |
| Clear lowest set bit | `n & (n - 1)` | `6 & 5 = 4` |
| Isolate lowest set bit | `n & -n` | `6 & -6 = 2` |
| Check power of 2 | `n > 0 and n & (n-1) == 0` | `8 & 7 = 0` → True |
| Multiply by 2 | `n << 1` | `5 << 1 = 10` |
| Divide by 2 | `n >> 1` | `5 >> 1 = 2` |
| Swap without temp | `a ^= b; b ^= a; a ^= b` | Swaps a and b |

---

## Start: [01-binary-basics.md](./01-binary-basics.md)

Begin with understanding binary representation and the fundamental bitwise operators.
