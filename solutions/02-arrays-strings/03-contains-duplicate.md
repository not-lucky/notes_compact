# Contains Duplicate

## Problem Statement

Given an integer array `nums`, return `true` if any value appears at least twice, and `false` if every element is distinct.

**Example:**
```
Input: nums = [1, 2, 3, 1]
Output: true

Input: nums = [1, 2, 3, 4]
Output: false
```

## Approach

### Method 1: Hash Set (Optimal)
Add elements to a set. If element already exists, return True.

### Method 2: Sorting
Sort array. Check if any adjacent elements are equal.

### Method 3: Brute Force
Check every pair - O(n²), not recommended.

## Implementation

```python
def contains_duplicate(nums: list[int]) -> bool:
    """
    Check if array contains any duplicates using hash set.

    Time: O(n) - single pass
    Space: O(n) - set stores up to n elements
    """
    seen = set()

    for num in nums:
        if num in seen:
            return True
        seen.add(num)

    return False


def contains_duplicate_pythonic(nums: list[int]) -> bool:
    """
    One-liner using set length comparison.

    Time: O(n) - set creation
    Space: O(n) - set storage
    """
    return len(nums) != len(set(nums))


def contains_duplicate_sorting(nums: list[int]) -> bool:
    """
    Sort and check adjacent elements.

    Time: O(n log n) - sorting
    Space: O(1) or O(n) - depends on sort implementation
    """
    nums.sort()

    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]:
            return True

    return False
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Hash Set | O(n) | O(n) | Best for general case |
| Sorting | O(n log n) | O(1)* | Better if space is limited |
| Brute Force | O(n²) | O(1) | Never use this |

*Space depends on whether in-place sorting is allowed

## Edge Cases

1. **Empty array**: No duplicates, return False
2. **Single element**: Can't have duplicate, return False
3. **All same elements**: `[1, 1, 1]` → True
4. **All unique**: `[1, 2, 3]` → False
5. **Large values**: Works with any integer range
6. **Negative numbers**: Handled same as positives

## Common Mistakes

1. **Forgetting edge cases**: Empty or single-element arrays
2. **Modifying input when sorting**: May not be allowed in some contexts

## Variations

### Contains Duplicate II
Return true if `nums[i] == nums[j]` AND `|i - j| <= k`.

```python
def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    """
    Check if duplicate exists within k indices.

    Time: O(n)
    Space: O(min(n, k)) - sliding window of size k
    """
    seen = {}  # value -> most recent index

    for i, num in enumerate(nums):
        if num in seen and i - seen[num] <= k:
            return True
        seen[num] = i

    return False
```

### Contains Duplicate III
Return true if `|nums[i] - nums[j]| <= t` AND `|i - j| <= k`.

```python
def contains_nearby_almost_duplicate(
    nums: list[int], index_diff: int, value_diff: int
) -> bool:
    """
    Check if almost-duplicate exists within index range.
    Uses bucket sort concept.

    Time: O(n)
    Space: O(min(n, k))
    """
    if value_diff < 0:
        return False

    buckets = {}
    bucket_size = value_diff + 1  # Avoid division by zero

    for i, num in enumerate(nums):
        bucket_id = num // bucket_size

        # Check current bucket
        if bucket_id in buckets:
            return True

        # Check adjacent buckets
        if bucket_id - 1 in buckets and \
           abs(num - buckets[bucket_id - 1]) <= value_diff:
            return True
        if bucket_id + 1 in buckets and \
           abs(num - buckets[bucket_id + 1]) <= value_diff:
            return True

        # Add to bucket
        buckets[bucket_id] = num

        # Remove old bucket (sliding window)
        if i >= index_diff:
            old_bucket = nums[i - index_diff] // bucket_size
            del buckets[old_bucket]

    return False
```

## Related Problems

- **Contains Duplicate II** - Within k indices
- **Contains Duplicate III** - Within k indices and value diff t
- **Find All Duplicates in Array** - Return all duplicate values
- **Find the Duplicate Number** - Single duplicate, Floyd's cycle
- **First Missing Positive** - Related array manipulation
