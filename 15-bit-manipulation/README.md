# Chapter 15: Bit Manipulation

Bit manipulation involves directly working with the binary representation of numbers using bitwise operators. These techniques provide elegant O(1) solutions to many problems and are highly valued in technical interviews for testing low-level understanding.

## Building Intuition

**Why Bits Matter: The Computer's Native Language**

Everything in a computer is ultimately bits. When you manipulate bits directly, you're speaking the computer's native language — no translation needed. This is why bit manipulation is fast: you're doing exactly what the hardware was designed to do.

**The Power of O(1) Operations**

Most bit operations map to a single CPU instruction, regardless of the value:

```
Checking if 1,000,000,000 is even:
  n % 2         → Modulo operation
  n & 1         → Single AND instruction

Same result. At the hardware level, the AND is the most direct mapping
to what the CPU actually does. Modern compilers will optimize n % 2 to
n & 1 anyway, but understanding the bit-level operation is the point.
```

> **Python note**: In CPython, both operations carry interpreter overhead since
> integers are heap-allocated objects. The performance advantage of bitwise ops
> is most pronounced in C/C++/Rust. In interviews, we still reason about the
> underlying bit-level cost.

**The Key Mental Shift**

Stop thinking about numbers as values; think about them as **arrays of bits**:

```
The number 13 isn't just "thirteen"
It's a bit pattern: 1 1 0 1

Position:  3   2   1   0      (bit 0 is the rightmost / least significant)
Bit:       1   1   0   1
Value:     8 + 4 + 0 + 1 = 13
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
- Commutative and associative: `a ^ b = b ^ a`, `(a ^ b) ^ c = a ^ (b ^ c)`
- It's its own inverse: `a ^ b ^ b = a`

These properties enable finding unique elements, swapping without temp variables, and simple encryption.

**The "Bit Trick" Pattern**

Most bit tricks follow a pattern:

1. Identify a property that's visible in binary representation
2. Find an operation that isolates or transforms that property
3. Use masking (AND/OR) to extract the result

```
Example: Is n a power of 2?
1. Property: Powers of 2 have exactly one 1-bit (e.g., 8 = 1000)
2. n - 1 flips all bits at and below that single 1-bit (e.g., 7 = 0111)
3. n & (n-1) clears the rightmost 1-bit — if the result is 0, there was only one
```

## When NOT to Use Bit Manipulation

**1. Readability Over Cleverness**

In production code, `n % 2 == 0` is better than `(n & 1) == 0`. Both compile to the same thing, but one is readable by everyone.

**2. Floating Point Numbers**

Bit manipulation is for integers only. Floats have a completely different internal representation (IEEE 754: sign, exponent, mantissa).

**3. When a Hashmap is Cleaner**

Not every "find unique element" problem needs XOR. If the constraints allow O(n) space, a `Counter` might be clearer.

**4. Python's Arbitrary Precision Integers**

Python integers have no fixed bit width. Some C/Java tricks need explicit masking:

```python
# In Python, ~5 gives -6 (conceptually infinite leading 1s in two's complement)
# To get 32-bit unsigned behavior, mask the result:
result = (~5) & 0xFFFFFFFF  # 4294967290 (32-bit NOT of 5)
```

---

## Why Bit Manipulation Matters

1. **Interview frequency**: Appears in ~5-8% of FANG interviews
2. **Efficiency**: O(1) time and space for many operations
3. **Elegance**: Impressive solutions that demonstrate deep understanding
4. **Systems knowledge**: Shows understanding of how computers work at a fundamental level

---

## Bitwise Operators Overview

| Operator    | Symbol | Description          | Example (a=5, b=3)                       |
| ----------- | ------ | -------------------- | ----------------------------------------- |
| AND         | `&`    | 1 if both bits are 1 | `5 & 3 = 1` (101 & 011 = 001)            |
| OR          | `\|`   | 1 if either bit is 1 | `5 \| 3 = 7` (101 \| 011 = 111)          |
| XOR         | `^`    | 1 if bits differ     | `5 ^ 3 = 6` (101 ^ 011 = 110)            |
| NOT         | `~`    | Flip all bits        | `~5 = -6` (two's complement inversion)    |
| Left Shift  | `<<`   | Shift bits left      | `5 << 1 = 10` (101 -> 1010)              |
| Right Shift | `>>`   | Shift bits right     | `5 >> 1 = 2` (101 -> 10)                 |

**How NOT works in Python**: `~n` equals `-(n + 1)`. This follows from two's complement: flipping all bits of `n` gives you `-(n+1)`.

```python
~0   # -1
~5   # -6
~(-3) # 2
```

---

## Binary Representation Visualization

```
Decimal 13 in binary (8-bit representation):

Position:   7   6   5   4   3   2   1   0
Power:    128  64  32  16   8   4   2   1
Bits:       0   0   0   0   1   1   0   1

13 = 8 + 4 + 1 = 2^3 + 2^2 + 2^0

Common values:
  0 = 0000       8 = 1000
  1 = 0001       15 = 1111
  2 = 0010       16 = 10000
  3 = 0011       31 = 11111
  4 = 0100       32 = 100000
  5 = 0101       64 = 1000000
  6 = 0110       128 = 10000000
  7 = 0111       255 = 11111111
```

**Python binary conversion**:

```python
bin(13)        # '0b1101'
int('1101', 2) # 13
f"{13:08b}"    # '00001101' (zero-padded to 8 bits)
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
4. **Negative numbers**: Be careful with sign bit and Python's arbitrary-width integers

---

## Core Bit Manipulation Patterns

| Pattern          | Technique        | Example Use Case      |
| ---------------- | ---------------- | --------------------- |
| XOR Pairing      | `a ^ a = 0`      | Find single number    |
| Bit Check        | `n & (1 << i)`   | Check if bit i is set |
| Bit Set          | `n \| (1 << i)`  | Set bit i to 1        |
| Bit Clear        | `n & ~(1 << i)`  | Clear bit i to 0      |
| Bit Toggle       | `n ^ (1 << i)`   | Flip bit i            |
| Power of Two     | `n & (n-1) == 0` | Check power of 2      |
| Lowest Set Bit   | `n & (-n)`       | Isolate rightmost 1   |
| Clear Lowest Bit | `n & (n-1)`      | Remove rightmost 1    |

---

## Chapter Contents

| #   | Topic                                                      | Key Concepts                             |
| --- | ---------------------------------------------------------- | ---------------------------------------- |
| 01  | [Binary Basics](./01-binary-basics.md)                     | Binary representation, bitwise operators |
| 02  | [Single Number](./02-single-number.md)                     | Single number I, II, III variants        |
| 03  | [Counting Bits](./03-counting-bits.md)                     | Count set bits, Hamming distance         |
| 04  | [Power of Two](./04-power-of-two.md)                       | Power of two/four checks                 |
| 05  | [XOR Tricks](./05-xor-tricks.md)                           | XOR properties, missing number           |
| 06  | [Bit Manipulation Tricks](./06-bit-manipulation-tricks.md) | Common tricks compendium                 |

---

## Implementation Template: Common Bit Operations

```python
class BitOperations:
    """Common bit manipulation operations.

    All operations are O(1) time and O(1) space,
    except count_set_bits which is O(k) where k = number of set bits.
    """

    @staticmethod
    def get_bit(n: int, i: int) -> bool:
        """Check if bit at position i is set (1). Bit 0 is the least significant."""
        return (n & (1 << i)) != 0

    @staticmethod
    def set_bit(n: int, i: int) -> int:
        """Set bit at position i to 1."""
        return n | (1 << i)

    @staticmethod
    def clear_bit(n: int, i: int) -> int:
        """Clear bit at position i (set to 0)."""
        return n & ~(1 << i)

    @staticmethod
    def toggle_bit(n: int, i: int) -> int:
        """Toggle (flip) bit at position i."""
        return n ^ (1 << i)

    @staticmethod
    def count_set_bits(n: int) -> int:
        """Count number of 1 bits (Brian Kernighan's algorithm).

        Time: O(k) where k is the number of set bits.
        Each iteration clears the lowest set bit, so we loop exactly k times.
        """
        # In Python, negative numbers have infinite-width two's complement.
        # Mask to 32 bits to avoid an infinite loop.
        if n < 0:
            n &= 0xFFFFFFFF

        count = 0
        while n:
            n &= n - 1  # Clear the lowest set bit
            count += 1
        return count

    @staticmethod
    def is_power_of_two(n: int) -> bool:
        """Check if n is a power of 2. Must be positive (0 is not a power of 2)."""
        return n > 0 and (n & (n - 1)) == 0

    @staticmethod
    def lowest_set_bit(n: int) -> int:
        """Isolate the lowest (rightmost) set bit. Returns 0 if n == 0."""
        return n & (-n)

    @staticmethod
    def clear_bits_above(n: int, i: int) -> int:
        """Clear all bits from position i+1 to the most significant bit.

        Example: clear_bits_above(0b11111111, 2) -> 0b111 (7)
        """
        mask = (1 << (i + 1)) - 1  # e.g., i=2 -> mask = 0b111
        return n & mask

    @staticmethod
    def clear_bits_below(n: int, i: int) -> int:
        """Clear all bits from position 0 to i (inclusive).

        Example: clear_bits_below(0b11111111, 2) -> 0b11111000 (248)
        """
        mask = ~((1 << (i + 1)) - 1)  # e.g., i=2 -> mask = ...11111000
        return n & mask


# Example usage
if __name__ == "__main__":
    print(BitOperations.get_bit(5, 2))       # True  (5 = 101, bit 2 is 1)
    print(BitOperations.get_bit(5, 1))       # False (5 = 101, bit 1 is 0)
    print(BitOperations.set_bit(5, 1))       # 7     (101 | 010 = 111)
    print(BitOperations.clear_bit(5, 2))     # 1     (101 & ~100 = 001)
    print(BitOperations.toggle_bit(5, 0))    # 4     (101 ^ 001 = 100)
    print(BitOperations.count_set_bits(7))   # 3     (111 has three 1-bits)
    print(BitOperations.is_power_of_two(8))  # True  (1000 has exactly one 1-bit)
    print(BitOperations.is_power_of_two(6))  # False (110 has two 1-bits)
    print(BitOperations.lowest_set_bit(12))  # 4     (1100 -> lowest set bit is 100 = 4)
```

---

## Common Mistakes

1. **Operator precedence**: Bitwise operators have lower precedence than comparison operators. Always use parentheses: `(n & mask) != 0`, **not** `n & mask != 0` (which parses as `n & (mask != 0)`)
2. **Sign extension in Python**: Python integers have arbitrary precision. `~5` gives `-6`, not `0xFFFFFFFA`. Mask when you need fixed-width behavior: `(~5) & 0xFFFFFFFF`
3. **Off-by-one in bit positions**: Bit 0 is the rightmost (least significant), not the leftmost
4. **Forgetting edge cases**: Always handle `n = 0`, negative numbers, and potential overflow (in fixed-width languages)
5. **Mixing logical and bitwise**: `and`/`or` (short-circuit logical) vs `&`/`|` (bitwise). They are not interchangeable
6. **Shifting by negative or excessive amounts**: `1 << -1` raises `ValueError` in Python. In C, it's undefined behavior

---

## Time Complexity Analysis

| Operation            | Time     | Space | Notes                          |
| -------------------- | -------- | ----- | ------------------------------ |
| Single bitwise op    | O(1)     | O(1)  | AND, OR, XOR, NOT, shifts     |
| Count set bits       | O(k)     | O(1)  | k = number of set bits         |
| Iterate all bits     | O(log n) | O(1)  | Or O(32) for fixed 32-bit int |
| `bin(n).count('1')`  | O(log n) | O(log n) | Creates a string of the bits |

---

## Space Complexity

```
O(1) for almost all bit manipulation operations.

Key insight: We're manipulating existing integers,
not allocating new data structures.

This is why bit manipulation is often the answer
when "O(1) space" is required.
```

---

## Classic Interview Problems by Company

| Company   | Favorite Bit Manipulation Problems                |
| --------- | ------------------------------------------------- |
| Google    | Single Number III, Hamming Distance, Reverse Bits |
| Meta      | Missing Number, Sum of Two Integers, Subsets      |
| Amazon    | Power of Two, Number of 1 Bits, Counting Bits     |
| Microsoft | Single Number, Bitwise AND of Range, Complement   |
| Apple     | UTF-8 Validation, Maximum XOR, Gray Code          |

---

## Bit Manipulation Problem Signals

Look for these keywords/patterns:

```
"Single/unique element"   -> XOR
"Power of two"            -> n & (n-1)
"Count bits/ones"         -> Brian Kernighan's algorithm or lookup table
"XOR" mentioned           -> XOR properties
"Binary representation"   -> Bit manipulation
"O(1) space" constraint   -> Consider encoding state in bits
"Subset generation"       -> Bitmask iteration (0 to 2^n - 1)
"Toggle/flip"             -> XOR
"Without +/-/*"           -> Bit manipulation to simulate arithmetic
```

---

## Comparison: When Bit Manipulation vs Other Approaches

| Scenario                | Use Bit Manipulation    | Use Alternative                      |
| ----------------------- | ----------------------- | ------------------------------------ |
| Find unique among pairs | XOR all elements        | Hash table (if pairs not guaranteed) |
| Check power of 2        | `n & (n-1) == 0`        | Loop (slower)                        |
| Count 1s in binary      | Brian Kernighan's       | `bin(n).count('1')` (Pythonic)       |
| Store boolean flags     | Bitmask                 | Array/set (if clarity needed)        |
| Generate subsets        | Bitmask `0` to `2^n - 1`| Backtracking (if order matters)      |
| Add without `+`         | XOR + carry with AND    | Not applicable (interview-specific)  |

---

## Quick Reference: Essential Formulas

| Goal                   | Formula                       | Example                            |
| ---------------------- | ----------------------------- | ---------------------------------- |
| Check bit i            | `(n >> i) & 1`                | `(13 >> 2) & 1 = 1` (bit 2 of 1101)|
| Set bit i              | `n \| (1 << i)`               | `9 \| (1 << 1) = 11` (1001 -> 1011)|
| Clear bit i            | `n & ~(1 << i)`               | `7 & ~(1 << 1) = 5` (111 -> 101)  |
| Toggle bit i           | `n ^ (1 << i)`                | `5 ^ (1 << 1) = 7` (101 -> 111)   |
| Clear lowest set bit   | `n & (n - 1)`                 | `12 & 11 = 8` (1100 -> 1000)      |
| Isolate lowest set bit | `n & -n`                      | `12 & -12 = 4` (isolates 100)     |
| Check power of 2       | `n > 0 and (n & (n-1)) == 0`  | `8 & 7 = 0` -> True               |
| Multiply by 2^k        | `n << k`                      | `5 << 1 = 10`, `5 << 3 = 40`      |
| Divide by 2^k (floor)  | `n >> k`                      | `13 >> 1 = 6`, `13 >> 2 = 3`      |
| Swap without temp      | `a ^= b; b ^= a; a ^= b`     | Swaps a and b                      |
| Get all 1s mask (k bits)| `(1 << k) - 1`               | `(1 << 4) - 1 = 15` (1111)        |

---

## Practice Problems (Progressive Difficulty)

### Problem 1: Check if Bit is Set (Easy)

**Problem**: Given an integer `n` and a bit position `i`, return `True` if bit `i` is set.

```python
def is_bit_set(n: int, i: int) -> bool:
    """Check if bit at position i is set (0-indexed from the right).

    >>> is_bit_set(13, 0)  # 1101 -> bit 0 is 1
    True
    >>> is_bit_set(13, 1)  # 1101 -> bit 1 is 0
    False
    >>> is_bit_set(13, 3)  # 1101 -> bit 3 is 1
    True
    """
    return (n >> i) & 1 == 1
```

**Key insight**: Shift the target bit to position 0 and mask with `1`.

---

### Problem 2: Check if Number is Even or Odd (Easy)

**Problem**: Determine if `n` is even without using modulo.

```python
def is_even(n: int) -> bool:
    """Check if n is even using bit manipulation.

    The least significant bit is 0 for even numbers, 1 for odd.

    >>> is_even(4)   # 100 -> LSB is 0
    True
    >>> is_even(7)   # 111 -> LSB is 1
    False
    >>> is_even(0)
    True
    """
    return (n & 1) == 0
```

**Key insight**: The least significant bit directly encodes parity.

---

### Problem 3: Single Number (Medium) — LeetCode 136

**Problem**: Every element appears twice except one. Find it in O(n) time, O(1) space.

```python
def single_number(nums: list[int]) -> int:
    """Find the element that appears exactly once.

    XOR of a number with itself is 0, and XOR with 0 is identity.
    XOR-ing all elements cancels out the pairs, leaving the unique one.

    >>> single_number([2, 2, 1])
    1
    >>> single_number([4, 1, 2, 1, 2])
    4
    """
    result: int = 0
    for num in nums:
        result ^= num
    return result
```

**Key insight**: `a ^ a = 0` and `a ^ 0 = a`. XOR is commutative and associative, so order doesn't matter — all pairs cancel out.

---

### Problem 4: Counting Set Bits (Medium) — LeetCode 191

**Problem**: Return the number of `1` bits in the binary representation of a non-negative integer.

```python
def count_ones(n: int) -> int:
    """Count set bits using Brian Kernighan's algorithm.

    n & (n - 1) clears the lowest set bit each iteration,
    so we loop exactly once per set bit.

    >>> count_ones(11)  # 1011 -> 3 set bits
    3
    >>> count_ones(128) # 10000000 -> 1 set bit
    1
    >>> count_ones(0)
    0
    """
    count: int = 0
    while n:
        n &= n - 1
        count += 1
    return count
```

**Key insight**: `n & (n - 1)` removes exactly one set bit per iteration. This is O(k) where k is the number of set bits — much better than checking all 32 positions.

---

### Problem 5: Reverse Bits (Medium) — LeetCode 190

**Problem**: Reverse the bits of a 32-bit unsigned integer.

```python
def reverse_bits(n: int) -> int:
    """Reverse bits of a 32-bit unsigned integer.

    Extract each bit from the right of n and build the result
    from the left.

    >>> reverse_bits(0b00000010100101000001111010011100)
    964176192
    >>> bin(reverse_bits(0b00000010100101000001111010011100))
    '0b111001011110000010100101000000'
    >>> reverse_bits(0)
    0
    """
    result: int = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```

**Key insight**: Extract bits from the right side of `n` one at a time and push them onto the left side of `result`.

---

### Problem 6: Missing Number (Medium) — LeetCode 268

**Problem**: Given an array containing `n` distinct numbers from `0` to `n`, find the missing one. O(1) space required.

```python
def missing_number(nums: list[int]) -> int:
    """Find the missing number in [0, n] using XOR.

    XOR all numbers 0..n with all numbers in the array.
    Every number that appears in both cancels out, leaving the missing one.

    >>> missing_number([3, 0, 1])
    2
    >>> missing_number([0, 1])
    2
    >>> missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1])
    8
    """
    n: int = len(nums)
    xor_all: int = 0

    for i in range(n + 1):
        xor_all ^= i
    for num in nums:
        xor_all ^= num

    return xor_all
```

**Key insight**: XOR the expected range `[0, n]` with the actual array. Pairs cancel, leaving the missing number. This avoids the sum formula approach which can overflow in fixed-width languages.

---

### Problem 7: Sum of Two Integers Without `+` or `-` (Hard) — LeetCode 371

**Problem**: Calculate the sum of two integers without using `+` or `-`.

```python
def get_sum(a: int, b: int) -> int:
    """Add two integers using only bitwise operations.

    XOR gives the sum without carries. AND shifted left gives the carries.
    Repeat until there are no more carries.

    Python integers are arbitrary-width, so we mask to 32 bits to simulate
    fixed-width overflow and handle negative results.

    >>> get_sum(1, 2)
    3
    >>> get_sum(-1, 1)
    0
    >>> get_sum(-12, -8)
    -20
    """
    MASK: int = 0xFFFFFFFF      # 32-bit mask
    MAX_INT: int = 0x7FFFFFFF   # Max positive 32-bit signed int

    # Mask both inputs to 32-bit two's complement
    a &= MASK
    b &= MASK

    while b:
        carry: int = (a & b) << 1 & MASK
        a = (a ^ b)
        b = carry

    # If the sign bit (bit 31) is set, convert from unsigned to signed
    return a if a <= MAX_INT else ~(a ^ MASK)
```

**Key insight**: Binary addition is `XOR` (sum without carry) + `AND << 1` (carry). Repeat until no carry remains. The 32-bit masking is essential in Python because Python integers have unlimited width.

---

### Problem 8: Single Number III (Hard) — LeetCode 260

**Problem**: Two elements appear once, all others appear twice. Find both in O(n) time, O(1) space.

```python
def single_number_iii(nums: list[int]) -> list[int]:
    """Find two elements that appear exactly once.

    1. XOR all elements -> gives xor of the two unique numbers (a ^ b).
    2. Find any set bit in (a ^ b) — this bit differs between a and b.
    3. Partition all numbers by that bit and XOR each group separately.
       Each group contains exactly one unique number.

    >>> sorted(single_number_iii([1, 2, 1, 3, 2, 5]))
    [3, 5]
    >>> sorted(single_number_iii([-1, 0]))
    [-1, 0]
    """
    # Step 1: XOR everything to get a ^ b
    xor_all: int = 0
    for num in nums:
        xor_all ^= num

    # Step 2: Isolate any differing bit (use the lowest set bit)
    diff_bit: int = xor_all & (-xor_all)

    # Step 3: Partition and XOR each group
    group_a: int = 0
    group_b: int = 0
    for num in nums:
        if num & diff_bit:
            group_a ^= num
        else:
            group_b ^= num

    return [group_a, group_b]
```

**Key insight**: After XOR-ing everything, you know which bits differ between the two unique numbers. Use any differing bit to split all numbers into two groups — each group contains exactly one unique number plus pairs that cancel out.

---

## Start: [01-binary-basics.md](./01-binary-basics.md)

Begin with understanding binary representation and the fundamental bitwise operators.
