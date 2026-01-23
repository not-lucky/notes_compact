# GCD and LCM

## Practice Problems

### 1. Greatest Common Divisor of Strings
**Difficulty:** Easy
**Concept:** GCD + string pattern

```python
from math import gcd

def gcdOfStrings(s1: str, s2: str) -> str:
    """
    Find the largest string x such that x divides both s1 and s2.
    Time: O(m + n)
    Space: O(m + n)
    """
    if s1 + s2 != s2 + s1:
        return ""

    return s1[:gcd(len(s1), len(s2))]
```

### 2. Water and Jug Problem
**Difficulty:** Medium
**Concept:** Bézout's identity

```python
from math import gcd

def canMeasureWater(x: int, y: int, target: int) -> bool:
    """
    Determine if you can measure exactly target liters with jugs of x and y.
    Time: O(log(min(x, y)))
    Space: O(1)
    """
    if target > x + y:
        return False
    return target % gcd(x, y) == 0
```
