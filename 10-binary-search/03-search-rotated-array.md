# Search in Rotated Sorted Array

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md)

## Interview Context

Rotated array search is a FANG+ favorite because:

1. **Tests adaptability**: Standard binary search needs modification
2. **Multiple variants**: With/without duplicates, find target/minimum
3. **Requires careful analysis**: Must identify the sorted half
4. **Edge case heavy**: Boundary conditions are tricky

---

## Building Intuition

**What Happens When You Rotate a Sorted Array?**

```
Original: [0, 1, 2, 3, 4, 5, 6, 7]
                        ↓ rotate at index 4
Rotated:  [4, 5, 6, 7, 0, 1, 2, 3]
                    ↑
             This is the "pivot"
```

The array breaks into TWO sorted subarrays joined at the pivot:

- Left portion: [4, 5, 6, 7] — sorted, but all values are LARGER
- Right portion: [0, 1, 2, 3] — sorted, but all values are SMALLER

**The Key Insight: One Half Is ALWAYS Sorted**

No matter where you pick `mid`, at least one half (left or right) is completely sorted. Why?

```
Case 1: mid is in the LEFT portion (larger values)
[4, 5, 6, 7, 0, 1, 2, 3]
       ↑
      mid=6
Left half [4,5,6] is sorted (we're before the pivot)
Right half [7,0,1,2,3] contains the pivot

Case 2: mid is in the RIGHT portion (smaller values)
[4, 5, 6, 7, 0, 1, 2, 3]
                ↑
               mid=1
Left half [4,5,6,7,0] contains the pivot
Right half [1,2,3] is sorted (we're after the pivot)
```

**Mental Model: The Mountain Range**

Think of the rotated array as two mountains side by side:

- A tall mountain (the larger values before rotation)
- A shorter mountain (the smaller values)

Binary search is like asking: "Is my target on the tall mountain or the short one?" Once you know which sorted slope to search, it's standard binary search.

**How to Identify the Sorted Half**

Compare `nums[left]` with `nums[mid]`:

- If `nums[left] <= nums[mid]`: Left half is sorted (no pivot in between)
- Otherwise: Right half is sorted

Then check if your target falls within the sorted half's range.

**Why This Works**

The sorted half has a predictable range: `[nums[left], nums[mid]]` or `[nums[mid], nums[right]]`. You can definitively say whether target is in that range. If not, target must be in the other (unsorted) half—and you recurse there.

---

## When NOT to Use Rotated Array Search

**1. The Array Isn't Rotated**

- A "rotation of 0" or "rotation of n" is just a sorted array
- Use standard binary search (it's simpler)
- The rotated search still works, but why add complexity?

**2. Array Has Many Duplicates**

- Duplicates break the `nums[left] <= nums[mid]` check
- Worst case degrades to O(n)
- See the variant with duplicates below

**3. Array Is Not Sorted Before Rotation**

- If original array wasn't sorted, rotation means nothing
- No binary search will help

**4. You Need All Occurrences**

- Rotated search finds ONE occurrence
- For all occurrences, you'd need additional boundary searches

**Red Flags in Problem Statements:**

- "Array may have duplicates" → Use O(n) fallback or careful duplicate handling
- "Find all positions of target" → Rotated search + boundary search
- "Array is not sorted" → Different problem entirely

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

| Variant          | Time                     | Space |
| ---------------- | ------------------------ | ----- |
| No duplicates    | O(log n)                 | O(1)  |
| With duplicates  | O(n) worst, O(log n) avg | O(1)  |
| Find pivot first | O(log n)                 | O(1)  |

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

| #   | Problem                                 | Difficulty | Key Insight          |
| --- | --------------------------------------- | ---------- | -------------------- |
| 1   | Search in Rotated Sorted Array          | Medium     | Identify sorted half |
| 2   | Search in Rotated Sorted Array II       | Medium     | Handle duplicates    |
| 3   | Find Minimum in Rotated Sorted Array    | Medium     | Find pivot           |
| 4   | Find Minimum in Rotated Sorted Array II | Hard       | Duplicates + pivot   |
| 5   | Rotation Count                          | Medium     | Index of minimum     |

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
