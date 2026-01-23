# Modular Arithmetic

## Practice Problems

### 1. Pow(x, n)
**Difficulty:** Medium
**Concept:** Binary exponentiation

```python
def myPow(x: float, n: int) -> float:
    """
    Calculate x raised to the power n.
    Time: O(log n)
    Space: O(1)
    """
    if n == 0:
        return 1.0
    if n < 0:
        x = 1 / x
        n = -n

    result = 1.0
    while n > 0:
        if n & 1:
            result *= x
        x *= x
        n >>= 1
    return result
```
