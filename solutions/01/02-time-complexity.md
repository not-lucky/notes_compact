# Time Complexity Analysis

## Practice Problems

### 1. Analyze a given code snippet
**Difficulty:** Easy
**Focus:** Loop analysis

```python
def analyze_loop(n: int) -> int:
    """
    Analyzes a loop with a non-standard increment.

    Time Complexity: O(log n) - The loop variable 'i' doubles each iteration.
    Space Complexity: O(1) - Uses only a constant amount of extra space.
    """
    count = 0
    i = 1
    while i < n:
        count += 1
        i *= 2
    return count
```

### 2. Compare recursive vs iterative
**Difficulty:** Easy
**Focus:** Recursion basics

```python
def factorial_iterative(n: int) -> int:
    """
    Iterative factorial implementation.
    Time: O(n)
    Space: O(1)
    """
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res

def factorial_recursive(n: int) -> int:
    """
    Recursive factorial implementation.
    Time: O(n)
    Space: O(n) - due to recursion stack depth
    """
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)
```

### 3. Identify amortized operations
**Difficulty:** Medium
**Focus:** Dynamic array

```python
def dynamic_array_append_analysis() -> None:
    """
    Analyzes the amortized time complexity of appending to a dynamic array.

    Time Complexity: O(1) amortized.
    While an occasional resize takes O(n), most appends take O(1).
    Over n appends, the total work is O(n), so average is O(1).
    """
    pass # Analysis only
```

### 4. Solve recurrence relations
**Difficulty:** Medium
**Focus:** Master theorem

```python
def merge_sort_recurrence(n: int) -> None:
    """
    Analyzes the recurrence relation T(n) = 2T(n/2) + O(n).

    By Master Theorem:
    a=2, b=2, d=1
    log_b(a) = log_2(2) = 1
    Since d = log_b(a), the complexity is O(n^d log n) = O(n log n).
    """
    pass # Analysis only
```

### 5. Two pointer complexity proof
**Difficulty:** Medium
**Focus:** Non-obvious O(n)

```python
def two_pointer_proof(arr: list[int]) -> None:
    """
    Proves why two pointers in a loop is O(n) even with nested structure.

    Time Complexity: O(n)
    Reasoning: The pointers 'left' and 'right' only move towards each other.
    Total distance covered is at most n, regardless of inner logic.
    """
    left, right = 0, len(arr) - 1
    while left < right:
        # Pointers only increase or decrease
        if True: # Placeholder for condition
            left += 1
        else:
            right -= 1
```
