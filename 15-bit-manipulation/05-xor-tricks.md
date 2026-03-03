# XOR Tricks

> **Prerequisites:** [Binary Basics](./01-binary-basics.md), [Single Number](./02-single-number.md)

## Interview Context

XOR is the most versatile bitwise operator for interviews. Its unique properties enable elegant solutions to seemingly complex problems. Mastering XOR tricks demonstrates deep understanding of bit manipulation.

---

## XOR Properties (Know These Cold)

XOR (exclusive or) outputs 1 when inputs differ:

```
Bit-level truth table:

  0 ^ 0 = 0
  0 ^ 1 = 1
  1 ^ 0 = 1
  1 ^ 1 = 0
```

### Property 1: Self-Inverse (a ^ a = 0)

Any value XORed with itself cancels out to zero.

```python
a = 42
print(a ^ a)  # 0

# This works because every bit matches itself:
#   0101 ^ 0101 = 0000
# Corresponding bits are always the same, so every position outputs 0.
```

This is the foundation of almost every XOR trick. When you XOR a collection
that contains pairs, the pairs cancel out, leaving only the unpaired value.

### Property 2: Identity (a ^ 0 = a)

XORing with zero leaves the value unchanged.

```python
a = 42
print(a ^ 0)  # 42

# No bits are toggled because 0 has no set bits:
#   0101 ^ 0000 = 0101
```

### Property 3: Commutativity (a ^ b = b ^ a)

Order of operands does not matter.

```python
a, b = 5, 3
print(a ^ b)  # 6
print(b ^ a)  # 6
```

### Property 4: Associativity ((a ^ b) ^ c = a ^ (b ^ c))

Grouping does not matter. You can rearrange and regroup XOR chains freely.

```python
a, b, c = 5, 3, 7
print((a ^ b) ^ c)  # 1
print(a ^ (b ^ c))  # 1
```

Together with commutativity, this means you can XOR a set of values in any
order and get the same result. This is why pair cancellation works regardless
of element positions in an array.

### Property 5: Pair Cancellation (a ^ b ^ a = b)

A direct consequence of self-inverse, identity, and associativity:

```python
# a ^ b ^ a
# = (a ^ a) ^ b   (commutativity + associativity)
# = 0 ^ b          (self-inverse)
# = b              (identity)

a, b = 5, 3
print(a ^ b ^ a)  # 3
```

### Property 6: Reversibility (if a ^ b = c, then b ^ c = a)

XOR is its own inverse, which enables encoding and decoding:

```python
a, b = 5, 3
c = a ^ b  # c = 6

# Recover a from b and c:
print(b ^ c)  # 5  (== a)

# Recover b from a and c:
print(a ^ c)  # 3  (== b)
```

This is the basis for:
- Swap without a temp variable
- Simple XOR encryption/decryption
- Decoding XOR-encoded arrays

### Cheat Sheet

```
1. a ^ a = 0             Self-inverse (cancellation)
2. a ^ 0 = a             Identity
3. a ^ b = b ^ a         Commutative
4. (a^b)^c = a^(b^c)     Associative
5. a ^ b ^ a = b         Pair cancellation
6. a ^ b = c → a = b ^ c Reversibility
```

---

## Building Intuition

**XOR as "Controlled Toggling"**

Think of XOR as a toggle switch controlled by another bit:

```
If control bit is 0: output = original (no change)
If control bit is 1: output = opposite of original (toggle/flip)

a ^ 0 = a   (control is 0, no toggling)
a ^ 1 = flips the last bit of a

This is why XOR with a mask selectively toggles bits:
  1010 ^ 0011 = 1001
         ^^         ^^ these bits were toggled
```

**The "Difference Detector" Mental Model**

XOR tells you WHERE two numbers differ:

```
a = 5 = 0101
b = 3 = 0011
a ^ b = 0110

The 1s in the result mark positions where a and b disagree.
Count these 1s → Hamming distance
Use any of these positions → partition the numbers into groups
```

**Why XOR for Missing/Single Number Works**

The core insight: XOR with the same value twice cancels out.

```
If you XOR:
- All indices 0 to n
- All array values

Indices that have their matching value: cancel to 0
The missing index: no value to cancel with → remains

Example: [0, 1, 3] (missing 2)
XOR indices: 0 ^ 1 ^ 2 ^ 3
XOR values:  0 ^ 1 ^ 3
Combined:    (0^0) ^ (1^1) ^ 2 ^ (3^3) = 0 ^ 0 ^ 2 ^ 0 = 2 ✓
```

**XOR Range Pattern: The Mod 4 Insight**

XORing 0 to n has a repeating pattern every 4 numbers:

```
n    XOR(0..n)
0    0
1    0^1 = 1
2    0^1^2 = 3
3    0^1^2^3 = 0
4    0^1^2^3^4 = 4
5    ...^5 = 1
6    ...^6 = 7
7    ...^7 = 0
8    ...^8 = 8

Pattern based on n % 4:
  n % 4 == 0 → n
  n % 4 == 1 → 1
  n % 4 == 2 → n + 1
  n % 4 == 3 → 0
```

Why? Every group of 4 consecutive numbers XORs to 0:

```
k ^ (k+1) ^ (k+2) ^ (k+3) = 0  (when k is divisible by 4)

The last 2 bits of k, k+1, k+2, k+3 cycle through 00, 01, 10, 11.
XOR of 00 ^ 01 ^ 10 ^ 11 = 00. Higher bits appear an even number
of times and also cancel. So every complete group of 4 vanishes,
and XOR(0..n) depends only on the remainder n % 4.
```

**Addition with XOR and AND: The Carry Insight**

XOR gives the sum ignoring carries. AND gives the carry bits:

```
Adding 5 + 3:
  5 = 0101
  3 = 0011

Step 1:
  sum without carry = 5 ^ 3      = 0110 (6)
  carry bits        = (5 & 3)<<1 = 0010 (2)

Step 2:
  sum without carry = 6 ^ 2      = 0100 (4)
  carry bits        = (6 & 2)<<1 = 0100 (4)

Step 3:
  sum without carry = 4 ^ 4      = 0000 (0)
  carry bits        = (4 & 4)<<1 = 1000 (8)

Step 4:
  sum without carry = 0 ^ 8      = 1000 (8)
  carry bits        = (0 & 8)<<1 = 0000 (0) ← no carry, done!

Result: 8 ✓  (5 + 3 = 8)
```

---

## When NOT to Use XOR Tricks

**1. When Order Matters**

XOR is commutative and associative — it loses ordering information:

```python
# "Find first duplicate" — XOR can't tell you which came first
# "Find k-th occurrence" — XOR doesn't track positions

# Use hashmap or other structures for order-sensitive problems
```

**2. For Subtraction or Division**

XOR simulates addition (with AND for carry), but subtraction is different:

```python
# XOR-based addition works, but for subtraction:
# You need two's complement: a - b = a + (~b + 1)
# More complex than just using the subtraction operator
```

**3. When Floating Point is Involved**

XOR is for integers only:

```python
# Can't XOR floats directly in Python
# Floats have sign, exponent, mantissa — XOR produces garbage
```

**4. When You Need to Preserve Values (Aliasing Hazard)**

XOR swap is destructive when used on the same memory location:

```python
# XOR swap fails when a and b are the same variable!
a = 5
a ^= a  # a becomes 0, original value lost
a ^= a  # still 0
a ^= a  # still 0

# Also fails for aliased references:
arr = [10, 20, 30]
i, j = 1, 1
# arr[i] ^= arr[j]  →  if i == j, you've zeroed the element!
```

**5. When There Are More Than Two Unique Elements**

XOR of multiple distinct elements gives their combined XOR, which is not
directly useful for identifying individuals:

```python
nums = [1, 2, 3, 4, 5]  # All unique
xor_all = 1 ^ 2 ^ 3 ^ 4 ^ 5  # = 1
# This single value tells you nothing about individual elements
```

**Red Flags (Don't Use XOR):**

- Need to track positions or order
- More than 2 unique elements among pairs
- Floating point data
- Same variable on both sides of XOR (aliasing)
- Need to preserve original values

---

## Practice Problems (Progressive Difficulty)

### Problem 1: Swap Two Numbers Without a Temp Variable

Exchange values of two variables without using a temporary variable.

**Difficulty:** Easy

```python
def swap_xor(a: int, b: int) -> tuple[int, int]:
    """
    Swap two integers using XOR.

    Step-by-step:
      a ^= b  →  a now holds (a ^ b)
      b ^= a  →  b = b ^ (a ^ b) = a   (original a)
      a ^= b  →  a = (a ^ b) ^ a = b   (original b)

    Guard: if a and b refer to the same memory, XOR swap
    zeroes the value. The a != b check prevents this.

    Time: O(1)
    Space: O(1)
    """
    if a != b:  # Guard against aliasing
        a ^= b
        b ^= a
        a ^= b
    return a, b


# In practice, Python's tuple swap is cleaner: a, b = b, a

# Test
x, y = 5, 10
x, y = swap_xor(x, y)
print(x, y)  # 10 5

x, y = swap_xor(x, y)
print(x, y)  # 5 10

# Edge case: same values
print(swap_xor(7, 7))  # (7, 7)
```

---

### Problem 2: Single Number (LeetCode 136)

Given a non-empty array where every element appears exactly twice except for
one, find the single element.

**Difficulty:** Easy

```
Input: nums = [4, 1, 2, 1, 2]
Output: 4

Input: nums = [1]
Output: 1
```

```python
def single_number(nums: list[int]) -> int:
    """
    XOR all elements. Pairs cancel (a ^ a = 0), leaving the single.

    Time: O(n)
    Space: O(1)
    """
    result = 0
    for num in nums:
        result ^= num
    return result


# Test
print(single_number([4, 1, 2, 1, 2]))  # 4
print(single_number([1]))               # 1
print(single_number([0, 1, 0]))         # 1
```

---

### Problem 3: Missing Number (LeetCode 268)

Given an array `nums` containing n distinct numbers in the range `[0, n]`,
return the only number in the range that is missing.

**Difficulty:** Easy

```
Input: nums = [3, 0, 1]
Output: 2     (range is [0, 1, 2, 3], missing 2)

Input: nums = [9, 6, 4, 2, 3, 5, 7, 0, 1]
Output: 8
```

```python
def missing_number(nums: list[int]) -> int:
    """
    XOR all array elements with all indices 0..n.
    Every number that IS present cancels with its index.
    The missing number has no partner and survives.

    We initialize result = n because indices go 0..n-1 but the
    range goes 0..n, so n itself is not an index.

    Time: O(n)
    Space: O(1)
    """
    result = len(nums)  # Start with n (the one index we don't loop over)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result


# Alternative: Arithmetic sum approach
def missing_number_sum(nums: list[int]) -> int:
    """Use Gauss's formula: expected sum minus actual sum."""
    n = len(nums)
    expected = n * (n + 1) // 2
    return expected - sum(nums)


# Test
print(missing_number([3, 0, 1]))                    # 2
print(missing_number([0, 1]))                        # 2
print(missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]))  # 8
```

**Why XOR Works (Walkthrough)**

```
nums = [3, 0, 1], n = 3

result starts at 3  (= n)

i=0: result ^= 0 ^ 3  →  result = 3 ^ 0 ^ 3 = 0
i=1: result ^= 1 ^ 0  →  result = 0 ^ 1 ^ 0 = 1
i=2: result ^= 2 ^ 1  →  result = 1 ^ 2 ^ 1 = 2

Rearranging the full XOR chain:
  3 ^ (0 ^ 3) ^ (1 ^ 0) ^ (2 ^ 1)
= (0^0) ^ (1^1) ^ 2 ^ (3^3)
= 0 ^ 0 ^ 2 ^ 0
= 2 ✓
```

---

### Problem 4: Decode XORed Array (LeetCode 1720)

Given an encoded array where `encoded[i] = arr[i] XOR arr[i+1]`, and the
first element, recover the original array.

**Difficulty:** Easy

```
Input: encoded = [1, 2, 3], first = 1
Output: [1, 0, 2, 1]

Because:
  arr[0] = 1 (given)
  arr[0] ^ arr[1] = 1  →  arr[1] = 1 ^ 1 = 0
  arr[1] ^ arr[2] = 2  →  arr[2] = 0 ^ 2 = 2
  arr[2] ^ arr[3] = 3  →  arr[3] = 2 ^ 3 = 1
```

```python
def decode(encoded: list[int], first: int) -> list[int]:
    """
    Decode an XOR-encoded array.

    Since encoded[i] = arr[i] ^ arr[i+1], we can recover:
      arr[i+1] = arr[i] ^ encoded[i]    (XOR reversibility)

    Time: O(n)
    Space: O(n) for the result array
    """
    result = [first]
    for val in encoded:
        result.append(result[-1] ^ val)
    return result


# Test
print(decode([1, 2, 3], 1))     # [1, 0, 2, 1]
print(decode([6, 2, 7, 3], 4))  # [4, 2, 0, 7, 4]
```

---

### Problem 5: Find the Duplicate Number (XOR Variant)

Given an array of n+1 integers where each integer is in `[1, n]` and exactly
one value is duplicated (appears exactly twice), find it using XOR.

**Difficulty:** Easy-Medium

> Note: The classic LeetCode 287 allows multiple duplicates and unknown
> counts, which requires Floyd's cycle detection. This simpler variant
> (exactly one duplicate, appearing exactly twice) is solvable with XOR.

```
Input: nums = [1, 3, 4, 2, 2]
Output: 2

Input: nums = [3, 1, 3, 2]
Output: 3
```

```python
def find_duplicate_xor(nums: list[int]) -> int:
    """
    XOR all array elements with 1..n.
    The non-duplicate values cancel. The duplicate appears
    twice in nums but once in 1..n, so one copy survives.

    Constraint: exactly one value appears exactly twice;
    all other values appear exactly once.

    Time: O(n)
    Space: O(1)
    """
    n = len(nums) - 1  # Array has n+1 elements, values in [1, n]
    xor_all = 0

    for num in nums:
        xor_all ^= num
    for i in range(1, n + 1):
        xor_all ^= i

    return xor_all


# Test
print(find_duplicate_xor([1, 3, 4, 2, 2]))  # 2
print(find_duplicate_xor([3, 1, 3, 2]))      # 3
```

---

### Problem 6: Single Number III (LeetCode 260)

Given an array where every element appears exactly twice except for two
elements that appear exactly once, find those two elements.

**Difficulty:** Medium

```
Input: nums = [1, 2, 1, 3, 2, 5]
Output: [3, 5]
```

```python
def single_number_iii(nums: list[int]) -> list[int]:
    """
    Two-pass XOR approach:

    Pass 1: XOR everything → get a ^ b (the two singles XORed).
    Pass 2: Use a set bit of (a ^ b) to partition all numbers
            into two groups. Each group contains exactly one of
            the singles, and the rest cancel in pairs.

    Time: O(n)
    Space: O(1)
    """
    # Pass 1: XOR all to get xor_ab = a ^ b
    xor_ab = 0
    for num in nums:
        xor_ab ^= num

    # Find any bit where a and b differ (rightmost set bit)
    diff_bit = xor_ab & (-xor_ab)

    # Pass 2: Partition by diff_bit and XOR each group
    a, b = 0, 0
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num

    return [a, b]


# Test
print(single_number_iii([1, 2, 1, 3, 2, 5]))  # [3, 5] or [5, 3]
```

---

### Problem 7: Find Two Missing Numbers

Given an array of n-2 distinct numbers from range `[1, n]`, find the two
missing numbers.

**Difficulty:** Medium

```
Input: nums = [1, 3, 5, 6], n = 6
Output: [2, 4]

Range: [1, 2, 3, 4, 5, 6]
Missing: 2 and 4
```

```python
def find_two_missing(nums: list[int], n: int) -> list[int]:
    """
    Same technique as Single Number III:
    1. XOR all values 1..n with all array elements → get a ^ b
    2. Find a bit where the two missing numbers differ
    3. Partition all numbers by that bit and XOR each group

    Time: O(n)
    Space: O(1)
    """
    # Step 1: XOR everything to get missing1 ^ missing2
    xor_all = 0
    for i in range(1, n + 1):
        xor_all ^= i
    for num in nums:
        xor_all ^= num

    # Step 2: Find rightmost set bit (where the two missing differ)
    diff_bit = xor_all & (-xor_all)

    # Step 3: Partition and XOR each group
    a, b = 0, 0
    for i in range(1, n + 1):
        if i & diff_bit:
            a ^= i
        else:
            b ^= i
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num

    return sorted([a, b])


# Test
print(find_two_missing([1, 3, 5, 6], 6))  # [2, 4]
print(find_two_missing([2, 3], 4))         # [1, 4]
```

---

### Problem 8: XOR of All Numbers in a Range [L, R]

Compute `L ^ (L+1) ^ ... ^ R` in O(1) time.

**Difficulty:** Medium

```
Input: L = 3, R = 9
Output: 3 ^ 4 ^ 5 ^ 6 ^ 7 ^ 8 ^ 9 = 2
```

```python
def xor_from_zero(n: int) -> int:
    """
    Compute XOR of all integers from 0 to n in O(1).

    The pattern repeats every 4 values:
      n % 4 == 0 → n
      n % 4 == 1 → 1
      n % 4 == 2 → n + 1
      n % 4 == 3 → 0
    """
    remainder = n % 4
    if remainder == 0:
        return n
    elif remainder == 1:
        return 1
    elif remainder == 2:
        return n + 1
    else:  # remainder == 3
        return 0


def xor_range(left: int, right: int) -> int:
    """
    Compute XOR of all integers in [left, right].

    Key insight: XOR(L..R) = XOR(0..R) ^ XOR(0..L-1)
    Because XOR(0..L-1) cancels the prefix, leaving only L..R.

    Time: O(1)
    Space: O(1)
    """
    return xor_from_zero(right) ^ xor_from_zero(left - 1)


# Test
print(xor_range(3, 9))   # 2
print(xor_range(1, 1))   # 1
print(xor_range(5, 8))   # 5 ^ 6 ^ 7 ^ 8 = 12

# Verify with brute force
from functools import reduce
from operator import xor
print(reduce(xor, range(3, 10)))  # 2 ✓
print(reduce(xor, range(5, 9)))   # 12 ✓
```

**Why the mod 4 pattern works:**

```
Every group of 4 consecutive numbers starting at a multiple of 4
XORs to 0:

  4k ^ (4k+1) ^ (4k+2) ^ (4k+3) = 0

The last 2 bits cycle through 00, 01, 10, 11 → XOR is 00.
Higher bits appear 4 times each (even count) → cancel to 0.

So XOR(0..n) only depends on the "leftover" after removing
complete groups of 4, which is determined by n % 4.
```

---

### Problem 9: Sum of Two Integers Without + or - (LeetCode 371)

Calculate the sum of two integers without using the `+` or `-` operators.

**Difficulty:** Medium

```
Input: a = 5, b = 3
Output: 8

Input: a = -1, b = 1
Output: 0
```

```python
def get_sum(a: int, b: int) -> int:
    """
    Add two integers using bit manipulation.

    XOR gives the sum without carries.
    AND gives positions where both bits are 1 (carry sources).
    Shift carry left by 1 (carry propagates to next column).
    Repeat until there are no carries.

    Python integers have arbitrary precision, so we must mask
    to 32 bits to simulate fixed-width arithmetic. Without this,
    negative numbers cause an infinite loop.

    Time: O(1) — at most 32 iterations
    Space: O(1)
    """
    MASK = 0xFFFFFFFF      # 32-bit mask
    MAX_INT = 0x7FFFFFFF   # Largest positive 32-bit signed int

    # Mask inputs to 32 bits
    a &= MASK
    b &= MASK

    while b != 0:
        carry = (a & b) << 1
        a = (a ^ b) & MASK
        b = carry & MASK

    # If the 32-bit result has its sign bit set, convert to negative
    return a if a <= MAX_INT else ~(a ^ MASK)


# Test
print(get_sum(5, 3))    # 8
print(get_sum(1, 2))    # 3
print(get_sum(-1, 1))   # 0
print(get_sum(-2, -3))  # -5
```

---

### Problem 10: Maximum XOR of Two Numbers in an Array (LeetCode 421)

Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]`
where `0 <= i < j < n`.

**Difficulty:** Hard

```
Input: nums = [3, 10, 5, 25, 2, 8]
Output: 28  (5 ^ 25 = 28)

Input: nums = [14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70]
Output: 127  (91 ^ 36 = 127)
```

```python
def find_maximum_xor(nums: list[int]) -> int:
    """
    Find the maximum XOR of any two numbers in the array.

    Greedy approach: build the answer bit by bit from the MSB down.
    At each bit position, check if we can set that bit to 1 in the
    answer by using the property: if a ^ b = c, then a ^ c = b.

    For each candidate answer (current best with the next bit set),
    store all prefixes in a set. If any two prefixes XOR to give
    the candidate, that candidate is achievable.

    Time: O(32 * n) = O(n)
    Space: O(n)
    """
    max_xor = 0
    mask = 0

    # Determine the highest bit position across all numbers
    max_num = max(nums)
    highest_bit = max_num.bit_length() - 1

    for i in range(highest_bit, -1, -1):
        # Grow the mask to include bit i
        mask |= (1 << i)

        # Extract prefixes (bits from highest down to i) for all nums
        prefixes = set()
        for num in nums:
            prefixes.add(num & mask)

        # Tentatively set bit i in the answer
        candidate = max_xor | (1 << i)

        # Check if any two prefixes XOR to give the candidate
        # If prefix1 ^ prefix2 = candidate, then prefix1 ^ candidate = prefix2
        for prefix in prefixes:
            if (prefix ^ candidate) in prefixes:
                max_xor = candidate
                break

    return max_xor


# Test
print(find_maximum_xor([3, 10, 5, 25, 2, 8]))  # 28
print(find_maximum_xor([14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70]))  # 127
print(find_maximum_xor([1, 2]))  # 3
print(find_maximum_xor([0, 0]))  # 0
```

**Why This Works (Walkthrough)**

```
nums = [3, 10, 5, 25, 2, 8]

In binary (5 bits):
  3  = 00011
  10 = 01010
  5  = 00101
  25 = 11001
  2  = 00010
  8  = 01000

We try to build the max XOR bit by bit from the MSB:

Bit 4 (16): Can we get a 1 here? Prefixes: {0, 1}
  candidate = 10000 (16). Is 0^1 = 1? No. Is 1^10000? 
  Check: 1 ^ 16 = 17, not in {0,1}. But 0 ^ 16 = 16, not in set.
  Actually check: prefix 1 → 1 ^ 16 = 17 not in set. prefix 0 → 0 ^ 16 = 16 not in set.
  Wait — prefix of 25 at mask 10000 is 10000 (16), and prefix of 3 is 00000 (0).
  16 ^ 16 = 0 ≠ candidate. But 0 ^ 16 = 16 = candidate. Yes! max_xor = 16.

Bit 3 (8): candidate = 11000 (24). Prefixes at mask 11000:
  3→00000, 10→01000, 5→00000, 25→11000, 2→00000, 8→01000
  Set: {0, 8, 24}. Check: 0^24=24 in set? Yes! max_xor = 24.

Bit 2 (4): candidate = 11100 (28). Prefixes at mask 11100:
  3→00000, 10→01000, 5→00100, 25→11000, 2→00000, 8→01000
  Set: {0, 8, 4, 24}. Check: 4^28=24 in set? Yes! max_xor = 28.

Bit 1 (2): candidate = 11110 (30). Prefixes at mask 11110:
  Set: {2, 10, 4, 24, 8}. No pair XORs to 30. max_xor stays 28.

Bit 0 (1): candidate = 11101 (29). Prefixes at mask 11111:
  Set: {3, 10, 5, 25, 2, 8}. No pair XORs to 29. max_xor stays 28.

Result: 28 = 5 ^ 25 ✓
```

---

## Common XOR Patterns (Quick Reference)

### 1. Find Single in Pairs

```python
def find_single(nums: list[int]) -> int:
    """XOR all elements; pairs cancel, single remains."""
    result = 0
    for num in nums:
        result ^= num
    return result
```

### 2. Toggle a Specific Bit

```python
def toggle_bit(n: int, pos: int) -> int:
    """Flip the bit at position `pos` (0-indexed from LSB)."""
    return n ^ (1 << pos)
```

### 3. Check if Two Numbers Have Opposite Signs

```python
def opposite_signs(a: int, b: int) -> bool:
    """
    XOR of two numbers with different signs has the sign bit set.
    Works in Python because negative integers are internally
    represented using two's complement.

    Note: treats 0 as non-negative, so opposite_signs(0, -5) returns True.
    Add an explicit zero check if you need opposite_signs(0, x) = False.
    """
    return (a ^ b) < 0
```

### 4. XOR of Range [0, n] in O(1)

```python
def xor_from_zero(n: int) -> int:
    """See Problem 8 for full explanation."""
    remainder = n % 4
    if remainder == 0:
        return n
    elif remainder == 1:
        return 1
    elif remainder == 2:
        return n + 1
    else:
        return 0
```

### 5. Check if Two Integers Are Equal (Without ==)

```python
def are_equal(a: int, b: int) -> bool:
    """a ^ b is 0 if and only if a == b."""
    return (a ^ b) == 0
```

---

## Complexity Summary

| Problem                 | Time    | Space | Key Technique               |
| ----------------------- | ------- | ----- | --------------------------- |
| Swap Without Temp       | O(1)    | O(1)  | Triple XOR                  |
| Single Number           | O(n)    | O(1)  | XOR all elements            |
| Missing Number          | O(n)    | O(1)  | XOR indices and values      |
| Decode XORed Array      | O(n)    | O(n)  | XOR reversibility           |
| Find Duplicate (XOR)    | O(n)    | O(1)  | XOR array and range         |
| Single Number III       | O(n)    | O(1)  | XOR + partition by diff bit |
| Two Missing Numbers     | O(n)    | O(1)  | XOR + partition by diff bit |
| XOR of Range [L, R]     | O(1)    | O(1)  | Mod 4 pattern               |
| Sum of Two Integers     | O(1)    | O(1)  | XOR for sum, AND for carry  |
| Maximum XOR of Two Nums | O(32n)  | O(n)  | Greedy bit-by-bit + hashset |

---

## Edge Cases

1. **Empty array**: Handle before any XOR loop
2. **Single element**: XOR result is that element itself
3. **All same elements (even count)**: XOR gives 0
4. **Negative numbers**: XOR works the same on two's complement integers
5. **Same variable on both sides**: XOR swap zeroes the value (aliasing bug)
6. **Overflow**: Not an issue in Python (arbitrary precision integers)

---

## Interview Tips

1. **Know the six XOR properties cold**: Self-inverse, identity, commutative, associative, pair cancellation, reversibility
2. **Draw the XOR truth table** if the interviewer asks — it shows you understand the operation at the bit level
3. **Explain why pairs cancel**: a ^ a = 0, so duplicate values vanish
4. **State time/space complexity**: XOR solutions typically give O(1) space vs. hash table O(n)
5. **Mention limitations**: XOR loses ordering, does not work with floats, aliasing hazard with swap
6. **Know the mod 4 pattern**: XOR(0..n) in O(1) is a common building block

---

## LeetCode Practice Problems

| #   | Problem                                  | Difficulty | Key Concept                |
| --- | ---------------------------------------- | ---------- | -------------------------- |
| 1   | 136. Single Number                       | Easy       | XOR all elements           |
| 2   | 268. Missing Number                      | Easy       | XOR indices and values     |
| 3   | 1720. Decode XORed Array                 | Easy       | XOR reversibility          |
| 4   | 1486. XOR Operation in an Array          | Easy       | XOR range pattern          |
| 5   | 371. Sum of Two Integers                 | Medium     | XOR for sum, AND for carry |
| 6   | 260. Single Number III                   | Medium     | XOR + partition            |
| 7   | 1310. XOR Queries of a Subarray          | Medium     | Prefix XOR                 |
| 8   | 137. Single Number II                    | Medium     | Generalized bit counting   |
| 9   | 421. Maximum XOR of Two Numbers in Array | Medium     | Greedy + hashset / Trie    |

---

## Related Sections

- [Binary Basics](./01-binary-basics.md) — XOR operator fundamentals
- [Single Number](./02-single-number.md) — Classic XOR applications
- [Bit Manipulation Tricks](./06-bit-manipulation-tricks.md) — More techniques
