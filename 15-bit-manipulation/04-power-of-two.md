# Power of Two

> **Prerequisites:** [Binary Basics](./01-binary-basics.md), [Counting Bits](./03-counting-bits.md)

## Interview Context

Power of two checks are common interview questions because they have an elegant O(1) bit manipulation solution. These problems test whether you understand binary representation and can recognize patterns. Mastery of the `n & (n-1)` trick also unlocks several related problems (power of four, counting set bits, isolating bits).

---

## Building Intuition

### Why Powers of Two Are Special in Binary

In decimal, powers of 10 look clean: 10, 100, 1000... They're a 1 followed by zeros.

In binary, powers of 2 have the exact same property — a single 1-bit followed by zeros:

```
Decimal  Binary     Set bits
──────── ────────── ────────
2⁰ =  1    0001     1 bit
2¹ =  2    0010     1 bit
2² =  4    0100     1 bit
2³ =  8    1000     1 bit
2⁴ = 16   10000     1 bit

Non-powers of 2:
3  = 0011  (two 1-bits)
5  = 0101  (two 1-bits)
6  = 0110  (two 1-bits)
7  = 0111  (three 1-bits)
```

**Key insight:** A positive integer is a power of two *if and only if* it has exactly one set bit.

### The `n & (n-1)` Trick: Why It Works

The expression `n & (n-1)` clears the lowest (rightmost) set bit of `n`. For powers of two there is only one set bit, so clearing it yields zero.

**Step-by-step trace of subtraction:**

When you compute `n - 1`:
1. Starting from the rightmost bit, every 0-bit must "borrow," flipping to 1.
2. The rightmost 1-bit supplies the borrow and flips to 0.
3. All bits to the left are untouched.

This means `n` and `n-1` share the same bits above the lowest set bit, and differ everywhere else — so their AND zeroes out from that bit down.

```
Power of 2 example (n = 8):
  n     = 1000
  n - 1 = 0111   (the single 1 flips to 0, trailing 0s flip to 1s)
  n & (n-1) = 1000 & 0111 = 0000  →  zero ✓

Non-power of 2 example (n = 6):
  n     = 0110
  n - 1 = 0101   (only the lowest 1-bit and below change)
  n & (n-1) = 0110 & 0101 = 0100  →  nonzero ✗

Another example (n = 16):
  n     = 10000
  n - 1 = 01111
  n & (n-1) = 10000 & 01111 = 00000  →  zero ✓
```

**Edge case:** `n = 0` has no set bits, so `n & (n-1) == 0` is trivially true — but 0 is *not* a power of two. Always guard with `n > 0`.

---

## When NOT to Use Bit Tricks

**1. When the base isn't 2 (or a power of 2)**

The `n & (n-1)` trick relies on the binary representation. It works for powers of 2 and can be extended to powers of 4 (since 4 = 2²). For bases like 3, 5, 10, etc., you need different approaches (modulo, repeated division).

**2. For construction, not just checking**

Finding the *next* power of 2 ≥ n, or the *previous* power of 2 ≤ n, requires building a result — see the practice problems below.

**3. When zero or negative numbers are valid inputs**

`n & (n-1) == 0` is true for `n = 0`. Negative numbers can't be powers of a positive base. Always check `n > 0` first.

**Red flags that bit tricks won't apply directly:**
- Base isn't 2 (or 4, which is 2²)
- You need the next/previous power, not just a check
- The problem is fundamentally about divisibility, not bit patterns

---

## Problem 1: Power of Two (Basic)

**LeetCode 231** · Easy

Given an integer `n`, return `True` if it is a power of two, otherwise return `False`.

### Examples

```
Input: n = 1   → Output: True   (2⁰ = 1)
Input: n = 16  → Output: True   (2⁴ = 16)
Input: n = 3   → Output: False
Input: n = 0   → Output: False
Input: n = -16 → Output: False
```

### Solution

```python
def is_power_of_two(n: int) -> bool:
    """
    A power of 2 has exactly one set bit.
    n & (n-1) clears the lowest set bit.
    If the result is 0, there was only one set bit.

    Guard n > 0 because 0 & (-1) == 0 but 0 is not a power of 2.

    Time:  O(1)
    Space: O(1)
    """
    return n > 0 and (n & (n - 1)) == 0


# Alternative: count set bits directly
def is_power_of_two_popcount(n: int) -> bool:
    """Use Python's bin() to count 1-bits."""
    return n > 0 and bin(n).count('1') == 1


# Tests
assert is_power_of_two(1) is True       # 2^0
assert is_power_of_two(16) is True      # 2^4
assert is_power_of_two(3) is False
assert is_power_of_two(0) is False
assert is_power_of_two(-16) is False
assert is_power_of_two(1024) is True    # 2^10
print("Problem 1: All tests passed")
```

---

## Problem 2: Power of Four

**LeetCode 342** · Easy

Given an integer `n`, return `True` if it is a power of four.

### Intuition

A power of 4 is a power of 2, but with the additional constraint that the single set bit must be at an **even** bit position (0, 2, 4, 6, ...).

```
Powers of 4 (bit at even position):
  4⁰ =  1 = 0000 0001   bit position 0 (even) ✓
  4¹ =  4 = 0000 0100   bit position 2 (even) ✓
  4² = 16 = 0001 0000   bit position 4 (even) ✓
  4³ = 64 = 0100 0000   bit position 6 (even) ✓

Powers of 2 that are NOT powers of 4 (bit at odd position):
  2  = 0000 0010   bit position 1 (odd) ✗
  8  = 0000 1000   bit position 3 (odd) ✗
  32 = 0010 0000   bit position 5 (odd) ✗
```

The mask `0x55555555` has 1s at all even positions:

```
0x55555555 = 01010101 01010101 01010101 01010101
```

If `n` is a power of 2 and `n & 0x55555555 != 0`, the single bit sits at an even position — so `n` is a power of 4.

### Examples

```
Input: n = 16 → Output: True   (4² = 16)
Input: n = 5  → Output: False
Input: n = 1  → Output: True   (4⁰ = 1)
Input: n = 2  → Output: False  (power of 2, but not 4)
```

### Solution

```python
def is_power_of_four(n: int) -> bool:
    """
    Three conditions:
      1. n > 0
      2. n is a power of 2  (single set bit)
      3. That bit is at an even position  (passes the 0x55555555 mask)

    Time:  O(1)
    Space: O(1)
    """
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0


# Alternative: power-of-2 check + modulo trick
# 4 ≡ 1 (mod 3), so 4^k ≡ 1^k ≡ 1 (mod 3) for all k >= 0.
# But 2·4^k ≡ 2 (mod 3), so powers of 2 that aren't powers of 4 fail.
def is_power_of_four_mod(n: int) -> bool:
    """Power of 4 minus 1 is always divisible by 3."""
    return n > 0 and (n & (n - 1)) == 0 and (n - 1) % 3 == 0


# Tests
assert is_power_of_four(1) is True      # 4^0
assert is_power_of_four(4) is True      # 4^1
assert is_power_of_four(16) is True     # 4^2
assert is_power_of_four(64) is True     # 4^3
assert is_power_of_four(2) is False     # power of 2 but not 4
assert is_power_of_four(8) is False     # power of 2 but not 4
assert is_power_of_four(5) is False
assert is_power_of_four(0) is False
print("Problem 2: All tests passed")
```

---

## Problem 3: Power of Three (Why Bit Tricks Don't Apply)

**LeetCode 326** · Easy

Given an integer `n`, return `True` if it is a power of three.

### Why Bits Don't Help Here

3 isn't a power of 2, so its powers don't produce a "single set bit" pattern:

```
3¹ =   3 = 11
3² =   9 = 1001
3³ =  27 = 11011
3⁴ =  81 = 1010001
3⁵ = 243 = 11110011

No clean binary pattern — can't use bit manipulation.
```

### The Number Theory Approach

Since 3 is prime, the only divisors of 3^k are 3^0, 3^1, ..., 3^k.

The largest power of 3 that fits in a 32-bit signed integer is **3¹⁹ = 1,162,261,467**.

Any power of 3 divides 3¹⁹ evenly. No non-power-of-3 can, because 3 is prime and the prime factorisation of 3¹⁹ contains only 3s.

```
3¹⁹ % 1  == 0  ✓  (3⁰)
3¹⁹ % 3  == 0  ✓  (3¹)
3¹⁹ % 27 == 0  ✓  (3³)
3¹⁹ % 6  != 0  ✗  (6 = 2 × 3, factor of 2 doesn't divide 3¹⁹)
3¹⁹ % 45 != 0  ✗  (45 = 3² × 5, factor of 5 doesn't divide 3¹⁹)
```

> **Note:** This trick works because 3 is prime. It would NOT work for, say, power-of-6 because 6 = 2 × 3 is composite, and non-powers like 12 could also divide a power of 6.

### Examples

```
Input: n = 27 → Output: True   (3³)
Input: n = 0  → Output: False
Input: n = 9  → Output: True   (3²)
Input: n = 45 → Output: False
```

### Solution

```python
# Largest power of 3 in a 32-bit signed integer: 3**19 = 1162261467
MAX_POWER_OF_3 = 3**19  # 1162261467

def is_power_of_three(n: int) -> bool:
    """
    If n is a power of 3, it must divide 3^19 evenly.
    Works because 3 is prime.

    Time:  O(1)
    Space: O(1)
    """
    return n > 0 and MAX_POWER_OF_3 % n == 0


# Alternative: repeated division (works for any base)
def is_power_of_three_loop(n: int) -> bool:
    """Divide out all factors of 3; if 1 remains, n was a power of 3."""
    if n <= 0:
        return False
    while n % 3 == 0:
        n //= 3
    return n == 1


# Tests
assert is_power_of_three(1) is True     # 3^0
assert is_power_of_three(9) is True     # 3^2
assert is_power_of_three(27) is True    # 3^3
assert is_power_of_three(45) is False
assert is_power_of_three(0) is False
assert is_power_of_three(-3) is False
print("Problem 3: All tests passed")
```

---

## Problem 4: Every Positive Integer Is a Sum of Powers of Two

This isn't a LeetCode problem, but it's an important conceptual insight.

### Explanation

Every positive integer can be expressed as a sum of distinct powers of 2 — that's exactly what binary representation means.

```
13 = 1101 in binary = 2³ + 2² + 2⁰ = 8 + 4 + 1
25 = 11001 in binary = 2⁴ + 2³ + 2⁰ = 16 + 8 + 1
7  = 111 in binary = 2² + 2¹ + 2⁰ = 4 + 2 + 1
```

So asking "is n a sum of powers of two?" is trivially true for every positive integer. The more interesting question is: **how many** powers of two sum to n? That's just the popcount (number of set bits).

```python
def count_powers_of_two_in_sum(n: int) -> int:
    """
    Every positive integer is a sum of distinct powers of 2.
    The number of terms equals the number of set bits.

    Time:  O(log n) — string conversion is proportional to bit length
    Space: O(log n) — for the binary string
    """
    if n <= 0:
        return 0
    return bin(n).count('1')


# Tests
assert count_powers_of_two_in_sum(13) == 3   # 8 + 4 + 1
assert count_powers_of_two_in_sum(16) == 1   # 16 (itself a power of 2)
assert count_powers_of_two_in_sum(7) == 3    # 4 + 2 + 1
assert count_powers_of_two_in_sum(0) == 0
print("Problem 4: All tests passed")
```

---

## Problem 5: Find the Highest and Lowest Set Bit

These operations come up frequently as sub-problems.

### Lowest Set Bit

The lowest (rightmost) set bit can be isolated with `n & (-n)`.

In two's complement, `-n` is computed as `~n + 1`, which flips all bits then adds 1. The bits below the lowest set bit (all 0s) become 1s after the flip, and the +1 cascades through them, flipping them back to 0 and flipping the lowest set bit itself back to 1. Everything above it gets inverted. So when you AND `n` with `-n`, only the lowest set bit survives.

```
n     = 12 = 1100
-n    =      0100  (two's complement)
n & (-n) =   0100  →  4 (bit position 2)

n     = 10 = 1010
-n    =      0110
n & (-n) =   0010  →  2 (bit position 1)
```

### Highest Set Bit

The highest (leftmost) set bit position is `bit_length() - 1`. To get its value, use `1 << (bit_length() - 1)`.

```python
def lowest_set_bit(n: int) -> int:
    """
    Isolate the lowest set bit of n.
    Returns 0 if n is 0.

    Example: lowest_set_bit(12) → 4 (binary 0100)

    Time:  O(1)
    Space: O(1)
    """
    if n == 0:
        return 0
    return n & (-n)


def highest_set_bit(n: int) -> int:
    """
    Isolate the highest set bit of n.
    Returns 0 if n <= 0.

    Example: highest_set_bit(12) → 8 (binary 1000)

    Time:  O(1)
    Space: O(1)
    """
    if n <= 0:
        return 0
    return 1 << (n.bit_length() - 1)


def lowest_set_bit_position(n: int) -> int:
    """Return the 0-indexed position of the lowest set bit, or -1 if n == 0."""
    if n == 0:
        return -1
    return (n & -n).bit_length() - 1


def highest_set_bit_position(n: int) -> int:
    """Return the 0-indexed position of the highest set bit, or -1 if n <= 0."""
    if n <= 0:
        return -1
    return n.bit_length() - 1


# Tests
assert lowest_set_bit(12) == 4       # 1100 → 0100
assert lowest_set_bit(10) == 2       # 1010 → 0010
assert lowest_set_bit(8) == 8        # 1000 → 1000
assert lowest_set_bit(0) == 0

assert highest_set_bit(12) == 8      # 1100 → 1000
assert highest_set_bit(10) == 8      # 1010 → 1000
assert highest_set_bit(1) == 1
assert highest_set_bit(0) == 0

assert lowest_set_bit_position(12) == 2
assert highest_set_bit_position(12) == 3
print("Problem 5: All tests passed")
```

---

## Problem 6: Round Up to Next Power of Two

Given a positive integer `n`, find the smallest power of 2 that is ≥ n.

### Intuition

The idea is to "smear" the highest set bit rightward until all lower bits are 1, then add 1.

```
n = 13 = 01101
Step 0: subtract 1       → 01100
Step 1: n |= n >> 1      → 01110
Step 2: n |= n >> 2      → 01111
Step 3: n |= n >> 4      → 01111  (no change, bits already filled)
Step 4: add 1             → 10000 = 16 ✓
```

We subtract 1 first so that if `n` is already a power of 2, it maps to itself (e.g., 8 → 7 → 7 → 8).

### Solution

```python
def next_power_of_two(n: int) -> int:
    """
    Find the smallest power of 2 >= n.

    Algorithm:
      1. Subtract 1 (so exact powers of 2 stay put)
      2. Smear the highest bit rightward to fill all lower bits
      3. Add 1 to get the next power of 2

    The 5 shifts (1, 2, 4, 8, 16) handle up to 32-bit integers.
    For 64-bit, add: n |= n >> 32

    Note: Python integers have arbitrary precision, so the bit-smearing
    approach is mainly useful in fixed-width languages (C/C++/Java).
    The bit_length() alternative below is idiomatic Python and works
    for any size.

    Time:  O(1)  (fixed number of operations)
    Space: O(1)
    """
    if n <= 1:
        return 1
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    # For 64-bit integers, uncomment:
    # n |= n >> 32
    return n + 1


# Python alternative using bit_length (simpler)
def next_power_of_two_simple(n: int) -> int:
    """Use bit_length to find the position, then shift."""
    if n <= 1:
        return 1
    return 1 << (n - 1).bit_length()


# Tests
assert next_power_of_two(1) == 1
assert next_power_of_two(2) == 2
assert next_power_of_two(3) == 4
assert next_power_of_two(5) == 8
assert next_power_of_two(8) == 8     # already a power of 2
assert next_power_of_two(17) == 32
assert next_power_of_two(0) == 1
assert next_power_of_two(-5) == 1
print("Problem 6: All tests passed")
```

---

## Problem 7: Previous Power of Two

Given a positive integer `n`, find the largest power of 2 that is ≤ n.

### Solution

```python
def prev_power_of_two(n: int) -> int:
    """
    Find the largest power of 2 <= n.

    Smear the highest bit rightward, then shift right and add 1
    to isolate just the highest bit.

    Time:  O(1)
    Space: O(1)
    """
    if n <= 0:
        return 0
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    return (n + 1) >> 1


# Python alternative using bit_length
def prev_power_of_two_simple(n: int) -> int:
    """Use bit_length to find the highest set bit position."""
    if n <= 0:
        return 0
    return 1 << (n.bit_length() - 1)


# Tests
assert prev_power_of_two(5) == 4
assert prev_power_of_two(8) == 8     # already a power of 2
assert prev_power_of_two(17) == 16
assert prev_power_of_two(1) == 1
assert prev_power_of_two(0) == 0
print("Problem 7: All tests passed")
```

---

## Problem 8: Log Base 2

Floor and ceiling of log₂ are useful for determining how many bits are needed, tree heights, and divide-and-conquer analysis.

### Solution

```python
def log2_floor(n: int) -> int:
    """
    Floor of log base 2 = position of the highest set bit.
    Returns -1 for n <= 0 (undefined).

    Time:  O(1) using Python's bit_length()
    Space: O(1)
    """
    if n <= 0:
        return -1
    return n.bit_length() - 1


def log2_ceil(n: int) -> int:
    """
    Ceiling of log base 2.
    Returns -1 for n <= 0 (undefined).

    If n is a power of 2, ceil == floor.
    Otherwise, ceil == floor + 1.

    Time:  O(1)
    Space: O(1)
    """
    if n <= 0:
        return -1
    result = n.bit_length() - 1
    # If n is not a power of 2, round up
    if n & (n - 1) != 0:
        result += 1
    return result


# Tests
assert log2_floor(1) == 0
assert log2_floor(8) == 3
assert log2_floor(10) == 3
assert log2_floor(16) == 4

assert log2_ceil(1) == 0
assert log2_ceil(8) == 3     # exact power of 2
assert log2_ceil(10) == 4    # between 8 and 16
assert log2_ceil(16) == 4
print("Problem 8: All tests passed")
```

---

## Problem 9: Bitwise AND of Numbers Range

**LeetCode 201** · Medium

Given two integers `left` and `right`, return the bitwise AND of all numbers in `[left, right]`.

### Intuition

When you AND all numbers in a range, any bit position that changes value at least once becomes 0. Only the **common prefix** — the leftmost bits where `left` and `right` agree — survives.

```
Range [5, 7]:
  5 = 101
  6 = 110
  7 = 111

Bit 2: 1, 1, 1  →  stays 1  (common prefix)
Bit 1: 0, 1, 1  →  varies   →  AND gives 0
Bit 0: 1, 0, 1  →  varies   →  AND gives 0

Result: 100 = 4
```

**Algorithm:** Shift both `left` and `right` right until they are equal (stripping off the differing suffix), then shift the common value back left.

### Examples

```
Input: left = 5, right = 7  → Output: 4
Input: left = 0, right = 0  → Output: 0
Input: left = 1, right = 2147483647 → Output: 0
```

### Solution

```python
def range_bitwise_and(left: int, right: int) -> int:
    """
    Find the common prefix of left and right in binary.

    Shift both right until they match, counting shifts.
    Then shift the common value back left.

    Time:  O(log n) where n is the value of right
    Space: O(1)
    """
    shift = 0
    while left < right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift


# Alternative: repeatedly clear the lowest set bit of right
def range_bitwise_and_v2(left: int, right: int) -> int:
    """
    Clear rightmost bit of right until right <= left.
    At that point, right IS the common prefix.

    Each n & (n-1) removes one bit, so this is also O(log n).
    """
    while right > left:
        right &= right - 1
    return right


# Trace for left=5, right=7:
#   shift=0: left=5(101), right=7(111)  →  5 < 7
#   shift=1: left=2(10),  right=3(11)   →  2 < 3
#   shift=2: left=1(1),   right=1(1)    →  equal, stop
#   return 1 << 2 = 4

# Tests
assert range_bitwise_and(5, 7) == 4
assert range_bitwise_and(0, 0) == 0
assert range_bitwise_and(1, 2147483647) == 0
assert range_bitwise_and(6, 7) == 6       # 110 & 111 = 110
assert range_bitwise_and(4, 4) == 4       # single element range
print("Problem 9: All tests passed")
```

---

## Complexity Summary

| Problem                     | Time     | Space    | Technique                          |
| --------------------------- | -------- | -------- | ---------------------------------- |
| Power of Two                | O(1)     | O(1)     | `n & (n-1) == 0`                  |
| Power of Four               | O(1)     | O(1)     | Power of 2 + even-position mask   |
| Power of Three              | O(1)     | O(1)     | Modulo by max power of 3          |
| Sum of Powers of Two        | O(log n) | O(log n) | Always true; count = popcount     |
| Highest / Lowest Set Bit    | O(1)     | O(1)     | `bit_length()` / `n & (-n)`       |
| Next Power of Two           | O(1)     | O(1)     | Bit smearing + add 1              |
| Previous Power of Two       | O(1)     | O(1)     | Bit smearing + shift              |
| Log Base 2                  | O(1)     | O(1)     | `bit_length() - 1`               |
| Bitwise AND of Range        | O(log n) | O(1)     | Common prefix via right-shifting  |

---

## Edge Cases

1. **Zero**: Not a power of any positive integer. Always check `n > 0`.
2. **One**: Power of every base (n⁰ = 1 for any n).
3. **Negative numbers**: Not powers of positive bases. The `n > 0` guard handles this.
4. **Large numbers**: Python integers have arbitrary precision, so no overflow concerns in Python. In languages with fixed-width integers, watch for overflow in `next_power_of_two`.
5. **Range where left == right**: Result is `left` (or `right`); the loop never executes.

---

## Interview Tips

1. **Know `n & (n-1)` cold.** It clears the lowest set bit. For power-of-2, that makes the result zero.
2. **Explain the binary insight.** Interviewers want to see understanding, not memorized formulas. Walk through the subtraction mechanics.
3. **Handle edge cases first.** Check `n > 0` before any bit operation. Mention 0 and negative numbers proactively.
4. **Know the 0x55555555 mask** for power-of-4. It shows depth of bit manipulation knowledge.
5. **Explain why power-of-3 is different.** 3 isn't a power of 2, so bits don't help. The modulo trick works because 3 is prime.
6. **Know `n & (-n)`** for isolating the lowest set bit — it comes up in Fenwick trees and many other problems.

---

## Practice Problems

| #   | Problem                      | Difficulty | Key Concept                         | LeetCode |
| --- | ---------------------------- | ---------- | ----------------------------------- | -------- |
| 1   | Power of Two                 | Easy       | `n & (n-1) == 0`                    | 231      |
| 2   | Power of Four                | Easy       | Even-position mask `0x55555555`     | 342      |
| 3   | Power of Three               | Easy       | Modulo by largest power (no bits)   | 326      |
| 4   | Sum of Powers of Two         | Easy       | Binary representation = the answer  | —        |
| 5   | Find Highest / Lowest Bit    | Easy       | `bit_length()`, `n & (-n)`          | —        |
| 6   | Round Up to Next Power of 2  | Medium     | Bit smearing                        | —        |
| 7   | Previous Power of Two        | Medium     | Bit smearing + shift                | —        |
| 8   | Log Base 2 (Floor / Ceiling) | Easy       | `bit_length() - 1`                 | —        |
| 9   | Bitwise AND of Numbers Range | Medium     | Common prefix / right-shift         | 201      |

### Additional Practice

| Problem                              | Difficulty | Key Concept                                   | LeetCode |
| ------------------------------------ | ---------- | --------------------------------------------- | -------- |
| Number of 1 Bits                     | Easy       | `n & (n-1)` to count set bits (Kernighan)     | 191      |
| Minimum Flips to Make a OR b Equal c | Medium     | Per-bit analysis, counting flips needed        | 1318     |
| Divide Two Integers                  | Medium     | Bit shifting to build quotient from powers of 2 | 29     |

---

## Related Sections

- [Binary Basics](./01-binary-basics.md) — Bitwise operators
- [Counting Bits](./03-counting-bits.md) — Popcount techniques
- [Bit Manipulation Tricks](./06-bit-manipulation-tricks.md) — More tricks
