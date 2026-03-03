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
= 3                        (identity: x ^ 0 = x)
```

**Single Number II Intuition: Bit Counting**

When numbers appear 3 times instead of 2, XOR doesn't directly work (3 is odd, so a triple XOR gives `a ^ a ^ a = a`, not 0). The insight is to think about EACH bit position independently:

```
If a bit appears 3k times across all numbers, it belongs to the triples.
If a bit appears 3k+1 times, the single number has that bit set.

Example: [2, 2, 3, 2] = [10, 10, 11, 10] in binary
Bit position 0: 0+0+1+0 = 1  (1 mod 3 = 1) -> single number has bit 0 set
Bit position 1: 1+1+1+1 = 4  (4 mod 3 = 1) -> single number has bit 1 set

Single number = 11 binary = 3 decimal
```

**Single Number III Intuition: Divide and Conquer with XOR**

When there are TWO unique numbers, XORing everything gives us `a ^ b`, not the individual values. But this result tells us WHERE a and b differ:

```
If bit i is set in (a ^ b), then a and b have different values at bit i.
We can use ANY such bit to partition all numbers into two groups:
- Group 1: numbers with bit i = 0
- Group 2: numbers with bit i = 1

a and b go to DIFFERENT groups (they differ at bit i by definition).
Paired numbers go to the SAME group (they have identical bits).

Now XOR each group separately -> each reveals its unique number!
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

XOR finds elements appearing an ODD number of times. If every element appears an even number of times, XOR gives 0 regardless:

```python
# XOR treats "never appeared" the same as "appeared twice"
nums_all_paired = [1, 1, 2, 2, 3, 3]  # XOR = 0, all elements appeared twice
nums_single = [4]                       # XOR = 4, the single element
```

**2. When You Need the Duplicate, Not the Unique**

Finding duplicates is a different problem. XOR cancels duplicates, which is exactly what you DON'T want:

```python
# Find duplicate in [1, 2, 3, 2]
# XOR: 1 ^ 2 ^ 3 ^ 2 = 1 ^ 3 = 2 -> seems to give 2 (the duplicate)
# But this is misleading!
#
# XOR gives the XOR of elements that appear an odd number of times.
# Here, 1 and 3 each appear once (odd), so XOR = 1^3 = 2.
# The result equals the duplicate only by coincidence.
#
# Consider [1, 3, 4, 2, 2] with range [1..4]:
# XOR all values: 1^3^4^2^2 = 1^3^4 = 6
# That's NOT the duplicate (2). The odd-occurring elements are 1, 3, 4.
#
# For "find the duplicate" problems, use Floyd's cycle detection or a hashset.
```

**3. When Multiple Elements Have Odd Occurrences**

XOR gives the XOR of ALL odd-occurring elements combined, not individual values:

```python
# [1, 1, 2, 3] -> 1 appears twice, 2 appears once, 3 appears once
# XOR: 1^1^2^3 = 0^2^3 = 1
# Result is 2^3 = 1, not [2, 3] individually. Not directly useful.
# (Single Number III handles exactly 2 unique elements with extra work.)
```

**4. When You Need Count Information**

If you need "how many times does the single element appear?", XOR can't help -- it only tells you WHAT the element is (for Single Number I) or requires state machines (Single Number II).

**Red Flags (Don't Use XOR):**

- "Find the duplicate" (not the unique)
- Elements can appear any number of times (not constrained to pairs + one)
- You need to preserve or count occurrences
- More than 2 unique elements among pairs (unless using Single Number III variant)

---

## Pattern: XOR for Finding Unique Elements

The key XOR properties that make these problems solvable:

```
1. a ^ a = 0     (self-cancellation)
2. a ^ 0 = a     (identity)
3. a ^ b = b ^ a (commutative)
4. (a ^ b) ^ c = a ^ (b ^ c) (associative)

Result: XORing all elements cancels out pairs, leaving the unique element.
```

### Visualization

```
Array: [4, 1, 2, 1, 2]

XOR all elements:
  4 ^ 1 ^ 2 ^ 1 ^ 2
= 4 ^ (1 ^ 1) ^ (2 ^ 2)  (reorder by commutativity + associativity)
= 4 ^ 0 ^ 0               (a ^ a = 0)
= 4                        (a ^ 0 = a)

The single number is 4!
```

---

## Problem 1: Single Number I

**LeetCode 136** | Easy

Given a non-empty array where every element appears twice except for one, find the single one. Must run in O(n) time and O(1) space.

### Examples

```
Input:  [2, 2, 1]
Output: 1

Input:  [4, 1, 2, 1, 2]
Output: 4
```

### Solution

```python
def single_number(nums: list[int]) -> int:
    """
    Find the element that appears only once (all others appear twice).

    Approach: XOR all elements. Pairs cancel out (a ^ a = 0),
    leaving only the unique element (0 ^ unique = unique).

    Time:  O(n) - single pass
    Space: O(1) - one variable
    """
    result = 0
    for num in nums:
        result ^= num
    return result


# Alternative: one-liner using reduce
from functools import reduce
from operator import xor

def single_number_reduce(nums: list[int]) -> int:
    """Single Number I using functools.reduce for a concise one-liner."""
    return reduce(xor, nums)


# Tests
assert single_number([2, 2, 1]) == 1
assert single_number([4, 1, 2, 1, 2]) == 4
assert single_number([7]) == 7
assert single_number_reduce([4, 1, 2, 1, 2]) == 4
```

### Step-by-Step Walkthrough

```
Input: [4, 1, 2, 1, 2]

Binary representations:
  4 = 100
  1 = 001
  2 = 010

XOR step by step (result starts at 000):

  result = 000
       XOR 100  (num = 4)
         = 100

  result = 100
       XOR 001  (num = 1)
         = 101

  result = 101
       XOR 010  (num = 2)
         = 111

  result = 111
       XOR 001  (num = 1, cancels the earlier 1)
         = 110

  result = 110
       XOR 010  (num = 2, cancels the earlier 2)
         = 100

Final result: 100 = 4
```

---

## Problem 2: Single Number II

**LeetCode 137** | Medium

Every element appears three times except for one element which appears exactly once. Find the single one. Must run in O(n) time and O(1) space.

### Examples

```
Input:  [2, 2, 3, 2]
Output: 3

Input:  [0, 1, 0, 1, 0, 1, 99]
Output: 99
```

### Solution 1: Bit Counting (Intuitive)

```python
def single_number_ii_bitcount(nums: list[int]) -> int:
    """
    Find element appearing once when all others appear 3 times.

    Approach: For each of the 32 bit positions, count how many numbers
    have a 1 at that position. If count % 3 != 0, the unique number
    must have a 1 at that position.

    Time:  O(32 * n) = O(n)
    Space: O(1)
    """
    result = 0

    for bit_pos in range(32):
        bit_count = 0
        for num in nums:
            # Check if bit at bit_pos is set in num
            bit_count += (num >> bit_pos) & 1

        # If count is not divisible by 3, the unique number has this bit set
        if bit_count % 3:
            result |= (1 << bit_pos)

    # Handle negative numbers in Python (two's complement)
    if result >= 2**31:
        result -= 2**32

    return result


# Tests
assert single_number_ii_bitcount([2, 2, 3, 2]) == 3
assert single_number_ii_bitcount([0, 1, 0, 1, 0, 1, 99]) == 99
assert single_number_ii_bitcount([-2, -2, 1, -2]) == 1
```

### Bit Counting Walkthrough

```
Input: [2, 2, 3, 2]

Binary:  2 = 10,  3 = 11

Bit position 0 (ones place):
  2 -> 0,  2 -> 0,  3 -> 1,  2 -> 0
  Count = 1,  1 % 3 = 1  -> unique number has bit 0 SET

Bit position 1 (twos place):
  2 -> 1,  2 -> 1,  3 -> 1,  2 -> 1
  Count = 4,  4 % 3 = 1  -> unique number has bit 1 SET

All higher bits: count = 0, 0 % 3 = 0 -> NOT SET

Result: bit 1 and bit 0 set -> 11 binary = 3
```

### Solution 2: State Machine (Optimal)

```python
def single_number_ii(nums: list[int]) -> int:
    """
    Find element appearing once when all others appear 3 times.

    Approach: Use two bitmasks (ones, twos) to track how many times
    each bit has been seen, modulo 3.

    State transitions for each bit position:
      (ones, twos): count mod 3
      (0, 0) -> count = 0  (seen 0 or 3 times)
      (1, 0) -> count = 1  (seen 1 time)
      (0, 1) -> count = 2  (seen 2 times)

    When a new 1 arrives at a bit position:
      (0, 0) -> (1, 0)  : 0 -> 1
      (1, 0) -> (0, 1)  : 1 -> 2
      (0, 1) -> (0, 0)  : 2 -> 3 (reset to 0)

    The formulas that achieve this:
      ones = (ones ^ num) & ~twos
      twos = (twos ^ num) & ~ones

    Time:  O(n)
    Space: O(1)
    """
    ones = 0  # Bits seen 1 time (mod 3)
    twos = 0  # Bits seen 2 times (mod 3)

    for num in nums:
        ones = (ones ^ num) & ~twos
        twos = (twos ^ num) & ~ones

    return ones


# Tests
assert single_number_ii([2, 2, 3, 2]) == 3
assert single_number_ii([0, 1, 0, 1, 0, 1, 99]) == 99
assert single_number_ii([-2, -2, 1, -2]) == 1  # Works with negatives in Python
```

### State Machine Walkthrough

```
Input: [3, 3, 3, 5]
Binary: 3 = 011,  5 = 101

Initial: ones = 000, twos = 000

After first 3 (011):
  ones = (000 ^ 011) & ~000 = 011 & 111 = 011
  twos = (000 ^ 011) & ~011 = 011 & 100 = 000
  State: ones=011, twos=000  (3 seen once)

After second 3 (011):
  ones = (011 ^ 011) & ~000 = 000 & 111 = 000
  twos = (000 ^ 011) & ~000 = 011 & 111 = 011
  State: ones=000, twos=011  (3 seen twice)

After third 3 (011):
  ones = (000 ^ 011) & ~011 = 011 & 100 = 000
  twos = (011 ^ 011) & ~000 = 000 & 111 = 000
  State: ones=000, twos=000  (3 seen 3 times -> reset!)

After 5 (101):
  ones = (000 ^ 101) & ~000 = 101 & 111 = 101
  twos = (000 ^ 101) & ~101 = 101 & 010 = 000
  State: ones=101, twos=000  (5 seen once)

Result: ones = 101 = 5
```

### Why the State Machine Formulas Work

```
ones = (ones ^ num) & ~twos

  (ones ^ num):  toggles bits from num into ones
  & ~twos:       clears any bit that's already in twos
                 (prevents a bit from being in both ones and twos)

twos = (twos ^ num) & ~ones

  (twos ^ num):  toggles bits from num into twos
  & ~ones:       clears any bit that just moved into ones
                 (the updated ones from the line above)

The order matters: ones is updated first, then twos uses the NEW ones.
This ensures the state transition happens atomically per bit.
```

---

## Problem 3: Single Number III

**LeetCode 260** | Medium

Exactly two elements appear once while all others appear twice. Find both unique elements.

### Examples

```
Input:  [1, 2, 1, 3, 2, 5]
Output: [3, 5]  (order doesn't matter)

Input:  [0, 1]
Output: [0, 1]
```

### Solution

```python
def single_number_iii(nums: list[int]) -> list[int]:
    """
    Find TWO elements that appear only once (all others appear twice).

    Approach:
    1. XOR all elements -> gives xor_all = a ^ b (the two uniques XORed)
    2. Find any set bit in xor_all (where a and b differ)
    3. Use that bit to partition all numbers into two groups
    4. XOR each group separately to isolate a and b

    Why partitioning works:
    - a and b differ at the chosen bit, so they go to DIFFERENT groups
    - Every paired number has identical bits, so both copies go to the SAME group
    - XOR within each group cancels pairs, leaving only the unique element

    Time:  O(n) - two passes
    Space: O(1)
    """
    # Step 1: XOR all to get a ^ b
    xor_all = 0
    for num in nums:
        xor_all ^= num

    # Step 2: Isolate the rightmost set bit (any set bit works)
    # x & (-x) gives the lowest set bit due to two's complement:
    #   -x flips all bits and adds 1, which turns off everything
    #   above the lowest set bit and keeps only that bit after AND
    diff_bit = xor_all & (-xor_all)

    # Step 3: Partition into two groups and XOR each
    num_a = 0
    num_b = 0
    for num in nums:
        if num & diff_bit:
            num_a ^= num  # Group: bit is set
        else:
            num_b ^= num  # Group: bit is clear

    return [num_a, num_b]


# Tests
result = single_number_iii([1, 2, 1, 3, 2, 5])
assert set(result) == {3, 5}

result = single_number_iii([0, 1])
assert set(result) == {0, 1}
```

### Step-by-Step Walkthrough

```
Input: [1, 2, 1, 3, 2, 5]

Binary: 1=001, 2=010, 3=011, 5=101

Step 1: XOR all elements
  1 ^ 2 ^ 1 ^ 3 ^ 2 ^ 5
  = (1^1) ^ (2^2) ^ (3^5)
  = 0 ^ 0 ^ 6
  = 6  (binary: 110)

  This tells us: 3 ^ 5 = 6.
  Bits 1 and 2 are set, meaning 3 and 5 differ at those positions.

Step 2: Isolate rightmost set bit
  6 & (-6)
  = 110 & 010     (in two's complement, -6 = ...11111010)
  = 010
  = 2

  We'll use bit position 1 to separate the two groups.

Step 3: Partition by bit 1 (value 2)
  1 = 001, bit 1 = 0 -> Group B
  2 = 010, bit 1 = 1 -> Group A
  1 = 001, bit 1 = 0 -> Group B
  3 = 011, bit 1 = 1 -> Group A
  2 = 010, bit 1 = 1 -> Group A
  5 = 101, bit 1 = 0 -> Group B

  Group A (bit set):   [2, 3, 2] -> XOR = 2^3^2 = 3
  Group B (bit clear): [1, 1, 5] -> XOR = 1^1^5 = 5

Result: [3, 5]
```

---

## Problem 4: Missing Number

**LeetCode 268** | Easy

Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.

### Examples

```
Input:  [3, 0, 1]
Output: 2  (range is [0, 3], missing 2)

Input:  [0, 1]
Output: 2  (range is [0, 2], missing 2)

Input:  [9, 6, 4, 2, 3, 5, 7, 0, 1]
Output: 8
```

### Solution

```python
def missing_number(nums: list[int]) -> int:
    """
    Find the missing number in range [0, n].

    Approach: XOR all numbers in the array with all numbers in [0, n].
    Every number that exists in both will cancel out (a ^ a = 0),
    leaving only the missing number.

    This is essentially Single Number I in disguise: imagine concatenating
    the array with [0, 1, 2, ..., n]. The missing number appears once;
    every other number appears twice.

    Time:  O(n)
    Space: O(1)
    """
    n = len(nums)
    result = n  # Start with n (since range is [0, n] but indices are [0, n-1])

    for i in range(n):
        result ^= i ^ nums[i]

    return result


# Alternative: using the sum formula (but can overflow in other languages)
def missing_number_sum(nums: list[int]) -> int:
    """Find the missing number using Gauss's sum formula."""
    n = len(nums)
    expected_sum = n * (n + 1) // 2
    return expected_sum - sum(nums)


# Tests
assert missing_number([3, 0, 1]) == 2
assert missing_number([0, 1]) == 2
assert missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
assert missing_number([0]) == 1
```

### Why XOR Works Here

```
Input: [3, 0, 1],  n = 3,  range = [0, 1, 2, 3]

We XOR indices [0, 1, 2] with array values [3, 0, 1] and include n=3:

  result = 3           (start with n)
  result ^= 0 ^ 3     (i=0, nums[0]=3)  -> result = 3 ^ 0 ^ 3 = 0
  result ^= 1 ^ 0     (i=1, nums[1]=0)  -> result = 0 ^ 1 ^ 0 = 1
  result ^= 2 ^ 1     (i=2, nums[2]=1)  -> result = 1 ^ 2 ^ 1 = 2

Equivalently, we computed:
  3 ^ (0 ^ 3) ^ (1 ^ 0) ^ (2 ^ 1)
  = (0 ^ 1 ^ 2 ^ 3) ^ (3 ^ 0 ^ 1)       (regroup: indices vs values)
  = (0^0) ^ (1^1) ^ (3^3) ^ 2             (pairs cancel)
  = 2                                       (the missing number)
```

---

## Problem 5: Find the Duplicate Number (Non-XOR)

**LeetCode 287** | Medium

Given an array of `n + 1` integers where each integer is in the range `[1, n]`, there is exactly one repeated number (but it could appear more than twice). Find it.

> **Note:** This problem cannot be solved with XOR alone because the duplicate may appear more than twice and some numbers in `[1, n]` may be missing. Use Floyd's cycle detection instead.

### Example

```
Input:  [1, 3, 4, 2, 2]
Output: 2

Input:  [3, 1, 3, 4, 2]
Output: 3
```

### Solution: Floyd's Cycle Detection

```python
def find_duplicate(nums: list[int]) -> int:
    """
    Find the duplicate number using Floyd's tortoise and hare algorithm.

    Key insight: Treat the array as a linked list where nums[i] points
    to the next node. Since there's a duplicate, two indices point to
    the same value, creating a cycle. The duplicate is the cycle entrance.

    Time:  O(n)
    Space: O(1)
    """
    # Phase 1: Detect cycle (find meeting point)
    slow = nums[0]
    fast = nums[0]

    while True:
        slow = nums[slow]          # Move 1 step
        fast = nums[nums[fast]]    # Move 2 steps
        if slow == fast:
            break

    # Phase 2: Find cycle entrance (the duplicate)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow


# Tests
assert find_duplicate([1, 3, 4, 2, 2]) == 2
assert find_duplicate([3, 1, 3, 4, 2]) == 3
assert find_duplicate([1, 1]) == 1
```

### Why XOR Doesn't Work Here

```
XOR approach attempt for [1, 3, 4, 2, 2]:
  XOR all values: 1 ^ 3 ^ 4 ^ 2 ^ 2 = 1 ^ 3 ^ 4 = 6
  XOR with range [1..4]: 1 ^ 2 ^ 3 ^ 4 = 4
  6 ^ 4 = 2 -> happens to give the right answer!

But this only works when there's exactly one extra copy.
For [3, 1, 3, 3, 2] (3 appears three times, 4 is missing):
  XOR all: 3^1^3^3^2 = 3^1^2 = 0
  XOR range [1..4]: 1^2^3^4 = 4
  0 ^ 4 = 4 -> WRONG (answer is 3)

The problem allows any distribution, so XOR is unreliable here.
```

---

## Problem 6: XOR Queries of a Subarray

**LeetCode 1310** | Medium

Given an array `arr` and a list of queries where each query is `[left, right]`, return the XOR of elements from index `left` to `right` (inclusive).

### Example

```
Input:  arr = [1, 3, 4, 8], queries = [[0, 1], [1, 2], [0, 3], [3, 3]]
Output: [2, 7, 14, 8]

Explanation:
  [0,1]: 1 ^ 3 = 2
  [1,2]: 3 ^ 4 = 7
  [0,3]: 1 ^ 3 ^ 4 ^ 8 = 14
  [3,3]: 8 = 8
```

### Solution: Prefix XOR

```python
def xor_queries(arr: list[int], queries: list[list[int]]) -> list[int]:
    """
    Answer XOR range queries efficiently using a prefix XOR array.

    Just like prefix sums allow O(1) range sum queries, prefix XOR
    allows O(1) range XOR queries. This works because:
      (a ^ b ^ c) ^ (a ^ b) = c
    XOR "undoes" itself, so subtracting a prefix is just XORing it.

    prefix[i] = arr[0] ^ arr[1] ^ ... ^ arr[i-1]
    XOR(left, right) = prefix[right+1] ^ prefix[left]

    Time:  O(n + q) where q = number of queries
    Space: O(n) for the prefix array
    """
    n = len(arr)

    # Build prefix XOR array
    # prefix[i] = XOR of arr[0..i-1], prefix[0] = 0
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] ^ arr[i]

    # Answer each query in O(1)
    results = []
    for left, right in queries:
        results.append(prefix[right + 1] ^ prefix[left])

    return results


# Tests
assert xor_queries([1, 3, 4, 8], [[0, 1], [1, 2], [0, 3], [3, 3]]) == [2, 7, 14, 8]
assert xor_queries([4, 8, 2, 10], [[2, 3], [1, 3], [0, 0], [0, 3]]) == [8, 0, 4, 4]
```

### Why Prefix XOR Works

```
arr    = [1,   3,   4,   8  ]
prefix = [0,   1,   2,   6,  14]
          ^    ^    ^    ^    ^
          |    |    |    |    1^3^4^8
          |    |    |    1^3^4
          |    |    1^3
          |    1
          (empty)

Query [1, 2] -> XOR of arr[1..2] = 3 ^ 4 = 7
  prefix[3] ^ prefix[1] = 6 ^ 1 = 7

  Why? prefix[3] = 1^3^4, prefix[1] = 1
       (1^3^4) ^ (1) = 3^4   (the 1 cancels out!)
```

---

## Complexity Summary

| Problem              | Time   | Space | Technique                     |
| -------------------- | ------ | ----- | ----------------------------- |
| Single Number I      | O(n)   | O(1)  | XOR all elements              |
| Single Number II     | O(n)   | O(1)  | Bit counting or state machine |
| Single Number III    | O(n)   | O(1)  | XOR + partition by diff bit   |
| Missing Number       | O(n)   | O(1)  | XOR indices with values       |
| Find Duplicate       | O(n)   | O(1)  | Floyd's cycle detection       |
| XOR Subarray Queries | O(n+q) | O(n)  | Prefix XOR                    |

---

## Generalization: Element Appearing Once, Others k Times

```python
def single_number_k_times(nums: list[int], k: int) -> int:
    """
    Find element appearing once when all others appear exactly k times.

    Approach: Same bit-counting idea as Single Number II, but mod k
    instead of mod 3. If a bit's total count mod k != 0, the unique
    number has that bit set.

    Time:  O(32 * n) = O(n)
    Space: O(1)
    """
    result = 0
    for bit_pos in range(32):
        bit_count = 0
        for num in nums:
            bit_count += (num >> bit_pos) & 1
        if bit_count % k:
            result |= (1 << bit_pos)

    # Handle negative numbers (Python two's complement)
    if result >= 2**31:
        result -= 2**32
    return result


# Tests
assert single_number_k_times([2, 2, 3, 2], 3) == 3           # k=3
assert single_number_k_times([5, 5, 5, 5, 9], 4) == 9        # k=4
assert single_number_k_times([1, 1, 1, 1, 1, 7], 5) == 7     # k=5
```

---

## Edge Cases

1. **Single element array**: `[x]` -> return `x`. XOR with 0 gives `x`.
2. **Negative numbers**: XOR works identically on negative numbers in Python. Bit counting needs two's complement handling (the `result -= 2**32` pattern).
3. **Zero in array**: `0 ^ x = x`, so zero participates correctly in XOR.
4. **Very large arrays**: All algorithms remain O(n) time, O(1) space.
5. **All elements identical except one**: Standard case, works directly.

---

## Interview Tips

1. **Start with Single Number I**: It's the foundation. Explain XOR properties clearly before jumping to the solution.
2. **Draw the binary**: Trace through a small example bit by bit. This demonstrates understanding and catches errors.
3. **Know the tradeoffs**:
   - Hash map: O(n) time, O(n) space -- simple to implement, easy to explain
   - Bit manipulation: O(n) time, O(1) space -- demonstrates deeper knowledge
4. **Explain WHY, not just HOW**: "XOR cancels pairs because `a ^ a = 0`" is better than "we just XOR everything."
5. **Handle negatives**: For Single Number II, mention two's complement. In Python, integers have arbitrary precision, so you need the `result -= 2**32` adjustment.
6. **Know the limits**: Be upfront about when XOR doesn't apply (see "When NOT to Use" section).

---

## Practice Problems

| #   | Problem                   | Difficulty | Key Concept             | LeetCode |
| --- | ------------------------- | ---------- | ----------------------- | -------- |
| 1   | Single Number             | Easy       | Basic XOR               | 136      |
| 2   | Missing Number            | Easy       | XOR indices with values | 268      |
| 3   | Single Number II          | Medium     | Bit counting / state    | 137      |
| 4   | Single Number III         | Medium     | XOR + partition         | 260      |
| 5   | Find the Duplicate Number | Medium     | Floyd's (not XOR)       | 287      |
| 6   | XOR Queries of a Subarray | Medium     | Prefix XOR              | 1310     |
| 7   | Complement of Base 10 Int | Easy       | XOR with mask           | 1009     |
| 8   | Total Hamming Distance    | Medium     | Bit counting per pos    | 477      |

---

## Related Sections

- [Binary Basics](./01-binary-basics.md) - XOR fundamentals
- [Counting Bits](./03-counting-bits.md) - Related bit techniques
- [XOR Tricks](./05-xor-tricks.md) - More XOR applications
