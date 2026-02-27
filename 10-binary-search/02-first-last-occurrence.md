# First and Last Occurrence

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md)

## Interview Context

Finding boundaries in sorted arrays is a classic interview pattern. It frequently appears in FANG interviews because it:

1. **Tests template mastery**: Requires modifying standard binary search logic, specifically Template 2 and Template 3.
2. **Proves edge-case awareness**: Exposes off-by-one errors and infinite loop traps when handling duplicates.
3. **Common building block**: Used as a subroutine in many complex problems (e.g., counting elements, finding ranges).
4. **LeetCode classic**: "Find First and Last Position of Element in Sorted Array" (LC 34) is a highly-tested question.

---

## Building Intuition

**Why Can't Standard Binary Search Find Boundaries?**

Standard binary search stops at the *first match it encounters*. If an array has duplicates, this match could be anywhere in the cluster of identical values.

```text
Array: [1, 2, 2, 2, 2, 2, 3]
Target: 2
                ↑
       Standard search might land on this '2' and stop.
       But the FIRST '2' is at index 1.
       And the LAST '2' is at index 5.
```

**The Key Insight: Don't Stop When You Find It**

Instead of returning immediately when `nums[mid] == target`, we must:

1. **Record the match**: Save the current index (it might be our final boundary).
2. **Keep searching**: Narrow the search space in the direction of the boundary we are looking for.

**Mental Model: The Thorough Detective**

Imagine you're a detective looking for the *first* person in a line who matches a description.
- **Lazy Detective** (Standard BS): Finds *a* match, stops looking, and says "Found one!"
- **Thorough Detective** (Boundary BS): Finds a match at index 5, records it, but says "Let me check indices 0-4 to see if there's an earlier match."

To find boundaries, we run two separate modified binary searches:
- **First occurrence (Left Boundary)**: If `nums[mid] >= target`, we know the first occurrence is at `mid` or to the left, so we search left (`right = mid`).
- **Last occurrence (Right Boundary)**: If `nums[mid] <= target`, we know the last occurrence is at `mid` or to the right, so we search right (`left = mid`).

**Visual: The Search Space Shrinks Toward the Boundary**

```text
Finding FIRST 2 in [1, 2, 2, 2, 2, 2, 3]:

Round 1: [1, 2, 2, 2, 2, 2, 3] (L=0, R=6)
                     M           nums[3]=2 >= 2. Search LEFT (R=M=3)

Round 2: [1, 2, 2, 2]          (L=0, R=3)
             M                   nums[1]=2 >= 2. Search LEFT (R=M=1)

Round 3: [1, 2]                (L=0, R=1)
          M                      nums[0]=1 < 2. Search RIGHT (L=M+1=1)

Done: L=1, R=1. First occurrence is at index 1.
```

---

## When NOT to Use Boundary Search

**1. When Any Occurrence Is Fine**
If you just need to check *existence*, standard binary search is simpler and can return slightly faster on average.

**2. Unsorted Arrays**
Boundaries only make sense in sorted order. For unsorted data, just scan linearly.

**3. When There Are Guaranteed No Duplicates**
If the array has distinct elements, standard binary search gives you the only occurrence.

**Red Flags:**
- "Find *any* element matching..." → Use standard search
- "Check if element exists..." → Use standard search
- "Find index in unsorted array..." → Linear scan (O(N))

---

## Core Problem: Search Range (LeetCode 34)

Given an array of integers `nums` sorted in non-decreasing order, find the starting and ending position of a given `target` value. If `target` is not found, return `[-1, -1]`.

Must write an algorithm with $O(\log n)$ runtime complexity.

```text
Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]

Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]
```

---

## The Solution: Two Binary Searches

We can write two distinct helper functions to find the left and right boundaries. This modular approach is much cleaner to explain in interviews than trying to cram both into one complex loop.

### 1. Finding First Occurrence (Left Boundary)

This uses Template 2 (Find Left Boundary). We search for the first index where `nums[i] >= target`.

```python
def find_first(nums: list[int], target: int) -> int:
    """
    Find leftmost index of target.
    Time: O(log n) | Space: O(1)
    """
    if not nums:
        return -1

    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] >= target:
            right = mid  # Answer could be mid, keep searching left
        else:
            left = mid + 1 # Answer must be to the right of mid

    # Check if target actually exists
    return left if nums[left] == target else -1
```

### 2. Finding Last Occurrence (Right Boundary)

This uses Template 3 (Find Right Boundary). We search for the last index where `nums[i] <= target`.

```python
def find_last(nums: list[int], target: int) -> int:
    """
    Find rightmost index of target.
    Time: O(log n) | Space: O(1)
    """
    if not nums:
        return -1

    left, right = 0, len(nums) - 1

    while left < right:
        # CRITICAL: We round UP for right boundary search (mid = left + (right - left + 1) // 2)
        # Without + 1, we get an infinite loop when left = right - 1
        mid = left + (right - left + 1) // 2

        if nums[mid] <= target:
            left = mid     # Answer could be mid, keep searching right
        else:
            right = mid - 1 # Answer must be to the left of mid

    # Check if target actually exists
    return left if nums[left] == target else -1
```

### Complete Solution

```python
def searchRange(nums: list[int], target: int) -> list[int]:
    # It's perfectly fine to define helpers inside the main function
    # or just call them if they are class methods.

    first = find_first(nums, target)

    # Optimization: If the target isn't found at all, we don't need
    # to search for the last occurrence.
    if first == -1:
        return [-1, -1]

    last = find_last(nums, target)

    return [first, last]
```

---

## Production Code: Using Python's `bisect`

In a FANG interview, you should *always* code the binary search from scratch unless the interviewer explicitly tells you to use library functions. However, knowing how to use `bisect` is a strong signal of Python mastery.

```python
import bisect

def search_range_bisect(nums: list[int], target: int) -> list[int]:
    if not nums:
        return [-1, -1]

    # bisect_left returns the FIRST position where target could be inserted
    # It tells us where the left boundary is (or would be)
    left_idx = bisect.bisect_left(nums, target)

    # Validate the target actually exists at the left_idx
    if left_idx == len(nums) or nums[left_idx] != target:
        return [-1, -1]

    # bisect_right returns the position AFTER the LAST occurrence
    # So we subtract 1 to get the actual last occurrence index
    right_idx = bisect.bisect_right(nums, target) - 1

    return [left_idx, right_idx]
```

---

## Common Application: Counting Occurrences

Once you know the boundaries, counting the frequency of an element in a sorted array is $O(1)$ math, keeping the total time complexity strictly $O(\log n)$.

```python
def count_occurrences(nums: list[int], target: int) -> int:
    """Time: O(log n) | Space: O(1)"""
    first = find_first(nums, target)
    if first == -1:
        return 0

    last = find_last(nums, target)

    # Formula: right_boundary - left_boundary + 1
    return last - first + 1
```

---

## Alternative: Unified "Find Boundary" Function

To avoid repeating code, you can combine the two searches into one function using a boolean flag. This is elegant but can be slightly harder to explain during a high-pressure interview. Use whatever you are most comfortable with.

```python
def searchRange(nums: list[int], target: int) -> list[int]:
    def find_boundary(find_first: bool) -> int:
        if not nums:
            return -1

        left, right = 0, len(nums) - 1

        while left < right:
            # Round down for first, up for last
            mid = left + (right - left + (0 if find_first else 1)) // 2

            if nums[mid] == target:
                if find_first:
                    right = mid      # Keep searching left for first
                else:
                    left = mid       # Keep searching right for last
            elif nums[mid] < target:
                left = mid + 1       # Target must be right
            else:
                right = mid - 1      # Target must be left

        return left if nums[left] == target else -1

    first = find_boundary(True)
    if first == -1:
        return [-1, -1]

    last = find_boundary(False)
    return [first, last]
```

---

## Related Boundary Problems

### 1. Find Smallest Letter Greater Than Target (LC 744)

Instead of finding an exact match, we want the first element *strictly greater* than the target. The array wraps around (circular).

```python
def nextGreatestLetter(letters: list[str], target: str) -> str:
    """Time: O(log n) | Space: O(1)"""
    left, right = 0, len(letters) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if letters[mid] > target:
            # mid might be the answer, but there could be a smaller valid letter to the left
            right = mid - 1
        else:
            # mid is smaller or equal to target, so we must search right
            left = mid + 1

    # After the loop, 'left' points to the first element strictly greater than target.
    # If target is >= the last letter, 'left' will be len(letters).
    # The modulo operator gracefully handles the wrap-around requirement!
    return letters[left % len(letters)]
```

### 2. Single Element in a Sorted Array (LC 540)

Every element appears twice except for one. The array is sorted. Find the single element in $O(\log n)$ time.

**Key Insight:** Index parity.
Because elements appear in pairs, they naturally start at even indices.
- **Before the single element:** Pairs start at even indices, so `nums[even] == nums[even+1]`.
- **After the single element:** The sequence is shifted by one, so pairs start at odd indices, meaning `nums[even] != nums[even+1]`.

This gives us a clear binary condition to search for the first element that violates the `nums[even] == nums[even+1]` rule.

```python
def singleNonDuplicate(nums: list[int]) -> int:
    """Time: O(log n) | Space: O(1)"""
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        # A common bitwise trick: mid ^ 1 toggles the last bit
        # If mid is even, mid ^ 1 is mid + 1
        # If mid is odd, mid ^ 1 is mid - 1
        # This elegantly pairs every even index with its subsequent odd index
        if nums[mid] == nums[mid ^ 1]:
            # The pair is intact, so the single element is to the right
            left = mid + 1
        else:
            # The pair is broken, so the single element is at mid or to the left
            right = mid

    return nums[left]
```

---

## Complexity Analysis

| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Find First Occurrence | $O(\log n)$ | $O(1)$ |
| Find Last Occurrence | $O(\log n)$ | $O(1)$ |
| Find Range `[first, last]` | $O(\log n)$ | $O(1)$ |
| Count Occurrences | $O(\log n)$ | $O(1)$ |

*Note: Even though finding the range requires running binary search twice, $O(2 \times \log n)$ simplifies to $O(\log n)$.*

---

## Edge Cases Checklist

When writing your code or tracing an example, test these cases:

- [ ] **Empty array**: `[]` → should safely return `[-1, -1]`
- [ ] **Target not in array**: `[1, 2, 4, 5]`, target=3 → `[-1, -1]`
- [ ] **Single element, match**: `[5]`, target=5 → `[0, 0]`
- [ ] **Single element, no match**: `[5]`, target=3 → `[-1, -1]`
- [ ] **All elements are target**: `[2, 2, 2, 2]`, target=2 → `[0, 3]`
- [ ] **Target at edges**: `[2, 3, 4, 5]`, target=2 or target=5.

---

## Interview Tips

1. **Optimize out the second search:** If `find_first` returns `-1`, don't bother running `find_last`. Mention this optimization to your interviewer.
2. **Explain the continuous search:** Clearly articulate *why* you are moving `right = mid` or `left = mid` even after finding the target. "I found a match, but I need to make sure there isn't an earlier/later match to its left/right."
3. **Be prepared to write it modularly:** It's usually better to write a `findBound(nums, target, isFirst)` helper rather than duplicating the binary search loop, but only if you are confident you won't introduce bugs with the boolean logic and integer rounding (`mid = ... + 1`). If in doubt, write two separate functions.
4. **Never use `.index()` or `.count()`**: In Python, these are $O(n)$ operations. Using them immediately fails the $O(\log n)$ constraint.

---

## Next Steps

Now that you understand how to modify binary search to find boundaries, let's look at how to apply binary search to arrays that aren't perfectly sorted.

**Next:** [Search in Rotated Sorted Arrays](./03-search-rotated-array.md)
