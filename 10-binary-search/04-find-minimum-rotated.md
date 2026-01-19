# Find Minimum in Rotated Sorted Array

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md), [Search Rotated Array](./03-search-rotated-array.md)

## Interview Context

Finding the minimum in a rotated array tests:
1. **Binary search adaptation**: Different comparison logic
2. **Edge case handling**: Non-rotated arrays, duplicates
3. **Boundary conditions**: When to include/exclude mid
4. **Problem decomposition**: Often a subproblem for other questions

---

## The Problem

Find the minimum element in a rotated sorted array:

```
Original: [1, 2, 3, 4, 5]
Rotated:  [3, 4, 5, 1, 2]  → minimum = 1

Rotated:  [1, 2, 3, 4, 5]  → minimum = 1 (no rotation)
```

---

## The Core Insight

The minimum is at the **rotation point** where the order breaks:

```
[3, 4, 5, 1, 2]
       ↓
    5 > 1  (order breaks here)
```

Compare `nums[mid]` with `nums[right]`:
- If `nums[mid] > nums[right]`: minimum is in right half
- If `nums[mid] < nums[right]`: minimum is in left half (including mid)
- If `nums[mid] == nums[right]`: can't determine (duplicates)

---

## Find Minimum (No Duplicates)

LeetCode 153: Find Minimum in Rotated Sorted Array

```python
def find_min(nums: list[int]) -> int:
    """
    Find minimum in rotated sorted array (no duplicates).

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            # Minimum is in right half (not including mid)
            left = mid + 1
        else:
            # Minimum is in left half (including mid)
            right = mid

    return nums[left]
```

### Why Compare with Right?

Comparing with `nums[left]` doesn't work:

```
[3, 4, 5, 1, 2]
 L     M     R

nums[mid]=5 > nums[left]=3  → But minimum is to the right!
nums[mid]=5 > nums[right]=2 → Correctly identifies right half
```

---

## Visual Walkthrough

Finding minimum in [4, 5, 6, 7, 0, 1, 2]:

```
Step 1: [4, 5, 6, 7, 0, 1, 2]
         L        M        R

         nums[M]=7 > nums[R]=2
         Minimum in right half
         L = mid + 1 = 4

Step 2: [4, 5, 6, 7, 0, 1, 2]
                     L  M  R

         nums[M]=1 < nums[R]=2
         Minimum in left half (including mid)
         R = mid = 5

Step 3: [4, 5, 6, 7, 0, 1, 2]
                     L  R
                     M

         nums[M]=0 < nums[R]=1
         R = mid = 4

Step 4: [4, 5, 6, 7, 0, 1, 2]
                     LR

         L == R, loop ends
         Return nums[4] = 0
```

---

## Find Minimum (With Duplicates)

LeetCode 154: Find Minimum in Rotated Sorted Array II

Duplicates break the comparison:

```
[2, 2, 2, 0, 1]
 L     M     R

nums[M]=2 == nums[R]=1? No, still works

[1, 1, 1, 1, 1]
 L     M     R

nums[M]=1 == nums[R]=1
Can't determine which half!
```

Solution: When `nums[mid] == nums[right]`, shrink right by 1.

```python
def find_min_duplicates(nums: list[int]) -> int:
    """
    Find minimum in rotated sorted array (with duplicates).

    Time: O(n) worst case, O(log n) average
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            # Minimum in right half
            left = mid + 1
        elif nums[mid] < nums[right]:
            # Minimum in left half (including mid)
            right = mid
        else:
            # nums[mid] == nums[right], can't determine
            # Safely shrink right (if nums[right] is min, mid has same value)
            right -= 1

    return nums[left]
```

**Why shrink right, not left?**
- If `nums[right]` is the minimum, `nums[mid]` has the same value
- We don't lose the minimum by removing `nums[right]`
- Shrinking left could skip the minimum

---

## Alternative: Find Rotation Count

The index of the minimum is the rotation count:

```python
def find_rotation_count(nums: list[int]) -> int:
    """
    Find how many times the array was rotated.

    Returns the index of the minimum element.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    # Array not rotated
    if nums[left] <= nums[right]:
        return 0

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return left
```

---

## Find Maximum in Rotated Array

The maximum is just before the minimum:

```python
def find_max(nums: list[int]) -> int:
    """
    Find maximum in rotated sorted array.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    # Not rotated: max is at the end
    if nums[left] <= nums[right]:
        return nums[right]

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    # left is at minimum, max is just before it
    return nums[left - 1]
```

---

## Check If Array Is Rotated and Sorted

```python
def check_rotated_sorted(nums: list[int]) -> bool:
    """
    Check if array is sorted and rotated.

    The array is valid if there's at most one "break point"
    where nums[i] > nums[i+1], and it wraps around correctly.

    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    count = 0

    for i in range(n):
        if nums[i] > nums[(i + 1) % n]:
            count += 1
            if count > 1:
                return False

    return True
```

---

## Complexity Analysis

| Variant | Time | Space |
|---------|------|-------|
| No duplicates | O(log n) | O(1) |
| With duplicates | O(n) worst case | O(1) |
| Find rotation count | O(log n) | O(1) |

---

## Common Mistakes

### 1. Wrong Loop Condition

```python
# Wrong: misses when left == right
while left <= right:  # Should be left < right

# Correct
while left < right:
```

### 2. Wrong Comparison Target

```python
# Wrong: comparing with left
if nums[mid] > nums[left]:  # Doesn't work reliably

# Correct: compare with right
if nums[mid] > nums[right]:
```

### 3. Including Mid When Shouldn't

```python
# Wrong: including mid when minimum is definitely not there
if nums[mid] > nums[right]:
    left = mid  # Should be mid + 1

# Correct
if nums[mid] > nums[right]:
    left = mid + 1  # mid is definitely not minimum
```

---

## Edge Cases Checklist

- [ ] Single element → return that element
- [ ] Two elements → compare and return smaller
- [ ] Not rotated (sorted) → return first element
- [ ] Rotated once → minimum at the end
- [ ] Rotated n-1 times → minimum at index 1
- [ ] All duplicates → any element (all are minimum)

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Find Minimum in Rotated Sorted Array | Medium | Compare with right |
| 2 | Find Minimum in Rotated Sorted Array II | Hard | Handle duplicates |
| 3 | Search in Rotated Sorted Array | Medium | Use minimum to partition |
| 4 | Rotation Count | Medium | Index of minimum |
| 5 | Check if Array is Sorted and Rotated | Easy | Count break points |

---

## Interview Tips

1. **Clarify duplicates**: Changes complexity significantly
2. **Consider non-rotated case**: Array might be fully sorted
3. **Explain the comparison**: Why right, not left
4. **Handle shrinking correctly**: When to use `mid` vs `mid+1`
5. **Mention worst case**: O(n) with all duplicates

---

## Key Takeaways

1. **Compare with right**: More reliable than comparing with left
2. **Loop until left == right**: Converges to minimum
3. **Duplicates are tricky**: May need to shrink bounds one at a time
4. **Rotation count = min index**: Useful for other problems
5. **Handle non-rotated arrays**: Check `nums[left] <= nums[right]` first

---

## Next: [05-peak-element.md](./05-peak-element.md)

Finding peak elements using binary search.
