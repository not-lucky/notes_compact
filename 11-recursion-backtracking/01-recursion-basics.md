# Recursion Basics

> **Prerequisites:** Basic understanding of function calls, stack data structure

## Interview Context

Recursion questions test:
1. **Mental model**: Can you trace through recursive calls?
2. **Base case identification**: Knowing when to stop
3. **Problem decomposition**: Breaking problems into smaller versions
4. **Space awareness**: Understanding call stack implications

---

## What is Recursion?

Recursion is when a function calls itself to solve a smaller instance of the same problem.

```
                    factorial(4)
                        │
              ┌─────────┴─────────┐
              │                   │
         return 4 × factorial(3)
                        │
              ┌─────────┴─────────┐
              │                   │
         return 3 × factorial(2)
                        │
              ┌─────────┴─────────┐
              │                   │
         return 2 × factorial(1)
                        │
                   return 1  (base case)
```

---

## The Three Components

### 1. Base Case
The condition where recursion stops. Without it, you get infinite recursion.

```python
def factorial(n: int) -> int:
    # Base case: stop when n is 0 or 1
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

### 2. Recursive Case
The part where the function calls itself with a smaller/simpler input.

```python
def sum_list(nums: list[int]) -> int:
    # Base case
    if not nums:
        return 0
    # Recursive case: first element + sum of rest
    return nums[0] + sum_list(nums[1:])
```

### 3. Progress Toward Base Case
Each recursive call must move closer to the base case.

```python
# WRONG: No progress toward base case
def infinite(n):
    return infinite(n)  # Never terminates!

# CORRECT: n decreases each call
def countdown(n):
    if n <= 0:
        return
    print(n)
    countdown(n - 1)  # Progress: n → n-1
```

---

## The Call Stack

When a function calls itself, each call is pushed onto the **call stack**:

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Call factorial(4):
# Stack: [factorial(4)]
# Stack: [factorial(4), factorial(3)]
# Stack: [factorial(4), factorial(3), factorial(2)]
# Stack: [factorial(4), factorial(3), factorial(2), factorial(1)]
# factorial(1) returns 1
# Stack: [factorial(4), factorial(3), factorial(2)] → returns 2*1 = 2
# Stack: [factorial(4), factorial(3)] → returns 3*2 = 6
# Stack: [factorial(4)] → returns 4*6 = 24
# Stack: [] → done
```

**Key insight**: Each function call has its own scope (local variables).

---

## Visualizing Recursion: The Tree

Many recursive problems form a **recursion tree**:

```
                    fib(5)
                   /      \
               fib(4)    fib(3)
              /    \     /    \
          fib(3) fib(2) fib(2) fib(1)
          /   \
      fib(2) fib(1)
```

This visualization helps:
- Understand the number of calls (time complexity)
- Identify overlapping subproblems (hint for DP)
- Debug recursive logic

---

## Recursion Patterns

### Pattern 1: Linear Recursion
One recursive call per function call. Forms a chain.

```python
def reverse_string(s: str) -> str:
    """
    Reverse a string recursively.

    Time: O(n) - n calls
    Space: O(n) - call stack depth
    """
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]

# reverse_string("hello")
# = reverse_string("ello") + "h"
# = (reverse_string("llo") + "e") + "h"
# = ((reverse_string("lo") + "l") + "e") + "h"
# = (((reverse_string("o") + "l") + "l") + "e") + "h"
# = ((("o" + "l") + "l") + "e") + "h"
# = "olleh"
```

### Pattern 2: Binary Recursion
Two recursive calls per function call. Forms a tree.

```python
def fibonacci(n: int) -> int:
    """
    Calculate nth Fibonacci number.

    Time: O(2^n) - exponential!
    Space: O(n) - max call stack depth
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### Pattern 3: Multiple Recursion
More than two recursive calls. Common in backtracking.

```python
def count_paths(grid, row, col):
    """Count paths from (0,0) to (row, col) moving right or down."""
    if row == 0 and col == 0:
        return 1
    if row < 0 or col < 0:
        return 0
    return count_paths(grid, row - 1, col) + count_paths(grid, row, col - 1)
```

---

## Thinking Recursively

### The "Leap of Faith"

**Trust** that your recursive call works correctly, then use it to solve the current problem.

Example: Reverse a linked list
```python
def reverse_list(head):
    # Base case: empty or single node
    if not head or not head.next:
        return head

    # LEAP OF FAITH: assume reverse_list correctly reverses head.next onward
    new_head = reverse_list(head.next)

    # Now just fix the connection
    head.next.next = head
    head.next = None

    return new_head
```

### The "Smaller Problem" Approach

Ask: "If I knew the answer to a smaller version, how would I use it?"

Example: Check if array is sorted
```python
def is_sorted(arr: list[int]) -> bool:
    # Base case
    if len(arr) <= 1:
        return True

    # If I knew whether arr[1:] is sorted...
    # I just need to check if arr[0] <= arr[1]
    return arr[0] <= arr[1] and is_sorted(arr[1:])
```

---

## Common Recursive Problems

### 1. Sum of Array

```python
def array_sum(arr: list[int]) -> int:
    """
    Time: O(n)
    Space: O(n) call stack
    """
    if not arr:
        return 0
    return arr[0] + array_sum(arr[1:])
```

### 2. Power Function

```python
def power(base: float, exp: int) -> float:
    """
    Calculate base^exp efficiently.

    Time: O(log n) - halving exp each time
    Space: O(log n) call stack
    """
    if exp == 0:
        return 1
    if exp < 0:
        return 1 / power(base, -exp)

    if exp % 2 == 0:
        half = power(base, exp // 2)
        return half * half
    else:
        return base * power(base, exp - 1)
```

### 3. Binary Search (Recursive)

```python
def binary_search(arr: list[int], target: int, left: int, right: int) -> int:
    """
    Time: O(log n)
    Space: O(log n) call stack
    """
    if left > right:
        return -1

    mid = left + (right - left) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, right)
    else:
        return binary_search(arr, target, left, mid - 1)
```

### 4. String Palindrome

```python
def is_palindrome(s: str) -> bool:
    """
    Time: O(n)
    Space: O(n) call stack
    """
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])
```

---

## Recursion vs Iteration

| Aspect | Recursion | Iteration |
|--------|-----------|-----------|
| Readability | Often cleaner for tree-like problems | Better for linear processes |
| Space | O(n) call stack | O(1) typically |
| Debugging | Harder to trace | Easier to step through |
| Risk | Stack overflow for deep recursion | No stack limit |

### Converting Recursion to Iteration

Any recursion can be converted using an explicit stack:

```python
# Recursive
def factorial_recursive(n):
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)

# Iterative equivalent
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Using explicit stack (mimics call stack)
def factorial_stack(n):
    stack = []
    # Push phase (simulates recursive calls)
    while n > 1:
        stack.append(n)
        n -= 1
    # Pop phase (simulates returns)
    result = 1
    while stack:
        result *= stack.pop()
    return result
```

---

## Tail Recursion

A function is **tail recursive** if the recursive call is the last operation.

```python
# NOT tail recursive (multiplication happens after recursive call)
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # Multiplication after recursion

# Tail recursive (recursive call is last)
def factorial_tail(n, accumulator=1):
    if n <= 1:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)  # Nothing after this
```

**Note**: Python does NOT optimize tail recursion, but some languages do.

---

## Stack Overflow and Limits

Python has a default recursion limit of ~1000:

```python
import sys
print(sys.getrecursionlimit())  # Usually 1000

# Increase if needed (use with caution)
sys.setrecursionlimit(10000)
```

For deep recursion, convert to iteration:

```python
# This will crash for n > 1000
def deep_recursion(n):
    if n == 0:
        return 0
    return 1 + deep_recursion(n - 1)

# Safe iterative version
def deep_iteration(n):
    return n
```

---

## Complexity Analysis

| Operation | Time | Space (Call Stack) |
|-----------|------|-------------------|
| Linear recursion (n calls) | O(n) | O(n) |
| Binary recursion (tree) | O(2^n) | O(n) depth |
| Divide and conquer | O(n log n) typical | O(log n) |
| Tail recursion | O(n) | O(1) if optimized |

---

## Edge Cases Checklist

- [ ] Empty input (empty array, empty string)
- [ ] Single element
- [ ] Maximum recursion depth
- [ ] Negative numbers (if applicable)
- [ ] Zero as input

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Fibonacci Number | Easy | Classic binary recursion |
| 2 | Power of Two | Easy | Linear recursion |
| 3 | Reverse String | Easy | Two-pointer or recursion |
| 4 | Merge Two Sorted Lists | Easy | Recursive merge |
| 5 | Maximum Depth of Binary Tree | Easy | Tree recursion |
| 6 | Climbing Stairs | Easy | Fibonacci variant |
| 7 | Pow(x, n) | Medium | Divide and conquer |

---

## Interview Tips

1. **Start with base case**: Always identify and write the base case first
2. **Trust the recursion**: Use the "leap of faith" approach
3. **Trace with small inputs**: Walk through with n=0, n=1, n=2
4. **Watch for duplicates**: If you see repeated work, consider memoization
5. **Know the limits**: Mention stack overflow concerns for deep recursion

---

## Key Takeaways

1. Every recursion needs: base case, recursive case, progress toward base
2. The call stack maintains state for each recursive call
3. Recursion trades space (stack) for code simplicity
4. Any recursion can be converted to iteration with explicit stack
5. Visualize recursion as a tree to understand complexity

---

## Next: [02-subsets.md](./02-subsets.md)

Learn how to generate all subsets using recursion and backtracking.
