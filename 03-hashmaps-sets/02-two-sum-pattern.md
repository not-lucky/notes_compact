# Two Sum Pattern

> **Prerequisites:** [01-hash-table-basics.md](./01-hash-table-basics.md)

## Interview Context

The Two Sum pattern is **the most important hashmap pattern** to master. It appears in:

- Direct "Two Sum" style questions
- As a building block for 3Sum, 4Sum, K-Sum
- In combination with other techniques (sliding window, binary search)

The core insight: instead of checking all pairs $O(n^2)$, use a hashmap to check if the complement exists in $O(1)$.

**Interview frequency**: Very high. This is often the first coding question in a phone screen.

---

## Building Intuition

**The Key Insight: Don't Search—Remember**

Brute force Two Sum asks: "For each number, does any OTHER number complete the sum?"
This requires checking all pairs → $O(n^2)$.

The hashmap insight flips this: "Have I ALREADY seen the number I need?"

```
Looking for pairs that sum to 9:

Brute Force Thinking:
  At num=2: "Is there a 7 somewhere?" → scan entire array

Hashmap Thinking:
  At num=2: "Have I seen 7 before?" → check hashmap $O(1)$
  Store 2 for future use.
  At num=7: "Have I seen 2 before?" → YES! Found it.
```

**Mental Model: The Party Introduction**

Imagine you're at a party looking for someone whose age + yours = 50:

```
Brute Force:
- For each person you meet, ask everyone else their age
- $O(n^2)$ conversations

Hashmap Approach:
- Memorize each person's age as you meet them
- When you meet someone new, check your memory:
  "Do I know someone who's (50 - their age)?"
- $O(n)$ conversations total
```

**Why One Pass Is Enough**

A common question: "What if the complement comes AFTER the current number?"

Answer: It doesn't matter! If nums[i] + nums[j] = target, we'll find the pair when we reach the LATER index (whichever is processed second):

```
nums = [7, 2], target = 9

i=0: num=7, need 2, haven't seen it → store {7: 0}
i=1: num=2, need 7, already stored! → return [0, 1]
```

The pair is found when we reach index 1, not index 0.

**The Complement Pattern Is Everywhere**

Once you recognize "find two things that combine to X," you'll see it everywhere:

- Two Sum (add to target)
- Pairs with XOR = k
- Pairs with product = k
- Songs with duration % 60 = 0 (modular arithmetic)

All use the same insight: store what you've seen, check for complement.

---

## When NOT to Use Hashmap Two Sum

**1. Array Is Already Sorted**

Use two pointers instead—$O(1)$ space vs $O(n)$:

```python
# Sorted array: two pointers is better
left, right = 0, len(nums) - 1
while left < right:
    current_sum = nums[left] + nums[right]
    if current_sum == target:
        return True
    elif current_sum < target:
        left += 1
    else:
        right -= 1
```

**2. Need Multiple Solutions But Array Has No Duplicates**

If the problem guarantees unique values and exactly one solution, hashmap is fine. But for counting all pairs or handling duplicates, you need Counter or careful deduplication.

**3. Memory Is Extremely Constrained**

Hashmap uses $O(n)$ extra space. For huge arrays with strict memory limits:

- Sort + two pointers: $O(1)$ space (if in-place sort allowed)
- Trade time for space with $O(n^2)$ brute force

**4. Looking for K-Sum with Large K**

For 3Sum/4Sum, hashmap alone isn't optimal:

- 3Sum: Sort + fix one + two pointers = $O(n^2)$
- 4Sum: Sort + fix two + two pointers = $O(n^3)$
- General K-Sum: Recursive reduction to 2Sum

Hashmap is the inner primitive, not the whole solution.

**Red Flags:**

- "Array is sorted" → Two pointers ($O(1)$ space)
- "Count all pairs" → Need Counter, not basic hashmap
- "Find closest sum to target" → Two pointers + tracking
- "Memory limit: $O(1)$" → Sort + two pointers

---

## Core Concept

**Problem**: Find two numbers in an array that add up to a target.

**Brute Force**: Check all pairs - $O(n^2)$

**HashMap Approach**: For each number, check if `target - num` was seen before - $O(n)$

```
nums = [2, 7, 11, 15], target = 9

Iteration 1: num = 2
  complement = 9 - 2 = 7
  Is 7 in hashmap? No
  Add 2 → index 0 to hashmap

Iteration 2: num = 7
  complement = 9 - 7 = 2
  Is 2 in hashmap? Yes! At index 0
  Return [0, 1]
```

---

## Template: Classic Two Sum

**Problem**: Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. Each input has exactly one solution, and you may not use the same element twice.

**Explanation**: We use a hashmap to store the values we've seen so far as keys and their indices as values. For each number, we calculate its `complement` (target - num). If the complement is in the map, we've found our pair and return their indices. Otherwise, we store the current number in the map and continue. This works because it reduces the search for a complement from $O(n)$ to $O(1)$.

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find indices of two numbers that add up to target.

    Time: $O(n)$ - single pass average case. $O(n^2)$ worst case if many hash collisions.
    Space: $O(n)$ - hashmap storage

    Example:
    nums = [2, 7, 11, 15], target = 9 → [0, 1]
    """
    seen: dict[int, int] = {}  # value → index

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []  # No solution found
```

### Visual Trace

```
nums = [2, 7, 11, 15], target = 9

i=0, num=2: complement=7, seen={} → not found → seen={2:0}
i=1, num=7: complement=2, seen={2:0} → FOUND! return [0,1]
```

---

## Template: Two Sum - Return Values (Not Indices)

**Problem**: Given an array of integers `nums` and an integer `target`, return the two numbers that add up to `target`. If no such pair exists, return `None`.

**Explanation**: Similar to the classic version, but we use a `set` since we only need to track the existence of values, not their indices. This is slightly more memory-efficient when indices aren't required.

```python
def two_sum_values(nums: list[int], target: int) -> list[int] | None:
    """
    Find two numbers that add up to target.

    Time: $O(n)$ - average case. $O(n^2)$ worst case if many hash collisions.
    Space: $O(n)$ - set storage

    Example:
    nums = [2, 7, 11, 15], target = 9 → [2, 7]
    """
    seen = set()

    for num in nums:
        complement = target - num

        if complement in seen:
            return [complement, num]

        seen.add(num)

    return None
```

---

## Template: Two Sum - Count Pairs

**Problem**: Given an array of integers `nums` and an integer `target`, return the total number of pairs that sum up to `target`.

**Explanation**: We use a `Counter` to get the frequency of each number. For each unique number, we check if its complement (`target - num`) exists. If `num == complement`, we choose 2 instances from the available count (nC2). If `num != complement`, we multiply their respective frequencies. We only process each pair once by checking `complement > num`.

```python
def two_sum_count(nums: list[int], target: int) -> int:
    """
    Count pairs that sum to target.

    Time: $O(n)$ - one pass through the counts
    Space: $O(n)$ - Counter storage

    Example:
    nums = [1, 1, 1], target = 2 → 3 (three ways to pick two 1s)
    """
    from collections import Counter

    count = Counter(nums)
    pairs = 0

    for num in count:
        complement = target - num

        if complement in count:
            if complement == num:
                # Same number: C(n, 2) = n * (n-1) / 2
                pairs += count[num] * (count[num] - 1) // 2
            elif complement > num:
                # Different numbers: count all combinations
                pairs += count[num] * count[complement]

    return pairs
```

---

## Template: Two Sum - All Pairs (Handle Duplicates)

**Problem**: Given an array of integers `nums` and an integer `target`, find all unique pairs that sum up to `target`.

**Explanation**: To ensure uniqueness of pairs, we use a frequency map and a `used` set. For each number, if its complement exists and hasn't been used in a pair yet, we add the pair to our result. If the number is its own complement, we ensure there are at least two occurrences.

```python
def two_sum_all_pairs(nums: list[int], target: int) -> list[tuple[int, int]]:
    """
    Find all unique pairs that sum to target.

    Time: $O(n)$ - one pass through counts
    Space: $O(n)$ - Counter and used set storage

    Example:
    nums = [1, 1, 2, 2, 3, 3], target = 4 → [(1, 3), (2, 2)]
    """
    from collections import Counter

    count = Counter(nums)
    result = []
    used = set()

    for num in count:
        if num in used:
            continue

        complement = target - num

        if complement in count:
            if complement == num:
                # Need at least 2 of same number
                if count[num] >= 2:
                    result.append((num, num))
            else:
                result.append((min(num, complement), max(num, complement)))

            used.add(num)
            used.add(complement)

    return result
```

---

## Template: Two Sum II - Sorted Array

**Problem**: Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific `target` number.

**Explanation**: Since the array is sorted, we can use two pointers (left and right). If the `current_sum` is too small, we increment the left pointer to increase the sum. If it's too large, we decrement the right pointer. This achieves $O(1)$ space complexity, which is better than the $O(n)$ hashmap approach.

```python
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    """
    Two Sum on sorted array - use two pointers instead of hashmap.
    Returns 1-indexed positions.

    Time: $O(n)$
    Space: $O(1)$ - better than hashmap!

    Example:
    numbers = [2, 7, 11, 15], target = 9 → [1, 2]
    """
    left, right = 0, len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]

        if current_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return []
```

**Key Insight**: For sorted arrays, two pointers is $O(1)$ space vs $O(n)$ for hashmap.

---

## Template: 3Sum (Extension of Two Sum)

**Problem**: Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`. The solution set must not contain duplicate triplets.

**Explanation**: We sort the array first. Then, we iterate through the array, fixing one element `nums[i]` and treating the rest of the problem as a "Two Sum II" (sorted) problem for the remaining target `-nums[i]`. We skip duplicate values for both the fixed element and the two pointers to ensure the result contains only unique triplets.

```python
def three_sum(nums: list[int]) -> list[tuple[int, int, int]]:
    """
    Find all unique triplets that sum to zero.

    Time: $O(n^2)$ - sort + two-pointer for each element
    Space: $O(n)$ or $O(\\log n)$ - Python's list.sort() uses Timsort which requires $O(n)$ space. In C++, std::sort takes $O(\\log n)$ space.

    Example:
    nums = [-1, 0, 1, 2, -1, -4] → [(-1, -1, 2), (-1, 0, 1)]
    """
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 2):
        # Skip duplicates for first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Two Sum II on remaining array
        target = -nums[i]
        left, right = i + 1, n - 1

        while left < right:
            current_sum = nums[left] + nums[right]

            if current_sum == target:
                result.append((nums[i], nums[left], nums[right]))

                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1

    return result
```

---

## Template: 4Sum (Generalized K-Sum)

**Problem**: Given an array `nums` of `n` integers, return an array of all the unique quadruplets `[nums[a], nums[b], nums[c], nums[d]]` such that their sum equals `target`.

**Explanation**: This is an extension of 3Sum. We fix two elements using nested loops and then use the two-pointer approach for the remaining two. Sorting and duplicate skipping are essential to maintain the uniqueness of the quadruplets.

```python
def four_sum(nums: list[int], target: int) -> list[tuple[int, int, int, int]]:
    """
    Find all unique quadruplets that sum to target.

    Time: $O(n^3)$ - fix two nested loops, two-pointer for the rest
    Space: $O(n)$ or $O(\\log n)$ - depending on the sorting algorithm implementation.

    Example:
    nums = [1, 0, -1, 0, -2, 2], target = 0
    → [(-2, -1, 1, 2), (-2, 0, 0, 2), (-1, 0, 0, 1)]
    """
    nums.sort()
    n = len(nums)
    result = []

    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue

            # Two Sum II for remaining two numbers
            left, right = j + 1, n - 1
            remaining = target - nums[i] - nums[j]

            while left < right:
                current_sum = nums[left] + nums[right]

                if current_sum == remaining:
                    result.append((nums[i], nums[j], nums[left], nums[right]))

                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1

                    left += 1
                    right -= 1
                elif current_sum < remaining:
                    left += 1
                else:
                    right -= 1

    return result
```

---

## Template: Two Sum Less Than K

**Problem**: Given an array `nums` of integers and integer `k`, return the maximum `sum` such that there exists `i < j` with `nums[i] + nums[j] = sum` and `sum < k`. If no such `i, j` exists, return -1.

**Explanation**: We sort the array and use two pointers. If `nums[left] + nums[right]` is less than `k`, it's a potential candidate. We record the sum and move the left pointer to try and find an even larger sum that is still less than `k`. If the sum is already `>= k`, we must decrease it by moving the right pointer left.

```python
def two_sum_less_than_k(nums: list[int], k: int) -> int:
    """
    Find maximum sum of two numbers that is less than k.

    Time: $O(n \log n)$ - sorting
    Space: $O(1)$

    Example:
    nums = [34, 23, 1, 24, 75, 33, 54, 8], k = 60 → 58 (34 + 24)
    """
    nums.sort()
    left, right = 0, len(nums) - 1
    max_sum = -1

    while left < right:
        current_sum = nums[left] + nums[right]

        if current_sum < k:
            max_sum = max(max_sum, current_sum)
            left += 1  # Try to find larger sum
        else:
            right -= 1  # Sum too large

    return max_sum
```

---

## Template: Pair with Closest Sum

**Problem**: Given an array `nums` and a `target`, find the pair of elements whose sum is closest to the `target`.

**Explanation**: After sorting, we use two pointers to explore possible sums. We maintain a `closest_diff` and update our result whenever we find a pair with a smaller absolute difference from the target. We move pointers based on whether the `current_sum` is smaller or larger than the target to converge on the closest possible value.

```python
def two_sum_closest(nums: list[int], target: int) -> list[int]:
    """
    Find pair with sum closest to target.

    Time: $O(n \log n)$
    Space: $O(1)$

    Example:
    nums = [1, 2, 3, 4, 5], target = 10 → [4, 5] (sum = 9)
    """
    nums.sort()
    left, right = 0, len(nums) - 1
    closest_diff = float('inf')
    result = []

    while left < right:
        current_sum = nums[left] + nums[right]
        diff = abs(current_sum - target)

        if diff < closest_diff:
            closest_diff = diff
            result = [nums[left], nums[right]]

        if current_sum < target:
            left += 1
        elif current_sum > target:
            right -= 1
        else:
            return result  # Exact match

    return result
```

---

## Common Variations

| Variation      | Key Change                             |
| -------------- | -------------------------------------- |
| Return indices | Store index in hashmap                 |
| Return values  | Use set instead                        |
| Count pairs    | Use Counter, handle same number case   |
| Sorted array   | Two pointers instead of hashmap        |
| 3Sum/4Sum      | Fix first element(s), use two pointers |
| Less than K    | Two pointers on sorted array           |
| Closest sum    | Track minimum difference               |

---

## Edge Cases

```python
# Empty or small array
[] → []
[1] → []

# No solution
[1, 2, 3], target=10 → []

# Duplicate values
[3, 3], target=6 → [0, 1] (need two 3s, not same index)

# Negative numbers
[-1, 2, 3, -4], target=-5 → [-1, -4] or indices

# Zero as target
[0, 0, 1], target=0 → [0, 1]

# Large numbers (overflow in other languages)
[2**30, 2**30], target=2**31 → handle carefully
```

---

## Interview Tips

1. **Clarify requirements**: Return indices or values? Handle duplicates?
2. **Mention brute force first**: "The naive approach is $O(n^2)$, but we can do better with a hashmap"
3. **Consider sorted input**: If sorted, mention two-pointer as $O(1)$ space alternative
4. **Handle edge cases**: Empty array, single element, no solution

---

## Practice Problems

| #   | Problem                                            | Difficulty | Pattern Variant             |
| --- | -------------------------------------------------- | ---------- | --------------------------- |
| 1   | Two Sum                                            | Easy       | Classic hashmap             |
| 2   | Two Sum II - Input Array Is Sorted                 | Medium     | Two pointers                |
| 3   | 3Sum                                               | Medium     | Fix one + two pointers      |
| 4   | 3Sum Closest                                       | Medium     | Two pointers + tracking     |
| 5   | 4Sum                                               | Medium     | Fix two + two pointers      |
| 6   | Two Sum Less Than K                                | Easy       | Two pointers + max tracking |
| 7   | Pairs of Songs With Total Duration Divisible by 60 | Medium     | Modular two sum             |
| 8   | Count Pairs With XOR in a Range                    | Hard       | Two sum with XOR            |

---

## Key Takeaways

1. **Two Sum is the foundation** for many hashmap problems
2. **Hashmap gives $O(n)$** by storing complements for $O(1)$ lookup
3. **Sorted arrays use two pointers** for $O(1)$ space
4. **K-Sum reduces to Two Sum** by fixing k-2 elements
5. **Handle duplicates carefully** - skip or count appropriately
6. **Always clarify** indices vs values, duplicates handling

---

## Next: [03-frequency-counting.md](./03-frequency-counting.md)

Learn frequency counting patterns for top K problems and more.
