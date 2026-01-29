# Find Minimum in Rotated Sorted Array

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md), [Search Rotated Array](./03-search-rotated-array.md)

## Interview Context

Finding the minimum in a rotated array tests:

1. **Binary search adaptation**: Different comparison logic
2. **Edge case handling**: Non-rotated arrays, duplicates
3. **Boundary conditions**: When to include/exclude mid
4. **Problem decomposition**: Often a subproblem for other questions

---

## Building Intuition

**Where Is the Minimum?**

The minimum is exactly at the "break point" where the rotation happened:

```
Original: [1, 2, 3, 4, 5, 6, 7]
Rotated:  [4, 5, 6, 7, 1, 2, 3]
                    ↑
            HERE - the minimum is where order breaks
```

Before the break: values are increasing
After the break: values continue increasing (but all smaller than before)

**The Key Insight: Compare with Right, Not Left**

Why compare `nums[mid]` with `nums[right]` instead of `nums[left]`?

```
[3, 4, 5, 1, 2]
 L     M     R

Comparing with LEFT (nums[left] = 3):
- nums[mid] = 5 > nums[left] = 3
- This tells us mid is in the "larger" part, so minimum is to the right... CORRECT!

[4, 5, 1, 2, 3]
 L     M     R

Comparing with LEFT (nums[left] = 4):
- nums[mid] = 1 < nums[left] = 4
- Minimum is on the left? But mid IS the minimum!
- We'd set right = mid - 1 and MISS IT!

Comparing with RIGHT (nums[right] = 3):
- nums[mid] = 1 < nums[right] = 3
- Minimum is at mid or to its left
- We set right = mid (keeping mid in range) ✓
```

**Mental Model: The Cliff**

Imagine walking along the array values like elevation. A rotated sorted array looks like:

```
        6  7
      5
    4
  3                      The values "fall off a cliff"
                        and start low again
                1  2  3
```

You're looking for the bottom of the cliff. When you're BEFORE the cliff (on the high side), you see `nums[mid] > nums[right]`. When you're AT or AFTER the cliff (on the low side), you see `nums[mid] <= nums[right]`.

**Why `left < right` Instead of `left <= right`?**

We're not looking for an exact target—we're looking for a POSITION (the minimum's index). When `left == right`, they've converged on that position. No need to check further.

---

## When NOT to Use This Approach

**1. Non-Rotated Array (Or Don't Know If Rotated)**

- If `nums[0] <= nums[n-1]`, the array is sorted → minimum is `nums[0]`
- Check this first to avoid unnecessary work

**2. Array Has Many Duplicates**

- When `nums[mid] == nums[right]`, you can't determine which half has the minimum
- Worst case becomes O(n)
- Use the duplicate-handling variant

**3. You Actually Need the Target, Not Minimum**

- Finding minimum is a SUBPROBLEM for "search in rotated array"
- But if you just need to find a target, use the direct approach from file 03

**4. Array Is Very Small (n <= 3)**

- Linear scan is simpler and just as fast
- Constant factor overhead of binary search not worth it

**Red Flags:**

- "Array contains duplicates" → Use O(n) fallback
- "Find target in rotated array" → Don't find minimum first (use direct search)
- "Array might not be rotated" → Check `nums[0] <= nums[n-1]` first

---

## The Problem

Find the minimum element in a rotated sorted array:

```
Original: [1, 2, 3, 4, 5]
Rotated:  [3, 4, 5, 1, 2]  → minimum = 1

Rotated:  [1, 2, 3, 4, 5]  → minimum = 1 (no rotation)
```

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

| Variant             | Time            | Space |
| ------------------- | --------------- | ----- |
| No duplicates       | O(log n)        | O(1)  |
| With duplicates     | O(n) worst case | O(1)  |
| Find rotation count | O(log n)        | O(1)  |

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

| #   | Problem                                 | Difficulty | Key Insight              |
| --- | --------------------------------------- | ---------- | ------------------------ |
| 1   | Find Minimum in Rotated Sorted Array    | Medium     | Compare with right       |
| 2   | Find Minimum in Rotated Sorted Array II | Hard       | Handle duplicates        |
| 3   | Search in Rotated Sorted Array          | Medium     | Use minimum to partition |
| 4   | Rotation Count                          | Medium     | Index of minimum         |
| 5   | Check if Array is Sorted and Rotated    | Easy       | Count break points       |

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
