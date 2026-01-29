# Set Operations

> **Prerequisites:** [01-hash-table-basics.md](./01-hash-table-basics.md)

## Interview Context

Sets provide **O(1) membership testing** and elegant solutions for:

- Intersection, union, difference problems
- Uniqueness and duplicate detection
- Cycle detection (Floyd's via set)
- Graph traversal visited tracking

The key insight: when you only care about existence (not count or order), use a set.

**Interview frequency**: Medium-high. Set operations appear as subproblems in many questions.

---

## Building Intuition

**Why Sets Over Lists for Membership?**

Lists check membership by scanning every element:

```python
# List: "Is 5 in here?" → Check index 0, 1, 2, ... → O(n)
5 in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Scans all elements
```

Sets use hashing:

```python
# Set: "Is 5 in here?" → hash(5) → check bucket → O(1)
5 in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}  # Direct lookup
```

**Mental Model: Filing Cabinet vs. Stack of Papers**

```
Stack of Papers (List):
"Find the red paper" → Flip through entire stack → O(n)

Filing Cabinet (Set):
"Find the red paper" → Open 'R' drawer → O(1)
```

**The XOR Trick Explained**

XOR has magical properties for "find the unique element":

```
a ^ a = 0      (anything XORed with itself is 0)
a ^ 0 = a      (anything XORed with 0 is itself)
XOR is commutative and associative

So: a ^ b ^ a = (a ^ a) ^ b = 0 ^ b = b

All duplicates cancel out, leaving only the unique element!
```

No extra space needed.

**Why "Check Sequence Start" for Longest Consecutive**

Naive approach:

```python
for num in nums:
    count = 1
    while num + 1 in set: ...  # Could recount same sequence many times!
```

Problem: If sequence is [1,2,3,4,5], we count:

- Starting at 1: length 5
- Starting at 2: length 4 (wasteful!)
- Starting at 3: length 3 (wasteful!)

Optimization: Only start counting from sequence START:

```python
if num - 1 not in set:  # This is the start!
    count from here
```

Now we count each element exactly once → O(n).

**Bidirectional Mapping for Isomorphism**

"egg" → "add": Is this a valid character replacement?

- e→a, g→d
- Both directions must be consistent

One-way mapping isn't enough:

```
"ab" → "cc": a→c, b→c
One-way: looks fine (each letter maps somewhere)
But: two different letters map to same letter → NOT isomorphic
```

Need BOTH:

- s_to_t: each s-char maps to exactly one t-char
- t_to_s: each t-char maps to exactly one s-char

---

## When NOT to Use Sets

**1. Order Matters**

Sets are unordered:

```python
s = {3, 1, 2}
list(s)  # Could be [1, 2, 3] or [2, 1, 3] or...
```

If you need insertion order: use dict (Python 3.7+) or list.

**2. Need to Count Occurrences**

Sets only store existence, not frequency:

```python
{1, 1, 1, 2, 2, 3}  # Becomes {1, 2, 3}
```

For counts, use Counter or dict.

**3. Need to Preserve Duplicates**

Intersection with counts (how many times does element appear in both?):

```python
# Set intersection: [1,1,2] ∩ [1,1,1] = {1, 2}... loses count info
# Need Counter for: [1,1,2] ∩ [1,1,1] = [1,1]
```

**4. Elements Aren't Hashable**

Can't put lists or dicts in a set:

```python
{[1, 2], [3, 4]}  # TypeError!
# Convert to tuples: {(1, 2), (3, 4)}
```

**5. Need Sorted Operations**

Finding "closest element" or "range of elements":

```python
# Set: O(n) to find element closest to x
# Sorted structure (BST, sorted list): O(log n)
```

Use `sortedcontainers.SortedSet` for ordered set operations.

**Red Flags:**

- "Maintain insertion order" → dict or list
- "Count occurrences in intersection" → Counter
- "Find closest element" → Sorted structure
- "Keys are lists or dicts" → Convert to tuples

---

## Core Concept

A set is an unordered collection of **unique elements** with O(1) average-case operations.

```python
s = {1, 2, 3}

# O(1) operations
1 in s           # True
s.add(4)         # {1, 2, 3, 4}
s.remove(1)      # {2, 3, 4}
s.discard(99)    # No error if missing
```

---

## Python Set Operations

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Union (elements in a OR b)
a | b            # {1, 2, 3, 4, 5, 6}
a.union(b)       # Same

# Intersection (elements in a AND b)
a & b            # {3, 4}
a.intersection(b)

# Difference (elements in a but NOT in b)
a - b            # {1, 2}
a.difference(b)

# Symmetric Difference (elements in a OR b but NOT both)
a ^ b            # {1, 2, 5, 6}
a.symmetric_difference(b)

# Subset/Superset
{1, 2} <= a      # True (subset)
a >= {1, 2}      # True (superset)
{1, 2} < a       # True (proper subset)
```

### Complexity Table

| Operation      | Method         | Time Complexity        |
| -------------- | -------------- | ---------------------- |
| Add            | `s.add(x)`     | O(1) average           |
| Remove         | `s.remove(x)`  | O(1) average           |
| Discard        | `s.discard(x)` | O(1) average           |
| Membership     | `x in s`       | O(1) average           |
| Union          | `a \| b`       | O(len(a) + len(b))     |
| Intersection   | `a & b`        | O(min(len(a), len(b))) |
| Difference     | `a - b`        | O(len(a))              |
| Symmetric Diff | `a ^ b`        | O(len(a) + len(b))     |

---

## Template: Intersection of Two Arrays

```python
def intersection(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Find elements that appear in both arrays (unique).

    Time: O(n + m)
    Space: O(n + m)

    Example:
    [1, 2, 2, 1], [2, 2] → [2]
    """
    return list(set(nums1) & set(nums2))
```

---

## Template: Intersection of Two Arrays II (With Frequency)

```python
def intersect(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Find intersection including duplicates (by frequency).

    Time: O(n + m)
    Space: O(min(n, m))

    Example:
    [1, 2, 2, 1], [2, 2] → [2, 2]
    """
    from collections import Counter

    # Use smaller array for counter
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    count = Counter(nums1)
    result = []

    for num in nums2:
        if count[num] > 0:
            result.append(num)
            count[num] -= 1

    return result
```

### Follow-up: Sorted Arrays

```python
def intersect_sorted(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    If arrays are sorted, use two pointers for O(1) space.

    Time: O(n + m)
    Space: O(1) excluding output
    """
    result = []
    i = j = 0

    while i < len(nums1) and j < len(nums2):
        if nums1[i] == nums2[j]:
            result.append(nums1[i])
            i += 1
            j += 1
        elif nums1[i] < nums2[j]:
            i += 1
        else:
            j += 1

    return result
```

---

## Template: Union of Arrays

```python
def union(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Find all unique elements from both arrays.

    Time: O(n + m)
    Space: O(n + m)
    """
    return list(set(nums1) | set(nums2))
```

---

## Template: Set Difference

```python
def difference(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Find elements in nums1 but not in nums2.

    Time: O(n + m)
    Space: O(n + m)
    """
    return list(set(nums1) - set(nums2))
```

---

## Template: Find the Difference (XOR Trick)

```python
def find_the_difference(s: str, t: str) -> str:
    """
    t is s with one extra character. Find it.

    Time: O(n)
    Space: O(1)
    """
    result = 0

    for char in s + t:
        result ^= ord(char)

    return chr(result)
```

---

## Template: Contains Duplicate

```python
def contains_duplicate(nums: list[int]) -> bool:
    """
    Check if any element appears more than once.

    Time: O(n)
    Space: O(n)
    """
    return len(nums) != len(set(nums))


def contains_duplicate_early_exit(nums: list[int]) -> bool:
    """
    Early exit version - better for large arrays with early duplicates.
    """
    seen = set()

    for num in nums:
        if num in seen:
            return True
        seen.add(num)

    return False
```

---

## Template: Single Number

```python
def single_number(nums: list[int]) -> int:
    """
    Every element appears twice except one. Find it.

    Time: O(n)
    Space: O(1) with XOR
    """
    result = 0
    for num in nums:
        result ^= num
    return result


def single_number_set(nums: list[int]) -> list[int]:
    """
    Alternative: 2 * sum(set) - sum(nums) = single element.

    Works because: 2(a + b + c) - (a + a + b + b + c) = c
    """
    return 2 * sum(set(nums)) - sum(nums)
```

---

## Template: Single Number III (Two Unique Numbers)

```python
def single_number_iii(nums: list[int]) -> list[int]:
    """
    All elements appear twice except two. Find them.

    Time: O(n)
    Space: O(1)

    Example:
    [1, 2, 1, 3, 2, 5] → [3, 5]
    """
    # XOR all numbers: result = a ^ b (two unique numbers)
    xor = 0
    for num in nums:
        xor ^= num

    # Find a bit where a and b differ
    diff_bit = xor & (-xor)  # Rightmost set bit

    # Partition numbers by this bit
    a = b = 0
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num

    return [a, b]
```

---

## Template: Happy Number

```python
def is_happy(n: int) -> bool:
    """
    A happy number eventually reaches 1 after repeated digit square sum.

    Time: O(log n) per step, O(log n) steps
    Space: O(log n) for set

    Example:
    19 → 82 → 68 → 100 → 1 (happy!)
    2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 (cycle, not happy)
    """
    def digit_square_sum(num):
        total = 0
        while num:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total

    seen = set()

    while n != 1 and n not in seen:
        seen.add(n)
        n = digit_square_sum(n)

    return n == 1


def is_happy_floyd(n: int) -> bool:
    """
    O(1) space using Floyd's cycle detection.
    """
    def digit_square_sum(num):
        total = 0
        while num:
            total += (num % 10) ** 2
            num //= 10
        return total

    slow = fast = n

    while True:
        slow = digit_square_sum(slow)
        fast = digit_square_sum(digit_square_sum(fast))

        if fast == 1:
            return True
        if slow == fast:
            return False
```

---

## Template: Longest Consecutive Sequence

```python
def longest_consecutive(nums: list[int]) -> int:
    """
    Find length of longest consecutive elements sequence.

    Time: O(n)
    Space: O(n)

    Example:
    [100, 4, 200, 1, 3, 2] → 4 (sequence: 1, 2, 3, 4)
    """
    if not nums:
        return 0

    num_set = set(nums)
    max_length = 0

    for num in num_set:
        # Only start counting from sequence start
        if num - 1 not in num_set:
            current = num
            length = 1

            while current + 1 in num_set:
                current += 1
                length += 1

            max_length = max(max_length, length)

    return max_length
```

### Visual Trace

```
nums = [100, 4, 200, 1, 3, 2]
num_set = {100, 4, 200, 1, 3, 2}

Check 100: 99 not in set → start sequence
  100+1=101 not in set → length=1

Check 4: 3 in set → not a start, skip

Check 200: 199 not in set → start sequence
  200+1=201 not in set → length=1

Check 1: 0 not in set → start sequence
  1+1=2 in set → length=2
  2+1=3 in set → length=3
  3+1=4 in set → length=4
  4+1=5 not in set → stop

Check 3: 2 in set → not a start, skip
Check 2: 1 in set → not a start, skip

Max length: 4
```

---

## Template: Missing Number

```python
def missing_number(nums: list[int]) -> int:
    """
    Find missing number in [0, n].

    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum


def missing_number_xor(nums: list[int]) -> int:
    """
    XOR approach: a ^ a = 0, so missing number remains.
    """
    result = len(nums)  # Include n

    for i, num in enumerate(nums):
        result ^= i ^ num

    return result


def missing_number_set(nums: list[int]) -> int:
    """
    Set approach (less efficient but clearer).
    """
    full_set = set(range(len(nums) + 1))
    return (full_set - set(nums)).pop()
```

---

## Template: Find All Numbers Disappeared

```python
def find_disappeared_numbers(nums: list[int]) -> list[int]:
    """
    Find all numbers in [1, n] not appearing in nums.

    Time: O(n)
    Space: O(1) excluding output - use array as set!
    """
    # Mark seen numbers by negating at that index
    for num in nums:
        index = abs(num) - 1
        nums[index] = -abs(nums[index])

    # Positive indices indicate missing numbers
    result = []
    for i in range(len(nums)):
        if nums[i] > 0:
            result.append(i + 1)

    return result
```

---

## Template: Isomorphic Strings

```python
def is_isomorphic(s: str, t: str) -> bool:
    """
    Check if characters in s can be replaced to get t.

    Time: O(n)
    Space: O(1) - limited alphabet

    Example:
    "egg", "add" → True (e→a, g→d)
    "foo", "bar" → False (o maps to both a and r)
    """
    if len(s) != len(t):
        return False

    s_to_t = {}
    t_to_s = {}

    for c1, c2 in zip(s, t):
        if c1 in s_to_t:
            if s_to_t[c1] != c2:
                return False
        else:
            s_to_t[c1] = c2

        if c2 in t_to_s:
            if t_to_s[c2] != c1:
                return False
        else:
            t_to_s[c2] = c1

    return True
```

---

## Template: Word Pattern

```python
def word_pattern(pattern: str, s: str) -> bool:
    """
    Check if words follow the same pattern.

    Time: O(n)
    Space: O(n)

    Example:
    pattern = "abba", s = "dog cat cat dog" → True
    """
    words = s.split()

    if len(pattern) != len(words):
        return False

    p_to_w = {}
    w_to_p = {}

    for p, w in zip(pattern, words):
        if p in p_to_w:
            if p_to_w[p] != w:
                return False
        else:
            p_to_w[p] = w

        if w in w_to_p:
            if w_to_p[w] != p:
                return False
        else:
            w_to_p[w] = p

    return True
```

---

## Template: Unique Email Addresses

```python
def num_unique_emails(emails: list[str]) -> int:
    """
    Count unique emails after applying rules:
    - Ignore dots in local name
    - Ignore everything after + in local name

    Time: O(n * m) where m is email length
    Space: O(n)
    """
    unique = set()

    for email in emails:
        local, domain = email.split('@')

        # Remove everything after +
        local = local.split('+')[0]

        # Remove dots
        local = local.replace('.', '')

        unique.add(f"{local}@{domain}")

    return len(unique)
```

---

## Set vs List vs Dict Comparison

| Need              | Use                 | Why                 |
| ----------------- | ------------------- | ------------------- |
| Check existence   | Set                 | O(1) lookup         |
| Count occurrences | Dict/Counter        | Need frequency      |
| Preserve order    | List or dict (3.7+) | Sets are unordered  |
| Remove duplicates | Set                 | Automatic dedup     |
| Find intersection | Set                 | Built-in & operator |

---

## Edge Cases

```python
# Empty input
set() & set()     # set()
set() | set()     # set()

# All same elements
{1, 1, 1, 1}      # {1}

# Single element
{5} & {5}         # {5}
{5} - {5}         # set()

# No common elements
{1, 2} & {3, 4}   # set()

# Subset check
set() <= {1}      # True (empty is subset of everything)
```

---

## Practice Problems

| #   | Problem                       | Difficulty | Pattern               |
| --- | ----------------------------- | ---------- | --------------------- |
| 1   | Intersection of Two Arrays    | Easy       | Set intersection      |
| 2   | Intersection of Two Arrays II | Easy       | Counter               |
| 3   | Contains Duplicate            | Easy       | Set size              |
| 4   | Single Number                 | Easy       | XOR trick             |
| 5   | Happy Number                  | Easy       | Cycle detection       |
| 6   | Longest Consecutive Sequence  | Medium     | Set + sequence start  |
| 7   | Missing Number                | Easy       | Sum or XOR            |
| 8   | Find All Numbers Disappeared  | Easy       | Index marking         |
| 9   | Isomorphic Strings            | Easy       | Bidirectional mapping |
| 10  | Word Pattern                  | Easy       | Pattern matching      |

---

## Key Takeaways

1. **Set for existence checks** - O(1) vs O(n) for list
2. **Set operations are powerful** - union, intersection, difference
3. **XOR for "appears twice except one"** - O(1) space trick
4. **Bidirectional mapping** for isomorphism problems
5. **Use array as set** when range is [1, n] for O(1) space
6. **Check sequence start** for longest consecutive - skip non-starts

---

## Next: [07-design-hashmap.md](./07-design-hashmap.md)

Learn how to implement your own HashMap from scratch.
