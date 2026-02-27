# Find Minimum in Rotated Sorted Array

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md), [Search Rotated Array](./03-search-rotated-array.md)

## Interview Context

Finding the minimum in a rotated array is a classic problem that tests:

1. **Binary search adaptation**: Modifying the condition for dropping halves.
2. **Boundary conditions**: Knowing when to include/exclude `mid` (`mid` vs `mid + 1`).
3. **Array properties**: Leveraging the invariant that at least one half of a rotated sorted array is always strictly sorted.
4. **Problem decomposition**: This is often step 1 in solving the larger "Search in Rotated Sorted Array" problem.

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

- **Before the break**: Values are strictly increasing, and all values are $\ge$ the first element.
- **After the break**: Values are strictly increasing, and all values are $\le$ the last element.

**The Key Insight: Compare `mid` with `right`**

When trying to find the minimum, comparing `nums[mid]` with `nums[left]` can be ambiguous. The bulletproof strategy is to compare `nums[mid]` with `nums[right]`.

Why? Because the rightmost element gives us a stable point of reference.

```text
Case 1: nums[mid] > nums[right]
[3, 4, 5, 1, 2]
 L     M     R

- Since 5 > 2, the array MUST break somewhere to the right of mid.
- The minimum cannot be at mid (because mid is larger than right).
- Action: search the right half strictly -> left = mid + 1

Case 2: nums[mid] <= nums[right]
[4, 5, 1, 2, 3]
       L  M  R

- Since 2 <= 3, the right half (from mid to right) is strictly sorted.
- The minimum MUST be at mid or to the left of mid.
- Action: search the left half, including mid -> right = mid
```

**Mental Model: The Cliff**

Imagine walking along the array values like elevation. A rotated sorted array looks like a cliff:

```text
        6  7
      5
    4
  3                      The values "fall off a cliff"
                        and start low again.
                1  2  3
```

You are searching for the bottom of the cliff. 
- If you're standing high (`nums[mid] > nums[right]`), the cliff is ahead of you. Move right.
- If you're standing low (`nums[mid] <= nums[right]`), the cliff is behind you (or you are exactly at the bottom). Move left, but don't step forward off your current spot (`right = mid`).

---

## Pattern 1: Find Minimum (No Duplicates)

LeetCode 153: Find Minimum in Rotated Sorted Array

**The Algorithm:**
1. Initialize `left = 0`, `right = len(nums) - 1`.
2. Loop while `left < right`.
3. Calculate `mid = left + (right - left) // 2`.
4. If `nums[mid] > nums[right]`, the minimum is in the right half -> `left = mid + 1`.
5. Else, the minimum is in the left half (including `mid`) -> `right = mid`.
6. When the loop ends (`left == right`), `nums[left]` is the minimum.

```python
def findMin(nums: list[int]) -> int:
    """
    Find minimum in rotated sorted array (no duplicates).
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    
    # Optional optimization: If the array is fully sorted (not rotated or 0 rotations),
    # the first element is the minimum.
    if nums[left] < nums[right]:
        return nums[left]

    # Use left < right to find the EXACT index of the minimum.
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] > nums[right]:
            # Minimum must be to the right of mid
            left = mid + 1
        else:
            # Minimum is at mid or to the left of mid
            right = mid
            
    # Loop terminates when left == right
    return nums[left]
```

### Why `left < right` instead of `left <= right`?

We're not looking for a specific *target* value that we can return immediately from inside the loop. We are narrowing down a *range* to find a *position*. 

When `left == right`, the search space has shrunk to a single element. That element *must* be the minimum. If we used `left <= right`, we would risk an infinite loop or an out-of-bounds error when trying to update `left` or `right` without finding a target.

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

**The Solution:** If `nums[mid] == nums[right]`, we know that the element at `right` has a duplicate at `mid`. Therefore, we can safely discard `nums[right]` without losing the minimum element. We simply decrement `right` by 1.

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
        
        if nums[mid] > nums[right]:
            # Minimum is definitely to the right
            left = mid + 1
        elif nums[mid] < nums[right]:
            # Minimum is at mid or to the left
            right = mid
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

If you need the maximum element in a rotated sorted array, the easiest approach is to find the minimum first.

- The maximum element is always exactly *before* the minimum element.
- Since the array wraps around, if the minimum is at index `i`, the maximum is at `(i - 1) % n`.

```python
def findMax(nums: list[int]) -> int:
    # 1. Edge case: fully sorted array
    if nums[0] < nums[-1]:
        return nums[-1]
        
    # 2. Find index of minimum
    left, right = 0, len(nums) - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
            
    # left is the index of the minimum.
    # The maximum is just before it. We handle wrap-around using modulo
    # (though in Python nums[-1] natively handles the index 0 case).
    return nums[left - 1] 
```

### 2. Finding Rotation Count

How many times was a sorted array rotated to produce the given array?

**Insight:** The index of the minimum element *is* the rotation count.
For example, `[4, 5, 1, 2, 3]` was rotated `2` times. The minimum (`1`) is at index `2`.

```python
def findRotationCount(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
            
    return left # Returns the index of the minimum
```

---

## Common Pitfalls & Edge Cases

1. **Comparing `mid` with `left` instead of `right`:**
   Comparing with `left` breaks when the sub-array is fully sorted. Always compare `nums[mid]` to `nums[right]`.

2. **Using `right = mid - 1` when `nums[mid] <= nums[right]`:**
   If `nums[mid]` is the minimum, `mid - 1` will skip over it. Since `mid` *could* be the minimum, you must use `right = mid`.

3. **Using `while left <= right:`:**
   This will cause an infinite loop because when `left == right`, `mid == left == right`, and the `else` block triggers `right = mid`, changing nothing. Use `while left < right:` to narrow down to a single element.

4. **Handling purely sorted arrays:**
   If an array like `[1, 2, 3, 4, 5]` is passed, `nums[mid] <= nums[right]` will be true, shrinking `right`. It will correctly find the `1`, but doing a quick `if nums[left] < nums[right]: return nums[left]` upfront avoids the binary search entirely for an $O(1)$ best case.

---

## Summary Checklist

| Condition / Step | Why? |
| :--- | :--- |
| **`while left < right`** | We are narrowing a range to find a position. Loop terminates when `left == right`, pointing precisely at the min. |
| **Compare `mid` to `right`** | Right bound acts as a stable reference to detect the "cliff". |
| **`nums[mid] > nums[right]`** | The array wraps around in the right half. The minimum is to the right. `left = mid + 1` |
| **`nums[mid] < nums[right]`** | The right half is strictly increasing. The minimum is at `mid` or left. `right = mid` |
| **`nums[mid] == nums[right]`** | (Duplicates only) Cannot determine which half. Safely discard `right`. `right -= 1` |
