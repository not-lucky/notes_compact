# Counting Bits

> **Prerequisites:** [Binary Basics](./01-binary-basics.md)

## Interview Context

Counting set bits (popcount / Hamming weight) and calculating Hamming distance are
fundamental bit manipulation operations. These problems test your ability to choose
between algorithms of different complexities — knowing when to reach for O(32),
O(k), or O(1) solutions matters in interviews.

---

## Building Intuition

### Why Counting Bits is Fundamental

At the hardware level, processors have dedicated instructions for counting bits
(POPCNT). Understanding this operation conceptually helps you:

- Recognize when bit counting is the right approach
- Choose between O(32), O(k), and O(1) algorithms depending on constraints
- Build dynamic programming solutions for counting bits across a range
- Reduce pairwise problems from O(n²) to O(n) by reasoning per-bit

### The Naive Approach and Its Insight

The simplest way to count bits is to check each position:

```text
n = 13 = 1101₂
Check bit 0: 1101 & 1 = 1    ✓  (set)
Check bit 1: 1101 >> 1 & 1 = 0   (not set)
Check bit 2: 1101 >> 2 & 1 = 1  ✓  (set)
Check bit 3: 1101 >> 3 & 1 = 1  ✓  (set)

Count: 3 set bits
Time: O(log n) — or O(32) for fixed-width 32-bit integers
```

This works by right-shifting n and checking the least significant bit (LSB)
each time. It's O(log n) because the number of bit positions in n is ⌊log₂(n)⌋ + 1.
But if n has only 2 set bits out of 32, we waste 30 iterations on zero bits.

### Brian Kernighan's Brilliant Insight

Instead of checking every bit, what if we could jump directly from one set bit
to the next? That's exactly what `n & (n - 1)` does — it clears the **rightmost**
set bit in one step.

**Why does this work?**

```text
Key property: n & (n - 1) clears the RIGHTMOST set bit

When you subtract 1 from n:
  - The rightmost 1-bit becomes 0
  - All bits to its right (which were 0) become 1
  - All bits to its left stay the same

n     = ...1000   (some prefix, then rightmost 1, then zeros)
n - 1 = ...0111   (same prefix, rightmost 1 flips to 0, trailing 0s flip to 1)
n & (n-1) = ...0000  (rightmost 1 and everything right of it → cleared)
                       (everything left of it → unchanged)

Example with n = 12:
n     = 1100
n - 1 = 1011
n & (n-1) = 1000  ← rightmost set bit (at position 2) cleared!

Now n = 8:
n     = 1000
n - 1 = 0111
n & (n-1) = 0000  ← rightmost set bit (at position 3) cleared, done!

Only 2 iterations for 2 set bits — not 4 for all bit positions.
```

### The DP Insight for Counting Bits Array

When you need to count bits for every number from 0 to n, recomputing each one
individually is wasteful. You've already computed the answer for smaller numbers,
so you can reuse that work.

**Recurrence using last-set-bit removal:**

```text
bits[i] = bits[i & (i - 1)] + 1

Why: i & (i - 1) removes one set bit from i, giving a smaller number
     whose popcount we already know. Adding 1 accounts for the removed bit.

Example:
bits[0] = 0                           (base case)
bits[1] = bits[1 & 0] + 1 = bits[0] + 1 = 1
bits[2] = bits[2 & 1] + 1 = bits[0] + 1 = 1
bits[3] = bits[3 & 2] + 1 = bits[2] + 1 = 2
bits[4] = bits[4 & 3] + 1 = bits[0] + 1 = 1
bits[5] = bits[5 & 4] + 1 = bits[4] + 1 = 2
bits[6] = bits[6 & 5] + 1 = bits[4] + 1 = 2
bits[7] = bits[7 & 6] + 1 = bits[6] + 1 = 3
```

**Alternative recurrence using right-shift:**

```text
bits[i] = bits[i >> 1] + (i & 1)

Why: i >> 1 is i with the LSB dropped. The popcount of i equals the popcount
     of i >> 1 (everything except the LSB), plus 1 if the LSB itself was set.
```

### Hamming Distance: XOR as a Difference Finder

Hamming distance counts positions where two numbers differ. XOR marks exactly
those positions with a 1:

```text
a = 5  = 0101
b = 9  = 1001

a XOR b = 0101 XOR 1001 = 1100

Position 0: 1 vs 1 → same   → XOR bit = 0
Position 1: 0 vs 0 → same   → XOR bit = 0
Position 2: 1 vs 0 → DIFFER → XOR bit = 1
Position 3: 0 vs 1 → DIFFER → XOR bit = 1

The 1s in the XOR result mark exactly the differing positions.
Hamming distance = popcount(a XOR b) = 2
```

### Total Hamming Distance: The Per-Bit Counting Trick

Computing Hamming distance for all pairs brute-force is O(n²). But we can
reason about each bit position independently:

```text
For bit position b:
  - Count how many numbers have a 1 at position b → call it k
  - The remaining (n - k) numbers have a 0 at position b
  - Every (1, 0) pair at this position contributes 1 to total Hamming distance
  - Number of such pairs: k × (n - k)

Sum contributions across all 32 bit positions.
Time: O(32 × n) = O(n) instead of O(n²)
```

This is a classic "think about each dimension independently" optimization that
appears often in bit manipulation and combinatorics problems.

---

## When NOT to Use Bit Counting Approaches

**1. When You Need Bit Positions, Not Just Count**

```python
# "Find all positions where bit is set"
# Brian Kernighan counts bits but doesn't tell you WHERE they are.
# Use iteration or repeated isolation instead.

def get_set_positions(n: int) -> list[int]:
    """
    Return indices of all set bits, LSB = index 0.

    Time:  O(log n) — checks each bit position
    Space: O(k) where k = number of set bits
    """
    positions = []
    pos = 0
    while n:
        if n & 1:
            positions.append(pos)
        n >>= 1
        pos += 1
    return positions
```

**2. When Built-in Functions Are Available and Clarity Matters**

Python provides fast, readable built-ins:

```python
count = bin(n).count('1')  # Works in all Python 3 versions

count = n.bit_count()      # Python 3.10+, fastest option

# In production code, prefer built-ins over manual implementations.
# Manual Kernighan is for interviews and understanding.
```

**3. When the Problem is Actually About Patterns, Not Counts**

Some problems look like bit counting but have simpler direct solutions:

```python
# "Do these two numbers have the same set bits?"
# Don't count — just compare!
same_bits = a == b

# "Does n have exactly one set bit?" (i.e., is it a power of 2?)
# Don't count — use the direct check!
is_power_of_2 = n > 0 and (n & (n - 1)) == 0
```

**Red Flags — Don't Use Bit Counting:**

- You need bit positions, not counts
- You're checking a property that has a direct formula (power of 2, etc.)
- The problem involves floating point numbers
- Built-in popcount is available and this isn't an interview

---

## Pattern: Counting Set Bits (Popcount)

Multiple approaches exist with different tradeoffs:

```text
Number 13 = 1101₂
Set bits (1s): positions 0, 2, 3
Count: 3

Methods:
1. Iterate all bits:       O(32) for 32-bit, O(log n) in general
2. Brian Kernighan:        O(k) where k = number of set bits
3. Lookup table:           O(1) with O(256) preprocessing
4. Built-in bin().count(): Implementation-dependent, very fast
5. int.bit_count():        Python 3.10+, fastest built-in
```

---

## Problem 1: Number of 1 Bits (Hamming Weight)

**LeetCode 191** · Easy

Write a function that takes an unsigned integer and returns the number of '1'
bits it has (also known as the Hamming weight).

### Examples

```text
Input: n = 11 (binary: 1011)
Output: 3

Input: n = 128 (binary: 10000000)
Output: 1

Input: n = 4294967293 (binary: 11111111111111111111111111111101)
Output: 31
```

### Solution 1: Iterate All Bits

Check each bit position by repeatedly shifting right and inspecting the LSB.

```python
def hammingWeight_iterate(n: int) -> int:
    """
    Count set bits by checking each bit position.

    We shift n right one position at a time and check whether the LSB is 1.
    This always visits every bit, regardless of how many are set.

    Time:  O(32) for 32-bit integer — O(log n) in general
    Space: O(1)
    """
    count = 0
    while n:
        count += n & 1  # Add 1 if LSB is set
        n >>= 1         # Shift right to check next bit
    return count
```

### Solution 2: Brian Kernighan's Algorithm (Optimal for Interviews)

Skip over zero bits entirely by clearing the rightmost set bit each iteration.

```python
def hammingWeight(n: int) -> int:
    """
    Count set bits using Brian Kernighan's algorithm.

    Key insight: n & (n - 1) clears the rightmost set bit.
    Each iteration removes exactly one set bit, so we iterate
    exactly k times where k is the number of set bits.

    Time:  O(k) where k = number of set bits (k ≤ 32)
    Space: O(1)
    """
    count = 0
    while n:
        n &= n - 1  # Clear rightmost set bit
        count += 1
    return count


# Test
print(hammingWeight(11))          # 3  (1011 has three 1s)
print(hammingWeight(128))         # 1  (10000000 has one 1)
print(hammingWeight(4294967293))  # 31
```

### Solution 3: Lookup Table

Pre-compute popcount for all byte values (0–255), then split the number into
bytes and sum their counts. This gives O(1) per query after O(256) setup.

```python
def hammingWeight_table(n: int) -> int:
    """
    Count set bits using a precomputed lookup table.

    We build a table of popcount for every possible byte value (0-255).
    Then for a 32-bit number, we look up each of the 4 bytes and sum.

    Time:  O(1) per query (4 lookups for a 32-bit integer)
    Space: O(256) for the table
    """
    # Build table: popcount for 0..255
    table = [0] * 256
    for i in range(1, 256):
        table[i] = table[i & (i - 1)] + 1  # DP using Kernighan's relation

    # Split n into 4 bytes and sum their popcounts
    return (table[n & 0xFF]
            + table[(n >> 8) & 0xFF]
            + table[(n >> 16) & 0xFF]
            + table[(n >> 24) & 0xFF])


# Test
print(hammingWeight_table(11))   # 3
print(hammingWeight_table(128))  # 1
```

### Solution 4: Python Built-ins

```python
def hammingWeight_builtin(n: int) -> int:
    """Using bin() — works in all Python 3 versions."""
    return bin(n).count('1')


def hammingWeight_bitcount(n: int) -> int:
    """Using int.bit_count() — Python 3.10+ only, fastest option."""
    return n.bit_count()
```

### Trace: Why Brian Kernighan Works

```text
n = 52 = 110100₂  (3 set bits)

Iteration 1:
  n     = 110100
  n - 1 = 110011
  n & (n-1) = 110000  ← rightmost 1 (at position 2) cleared
  count = 1

Iteration 2:
  n     = 110000
  n - 1 = 101111
  n & (n-1) = 100000  ← next 1 (at position 4) cleared
  count = 2

Iteration 3:
  n     = 100000
  n - 1 = 011111
  n & (n-1) = 000000  ← last 1 (at position 5) cleared
  count = 3

Result: 3 iterations for exactly 3 set bits.
Contrast: the naive approach would take 6 iterations (for all bit positions).
```

---

## Problem 2: Counting Bits for Range [0, n]

**LeetCode 338** · Easy

Given an integer `n`, return an array `ans` of length `n + 1` such that `ans[i]`
is the number of 1's in the binary representation of `i`.

**Follow-up:** Can you do it in O(n) time and without calling popcount for each number?

### Examples

```text
Input: n = 5
Output: [0, 1, 1, 2, 1, 2]

Explanation:
  0 = 0    → 0 ones
  1 = 1    → 1 one
  2 = 10   → 1 one
  3 = 11   → 2 ones
  4 = 100  → 1 one
  5 = 101  → 2 ones
```

### Solution 1: Brute Force (Kernighan for Each Number)

```python
def countBits_brute(n: int) -> list[int]:
    """
    Count bits for each number independently using Brian Kernighan.

    Time:  O(n × k_avg) — worst case O(n log n)
    Space: O(n) for result array
    """
    def popcount(x: int) -> int:
        count = 0
        while x:
            x &= x - 1
            count += 1
        return count

    return [popcount(i) for i in range(n + 1)]
```

### Solution 2: DP with Last Set Bit (Optimal)

Each number's popcount is 1 more than the popcount of the number with its
rightmost set bit removed. Since that smaller number's answer is already
computed, this is a single O(1) lookup per number.

```python
def countBits(n: int) -> list[int]:
    """
    DP recurrence: bits[i] = bits[i & (i - 1)] + 1

    Why this works:
      i & (i - 1) removes the rightmost set bit from i, yielding a
      strictly smaller number j < i whose popcount we already know.
      Since we removed exactly one bit: popcount(i) = popcount(j) + 1.

    Time:  O(n) — one O(1) operation per number
    Space: O(n) for result array (no extra space beyond output)
    """
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i & (i - 1)] + 1
    return bits


# Test
print(countBits(5))   # [0, 1, 1, 2, 1, 2]
print(countBits(10))  # [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2]
```

### Solution 3: DP with Right Shift (Alternative)

```python
def countBits_shift(n: int) -> list[int]:
    """
    DP recurrence: bits[i] = bits[i >> 1] + (i & 1)

    Why this works:
      i >> 1 drops the LSB, giving a number whose popcount we already know.
      If the dropped LSB was 1 (i.e., i is odd), we add 1; otherwise 0.

      Equivalently: popcount(i) = popcount(i // 2) + (i mod 2)

    Time:  O(n)
    Space: O(n)
    """
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits
```

### DP Relationship Visualization

```text
Using bits[i] = bits[i >> 1] + (i & 1):

i = 0:  bits[0] = 0                          (base case)
i = 1:  bits[1] = bits[0] + 1 = 0 + 1 = 1   (1 is odd → +1)
i = 2:  bits[2] = bits[1] + 0 = 1 + 0 = 1   (2 is even → +0)
i = 3:  bits[3] = bits[1] + 1 = 1 + 1 = 2   (3 is odd → +1)
i = 4:  bits[4] = bits[2] + 0 = 1 + 0 = 1   (4 is even → +0)
i = 5:  bits[5] = bits[2] + 1 = 1 + 1 = 2   (5 is odd → +1)
i = 6:  bits[6] = bits[3] + 0 = 2 + 0 = 2   (6 is even → +0)
i = 7:  bits[7] = bits[3] + 1 = 2 + 1 = 3   (7 is odd → +1)

Pattern: right-shifting halves the number. We just track whether the
         dropped bit was a 1 (odd) or 0 (even).
```

---

## Problem 3: Hamming Distance

**LeetCode 461** · Easy

The Hamming distance between two integers is the number of positions at which
the corresponding bits are different. Given two integers `x` and `y`, return
the Hamming distance between them.

### Examples

```text
Input: x = 1, y = 4
Output: 2

  1 = 0 0 0 1
  4 = 0 1 0 0
      ─ ↑ ─ ↑  ← two positions differ (bits 0 and 2)
```

### Solution: XOR + Popcount

The key insight: XOR produces a 1 at every position where the two inputs
differ, and a 0 where they match. So Hamming distance = popcount(x XOR y).

```python
def hammingDistance(x: int, y: int) -> int:
    """
    XOR marks differing bit positions with 1s.
    Then count those 1s using Brian Kernighan.

    Time:  O(k) where k = number of differing bits
    Space: O(1)
    """
    xor = x ^ y
    distance = 0
    while xor:
        xor &= xor - 1  # Clear rightmost set bit
        distance += 1
    return distance


def hammingDistance_builtin(x: int, y: int) -> int:
    """One-liner using Python built-in."""
    return bin(x ^ y).count('1')


# Test
print(hammingDistance(1, 4))  # 2
print(hammingDistance(3, 1))  # 1
print(hammingDistance(0, 0))  # 0  (identical → distance 0)
```

---

## Problem 4: Minimum Bit Flips to Convert

**LeetCode 2220** · Easy

A bit flip of a number `x` is choosing a bit and toggling it. Given two
integers `start` and `goal`, return the minimum number of bit flips to
convert `start` to `goal`.

This is exactly the Hamming distance — each differing bit requires one flip.

```python
def minBitFlips(start: int, goal: int) -> int:
    """
    Minimum flips = Hamming distance between start and goal.
    XOR identifies the differing bits; Kernighan counts them.

    Time:  O(k) where k = number of differing bits
    Space: O(1)
    """
    xor = start ^ goal
    flips = 0
    while xor:
        xor &= xor - 1
        flips += 1
    return flips


# Test
print(minBitFlips(10, 7))  # 3  (1010 vs 0111 → XOR = 1101, 3 bits set)
print(minBitFlips(3, 4))   # 3  (011 vs 100 → XOR = 111, 3 bits set)
```

---

## Problem 5: Sort Integers by the Number of 1 Bits

**LeetCode 1356** · Easy

Given an integer array `arr`, sort the integers in ascending order by the
number of 1's in their binary representation. For integers with the same
number of 1's, sort by value.

This bridges popcount to a practical use case and previews the per-number
reasoning needed for Total Hamming Distance.

### Examples

```text
Input: arr = [0, 1, 2, 3, 4, 5, 6, 7, 8]
Output: [0, 1, 2, 4, 8, 3, 5, 6, 7]

Explanation (grouped by popcount):
  0 bits: [0]
  1 bit:  [1, 2, 4, 8]    ← sorted by value within group
  2 bits: [3, 5, 6]
  3 bits: [7]
```

### Solution

```python
def sortByBits(arr: list[int]) -> list[int]:
    """
    Sort by (popcount, value). Python's sort is stable, so equal
    popcount entries retain their relative order from the secondary
    sort key (the value itself).

    Time:  O(n log n) for the sort, O(k) per popcount
    Space: O(n) for sort output
    """
    return sorted(arr, key=lambda x: (bin(x).count('1'), x))


# Test
print(sortByBits([0, 1, 2, 3, 4, 5, 6, 7, 8]))
# [0, 1, 2, 4, 8, 3, 5, 6, 7]
```

---

## Problem 6: Total Hamming Distance

**LeetCode 477** · Medium

Given an integer array `nums`, return the sum of Hamming distances between all
pairs `(nums[i], nums[j])` where `i < j`.

### Examples

```text
Input: nums = [4, 14, 2]
Output: 6

Pairs and their Hamming distances:
  hammingDist(4, 14) = 2
  hammingDist(4, 2)  = 2
  hammingDist(14, 2) = 2
Total: 6
```

### Solution 1: Brute Force (TLE for Large Input)

```python
def totalHammingDistance_brute(nums: list[int]) -> int:
    """
    Compare all O(n²) pairs explicitly.

    Time:  O(n² × 32)
    Space: O(1)
    """
    total = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            total += bin(nums[i] ^ nums[j]).count('1')
    return total
```

### Solution 2: Per-Bit Counting (Optimal)

Instead of comparing pairs, reason about each bit position independently.
For any single bit position: if `k` numbers have a 1 there and `(n - k)` have
a 0, then the number of pairs that differ at this position is `k × (n - k)`.

```python
def totalHammingDistance(nums: list[int]) -> int:
    """
    For each of 32 bit positions, count how many numbers have a 1.
    If k numbers have 1 and (n-k) have 0 at a given position,
    those bits contribute k * (n-k) to the total Hamming distance
    (every 1 pairs with every 0 at that position).

    Time:  O(32 × n) = O(n)
    Space: O(1)
    """
    n = len(nums)
    total = 0

    for bit in range(32):  # Check each of the 32 bit positions
        ones = sum(1 for num in nums if (num >> bit) & 1)
        zeros = n - ones
        total += ones * zeros  # Each (1, 0) pair contributes 1

    return total


# Test
print(totalHammingDistance([4, 14, 2]))  # 6
```

### Trace: Why Per-Bit Counting Works

```text
Array: [4, 14, 2]
  4  = 0100
  14 = 1110
  2  = 0010

Bit 0 (rightmost):
  4 → 0,  14 → 0,  2 → 0
  ones = 0, zeros = 3
  contribution = 0 × 3 = 0

Bit 1:
  4 → 0,  14 → 1,  2 → 1
  ones = 2, zeros = 1
  contribution = 2 × 1 = 2   ← pairs (14,4) and (2,4) differ here

Bit 2:
  4 → 1,  14 → 1,  2 → 0
  ones = 2, zeros = 1
  contribution = 2 × 1 = 2   ← pairs (4,2) and (14,2) differ here

Bit 3:
  4 → 0,  14 → 1,  2 → 0
  ones = 1, zeros = 2
  contribution = 1 × 2 = 2   ← pairs (14,4) and (14,2) differ here

Total: 0 + 2 + 2 + 2 = 6 ✓
```

---

## Problem 7: Prime Number of Set Bits in Binary Representation

**LeetCode 762** · Easy

Given two integers `left` and `right`, return the count of numbers in the
inclusive range `[left, right]` having a prime number of set bits.

Since values are ≤ 10⁶ < 2²⁰, the popcount is at most 20. The primes up
to 20 are {2, 3, 5, 7, 11, 13, 17, 19} — a small, fixed set.

```python
def countPrimeSetBits(left: int, right: int) -> int:
    """
    For each number in [left, right], count its set bits and check
    if that count is prime. Since max bits ≤ 20, we use a fixed set.

    Time:  O((right - left) × 20) — popcount is O(20) per number
    Space: O(1)
    """
    primes = {2, 3, 5, 7, 11, 13, 17, 19}
    count = 0
    for num in range(left, right + 1):
        if bin(num).count('1') in primes:
            count += 1
    return count


# Test
print(countPrimeSetBits(6, 10))    # 4 (6→2✓, 7→3✓, 8→1✗, 9→2✓, 10→2✓)
print(countPrimeSetBits(10, 15))   # 5
```

---

## Complexity Summary

| Problem                | Approach           | Time       | Space  |
| ---------------------- | ------------------ | ---------- | ------ |
| Number of 1 Bits       | Iterate all bits   | O(32)      | O(1)   |
| Number of 1 Bits       | Brian Kernighan    | O(k)       | O(1)   |
| Number of 1 Bits       | Lookup table       | O(1)       | O(256) |
| Counting Bits [0..n]   | Brute force        | O(n log n) | O(n)   |
| Counting Bits [0..n]   | DP (last set bit)  | O(n)       | O(n)   |
| Counting Bits [0..n]   | DP (right shift)   | O(n)       | O(n)   |
| Hamming Distance       | XOR + Kernighan    | O(k)       | O(1)   |
| Min Bit Flips          | XOR + Kernighan    | O(k)       | O(1)   |
| Sort by 1 Bits         | Sort + popcount    | O(n log n) | O(n)   |
| Total Hamming Distance | Per-bit counting   | O(32n)     | O(1)   |
| Prime Set Bits         | Count + set lookup | O(n × 20)  | O(1)   |

---

## Common Variations

### Counting Bits in a Range [left, right]

Count the total number of set bits across all integers in `[left, right]`.
Use a prefix-sum approach: total in `[left, right]` = total in `[0, right]` − total in `[0, left-1]`.

```python
def count_bits_in_range(left: int, right: int) -> int:
    """
    Count total set bits for all numbers in [left, right].

    Uses prefix sums: total_in_range = count_up_to(right) - count_up_to(left - 1).
    count_up_to(n) analyzes each bit position p: bits cycle with period
    2^(p+1), and in each full cycle exactly 2^p bits are set.

    Time:  O(log n) — iterates through bit positions
    Space: O(1)
    """
    def count_up_to(n: int) -> int:
        """Count total set bits across all numbers in [0, n]."""
        if n < 0:
            return 0
        total = 0
        power = 1  # Represents 2^p for current bit position p
        while power <= n:
            # Period of the cycle for this bit position
            cycle = power * 2

            # Number of complete cycles in [0, n]
            full_cycles = (n + 1) // cycle
            total += full_cycles * power

            # Remaining numbers in the partial cycle
            remainder = (n + 1) % cycle
            total += max(0, remainder - power)

            power *= 2
        return total

    return count_up_to(right) - count_up_to(left - 1)


# Test
print(count_bits_in_range(0, 5))   # 7  (0+1+1+2+1+2)
print(count_bits_in_range(3, 10))  # 15
```

### Set Bits at Specific Positions

```python
def count_bits_at_positions(n: int, positions: list[int]) -> int:
    """
    Count how many of the specified bit positions are set in n.

    Args:
        n: The integer to inspect.
        positions: List of bit indices (0-indexed from LSB) to check.

    Returns:
        Number of specified positions that have a 1-bit in n.

    Time:  O(len(positions))
    Space: O(1)
    """
    count = 0
    for pos in positions:
        if (n >> pos) & 1:
            count += 1
    return count
```

---

## Edge Cases

1. **Zero**: Has 0 set bits — both Kernighan and iterate handle this (loop body never executes)
2. **Power of 2**: Has exactly 1 set bit — Kernighan finishes in 1 iteration
3. **All 1s (e.g., 2³² − 1)**: Maximum set bits — Kernighan takes 32 iterations (same as naive)
4. **Equal numbers for Hamming distance**: XOR is 0, distance is 0
5. **Single-element array for total Hamming distance**: No pairs exist, result is 0
6. **Python's arbitrary-precision integers**: No overflow, but bit counts can exceed 32

---

## Interview Tips

1. **Know Brian Kernighan**: It's the expected optimal approach and shows you understand bit tricks
2. **Explain the O(k) advantage**: When k ≪ 32 (sparse bits), Kernighan is much faster than iterating all positions
3. **Mention built-ins**: `bin(n).count('1')` and `int.bit_count()` (3.10+) — shows you know Python well
4. **DP for Counting Bits**: The recurrence `bits[i] = bits[i & (i-1)] + 1` is elegant and interviewers love it
5. **Total Hamming Distance**: The per-bit counting trick reduces O(n²) to O(n) — this is the key insight
6. **Lookup table**: Mention it as an O(1) approach when asked about further optimization

---

## Practice Problems

| #   | Problem                      | Difficulty | Key Concept                 | LeetCode |
| --- | ---------------------------- | ---------- | --------------------------- | -------- |
| 1   | Number of 1 Bits             | Easy       | Brian Kernighan's algorithm | 191      |
| 2   | Counting Bits                | Easy       | DP with bit recurrence      | 338      |
| 3   | Hamming Distance             | Easy       | XOR then popcount           | 461      |
| 4   | Minimum Bit Flips to Convert | Easy       | Same as Hamming distance    | 2220     |
| 5   | Sort Integers by 1 Bits      | Easy       | Popcount as sort key        | 1356     |
| 6   | Total Hamming Distance       | Medium     | Per-bit independent count   | 477      |
| 7   | Prime Number of Set Bits     | Easy       | Popcount + prime check      | 762      |

---

## Related Sections

- [Binary Basics](./01-binary-basics.md) — Bitwise fundamentals
- [Single Number](./02-single-number.md) — Related XOR techniques
- [Power of Two](./04-power-of-two.md) — Related bit patterns (`n & (n-1)` reuse)
