# Counting Bits

> **Prerequisites:** [Binary Basics](./01-binary-basics.md)

## Interview Context

Counting set bits (popcount) and calculating Hamming distance are fundamental bit manipulation operations. These problems test efficiency awareness—knowing O(k) vs O(log n) solutions matters in interviews.

---

## Building Intuition

**Why Counting Bits is Fundamental**

At the hardware level, processors have dedicated instructions for counting bits (POPCNT). Understanding this operation conceptually helps you:

- Recognize when bit counting is the right approach
- Choose between O(log n) and O(k) algorithms
- Build dynamic programming solutions for counting bits efficiently

**The Naive Approach and Its Insight**

The simplest way to count bits is to check each position:

```
n = 13 = 1101
Check bit 0: 1101 & 1 = 1    ✓
Check bit 1: 1101 >> 1 & 1 = 0
Check bit 2: 1101 >> 2 & 1 = 1  ✓
Check bit 3: 1101 >> 3 & 1 = 1  ✓

Count: 3 set bits
Time: O(log n) or O(32) for 32-bit integers
```

This is O(log n) because we check every bit position. But what if n has only 2 set bits out of 32? We're wasting checks on 30 zero bits.

**Brian Kernighan's Brilliant Insight**

Instead of checking every bit, what if we could jump directly from one set bit to the next?

```
Key property: n & (n-1) clears the RIGHTMOST set bit

Why does this work?
n = ...1000 (some bits, then rightmost 1, then zeros)
n-1 = ...0111 (same bits until rightmost 1, which becomes 0, and all bits right of it become 1)

n & (n-1): The rightmost 1 and everything right of it become 0
           Everything left of it stays the same

Example:
n = 12 = 1100
n-1 = 11 = 1011
n & (n-1) = 1000 (rightmost 1 cleared!)

Now we have 8:
n = 8 = 1000
n-1 = 7 = 0111
n & (n-1) = 0000 (done!)

Only 2 iterations for 2 set bits (not 4 for all bit positions)
```

**The DP Insight for Counting Bits Array**

When you need to count bits for every number from 0 to n, recomputing each one is wasteful. The insight is that you've already computed the answer for smaller numbers:

```
bits[i] = bits[i with one less bit set] + 1
        = bits[i & (i-1)] + 1

Example:
bits[0] = 0
bits[1] = bits[0] + 1 = 1  (1 & 0 = 0)
bits[2] = bits[0] + 1 = 1  (2 & 1 = 0)
bits[3] = bits[2] + 1 = 2  (3 & 2 = 2, bits[2] = 1)
bits[4] = bits[0] + 1 = 1  (4 & 3 = 0)
bits[5] = bits[4] + 1 = 2  (5 & 4 = 4, bits[4] = 1)
```

**Hamming Distance: XOR as a Difference Finder**

Hamming distance counts positions where two numbers differ. The insight is that XOR marks exactly those positions:

```
a = 5 = 101
b = 9 = 1001

Where do they differ?
Position 0: 1 vs 1 → same
Position 1: 0 vs 0 → same
Position 2: 1 vs 0 → DIFFERENT
Position 3: 0 vs 1 → DIFFERENT

a XOR b = 0101 XOR 1001 = 1100

The 1s in the XOR result mark exactly the differing positions!
Now just count the 1s: Hamming distance = 2
```

**Total Hamming Distance: The Counting Optimization**

For all pairs, brute force is O(n²). But we can think about each bit position independently:

```
For bit position i:
- Count how many numbers have 1 at position i (call it k)
- Then (n-k) numbers have 0 at position i
- Every 1-bit pairs with every 0-bit, contributing to Hamming distance
- Contribution: k × (n-k)

Sum contributions across all bit positions.
Time: O(32n) = O(n) instead of O(n²)!
```

This is a classic "think about each position independently" insight that appears often in bit manipulation problems.

---

## When NOT to Use Bit Counting Approaches

**1. When You Need the Actual Bit Positions, Not Just Count**

```python
# "Find all positions where bit is set"
# Brian Kernighan doesn't tell you WHERE the bits are
# Use iteration or repeated isolation instead

def get_set_positions(n):
    positions = []
    pos = 0
    while n:
        if n & 1:
            positions.append(pos)
        n >>= 1
        pos += 1
    return positions
```

**2. When Built-in is Available and Clarity Matters**

Python's built-in is fast and readable:

```python
count = bin(n).count('1')  # Pythonic, likely C-optimized

# In production code, prefer this over manual implementation
# Manual Kernighan is for interviews and understanding
```

**3. For Very Large Numbers with Few Set Bits**

In Python with arbitrary precision integers, Brian Kernighan is still O(k), but if k is very large (thousands of set bits), you might want different approaches (e.g., table lookup for chunks).

**4. When the Problem is Actually About Patterns, Not Counts**

Some problems look like bit counting but aren't:

```python
# "Do these two numbers have the same set bits?"
# You don't need to count - just compare!
same_bits = (a ^ b) == 0  # or just a == b

# "Does n have exactly one set bit?"
# Don't count - use the power of 2 check!
is_power_of_2 = n > 0 and (n & (n-1)) == 0
```

**Red Flags (Don't Use Bit Counting):**

- You need bit positions, not count
- You're checking a property that has a direct formula (power of 2)
- The problem involves floating point
- Built-in popcount is available and this isn't an interview

---

## Pattern: Counting Set Bits (Popcount)

Multiple approaches exist with different time complexities:

```
Number 13 = 1101 in binary
Set bits (1s): positions 0, 2, 3
Count: 3

Methods:
1. Iterate all bits: O(log n) or O(32)
2. Brian Kernighan: O(k) where k = number of set bits
3. Lookup table: O(1) with preprocessing
4. Built-in: bin(n).count('1') in Python
```

---

## Problem: Number of 1 Bits

**LeetCode 191**: Write a function that takes a positive integer and returns the number of '1' bits (Hamming weight).

### Example

```
Input: n = 11 (binary: 1011)
Output: 3

Input: n = 128 (binary: 10000000)
Output: 1

Input: n = 4294967293 (binary: 11111111111111111111111111111101)
Output: 31
```

### Solution 1: Iterate All Bits

```python
def hammingWeight_iterate(n: int) -> int:
    """
    Count set bits by checking each bit position.

    Time: O(32) for 32-bit integer = O(1)
    Space: O(1)
    """
    count = 0
    while n:
        count += n & 1  # Check LSB
        n >>= 1         # Shift right
    return count
```

### Solution 2: Brian Kernighan's Algorithm (Optimal)

```python
def hammingWeight(n: int) -> int:
    """
    Count set bits using Brian Kernighan's algorithm.

    Key insight: n & (n-1) clears the rightmost set bit.

    Time: O(k) where k = number of set bits
    Space: O(1)
    """
    count = 0
    while n:
        n &= n - 1  # Clear rightmost set bit
        count += 1
    return count


# Test
print(hammingWeight(11))   # 3 (1011)
print(hammingWeight(128))  # 1 (10000000)
```

### Why Brian Kernighan Works

```
n = 52 = 110100

Iteration 1:
  n     = 110100
  n - 1 = 110011
  n & (n-1) = 110000  (rightmost 1 cleared!)
  count = 1

Iteration 2:
  n     = 110000
  n - 1 = 101111
  n & (n-1) = 100000  (next 1 cleared!)
  count = 2

Iteration 3:
  n     = 100000
  n - 1 = 011111
  n & (n-1) = 000000  (last 1 cleared!)
  count = 3

Total: 3 iterations (exactly as many as set bits)
```

---

## Problem: Counting Bits

**LeetCode 338**: Given an integer n, return an array `ans` of length n+1 such that `ans[i]` is the number of 1's in the binary representation of i.

### Example

```
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

### Solution 1: Brute Force

```python
def countBits_brute(n: int) -> list[int]:
    """
    Count bits for each number individually.

    Time: O(n log n) or O(n × 32)
    Space: O(n) for result
    """
    def popcount(x):
        count = 0
        while x:
            x &= x - 1
            count += 1
        return count

    return [popcount(i) for i in range(n + 1)]
```

### Solution 2: DP with Last Set Bit

```python
def countBits(n: int) -> list[int]:
    """
    Use DP: bits[i] = bits[i & (i-1)] + 1

    Key insight: i & (i-1) removes the last set bit.
    So bits[i] = bits[i with last bit removed] + 1

    Time: O(n)
    Space: O(n) for result (O(1) extra)
    """
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i & (i - 1)] + 1
    return bits


# Test
print(countBits(5))  # [0, 1, 1, 2, 1, 2]
```

### Solution 3: DP with Right Shift

```python
def countBits_shift(n: int) -> list[int]:
    """
    Use DP: bits[i] = bits[i >> 1] + (i & 1)

    Key insight: i >> 1 is i with LSB removed.
    bits[i] = bits[i // 2] + (1 if i is odd else 0)

    Time: O(n)
    Space: O(n) for result
    """
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits
```

### DP Relationship Visualization

```
Using bits[i] = bits[i >> 1] + (i & 1):

i = 0:  bits[0] = 0 (base case)
i = 1:  bits[1] = bits[0] + 1 = 0 + 1 = 1
i = 2:  bits[2] = bits[1] + 0 = 1 + 0 = 1
i = 3:  bits[3] = bits[1] + 1 = 1 + 1 = 2
i = 4:  bits[4] = bits[2] + 0 = 1 + 0 = 1
i = 5:  bits[5] = bits[2] + 1 = 1 + 1 = 2
i = 6:  bits[6] = bits[3] + 0 = 2 + 0 = 2
i = 7:  bits[7] = bits[3] + 1 = 2 + 1 = 3

Pattern: Right shift divides by 2, we just add 1 if LSB was set
```

---

## Problem: Hamming Distance

**LeetCode 461**: The Hamming distance between two integers is the number of positions at which the corresponding bits differ. Given two integers x and y, return the Hamming distance.

### Example

```
Input: x = 1, y = 4
Output: 2

  1 = 0001
  4 = 0100
      ↑  ↑ (two positions differ)
```

### Solution

```python
def hammingDistance(x: int, y: int) -> int:
    """
    Count positions where bits differ.

    Key insight: XOR gives 1s exactly where bits differ.
    Then count set bits in the XOR result.

    Time: O(k) where k = number of differing bits
    Space: O(1)
    """
    xor = x ^ y
    count = 0
    while xor:
        xor &= xor - 1  # Brian Kernighan
        count += 1
    return count


# One-liner
def hammingDistance_oneliner(x: int, y: int) -> int:
    return bin(x ^ y).count('1')


# Test
print(hammingDistance(1, 4))  # 2
print(hammingDistance(3, 1))  # 1
```

---

## Problem: Total Hamming Distance

**LeetCode 477**: Find the sum of Hamming distances between all pairs of integers in an array.

### Example

```
Input: [4, 14, 2]
Output: 6

Pairs:
  (4, 14) = 2
  (4, 2)  = 2
  (14, 2) = 2
Total: 6
```

### Solution

```python
def totalHammingDistance(nums: list[int]) -> int:
    """
    Sum of Hamming distances for all pairs.

    Brute force: O(n² × 32) - compare all pairs
    Optimal: O(32n) - count bits at each position

    Key insight: For each bit position, if k numbers have 1 and
    (n-k) have 0, the contribution is k × (n-k) (pairs that differ).

    Time: O(32n) = O(n)
    Space: O(1)
    """
    n = len(nums)
    total = 0

    for bit in range(32):
        ones = sum((num >> bit) & 1 for num in nums)
        zeros = n - ones
        total += ones * zeros  # Pairs that differ at this bit

    return total


# Test
print(totalHammingDistance([4, 14, 2]))  # 6
```

### Why This Works

```
Array: [4, 14, 2]
4  = 0100
14 = 1110
2  = 0010

Bit 0 (rightmost):
  4 → 0, 14 → 0, 2 → 0
  ones = 0, zeros = 3
  contribution = 0 × 3 = 0

Bit 1:
  4 → 0, 14 → 1, 2 → 1
  ones = 2, zeros = 1
  contribution = 2 × 1 = 2

Bit 2:
  4 → 1, 14 → 1, 2 → 0
  ones = 2, zeros = 1
  contribution = 2 × 1 = 2

Bit 3:
  4 → 0, 14 → 1, 2 → 0
  ones = 1, zeros = 2
  contribution = 1 × 2 = 2

Total: 0 + 2 + 2 + 2 = 6
```

---

## Complexity Analysis

| Problem                | Approach        | Time       | Space |
| ---------------------- | --------------- | ---------- | ----- |
| Number of 1 Bits       | Iterate         | O(32)      | O(1)  |
| Number of 1 Bits       | Brian Kernighan | O(k)       | O(1)  |
| Counting Bits          | Brute force     | O(n log n) | O(n)  |
| Counting Bits          | DP              | O(n)       | O(n)  |
| Hamming Distance       | XOR + count     | O(k)       | O(1)  |
| Total Hamming Distance | Bit counting    | O(32n)     | O(1)  |

---

## Common Variations

### 1. Counting Bits in a Range

```python
def count_bits_in_range(left: int, right: int) -> int:
    """Count total set bits for all numbers in [left, right]."""
    def count_up_to(n):
        """Count total set bits in [0, n]."""
        if n < 0:
            return 0
        total = 0
        power = 1
        while power <= n:
            # How many complete cycles of 2*power
            full_cycles = (n + 1) // (power * 2)
            total += full_cycles * power
            # Remaining bits in partial cycle
            remainder = (n + 1) % (power * 2)
            total += max(0, remainder - power)
            power *= 2
        return total

    return count_up_to(right) - count_up_to(left - 1)
```

### 2. Minimum Bit Flips to Convert

```python
def minBitFlips(start: int, goal: int) -> int:
    """
    Minimum bit flips to convert start to goal.
    Same as Hamming distance!
    """
    xor = start ^ goal
    count = 0
    while xor:
        xor &= xor - 1
        count += 1
    return count
```

### 3. Set Bits at Specific Positions

```python
def count_bits_at_positions(n: int, positions: list[int]) -> int:
    """Count set bits only at specified positions."""
    count = 0
    for pos in positions:
        if (n >> pos) & 1:
            count += 1
    return count
```

---

## Edge Cases

1. **Zero**: Has 0 set bits
2. **Power of 2**: Has exactly 1 set bit
3. **All 1s (like 2^32 - 1)**: Has 32 set bits
4. **Negative numbers**: Need to handle two's complement representation
5. **Equal numbers for Hamming distance**: Distance is 0

---

## Interview Tips

1. **Know Brian Kernighan**: It's the optimal approach and shows you know bit tricks
2. **Explain the optimization**: O(k) vs O(log n) matters when k is small
3. **Mention built-ins**: `bin(n).count('1')` in Python, `popcount` in other languages
4. **DP insight for Counting Bits**: The relationship `bits[i] = bits[i & (i-1)] + 1`
5. **Total Hamming Distance trick**: Per-bit counting is the key insight

---

## Practice Problems

| #   | Problem                      | Difficulty | Key Concept         |
| --- | ---------------------------- | ---------- | ------------------- |
| 1   | Number of 1 Bits             | Easy       | Brian Kernighan     |
| 2   | Counting Bits                | Easy       | DP relationship     |
| 3   | Hamming Distance             | Easy       | XOR then count      |
| 4   | Total Hamming Distance       | Medium     | Per-bit counting    |
| 5   | Minimum Bit Flips to Convert | Easy       | Same as Hamming     |
| 6   | Prime Number of Set Bits     | Easy       | Count + prime check |

---

## Related Sections

- [Binary Basics](./01-binary-basics.md) - Bitwise fundamentals
- [Single Number](./02-single-number.md) - Related XOR techniques
- [Power of Two](./04-power-of-two.md) - Related bit patterns
