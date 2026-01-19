# Space Complexity Analysis

> **Prerequisites:** [01-big-o-notation.md](./01-big-o-notation.md)

## Interview Context

Space complexity is the **most commonly forgotten** aspect of complexity analysis. Interviewers frequently ask:

- "What's the space complexity?" (after you only mentioned time)
- "Can you do this in-place?"
- "What's the space usage of your recursive solution?"

Missing space analysis can cost you a hire decision. Always mention both time AND space.

---

## What Counts as Space?

### Auxiliary Space vs Total Space

- **Auxiliary space**: Extra space your algorithm uses (not counting input)
- **Total space**: Auxiliary space + input space

In interviews, when asked about space complexity, they usually mean **auxiliary space**.

```python
def sum_array(arr: list[int]) -> int:
    """
    Space: O(1) auxiliary - only using 'total' variable
    Total space: O(n) - but input doesn't count

    We report: O(1) space
    """
    total = 0
    for num in arr:
        total += num
    return total
```

### What Counts

| Category | Counts | Example |
|----------|--------|---------|
| New data structures | Yes | `result = []`, `seen = set()` |
| Primitive variables | Yes (but usually O(1)) | `count = 0`, `i = 0` |
| Recursion call stack | Yes | Each recursive call adds a frame |
| Input data | Usually no | The array passed in |
| Output data | Depends | Sometimes counted, sometimes not |

---

## Common Space Complexities

### O(1) - Constant Space

```python
def find_max(arr: list[int]) -> int:
    """
    Space: O(1) - only storing a single value
    """
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val

def swap_in_place(arr: list[int], i: int, j: int) -> None:
    """
    Space: O(1) - modifying in-place
    """
    arr[i], arr[j] = arr[j], arr[i]

def reverse_in_place(arr: list[int]) -> None:
    """
    Space: O(1) - in-place modification
    """
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

### O(n) - Linear Space

```python
def duplicate_array(arr: list[int]) -> list[int]:
    """
    Space: O(n) - creating new array of same size
    """
    return arr[:]

def frequency_count(arr: list[int]) -> dict[int, int]:
    """
    Space: O(n) - in worst case, all elements unique
    """
    freq = {}
    for num in arr:
        freq[num] = freq.get(num, 0) + 1
    return freq

def filter_positive(arr: list[int]) -> list[int]:
    """
    Space: O(n) - in worst case, all elements positive
    """
    return [x for x in arr if x > 0]
```

### O(n²) - Quadratic Space

```python
def create_matrix(n: int) -> list[list[int]]:
    """
    Space: O(n²) - n×n grid
    """
    return [[0] * n for _ in range(n)]

def all_pairs(arr: list[int]) -> list[tuple[int, int]]:
    """
    Space: O(n²) - storing all pairs
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

Every recursive call adds a **stack frame** to memory. The stack depth determines additional space.

### Linear Recursion - O(n) Stack Space

```python
def factorial(n: int) -> int:
    """
    Time: O(n)
    Space: O(n) - recursion stack depth is n

    Stack at n=5:
    factorial(5)
      factorial(4)
        factorial(3)
          factorial(2)
            factorial(1)  ← max depth = 5
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def reverse_linked_list_recursive(head):
    """
    Time: O(n)
    Space: O(n) - recursion stack

    Many candidates say "O(1)" but forget the call stack!
    """
    if not head or not head.next:
        return head
    new_head = reverse_linked_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

### Logarithmic Recursion - O(log n) Stack Space

```python
def binary_search_recursive(arr, target, left=0, right=None):
    """
    Time: O(log n)
    Space: O(log n) - recursion stack depth is log n

    Stack for n=16:
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
def tree_height(root) -> int:
    """
    Time: O(n) - visit every node
    Space: O(h) where h = height of tree

    Balanced tree: h = log n → O(log n) space
    Skewed tree: h = n → O(n) space
    """
    if not root:
        return 0
    return 1 + max(tree_height(root.left), tree_height(root.right))
```

### Exponential Recursion - Space Can Vary

```python
def fibonacci_naive(n: int) -> int:
    """
    Time: O(2^n)
    Space: O(n) - NOT O(2^n)!

    Why? At any point, only one path from root to leaf is active.
    Max stack depth = n (the longest path).
    """
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)
```

**Key insight**: For recursion space, think about **maximum depth at any point**, not total number of calls.

---

## Tail Recursion (Optimization)

Some languages optimize tail recursion to O(1) space. Python does NOT.

```python
# NOT tail-recursive (Python doesn't optimize anyway)
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # Must wait for recursive call

# Tail-recursive version (still O(n) in Python)
def factorial_tail(n: int, acc: int = 1) -> int:
    if n <= 1:
        return acc
    return factorial_tail(n - 1, n * acc)  # Last operation is recursive call

# Iterative version - truly O(1) space
def factorial_iterative(n: int) -> int:
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

In interviews, if asked about space optimization for recursion in Python, convert to iterative.

---

## Space-Time Trade-offs

Often you can trade space for time or vice versa.

### Example: Two Sum

```python
# Approach 1: O(1) space, O(n²) time
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

# Approach 2: O(n) space, O(n) time
def two_sum_hash(nums: list[int], target: int) -> list[int]:
    """
    Time: O(n)
    Space: O(n)

    Trade-off: Use extra memory to gain speed.
    """
    seen = {}  # O(n) space
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

### Example: Check Duplicate

```python
# O(1) space, O(n log n) time - sort in-place
def has_duplicate_sort(nums: list[int]) -> bool:
    """
    Time: O(n log n)
    Space: O(1) - if sort is in-place
    """
    nums.sort()  # Modifies input
    for i in range(len(nums) - 1):
        if nums[i] == nums[i + 1]:
            return True
    return False

# O(n) space, O(n) time - use set
def has_duplicate_set(nums: list[int]) -> bool:
    """
    Time: O(n)
    Space: O(n)
    """
    return len(nums) != len(set(nums))
```

---

## In-Place Algorithms

"In-place" means O(1) auxiliary space (not counting input/output).

### Common In-Place Operations

```python
def reverse_array(arr: list[int]) -> None:
    """
    Space: O(1) - in-place
    """
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

def remove_duplicates_sorted(arr: list[int]) -> int:
    """
    Space: O(1) - in-place modification
    Returns new length.
    """
    if not arr:
        return 0

    write = 1
    for read in range(1, len(arr)):
        if arr[read] != arr[read - 1]:
            arr[write] = arr[read]
            write += 1
    return write
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
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

---

## Hidden Space Usage

### String Operations in Python

```python
# O(n) space - strings are immutable
def add_char(s: str, c: str) -> str:
    """
    Space: O(n) - creates new string
    """
    return s + c  # Creates entirely new string

# Building string character by character
def build_string_bad(n: int) -> str:
    """
    Space: O(n) at any time
    But creates O(n²) total memory due to copying
    """
    s = ""
    for i in range(n):
        s += str(i)  # Each += creates new string
    return s

# Better: use list
def build_string_good(n: int) -> str:
    """
    Space: O(n)
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
    Space: O(n) - slice creates copy!
    """
    mid = len(arr) // 2
    first_half = arr[:mid]  # O(n/2) = O(n) copy
    return first_half
```

---

## Space Complexity Summary Table

| Pattern | Auxiliary Space |
|---------|-----------------|
| Few variables | O(1) |
| Fixed-size array | O(1) |
| Hash map with up to n entries | O(n) |
| Result list of size n | O(n) |
| n×n matrix | O(n²) |
| Linear recursion depth | O(n) |
| Binary recursion depth | O(n) (max path) |
| Divide-and-conquer depth | O(log n) |

---

## Practice Problems

| # | Problem | Difficulty | Focus |
|---|---------|------------|-------|
| 1 | Analyze space of iterative vs recursive solution | Easy | Call stack |
| 2 | Identify in-place modifications | Easy | O(1) space |
| 3 | Space-time trade-off comparison | Medium | Trade-offs |
| 4 | Hidden space in string operations | Medium | Language specifics |
| 5 | Optimize recursive solution space | Medium | Convert to iterative |

---

## Key Takeaways

1. **Always mention space complexity** alongside time
2. **Recursion uses stack space** proportional to max depth
3. **"In-place" means O(1) auxiliary space**
4. **Strings in Python create copies** on concatenation
5. **List slicing creates copies**
6. **Trade space for time** is a common optimization

---

## Next: [04-common-patterns.md](./04-common-patterns.md)

Quick reference for the complexity of common data structure operations.
