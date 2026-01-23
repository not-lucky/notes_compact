# Solution: Time Complexity Practice Problems

## Problem 1: Analyze a given code snippet
Analyze the time complexity of the following code:
```python
def mystery1(n):
    i = 1
    while i < n:
        for j in range(n):
            pass
        i *= 2
```

### Constraints
- `n >= 1`

### Example
For `n = 4`:
- `i = 1`: `j` runs 4 times. `i` becomes 2.
- `i = 2`: `j` runs 4 times. `i` becomes 4.
Total work is proportional to `n * log n`.

### Python Implementation
```python
def mystery1(n: int) -> None:
    """
    Time Complexity: O(n log n)
    Space Complexity: O(1)

    The outer while loop runs log(n) times because i doubles in each iteration.
    The inner for loop runs n times for each outer iteration.
    Total time = O(n * log n).
    """
    i = 1
    while i < n:
        for j in range(n):
            pass
        i *= 2
```

---

## Problem 2: Compare recursive vs iterative
Compare the time and space complexity of recursive vs iterative factorial.

### Constraints
- `n >= 0`

### Python Implementation
```python
def factorial_recursive(n: int) -> int:
    """
    Time: O(n)
    Space: O(n) - due to recursion stack
    """
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)

def factorial_iterative(n: int) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res
```
