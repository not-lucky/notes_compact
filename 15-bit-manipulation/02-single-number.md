# Single Number

> **Prerequisites:** [Binary Basics](./01-binary-basics.md)

## Interview Context

The "Single Number" family of problems is a classic demonstration of XOR properties. These problems appear frequently in interviews because they test understanding of bit manipulation and require elegant O(1) space solutions.

---

## Building Intuition

**Why XOR is Perfect for Finding Unique Elements**

Imagine you have a bag of paired socks, except one sock has no pair. How do you find it? You could sort them and look for the odd one out, or you could use a hashmap to count. But XOR gives you a magical approach:

```
XOR is like a "toggle switch" for each bit position.
- See a 1? Toggle that bit.
- See the same 1 again? Toggle it back to original.

After processing all numbers, only the unique number's bits remain toggled.
```

**The Self-Cancellation Property is Key**

This single property makes everything work:

```
a ^ a = 0  (any number XOR'd with itself equals zero)

Why? Every bit position where a has a 1, XORing with itself means:
1 XOR 1 = 0 (bits are same, result is 0)

And where a has a 0:
0 XOR 0 = 0 (bits are same, result is 0)

So a ^ a = all zeros = 0
```

**Why Order Doesn't Matter**

XOR is both commutative and associative:

```
Commutative: a ^ b = b ^ a
Associative: (a ^ b) ^ c = a ^ (b ^ c)

This means we can regroup any XOR expression however we want.
Paired numbers will always find each other and cancel:

1 ^ 2 ^ 3 ^ 2 ^ 1
= (1 ^ 1) ^ (2 ^ 2) ^ 3  (regroup)
= 0 ^ 0 ^ 3               (pairs cancel)
= 3                       (identity: x ^ 0 = x)
```

**Single Number II Intuition: Bit Counting**

When numbers appear 3 times instead of 2, XOR doesn't directly work (3 is odd, so bits don't cancel). The insight is to think about EACH bit position independently:

```
If a bit appears 3k times across all numbers, it's from the triples.
If a bit appears 3k+1 times, the single number has that bit.

Example: [2, 2, 3, 2] = [10, 10, 11, 10] in binary
Bit position 0: 0+0+1+0 = 1  (mod 3 = 1) → single has bit 0
Bit position 1: 1+1+1+1 = 4  (mod 3 = 1) → single has bit 1

Single number = 11 binary = 3 decimal ✓
```

**Single Number III Intuition: Divide and Conquer with XOR**

When there are TWO unique numbers, XORing everything gives us `a ^ b`, not the individual values. But this result tells us WHERE a and b differ:

```
If bit i is set in (a ^ b), then a and b have different values at bit i.
We can use ANY such bit to partition all numbers into two groups:
- Group 1: numbers with bit i = 0
- Group 2: numbers with bit i = 1

a and b go to DIFFERENT groups.
Paired numbers go to the SAME group (they have identical bits).

Now XOR each group separately → each reveals its unique number!
```

**The Mental Model: XOR as a "Difference Accumulator"**

Think of XOR as accumulating differences:

```
Start with 0 (no differences seen)
Each number toggles its bit pattern into the accumulator
Seeing the same pattern twice cancels it out
What remains is the pattern that appeared an odd number of times
```

---

## When NOT to Use XOR for Finding Unique Elements

**1. When Duplicates Appear an Even Number of Times (Including 0)**

XOR finds elements appearing an ODD number of times. If you need to find elements appearing exactly once (not 0, not 2), XOR can't distinguish:

```python
# XOR treats "never appeared" the same as "appeared twice"
[1, 1, 2, 2, 3, 3]  # XOR gives 0, but ALL elements appeared twice
[4]                  # XOR gives 4, the single element
```

**2. When You Need the Duplicate, Not the Unique**

Finding duplicates is a different problem. XOR cancels duplicates, which is exactly what you DON'T want:

```python
# Find duplicate in [1, 2, 3, 2]
# XOR: 1 ^ 2 ^ 3 ^ 2 = 1 ^ 3 = 2... wait, this works?
# Only by coincidence! If array was [1, 2, 3, 1], XOR = 2^3 = 1... wrong!
```

For finding duplicates, use Floyd's cycle detection or hashset.

**3. When Multiple Elements Have Odd Occurrences**

XOR gives the XOR of ALL odd-occurring elements, not a list:

```python
[1, 1, 2, 3]  # 2 appears once, 3 appears once
# XOR: 1^1^2^3 = 0^2^3 = 2^3 = 1  ← Not useful!
```

**4. When You Need Count Information**

If you need "how many times does the single element appear?", XOR can't help—it only tells you WHAT the element is (for Single Number I) or requires state machines (Single Number II).

**Red Flags (Don't Use XOR):**
- "Find the duplicate" (not the unique)
- Elements can appear any number of times (not constrained to pairs+one)
- You need to preserve or count occurrences
- More than 2 unique elements among pairs

---

## Pattern: XOR for Finding Unique Elements

The key XOR properties that make these problems solvable:

```
1. a ^ a = 0     (self-cancellation)
2. a ^ 0 = a     (identity)
3. a ^ b = b ^ a (commutative)
4. (a ^ b) ^ c = a ^ (b ^ c) (associative)

Result: XORing all elements cancels out duplicates!
```

### Visualization

```
Array: [4, 1, 2, 1, 2]

XOR all elements:
  4 ^ 1 ^ 2 ^ 1 ^ 2
= 4 ^ (1 ^ 1) ^ (2 ^ 2)  (reorder by associativity)
= 4 ^ 0 ^ 0              (a ^ a = 0)
= 4                      (a ^ 0 = a)

The single number is 4!
```

---

## Problem: Single Number I

**LeetCode 136**: Given a non-empty array where every element appears twice except for one, find the single one. Must run in O(n) time and O(1) space.

### Example

```
Input: [2, 2, 1]
Output: 1

Input: [4, 1, 2, 1, 2]
Output: 4
```

### Solution

```python
def singleNumber(nums: list[int]) -> int:
    """
    Find the element that appears only once (all others appear twice).

    Approach: XOR all elements - pairs cancel out, leaving the single.

    Time: O(n) - single pass
    Space: O(1) - just one variable
    """
    result = 0
    for num in nums:
        result ^= num
    return result


# One-liner using reduce
from functools import reduce
def singleNumber_reduce(nums: list[int]) -> int:
    return reduce(lambda a, b: a ^ b, nums)


# Test
print(singleNumber([2, 2, 1]))        # 1
print(singleNumber([4, 1, 2, 1, 2]))  # 4
```

### Why XOR Works

```
Consider [4, 1, 2, 1, 2] in binary:

4 = 100
1 = 001
2 = 010
1 = 001
2 = 010

XOR step by step:
  000 (initial result)
^ 100 (4)
= 100

  100
^ 001 (1)
= 101

  101
^ 010 (2)
= 111

  111
^ 001 (1)  ← 1 appears again, cancels previous 1
= 110

  110
^ 010 (2)  ← 2 appears again, cancels previous 2
= 100 = 4

Final answer: 4
```

---

## Problem: Single Number II

**LeetCode 137**: Every element appears three times except for one. Find the single one. Must run in O(n) time and O(1) space.

### Example

```
Input: [2, 2, 3, 2]
Output: 3

Input: [0, 1, 0, 1, 0, 1, 99]
Output: 99
```

### Solution 1: Bit Counting

```python
def singleNumber2_bitcount(nums: list[int]) -> int:
    """
    Find element appearing once when others appear 3 times.

    Approach: Count each bit position across all numbers.
    If count % 3 != 0, the single number has a 1 at that position.

    Time: O(32n) = O(n)
    Space: O(1)
    """
    result = 0

    for i in range(32):
        bit_count = 0
        for num in nums:
            # Count how many numbers have bit i set
            bit_count += (num >> i) & 1

        # If count not divisible by 3, single number has this bit
        if bit_count % 3:
            result |= (1 << i)

    # Handle negative numbers (two's complement)
    if result >= 2**31:
        result -= 2**32

    return result
```

### Solution 2: State Machine (Optimal)

```python
def singleNumber2(nums: list[int]) -> int:
    """
    Find element appearing once when others appear 3 times.

    Approach: Use two variables (ones, twos) as state machine.
    - ones: bits that have appeared 1 time (mod 3)
    - twos: bits that have appeared 2 times (mod 3)
    - When a bit appears 3 times, it's cleared from both

    Time: O(n)
    Space: O(1)
    """
    ones = 0  # Bits seen once
    twos = 0  # Bits seen twice

    for num in nums:
        # Add to ones if not in twos, then add to twos if was in ones
        ones = (ones ^ num) & ~twos
        twos = (twos ^ num) & ~ones

    return ones


# Test
print(singleNumber2([2, 2, 3, 2]))           # 3
print(singleNumber2([0, 1, 0, 1, 0, 1, 99]))  # 99
```

### State Machine Visualization

```
State transitions for each bit:
  (ones, twos) → after seeing a 1 at this bit position

  (0, 0) → (1, 0)  : seen once
  (1, 0) → (0, 1)  : seen twice
  (0, 1) → (0, 0)  : seen three times (reset!)

Example with [3, 3, 3, 5]:
  3 = 011, 5 = 101

  Initial: ones=000, twos=000

  After first 3 (011):
    ones = 011, twos = 000  (seen once)

  After second 3 (011):
    ones = 000, twos = 011  (seen twice)

  After third 3 (011):
    ones = 000, twos = 000  (reset!)

  After 5 (101):
    ones = 101, twos = 000  (5 seen once)

  Result: ones = 101 = 5
```

---

## Problem: Single Number III

**LeetCode 260**: Two elements appear exactly once while all others appear twice. Find both elements.

### Example

```
Input: [1, 2, 1, 3, 2, 5]
Output: [3, 5] (order doesn't matter)
```

### Solution

```python
def singleNumber3(nums: list[int]) -> list[int]:
    """
    Find TWO elements that appear only once (others appear twice).

    Approach:
    1. XOR all elements → gets a ^ b (the two singles XORed)
    2. Find any bit where a and b differ (they must differ somewhere!)
    3. Use that bit to partition array into two groups
    4. XOR each group to find each single number

    Time: O(n)
    Space: O(1)
    """
    # Step 1: XOR all to get a ^ b
    xor_all = 0
    for num in nums:
        xor_all ^= num

    # Step 2: Find rightmost set bit (where a and b differ)
    # This bit is 1 in one number and 0 in the other
    diff_bit = xor_all & (-xor_all)  # Isolates rightmost set bit

    # Step 3: Partition and XOR each group
    a, b = 0, 0
    for num in nums:
        if num & diff_bit:
            a ^= num  # Group where this bit is 1
        else:
            b ^= num  # Group where this bit is 0

    return [a, b]


# Test
print(singleNumber3([1, 2, 1, 3, 2, 5]))  # [3, 5] or [5, 3]
```

### Visualization

```
Array: [1, 2, 1, 3, 2, 5]

Step 1: XOR all
1 ^ 2 ^ 1 ^ 3 ^ 2 ^ 5
= (1^1) ^ (2^2) ^ (3^5)
= 0 ^ 0 ^ 6
= 6 (binary: 110)

Step 2: Find diff bit
6 & (-6) = 110 & 010 = 010 = 2
(The bit at position 1 differs between 3 and 5)

Step 3: Partition by bit 1
  Bit 1 is SET (= 1):    [2, 3, 2]   → 2^3^2 = 3
  Bit 1 is CLEAR (= 0):  [1, 1, 5]   → 1^1^5 = 5

Result: [3, 5]

Why does partitioning work?
- 3 = 011 (bit 1 is 1) → goes to first group
- 5 = 101 (bit 1 is 0) → goes to second group
- Paired numbers go to same group (both have same bit)
- XOR in each group cancels pairs, leaving the single
```

---

## Complexity Analysis

| Problem | Time | Space | Technique |
|---------|------|-------|-----------|
| Single Number I | O(n) | O(1) | XOR all elements |
| Single Number II | O(n) | O(1) | Bit counting or state machine |
| Single Number III | O(n) | O(1) | XOR + partition by diff bit |

---

## Common Variations

### 1. Find Element Appearing Once (Others k Times)

Generalization of Single Number II:

```python
def singleNumber_k_times(nums: list[int], k: int) -> int:
    """
    Find element appearing once when others appear k times.

    Time: O(32n) = O(n)
    Space: O(1)
    """
    result = 0
    for i in range(32):
        bit_count = sum((num >> i) & 1 for num in nums)
        if bit_count % k:
            result |= (1 << i)

    # Handle negative numbers
    if result >= 2**31:
        result -= 2**32
    return result
```

### 2. All Elements Appear Twice Except Two (Different Counts)

```python
def find_two_singles_different_counts(nums: list[int]) -> list[int]:
    """
    Find elements where one appears once, another appears 3 times,
    all others appear twice.

    This requires different approach (hash map or sorting).
    """
    from collections import Counter
    counts = Counter(nums)
    return [num for num, count in counts.items() if count in (1, 3)]
```

---

## Edge Cases

1. **Single element array**: Return that element
2. **All same elements**: Not valid for Single Number I (violates problem constraints)
3. **Negative numbers**: XOR works the same, but bit counting needs two's complement handling
4. **Zero in array**: Zero XOR'd with anything gives that thing, works correctly
5. **Large arrays**: Algorithm still O(n) and O(1) space

---

## Interview Tips

1. **Start with Single Number I**: It's the foundation for understanding XOR
2. **Explain XOR properties**: Show you understand why it works
3. **Draw bit examples**: Helps avoid mistakes and impresses interviewer
4. **Know the tradeoffs**:
   - Hash map: O(n) time, O(n) space (easier to implement)
   - Bit manipulation: O(n) time, O(1) space (impressive solution)
5. **Handle edge cases**: Especially negative numbers for Single Number II

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Single Number | Easy | Basic XOR |
| 2 | Single Number II | Medium | Bit counting / state machine |
| 3 | Single Number III | Medium | XOR + partition |
| 4 | Find the Duplicate Number | Medium | Different approach (Floyd's) |
| 5 | Missing Number | Easy | XOR with indices |

---

## Related Sections

- [Binary Basics](./01-binary-basics.md) - XOR fundamentals
- [XOR Tricks](./05-xor-tricks.md) - More XOR applications
- [Counting Bits](./03-counting-bits.md) - Related bit techniques
