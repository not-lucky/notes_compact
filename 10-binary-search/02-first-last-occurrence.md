# First and Last Occurrence

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md)

## Interview Context

Finding boundaries in sorted arrays is a classic interview pattern:
1. **Tests template mastery**: Requires modifying standard binary search
2. **Common building block**: Used in many other problems
3. **Edge case focus**: Handling duplicates, not found, boundaries
4. **LeetCode classic**: "Find First and Last Position of Element in Sorted Array"

---

## The Problem

Given a sorted array with duplicates, find:
- **First occurrence**: Leftmost index of target
- **Last occurrence**: Rightmost index of target
- **Range**: [first, last] positions

```
Array:  [1, 2, 2, 2, 3, 4, 5]
Target: 2
Output: first=1, last=3
```

---

## Pattern: Continue Searching After Finding

The key insight: **don't stop when you find the target**.

Standard binary search stops immediately when `nums[mid] == target`. To find boundaries, we record the match and continue searching in the appropriate direction.

---

## Finding First Occurrence (Left Boundary)

```python
def find_first(nums: list[int], target: int) -> int:
    """
    Find first occurrence of target in sorted array.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            result = mid       # Record this match
            right = mid - 1    # Keep searching left
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

### Visual Walkthrough

Finding first 2 in [1, 2, 2, 2, 3, 4, 5]:

```
Step 1: [1, 2, 2, 2, 3, 4, 5]
         L        M        R     mid=3, nums[3]=2==target
                                 result=3, search left

Step 2: [1, 2, 2, 2, 3, 4, 5]
         L  M  R                 mid=1, nums[1]=2==target
                                 result=1, search left

Step 3: [1, 2, 2, 2, 3, 4, 5]
         LR                      mid=0, nums[0]=1<target
         M                       search right

Step 4: [1, 2, 2, 2, 3, 4, 5]
            L                    left > right, stop
         R                       return result=1
```

---

## Finding Last Occurrence (Right Boundary)

```python
def find_last(nums: list[int], target: int) -> int:
    """
    Find last occurrence of target in sorted array.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            result = mid       # Record this match
            left = mid + 1     # Keep searching right
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

### Visual Walkthrough

Finding last 2 in [1, 2, 2, 2, 3, 4, 5]:

```
Step 1: [1, 2, 2, 2, 3, 4, 5]
         L        M        R     mid=3, nums[3]=2==target
                                 result=3, search right

Step 2: [1, 2, 2, 2, 3, 4, 5]
                     L  M  R     mid=5, nums[5]=4>target
                                 search left

Step 3: [1, 2, 2, 2, 3, 4, 5]
                     LR          mid=4, nums[4]=3>target
                     M           search left

Step 4: [1, 2, 2, 2, 3, 4, 5]
                  R  L           left > right, stop
                                 return result=3
```

---

## Complete Solution: Search Range

LeetCode 34: Find First and Last Position of Element in Sorted Array

```python
def search_range(nums: list[int], target: int) -> list[int]:
    """
    Find first and last position of target.

    Time: O(log n)
    Space: O(1)
    """
    def find_first():
        left, right = 0, len(nums) - 1
        result = -1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                result = mid
                right = mid - 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return result

    def find_last():
        left, right = 0, len(nums) - 1
        result = -1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                result = mid
                left = mid + 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return result

    return [find_first(), find_last()]
```

---

## Using Python's bisect

```python
import bisect

def search_range_bisect(nums: list[int], target: int) -> list[int]:
    """
    Using bisect module for boundary finding.

    Time: O(log n)
    Space: O(1)
    """
    left_idx = bisect.bisect_left(nums, target)

    # Check if target exists
    if left_idx >= len(nums) or nums[left_idx] != target:
        return [-1, -1]

    right_idx = bisect.bisect_right(nums, target) - 1

    return [left_idx, right_idx]
```

---

## Counting Occurrences

Once you have first and last positions:

```python
def count_occurrences(nums: list[int], target: int) -> int:
    """
    Count occurrences of target in sorted array.

    Time: O(log n)
    Space: O(1)
    """
    first = find_first(nums, target)
    if first == -1:
        return 0

    last = find_last(nums, target)
    return last - first + 1
```

---

## Alternative: Unified Template

A single function with a parameter:

```python
def find_boundary(nums: list[int], target: int, find_first: bool) -> int:
    """
    Find first or last occurrence based on flag.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            result = mid
            if find_first:
                right = mid - 1  # Search left for first
            else:
                left = mid + 1   # Search right for last
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

---

## Related Problems

### Find Smallest Letter Greater Than Target

```python
def next_greatest_letter(letters: list[str], target: str) -> str:
    """
    Find smallest letter greater than target (circular).

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(letters) - 1

    # If target >= last letter, wrap to first
    if target >= letters[-1]:
        return letters[0]

    while left < right:
        mid = left + (right - left) // 2

        if letters[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return letters[left]
```

### Find Element Appearing Once

In a sorted array where every element appears twice except one:

```python
def single_non_duplicate(nums: list[int]) -> int:
    """
    Find single element in sorted array of pairs.

    Key insight: Before single element, pairs start at even indices.
    After single element, pairs start at odd indices.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        # Ensure mid is even for pair comparison
        if mid % 2 == 1:
            mid -= 1

        # If pair is intact, single is to the right
        if nums[mid] == nums[mid + 1]:
            left = mid + 2
        else:
            right = mid

    return nums[left]
```

---

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Find first occurrence | O(log n) | O(1) |
| Find last occurrence | O(log n) | O(1) |
| Find range [first, last] | O(log n) | O(1) |
| Count occurrences | O(log n) | O(1) |

---

## Edge Cases Checklist

- [ ] Empty array → return -1 or [-1, -1]
- [ ] Single element, target found → [0, 0]
- [ ] Single element, target not found → [-1, -1]
- [ ] Target not in array → [-1, -1]
- [ ] All elements are target → [0, n-1]
- [ ] Target at beginning only → [0, 0]
- [ ] Target at end only → [n-1, n-1]

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Find First and Last Position | Medium | Left and right boundary |
| 2 | Count of Smaller Numbers After Self | Hard | Binary search tree / merge sort |
| 3 | Find Smallest Letter Greater Than Target | Easy | Right boundary with wrap |
| 4 | Single Element in Sorted Array | Medium | Pair index parity |
| 5 | Find Minimum in Rotated Sorted Array | Medium | Boundary in rotated |
| 6 | Search Insert Position | Easy | Left boundary |

---

## Interview Tips

1. **Clarify duplicates**: Ask if array has duplicates
2. **Handle not found**: Decide what to return (-1 vs insertion point)
3. **Explain the difference**: Why continue searching after match
4. **Consider bisect**: Mention Python's built-in for production code
5. **Test boundaries**: Check first element, last element, single element

---

## Key Takeaways

1. **Don't stop on match**: Record and continue searching
2. **Left boundary**: Continue searching left after match
3. **Right boundary**: Continue searching right after match
4. **Same complexity**: Still O(log n) with boundary search
5. **Building block**: Used in many advanced problems

---

## Next: [03-search-rotated-array.md](./03-search-rotated-array.md)

Search in arrays that have been rotated.
