# Subarray Sum with HashMap

> **Prerequisites:** [02-arrays-strings/06-prefix-sum.md](../02-arrays-strings/06-prefix-sum.md), [01-hash-table-basics.md](./01-hash-table-basics.md)

## Interview Context

The prefix sum + hashmap combination is a **powerful pattern** for subarray problems. It appears in:

- Subarray sum equals K
- Subarray sum divisible by K
- Count subarrays with given sum
- Maximum size subarray with sum K

The key insight: `sum(i, j) = prefix[j] - prefix[i-1] = k` means `prefix[i-1] = prefix[j] - k`.

**Interview frequency**: High. Subarray Sum Equals K is a FAANG classic.

---

## Building Intuition

**The Key Insight: Prefix Sums Turn Ranges Into Differences**

Without prefix sums:

```text
"What's the sum of elements from index 2 to 5?"
→ Add nums[2] + nums[3] + nums[4] + nums[5] → O(N) each time
```

With prefix sums (O(N) preprocessing):

```text
prefix = [0, a, a+b, a+b+c, ...]
sum(2, 5) = prefix[6] - prefix[2] → O(1)
```

**The Hashmap Insight: Don't Search—Remember**

Naive approach for "find subarray with sum k":

```text
For each end position j:
  For each start position i:
    Check if sum(i, j) == k → O(N²)
```

Hashmap insight:

```text
sum(i, j) = k
→ prefix[j] - prefix[i-1] = k
→ prefix[i-1] = prefix[j] - k

At position j: "Have I seen prefix_sum = (current_prefix - k) before?"
→ O(1) lookup in hashmap!
```

**Mental Model: The Bank Account**

Think of prefix sums as a running bank balance:

```text
Deposits: [+3, +1, -2, +4]
Balance:  [3, 4, 2, 6]

"When was my balance exactly 2 less than now?"
→ If current balance is 6 and I want a period of net +4...
→ I need a previous balance of 6-4=2
→ Check hashmap: balance 2 occurred at index 2
→ Period from index 3 to now has sum 4
```

**Why {0: 1} Is Crucial**

The dummy prefix represents "before the array started":

```text
nums = [3], k = 3

Without {0: 1}:
  prefix = 3, looking for 3-3=0
  0 not in hashmap → WRONG! Miss [3] itself

With {0: 1}:
  prefix = 3, looking for 3-3=0
  0 in hashmap at "index -1" → Found subarray [0, 0] → [3]
```

It lets you find subarrays that START at index 0.

**Why Mod Works for Divisibility**

If two prefix sums have the same remainder when divided by k:

```text
prefix[i] = a × k + r
prefix[j] = b × k + r

prefix[j] - prefix[i] = (b - a) × k → divisible by k!
```

So: group by remainder, pairs within same group form valid subarrays.

**Note on Negative Modulo:**
In Python, the modulo operator (`%`) with a negative dividend and positive divisor always returns a positive result (e.g., `-5 % 3 == 1`). In C++ or Java, `-5 % 3` returns `-2`. When porting code or explaining logic, it's important to mention that Python automatically normalizes negative remainders, making divisibility logic simpler. In C++/Java, you must explicitly normalize: `mod = ((prefix_sum % k) + k) % k`.

**Extending to 2D (Prefix Sum Matrix)**
The 1D prefix sum pattern can be extended to 2D matrices.
Instead of `prefix[i]`, we compute `prefix[r][c]` which stores the sum of the submatrix from `(0,0)` to `(r,c)`.
The sum of any submatrix defined by top-left `(r1, c1)` and bottom-right `(r2, c2)` is:
`sum = prefix[r2][c2] - prefix[r1-1][c2] - prefix[r2][c1-1] + prefix[r1-1][c1-1]`
You can then use hashmaps on these 1D row/col projections or prefix values to solve 2D subarray sum problems (like "Number of Submatrices That Sum to Target" which fixes two rows and applies the 1D hashmap technique to the columns).

---

## When NOT to Use Prefix Sum + Hashmap

**1. All Numbers Are Positive → Use Sliding Window**

For positive-only arrays with sum >= k:

```python
# Sliding window: O(1) space
# Prefix + hashmap: O(N) space
```

Sliding window works because sum only increases when expanding, only decreases when shrinking. Monotonic property → no need to store history.

**2. You Need the Actual Subarray, Not Just Count**

Hashmap stores counts, not positions:

```python
# "Find all subarrays with sum k" → Need to store indices, not just counts
# This changes the data structure significantly
```

For returning actual subarrays, track list of indices per prefix sum.

**3. 2D or Multi-dimensional Arrays**

Prefix sum + hashmap is 1D. For 2D:

- Fix two rows, reduce to 1D problem (Time: $O(R^2 \cdot C)$)
- Or use 2D prefix sum matrix

**4. "At Least K" or "At Most K" Instead of "Exactly K"**

Exact match uses hashmap; range conditions use:

- Sliding window (for positive numbers)
- Two-pointer approaches
- Binary search on sorted prefix array

**5. Streaming Data with Bounded Memory**

Hashmap grows with unique prefix sums. For streams:

- Sliding window if applicable
- Approximate algorithms otherwise

**Red Flags:**

- "All positive integers" + "sum >= k" → Sliding window
- "Return all subarrays" → Store indices, not counts
- "Sum in range [a, b]" → Different approach needed
- "2D matrix" → Reduce dimension first

---

## Core Concept

For any subarray `[i, j]`:

- Sum = `prefix[j] - prefix[i-1]`
- If we want sum = k, then `prefix[j] - k = prefix[i-1]`

So at each position j, we ask: "How many previous prefix sums equal `prefix[j] - k`?"

```text
nums = [1, 2, 3], k = 3

Prefix sums: [0, 1, 3, 6]
             ↑  ↑  ↑  ↑
           0  1  2  3 (indices including dummy 0)

At index 2 (prefix=3): prefix - k = 0, count of 0 = 1 → found [1,2]
At index 3 (prefix=6): prefix - k = 3, count of 3 = 1 → found [3]
Total: 2 subarrays
```

---

## Template: Subarray Sum Equals K

**Problem**: Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals to `k`.

**Explanation**: We use the prefix sum pattern. A subarray `nums[i...j]` has sum `k` if `prefix_sum[j] - prefix_sum[i-1] = k`, which is equivalent to `prefix_sum[i-1] = prefix_sum[j] - k`. As we iterate and compute the running `prefix_sum`, we use a hashmap to track how many times each prefix sum has occurred. This allows us to count how many previous indices `i-1` satisfy the condition in O(1) average time.

```python
def subarray_sum(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum equal to k.

    Time Complexity: O(N) where N is the length of nums. We iterate through the array once.
                     Hashmap operations (lookup and insert) take O(1) on average.
                     In the worst case (many hash collisions), it could degrade to O(N²),
                     but standard interview analysis considers it O(N).
    Space Complexity: O(N) to store the hashmap, as there can be at most N unique prefix sums.

    Example:
    nums = [1, 1, 1], k = 2 → 2
    nums = [1, 2, 3], k = 3 → 2 ([1,2] and [3])
    """
    count = 0
    prefix_sum = 0
    prefix_count = {0: 1}  # prefix_sum → how many times seen

    for num in nums:
        prefix_sum += num

        # If (prefix_sum - k) exists, found subarrays ending here
        if prefix_sum - k in prefix_count:
            count += prefix_count[prefix_sum - k]

        # Record current prefix sum
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return count
```

### Visual Trace

```text
nums = [1, 2, 3], k = 3

i=0: prefix=1, check 1-3=-2 (not found), prefix_count={0:1, 1:1}
i=1: prefix=3, check 3-3=0 (found, count+=1), prefix_count={0:1, 1:1, 3:1}
i=2: prefix=6, check 6-3=3 (found, count+=1), prefix_count={0:1, 1:1, 3:1, 6:1}

Total: 2 subarrays ([1,2] and [3])
```

### Why We Need {0: 1}

```text
Without {0: 1}:
nums = [3], k = 3

prefix=3, check 3-3=0 → NOT FOUND! (wrong)

With {0: 1}:
prefix=3, check 3-3=0 → FOUND in {0: 1} (correct)

The dummy 0 represents "empty prefix" for subarrays starting at index 0.
```

---

## Template: Subarray Sum Divisible by K

**Problem**: Given an integer array `nums` and an integer `k`, return the number of non-empty subarrays that have a sum divisible by `k`.

**Explanation**: A subarray sum `prefix_sum[j] - prefix_sum[i-1]` is divisible by `k` if `prefix_sum[j] % k == prefix_sum[i-1] % k`. We store the frequencies of the remainders (modulos) of prefix sums in a hashmap. When we encounter a remainder we've seen before, it means the subarray between the previous occurrence and the current one is divisible by `k`.

```python
def subarrays_div_by_k(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum divisible by k.

    Key insight: If prefix[j] % k == prefix[i] % k,
    then (prefix[j] - prefix[i]) % k == 0.

    Time Complexity: O(N) where N is the length of nums.
    Space Complexity: O(K) because the remainder will always be in the range [0, k-1],
                      so the hashmap will store at most K key-value pairs.

    Example:
    nums = [4, 5, 0, -2, -3, 1], k = 5 → 7
    """
    count = 0
    prefix_sum = 0
    mod_count = {0: 1}  # remainder → count

    for num in nums:
        prefix_sum += num
        mod = prefix_sum % k

        # Note: Python's modulo naturally handles negative numbers
        # e.g., -2 % 5 returns 3.
        # In C++/Java, you would need: mod = (mod + k) % k

        if mod in mod_count:
            count += mod_count[mod]

        mod_count[mod] = mod_count.get(mod, 0) + 1

    return count
```

### Visual Trace

```text
nums = [4, 5, 0, -2, -3, 1], k = 5

i=0: prefix=4, mod=4, count+=0, mod_count={0:1, 4:1}
i=1: prefix=9, mod=4, count+=1, mod_count={0:1, 4:2}
i=2: prefix=9, mod=4, count+=2, mod_count={0:1, 4:3}
i=3: prefix=7, mod=2, count+=0, mod_count={0:1, 4:3, 2:1}
i=4: prefix=4, mod=4, count+=3, mod_count={0:1, 4:4, 2:1}
i=5: prefix=5, mod=0, count+=1, mod_count={0:2, 4:4, 2:1}

Total: 7
```

---

## Template: Maximum Size Subarray Sum Equals K

**Problem**: Given an array `nums` and a target value `k`, find the maximum length of a subarray that sums to `k`. If there isn't one, return 0 instead.

**Explanation**: Similar to "Subarray Sum Equals K", but instead of counting occurrences, we store the *earliest* index where each prefix sum was first seen. This allows us to calculate the maximum distance between two prefix sums that differ by `k`.

```python
def max_subarray_len(nums: list[int], k: int) -> int:
    """
    Find length of longest subarray with sum k.

    Time Complexity: O(N) where N is the length of nums.
    Space Complexity: O(N) to store the earliest index of each prefix sum.

    Example:
    nums = [1, -1, 5, -2, 3], k = 3 → 4 ([1, -1, 5, -2])
    """
    prefix_sum = 0
    first_occurrence = {0: -1}  # prefix_sum → first index
    max_len = 0

    for i, num in enumerate(nums):
        prefix_sum += num

        if prefix_sum - k in first_occurrence:
            max_len = max(max_len, i - first_occurrence[prefix_sum - k])

        # Only store FIRST occurrence to maximize (i - earliest_index)
        if prefix_sum not in first_occurrence:
            first_occurrence[prefix_sum] = i

    return max_len
```

### Why First Occurrence Only?

```text
For MAXIMUM length, we want the EARLIEST index with the required prefix sum.

nums = [1, 0, 0, -1, 2], k = 2
prefixes = [1, 1, 1, 0, 2]

At index 4 (prefix=2), we look for prefix=0:
- First occurrence of 0 is at index -1 (dummy)
- Length = 4 - (-1) = 5 (entire array)

If we stored last occurrence, we'd get:
- Last occurrence of 0 is at index 3
- Length = 4 - 3 = 1 (just [2])

First occurrence → maximum length
```

---

## Template: Minimum Size Subarray Sum (Positive Numbers)

**Problem**: Given an array of positive integers `nums` and a positive integer `target`, return the minimal length of a contiguous subarray of which the sum is greater than or equal to `target`. If there is no such subarray, return 0 instead.

**Explanation**: For arrays with only positive numbers, we don't need a hashmap. We can use a sliding window (two pointers) to find the minimum length. We expand the window until the sum is `≥ target`, then contract it from the left to find the smallest possible valid window. This is O(N) time and O(1) space.

```python
def min_subarray_len(target: int, nums: list[int]) -> int:
    """
    Find minimum length subarray with sum >= target.
    All numbers are positive.

    Time Complexity: O(N). Each element is processed at most twice (once added to the window,
                     once removed).
    Space Complexity: O(1). We only use a few integer variables to keep track of the window.

    Note: For positive numbers, sliding window is better than prefix sum + hashmap!
    """
    left = 0
    current_sum = 0
    min_len = float('inf')

    for right, num in enumerate(nums):
        current_sum += num

        while current_sum >= target:
            min_len = min(min_len, right - left + 1)
            current_sum -= nums[left]
            left += 1

    return min_len if min_len != float('inf') else 0
```

**Key Insight**: For positive-only arrays, sliding window is $O(1)$ space. Prefix sum + hashmap is needed when negatives are present because the prefix sum array is no longer monotonic (sorted).

---

## Template: Contiguous Array (Equal 0s and 1s)

**Problem**: Given a binary array `nums`, return the maximum length of a contiguous subarray with an equal number of 0 and 1.

**Explanation**: We transform the problem by treating `0` as `-1`. Now, the problem is to find the longest subarray with a sum of `0`. We use a hashmap to store the first occurrence of each prefix sum and calculate the maximum distance whenever a prefix sum repeats.

```python
def find_max_length(nums: list[int]) -> int:
    """
    Find longest subarray with equal number of 0s and 1s.

    Trick: Replace 0 with -1, then find longest subarray with sum 0.

    Time Complexity: O(N) where N is the length of nums.
    Space Complexity: O(N) to store the first occurrences of prefix sums.

    Example:
    [0, 1] → 2
    [0, 1, 0] → 2
    """
    prefix_sum = 0
    first_occurrence = {0: -1}
    max_len = 0

    for i, num in enumerate(nums):
        # Convert: 0 → -1, 1 → 1
        prefix_sum += 1 if num == 1 else -1

        if prefix_sum in first_occurrence:
            max_len = max(max_len, i - first_occurrence[prefix_sum])
        else:
            first_occurrence[prefix_sum] = i

    return max_len
```

### Visual Trace

```text
nums = [0, 1, 0, 1, 1, 0]
converted = [-1, 1, -1, 1, 1, -1]

i=0: prefix=-1, first_occurrence={0:-1, -1:0}
i=1: prefix=0, found at -1, len=1-(-1)=2, first_occurrence unchanged
i=2: prefix=-1, found at 0, len=2-0=2
i=3: prefix=0, found at -1, len=3-(-1)=4
i=4: prefix=1, first_occurrence={0:-1, -1:0, 1:4}
i=5: prefix=0, found at -1, len=5-(-1)=6

Max length: 6
```

---

## Template: Continuous Subarray Sum (Multiple of K)

**Problem**: Given an integer array `nums` and an integer `k`, return `true` if `nums` has a contiguous subarray of size at least two whose elements sum up to a multiple of `k`.

**Explanation**: We use the prefix sum modulo `k`. If we see the same remainder twice, the elements between those two points sum to a multiple of `k`. We use a hashmap to store the first occurrence of each remainder and ensure the distance between indices is at least 2.

```python
def check_subarray_sum(nums: list[int], k: int) -> bool:
    """
    Check if there exists a subarray of size >= 2 whose sum is a multiple of k.

    Time Complexity: O(N) where N is the length of nums.
    Space Complexity: O(min(N, K)) since the hashmap only stores up to K remainders,
                      and there are at most N elements.

    Example:
    nums = [23, 2, 4, 6, 7], k = 6 → True ([2, 4] sums to 6)
    """
    prefix_sum = 0
    first_occurrence = {0: -1}  # mod → first index

    for i, num in enumerate(nums):
        prefix_sum += num
        mod = prefix_sum % k

        if mod in first_occurrence:
            if i - first_occurrence[mod] >= 2:  # Size >= 2
                return True
        else:
            first_occurrence[mod] = i

    return False
```

---

## Template: Binary Subarrays With Sum

**Problem**: Given a binary array `nums` and an integer `goal`, return the number of non-empty subarrays with a sum equal to `goal`.

**Explanation**: Since the values are only 0 and 1, the prefix sum is non-decreasing. We can use the standard "Subarray Sum Equals K" hashmap approach to count subarrays that sum to the `goal`.

```python
def num_subarrays_with_sum(nums: list[int], goal: int) -> int:
    """
    Count subarrays with sum equal to goal (binary array).

    Time Complexity: O(N) where N is the length of nums.
    Space Complexity: O(N) to store prefix sum counts.

    Example:
    nums = [1, 0, 1, 0, 1], goal = 2 → 4
    """
    count = 0
    prefix_sum = 0
    prefix_count = {0: 1}

    for num in nums:
        prefix_sum += num

        if prefix_sum - goal in prefix_count:
            count += prefix_count[prefix_sum - goal]

        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return count
```

---

## Template: Count Nice Subarrays (Odd Numbers)

**Problem**: Given an array of integers `nums` and an integer `k`. A contiguous subarray is called nice if there are `k` odd numbers in it. Return the number of nice subarrays.

**Explanation**: We transform the problem by treating odd numbers as `1` and even numbers as `0`. Now we just need to find the number of subarrays with sum equal to `k`, which we solve using the prefix sum and hashmap count pattern.

```python
def number_of_subarrays(nums: list[int], k: int) -> int:
    """
    Count subarrays with exactly k odd numbers.

    Trick: Convert to binary (odd=1, even=0), then count subarrays with sum k.

    Time Complexity: O(N) where N is the length of nums.
    Space Complexity: O(N) to store prefix sum counts.
    """
    count = 0
    prefix_sum = 0  # Count of odd numbers so far
    prefix_count = {0: 1}

    for num in nums:
        prefix_sum += num % 2  # 1 if odd, 0 if even

        if prefix_sum - k in prefix_count:
            count += prefix_count[prefix_sum - k]

        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return count
```

---

## Template: Subarray with 0 Sum

**Problem**: Given an array of integers, check if there is a subarray with sum equal to 0.

**Explanation**: A subarray sums to 0 if any prefix sum repeats. We use a set to store prefix sums as we calculate them. If the current `prefix_sum` is already in the set, we've found a subarray with sum 0.

```python
def has_zero_sum_subarray(nums: list[int]) -> bool:
    """
    Check if any subarray has sum 0.

    Time Complexity: O(N) where N is the length of nums.
    Space Complexity: O(N) in the worst case if all prefix sums are unique.
    """
    prefix_sum = 0
    seen = {0}  # Include 0 for subarray starting at index 0

    for num in nums:
        prefix_sum += num

        if prefix_sum in seen:
            return True

        seen.add(prefix_sum)

    return False
```

---

## When to Use What

| Problem Type               | Technique             | Space |
| -------------------------- | --------------------- | ----- |
| Sum = K (with negatives)   | Prefix sum + HashMap  | $O(N)$  |
| Sum >= K (positive only)   | Sliding window        | $O(1)$  |
| Sum divisible by K         | Prefix mod + HashMap  | $O(K)$  |
| Max length with sum K      | First occurrence only | $O(N)$  |
| Count subarrays with sum K | Count all occurrences | $O(N)$  |

---

## Edge Cases

```python
# Empty array
[] → 0 subarrays

# Single element equals k
[k], k → 1 subarray

# All zeros, k=0
[0, 0, 0] → 6 subarrays (each single 0, pairs, and full)

# Negative numbers
[-1, 1, 0], k=0 → multiple subarrays

# k=0 special case
Need to count subarrays that sum to 0, {0: 1} handles starting cases

# Large k with small elements
May have no valid subarrays

# Overflow consideration
Use Python (no overflow) or be careful in other languages
```

---

## Common Mistakes

1. **Forgetting `{0: 1}`**: Misses subarrays starting at index 0.
2. **Wrong first/last occurrence**: Use first occurrence for max length, use count for total number of subarrays.
3. **Positive-only optimization**: Don't use a hashmap when a sliding window works (and requires $O(1)$ space).
4. **Mod with negatives**: Ensure positive remainder in languages like C++/Java (`mod = (mod + k) % k`). Python automatically handles it.
5. **Size >= 2 constraint**: Check length (`i - earliest_index >= 2`), not just existence.
6. **Shadowing Built-ins**: Avoid using `sum` or `max` as variable names. Use `current_sum` or `max_len` instead.

---

## Practice Problems

| #   | Problem                            | Difficulty | Variant                   |
| --- | ---------------------------------- | ---------- | ------------------------- |
| 1   | Subarray Sum Equals K              | Medium     | Count with hashmap        |
| 2   | Subarray Sums Divisible by K       | Medium     | Mod prefix sum            |
| 3   | Maximum Size Subarray Sum Equals K | Medium     | First occurrence          |
| 4   | Contiguous Array                   | Medium     | 0→-1 transform            |
| 5   | Continuous Subarray Sum            | Medium     | Size >= 2 constraint      |
| 6   | Binary Subarrays With Sum          | Medium     | Binary array              |
| 7   | Count Nice Subarrays               | Medium     | Odd count transform       |
| 8   | Minimum Size Subarray Sum          | Medium     | Sliding window (positive) |

---

## Key Takeaways

1. **Prefix sum + HashMap = $O(N)$** for subarray sum problems (when array contains negatives).
2. **`{0: 1}` is crucial** - represents empty prefix for index-0 subarrays.
3. **First occurrence for max length**, count all for number of subarrays.
4. **Mod arithmetic for divisibility** - group by remainders.
5. **Transform problems**: 0→-1 for equal count, odd→1 for odd count.
6. **Sliding window for positive-only** - simpler and $O(1)$ space.

---

## Next: [06-set-operations.md](./06-set-operations.md)

Learn set operations for intersection, union, and uniqueness problems.
