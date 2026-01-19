# Two Sum Pattern

> **Prerequisites:** [01-hash-table-basics.md](./01-hash-table-basics.md)

## Interview Context

The Two Sum pattern is **the most important hashmap pattern** to master. It appears in:

- Direct "Two Sum" style questions
- As a building block for 3Sum, 4Sum, K-Sum
- In combination with other techniques (sliding window, binary search)

The core insight: instead of checking all pairs O(n²), use a hashmap to check if the complement exists in O(1).

**Interview frequency**: Very high. This is often the first coding question in a phone screen.

---

## Core Concept

**Problem**: Find two numbers in an array that add up to a target.

**Brute Force**: Check all pairs - O(n²)

**HashMap Approach**: For each number, check if `target - num` was seen before - O(n)

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

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find indices of two numbers that add up to target.

    Time: O(n) - single pass
    Space: O(n) - hashmap storage

    Example:
    nums = [2, 7, 11, 15], target = 9 → [0, 1]
    """
    seen = {}  # value → index

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

```python
def two_sum_values(nums: list[int], target: int) -> list[int] | None:
    """
    Find two numbers that add up to target.

    Time: O(n)
    Space: O(n)

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

```python
def two_sum_count(nums: list[int], target: int) -> int:
    """
    Count pairs that sum to target.

    Time: O(n)
    Space: O(n)

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

```python
def two_sum_all_pairs(nums: list[int], target: int) -> list[list[int]]:
    """
    Find all unique pairs that sum to target.

    Time: O(n)
    Space: O(n)

    Example:
    nums = [1, 1, 2, 2, 3, 3], target = 4 → [[1, 3], [2, 2]]
    """
    from collections import Counter

    count = Counter(nums)
    result = []
    used = set()

    for num in count:
        complement = target - num

        if complement in count and num not in used and complement not in used:
            if complement == num:
                # Need at least 2 of same number
                if count[num] >= 2:
                    result.append([num, num])
            else:
                result.append(sorted([num, complement]))
                used.add(complement)

            used.add(num)

    return result
```

---

## Template: Two Sum II - Sorted Array

```python
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    """
    Two Sum on sorted array - use two pointers instead of hashmap.
    Returns 1-indexed positions.

    Time: O(n)
    Space: O(1) - better than hashmap!

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

**Key Insight**: For sorted arrays, two pointers is O(1) space vs O(n) for hashmap.

---

## Template: 3Sum (Extension of Two Sum)

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    """
    Find all unique triplets that sum to zero.

    Time: O(n²) - sort + two-pointer for each element
    Space: O(1) excluding output (O(n) for sorting in Python)

    Example:
    nums = [-1, 0, 1, 2, -1, -4] → [[-1, -1, 2], [-1, 0, 1]]
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
                result.append([nums[i], nums[left], nums[right]])

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

```python
def four_sum(nums: list[int], target: int) -> list[list[int]]:
    """
    Find all unique quadruplets that sum to target.

    Time: O(n³)
    Space: O(1) excluding output

    Example:
    nums = [1, 0, -1, 0, -2, 2], target = 0
    → [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
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
                    result.append([nums[i], nums[j], nums[left], nums[right]])

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

```python
def two_sum_less_than_k(nums: list[int], k: int) -> int:
    """
    Find maximum sum of two numbers that is less than k.

    Time: O(n log n) - sorting
    Space: O(1)

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

```python
def two_sum_closest(nums: list[int], target: int) -> list[int]:
    """
    Find pair with sum closest to target.

    Time: O(n log n)
    Space: O(1)

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

| Variation | Key Change |
|-----------|------------|
| Return indices | Store index in hashmap |
| Return values | Use set instead |
| Count pairs | Use Counter, handle same number case |
| Sorted array | Two pointers instead of hashmap |
| 3Sum/4Sum | Fix first element(s), use two pointers |
| Less than K | Two pointers on sorted array |
| Closest sum | Track minimum difference |

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
2. **Mention brute force first**: "The naive approach is O(n²), but we can do better with a hashmap"
3. **Consider sorted input**: If sorted, mention two-pointer as O(1) space alternative
4. **Handle edge cases**: Empty array, single element, no solution

---

## Practice Problems

| # | Problem | Difficulty | Pattern Variant |
|---|---------|------------|-----------------|
| 1 | Two Sum | Easy | Classic hashmap |
| 2 | Two Sum II - Input Array Is Sorted | Medium | Two pointers |
| 3 | 3Sum | Medium | Fix one + two pointers |
| 4 | 3Sum Closest | Medium | Two pointers + tracking |
| 5 | 4Sum | Medium | Fix two + two pointers |
| 6 | Two Sum Less Than K | Easy | Two pointers + max tracking |
| 7 | Pairs of Songs With Total Duration Divisible by 60 | Medium | Modular two sum |
| 8 | Count Pairs With XOR in a Range | Hard | Two sum with XOR |

---

## Key Takeaways

1. **Two Sum is the foundation** for many hashmap problems
2. **Hashmap gives O(n)** by storing complements for O(1) lookup
3. **Sorted arrays use two pointers** for O(1) space
4. **K-Sum reduces to Two Sum** by fixing k-2 elements
5. **Handle duplicates carefully** - skip or count appropriately
6. **Always clarify** indices vs values, duplicates handling

---

## Next: [03-frequency-counting.md](./03-frequency-counting.md)

Learn frequency counting patterns for top K problems and more.
