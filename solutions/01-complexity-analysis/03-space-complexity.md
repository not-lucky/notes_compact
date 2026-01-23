# Solution: Space Complexity Practice Problems

## Problem 1: Analyze space of iterative vs recursive solution
Analyze the space complexity for calculating the Nth Fibonacci number using a naive recursive approach.

### Constraints
- `n >= 0`

### Python Implementation
```python
def fibonacci_recursive(n: int) -> int:
    """
    Time Complexity: O(2^n)
    Space Complexity: O(n)

    The maximum depth of the recursion tree is n, meaning at most n stack frames
    are active at any given time.
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
```

---

## Problem 2: Identify in-place modifications
Implement an in-place array reversal.

### Constraints
- Input is a list of elements.

### Example
Input: `[1, 2, 3]`
Output: `[3, 2, 1]`

### Python Implementation
```python
def reverse_in_place(arr: list) -> None:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```
