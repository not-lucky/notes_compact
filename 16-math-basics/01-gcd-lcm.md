# GCD and LCM

> **Prerequisites:** None (foundational math concept)

## Interview Context

GCD (Greatest Common Divisor) and LCM (Least Common Multiple) appear frequently in interviews involving:
- String problems (GCD of strings)
- Fraction simplification
- Array operations (finding common periods)
- Water jug / pouring problems
- Scheduling (finding common cycles)

The Euclidean algorithm is the go-to approach—it's elegant, efficient, and easy to remember.

---

## Pattern: Euclidean Algorithm for GCD

The Euclidean algorithm is based on this key insight:

```
gcd(a, b) = gcd(b, a % b)
```

### Why This Works

```
If d divides both a and b, then d also divides (a - b).
Therefore, d divides (a mod b).

So gcd(a, b) = gcd(b, a mod b)

Base case: gcd(a, 0) = a (anything divides 0)
```

### Visual Example

```
Find gcd(48, 18):

Step 1: 48 = 18 × 2 + 12    →  gcd(48, 18) = gcd(18, 12)
Step 2: 18 = 12 × 1 + 6     →  gcd(18, 12) = gcd(12, 6)
Step 3: 12 = 6 × 2 + 0      →  gcd(12, 6)  = gcd(6, 0) = 6

Answer: gcd(48, 18) = 6
```

---

## Implementation

### GCD: Iterative Euclidean Algorithm

```python
def gcd(a: int, b: int) -> int:
    """
    Greatest Common Divisor using Euclidean algorithm.

    Time: O(log(min(a, b)))
    Space: O(1)
    """
    # Handle negative numbers
    a, b = abs(a), abs(b)

    while b:
        a, b = b, a % b
    return a


# Test
print(gcd(48, 18))   # 6
print(gcd(17, 5))    # 1 (coprime)
print(gcd(100, 25))  # 25
print(gcd(0, 5))     # 5
print(gcd(-12, 8))   # 4
```

### GCD: Recursive Version

```python
def gcd_recursive(a: int, b: int) -> int:
    """
    GCD using recursion (elegant but uses O(log n) stack space).

    Time: O(log(min(a, b)))
    Space: O(log(min(a, b))) - call stack
    """
    a, b = abs(a), abs(b)
    return a if b == 0 else gcd_recursive(b, a % b)
```

### LCM: Using GCD

```python
def lcm(a: int, b: int) -> int:
    """
    Least Common Multiple using the formula: lcm(a,b) = |a*b| / gcd(a,b)

    Time: O(log(min(a, b)))
    Space: O(1)
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


# Test
print(lcm(4, 6))    # 12
print(lcm(3, 5))    # 15
print(lcm(12, 18))  # 36
print(lcm(7, 0))    # 0
```

### LCM of Multiple Numbers

```python
from functools import reduce

def lcm_of_list(numbers: list[int]) -> int:
    """
    LCM of a list of numbers.

    Time: O(n * log(max_value))
    Space: O(1)
    """
    return reduce(lcm, numbers)


# Test
print(lcm_of_list([2, 3, 4]))     # 12
print(lcm_of_list([5, 10, 15]))   # 30
```

---

## Problem: Greatest Common Divisor of Strings

**LeetCode 1071**: Given two strings `s1` and `s2`, return the largest string `x` such that `x` divides both `s1` and `s2`.

### Example

```
Input: s1 = "ABCABC", s2 = "ABC"
Output: "ABC"

Input: s1 = "ABABAB", s2 = "ABAB"
Output: "AB"

Input: s1 = "LEET", s2 = "CODE"
Output: "" (no common divisor)
```

### Key Insight

If a GCD string exists, then `s1 + s2 == s2 + s1`. The GCD length is `gcd(len(s1), len(s2))`.

### Solution

```python
def gcdOfStrings(s1: str, s2: str) -> str:
    """
    Find the GCD of two strings.

    Time: O(m + n) for concatenation checks, O(log(min(m,n))) for GCD
    Space: O(m + n) for string concatenation
    """
    # If s1 + s2 != s2 + s1, no GCD exists
    if s1 + s2 != s2 + s1:
        return ""

    # GCD of lengths gives the GCD string length
    from math import gcd
    gcd_length = gcd(len(s1), len(s2))

    return s1[:gcd_length]


# Test
print(gcdOfStrings("ABCABC", "ABC"))     # "ABC"
print(gcdOfStrings("ABABAB", "ABAB"))    # "AB"
print(gcdOfStrings("LEET", "CODE"))      # ""
```

### Why `s1 + s2 == s2 + s1` Works

```
If x divides both s1 and s2:
  s1 = x + x + ... + x  (k1 times)
  s2 = x + x + ... + x  (k2 times)

Then:
  s1 + s2 = x repeated (k1 + k2) times
  s2 + s1 = x repeated (k2 + k1) times

Since k1 + k2 = k2 + k1, we have s1 + s2 = s2 + s1

The converse is also true: if s1 + s2 = s2 + s1,
then s1 and s2 are made of the same repeating unit.
```

---

## Problem: Water Jugs Problem

**LeetCode 365**: Given jugs of capacity `x` and `y` liters and unlimited water supply, determine if you can measure exactly `target` liters.

### Key Insight

By Bézout's identity: `ax + by = target` has integer solutions if and only if `gcd(x, y)` divides `target`.

### Solution

```python
def canMeasureWater(x: int, y: int, target: int) -> bool:
    """
    Can we measure exactly target liters with jugs of capacity x and y?

    Time: O(log(min(x, y)))
    Space: O(1)
    """
    from math import gcd

    # Can't exceed total capacity
    if target > x + y:
        return False

    # target must be divisible by gcd(x, y)
    return target % gcd(x, y) == 0


# Test
print(canMeasureWater(3, 5, 4))   # True (5 - 3 + 3 - 1 = 4)
print(canMeasureWater(2, 6, 5))   # False (gcd=2, 5%2 != 0)
print(canMeasureWater(1, 2, 3))   # True (1 + 2 = 3)
```

---

## Problem: Fraction Simplification

Given a fraction, reduce it to lowest terms.

```python
def simplify_fraction(numerator: int, denominator: int) -> tuple[int, int]:
    """
    Simplify a fraction to lowest terms.

    Time: O(log(min(num, denom)))
    Space: O(1)
    """
    from math import gcd

    if denominator == 0:
        raise ValueError("Denominator cannot be zero")

    # Handle signs (put negative in numerator only)
    if denominator < 0:
        numerator, denominator = -numerator, -denominator

    # Reduce by GCD
    g = gcd(abs(numerator), abs(denominator))
    return numerator // g, denominator // g


# Test
print(simplify_fraction(6, 8))     # (3, 4)
print(simplify_fraction(-12, 18))  # (-2, 3)
print(simplify_fraction(4, -8))    # (-1, 2)
print(simplify_fraction(17, 5))    # (17, 5) - already simplified
```

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| GCD (iterative) | O(log(min(a,b))) | O(1) | Best choice |
| GCD (recursive) | O(log(min(a,b))) | O(log n) | Stack space |
| LCM | O(log(min(a,b))) | O(1) | Uses GCD |
| LCM of n numbers | O(n log max) | O(1) | Reduce over list |

---

## Extended Euclidean Algorithm

For some problems (modular inverse, etc.), we need coefficients `x, y` such that `ax + by = gcd(a, b)`.

```python
def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b)

    Time: O(log(min(a, b)))
    Space: O(log(min(a, b))) for recursion
    """
    if b == 0:
        return a, 1, 0

    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1

    return g, x, y


# Test
g, x, y = extended_gcd(35, 15)
print(f"gcd=35*{x} + 15*{y} = {35*x + 15*y}")  # gcd=35*1 + 15*(-2) = 5
```

---

## Common Variations

### 1. GCD of Array

```python
from functools import reduce
from math import gcd

def gcd_of_list(numbers: list[int]) -> int:
    """Find GCD of all numbers in list."""
    return reduce(gcd, numbers)


# Test
print(gcd_of_list([12, 18, 24]))  # 6
```

### 2. Check if Coprime

```python
def are_coprime(a: int, b: int) -> bool:
    """Two numbers are coprime if gcd(a, b) = 1."""
    from math import gcd
    return gcd(a, b) == 1


print(are_coprime(14, 15))  # True
print(are_coprime(14, 21))  # False (both divisible by 7)
```

### 3. N-th Ugly Number (involving LCM)

Numbers whose only prime factors are 2, 3, and 5.

```python
def nthUglyNumber(n: int) -> int:
    """
    Find the nth ugly number using DP.

    Time: O(n)
    Space: O(n)
    """
    ugly = [0] * n
    ugly[0] = 1

    i2 = i3 = i5 = 0
    next2, next3, next5 = 2, 3, 5

    for i in range(1, n):
        ugly[i] = min(next2, next3, next5)

        if ugly[i] == next2:
            i2 += 1
            next2 = ugly[i2] * 2
        if ugly[i] == next3:
            i3 += 1
            next3 = ugly[i3] * 3
        if ugly[i] == next5:
            i5 += 1
            next5 = ugly[i5] * 5

    return ugly[n - 1]


print(nthUglyNumber(10))  # 12 (1,2,3,4,5,6,8,9,10,12)
```

---

## Edge Cases

1. **Zero**: `gcd(0, n) = n`, `lcm(0, n) = 0`
2. **Negative numbers**: Take absolute values
3. **Both zero**: `gcd(0, 0)` is undefined (often return 0)
4. **Coprime numbers**: `gcd = 1`, `lcm = a * b`
5. **Same numbers**: `gcd(n, n) = n`, `lcm(n, n) = n`

---

## Python Built-ins

```python
from math import gcd, lcm  # lcm added in Python 3.9

print(gcd(48, 18))     # 6
print(lcm(4, 6))       # 12
print(gcd(0, 5))       # 5

# For multiple numbers (Python 3.9+)
from math import gcd, lcm
print(gcd(12, 18, 24))    # 6
print(lcm(2, 3, 4))       # 12
```

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Greatest Common Divisor of Strings | Easy | GCD + string pattern |
| 2 | Water and Jug Problem | Medium | Bézout's identity |
| 3 | Ugly Number II | Medium | LCM with DP |
| 4 | Fraction to Recurring Decimal | Medium | GCD for simplification |
| 5 | X of a Kind in a Deck of Cards | Easy | GCD of all counts ≥ 2 |

---

## Related Sections

- [Prime Numbers](./02-prime-numbers.md) - Related to GCD factorization
- [Modular Arithmetic](./03-modular-arithmetic.md) - Uses extended GCD
