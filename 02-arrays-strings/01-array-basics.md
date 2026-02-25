# Array Basics

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

## Overview

An array is a contiguous block of memory that stores elements of the same type, accessible by index in $\mathcal{O}(1)$ time. It's the most fundamental data structure in computer science, serving as the building block for almost every other data structure.

## Building Intuition

**Why are arrays so powerful?**

Think of an array as a row of numbered mailboxes in an apartment building. Each mailbox has an address (index), and you can go directly to any mailbox without checking the others. This is the $\mathcal{O}(1)$ random access superpower that makes arrays unique.

**The Memory Model**:

1. **Contiguous Allocation**: Arrays occupy consecutive memory locations. If element 0 is at address 1000 and each element takes 4 bytes, element 5 is at address 1000 + (5 × 4) = 1020. The CPU calculates this in one step—no searching required.

2. **Cache Friendliness**: Because elements are adjacent in memory, accessing one element often pre-loads nearby elements into the CPU cache. This makes sequential array traversal extremely fast—often 10-100x faster than pointer-chasing through scattered memory (like linked lists).

3. **The Trade-off**: This contiguous layout means insertion/deletion in the middle is expensive ($\mathcal{O}(n)$)—you must shift elements to maintain the sequence. Arrays excel at random access and sequential processing, not frequent modifications.

**Mental Model**: Think of an array as a long shelf of numbered cubbies. Because they are all in a straight line and exactly the same size, you can calculate the exact physical distance to cubby #450 and walk straight to it in $\mathcal{O}(1)$ time. A linked list, by contrast, is like a scavenger hunt where each clue tells you where to find the next one; to find the 450th clue, you must visit the first 449. Inserting a new cubby in the middle of a full shelf requires sliding all subsequent cubbies down one spot ($\mathcal{O}(n)$ time), whereas inserting a new clue in a scavenger hunt just means rewriting one clue's destination ($\mathcal{O}(1)$ time).

## When NOT to Use Arrays

Arrays aren't always the best choice. Consider alternatives when:

1. **Frequent Insertions/Deletions in Middle**: If you're constantly adding or removing elements at arbitrary positions, linked lists or balanced trees (O(log n) insert) may be better. Arrays require O(n) shifts.

2. **Unknown or Highly Variable Size**: If the size changes dramatically and unpredictably, dynamic arrays (like Python lists) handle this via amortized $\mathcal{O}(1)$ appends, but occasionally hit an $\mathcal{O}(n)$ resize cost. If inserts *in the middle* dominate, consider other structures.

3. **Need Fast Membership Testing**: "Is X in the array?" is $\mathcal{O}(n)$ for unsorted arrays. Use a hash set (amortized $\mathcal{O}(1)$) or a sorted array with binary search ($\mathcal{O}(\log n)$) instead.

4. **Sparse Data**: If most elements are empty/zero (e.g., a 1,000,000-element array with only 100 values), use a hash map to store only non-empty entries (amortized $\mathcal{O}(1)$ lookup).

5. **Need Fast Min/Max with Updates**: Finding min/max is $\mathcal{O}(n)$. Use a heap ($\mathcal{O}(\log n)$ insert, $\mathcal{O}(1)$ min) if you need repeated min/max operations with frequent updates.

**Red Flags in Problem Statements:**

- "Insert/delete frequently" → Consider linked list
- "Find if element exists" → Consider hash set
- "Get minimum/maximum repeatedly" → Consider heap

---

## Interview Context

Understanding array fundamentals is essential because:

- Arrays are the building block for almost every other data structure
- Interviewers expect $\mathcal{O}(1)$ access and $\mathcal{O}(n)$ traversal to be automatic knowledge
- Many "medium" problems are just clever combinations of basic array operations

---

## What is an Array?

An array is a contiguous block of memory storing elements of the same type. Each element is accessible by its index in $\mathcal{O}(1)$ time.

```
Memory Layout:
┌───┬───┬───┬───┬───┐
│ 5 │ 2 │ 8 │ 1 │ 9 │
└───┴───┴───┴───┴───┘
  0   1   2   3   4   ← indices
```

### Python Lists

In Python, `list` is a dynamic array under the hood. It maintains a contiguous array of pointers to objects in memory. Because it handles resizing automatically, `append` takes amortized $\mathcal{O}(1)$ time.

```python
# Creation
arr: list[int] = [1, 2, 3, 4, 5]
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

| Operation         | Time          | Space         | Notes                                |
| ----------------- | ------------- | ------------- | ------------------------------------ |
| Access by index   | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | `arr[i]`                             |
| Update by index   | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | `arr[i] = x`                         |
| Append            | $\mathcal{O}(1)$* | $\mathcal{O}(1)$ | `arr.append(x)` - amortized          |
| Insert at index   | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | `arr.insert(i, x)` - shifts elements |
| Delete by index   | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | `arr.pop(i)` - shifts elements       |
| Delete from end   | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | `arr.pop()`                          |
| Search (unsorted) | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | `x in arr`                           |
| Search (sorted)   | $\mathcal{O}(\log n)$ | $\mathcal{O}(1)$ | Binary search                        |

\*Amortized $\mathcal{O}(1)$ due to dynamic resizing under the hood. In Python, a list is implemented as a dynamic array. When it fills up, it allocates a larger chunk of memory and copies existing elements ($\mathcal{O}(n)$ cost), but this happens infrequently enough that the average cost per append is $\mathcal{O}(1)$.

---

## Common Traversal Patterns

### Forward Traversal

```python
def forward_traversal(arr: list[int]) -> None:
    """
    Time: O(n) - visit each element once
    Space: O(1) - constant extra space (not counting input)
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

    # Using reversed() - returns an iterator, O(1) space
    for num in reversed(arr):
        print(num)
```

### Traversal with Step

```python
def every_other(arr: list[int]) -> list[int]:
    """
    Time: O(n)
    Space: O(n) - creates a new list with n/2 elements
    """
    return arr[::2]  # Elements at even indices

def every_third_backwards(arr: list[int]) -> list[int]:
    """
    Time: O(n)
    Space: O(n) - creates a new list
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
This is $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space.

### Left Rotation

Rotate array left by k positions: `[1,2,3,4,5]` rotated left by 2 → `[3,4,5,1,2]`

```python
def rotate_left_naive(arr: list[int], k: int) -> list[int]:
    """
    Time: O(n)
    Space: O(n) - creates new list due to slicing
    """
    if not arr: return []
    n = len(arr)
    k = k % n  # Handle k >= n
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

    if not arr: return
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

    Trick: reverse all, reverse first k, reverse rest

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

    if not arr: return
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
min_idx = arr.index(min(arr))  # 3 (O(n) search + O(n) min = O(n))

# More efficient - single pass O(n) time
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

# Slicing creates a COPY taking O(n) space
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

### String Concatenation Nuances

When building strings in Python, avoid using `+=` in a loop. Strings are immutable, so `+=` creates a new string each time, resulting in an $\mathcal{O}(n^2)$ time complexity operation as it continually reallocates and copies memory. Instead, use a list to accumulate substrings and call `.join()` at the end for an $\mathcal{O}(n)$ operation.

```python
def bad_concat(words: list[str]) -> str:
    """
    Time: O(n^2) - reallocates memory on each +=
    Space: O(n)
    """
    result = ""
    for w in words:
        result += w  # BAD: string is immutable
    return result

def good_concat(words: list[str]) -> str:
    """
    Time: O(n) - list append is amortized O(1), .join() is O(n)
    Space: O(n) - holds n strings before joining
    """
    result = []
    for w in words:
        result.append(w)
    return "".join(result)
```

---

## Edge Cases to Always Check

```python
from typing import Any

def robust_function(arr: list[Any]) -> Any:
    # Empty array
    if not arr:
        return 0  # or -1, or raise ValueError("Empty array")

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
Access by index     $\mathcal{O}(1)$ ✓          $\mathcal{O}(n)$
Insert at start     $\mathcal{O}(n)$            $\mathcal{O}(1)$ ✓
Insert at end       $\mathcal{O}(1)$*           $\mathcal{O}(1)$
Insert in middle    $\mathcal{O}(n)$            $\mathcal{O}(1)$**
Delete              $\mathcal{O}(n)$            $\mathcal{O}(1)$**
Memory              Contiguous      Scattered
Cache               Friendly ✓      Unfriendly

* Amortized
** After finding the node
```

---

## Practice Problems

| #   | Problem                         | Difficulty | Key Concept            |
| --- | ------------------------------- | ---------- | ---------------------- |
| 1   | Rotate Array                    | Medium     | Reversal trick         |
| 2   | Plus One                        | Easy       | Carry propagation      |
| 3   | Move Zeroes                     | Easy       | Two pointers           |
| 4   | Remove Element                  | Easy       | In-place modification  |
| 5   | Find All Duplicates in an Array | Medium     | Index as hash          |
| 6   | Product of Array Except Self    | Medium     | Prefix/suffix products |

---

## Key Takeaways

1. **$\mathcal{O}(1)$ access** is the superpower of arrays - use it!
2. **Slicing creates copies** - be aware of $\mathcal{O}(n)$ space.
3. **Rotation uses reversal trick** - memorize the pattern.
4. **Always handle edge cases**: empty, single element, all same.
5. **Python lists are dynamic** - append is amortized $\mathcal{O}(1)$.
6. **Beware String `+=`** - build a list and `.join()` instead to avoid $\mathcal{O}(n^2)$ time penalties.

---

## Next: [02-two-pointers-same-direction.md](./02-two-pointers-same-direction.md)

Learn the fast/slow pointer technique for in-place array processing.
