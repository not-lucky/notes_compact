# Binary Basics

> **Prerequisites:** None (foundational topic)

## Interview Context

Understanding binary representation and bitwise operators is fundamental to all bit manipulation problems. Interviewers expect you to know these basics cold -- they're the building blocks for more complex bit manipulation techniques.

---

## Building Intuition

**Why Binary Matters for Programming**

Every piece of data in a computer -- numbers, text, images, code -- is ultimately stored as binary: sequences of 0s and 1s. Understanding binary isn't just academic; it's the language your computer actually speaks.

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

- **AND**: "Are BOTH bits 1?" -- Used for masking (extracting specific bits)
- **OR**: "Is AT LEAST ONE bit 1?" -- Used for setting bits
- **XOR**: "Are the bits DIFFERENT?" -- Used for toggling and finding uniqueness

```
Think of AND as an "intersection" — keeps only what's in both
Think of OR as a "union" — includes everything from either
Think of XOR as a "difference detector" — marks where they disagree
```

**Why XOR is Special**

XOR has a property no other bitwise operator has: it's its own inverse.

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
count = n.bit_length()     # For finding highest bit position

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

## Two's Complement

Two's complement is how computers represent negative integers. Understanding it is essential for interviews involving negative numbers and bitwise NOT.

### How It Works

For an N-bit number, the most significant bit (MSB) is the **sign bit**:
- `0` in the MSB means positive (or zero)
- `1` in the MSB means negative

To negate a number in two's complement: **flip all bits, then add 1**.

```
Example with 8 bits:

 5 in binary:  0000 0101
 Flip all bits: 1111 1010
 Add 1:         1111 1011  = -5

Verify: 0000 0101 + 1111 1011 = 1 0000 0000  (overflow discarded = 0) ✓
```

### Range of N-bit Two's Complement

```
N bits can represent: -2^(N-1) to 2^(N-1) - 1

 8-bit:  -128 to 127
16-bit:  -32,768 to 32,767
32-bit:  -2,147,483,648 to 2,147,483,647
```

### Key Properties

```
 0 =  0000 0000
-1 =  1111 1111   (all ones)
-2 =  1111 1110
 1 =  0000 0001

Negation: -x = ~x + 1
Identity: x + (~x) = -1  (all ones)
```

### Two's Complement in Python

Python integers have arbitrary precision (no fixed bit width), so two's complement works differently than in C/Java. For interview problems that assume 32-bit integers, use a mask:

```python
MASK_32 = 0xFFFFFFFF       # 32 ones: keeps only the lower 32 bits
MAX_INT_32 = 0x7FFFFFFF    # largest positive 32-bit int: 2^31 - 1

def to_twos_complement_32(n: int) -> int:
    """Convert a Python int to its 32-bit two's complement value."""
    return n & MASK_32

def from_twos_complement_32(n: int) -> int:
    """Interpret a 32-bit two's complement value as a signed Python int."""
    if n > MAX_INT_32:
        # Sign bit is set, so this is a negative number
        return n - (1 << 32)
    return n

# Examples
print(to_twos_complement_32(5))     # 5
print(to_twos_complement_32(-5))    # 4294967291 (0xFFFFFFFB)
print(from_twos_complement_32(4294967291))  # -5
```

---

## Bitwise Operators

### AND (`&`)

Returns 1 only if **both** bits are 1.

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
- Check even/odd: (n & 1) == 0 means even
```

### OR (`|`)

Returns 1 if **either** (or both) bits are 1.

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

Returns 1 if the bits **differ**.

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
- a ^ a = 0      (self-cancellation)
- a ^ 0 = a      (identity)
- a ^ b = b ^ a  (commutative)
- (a ^ b) ^ c = a ^ (b ^ c)  (associative)

Use cases:
- Find single number among pairs
- Toggle bits
- Swap without temp variable
```

### NOT (`~`)

Flips all bits (bitwise complement).

```
    ~ 0 1 0 1  (5)
    ---------
      1 0 1 0  (-6 in two's complement)

In Python, ~n = -(n + 1):
  ~5    = -6
  ~0    = -1
  ~(-1) = 0
  ~(-6) = 5

Why -(n+1)? Because n + ~n = all 1s = -1, so ~n = -1 - n = -(n+1).
```

### Left Shift (`<<`)

Shifts bits left, filling with 0s. Equivalent to multiplying by 2^k.

```
    5 << 1:
    0101 << 1 = 1010 (10)    # 5 * 2 = 10

    5 << 2:
    0101 << 2 = 10100 (20)   # 5 * 4 = 20

    In general: n << k = n × 2^k
```

### Right Shift (`>>`)

Shifts bits right, discarding the lowest bits. Equivalent to floor division by 2^k.

```
    20 >> 1:
    10100 >> 1 = 1010 (10)   # 20 // 2 = 10

    20 >> 2:
    10100 >> 2 = 101 (5)     # 20 // 4 = 5

    In general: n >> k = n // 2^k  (floor division)

Note: For negative numbers, Python uses arithmetic right shift
(the sign bit is preserved, so negative numbers stay negative).
    -8 >> 1 = -4
    -7 >> 1 = -4  (floors toward negative infinity)
```

---

## Python 3 Binary Utilities

Python 3 has excellent built-in support for binary operations. Know these for interviews:

```python
n = 45

# --- Viewing binary ---
bin(n)                   # '0b101101'
bin(n)[2:]               # '101101'  (strip the '0b' prefix)
format(n, 'b')           # '101101'  (cleaner way to strip prefix)
format(n, '08b')         # '00101101' (zero-padded to 8 bits)
f"{n:b}"                 # '101101'  (f-string shorthand)
f"{n:08b}"               # '00101101' (f-string with padding)

# --- Parsing binary ---
int('101101', 2)         # 45
int('0b101101', 0)       # 45 (auto-detect base from prefix)

# --- Useful methods ---
n.bit_length()           # 6 (number of bits needed, excluding sign and leading zeros)
(0).bit_length()         # 0

# Python 3.10+:
n.bit_count()            # 4 (number of set bits / popcount) -- same as bin(n).count('1')
```

---

## Implementation

### Basic Bit Operations

```python
def get_bit(n: int, i: int) -> bool:
    """
    Get the value of bit at position i (0-indexed from right).

    Example: get_bit(0b1010, 1) -> True  (bit 1 is '1')
             get_bit(0b1010, 2) -> False (bit 2 is '0')

    Time: O(1)
    Space: O(1)
    """
    return (n & (1 << i)) != 0


def set_bit(n: int, i: int) -> int:
    """
    Set bit at position i to 1.

    Example: set_bit(0b1010, 0) -> 0b1011

    Time: O(1)
    Space: O(1)
    """
    return n | (1 << i)


def clear_bit(n: int, i: int) -> int:
    """
    Clear bit at position i (set to 0).

    Example: clear_bit(0b1010, 3) -> 0b0010

    Time: O(1)
    Space: O(1)
    """
    return n & ~(1 << i)


def toggle_bit(n: int, i: int) -> int:
    """
    Toggle bit at position i (0 -> 1 or 1 -> 0).

    Example: toggle_bit(0b1010, 1) -> 0b1000

    Time: O(1)
    Space: O(1)
    """
    return n ^ (1 << i)


def update_bit(n: int, i: int, value: bool) -> int:
    """
    Update bit at position i to given value (0 or 1).

    Example: update_bit(0b1010, 0, True) -> 0b1011

    Time: O(1)
    Space: O(1)
    """
    # Clear the bit first, then set if value is True
    cleared = n & ~(1 << i)
    return cleared | (int(value) << i)


# --- Demonstrations ---
n = 0b1010  # 10 in decimal

print(f"n = {n} = {bin(n)}")                       # n = 10 = 0b1010
print(f"bit 1: {get_bit(n, 1)}")                   # True  (bit 1 of 1010 is 1)
print(f"bit 2: {get_bit(n, 2)}")                   # False (bit 2 of 1010 is 0)
print(f"set bit 0: {bin(set_bit(n, 0))}")          # 0b1011
print(f"clear bit 3: {bin(clear_bit(n, 3))}")      # 0b10
print(f"toggle bit 1: {bin(toggle_bit(n, 1))}")    # 0b1000
```

### Conversion Utilities

```python
def decimal_to_binary(n: int) -> str:
    """
    Convert decimal to binary string representation.
    Handles 0 and negative numbers (shows negative sign, not two's complement).

    Time: O(log n)
    Space: O(log n)
    """
    if n == 0:
        return "0"

    is_negative = n < 0
    n = abs(n)
    result = []

    while n:
        result.append(str(n & 1))  # Extract least significant bit
        n >>= 1                    # Shift right to process next bit

    binary = ''.join(reversed(result))
    return f"-{binary}" if is_negative else binary


def binary_to_decimal(s: str) -> int:
    """
    Convert binary string to decimal integer.
    Handles optional leading '-' for negative numbers.

    Time: O(n) where n is string length
    Space: O(1)
    """
    if not s:
        return 0

    is_negative = s[0] == '-'
    digits = s[1:] if is_negative else s

    result = 0
    for char in digits:
        result = (result << 1) | (1 if char == '1' else 0)

    return -result if is_negative else result


# Python built-ins (preferred in interviews for speed)
n = 45
print(bin(n))            # '0b101101'
print(format(n, 'b'))    # '101101' (no prefix)
print(int('101101', 2))  # 45
```

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
# Odd numbers always have LSB = 1:  5 = 101, 7 = 111, 3 = 11
# Even numbers always have LSB = 0: 4 = 100, 6 = 110, 8 = 1000
```

### 2. Swap Without Temp Variable

```python
def swap(a: int, b: int) -> tuple[int, int]:
    """Swap two numbers using XOR (no temporary variable)."""
    a ^= b  # a now holds a ^ b
    b ^= a  # b = b ^ (a ^ b) = original a
    a ^= b  # a = (a ^ b) ^ original a = original b
    return a, b

# Example
x, y = 5, 10
x, y = swap(x, y)
print(x, y)  # 10, 5

# Caution: XOR swap fails when swapping the SAME memory location.
# This matters in-place with arrays -- never use it when i == j:
#   arr[i] ^= arr[j]  # if i == j, this zeroes arr[i]!
# In Python, just use: a, b = b, a (or arr[i], arr[j] = arr[j], arr[i])
# XOR swap is mainly for interviews and low-level programming.
```

### 3. Isolate the Rightmost Set Bit

```python
def rightmost_set_bit(n: int) -> int:
    """
    Isolate the lowest (rightmost) set bit.

    Example: n = 12 (1100) -> returns 4 (0100)

    Why it works: -n is two's complement (~n + 1).
    n & -n keeps only the lowest set bit because all lower bits
    flip between n and -n, but the lowest set bit stays the same.
    """
    return n & (-n)

print(rightmost_set_bit(12))  # 4  (1100 -> 0100)
print(rightmost_set_bit(10))  # 2  (1010 -> 0010)
print(rightmost_set_bit(8))   # 8  (1000 -> 1000)
```

### 4. Remove the Rightmost Set Bit

```python
def clear_rightmost_set_bit(n: int) -> int:
    """
    Turn off the lowest (rightmost) set bit.

    Example: n = 12 (1100) -> returns 8 (1000)

    Why it works: (n-1) flips the rightmost set bit and all bits below it.
    AND-ing with n clears the rightmost set bit.
    """
    return n & (n - 1)

print(clear_rightmost_set_bit(12))  # 8  (1100 -> 1000)
print(clear_rightmost_set_bit(10))  # 8  (1010 -> 1000)
print(clear_rightmost_set_bit(7))   # 6  (0111 -> 0110)
```

### 5. Check if Power of Two

```python
def is_power_of_two(n: int) -> bool:
    """
    Check if n is a power of 2.

    Powers of 2 have exactly one set bit: 1, 10, 100, 1000, ...
    n & (n - 1) clears the rightmost set bit.
    If the result is 0, there was only one set bit -> power of 2.
    """
    return n > 0 and (n & (n - 1)) == 0

print(is_power_of_two(8))   # True  (1000)
print(is_power_of_two(6))   # False (0110)
print(is_power_of_two(1))   # True  (0001)
print(is_power_of_two(0))   # False
```

### 6. Sign of Number

```python
def sign(n: int) -> int:
    """Return 1 for positive, -1 for negative, 0 for zero."""
    if n == 0:
        return 0
    return -1 if n < 0 else 1

# For 32-bit integers specifically:
def is_negative_32bit(n: int) -> bool:
    """Check if bit 31 (sign bit) is set in a 32-bit integer."""
    return (n >> 31) & 1 == 1
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
def add_binary(a: str, b: str) -> str:
    """
    Add two binary strings using grade-school addition (right to left with carry).

    Time: O(max(m, n)) where m, n are string lengths
    Space: O(max(m, n)) for the result
    """
    result = []
    carry = 0
    i, j = len(a) - 1, len(b) - 1

    while i >= 0 or j >= 0 or carry:
        # Get current digits (0 if index is out of bounds)
        digit_a = int(a[i]) if i >= 0 else 0
        digit_b = int(b[j]) if j >= 0 else 0

        # Sum the two digits plus carry
        total = digit_a + digit_b + carry
        result.append(str(total % 2))  # Current bit: 0 or 1
        carry = total // 2             # Carry: 0 or 1

        i -= 1
        j -= 1

    return ''.join(reversed(result))


# Alternative: Use Python built-ins (mention as a one-liner, but explain the above)
def add_binary_pythonic(a: str, b: str) -> str:
    return bin(int(a, 2) + int(b, 2))[2:]


# Test
print(add_binary("11", "1"))       # "100"
print(add_binary("1010", "1011"))  # "10101"
```

---

## Problem: Number Complement

**LeetCode 476**: Given a positive integer, return its complement number. The complement flips all bits in the binary representation (only the significant bits, not leading zeros).

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
def find_complement(num: int) -> int:
    """
    Find the complement of a number (flip all significant bits).

    Key insight: XOR with a mask of all 1s flips every bit.
    We build a mask the same width as num's binary representation.

    Example: num = 5 (101)
             mask = 111 (7)
             101 ^ 111 = 010 = 2

    Time: O(log n) - need to find bit length
    Space: O(1)
    """
    if num == 0:
        return 1

    # Create a mask with all 1s of the same bit-length as num
    # e.g., if num = 5 (101, 3 bits), mask = 111 (7)
    mask = (1 << num.bit_length()) - 1

    # XOR with mask flips all significant bits
    return num ^ mask


# Alternative: Build mask iteratively
def find_complement_v2(num: int) -> int:
    mask = 1
    while mask <= num:
        mask <<= 1
    return (mask - 1) ^ num


# Test
print(find_complement(5))   # 2  (101 -> 010)
print(find_complement(7))   # 0  (111 -> 000)
print(find_complement(10))  # 5  (1010 -> 0101)
```

---

## Complexity Analysis

| Operation        | Time     | Space    | Notes              |
| ---------------- | -------- | -------- | ------------------ |
| Get bit          | O(1)     | O(1)     | Single AND + shift |
| Set bit          | O(1)     | O(1)     | Single OR + shift  |
| Clear bit        | O(1)     | O(1)     | AND with NOT       |
| Toggle bit       | O(1)     | O(1)     | Single XOR + shift |
| NOT              | O(1)     | O(1)     | Single NOT         |
| Left/Right shift | O(1)     | O(1)     | Single shift       |
| Decimal <-> Binary | O(log n) | O(log n) | Process each bit |

---

## Edge Cases

1. **Zero**: `bin(0)` = `'0b0'`, many formulas need special handling (e.g., `bit_length()` returns 0)
2. **Negative numbers**: Python uses arbitrary precision, no fixed bit width. Use `& 0xFFFFFFFF` to simulate 32-bit behavior.
3. **Overflow**: Python integers never overflow, but interview problems often assume 32-bit. Mask with `0xFFFFFFFF` and handle sign conversion.
4. **Large numbers**: Python handles arbitrarily large integers natively.
5. **Empty/invalid strings**: Handle in binary string problems.
6. **Leading zeros**: May or may not be significant depending on the problem.

---

## Interview Tips

1. **Operator precedence awareness**: In **C/Java**, bitwise operators have **lower** precedence than comparison operators -- a classic trap:
   ```c
   // C/Java TRAP:
   // n & 1 == 0  is parsed as  n & (1 == 0)  -- WRONG!
   // (n & 1) == 0  is the intended check
   ```
   **Python gets this right**: `&`, `^`, `|` bind tighter than `==` in Python, so `n & 1 == 0` correctly parses as `(n & 1) == 0`. Still, adding parentheses is good practice for clarity and cross-language consistency:
   ```python
   (n & 1) == 0  # Always parenthesize for clarity
   ```

2. **Know `bit_length()`**: Returns the number of bits needed to represent the number (excluding sign and leading zeros).
   ```python
   (5).bit_length()   # 3  (5 = 101)
   (0).bit_length()   # 0
   (1).bit_length()   # 1
   ```

3. **Use `bin()` for debugging**: Quick way to visualize what's happening.
   ```python
   bin(5)       # '0b101'
   f"{5:08b}"   # '00000101' (padded, no prefix)
   ```

4. **Mention time/space**: All basic bit operations are O(1).

5. **Draw it out**: Binary visualization on paper helps avoid off-by-one errors in bit positions.

6. **32-bit mask**: When a problem says "32-bit integer", always apply `& 0xFFFFFFFF` to constrain results.

---

## Practice Problems

### Easy: Count Set Bits (Hamming Weight)

**LeetCode 191**: See [03-counting-bits.md](./03-counting-bits.md) for full solution and multiple approaches (iterate, Brian Kernighan, lookup table, built-in).

---

### Easy: Reverse Bits

**LeetCode 190**: See [06-bit-manipulation-tricks.md](./06-bit-manipulation-tricks.md) (Trick 7) for full solution including a divide-and-conquer variant.

---

### Easy: Convert Binary Number in a Linked List to Integer

**LeetCode 1290**: Given a singly linked list where each node contains a binary digit (0 or 1), return the decimal value.

```python
class ListNode:
    def __init__(self, val: int = 0, next_node: "ListNode | None" = None):
        self.val = val
        self.next = next_node

def get_decimal_value(head: ListNode) -> int:
    """
    Convert binary linked list to decimal integer.

    Approach: Traverse the list. For each node, shift the accumulated
    result left by 1 (multiply by 2) and OR in the current bit.

    Time: O(n) where n is the number of nodes
    Space: O(1)
    """
    result = 0
    current = head
    while current:
        result = (result << 1) | current.val
        current = current.next
    return result

# Test: List representing 101 (binary) = 5
node3 = ListNode(1)
node2 = ListNode(0, node3)
node1 = ListNode(1, node2)
print(get_decimal_value(node1))  # 5
```

---

### Medium: Single Number (XOR Application)

**LeetCode 136**: See [02-single-number.md](./02-single-number.md) for full solution. Key idea: XOR all elements — pairs cancel to 0, leaving the unique element.

---

### Medium: Hamming Distance

**LeetCode 461**: See [03-counting-bits.md](./03-counting-bits.md) for full solution. Key idea: XOR the two numbers, then count set bits (Brian Kernighan's trick).

---

### Medium: Concatenation of Consecutive Binary Numbers

**LeetCode 1680**: Given an integer `n`, return the decimal value of the binary string formed by concatenating the binary representations of 1 to n in order, modulo 10^9 + 7.

```python
def concatenated_binary(n: int) -> int:
    """
    Concatenate binary of 1, 2, ..., n and return decimal value mod 10^9+7.

    Example: n=3 -> "1" + "10" + "11" = "11011" = 27

    Approach: For each number i, shift the accumulated result left by
    the bit-length of i, then OR in i.

    Time: O(n log n)
    Space: O(1)
    """
    MOD = 10**9 + 7
    result = 0

    for i in range(1, n + 1):
        bit_len = i.bit_length()
        result = ((result << bit_len) | i) % MOD

    return result

# Test
print(concatenated_binary(1))   # 1   ("1" = 1)
print(concatenated_binary(3))   # 27  ("11011" = 27)
print(concatenated_binary(12))  # 505379714
```

---

### Hard: Maximum XOR of Two Numbers in an Array

**LeetCode 421**: See [05-xor-tricks.md](./05-xor-tricks.md) for full solution. Key idea: build the answer bit-by-bit from MSB down, using prefix sets to greedily set each bit.

---

### Easy: Missing Number

**LeetCode 268**: See [02-single-number.md](./02-single-number.md) for full solution. Key idea: XOR all indices 0..n with all values — the missing number is the only unpaired value.

---

### Medium: Counting Bits

**LeetCode 338**: See [03-counting-bits.md](./03-counting-bits.md) for full solution. Key idea: DP using `ans[i] = ans[i & (i-1)] + 1` — the count for `i` is one more than the count with its lowest set bit cleared.

---

## Related Sections

- [Single Number](./02-single-number.md) - XOR applications
- [Counting Bits](./03-counting-bits.md) - Counting set bits
- [Power of Two](./04-power-of-two.md) - Power of two checks
- [XOR Tricks](./05-xor-tricks.md) - Advanced XOR techniques
