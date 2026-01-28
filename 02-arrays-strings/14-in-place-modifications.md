# In-Place Modifications

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

In-place modification techniques transform arrays without extra space by clever reuse of the input array itself. The key patterns—read/write pointers, swap-based partitioning, and index encoding—achieve O(1) space where naive approaches would need O(n).

## Building Intuition

**Why can we modify in-place without losing data?**

The key insight is **overwritten data is no longer needed**:

1. **Read/Write Pointer Model**: The read pointer (fast) scans ahead, finding elements to keep. The write pointer (slow) marks where to place them. Everything between read and write is "garbage"—we've already decided what to keep from that region.

2. **Swap-Based Partitioning**: Instead of copying elements, swap them to their correct region. Dutch National Flag uses three regions (0s, 1s, 2s) managed by three pointers, swapping elements to their destination.

3. **Index Encoding**: When values are bounded (1 to n), the array indices themselves become storage. Mark visited by negating: `arr[abs(num)-1] *= -1`. Recover originals later if needed.

**Mental Model - Move Zeroes**: Imagine a deck of cards where you're pulling out all non-joker cards and stacking them at the front. Once you've processed a card and decided it's a joker, you don't need to look at it again—just keep stacking non-jokers at the write position.

**Why Dutch National Flag Works**:

```
Three regions: [0s | 1s | unknown | 2s]
              0    low  mid      high   n-1

Invariants:
- Elements before low are all 0
- Elements between low and mid are all 1
- Elements after high are all 2
- mid scans through unknown region

On each step:
- arr[mid] == 0: swap with low, both advance
- arr[mid] == 1: just advance mid
- arr[mid] == 2: swap with high, only high retreats
                 (don't advance mid—need to check what came from high!)
```

**Index Encoding Trick**:

```
Array: [4, 3, 2, 7, 8, 2, 3, 1] (values 1-8, indices 0-7)
Task: Find duplicates (O(1) space)

Idea: For each num, mark index (num-1) as visited by negating.
If already negative, we've seen this num before → duplicate!

Trace:
4 → mark index 3: [4, 3, 2, -7, 8, 2, 3, 1]
3 → mark index 2: [4, 3, -2, -7, 8, 2, 3, 1]
2 → mark index 1: [4, -3, -2, -7, 8, 2, 3, 1]
7 → mark index 6: [4, -3, -2, -7, 8, 2, -3, 1]
8 → mark index 7: [4, -3, -2, -7, 8, 2, -3, -1]
2 → index 1 already negative → 2 is duplicate!
3 → index 2 already negative → 3 is duplicate!
1 → mark index 0: [-4, -3, -2, -7, 8, 2, -3, -1]
```

## When NOT to Use In-Place Modifications

In-place isn't always appropriate:

1. **Need Original Array Later**: In-place destroys the original. If you need it for verification, debugging, or subsequent operations, copy first.

2. **Complex Ordering Requirements**: If the output ordering is complex (not just partitioning or filtering), in-place may be error-prone. Consider if extra space simplifies the logic.

3. **Immutable Data Structures**: In some languages/contexts (functional programming, string types), in-place modification isn't possible.

4. **Concurrent Access**: If multiple threads read the array while you modify, you'll have race conditions. Need synchronization or copy-on-write.

5. **When O(n) Space Is Acceptable**: If extra space is cheap and simplifies code significantly, it may be worth it. Correctness > optimization.

**Red Flags:**

- "Return original and modified" → Need copy
- "Stable partition" (preserve relative order) → May need extra space or O(n²) time
- "String modification" in Python → Must convert to list first

---

## Interview Context

In-place modification problems test your ability to:

- Optimize for O(1) space
- Handle tricky edge cases
- Use clever techniques like two-pointers or swapping
- Work with constraints that prevent extra arrays

Common in phone screens where interviewers want to see clean, efficient code.

---

## Why In-Place?

- Space complexity matters in real systems
- Shows understanding of memory constraints
- Often more elegant than brute force
- Interviewers explicitly ask "can you do it in O(1) space?"

---

## Template: Move Zeroes

```python
def move_zeroes(arr: list[int]) -> None:
    """
    Move all zeros to end, maintaining order of non-zeros.

    Time: O(n)
    Space: O(1)

    Example:
    [0, 1, 0, 3, 12] → [1, 3, 12, 0, 0]
    """
    # Position to place next non-zero
    write_idx = 0

    # Move all non-zeros to front
    for read_idx in range(len(arr)):
        if arr[read_idx] != 0:
            arr[write_idx] = arr[read_idx]
            write_idx += 1

    # Fill remaining with zeros
    while write_idx < len(arr):
        arr[write_idx] = 0
        write_idx += 1
```

### Single-Pass with Swap

```python
def move_zeroes_swap(arr: list[int]) -> None:
    """
    Single pass using swaps.
    Fewer writes when there are few zeros.
    """
    write_idx = 0

    for read_idx in range(len(arr)):
        if arr[read_idx] != 0:
            arr[write_idx], arr[read_idx] = arr[read_idx], arr[write_idx]
            write_idx += 1
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
    → [2, 2, _, _], returns 2
    """
    write_idx = 0

    for read_idx in range(len(arr)):
        if arr[read_idx] != val:
            arr[write_idx] = arr[read_idx]
            write_idx += 1

    return write_idx
```

### When Element is Rare

```python
def remove_element_rare(arr: list[int], val: int) -> int:
    """
    Optimized when val is rare - swap with end.
    Fewer operations but doesn't preserve order.
    """
    i = 0
    n = len(arr)

    while i < n:
        if arr[i] == val:
            arr[i] = arr[n - 1]
            n -= 1
        else:
            i += 1

    return n
```

---

## Template: Remove Duplicates from Sorted Array

```python
def remove_duplicates(arr: list[int]) -> int:
    """
    Remove duplicates in-place from sorted array.
    Returns new length.

    Time: O(n)
    Space: O(1)

    Example:
    [1, 1, 2] → [1, 2, _], returns 2
    """
    if not arr:
        return 0

    write_idx = 1

    for read_idx in range(1, len(arr)):
        if arr[read_idx] != arr[write_idx - 1]:
            arr[write_idx] = arr[read_idx]
            write_idx += 1

    return write_idx
```

---

## Template: Sort Colors (Dutch National Flag)

```python
def sort_colors(arr: list[int]) -> None:
    """
    Sort array containing only 0, 1, 2 in-place.
    Single pass.

    Time: O(n)
    Space: O(1)

    Example:
    [2, 0, 2, 1, 1, 0] → [0, 0, 1, 1, 2, 2]
    """
    low = 0          # Next position for 0
    mid = 0          # Current element
    high = len(arr) - 1  # Next position for 2

    while mid <= high:
        if arr[mid] == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else:  # arr[mid] == 2
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
            # Don't increment mid - need to check swapped element
```

### Visual: Dutch National Flag

```
[2, 0, 2, 1, 1, 0]
 L
 M
             H

After processing:
[0, 0, 1, 1, 2, 2]
       L
             M
          H
```

---

## Template: Reverse Array

```python
def reverse(arr: list[int]) -> None:
    """
    Reverse array in-place.

    Time: O(n)
    Space: O(1)
    """
    left, right = 0, len(arr) - 1

    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

---

## Template: Rotate Array

```python
def rotate(arr: list[int], k: int) -> None:
    """
    Rotate array right by k positions in-place.

    Time: O(n)
    Space: O(1)

    Example:
    [1, 2, 3, 4, 5, 6, 7], k = 3
    → [5, 6, 7, 1, 2, 3, 4]
    """
    def reverse(left: int, right: int) -> None:
        while left < right:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1

    n = len(arr)
    k = k % n  # Handle k > n

    # Reverse all, then reverse first k, then reverse rest
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
```

---

## Template: Next Permutation

```python
def next_permutation(arr: list[int]) -> None:
    """
    Rearrange to next lexicographically greater permutation.
    If already greatest, rearrange to smallest (sorted).

    Time: O(n)
    Space: O(1)

    Example:
    [1, 2, 3] → [1, 3, 2]
    [3, 2, 1] → [1, 2, 3]
    [1, 1, 5] → [1, 5, 1]
    """
    n = len(arr)

    # Step 1: Find first decreasing element from right
    i = n - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1

    if i >= 0:
        # Step 2: Find smallest element greater than arr[i] from right
        j = n - 1
        while arr[j] <= arr[i]:
            j -= 1
        # Step 3: Swap
        arr[i], arr[j] = arr[j], arr[i]

    # Step 4: Reverse everything after index i
    left, right = i + 1, n - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

---

## Template: Partition Array

```python
def partition(arr: list[int], pivot: int) -> int:
    """
    Partition array around pivot value.
    Elements < pivot go left, >= go right.
    Returns partition index.

    Time: O(n)
    Space: O(1)
    """
    write_idx = 0

    for read_idx in range(len(arr)):
        if arr[read_idx] < pivot:
            arr[write_idx], arr[read_idx] = arr[read_idx], arr[write_idx]
            write_idx += 1

    return write_idx
```

---

## Template: Rearrange Alternating

```python
def rearrange_alternating(arr: list[int]) -> None:
    """
    Rearrange so arr[0] < arr[1] > arr[2] < arr[3] > ...

    Time: O(n)
    Space: O(1)

    Example:
    [3, 5, 2, 1, 6, 4] → [3, 5, 1, 6, 2, 4] or similar
    """
    for i in range(len(arr) - 1):
        if i % 2 == 0:
            # Even index: should be less than next
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
        else:
            # Odd index: should be greater than next
            if arr[i] < arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
```

---

## Template: Segregate Negatives

```python
def segregate_negatives(arr: list[int]) -> None:
    """
    Move all negatives to front, positives to back.
    Maintains relative order (stable).

    Time: O(n²) - due to shifting elements
    Space: O(1)

    Note: This is the stable but slower approach.
    For O(n) without order preservation, see below.
    """
    write_idx = 0

    for read_idx in range(len(arr)):
        if arr[read_idx] < 0:
            # Shift elements and insert
            val = arr[read_idx]
            for j in range(read_idx, write_idx, -1):
                arr[j] = arr[j - 1]
            arr[write_idx] = val
            write_idx += 1
```

### Without Order Preservation

```python
def segregate_negatives_unordered(arr: list[int]) -> None:
    """
    Move negatives to front (order not preserved).

    Time: O(n)
    Space: O(1)
    """
    left, right = 0, len(arr) - 1

    while left < right:
        while left < right and arr[left] < 0:
            left += 1
        while left < right and arr[right] >= 0:
            right -= 1

        if left < right:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1
```

---

## Common Techniques Summary

| Technique               | Use Case             | Example                     |
| ----------------------- | -------------------- | --------------------------- |
| Two Pointers (same dir) | Remove/filter        | Move Zeroes, Remove Element |
| Two Pointers (opposite) | Reverse, Partition   | Reverse Array, Sort Colors  |
| Three Pointers          | 3-way partition      | Dutch National Flag         |
| Reversal Trick          | Rotate               | Rotate Array                |
| Index Encoding          | Use array as storage | Find Duplicates             |

---

## Index Encoding Technique

When array contains values 1 to n, use indices as extra storage:

```python
def find_duplicates(arr: list[int]) -> list[int]:
    """
    Find all duplicates in array where 1 <= arr[i] <= n.
    Mark visited by negating.

    Time: O(n)
    Space: O(1)
    """
    result = []

    for num in arr:
        idx = abs(num) - 1
        if arr[idx] < 0:
            result.append(abs(num))
        else:
            arr[idx] = -arr[idx]

    return result
```

---

## Edge Cases

```python
# Empty array
[] → nothing to modify

# Single element
[5] → already done for most operations

# All same elements
[1, 1, 1] → remove duplicates → [1]

# Already in desired state
[0, 0, 0] with move zeros → unchanged

# k larger than array length
Rotate by k % n
```

---

## Practice Problems

| #   | Problem                             | Difficulty | Technique                 |
| --- | ----------------------------------- | ---------- | ------------------------- |
| 1   | Move Zeroes                         | Easy       | Two pointers              |
| 2   | Remove Element                      | Easy       | Two pointers              |
| 3   | Remove Duplicates from Sorted Array | Easy       | Two pointers              |
| 4   | Sort Colors                         | Medium     | Dutch flag                |
| 5   | Rotate Array                        | Medium     | Reversal trick            |
| 6   | Next Permutation                    | Medium     | Find pivot, swap, reverse |
| 7   | Find All Duplicates in Array        | Medium     | Index encoding            |
| 8   | Wiggle Sort II                      | Medium     | Virtual indexing          |

---

## Key Takeaways

1. **Two pointers** (read/write) for filtering
2. **Swap** to avoid extra arrays
3. **Reversal trick** for rotation
4. **Index encoding** when values are bounded
5. **Don't increment** after swap from end (might need to recheck)

---

## Next: [15-interval-problems.md](./15-interval-problems.md)

Learn interval manipulation: merge, insert, and scheduling.
