# Space Complexity Analysis

## Practice Problems

### 1. Analyze space of iterative vs recursive solution
**Difficulty:** Easy
**Focus:** Call stack

```python
def reverse_iterative(s: str) -> str:
    """
    Iteratively reverses a string.
    Space: O(n) to store the result list, but O(1) auxiliary scratch space.
    """
    res = list(s)
    l, r = 0, len(res) - 1
    while l < r:
        res[l], res[r] = res[r], res[l]
        l += 1
        r -= 1
    return "".join(res)

def reverse_recursive(s: str) -> str:
    """
    Recursively reverses a string.
    Space: O(n) auxiliary space due to the recursion call stack.
    """
    if not s:
        return ""
    return reverse_recursive(s[1:]) + s[0]
```

### 2. Identify in-place modifications
**Difficulty:** Easy
**Focus:** O(1) space

```python
def reverse_in_place(arr: list[int]) -> None:
    """
    Reverses an array in-place.
    Time: O(n)
    Space: O(1) - No extra space proportional to input size.
    """
    l, r = 0, len(arr) - 1
    while l < r:
        arr[l], arr[r] = arr[r], arr[l]
        l += 1
        r -= 1
```

### 3. Space-time trade-off comparison
**Difficulty:** Medium
**Focus:** Trade-offs

```python
def has_duplicate_brute(nums: list[int]) -> bool:
    """Space: O(1), Time: O(n^2)"""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]: return True
    return False

def has_duplicate_optimized(nums: list[int]) -> bool:
    """Space: O(n), Time: O(n)"""
    return len(nums) != len(set(nums))
```

### 4. Hidden space in string operations
**Difficulty:** Medium
**Focus:** Language specifics

```python
def string_concat_space(n: int) -> str:
    """
    Demonstrates hidden space usage in Python string concatenation.

    Each `s += char` creates a new string object, copying the old contents.
    Total space allocation over n steps is O(n^2).
    """
    s = ""
    for i in range(n):
        s += "a"
    return s
```

### 5. Optimize recursive solution space
**Difficulty:** Medium
**Focus:** Convert to iterative

```python
def fibonacci_iterative(n: int) -> int:
    """
    Optimizes space for Fibonacci calculation by converting to iterative.
    Recursive: O(n) stack space
    Iterative: O(1) auxiliary space (storing only last two values)
    """
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```
