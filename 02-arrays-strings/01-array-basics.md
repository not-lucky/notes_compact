# Array Basics

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

## Overview

An array is a contiguous block of memory that stores elements of the same type, accessible by index in O(1) time. It's the most fundamental data structure in computer science, serving as the building block for almost every other data structure.

## Building Intuition

**Why are arrays so powerful?**

Think of an array as a row of numbered mailboxes in an apartment building. Each mailbox has an address (index), and you can go directly to any mailbox without checking the others. This is the O(1) random access superpower that makes arrays unique.

**The Memory Model**:
1. **Contiguous Allocation**: Arrays occupy consecutive memory locations. If element 0 is at address 1000 and each element takes 4 bytes, element 5 is at address 1000 + (5 × 4) = 1020. The CPU calculates this in one step—no searching required.

2. **Cache Friendliness**: Because elements are adjacent in memory, accessing one element often pre-loads nearby elements into the CPU cache. This makes sequential array traversal extremely fast—often 10-100x faster than pointer-chasing through scattered memory (like linked lists).

3. **The Trade-off**: This contiguous layout means insertion/deletion in the middle is expensive (O(n))—you must shift elements to maintain the sequence. Arrays excel at random access and sequential processing, not frequent modifications.

**Mental Model**: Think of arrays as "printed books" vs linked lists as "choose-your-own-adventure books with page jumps." In a printed book, you can flip directly to page 100 (O(1)), but inserting a new page 50 requires reprinting everything after it (O(n)).

## When NOT to Use Arrays

Arrays aren't always the best choice. Consider alternatives when:

1. **Frequent Insertions/Deletions in Middle**: If you're constantly adding or removing elements at arbitrary positions, linked lists or balanced trees (O(log n) insert) may be better. Arrays require O(n) shifts.

2. **Unknown or Highly Variable Size**: If the size changes dramatically and unpredictably, dynamic arrays (Python lists) handle this, but with occasional O(n) resize costs. If inserts dominate, consider other structures.

3. **Need Fast Membership Testing**: "Is X in the array?" is O(n) for arrays. Use a hash set (O(1)) or sorted array with binary search (O(log n)) instead.

4. **Sparse Data**: If most elements are empty/zero (e.g., a 1,000,000-element array with only 100 values), use a hash map to store only non-empty entries.

5. **Need Fast Min/Max with Updates**: Finding min/max is O(n). Use a heap (O(log n) insert, O(1) min) if you need repeated min/max operations.

**Red Flags in Problem Statements:**
- "Insert/delete frequently" → Consider linked list
- "Find if element exists" → Consider hash set
- "Get minimum/maximum repeatedly" → Consider heap

---

## Interview Context

Understanding array fundamentals is essential because:

- Arrays are the building block for almost every other data structure
- Interviewers expect O(1) access and O(n) traversal to be automatic knowledge
- Many "medium" problems are just clever combinations of basic array operations

---

## What is an Array?

An array is a contiguous block of memory storing elements of the same type. Each element is accessible by its index in O(1) time.

```
Memory Layout:
┌───┬───┬───┬───┬───┐
│ 5 │ 2 │ 8 │ 1 │ 9 │
└───┴───┴───┴───┴───┘
  0   1   2   3   4   ← indices
```

### Python Lists

In Python, `list` is a dynamic array that can hold any type:

```python
# Creation
arr = [1, 2, 3, 4, 5]
arr = [0] * 10           # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
arr = list(range(5))     # [0, 1, 2, 3, 4]

# Access
first = arr[0]           # O(1)
last = arr[-1]           # O(1) - Python negative indexing

# Length
n = len(arr)             # O(1)
```

---

## Core Operations and Complexity

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Access by index | O(1) | O(1) | `arr[i]` |
| Update by index | O(1) | O(1) | `arr[i] = x` |
| Append | O(1)* | O(1) | `arr.append(x)` - amortized |
| Insert at index | O(n) | O(1) | `arr.insert(i, x)` - shifts elements |
| Delete by index | O(n) | O(1) | `arr.pop(i)` - shifts elements |
| Delete from end | O(1) | O(1) | `arr.pop()` |
| Search (unsorted) | O(n) | O(1) | `x in arr` |
| Search (sorted) | O(log n) | O(1) | Binary search |

*Amortized O(1) due to dynamic resizing

---

## Common Traversal Patterns

### Forward Traversal

```python
def forward_traversal(arr: list[int]) -> None:
    """
    Time: O(n) - visit each element once
    Space: O(1)
    """
    for num in arr:
        print(num)

    # With index
    for i in range(len(arr)):
        print(f"Index {i}: {arr[i]}")

    # Pythonic with index
    for i, num in enumerate(arr):
        print(f"Index {i}: {num}")
```

### Backward Traversal

```python
def backward_traversal(arr: list[int]) -> None:
    """
    Time: O(n)
    Space: O(1)
    """
    # Using range with step -1
    for i in range(len(arr) - 1, -1, -1):
        print(arr[i])

    # Using reversed()
    for num in reversed(arr):
        print(num)
```

### Traversal with Step

```python
def every_other(arr: list[int]) -> list[int]:
    """
    Time: O(n/2) = O(n)
    Space: O(n/2) for result
    """
    return arr[::2]  # Elements at even indices

def every_third_backwards(arr: list[int]) -> list[int]:
    """
    Time: O(n/3) = O(n)
    """
    return arr[::-3]  # Every 3rd, backwards
```

---

## Array Rotation

### Problem: Rotate Array
**Problem Statement:** Given an array, rotate the array to the right or left by `k` steps, where `k` is non-negative.

**Why it works (The Reversal Trick):**
To rotate an array by `k` steps without extra space, we can use the property that reversing parts of the array and then the whole array can reorder elements. 
1. Reversing the segments that will be "moved" and the segment that "stays" reorders them locally.
2. Reversing the entire array then places these segments into their final rotated positions.
This is O(n) time and O(1) space.

### Left Rotation

Rotate array left by k positions: `[1,2,3,4,5]` rotated left by 2 → `[3,4,5,1,2]`

```python
def rotate_left_naive(arr: list[int], k: int) -> list[int]:
    """
    Time: O(n)
    Space: O(n) - creates new list
    """
    n = len(arr)
    k = k % n  # Handle k > n
    return arr[k:] + arr[:k]

def rotate_left_inplace(arr: list[int], k: int) -> None:
    """
    Time: O(n)
    Space: O(1) - in-place using reversal trick

    Idea: reverse(0, k-1), reverse(k, n-1), reverse(0, n-1)

    [1,2,3,4,5] k=2
    → [2,1,3,4,5] reverse first k
    → [2,1,5,4,3] reverse rest
    → [3,4,5,1,2] reverse all
    """
    def reverse(left: int, right: int) -> None:
        while left < right:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1

    n = len(arr)
    k = k % n
    if k == 0:
        return

    reverse(0, k - 1)
    reverse(k, n - 1)
    reverse(0, n - 1)
```

### Right Rotation

Rotate array right by k positions: `[1,2,3,4,5]` rotated right by 2 → `[4,5,1,2,3]`

```python
def rotate_right_inplace(arr: list[int], k: int) -> None:
    """
    Time: O(n)
    Space: O(1)

    Trick: right rotation by k = left rotation by (n - k)
    Or: reverse all, reverse first k, reverse rest

    [1,2,3,4,5] k=2
    → [5,4,3,2,1] reverse all
    → [4,5,3,2,1] reverse first k
    → [4,5,1,2,3] reverse rest
    """
    def reverse(left: int, right: int) -> None:
        while left < right:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1

    n = len(arr)
    k = k % n
    if k == 0:
        return

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
```

---

## Common Array Idioms in Python

### Swapping Elements

```python
# Pythonic swap - no temp variable needed
arr[i], arr[j] = arr[j], arr[i]
```

### Finding Min/Max with Index

```python
arr = [5, 2, 8, 1, 9]

# Just the value
min_val = min(arr)  # 1
max_val = max(arr)  # 9

# With index
min_idx = arr.index(min(arr))  # 3 (O(2n) = O(n))

# More efficient - single pass
min_idx = min(range(len(arr)), key=lambda i: arr[i])
```

### Slicing

```python
arr = [0, 1, 2, 3, 4, 5]

arr[2:5]    # [2, 3, 4] - indices 2,3,4
arr[:3]     # [0, 1, 2] - first 3
arr[3:]     # [3, 4, 5] - from index 3
arr[-2:]    # [4, 5] - last 2
arr[::2]    # [0, 2, 4] - every other
arr[::-1]   # [5, 4, 3, 2, 1, 0] - reversed

# Slicing creates a COPY
copy = arr[:]
```

### List Comprehensions

```python
# Filter
evens = [x for x in arr if x % 2 == 0]

# Transform
doubled = [x * 2 for x in arr]

# Combined
even_doubled = [x * 2 for x in arr if x % 2 == 0]
```

---

## Edge Cases to Always Check

```python
def robust_function(arr: list[int]) -> int:
    # Empty array
    if not arr:
        return 0  # or -1, or raise exception

    # Single element
    if len(arr) == 1:
        return arr[0]

    # Two elements (often special case for comparisons)
    # ...

    # All same values
    # ...

    # Already sorted / reverse sorted
    # ...
```

---

## Visual: Array vs Linked List Trade-offs

```
                    Array           Linked List
                    ─────           ───────────
Access by index     O(1) ✓          O(n)
Insert at start     O(n)            O(1) ✓
Insert at end       O(1)*           O(1)
Insert in middle    O(n)            O(1)**
Delete              O(n)            O(1)**
Memory              Contiguous      Scattered
Cache               Friendly ✓      Unfriendly

* Amortized
** After finding the node
```

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Rotate Array | Medium | Reversal trick |
| 2 | Plus One | Easy | Carry propagation |
| 3 | Move Zeroes | Easy | Two pointers |
| 4 | Remove Element | Easy | In-place modification |
| 5 | Find All Duplicates in an Array | Medium | Index as hash |
| 6 | Product of Array Except Self | Medium | Prefix/suffix products |

---

## Key Takeaways

1. **O(1) access** is the superpower of arrays - use it!
2. **Slicing creates copies** - be aware of O(n) space
3. **Rotation uses reversal trick** - memorize the pattern
4. **Always handle edge cases**: empty, single element, all same
5. **Python lists are dynamic** - append is amortized O(1)

---

## Next: [02-two-pointers-same-direction.md](./02-two-pointers-same-direction.md)

Learn the fast/slow pointer technique for in-place array processing.
