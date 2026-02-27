# Find Minimum in Rotated Sorted Array

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md), [Search Rotated Array](./03-search-rotated-array.md)

## Interview Context

Finding the minimum in a rotated array is a classic problem that tests:

1. **Binary search adaptation**: Modifying the condition for dropping halves based on the array's rotation property.
2. **Boundary conditions**: Knowing when to include/exclude `mid` (`right = mid` vs `left = mid + 1`).
3. **Template mastery**: Recognizing that this is fundamentally a "Find Left Boundary" problem (Template 2).

---

## Building Intuition

**Where Is the Minimum?**

A rotated sorted array is essentially two sorted subarrays placed back-to-back. The minimum element is exactly at the "break point" or "inflection point" where the rotation happened:

```text
Original: [1, 2, 3, 4, 5, 6, 7]
Rotated:  [4, 5, 6, 7, 1, 2, 3]
                    ↑
            HERE - the minimum is where the order breaks
```

### The Key Insight: Compare `nums[mid]` with `nums[right]`

When trying to find the minimum, comparing `nums[mid]` with `nums[left]` can be ambiguous. The bulletproof strategy is to always compare `nums[mid]` with `nums[right]`.

Why? Because the rightmost element gives us a stable point of reference. In a valid rotated sorted array, the minimum element MUST be less than or equal to the rightmost element. 

### The Monotonic Property (Connecting to Template 2)

Recall from the [Binary Search Template](./01-binary-search-template.md) that binary search requires a condition that evaluates to `[False, False, ..., True, True]`.

If we check if elements belong to the "right-side sorted portion" by evaluating `nums[i] <= nums[right]`, we get exactly this property!

```text
Array:     [4,  5,  6,  7,  1,  2,  3]
Target:    Compare with nums[right] which is 3
Condition: nums[i] <= 3

Eval:      [F,  F,  F,  F,  T,  T,  T]
                                ↑
                We want the FIRST True!
```

Since we are looking for the **first occurrence** where `nums[i] <= nums[right]`, this is a textbook application of **Template 2 (Find Left Boundary)**. 

---

## Pattern 1: Find Minimum (No Duplicates)

LeetCode 153: Find Minimum in Rotated Sorted Array

**The Algorithm:**
1. Initialize `left = 0`, `right = len(nums) - 1`.
2. Loop while `left < right`.
3. Calculate `mid`.
4. If `nums[mid] <= nums[right]`, `mid` is in the right-side portion. The minimum is at `mid` or to its left $\rightarrow$ `right = mid`.
5. Else, `mid` is in the left-side portion. The minimum is strictly to the right $\rightarrow$ `left = mid + 1`.

```python
def findMin(nums: list[int]) -> int:
    """
    Find minimum in rotated sorted array (no duplicates).

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    left, right = 0, len(nums) - 1

    # Optional optimization: If the array is fully sorted
    # the first element is the minimum.
    if nums[left] <= nums[right]:
        return nums[left]

    # Template 2: Find Left Boundary
    while left < right:
        mid = left + (right - left) // 2

        # Does mid belong to the right-side sorted portion?
        if nums[mid] <= nums[right]:
            # It does. The minimum (boundary) could be mid or to the left.
            right = mid
        else:
            # It doesn't. The minimum must be to the right.
            left = mid + 1

    # Loop terminates when left == right
    return nums[left]
```

### Why `left < right` instead of `left <= right`?

We're not looking for a specific *target* value that we can return immediately from inside the loop. We are narrowing down a *range* to find a *boundary position*. 

This perfectly matches **Template 2**. When `left == right`, the search space has shrunk to a single element, which *must* be the answer. If we used `left <= right`, we would risk an infinite loop or out-of-bounds error when updating boundaries without a `return mid` statement.

---

## Pattern 2: Find Minimum (With Duplicates)

LeetCode 154: Find Minimum in Rotated Sorted Array II

When duplicates are introduced, comparing `nums[mid]` with `nums[right]` can lead to a third case: `nums[mid] == nums[right]`.

```text
[1, 0, 1, 1, 1]
 L     M     R
nums[M] == nums[R] -> Minimum is on the left (index 1)

[1, 1, 1, 0, 1]
 L     M     R
nums[M] == nums[R] -> Minimum is on the right (index 3)
```

**The Problem:** We cannot determine which half contains the minimum.

**The Solution:** If `nums[mid] == nums[right]`, we know that the element at `right` has a duplicate at `mid`. Because we still have `mid` in our search space, we can safely discard `nums[right]` without losing the minimum element. We simply decrement `right` by 1.

```python
def findMinDuplicates(nums: list[int]) -> int:
    """
    Find minimum in rotated sorted array (with duplicates).

    Time Complexity: O(log n) average, O(n) worst case
    Space Complexity: O(1)
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] < nums[right]:
            # mid is in the right-side sorted portion
            right = mid
        elif nums[mid] > nums[right]:
            # mid is in the left-side sorted portion
            left = mid + 1
        else:
            # nums[mid] == nums[right]
            # We can't be sure which half holds the minimum, but we can
            # safely eliminate nums[right] because nums[mid] is identical.
            right -= 1

    return nums[left]
```

**Why is Worst Case O(n)?**
If the array is filled with identical elements (e.g., `[1, 1, 1, 1, 1]`), `nums[mid] == nums[right]` will trigger every time, causing `right` to decrement by 1 in each step. This devolves the binary search into a linear scan.

---

## Extensions & Related Concepts

### 1. Finding the Maximum

There are two great ways to find the maximum element in a rotated sorted array.

**Approach 1: Using the Minimum (The Clever Way)**

The maximum element is always exactly *before* the minimum element. Once you find the index of the minimum, `(index - 1) % n` gives you the maximum. Python's negative indexing handles this natively.

```python
def findMax(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1

    if nums[left] <= nums[right]:
        return nums[right]

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] <= nums[right]:
            right = mid
        else:
            left = mid + 1

    # left is the index of the minimum. The max is just before it.
    return nums[left - 1]
```

**Approach 2: Template 3 (The Rigorous Way)**

We can also find the maximum directly by finding the LAST element before the drop-off. If we compare elements to `nums[0]`, we get a `[True, True, ..., False, False]` pattern!

```text
Array:     [4,  5,  6,  7,  1,  2,  3]
Condition: nums[i] >= 4 (nums[0])

Eval:      [T,  T,  T,  T,  F,  F,  F]
                        ↑
            We want the LAST True!
```

This perfectly matches **Template 3 (Find Right Boundary)**:

```python
def findMaxDirect(nums: list[int]) -> int:
    """Find max directly using Template 3 (Right Boundary)"""
    left, right = 0, len(nums) - 1
    
    # Edge case: fully sorted array
    if nums[left] <= nums[right]:
        return nums[right]
        
    while left < right:
        # CRITICAL: Template 3 requires rounding up for mid!
        mid = left + (right - left + 1) // 2
        
        # Does mid belong to the left-side sorted portion?
        if nums[mid] >= nums[0]:
            left = mid      # It does. Answer could be mid or to the right.
        else:
            right = mid - 1 # It doesn't. Answer must be to the left.
            
    return nums[left]
```

### 2. Finding Rotation Count

How many times was a strictly sorted array rotated to produce the given array?

**Insight:** The index of the minimum element *is* the rotation count.
For example, `[4, 5, 1, 2, 3]` was rotated `2` times. The minimum (`1`) is at index `2`.

```python
def findRotationCount(nums: list[int]) -> int:
    """
    Find how many times a strictly sorted array was rotated to the right.
    Equivalent to finding the index of the minimum element.
    """
    left, right = 0, len(nums) - 1

    if nums[left] <= nums[right]:
        return 0

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] <= nums[right]:
            right = mid
        else:
            left = mid + 1

    return left # Returns the index of the minimum, which equals rotation count
```

---

## Common Pitfalls & Edge Cases

1. **Comparing `mid` with `left` instead of `right`:**
   Comparing with `left` breaks when the sub-array is fully sorted. In `[1, 2, 3, 4, 5]`, `nums[mid] > nums[left]` is true, which might incorrectly imply the minimum is to the right. Always compare `nums[mid]` to `nums[right]` for a stable reference point.

2. **Using `right = mid - 1` when `nums[mid] <= nums[right]`:**
   If `nums[mid]` happens to be the minimum, doing `right = mid - 1` will skip right past it. Since `mid` evaluates to `True` for our boundary condition, you must keep it in the search space using `right = mid`.

3. **Using `while left <= right:` for boundary finding:**
   This will cause an infinite loop because when `left == right`, `mid == left == right`, and the `if` block triggers `right = mid`, changing nothing. Since you are narrowing a range rather than searching for a specific target, always use `while left < right:` to narrow down to a single element.

4. **Handling purely sorted arrays:**
   If an array like `[1, 2, 3, 4, 5]` is passed, doing a quick `if nums[left] <= nums[right]: return nums[left]` upfront avoids the binary search entirely for an $O(1)$ best case.

---

## Summary Checklist

| Condition / Step | Why? |
| :--- | :--- |
| **`while left < right`** | We are finding a boundary position (Template 2). Loop terminates when `left == right`, pointing precisely at the min. |
| **Compare `mid` to `right`** | Right bound acts as a stable reference to evaluate the monotonic condition `nums[i] <= nums[right]`. |
| **`nums[mid] <= nums[right]`** | `mid` is in the right-side portion. The minimum is at `mid` or left. `right = mid` |
| **`nums[mid] > nums[right]`** | `mid` is in the left-side portion. The minimum is to the right. `left = mid + 1` |
| **`nums[mid] == nums[right]`** | (Duplicates only) Cannot determine which half. Safely discard `right` since `mid` has same value. `right -= 1` |
