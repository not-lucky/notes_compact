# Search in Rotated Sorted Array

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md)

## Interview Context

Rotated array search is a FANG+ favorite because:
1. **Tests adaptability**: Standard binary search needs modification
2. **Multiple variants**: With/without duplicates, find target/minimum
3. **Requires careful analysis**: Must identify the sorted half
4. **Edge case heavy**: Boundary conditions are tricky

---

## What is a Rotated Sorted Array?

A sorted array rotated at some pivot:

```
Original: [0, 1, 2, 4, 5, 6, 7]
Rotated:  [4, 5, 6, 7, 0, 1, 2]  (rotated at index 4)
               ↑
            pivot point
```

Properties:
- The array consists of two sorted subarrays
- One half is always completely sorted
- The minimum element is at the rotation point

---

## The Core Insight

At any `mid` point, **at least one half is sorted**:

```
[4, 5, 6, 7, 0, 1, 2]
 L        M        R

nums[L]=4 <= nums[M]=7  → Left half [4,5,6,7] is sorted
nums[M]=7 > nums[R]=2   → Right half contains rotation
```

Strategy:
1. Find which half is sorted
2. Check if target is in the sorted half
3. Search accordingly

---

## Search in Rotated Array (No Duplicates)

LeetCode 33: Search in Rotated Sorted Array

```python
def search(nums: list[int], target: int) -> int:
    """
    Search target in rotated sorted array (no duplicates).

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # Determine which half is sorted
        if nums[left] <= nums[mid]:
            # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1  # Target in left half
            else:
                left = mid + 1   # Target in right half
        else:
            # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1   # Target in right half
            else:
                right = mid - 1  # Target in left half

    return -1
```

---

## Visual Walkthrough

Finding target=0 in [4, 5, 6, 7, 0, 1, 2]:

```
Step 1: [4, 5, 6, 7, 0, 1, 2]
         L        M        R

         nums[L]=4 <= nums[M]=7 → Left sorted
         Is 4 <= 0 < 7? No
         Search right half, L = mid + 1 = 4

Step 2: [4, 5, 6, 7, 0, 1, 2]
                     L  M  R

         nums[L]=0 <= nums[M]=1 → Left sorted
         Is 0 <= 0 < 1? Yes
         Search left half, R = mid - 1 = 4

Step 3: [4, 5, 6, 7, 0, 1, 2]
                     LR
                     M

         nums[M]=0 == target
         Return mid = 4
```

---

## Search in Rotated Array (With Duplicates)

LeetCode 81: Search in Rotated Sorted Array II

Duplicates break the `nums[left] <= nums[mid]` check:

```
[1, 0, 1, 1, 1]
 L     M     R

nums[L]=1, nums[M]=1, nums[R]=1
Can't determine which half is sorted!
```

Solution: Skip duplicates at boundaries.

```python
def search_with_duplicates(nums: list[int], target: int) -> bool:
    """
    Search target in rotated sorted array (with duplicates).

    Time: O(n) worst case, O(log n) average
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return True

        # Handle duplicates: can't determine sorted half
        if nums[left] == nums[mid] == nums[right]:
            left += 1
            right -= 1
        elif nums[left] <= nums[mid]:
            # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return False
```

**Important**: With duplicates, worst case is O(n) when all elements are the same except one.

---

## Alternative Approach: Find Pivot First

1. Find the rotation point (minimum element)
2. Determine which half contains target
3. Do standard binary search on that half

```python
def search_via_pivot(nums: list[int], target: int) -> int:
    """
    Search by first finding rotation point.

    Time: O(log n)
    Space: O(1)
    """
    n = len(nums)

    # Find rotation point (minimum element index)
    left, right = 0, n - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    pivot = left

    # Determine which half to search
    if target >= nums[pivot] and target <= nums[n - 1]:
        left, right = pivot, n - 1
    else:
        left, right = 0, pivot - 1

    # Standard binary search
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

---

## Complexity Analysis

| Variant | Time | Space |
|---------|------|-------|
| No duplicates | O(log n) | O(1) |
| With duplicates | O(n) worst, O(log n) avg | O(1) |
| Find pivot first | O(log n) | O(1) |

---

## Common Mistakes

### 1. Wrong Sorted Half Detection

```python
# Wrong: using < instead of <=
if nums[left] < nums[mid]:  # Fails when left == mid

# Correct: use <=
if nums[left] <= nums[mid]:
```

### 2. Wrong Target Range Check

```python
# Wrong: missing = sign
if nums[left] < target < nums[mid]:  # Misses when target == nums[left]

# Correct: include left boundary
if nums[left] <= target < nums[mid]:
```

### 3. Not Handling Single Element

```python
# Edge case: single element
nums = [1], target = 1
# Make sure left <= right condition catches this
```

---

## Variant: Search in Nearly Sorted Array

Array where element at index `i` may be at `i-1`, `i`, or `i+1`:

```python
def search_nearly_sorted(nums: list[int], target: int) -> int:
    """
    Search in array where elements can be ±1 from sorted position.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        # Check mid and neighbors
        if nums[mid] == target:
            return mid
        if mid > left and nums[mid - 1] == target:
            return mid - 1
        if mid < right and nums[mid + 1] == target:
            return mid + 1

        # Decide which half
        if nums[mid] < target:
            left = mid + 2  # Skip mid+1 (already checked)
        else:
            right = mid - 2  # Skip mid-1 (already checked)

    return -1
```

---

## Edge Cases Checklist

- [ ] Array not rotated (rotation = 0)
- [ ] Single element
- [ ] Two elements
- [ ] Target is first element
- [ ] Target is last element
- [ ] Target is at rotation point
- [ ] Target not in array
- [ ] All duplicates (for variant with duplicates)

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Search in Rotated Sorted Array | Medium | Identify sorted half |
| 2 | Search in Rotated Sorted Array II | Medium | Handle duplicates |
| 3 | Find Minimum in Rotated Sorted Array | Medium | Find pivot |
| 4 | Find Minimum in Rotated Sorted Array II | Hard | Duplicates + pivot |
| 5 | Rotation Count | Medium | Index of minimum |

---

## Interview Tips

1. **Clarify duplicates**: Significantly changes complexity
2. **Draw the array**: Visualize the rotation
3. **State your approach**: "First identify which half is sorted"
4. **Handle edge cases**: Non-rotated array, single element
5. **Mention tradeoffs**: One-pass vs find-pivot-first approaches

---

## Key Takeaways

1. **One half is always sorted**: Key insight for binary search
2. **Check target in sorted half**: Easier to verify bounds
3. **Duplicates complicate things**: May need linear fallback
4. **Two approaches**: Single-pass or find-pivot-first
5. **Watch boundary conditions**: Include/exclude equals signs carefully

---

## Next: [04-find-minimum-rotated.md](./04-find-minimum-rotated.md)

Finding the minimum element (rotation point) in rotated arrays.
