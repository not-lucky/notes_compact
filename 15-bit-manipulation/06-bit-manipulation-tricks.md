# Bit Manipulation Tricks

> **Prerequisites:** [Binary Basics](./01-binary-basics.md), [Counting Bits](./03-counting-bits.md)

## Interview Context

This section is a compendium of bit manipulation tricks that appear across various interview problems. These techniques are building blocks that combine to solve complex problems elegantly.

---

## Building Intuition

**Why These Tricks Work: The Underlying Patterns**

Most bit tricks exploit a few core patterns. Understanding these patterns helps you derive tricks rather than memorize them.

**Pattern 1: Subtraction Creates a "Ripple" Effect**

When you compute `n - 1`, the binary subtraction causes a ripple from the rightmost bit leftward until it finds a 1 to borrow from:

```
n = 12 = 1100
        ↓
n - 1:  We need to subtract 1 from rightmost position
        Position 0 is 0, can't borrow → ripples left
        Position 1 is 0, can't borrow → ripples left
        Position 2 is 1, BORROW!
        Positions 0,1 become 1 (borrowed value distributed)
        Position 2 becomes 0

n - 1 = 11 = 1011

Key insight: n-1 flips the rightmost 1 to 0 and all 0s to its right become 1s
```

This pattern underlies:

- `n & (n-1)`: Clear rightmost set bit
- Power of 2 check: Only one bit means clearing it gives 0
- Brian Kernighan's algorithm: Each step removes exactly one bit

**Pattern 2: Two's Complement Creates a "Mirror" Effect**

In two's complement, `-n = ~n + 1`. This means `-n` has the same rightmost set bit as `n`, but everything else is inverted:

```
n = 12 = 0...01100
~n =     1...10011
~n+1 =   1...10100 = -12

Notice: The rightmost 1 and everything to its right is the SAME!
        Everything to the left is INVERTED!

n & (-n) keeps only the rightmost 1 (where they agree)
```

This pattern underlies:

- `n & (-n)`: Isolate rightmost set bit
- Fenwick trees (Binary Indexed Trees)

**Pattern 3: OR Propagates 1s, AND Propagates 0s**

```
OR with 1 → sets that bit to 1 (regardless of original)
OR with 0 → keeps original

AND with 0 → sets that bit to 0 (regardless of original)
AND with 1 → keeps original

This is why:
- Set bit i: n | (1 << i)    — OR with 1 at position i
- Clear bit i: n & ~(1 << i) — AND with 0 at position i
```

**Pattern 4: XOR Toggles**

```
XOR with 1 → flips the bit
XOR with 0 → keeps the bit

This is why:
- Toggle bit i: n ^ (1 << i)
- Swap without temp: uses three XORs to toggle values through each other
```

**Pattern 5: Shifting is Multiplication/Division by 2**

```
Each left shift = × 2
Each right shift = ÷ 2 (floor)

But more powerfully:
Left shift "makes room" at the right for new bits
Right shift "examines" bits by moving them to position 0

n >> i & 1 = get bit at position i (shift it to position 0, then mask)
```

**The "Mask" Mental Model**

Think of bit operations as applying a "mask" over the number:

```
AND mask: Keeps only where mask has 1s (like a stencil)
          n & 0x00FF → keeps only bottom 8 bits

OR mask:  Sets bits where mask has 1s
          n | 0x00FF → sets bottom 8 bits to 1

XOR mask: Flips bits where mask has 1s
          n ^ 0x00FF → flips bottom 8 bits
```

---

## When NOT to Use Bit Tricks

**1. When Clarity is More Important**

Bit tricks are compact but often cryptic:

```python
# Cryptic
is_odd = n & 1

# Clear (and compiled to same code)
is_odd = n % 2 == 1

# In production code, prefer the clear version
# In interviews, use bit version and explain it
```

**2. When Working with Negative Numbers in Python**

Python's arbitrary-precision integers don't have fixed bit width:

```python
# In C: ~5 = -6 (assuming 32-bit)
# In Python: ~5 = -6, but the "bit representation" is conceptually infinite

# Many tricks assume 32-bit integers
# You need explicit masking in Python:
result = (~n) & 0xFFFFFFFF  # Force 32-bit behavior
```

**3. For Non-Integer Types**

Bit operations are for integers only:

```python
# Strings, floats, objects — no bit operations
"hello" ^ "world"  # TypeError
3.14 & 2           # TypeError
```

**4. When the "Trick" is Actually Slower**

Some bit tricks that seem clever are actually slower:

```python
# Computing floor(n/2):
n >> 1        # Bit shift
n // 2        # Integer division

# On modern CPUs, these compile to the same instruction
# But division by non-power-of-2 is different:
n >> 1  # Always shift
n // 3  # Actually does division, can't optimize to shift
```

**5. When You Don't Fully Understand It**

Using a trick you don't understand leads to bugs:

```python
# "I saw this swap trick online"
a ^= b
b ^= a
a ^= b
# Works correctly but is confusing — prefer a, b = b, a in Python.

# If you can't explain why it works, don't use it in an interview
```

**Red Flags (Don't Use Bit Tricks):**

- Production code where maintainability matters
- Python with arbitrary-width integers (need explicit masking)
- You can't explain WHY the trick works
- The readable version is just as efficient
- Non-integer types

---

## Trick 1: Isolate the Rightmost Set Bit

```python
def isolate_rightmost_set_bit(n: int) -> int:
    """
    Isolate the rightmost 1 bit.

    Formula: n & (-n)

    Why it works:
    -n = ~n + 1 (two's complement)
    This flips all bits and adds 1, which means:
    - All bits left of rightmost 1 become opposite
    - Rightmost 1 stays 1
    - All bits right of it (were 0, flipped to 1, +1 ripples through) become 0

    So n and -n agree ONLY at the rightmost set bit. AND keeps only that bit.

    Example walkthrough:
      n  = 12 = 1100
      ~n =      0011
      -n = ~n+1 = 0100

      1100 & 0100 = 0100 = 4  (rightmost set bit isolated)

    Time: O(1)
    """
    return n & (-n)


# Examples
print(bin(isolate_rightmost_set_bit(12)))  # 0b100  (12=1100, rightmost 1 at position 2)
print(bin(isolate_rightmost_set_bit(10)))  # 0b10   (10=1010, rightmost 1 at position 1)
print(bin(isolate_rightmost_set_bit(8)))   # 0b1000 (8=1000, only bit is position 3)
```

### Visualization

```
n = 12 = 1100
-n =     0100 (two's complement: ~1100 + 1 = 0011 + 1 = 0100)

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
    n - 1 flips the rightmost 1 to 0 and all bits to its right become 1.
    ANDing n with n-1:
    - Bits left of the rightmost 1: same in both → preserved
    - The rightmost 1: is 1 in n but 0 in n-1 → cleared
    - Bits right of it: are 0 in n but 1 in n-1 → stay 0

    This is Brian Kernighan's trick!

    Example walkthrough:
      n     = 12 = 1100
      n - 1 = 11 = 1011

      1100 & 1011 = 1000 = 8

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
    n + 1 flips the rightmost 0 to 1 (carry ripples through any trailing 1s).
    - At the rightmost 0: n has 0, n+1 has 1 → OR gives 1 (set!)
    - Left of the rightmost 0: same in both → preserved by OR
    - Right of the rightmost 0 (trailing 1s that got flipped by carry):
      n has 1s there, so OR preserves them regardless of n+1

    Example walkthrough:
      n     = 12 = 1100
      n + 1 = 13 = 1101

      1100 | 1101 = 1101 = 13

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
def turn_off_trailing_ones(n: int) -> int:
    """
    Turn off all trailing 1s (rightmost consecutive 1s).

    Formula: n & (n + 1)

    Why it works:
    When n has trailing 1s (e.g., ...10111), adding 1 ripples the carry
    through those trailing 1s, turning them to 0 and setting the next 0 to 1:
      n     = 10111
      n + 1 = 11000

    ANDing: bits left of the trailing block are the same → preserved.
    The trailing 1s in n are 0 in n+1 → cleared by AND.

    Example walkthrough:
      n     = 0b1011 = 11
      n + 1 = 0b1100 = 12

      1011 & 1100 = 1000 = 8  (trailing "11" cleared)

    Time: O(1)
    """
    return n & (n + 1)


# Examples
print(bin(turn_off_trailing_ones(0b1011)))  # 0b1000
print(bin(turn_off_trailing_ones(0b1111)))  # 0b0
print(bin(turn_off_trailing_ones(0b1100)))  # 0b1100 (no trailing 1s)
```

---

## Trick 5: Check if Integer is Power of 2

```python
def is_power_of_two(n: int) -> bool:
    """
    Check if n is a power of 2.

    Formula: n > 0 and (n & (n - 1)) == 0

    Why: Powers of 2 have exactly one set bit (e.g., 8 = 1000).
    n & (n-1) clears the rightmost set bit. If that was the ONLY bit,
    the result is 0. If there were other bits, they remain.

    Must also check n > 0 because 0 has no set bits and would
    pass the AND test (0 & -1 = 0).

    Time: O(1)
    """
    return n > 0 and (n & (n - 1)) == 0


# Examples
print(is_power_of_two(8))   # True  (1000 — one set bit)
print(is_power_of_two(6))   # False (110 — two set bits)
print(is_power_of_two(1))   # True  (2^0 = 1)
print(is_power_of_two(0))   # False (no set bits)
```

---

## Trick 6: Get/Set/Clear/Toggle Bit at Position

```python
def get_bit(n: int, pos: int) -> int:
    """
    Get bit at position pos (0-indexed from the right / LSB).

    Shift n right by pos so the target bit is at position 0,
    then AND with 1 to isolate it.
    """
    return (n >> pos) & 1


def set_bit(n: int, pos: int) -> int:
    """
    Set bit at position pos to 1.

    Create a mask with only bit pos set (1 << pos),
    then OR with n. OR with 1 always produces 1.
    """
    return n | (1 << pos)


def clear_bit(n: int, pos: int) -> int:
    """
    Clear bit at position pos to 0.

    Create a mask with all bits set EXCEPT position pos: ~(1 << pos).
    AND with n. AND with 0 always produces 0.
    """
    return n & ~(1 << pos)


def toggle_bit(n: int, pos: int) -> int:
    """
    Toggle (flip) the bit at position pos.

    XOR with a mask that has bit pos set. XOR with 1 flips the bit.
    """
    return n ^ (1 << pos)


# Examples with n = 0b1010 (10)
n = 0b1010
print(f"n = {bin(n)}")                        # 0b1010
print(f"get_bit(n, 1) = {get_bit(n, 1)}")     # 1  (bit 1 is set)
print(f"get_bit(n, 0) = {get_bit(n, 0)}")     # 0  (bit 0 is clear)
print(f"set_bit(n, 0) = {bin(set_bit(n, 0))}") # 0b1011 (set bit 0)
print(f"clear_bit(n, 3) = {bin(clear_bit(n, 3))}") # 0b10 (clear bit 3)
print(f"toggle_bit(n, 2) = {bin(toggle_bit(n, 2))}") # 0b1110 (flip bit 2: 0→1)
```

---

## Trick 7: Reverse Bits of a 32-bit Integer

```python
def reverse_bits(n: int) -> int:
    """
    Reverse all 32 bits of an unsigned integer.

    LeetCode 190

    Approach: Extract each bit from the right, append it to the result
    on the left. After 32 iterations every bit has been mirrored.

    Time: O(1) — fixed 32 iterations
    Space: O(1)
    """
    result = 0
    for _ in range(32):
        # Shift result left to make room, then add the lowest bit of n
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


def reverse_bits_divide_and_conquer(n: int) -> int:
    """
    Reverse using parallel swapping (divide and conquer).

    The idea: recursively swap halves at every scale.
    1. Swap the two 16-bit halves
    2. Within each half, swap 8-bit quarters
    3. Within each quarter, swap 4-bit nibbles
    4. Within each nibble, swap 2-bit pairs
    5. Within each pair, swap adjacent bits

    Each step uses a mask to isolate the relevant groups,
    then shifts them into their swapped positions.

    Time: O(1) — exactly 5 operations
    Space: O(1)
    """
    n = ((n & 0xFFFF0000) >> 16) | ((n & 0x0000FFFF) << 16)  # Swap 16-bit halves
    n = ((n & 0xFF00FF00) >> 8)  | ((n & 0x00FF00FF) << 8)   # Swap 8-bit pairs
    n = ((n & 0xF0F0F0F0) >> 4)  | ((n & 0x0F0F0F0F) << 4)  # Swap 4-bit nibbles
    n = ((n & 0xCCCCCCCC) >> 2)  | ((n & 0x33333333) << 2)   # Swap 2-bit pairs
    n = ((n & 0xAAAAAAAA) >> 1)  | ((n & 0x55555555) << 1)   # Swap adjacent bits
    return n


# Example
original = 0b00000010100101000001111010011100
print(f"Original:  {bin(original)}")
print(f"Reversed:  {reverse_bits(original)}")  # 964176192
print(f"Reversed:  {bin(reverse_bits(original))}")
# 0b111001011110000010100101000000 (= 964176192)
print(f"Reversed (D&C): {reverse_bits_divide_and_conquer(original)}")  # 964176192
```

---

## Trick 8: Subsets Using Bitmask

```python
def generate_subsets(nums: list[int]) -> list[list[int]]:
    """
    Generate all subsets using bit manipulation.

    For n elements, iterate from 0 to 2^n - 1.
    Each integer in this range is a bitmask where bit i indicates
    whether nums[i] is included in the subset.

    LeetCode 78

    Why it works:
    There are 2^n possible subsets of n elements (each element is
    either included or excluded — 2 choices per element). A bitmask
    of n bits also has exactly 2^n values (0 to 2^n - 1). So there
    is a natural 1-to-1 mapping between bitmasks and subsets.

    Time: O(n * 2^n)
    Space: O(n * 2^n) for the output
    """
    n = len(nums)
    result = []

    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):  # If bit i is set, include nums[i]
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

### Iterating Over Subsets of a Bitmask

A powerful trick: iterate over all subsets of a given bitmask (not all subsets of the full set, but all sub-masks of a specific mask):

```python
def iterate_submasks(mask: int) -> list[int]:
    """
    Enumerate all submasks of a given bitmask, including 0.

    Why it works:
    Starting from mask itself, (submask - 1) & mask drops the lowest
    set bit of submask and fills in the lower bits that are present
    in the original mask. This systematically visits every submask
    in decreasing order.

    Time: O(2^k) where k = number of set bits in mask
    """
    submasks = []
    submask = mask
    while submask > 0:
        submasks.append(submask)
        submask = (submask - 1) & mask  # Next smaller submask
    submasks.append(0)  # Empty submask
    return submasks


# Example: all submasks of 0b1010
print([bin(s) for s in iterate_submasks(0b1010)])
# ['0b1010', '0b1000', '0b10', '0b0']
```

---

## Trick 9: Hamming Distance (Count Differing Bits)

```python
def hamming_distance(a: int, b: int) -> int:
    """
    Count the number of bit positions where a and b differ.

    LeetCode 461

    Why it works:
    XOR produces a 1 at every position where a and b differ,
    and 0 where they agree. Counting the 1s in the XOR result
    gives the Hamming distance.

    Time: O(k) where k = number of differing bits
    Space: O(1)
    """
    xor = a ^ b
    count = 0
    while xor:
        count += 1
        xor &= (xor - 1)  # Brian Kernighan's trick: clear rightmost set bit
    return count


def differing_bit_positions(a: int, b: int) -> list[int]:
    """
    Find all positions where a and b differ.

    Time: O(k) where k = number of differing bits
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


# Examples
print(hamming_distance(5, 9))             # 2  (5=0101, 9=1001 → XOR=1100)
print(differing_bit_positions(5, 9))      # [2, 3]
```

---

## Trick 10: Swap All Even and Odd Bits

```python
def swap_even_odd_bits(n: int) -> int:
    """
    Swap bits at even positions with bits at odd positions (32-bit).

    Positions are 0-indexed from the LSB:
      - Even positions: 0, 2, 4, ...  (mask: 0x55555555 = 01010101...)
      - Odd positions:  1, 3, 5, ...  (mask: 0xAAAAAAAA = 10101010...)

    Why it works:
    1. Extract bits at even positions using AND with 0x55555555
    2. Extract bits at odd positions using AND with 0xAAAAAAAA
    3. Shift even bits LEFT by 1 (moving them to odd positions)
    4. Shift odd bits RIGHT by 1 (moving them to even positions)
    5. OR the results to combine

    Time: O(1)
    """
    EVEN_MASK = 0x55555555  # Bits at even positions: 01010101...
    ODD_MASK = 0xAAAAAAAA   # Bits at odd positions:  10101010...

    even_bits = n & EVEN_MASK  # Isolate even-position bits
    odd_bits = n & ODD_MASK    # Isolate odd-position bits

    return (even_bits << 1) | (odd_bits >> 1)


# Example
print(bin(swap_even_odd_bits(0b10101010)))  # 0b1010101 (85; leading 0 dropped by bin())
print(bin(swap_even_odd_bits(0b11100010)))  # 0b11010001
```

---

## Trick 11: Gray Code

```python
def to_gray(n: int) -> int:
    """
    Convert binary to Gray code.
    Gray code: adjacent values differ by exactly one bit.

    Formula: n ^ (n >> 1)

    Why it works:
    In standard binary, incrementing can flip many bits (e.g., 0111 → 1000
    flips 4 bits). Gray code ensures only 1 bit changes at a time.

    n ^ (n >> 1) works because:
    - Bit i of the Gray code = bit i XOR bit (i+1) of the binary value
    - Adjacent binary numbers differ in a run of bits, but XORing with
      the shifted version cancels out all but the highest changed bit

    Time: O(1)
    """
    return n ^ (n >> 1)


def from_gray(gray: int) -> int:
    """
    Convert Gray code back to binary.

    Why it works:
    The highest bit is the same. Each subsequent bit is XOR of the
    Gray code bit and the previously decoded binary bit. We achieve
    this by repeatedly XORing with right-shifted versions of itself,
    doubling the shift each time (like a prefix XOR).

    Time: O(log n) — number of bits
    """
    n = gray
    shift = 1
    while (gray >> shift) > 0:
        n ^= (n >> shift)
        shift <<= 1  # Double the shift: 1, 2, 4, 8, ...
    return n


def generate_gray_code(num_bits: int) -> list[int]:
    """
    Generate num_bits-bit Gray code sequence.
    LeetCode 89

    Time: O(2^num_bits)
    """
    return [i ^ (i >> 1) for i in range(1 << num_bits)]


# Example
gray_sequence = generate_gray_code(3)
print([bin(x) for x in gray_sequence])
# ['0b0', '0b1', '0b11', '0b10', '0b110', '0b111', '0b101', '0b100']

# Verify: each adjacent pair differs by exactly 1 bit
for i in range(len(gray_sequence) - 1):
    diff = gray_sequence[i] ^ gray_sequence[i + 1]
    assert diff & (diff - 1) == 0, "Should differ by exactly 1 bit"
```

---

## Trick 12: Find Position of Only Set Bit

```python
def position_of_only_set_bit(n: int) -> int:
    """
    If n has exactly one set bit (i.e., n is a power of 2),
    return that bit's position. Returns -1 otherwise.

    Time: O(log n)
    """
    if n <= 0 or (n & (n - 1)) != 0:
        return -1  # Not exactly one set bit

    position = 0
    while n > 1:
        n >>= 1
        position += 1
    return position


def position_of_only_set_bit_builtin(n: int) -> int:
    """Same as above using Python built-in."""
    if n <= 0 or (n & (n - 1)) != 0:
        return -1
    return n.bit_length() - 1


# Examples
print(position_of_only_set_bit(8))   # 3  (1000 → bit 3)
print(position_of_only_set_bit(16))  # 4  (10000 → bit 4)
print(position_of_only_set_bit(5))   # -1 (101 → not a power of 2)
```

---

## Trick 13: Absolute Value Without Branching

```python
def abs_without_branching(n: int) -> int:
    """
    Get absolute value without using if/else (for 32-bit signed integer).

    Why it works:
    mask = n >> 31 produces:
      - 0 (all 0s) if n >= 0  (arithmetic shift preserves sign bit)
      - -1 (all 1s in two's complement) if n < 0

    If n >= 0: (n + 0) ^ 0 = n              → unchanged
    If n < 0:  (n + (-1)) ^ (-1) = (n - 1) ^ (-1)
               XOR with all 1s = bitwise NOT = ~(n - 1) = -n  → positive

    Note: This relies on arithmetic right shift and 32-bit integer semantics.
    In Python, arithmetic right shift preserves the sign, so n >> 31 yields
    -1 for negative n and 0 for non-negative n — but ONLY for values in
    the 32-bit signed range [-2^31, 2^31 - 1]. Outside that range, the
    shift result is wrong. In practice, just use abs(n). This is educational.

    Time: O(1)
    """
    mask = n >> 31  # -1 if negative, 0 if positive (arithmetic shift)
    return (n + mask) ^ mask


# Examples (only correct for 32-bit signed range: -2^31 to 2^31 - 1)
print(abs_without_branching(-5))  # 5
print(abs_without_branching(5))   # 5
print(abs_without_branching(0))   # 0
```

---

## Trick 14: Minimum/Maximum Without Branching

```python
def min_without_branching(a: int, b: int) -> int:
    """
    Find minimum without using if or ternary.

    Why it works:
    (a < b) is True (1) or False (0) in Python.
    -(a < b) is -1 (all 1s) or 0 (all 0s).

    If a < b: (a ^ b) & -1 = a ^ b, so b ^ (a ^ b) = a = min
    If a >= b: (a ^ b) & 0 = 0, so b ^ 0 = b = min

    Note: Primarily educational. Use min() in practice.
    """
    return b ^ ((a ^ b) & -(a < b))


def max_without_branching(a: int, b: int) -> int:
    """
    Find maximum without branching.

    If a < b: (a ^ b) & -1 = a ^ b, so a ^ (a ^ b) = b = max
    If a >= b: (a ^ b) & 0 = 0, so a ^ 0 = a = max
    """
    return a ^ ((a ^ b) & -(a < b))


# Examples
print(min_without_branching(3, 5))  # 3
print(max_without_branching(3, 5))  # 5
print(min_without_branching(7, 2))  # 2
print(max_without_branching(7, 2))  # 7
```

---

## Common Bitmasks Reference

```python
# 32-bit masks
ALL_ONES_32 = 0xFFFFFFFF       # 11111111 11111111 11111111 11111111
EVEN_POS    = 0x55555555       # 01010101 01010101 01010101 01010101 (positions 0,2,4,...)
ODD_POS     = 0xAAAAAAAA       # 10101010 10101010 10101010 10101010 (positions 1,3,5,...)
HIGH_HALF   = 0xFFFF0000       # Upper 16 bits
LOW_HALF    = 0x0000FFFF       # Lower 16 bits

# Useful for extracting bytes
BYTE_0 = 0x000000FF  # Lowest byte  (bits 0-7)
BYTE_1 = 0x0000FF00  # Second byte  (bits 8-15)
BYTE_2 = 0x00FF0000  # Third byte   (bits 16-23)
BYTE_3 = 0xFF000000  # Highest byte (bits 24-31)

# Bit count masks (used in parallel bit counting / popcount)
MASK_01 = 0x55555555  # 01010101... — isolate every other bit
MASK_0011 = 0x33333333  # 00110011... — isolate pairs
MASK_00001111 = 0x0F0F0F0F  # 00001111... — isolate nibbles
```

---

## Complexity Analysis

| Trick                | Time       | Space  | Common Use                |
| -------------------- | ---------- | ------ | ------------------------- |
| Isolate rightmost 1  | O(1)       | O(1)   | Loop control, BIT/Fenwick |
| Clear rightmost 1    | O(1)       | O(1)   | Counting bits, power of 2 |
| Get/Set/Clear/Toggle | O(1)       | O(1)   | Bit manipulation basics   |
| Reverse bits         | O(1)       | O(1)   | Networking, cryptography  |
| Generate subsets     | O(n * 2^n) | O(2^n) | Backtracking alternative  |
| Hamming distance     | O(k)       | O(1)   | Error detection, diff     |
| Gray code            | O(1)       | O(1)   | Error-resistant encoding  |

---

## Interview Tips

1. **Know the formulas**: `n & (n-1)`, `n & (-n)`, `n ^ (n >> 1)`
2. **Explain why they work**: Draw out the bit patterns
3. **Recognize when to use bitmasks**: Subsets, flags, state compression
4. **Start with simpler approach**: Then optimize with bit tricks
5. **Practice reading binary**: Quick mental conversion helps
6. **Watch for Python pitfalls**: Arbitrary-precision integers need explicit 32-bit masking

---

## Practice Problems

Problems are arranged in progressive difficulty. Each exercises tricks from this file specifically. For problems covered in other sections (LeetCode 190, 461, 78, 338, 260), see the [Related Sections](#related-sections) links.

---

### Problem 1: Bit Masking — Extract and Replace a Bit Field (Medium)

> Extract bits [lo, hi] from an integer, or replace them with a new value.

```python
def extract_bits(n: int, lo: int, hi: int) -> int:
    """
    Extract bits from position lo to hi (inclusive, 0-indexed from LSB).

    Steps:
    1. Create a mask with (hi - lo + 1) ones: (1 << width) - 1
    2. Shift n right by lo to bring the target field to position 0
    3. AND with the mask to isolate only those bits

    Example: extract bits [1, 3] from 0b11010110
      n >> 1 = 0b1101011
      mask = 0b111 (3 bits wide)
      result = 0b011 = 3
    """
    width = hi - lo + 1
    mask = (1 << width) - 1
    return (n >> lo) & mask


def replace_bits(n: int, lo: int, hi: int, value: int) -> int:
    """
    Replace bits [lo, hi] in n with the given value.

    Steps:
    1. Create a mask covering [lo, hi] and invert it to clear those bits in n
    2. Shift value into position and OR it in

    Example: replace bits [1, 3] of 0b11010110 with 0b101
      Clear: 0b11010110 & ~(0b1110) = 0b11010000
      Insert: 0b101 << 1 = 0b1010
      Result: 0b11011010
    """
    width = hi - lo + 1
    mask = ((1 << width) - 1) << lo  # Mask covering [lo, hi]
    cleared = n & ~mask              # Clear the target bits
    return cleared | ((value & ((1 << width) - 1)) << lo)  # Insert new value


# Examples
n = 0b11010110  # 214
print(bin(extract_bits(n, 1, 3)))       # 0b11 (bits 1-3 of 11010110 = 011)
print(bin(replace_bits(n, 1, 3, 0b101)))  # 0b11011010 (replaced bits 1-3 with 101)
```

---

### Problem 2: Bitwise AND of a Range [m, n] (Medium)

**LeetCode 201**: See [04-power-of-two.md](./04-power-of-two.md) for full solution and two approaches (shift until equal, Brian Kernighan's trick). Key idea: the result is the common binary prefix of `left` and `right`, with lower bits zeroed.

---

### Problem 3: Next Higher Number With Same Number of Set Bits (Medium)

> Given a positive integer `n`, find the smallest integer greater than `n`
> that has the same number of 1-bits. This is a classic trick combining
> isolate-rightmost-bit, clear-rightmost-bit, and shifting.

```python
def next_higher_same_bits(n: int) -> int:
    """
    Find the next integer > n with the same popcount.

    Algorithm (Gosper's hack):
    1. Isolate the rightmost set bit: c = n & (-n)
    2. Add c to n — this clears the trailing run of 1s and sets the
       next higher 0 to 1: r = n + c
    3. XOR r with n to get the bits that changed, then divide by c
       and right-shift by 2 to get the "leftover" 1s that need to be
       packed into the lowest positions.
    4. OR r with the packed bits.

    Example: n = 0b10110 (22)
      c = 0b10 (rightmost set bit)
      r = 0b11000 (22 + 2 = 24)
      xor = 0b01110, xor // c = 0b0111, >> 2 = 0b01 = 1
      result = 0b11000 | 0b01 = 0b11001 = 25

      Verify: popcount(22) = 3, popcount(25) = 3 ✓

    Time: O(1)
    Space: O(1)
    """
    c = n & (-n)              # Rightmost set bit
    r = n + c                 # Ripple carry: clears trailing 1s, sets next 0
    leftover = ((r ^ n) >> 2) // c  # Pack remaining 1s to lowest positions
    return r | leftover


# Tests
print(next_higher_same_bits(6))   # 9   (110 → 1001, both have two 1s)
print(next_higher_same_bits(22))  # 25  (10110 → 11001, both have three 1s)
print(next_higher_same_bits(12))  # 17  (01100 → 10001, both have two 1s)
print(next_higher_same_bits(7))   # 11  (0111 → 1011, both have three 1s)

# Verify popcount is preserved
for val in [6, 22, 12, 7, 15, 31, 100]:
    nxt = next_higher_same_bits(val)
    assert bin(val).count('1') == bin(nxt).count('1'), f"Failed for {val}"
    assert nxt > val, f"Not higher for {val}"
```

---

### Problem 4: Detect if Two Integers Have Opposite Signs (Easy)

> Given two integers, determine if they have opposite signs using bit
> manipulation. Uses the fact that XOR of two numbers with different
> sign bits produces a negative number.

```python
def opposite_signs(a: int, b: int) -> bool:
    """
    Check if a and b have opposite signs.

    Why it works:
    In two's complement, the MSB (sign bit) is 1 for negative, 0 for
    non-negative. XOR of two numbers with different sign bits sets the
    MSB of the result to 1, making it negative.

    Note: 0 is considered non-negative. So (0, -1) → True,
    (0, 1) → False.

    Time: O(1)
    """
    return (a ^ b) < 0


# Tests
print(opposite_signs(3, -5))    # True
print(opposite_signs(-3, -5))   # False
print(opposite_signs(3, 5))     # False
print(opposite_signs(0, -1))    # True
print(opposite_signs(0, 1))     # False
```

---

### Problem 5: Round Up to Next Power of Two (Easy)

> Given a positive integer `n`, find the smallest power of 2 that is >= `n`.
> Uses bit propagation to fill all bits below the highest set bit.

```python
def next_power_of_two(n: int) -> int:
    """
    Round up n to the next power of 2 (or n itself if already a power of 2).

    Why it works:
    1. Subtract 1 so that exact powers of 2 don't get doubled.
    2. Propagate the highest set bit downward by OR-shifting:
       after all shifts, every bit below the MSB is set.
    3. Add 1 to get the next power of 2.

    Example: n = 13 = 0b1101
      n - 1 = 12 = 0b1100
      After propagation: 0b1111 = 15
      15 + 1 = 16 (next power of 2)

    Time: O(1)  — fixed number of operations (5 shifts for 32-bit)
    """
    if n <= 0:
        return 1
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    return n + 1


# Tests
print(next_power_of_two(1))   # 1
print(next_power_of_two(5))   # 8
print(next_power_of_two(13))  # 16
print(next_power_of_two(16))  # 16  (already a power of 2)
print(next_power_of_two(17))  # 32
```

---

### Problem 6: Count Flips to Convert A to B (Easy)

> Given two integers `a` and `b`, count the minimum number of bit flips
> required to convert `a` to `b`. Combines XOR (to find differing bits)
> with Brian Kernighan's trick (to count them efficiently).

```python
def count_flips(a: int, b: int) -> int:
    """
    Count bits that need to flip to convert a to b.

    XOR marks every position where a and b differ.
    Then count set bits using Kernighan's trick.

    Time: O(k) where k = number of differing bits
    Space: O(1)
    """
    xor = a ^ b
    flips = 0
    while xor:
        xor &= (xor - 1)  # Clear rightmost set bit
        flips += 1
    return flips


# Tests
print(count_flips(10, 20))  # 4  (01010 vs 10100 → XOR=11110, 4 bits)
print(count_flips(7, 10))   # 3  (0111 vs 1010 → XOR=1101, 3 bits)
print(count_flips(0, 0))    # 0
```

---

### Problem 7: Bitmask DP — Minimum Cost to Visit All Cities (Medium)

> Given `n` cities (n <= 20) and a cost matrix `dist[i][j]`, find the minimum
> cost to visit every city starting from city 0 (Travelling Salesman variant).
> This is the classic bitmask DP problem where a bitmask tracks visited cities.

```python
def min_cost_visit_all(dist: list[list[int]]) -> int:
    """
    Bitmask DP for shortest Hamiltonian path from city 0.

    State: dp[mask][i] = minimum cost to reach city i having visited
    exactly the cities indicated by the set bits in mask.

    Transition: For each city j not in mask, try extending from i to j:
      dp[mask | (1 << j)][j] = min(dp[mask | (1 << j)][j],
                                    dp[mask][i] + dist[i][j])

    The bitmask iteration uses Trick 8 patterns: checking and setting
    individual bits to track which cities are in the visited set.

    Time: O(n^2 * 2^n)
    Space: O(n * 2^n)
    """
    n = len(dist)
    full_mask = (1 << n) - 1
    INF = float('inf')

    # dp[mask][i] = min cost to be at city i with visited set = mask
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Start at city 0, mask = 0b...001

    for mask in range(1 << n):
        for i in range(n):
            if dp[mask][i] == INF:
                continue
            if not (mask & (1 << i)):  # City i must be in the visited set
                continue
            for j in range(n):
                if mask & (1 << j):    # City j already visited
                    continue
                new_mask = mask | (1 << j)
                new_cost = dp[mask][i] + dist[i][j]
                if new_cost < dp[new_mask][j]:
                    dp[new_mask][j] = new_cost

    return min(dp[full_mask][i] for i in range(n))


# Test: 4 cities
dist = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0],
]
print(min_cost_visit_all(dist))  # 65  (path 0→1→3→2: 10+25+30=65)

# Verify with brute force for small input
from itertools import permutations
def brute_force(dist: list[list[int]]) -> int:
    n = len(dist)
    best = float('inf')
    for perm in permutations(range(1, n)):
        cost = dist[0][perm[0]]
        for k in range(len(perm) - 1):
            cost += dist[perm[k]][perm[k + 1]]
        best = min(best, cost)
    return best

assert min_cost_visit_all(dist) == brute_force(dist)
print("Verified against brute force")
```

---

### Problem 8: Gray Code Sequence (Medium)

> LeetCode 89. Generate an n-bit Gray code sequence (each adjacent pair
> differs by exactly one bit). Uses the `n ^ (n >> 1)` trick from Trick 11.

```python
def gray_code(n: int) -> list[int]:
    """
    Generate the n-bit Gray code sequence.

    Each value i maps to its Gray code via i ^ (i >> 1).
    The sequence has 2^n values where adjacent entries differ by 1 bit,
    and the last entry also differs from the first by 1 bit (cyclic).

    Time: O(2^n)
    Space: O(2^n)
    """
    return [i ^ (i >> 1) for i in range(1 << n)]


# Test
seq = gray_code(3)
print(seq)  # [0, 1, 3, 2, 6, 7, 5, 4]

# Verify: each adjacent pair (including wrap-around) differs by exactly 1 bit
for i in range(len(seq)):
    diff = seq[i] ^ seq[(i + 1) % len(seq)]
    assert diff & (diff - 1) == 0, f"Pair ({seq[i]}, {seq[(i+1)%len(seq)]}) differs by >1 bit"
print("All adjacent pairs differ by exactly 1 bit (including wrap-around)")
```

---

## Related Sections

- [Binary Basics](./01-binary-basics.md) - Operator fundamentals
- [Single Number](./02-single-number.md) - XOR applications
- [Power of Two](./04-power-of-two.md) - n & (n-1) applications
- [XOR Tricks](./05-xor-tricks.md) - XOR-specific techniques
