# Space Complexity Analysis

> **Prerequisites:** [01-big-o-notation.md](./01-big-o-notation.md)

## Building Intuition

**The "Desk Space" Mental Model**

Imagine your algorithm is doing paperwork at a desk:

- **Input papers**: The data you're given to process.
- **Scratch paper**: Extra notes you make to solve the problem (THIS is what we measure).
- **Stack of pending work**: Recursive calls waiting to be processed.

Space complexity asks: "How much scratch paper do I need?"

```text
Finding max in array:  Just one sticky note for "current max" → O(1)
Making a copy:         Photocopy every page of the input → O(n)
Building a matrix:     n×n grid of sticky notes → O(n²)
Recursive factorial:   Stack of n pending calculations → O(n)
```

**The Forgotten Cost: Recursion Stack**

Every recursive call is like putting a bookmark in a book and starting a new chapter. You need to remember where you were so you can return to it.

```python
factorial(5)      # Bookmark 1: "Return to multiply by 5"
  factorial(4)    # Bookmark 2: "Return to multiply by 4"
    factorial(3)  # Bookmark 3: "Return to multiply by 3"
      ...         # Stack grows with n bookmarks → O(n) space!
```

**Key Insight**

A recursive solution that "looks" like it uses O(1) space often uses O(n) stack space under the hood. Always ask: "How deep can the recursion go?"

---

## Interview Context

Space complexity is the **most commonly forgotten** aspect of complexity analysis. Interviewers frequently ask:

- "What's the space complexity?" (often asked if you only mentioned time)
- "Can you do this in-place?" (a hint to reduce space complexity to O(1))
- "What's the space usage of your recursive solution?" (testing if you understand the call stack)

Missing space analysis is a red flag. Build the habit: always mention **both** time AND space upfront.

---

## What Counts as Space?

### Auxiliary Space vs Total Space

- **Auxiliary space**: The *extra* space your algorithm uses (excluding the input space).
- **Total space**: Auxiliary space + Input space.

In interviews, when asked about "space complexity", they almost always mean **auxiliary space**.

```python
def sum_array(arr: list[int]) -> int:
    """
    Auxiliary Space: O(1) - only using a single 'total' variable.
    Total space: O(n) - because the input array is size n.

    We report: O(1) space
    """
    total = 0
    for num in arr:
        total += num
    return total
```

### What Counts

| Category             | Counts in Auxiliary Space? | Example                          |
| -------------------- | -------------------------- | -------------------------------- |
| New data structures  | Yes                        | `result = []`, `seen = set()`    |
| Primitive variables  | Yes (but usually O(1))     | `count = 0`, `i = 0`             |
| Recursion call stack | Yes                        | Each recursive call adds a frame |
| Input data           | No                         | The `arr` passed into the function |
| Output data          | Usually No                 | Space allocated strictly to return the answer is often ignored, unless specifically requested to count it. |

---

## Common Space Complexities

### O(1) - Constant Space

Uses a fixed amount of memory regardless of input size. Often associated with "in-place" algorithms.

```python
def find_max(arr: list[int]) -> int:
    """
    Space: O(1) - only storing a single value.
    """
    if not arr:
        return float('-inf')

    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val

def reverse_in_place(arr: list[int]) -> None:
    """
    Space: O(1) - modifying the input array in-place.
    """
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

### O(n) - Linear Space

Space scales directly with the input size.

```python
def duplicate_array(arr: list[int]) -> list[int]:
    """
    Space: O(n) - creating a new array of the same size.
    """
    return arr[:]

def frequency_count(arr: list[int]) -> dict[int, int]:
    """
    Space: O(n) - in the worst case (all elements unique),
    the dictionary stores n key-value pairs.
    """
    freq = {}
    for num in arr:
        freq[num] = freq.get(num, 0) + 1
    return freq
```

### O(n²) - Quadratic Space

Space scales with the square of the input size. Often seen with 2D matrices or finding all pairs.

```python
def create_matrix(n: int) -> list[list[int]]:
    """
    Space: O(n²) - allocating an n×n grid.
    """
    return [[0] * n for _ in range(n)]

def all_pairs(arr: list[int]) -> list[tuple[int, int]]:
    """
    Space: O(n²) - storing all n*(n-1)/2 pairs in a new list.
    """
    pairs = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            pairs.append((arr[i], arr[j]))
    return pairs
```

---

## Recursion and Call Stack

**This is where most candidates make mistakes.**

Every recursive call adds a **stack frame** to memory. The maximum stack depth determines the space complexity.

### Linear Recursion - O(n) Stack Space

```python
def factorial(n: int) -> int:
    """
    Time: O(n)
    Space: O(n) - recursion stack depth is n.

    Stack trace at n=5:
    factorial(5)
      factorial(4)
        factorial(3)
          factorial(2)
            factorial(1)  ← max depth = 5
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

### Logarithmic Recursion - O(log n) Stack Space

```python
from typing import Optional

def binary_search_recursive(arr: list[int], target: int, left: int = 0, right: Optional[int] = None) -> int:
    """
    Time: O(log n)
    Space: O(log n) - recursion stack depth is log n.

    Stack depth halves each time:
    search(16 elements)
      search(8 elements)
        search(4 elements)
          search(2 elements)  ← max depth = 4 = log₂(16)
    """
    if right is None:
        right = len(arr) - 1
    if left > right:
        return -1

    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)
```

### Tree Recursion - Depends on Depth

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def tree_height(root: Optional[TreeNode]) -> int:
    """
    Time: O(n) - visit every node.
    Space: O(h) - where h is the height of the tree.

    Balanced tree: h = log n → O(log n) space
    Skewed tree (linked list): h = n → O(n) space
    """
    if not root:
        return 0
    return 1 + max(tree_height(root.left), tree_height(root.right))
```

### Exponential Time, but Linear Space

```python
def fibonacci_naive(n: int) -> int:
    """
    Time: O(2^n)
    Space: O(n) - NOT O(2^n)!

    Why? The execution is a depth-first traversal of the recursion tree.
    At any given moment, the call stack only holds the current path
    from the root down to a leaf. The longest path is length n.
    """
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)
```

**Key insight**: For recursion space, always think about the **maximum depth of the call stack at any single point in time**, not the total number of calls made.

---

## Space-Time Trade-offs

A fundamental concept in computer science: you can often use extra memory to make an algorithm run faster, or accept a slower runtime to save memory.

### Example: Two Sum

```python
# Approach 1: Optimize for Space
def two_sum_brute(nums: list[int], target: int) -> list[int]:
    """
    Time: O(n²)
    Space: O(1)
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

# Approach 2: Optimize for Time
def two_sum_hash(nums: list[int], target: int) -> list[int]:
    """
    Time: O(n)
    Space: O(n)

    Trade-off: We allocate an O(n) hash map to achieve O(n) time.
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

---

## In-Place Algorithms

"In-place" means the algorithm transforms input using no auxiliary data structures. However, a small amount of extra storage space is allowed for variables. This results in **O(1) auxiliary space**.

### Common In-Place Operations

```python
def remove_duplicates_sorted(arr: list[int]) -> int:
    """
    Space: O(1) - in-place modification.
    Returns the new logical length of the array.
    """
    if not arr:
        return 0

    write_idx = 1
    for read_idx in range(1, len(arr)):
        if arr[read_idx] != arr[read_idx - 1]:
            arr[write_idx] = arr[read_idx]
            write_idx += 1

    return write_idx
```

### Dutch National Flag (In-Place Partition)

```python
def sort_colors(nums: list[int]) -> None:
    """
    Sort array of 0s, 1s, 2s in-place.
    Time: O(n)
    Space: O(1)
    """
    low, mid, high = 0, 0, len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            # Notice we don't increment mid here, because the element
            # swapped from 'high' still needs to be evaluated.
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

---

## Hidden Space Usage

Certain operations in high-level languages like Python hide space complexities.

### String Operations in Python

Strings in Python are **immutable**. You cannot modify them in place.

```python
# O(n) space - strings are immutable
def add_char(s: str, c: str) -> str:
    """
    Space: O(n) - allocating a brand new string of length n+1.
    """
    return s + c

# Building string character by character
def build_string_bad(n: int) -> str:
    """
    Peak Auxiliary Space: O(n) at the end.
    Time Complexity: Technically O(n²) because each `+=` creates a new
    string, leading to 1 + 2 + 3 + ... + n operations and total memory churn.
    (Note: CPython has an optimization that sometimes makes this O(n) time,
    but architecturally it is O(n²) and considered bad practice).
    """
    s = ""
    for i in range(n):
        s += str(i)
    return s

# Best Practice: Use a list buffer
def build_string_good(n: int) -> str:
    """
    Time: O(n)
    Space: O(n) - using a list to buffer characters, then joining once.
    """
    chars = []
    for i in range(n):
        chars.append(str(i))
    return "".join(chars)
```

### Slicing Creates Copies

```python
def process_half(arr: list[int]) -> list[int]:
    """
    Space: O(n) - slicing a list creates a shallow copy!
    """
    mid = len(arr) // 2
    first_half = arr[:mid]  # This operation takes O(n) time and O(n) space
    return first_half

# Better approach to avoid copying: pass indices instead of slicing.
```

---

## Space Complexity Summary Table

| Pattern                       | Auxiliary Space | Example |
| ----------------------------- | --------------- | ------- |
| Primitive variables           | O(1)            | Pointers, counters |
| Modifying input directly      | O(1)            | Two pointers, in-place swaps |
| Hash map / Set                | O(n)            | Frequency maps, seen sets |
| Copying a list / array        | O(n)            | `arr[:]`, `.copy()` |
| 2D Matrix                     | O(n²)           | Dynamic programming grids |
| Linear recursion depth        | O(n)            | Traversing a linked list recursively |
| Binary tree max depth         | O(h) or O(n)    | Tree traversals (worst case skewed = O(n)) |
| Divide-and-conquer depth      | O(log n)        | Binary search, Merge sort call stack |

---

## Key Takeaways

1. **Always mention space complexity**: Make it a reflex alongside time complexity.
2. **Recursion is not free**: The call stack consumes space proportional to the maximum depth of the recursion tree.
3. **"In-place" means O(1) auxiliary space**: Modifying the input data structure without creating a new one.
4. **Beware hidden copies**: String concatenation and array slicing in Python allocate new memory.
5. **Trade space for time**: The most common optimization technique is using a Hash Map (O(n) extra space) to improve time from O(n²) to O(n).

---

## Next: [04-common-patterns.md](./04-common-patterns.md)

Quick reference for the complexity of common data structure operations.
