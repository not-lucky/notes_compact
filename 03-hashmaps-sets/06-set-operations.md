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
"Find the red paper" → Flip through entire stack → O(N)

Filing Cabinet (Set):
"Find the red paper" → Open 'R' drawer → Amortized O(1)
```

**Floyd's Cycle Detection vs Set-based Cycle Detection**
For problems like "Happy Number" or linked list cycles:
- **Set-based**: Easier to implement and reason about. Stores visited states. Takes $O(N)$ space.
- **Floyd's (Tortoise & Hare)**: Slightly more complex logic, but takes $O(1)$ auxiliary space.
Use sets in an interview first for speed/correctness, then optimize to Floyd's if asked to improve space complexity.

**The XOR Trick Explained**

XOR has magical properties for "find the unique element":

```
a ^ a = 0      (anything XORed with itself is 0)
a ^ 0 = a      (anything XORed with 0 is itself)
XOR is commutative and associative

So: a ^ b ^ a = (a ^ a) ^ b = 0 ^ b = b

All duplicates cancel out, leaving only the unique element!
```

No extra space needed ($O(1)$ auxiliary space).

**Why "Check Sequence Start" for Longest Consecutive**

Naive approach:

```python
for num in nums:
    count = 1
    while num + 1 in num_set: ...  # Could recount same sequence many times!
```

Problem: If sequence is [1,2,3,4,5], we count:

- Starting at 1: length 5
- Starting at 2: length 4 (wasteful!)
- Starting at 3: length 3 (wasteful!)

Optimization: Only start counting from sequence START:

```python
if num - 1 not in num_set:  # This is the start!
    count from here
```

Now we count each element exactly once within the while loop → $O(N)$ overall time.

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
s: set[int] = {3, 1, 2}
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
# Set: O(N) to find element closest to x
# Sorted structure (BST, sorted list): O(log N)
```

Use `sortedcontainers.SortedSet` for ordered set operations.

**Red Flags:**

- "Maintain insertion order" → dict or list
- "Count occurrences in intersection" → Counter
- "Find closest element" → Sorted structure
- "Keys are lists or dicts" → Convert to tuples

---

## Core Concept

A set is an unordered collection of **unique elements** with amortized $O(1)$ operations.

```python
s: set[int] = {1, 2, 3}

# Amortized O(1) operations
1 in s           # True
s.add(4)         # {1, 2, 3, 4}
s.remove(1)      # {2, 3, 4}
s.discard(99)    # No error if missing
```

---

## Python Set Operations

```python
a: set[int] = {1, 2, 3, 4}
b: set[int] = {3, 4, 5, 6}

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
| Add            | `s.add(x)`     | $O(1)$ amortized       |
| Remove         | `s.remove(x)`  | $O(1)$ average         |
| Discard        | `s.discard(x)` | $O(1)$ average         |
| Membership     | `x in s`       | $O(1)$ average         |
| Union          | `a \| b`       | $O(N + M)$             |
| Intersection   | `a & b`        | $O(\min(N, M))$        |
| Difference     | `a - b`        | $O(N)$                 |
| Symmetric Diff | `a ^ b`        | $O(N + M)$             |

*Note on Insertion & Lookup*: Sets use hash tables under the hood. Insertion is amortized $O(1)$ and lookup is average $O(1)$, but both can degrade to $O(N)$ in the worst case due to hash collisions.
*Note on Intersection Efficiency*: In Python, `set_a & set_b` is optimized to iterate over the smaller set and check membership in the larger set. If sizes are drastically different ($M \ll N$), the intersection takes $O(M)$ time.

---

## Template: Intersection of Two Arrays

**Problem**: Given two integer arrays `nums1` and `nums2`, return an array of their intersection. Each element in the result must be unique.

**Explanation**: We convert both arrays to sets and use the set intersection operator `&`. This returns only the unique elements present in both sets in O(n + m) time.

```python
def intersection(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Find elements that appear in both arrays (unique).

    Time: O(N + M)
    Space: O(N + M) for the sets, output takes O(min(N, M))

    Example:
    [1, 2, 2, 1], [2, 2] → [2]
    """
    return list(set(nums1) & set(nums2))
```

---

## Template: Intersection of Two Arrays II (With Frequency)

**Problem**: Given two integer arrays `nums1` and `nums2`, return an array of their intersection. Each element in the result must appear as many times as it shows in both arrays.

**Explanation**: We use a frequency map (Counter) for one array and then iterate through the second array. If a number exists in the frequency map with a count > 0, we add it to our result and decrement the count in the map.

```python
def intersect(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Find intersection including duplicates (by frequency).

    Time: O(N + M)
    Space: O(min(N, M)) for Counter

    Example:
    [1, 2, 2, 1], [2, 2] → [2, 2]
    """
    from collections import Counter

    # Use smaller array for counter to optimize space
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    count: dict[int, int] = Counter(nums1)
    result: list[int] = []

    for num in nums2:
        if count.get(num, 0) > 0:
            result.append(num)
            count[num] -= 1

    return result
```

### Follow-up: Sorted Arrays

**Problem**: Find the intersection of two arrays that are already sorted.

**Explanation**: Since the arrays are sorted, we can use two pointers to find the intersection in O(n + m) time and O(1) space (excluding the result array). We move the pointers based on which element is smaller, or add to result and move both if they are equal.

```python
def intersect_sorted(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    If arrays are sorted, use two pointers for O(1) auxiliary space.

    Time: O(N + M) where N, M are lengths of the arrays
    Space: O(1) auxiliary, O(min(N, M)) for output
    """
    result: list[int] = []
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

**Problem**: Find all unique elements present in either of two arrays.

**Explanation**: We convert both arrays to sets and use the set union operator `|`. This combines all unique elements from both arrays into a single set.

```python
def union(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Find all unique elements from both arrays.

    Time: O(N + M)
    Space: O(N + M) for sets
    """
    return list(set(nums1) | set(nums2))
```

---

## Template: Set Difference

**Problem**: Find elements that are in the first array but not in the second.

**Explanation**: Convert both to sets and use the set difference operator `-`. This returns elements present in the first set but absent from the second.

```python
def difference(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Find elements in nums1 but not in nums2.

    Time: O(N + M)
    Space: O(N + M) for sets
    """
    return list(set(nums1) - set(nums2))
```

---

## Template: Find the Difference (XOR Trick)

**Problem**: String `t` is generated by random shuffling string `s` and then adding one more letter at a random position. Return the letter that was added.

**Explanation**: By XORing the character codes of all characters in both strings, identical characters cancel each other out (since `a ^ a = 0`), leaving only the extra character. This is more space-efficient than using a frequency map.

```python
def find_the_difference(s: str, t: str) -> str:
    """
    t is s with one extra character. Find it.

    Time: O(N) where N is len(s)
    Space: O(1) auxiliary
    """
    result = 0

    for char in s + t:
        result ^= ord(char)

    return chr(result)
```

---

## Template: Contains Duplicate

**Problem**: Check if an array contains any duplicate elements.

**Explanation**: We compare the length of the original array with the length of its set version. If they differ, it means duplicates were removed when creating the set.

```python
def contains_duplicate(nums: list[int]) -> bool:
    """
    Check if any element appears more than once.

    Time: O(N)
    Space: O(N) worst case
    """
    return len(nums) != len(set(nums))


def contains_duplicate_early_exit(nums: list[int]) -> bool:
    """
    Early exit version - better for large arrays with early duplicates.

    Time: O(N) worst case, but average time is faster if duplicate exists early
    Space: O(N) worst case
    """
    seen: set[int] = set()

    for num in nums:
        if num in seen:
            return True
        seen.add(num)

    return False
```

---

## Template: Single Number

**Problem**: Every element appears twice except for one. Find that single one.

**Explanation**: The XOR approach (`a ^ a = 0`) is the most efficient O(1) space solution. Alternatively, using set theory: `2 * sum(set(nums)) - sum(nums)` will equal the unique element because every other element was counted twice in the first term but twice in the second, while the unique element was counted twice in the first and only once in the second.

```python
def single_number(nums: list[int]) -> int:
    """
    Every element appears twice except one. Find it.

    Time: O(N)
    Space: O(1) auxiliary with XOR trick
    """
    result = 0
    for num in nums:
        result ^= num
    return result


def single_number_set(nums: list[int]) -> int:
    """
    Alternative: 2 * sum(set) - sum(nums) = single element.

    Time: O(N)
    Space: O(N) for set

    Works because: 2(a + b + c) - (a + a + b + b + c) = c
    """
    # Note: Using int instead of list[int] for return type
    return 2 * sum(set(nums)) - sum(nums)
```

---

## Template: Single Number III (Two Unique Numbers)

**Problem**: Given an integer array `nums`, in which exactly two elements appear only once and all the other elements appear exactly twice. Find the two elements that appear only once.

**Explanation**: First, we XOR all numbers to get `a ^ b` (the two unique numbers). We then find any bit that is set in `a ^ b` (e.g., the rightmost set bit), which must be different between `a` and `b`. We use this bit to partition all numbers in the array into two groups and XOR them separately. Each group will contain one of the unique numbers and some pairs of duplicates, effectively isolating `a` and `b`.

```python
def single_number_iii(nums: list[int]) -> list[int]:
    """
    All elements appear twice except two. Find them.

    Time: O(N)
    Space: O(1) auxiliary

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

**Problem**: Write an algorithm to determine if a number `n` is happy. A happy number is defined by replacing the number by the sum of the squares of its digits, and repeating the process until the number equals 1. If it loops endlessly in a cycle which does not include 1, the number is not happy.

**Explanation**: We use a set to keep track of the numbers we've seen in our sequence. If we encounter a number that's already in the set, we've found a cycle and the number is not happy. Alternatively, Floyd's Cycle-Finding Algorithm (Slow and Fast pointers) can be used for O(1) space.

```python
def is_happy(n: int) -> bool:
    """
    A happy number eventually reaches 1 after repeated digit square sum.

    Time: O(log n) per step, overall time is bound by properties of digit sum (usually constant bounded loops)
    Space: O(log n) for set storing history

    Example:
    19 → 82 → 68 → 100 → 1 (happy!)
    2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 (cycle, not happy)
    """
    def digit_square_sum(num: int) -> int:
        total = 0
        while num:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total

    seen: set[int] = set()

    while n != 1 and n not in seen:
        seen.add(n)
        n = digit_square_sum(n)

    return n == 1


def is_happy_floyd(n: int) -> bool:
    """
    O(1) auxiliary space using Floyd's cycle detection.
    """
    def digit_square_sum(num: int) -> int:
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

**Problem**: Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. The algorithm must run in O(n) time.

**Explanation**: We put all numbers into a set. Then we iterate through the set, and for each number `num`, we check if `num - 1` is also in the set. If it's not, then `num` is the start of a potential sequence. We then count how many consecutive numbers follow it (`num + 1`, `num + 2`, etc.) by checking their existence in the set. This ensures each number is processed at most twice, resulting in O(n) time.

```python
def longest_consecutive(nums: list[int]) -> int:
    """
    Find length of longest consecutive elements sequence.

    Time: O(N) because each number is checked at most twice (once for existence, once in inner loop)
    Space: O(N) for set storage

    Example:
    [100, 4, 200, 1, 3, 2] → 4 (sequence: 1, 2, 3, 4)
    """
    if not nums:
        return 0

    num_set: set[int] = set(nums)
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

**Problem**: Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.

**Explanation**: We can use the mathematical sum formula `n*(n+1)/2` and subtract the actual sum of the array to find the missing number. Alternatively, XORing all numbers from `0` to `n` and all numbers in the array will cancel out all existing numbers, leaving only the missing one.

```python
def missing_number(nums: list[int]) -> int:
    """
    Find missing number in [0, n].

    Time: O(N)
    Space: O(1) auxiliary
    """
    n = len(nums)
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum


def missing_number_xor(nums: list[int]) -> int:
    """
    XOR approach: a ^ a = 0, so missing number remains.

    Time: O(N)
    Space: O(1) auxiliary
    """
    result = len(nums)  # Include n

    for i, num in enumerate(nums):
        result ^= i ^ num

    return result


def missing_number_set(nums: list[int]) -> int:
    """
    Set approach (less efficient but clearer).
    Note: Space complexity is O(N), unlike math/XOR which are O(1) auxiliary.
    """
    full_set: set[int] = set(range(len(nums) + 1))
    return (full_set - set(nums)).pop()
```

---

## Template: Find All Numbers Disappeared

**Problem**: Given an array `nums` of `n` integers where `nums[i]` is in the range `[1, n]`, return an array of all the integers in the range `[1, n]` that do not appear in `nums`.

**Explanation**: Since the range is `[1, n]`, we can use index marking. For each number `x` in the array, we mark the element at index `abs(x)-1` as negative. After one pass, any index that still contains a positive number corresponds to a missing value.

```python
def find_disappeared_numbers(nums: list[int]) -> list[int]:
    """
    Find all numbers in [1, n] not appearing in nums.

    Time: O(N)
    Space: O(1) auxiliary - mutates input array to serve as marker set!
    """
    # Mark seen numbers by negating value at corresponding index
    for num in nums:
        index = abs(num) - 1
        nums[index] = -abs(nums[index])

    # Positive values mean their indices were never seen
    result: list[int] = []
    for i in range(len(nums)):
        if nums[i] > 0:
            result.append(i + 1)

    return result
```

---

## Template: Isomorphic Strings

**Problem**: Given two strings `s` and `t`, determine if they are isomorphic. Two strings are isomorphic if the characters in `s` can be replaced to get `t`.

**Explanation**: We must maintain a consistent one-to-one mapping between characters of `s` and `t`. This requires two hashmaps: one to store `s -> t` mappings and another for `t -> s` to ensure no two characters in `s` map to the same character in `t`, and vice versa.

```python
def is_isomorphic(s: str, t: str) -> bool:
    """
    Check if characters in s can be replaced to get t.

    Time: O(N) where N is len(s)
    Space: O(K) where K is size of character set (O(1) if bounded e.g., ASCII)

    Example:
    "egg", "add" → True (e→a, g→d)
    "foo", "bar" → False (o maps to both a and r)
    """
    if len(s) != len(t):
        return False

    s_to_t: dict[str, str] = {}
    t_to_s: dict[str, str] = {}

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

**Problem**: Given a `pattern` and a string `s`, find if `s` follows the same pattern.

**Explanation**: Similar to isomorphic strings, we need to map characters in the pattern to words in `s` and words in `s` back to characters in the pattern. If all mappings are consistent and one-to-one, the pattern is followed.

```python
def word_pattern(pattern: str, s: str) -> bool:
    """
    Check if words follow the same pattern.

    Time: O(N) where N is len(s) or len(pattern)
    Space: O(N) for split words array and hashmaps

    Example:
    pattern = "abba", s = "dog cat cat dog" → True
    """
    words = s.split()

    if len(pattern) != len(words):
        return False

    p_to_w: dict[str, str] = {}
    w_to_p: dict[str, str] = {}

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

**Problem**: Given an array of strings `emails`, count how many unique email addresses are present after applying local name rules (dots are ignored, everything after '+' is ignored).

**Explanation**: For each email, we parse the local name and domain. We apply the cleaning rules to the local name and then join it back with the domain. We store these normalized emails in a set to count the unique entries.

```python
def num_unique_emails(emails: list[str]) -> int:
    """
    Count unique emails after applying rules:
    - Ignore dots in local name
    - Ignore everything after + in local name

    Time: O(N * M) where N is number of emails, M is average length
    Space: O(N * M) for the set storing processed emails
    """
    unique: set[str] = set()

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
| Check existence   | Set                 | Amortized $O(1)$ lookup |
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

1. **Set for existence checks** - Amortized $O(1)$ vs $O(N)$ for list
2. **Set operations are powerful** - union, intersection, difference
3. **XOR for "appears twice except one"** - $O(1)$ auxiliary space trick
4. **Bidirectional mapping** for isomorphism problems
5. **Use array as set** when range is [1, n] for $O(1)$ auxiliary space
6. **Check sequence start** for longest consecutive - skip non-starts

---

## Next: [07-design-hashmap.md](./07-design-hashmap.md)

Learn how to implement your own HashMap from scratch.
