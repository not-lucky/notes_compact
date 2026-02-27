# Search in Rotated Sorted Array

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md)

## What is a Rotated Sorted Array?

A sorted array that has been circularly shifted (rotated) at some unknown pivot index.

```text
Original: [0, 1, 2, 4, 5, 6, 7]
Rotated:  [4, 5, 6, 7, 0, 1, 2]  (rotated at index 4)
               ↑
            pivot point (minimum element)
```

**Key Properties:**
1. The array consists of **two completely sorted subarrays**.
2. All elements in the left subarray are strictly greater than all elements in the right subarray.
3. The minimum element is at the rotation point.

## Interview Context

Rotated array search is a FANG+ staple because:
1. **It tests fundamental adaptability**: Can you modify the standard binary search template when the array isn't fully sorted?
2. **It forces careful case analysis**: You must identify the sorted half and manage boundaries meticulously.
3. **It has multiple variants**: Searching for a target, handling duplicates, or finding the minimum element.

---

## The Core Concept: The "One Sorted Half" Rule

**The Insight:** No matter where you place your `mid` pointer, **at least one half of the array will always be completely sorted**.

```text
Case 1: mid is in the LEFT (taller) portion
[4, 5, 6, 7, 0, 1, 2, 3]
       ↑
      mid=6
Left half [4, 5, 6] is completely sorted.
Right half [7, 0, 1, 2, 3] contains the pivot.

Case 2: mid is in the RIGHT (shorter) portion
[4, 5, 6, 7, 0, 1, 2, 3]
                ↑
               mid=1
Left half [4, 5, 6, 7, 0] contains the pivot.
Right half [1, 2, 3] is completely sorted.
```

### How to use this property:
1. Compare `nums[left]` and `nums[mid]` to determine **which half is sorted**.
   - If `nums[left] <= nums[mid]`, the left half is sorted.
   - Otherwise, the right half is sorted.
2. Check if the `target` falls within the range of the **sorted** half.
   - If it does, discard the unsorted half.
   - If it doesn't, discard the sorted half.

---

## Approach 1: One-Pass Binary Search (Standard)

This is the standard, most expected approach in an interview for **LeetCode 33: Search in Rotated Sorted Array**.

```python
def search(nums: list[int], target: int) -> int:
    """
    Search target in rotated sorted array (no duplicates).

    Time: O(log n)
    Space: O(1)
    """
    if not nums:
        return -1

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # 1. Determine which half is completely sorted
        if nums[left] <= nums[mid]:
            # Left half is sorted

            # 2. Check if target is strictly within this sorted half
            if nums[left] <= target < nums[mid]:
                right = mid - 1  # Target is in the left half
            else:
                left = mid + 1   # Target must be in the right half
        else:
            # Right half is sorted

            # 2. Check if target is strictly within this sorted half
            if nums[mid] < target <= nums[right]:
                left = mid + 1   # Target is in the right half
            else:
                right = mid - 1  # Target must be in the left half

    return -1
```

### Visual Walkthrough
Finding `target=0` in `[4, 5, 6, 7, 0, 1, 2]`:
1. `L=0(4)`, `R=6(2)` -> `mid=3(7)`.
   `nums[L] <= nums[mid]` (4 <= 7) -> Left is sorted `[4, 5, 6, 7]`.
   Is `0` between `4` and `7`? No.
   Search right: `L = mid + 1 = 4`.
2. `L=4(0)`, `R=6(2)` -> `mid=5(1)`.
   `nums[L] <= nums[mid]` (0 <= 1) -> Left is sorted `[0, 1]`.
   Is `0` between `0` and `1`? Yes (`nums[L] <= 0 < nums[mid]`).
   Search left: `R = mid - 1 = 4`.
3. `L=4(0)`, `R=4(0)` -> `mid=4(0)`.
   `nums[mid] == 0`. Target found! Return 4.

---

## Approach 2: Find Pivot First (Two-Pass)

**FANG Fave Tip:** Many candidates struggle with the complex `if/else` bounds in the one-pass approach. The two-pass approach is often viewed favorably by interviewers because it breaks the problem into two simpler, standard binary searches.

1. **Find the rotation point (minimum element).** This tells us where the array is "split".
2. **Determine which sorted subarray the target belongs to.**
3. **Run a standard binary search** on that specific subarray.

```python
def search_via_pivot(nums: list[int], target: int) -> int:
    """
    Two-pass approach: Find pivot, then standard binary search.

    Time: O(log n)
    Space: O(1)
    """
    if not nums:
        return -1

    n = len(nums)

    # Pass 1: Find rotation point (index of minimum element)
    left, right = 0, n - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1   # Min is to the right
        else:
            right = mid      # Min is mid or to the left

    pivot = left  # Index of the minimum element

    # Pass 2: Determine which half to search
    # Since nums[pivot] is the absolute minimum:
    # If target is <= the last element, it must be in the right sorted portion
    if target <= nums[n - 1]:
        left, right = pivot, n - 1
    else:
        left, right = 0, pivot - 1

    # Pass 3: Standard binary search
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

## Follow-up: Search in Rotated Array (With Duplicates)

**LeetCode 81: Search in Rotated Sorted Array II**

When duplicates are allowed, the core check `nums[left] <= nums[mid]` breaks down.
Consider: `nums = [1, 0, 1, 1, 1]`, `target = 0`
- `L=0 (1)`, `M=2 (1)`.
- `nums[L] == nums[M]`. Which half is sorted? We don't know! It could be `[1, 1, 1, 0, 1]` or `[1, 0, 1, 1, 1]`.

**Solution:** When `nums[left] == nums[mid]`, we cannot safely eliminate either half based on standard logic. However, since `nums[mid] != target` (checked at the start of loop), and `nums[left] == nums[mid]`, we know `nums[left] != target`. We can safely shrink the search space by `left += 1`.

```python
def search_with_duplicates(nums: list[int], target: int) -> bool:
    """
    Search target in rotated sorted array WITH duplicates.

    Time: O(log n) average, O(n) worst case
    Space: O(1)
    """
    if not nums:
        return False

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return True

        # Handle duplicates: shrink window when we can't determine sorted half
        if nums[left] == nums[mid]:
            left += 1

        # Left half is strictly sorted
        elif nums[left] < nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1

        # Right half is strictly sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return False
```
**Important Interview Note:** The worst-case time complexity degrades to **O(N)** (e.g., array is `[1,1,1,1,1]` and target is `2`). Be sure to explicitly state this to your interviewer!

---

## Common Mistakes & Edge Cases

### 1. Wrong Sorted Half Detection
```python
# ❌ WRONG: Fails when left == mid (e.g. 2 elements left)
if nums[left] < nums[mid]:

# ✅ CORRECT: Must use <= to handle window size 2
if nums[left] <= nums[mid]:
```

### 2. Missing Equality in Range Checks
```python
# ❌ WRONG: Misses when target == nums[left] or target == nums[right]
if nums[left] < target < nums[mid]:

# ✅ CORRECT: The boundary of the array must be inclusive
if nums[left] <= target < nums[mid]:
```

### 3. Edge Cases Checklist
Always test your code mentally against:
- [ ] `nums = [1]`, `target = 1` (Single element)
- [ ] `nums = [3, 1]`, `target = 1` (Two elements, rotated)
- [ ] `nums = [1, 2, 3, 4, 5]` (Not rotated at all)
- [ ] Target is not in the array
- [ ] Array contains only duplicates of one number (for LC 81 variant)

---

## Complexity Analysis

| Variant | Time Complexity | Space Complexity |
|---------|-----------------|------------------|
| No Duplicates (1-Pass) | $O(\log N)$ | $O(1)$ |
| No Duplicates (2-Pass Pivot) | $O(\log N)$ | $O(1)$ |
| With Duplicates | $O(\log N)$ avg, $O(N)$ worst | $O(1)$ |

---

## Practice Problems

| Problem | Difficulty | Key Insight |
|---------|------------|-------------|
| [LC 33: Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | Identify sorted half, manage bounds |
| [LC 81: Search in Rotated Sorted Array II](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/) | Medium | Handle duplicates with `left += 1` |
| [LC 153: Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | Medium | Find the pivot |
| [LC 154: Find Minimum in Rotated Array II](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/) | Hard | Find the pivot with duplicates |

---

## Next: [04-find-minimum-rotated.md](./04-find-minimum-rotated.md)

Finding the minimum element (rotation point) in rotated arrays.