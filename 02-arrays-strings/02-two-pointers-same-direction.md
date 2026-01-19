# Two Pointers: Same Direction

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Interview Context

The same-direction two-pointer technique (also called "fast and slow pointers" or "reader-writer pattern") is fundamental for:

- Removing duplicates in-place
- Partitioning arrays
- Cycle detection (in linked lists)
- Processing arrays with O(1) space requirement

This pattern appears in 15-20% of array problems at FANG+ companies.

---

## Core Concept

Use two pointers moving in the same direction at different speeds or with different roles:

```
Typical setup:
- slow: marks the "write" position (or keeps track of valid portion)
- fast: scans ahead (reads/explores the array)

┌───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 1 │ 2 │ 2 │ 2 │ 3 │ 4 │
└───┴───┴───┴───┴───┴───┴───┘
  ↑               ↑
 slow           fast
```

The key insight: **slow only advances when we find valid elements to keep**.

---

## Template: Remove Duplicates Pattern

```python
def remove_duplicates(arr: list[int]) -> int:
    """
    Remove duplicates in-place from sorted array.
    Returns new length.

    Time: O(n) - single pass
    Space: O(1) - in-place

    Example:
    [1, 1, 2, 2, 2, 3, 4]
    → [1, 2, 3, 4, _, _, _] returns 4
    """
    if not arr:
        return 0

    slow = 0  # Points to last unique element

    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]

    return slow + 1  # Length of unique portion
```

### Visual Trace

```
Initial: [1, 1, 2, 2, 2, 3, 4]
         s  f

Step 1: arr[1] == arr[0] → skip
        [1, 1, 2, 2, 2, 3, 4]
         s     f

Step 2: arr[2] != arr[0] → slow++, copy
        [1, 2, 2, 2, 2, 3, 4]
            s  f

Step 3-4: skip duplicates
        [1, 2, 2, 2, 2, 3, 4]
            s        f

Step 5: arr[5] != arr[1] → slow++, copy
        [1, 2, 3, 2, 2, 3, 4]
               s        f

Step 6: arr[6] != arr[2] → slow++, copy
        [1, 2, 3, 4, 2, 3, 4]
                  s        f

Final: return slow + 1 = 4
```

---

## Template: Partition Pattern

```python
def move_zeroes(arr: list[int]) -> None:
    """
    Move all zeros to end, maintaining order of non-zeros.
    In-place modification.

    Time: O(n)
    Space: O(1)

    Example:
    [0, 1, 0, 3, 12] → [1, 3, 12, 0, 0]
    """
    slow = 0  # Next position for non-zero

    # Move all non-zeros to front
    for fast in range(len(arr)):
        if arr[fast] != 0:
            arr[slow] = arr[fast]
            slow += 1

    # Fill rest with zeros
    while slow < len(arr):
        arr[slow] = 0
        slow += 1
```

### Alternative: Swap Version

```python
def move_zeroes_swap(arr: list[int]) -> None:
    """
    Same result, but uses swapping.
    Fewer writes when there are few zeros.

    Time: O(n)
    Space: O(1)
    """
    slow = 0

    for fast in range(len(arr)):
        if arr[fast] != 0:
            arr[slow], arr[fast] = arr[fast], arr[slow]
            slow += 1
```

---

## Template: Remove Element

```python
def remove_element(arr: list[int], val: int) -> int:
    """
    Remove all occurrences of val in-place.
    Returns new length.

    Time: O(n)
    Space: O(1)

    Example:
    arr = [3, 2, 2, 3], val = 3
    → [2, 2, _, _] returns 2
    """
    slow = 0

    for fast in range(len(arr)):
        if arr[fast] != val:
            arr[slow] = arr[fast]
            slow += 1

    return slow
```

---

## Template: Allow K Duplicates

```python
def remove_duplicates_k(arr: list[int], k: int = 2) -> int:
    """
    Remove duplicates so each element appears at most k times.

    Time: O(n)
    Space: O(1)

    Example with k=2:
    [1, 1, 1, 2, 2, 3] → [1, 1, 2, 2, 3, _] returns 5
    """
    if len(arr) <= k:
        return len(arr)

    slow = k  # First k elements always valid

    for fast in range(k, len(arr)):
        # Compare with element k positions back
        if arr[fast] != arr[slow - k]:
            arr[slow] = arr[fast]
            slow += 1

    return slow
```

### Why Compare with `arr[slow - k]`?

```
For k = 2:
[1, 1, 1, 2, 2, 3]
       s  f

arr[slow - 2] = arr[0] = 1
arr[fast] = 1

They're equal! This would be the 3rd '1', so skip it.

Next iteration:
[1, 1, 1, 2, 2, 3]
       s     f

arr[slow - 2] = arr[0] = 1
arr[fast] = 2

Different! Copy and advance slow.
```

---

## Template: Squaring Sorted Array

```python
def sorted_squares(arr: list[int]) -> list[int]:
    """
    Given sorted array (may have negatives), return sorted squares.

    Time: O(n)
    Space: O(n) for result

    Example:
    [-4, -1, 0, 3, 10] → [0, 1, 9, 16, 100]
    """
    n = len(arr)
    result = [0] * n

    left = 0
    right = n - 1
    pos = n - 1  # Fill result from end (largest first)

    while left <= right:
        left_sq = arr[left] ** 2
        right_sq = arr[right] ** 2

        if left_sq > right_sq:
            result[pos] = left_sq
            left += 1
        else:
            result[pos] = right_sq
            right -= 1
        pos -= 1

    return result
```

---

## Common Variations

### Slow Catches Up to Fast

```python
def find_length_of_lcis(arr: list[int]) -> int:
    """
    Longest continuous increasing subsequence.

    Time: O(n)
    Space: O(1)
    """
    if not arr:
        return 0

    max_len = 1
    slow = 0

    for fast in range(1, len(arr)):
        if arr[fast] <= arr[fast - 1]:
            slow = fast  # Reset slow to current position

        max_len = max(max_len, fast - slow + 1)

    return max_len
```

### Gap Pointer

```python
def compare_with_gap(arr: list[int], gap: int) -> bool:
    """
    Check if any element equals another element 'gap' positions away.

    Time: O(n)
    Space: O(1)
    """
    for i in range(len(arr) - gap):
        if arr[i] == arr[i + gap]:
            return True
    return False
```

---

## Edge Cases

```python
# Empty array
[] → return 0 or []

# Single element
[1] → no duplicates possible, return 1

# All same elements
[5, 5, 5, 5, 5] → [5] or [5, 5] depending on k

# No duplicates
[1, 2, 3, 4, 5] → unchanged

# All elements to remove
[3, 3, 3], val=3 → [] return 0
```

---

## Visual: Same vs Opposite Direction

```
Same Direction (this section):
┌───┬───┬───┬───┬───┐
│   │   │   │   │   │
└───┴───┴───┴───┴───┘
 s→      f→

Use when: processing stream, removing elements, partitioning

Opposite Direction (next section):
┌───┬───┬───┬───┬───┐
│   │   │   │   │   │
└───┴───┴───┴───┴───┘
 ←l           r→

Use when: sorted array pair finding, palindromes, reversing
```

---

## Practice Problems

| # | Problem | Difficulty | Pattern |
|---|---------|------------|---------|
| 1 | Remove Duplicates from Sorted Array | Easy | Basic slow/fast |
| 2 | Remove Duplicates from Sorted Array II | Medium | Allow k duplicates |
| 3 | Move Zeroes | Easy | Partition |
| 4 | Remove Element | Easy | Filter in-place |
| 5 | Sort Colors (Dutch Flag) | Medium | Three-way partition |
| 6 | Squares of a Sorted Array | Easy | Fill from ends |
| 7 | Linked List Cycle | Easy | Fast/slow pointers |

---

## Key Takeaways

1. **Slow = write position, fast = read position**
2. **Slow only advances when finding valid elements**
3. **Works for sorted arrays** (duplicates) and unsorted (partitioning)
4. **O(1) space** by modifying in-place
5. **Compare carefully**: with previous element? with slow? with gap?

---

## Next: [03-two-pointers-opposite.md](./03-two-pointers-opposite.md)

Learn converging pointers for pair-finding and optimization problems.
