# Square Root Problems

## Practice Problems

### 1. Sqrt(x)
**Difficulty:** Easy
**Concept:** Binary search

```python
def mySqrt(x: int) -> int:
    """
    Compute floor(sqrt(x)).
    Time: O(log x)
    Space: O(1)
    """
    if x < 2:
        return x

    left, right = 1, x // 2
    while left <= right:
        mid = (left + right) // 2
        if mid * mid == x:
            return mid
        if mid * mid < x:
            left = mid + 1
        else:
            right = mid - 1
    return right
```

### 2. Valid Perfect Square
**Difficulty:** Easy
**Concept:** Binary search or math

```python
def isPerfectSquare(num: int) -> bool:
    """
    Check if a number is a perfect square.
    Time: O(log num)
    Space: O(1)
    """
    if num < 1:
        return False

    left, right = 1, num
    while left <= right:
        mid = (left + right) // 2
        sq = mid * mid
        if sq == num:
            return True
        if sq < num:
            left = mid + 1
        else:
            right = mid - 1
    return False
```
