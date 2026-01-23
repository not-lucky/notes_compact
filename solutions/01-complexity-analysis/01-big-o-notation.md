# Solution: Analyze Nested Loop Patterns

## Problem Statement
Analyze the time and space complexity of the following Python code snippet:
```python
def mystery(n):
    for i in range(n):
        for j in range(i):
            print(i, j)
```

## Constraints
- `n` is a non-negative integer.

## Example
Input: `n = 3`
Output:
```
1 0
2 0
2 1
```

## Python Implementation
```python
def mystery(n: int) -> None:
    """
    Time Complexity: O(n^2)
    Space Complexity: O(1)

    The inner loop runs 0, 1, 2, ..., n-1 times.
    Total iterations = 0 + 1 + 2 + ... + (n-1) = n(n-1)/2, which is O(n^2).
    """
    for i in range(n):
        for j in range(i):
            print(i, j)
```
