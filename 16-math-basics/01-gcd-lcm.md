# GCD and LCM

> **Prerequisites:** None (foundational math concept)

## Building Intuition

### The "Shared Building Block" Mental Model

Think of GCD as finding the **largest unit** that tiles both numbers perfectly:

```
For 48 and 18:
  48 = 6 x 8
  18 = 6 x 3
  GCD = 6 (the largest shared building block)

For 35 and 15:
  35 = 5 x 7
  15 = 5 x 3
  GCD = 5
```

### Why the Euclidean Algorithm Works

**Core insight:** if `d` divides both `a` and `b`, then `d` also divides `a - b`.
Therefore we can keep subtracting the smaller from the larger without changing the GCD:

```
gcd(48, 18) = gcd(48 - 18, 18) = gcd(30, 18)
             = gcd(30 - 18, 18) = gcd(12, 18)
             = gcd(12, 18 - 12) = gcd(12, 6)
             = gcd(12 - 6, 6)   = gcd(6, 6)
             = gcd(6 - 6, 6)    = gcd(0, 6) = 6
```

That's a lot of subtractions. Modulo is just **fast repeated subtraction**:
`48 % 18 = 12` computes `48 - 18 - 18 = 12` in one step.

So the Euclidean algorithm replaces subtraction with modulo:
**`gcd(a, b) = gcd(b, a % b)`**, base case **`gcd(a, 0) = a`**.

### LCM: The Flip Side

LCM answers: "how often do these cycles sync up?"

- Bus A comes every 4 minutes, Bus B every 6 minutes
- When do they arrive together? Every **LCM(4, 6) = 12** minutes

**Formula:** `LCM(a, b) = |a * b| / GCD(a, b)`

**Why this formula works:** Every number can be expressed as a product of primes.
GCD picks the **minimum** exponent of each prime, LCM picks the **maximum**.
Since `min(x, y) + max(x, y) = x + y` for any exponents, we get:
`GCD(a, b) * LCM(a, b) = a * b`.

---

## Interview Context

GCD and LCM appear frequently in interviews involving:

- **String problems** — GCD of strings (LeetCode 1071)
- **Fraction simplification** — reduce to lowest terms
- **Array operations** — finding common divisors across all elements
- **Water jug / pouring problems** — Bezout's identity
- **Scheduling** — finding common cycles, sync points
- **Counting / inclusion-exclusion** — multiples of a or b up to n

The Euclidean algorithm is the go-to approach — it's elegant, efficient, and easy to remember.

---

## Pattern: Euclidean Algorithm for GCD

```
gcd(a, b) = gcd(b, a % b)
gcd(a, 0) = a
```

### Proof Sketch

```
Let d = gcd(a, b).  We can write a = b*q + r  where r = a mod b.

Since d divides a and b, it must divide r = a - b*q.
So d divides both b and r  ->  d divides gcd(b, r).

Conversely, any divisor of b and r also divides a = b*q + r.
So gcd(a, b) = gcd(b, a mod b).

Base case: gcd(a, 0) = a  (every integer divides 0).
```

### Worked Example

```
Find gcd(48, 18):

Step 1: 48 = 18 x 2 + 12   ->  gcd(48, 18) = gcd(18, 12)
Step 2: 18 = 12 x 1 + 6    ->  gcd(18, 12) = gcd(12, 6)
Step 3: 12 = 6  x 2 + 0    ->  gcd(12, 6)  = gcd(6, 0) = 6

Answer: gcd(48, 18) = 6
```

---

## Implementation

### GCD: Iterative (Preferred)

```python
def gcd(a: int, b: int) -> int:
    """
    Greatest Common Divisor using the Euclidean algorithm.

    Time:  O(log(min(a, b)))  — each step reduces the larger number by at least half
    Space: O(1)
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


# Tests
print(gcd(48, 18))   # 6
print(gcd(17, 5))    # 1 (coprime)
print(gcd(100, 25))  # 25
print(gcd(0, 5))     # 5
print(gcd(-12, 8))   # 4
```

### GCD: Recursive

```python
def gcd_recursive(a: int, b: int) -> int:
    """
    GCD using recursion — elegant but uses stack space.

    Time:  O(log(min(a, b)))
    Space: O(log(min(a, b))) — call stack
    """
    a, b = abs(a), abs(b)
    if b == 0:
        return a
    return gcd_recursive(b, a % b)
```

> **Note:** In interviews, the iterative version is preferred — no risk of stack
> overflow on large inputs.

### LCM: Using GCD

```python
def lcm(a: int, b: int) -> int:
    """
    Least Common Multiple: lcm(a, b) = |a * b| / gcd(a, b).

    We compute a // gcd(a, b) * b instead of a * b // gcd(a, b)
    to avoid unnecessary overflow in languages with fixed-width integers.

    Time:  O(log(min(a, b)))
    Space: O(1)
    """
    if a == 0 or b == 0:
        return 0
    return abs(a // gcd(a, b) * b)


# Tests
print(lcm(4, 6))    # 12
print(lcm(3, 5))    # 15
print(lcm(12, 18))  # 36
print(lcm(7, 0))    # 0
```

### GCD / LCM of Multiple Numbers

```python
from functools import reduce

def gcd_of_list(numbers: list[int]) -> int:
    """GCD of a list of numbers, computed pairwise via reduce."""
    return reduce(gcd, numbers)


def lcm_of_list(numbers: list[int]) -> int:
    """
    LCM of a list of numbers, computed pairwise via reduce.

    Time:  O(n * log(max_value))
    Space: O(1)
    """
    return reduce(lcm, numbers)


# Tests
print(gcd_of_list([12, 18, 24]))     # 6
print(lcm_of_list([2, 3, 4]))        # 12
print(lcm_of_list([5, 10, 15]))      # 30
```

---

## Extended Euclidean Algorithm

For some problems (modular inverse, Bezout coefficients), we need integers `x, y`
such that **`a*x + b*y = gcd(a, b)`** (Bezout's identity).

This guarantees that integer solutions exist for any integers `a, b` (not both zero).

```python
def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    Returns (g, x, y) such that a*x + b*y = g = gcd(a, b).

    Time:  O(log(min(a, b)))
    Space: O(log(min(a, b))) — recursion stack
    """
    if b == 0:
        return a, 1, 0  # a*1 + 0*0 = a

    g, x1, y1 = extended_gcd(b, a % b)
    # From the recursive call we have: b*x1 + (a % b)*y1 = g
    # Since a % b = a - (a // b) * b, substitute:
    #   b*x1 + (a - (a//b)*b)*y1 = g
    #   a*y1 + b*(x1 - (a//b)*y1) = g
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


# Test
g, x, y = extended_gcd(35, 15)
print(f"gcd(35, 15) = {g}, coefficients: x={x}, y={y}")
print(f"Verify: 35*{x} + 15*{y} = {35*x + 15*y}")
# gcd(35, 15) = 5, coefficients: x=1, y=-2
# Verify: 35*1 + 15*-2 = 5
```

### Iterative Extended GCD

```python
def extended_gcd_iterative(a: int, b: int) -> tuple[int, int, int]:
    """
    Iterative Extended Euclidean Algorithm — avoids recursion stack.
    Returns (g, x, y) such that a*x + b*y = g = gcd(a, b).

    Time:  O(log(min(a, b)))
    Space: O(1)
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    # old_r = gcd, old_s = x, old_t = y
    return old_r, old_s, old_t


# Test
g, x, y = extended_gcd_iterative(35, 15)
print(f"gcd(35, 15) = {g}, x={x}, y={y}")  # 5, 1, -2
print(f"Verify: 35*{x} + 15*{y} = {35*x + 15*y}")  # 5
```

---

## Complexity Analysis

| Operation          | Time               | Space        | Notes                     |
| ------------------ | ------------------ | ------------ | ------------------------- |
| GCD (iterative)    | O(log(min(a, b)))  | O(1)         | Best choice for interviews|
| GCD (recursive)    | O(log(min(a, b)))  | O(log(min))  | Stack space               |
| LCM (pair)         | O(log(min(a, b)))  | O(1)         | Via GCD                   |
| LCM of n numbers   | O(n * log(max))    | O(1)         | Pairwise reduce           |
| Extended GCD       | O(log(min(a, b)))  | O(1) or O(log) | Iterative or recursive |

**Why O(log(min(a, b)))?** Each modulo step reduces the larger value by at least
half (if `a >= b`, then `a mod b < a/2`). So the algorithm terminates in at most
`2 * log2(min(a, b))` steps. This is proven via the connection to Fibonacci numbers —
the worst-case inputs for the Euclidean algorithm are consecutive Fibonacci numbers.

---

## Common Variations

### Check if Two Numbers Are Coprime

```python
from math import gcd

def are_coprime(a: int, b: int) -> bool:
    """Two numbers are coprime if their GCD is 1 (no shared prime factors)."""
    return gcd(a, b) == 1


print(are_coprime(14, 15))  # True  (factors: {2,7} vs {3,5})
print(are_coprime(14, 21))  # False (both divisible by 7)
```

### Modular Inverse via Extended GCD

The modular inverse of `a` modulo `m` exists iff `gcd(a, m) = 1`. When it exists,
`x` from the extended GCD (`a*x + m*y = 1`) gives the inverse: `a*x = 1 (mod m)`.

```python
def mod_inverse(a: int, m: int) -> int:
    """
    Returns x such that (a * x) % m == 1.
    Raises ValueError if gcd(a, m) != 1 (inverse doesn't exist).

    Time:  O(log(min(a, m)))
    Space: O(1)
    """
    g, x, _ = extended_gcd_iterative(a, m)
    if g != 1:
        raise ValueError(f"Modular inverse does not exist (gcd({a}, {m}) = {g})")
    return x % m  # ensure positive result


print(mod_inverse(3, 7))   # 5  (because 3*5 = 15, 15 % 7 = 1)
print(mod_inverse(7, 11))  # 8  (because 7*8 = 56, 56 % 11 = 1)
```

---

## Python Built-ins

```python
from math import gcd, lcm  # lcm added in Python 3.9

# Single pair
print(gcd(48, 18))     # 6
print(lcm(4, 6))       # 12
print(gcd(0, 5))       # 5

# Multiple arguments (Python 3.9+)
print(gcd(12, 18, 24))    # 6
print(lcm(2, 3, 4))       # 12
```

> **Interview tip:** In coding interviews you can usually say "I'll use `math.gcd`"
> and implement LCM on top of it. Know the underlying algorithm in case asked.

---

## Edge Cases

1. **Zero:** `gcd(0, n) = n`, `lcm(0, n) = 0`
2. **Negative numbers:** Take absolute values first
3. **Both zero:** `gcd(0, 0)` is mathematically undefined; Python returns `0`
4. **Coprime numbers:** `gcd = 1`, `lcm = a * b`
5. **Same number:** `gcd(n, n) = n`, `lcm(n, n) = n`
6. **One is a multiple of the other:** `gcd(n, k*n) = n`, `lcm(n, k*n) = k*n`
7. **Overflow risk:** `a * b` can overflow in fixed-width languages; compute `a // gcd(a,b) * b` instead

---

## Practice Problems (Progressive)

### Easy: Greatest Common Divisor of Strings (LeetCode 1071)

Given two strings `s1` and `s2`, return the largest string `x` such that `x`
divides both `s1` and `s2`. A string `t` divides `s` if `s = t + t + ... + t`.

```
Input: s1 = "ABCABC", s2 = "ABC"  ->  Output: "ABC"
Input: s1 = "ABABAB", s2 = "ABAB" ->  Output: "AB"
Input: s1 = "LEET",   s2 = "CODE" ->  Output: ""
```

**Key insight:** If any GCD string exists, then `s1 + s2 == s2 + s1`. The length
of the GCD string equals `gcd(len(s1), len(s2))`.

**Why `s1 + s2 == s2 + s1` works:**

```
If x divides both s1 and s2:
  s1 = x repeated k1 times
  s2 = x repeated k2 times
Then:
  s1 + s2 = x repeated (k1 + k2) times = s2 + s1

Conversely, if s1 + s2 = s2 + s1, both strings must be built
from the same repeating unit (a theorem in combinatorics on words).
```

```python
from math import gcd

def gcd_of_strings(s1: str, s2: str) -> str:
    """
    Time:  O(m + n) for concatenation check
    Space: O(m + n) for the concatenated strings
    """
    # If no common divisor string exists, concatenations won't match
    if s1 + s2 != s2 + s1:
        return ""
    # The GCD string length must be gcd of the two lengths
    return s1[:gcd(len(s1), len(s2))]


print(gcd_of_strings("ABCABC", "ABC"))     # "ABC"
print(gcd_of_strings("ABABAB", "ABAB"))    # "AB"
print(gcd_of_strings("LEET", "CODE"))      # ""
```

---

### Easy: X of a Kind in a Deck of Cards (LeetCode 914)

Given a deck of cards where `deck[i]` is the number written on the i-th card,
return `True` if we can partition the deck into groups where each group has
**exactly X cards** (X >= 2) with the same number.

```
Input: deck = [1,2,3,4,4,3,2,1]  ->  Output: True  (groups of 2)
Input: deck = [1,1,1,2,2,2,3,3]  ->  Output: True  (groups of 2)
Input: deck = [1]                 ->  Output: False  (need X >= 2)
Input: deck = [1,1,2,2,2,2]      ->  Output: True   (X=2: [1,1],[2,2],[2,2])
```

**Key insight:** Count each card value's frequency. We need an `X >= 2` that divides
**every** frequency. That `X` exists iff `gcd(all frequencies) >= 2`.

```python
from math import gcd
from functools import reduce
from collections import Counter

def has_groups_size_x(deck: list[int]) -> bool:
    """
    Time:  O(n + k * log(max_count)) where k = distinct values
    Space: O(k) for the counter
    """
    counts = Counter(deck).values()
    overall_gcd = reduce(gcd, counts)
    return overall_gcd >= 2


print(has_groups_size_x([1,2,3,4,4,3,2,1]))  # True
print(has_groups_size_x([1,1,1,2,2,2,3,3]))  # True
print(has_groups_size_x([1]))                 # False
print(has_groups_size_x([1,1,2,2,2,2]))       # True
```

---

### Easy: Number of Steps to Reduce to Zero (LeetCode 1342 variant)

Not a direct GCD problem, but understanding why the Euclidean algorithm is
O(log n) helps here. A useful warm-up for thinking about how fast modular
reduction shrinks values.

```
Given two numbers, count how many Euclidean steps it takes to find their GCD.
```

```python
def gcd_steps(a: int, b: int) -> int:
    """
    Count the number of modulo steps in the Euclidean algorithm.
    Worst case is consecutive Fibonacci numbers.

    Time:  O(log(min(a, b)))
    Space: O(1)
    """
    steps = 0
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
        steps += 1
    return steps


print(gcd_steps(48, 18))     # 3 steps
print(gcd_steps(21, 13))     # 7 steps (Fibonacci pair — worst case)
print(gcd_steps(100, 1))     # 1 step  (best case)
```

---

### Medium: Water and Jug Problem (LeetCode 365)

Given jugs of capacity `x` and `y` liters with unlimited water supply,
determine if you can measure exactly `target` liters.

**Key insight — Bezout's identity:** The equation `a*x + b*y = target` has
integer solutions if and only if `gcd(x, y)` divides `target`. The operations
(fill, empty, pour) correspond to adding or subtracting multiples of x and y.

```python
from math import gcd

def can_measure_water(x: int, y: int, target: int) -> bool:
    """
    Time:  O(log(min(x, y)))
    Space: O(1)
    """
    if target > x + y:
        return False  # can't exceed total capacity
    if x == 0 and y == 0:
        return target == 0
    return target % gcd(x, y) == 0


print(can_measure_water(3, 5, 4))  # True  (5 - 3 + 5 - 3 = 4)
print(can_measure_water(2, 6, 5))  # False (gcd=2, 5 % 2 != 0)
print(can_measure_water(1, 2, 3))  # True  (1 + 2 = 3)
```

---

### Medium: Fraction Simplification

Reduce a fraction to lowest terms by dividing numerator and denominator by their GCD.
This pattern appears in LeetCode 592 (Fraction Addition and Subtraction) among others.

```python
from math import gcd

def simplify_fraction(numerator: int, denominator: int) -> tuple[int, int]:
    """
    Time:  O(log(min(|num|, |denom|)))
    Space: O(1)
    """
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")

    # Normalize sign: negative goes in numerator only
    if denominator < 0:
        numerator, denominator = -numerator, -denominator

    g = gcd(abs(numerator), denominator)
    return numerator // g, denominator // g


print(simplify_fraction(6, 8))     # (3, 4)
print(simplify_fraction(-12, 18))  # (-2, 3)
print(simplify_fraction(4, -8))    # (-1, 2)
print(simplify_fraction(0, 5))     # (0, 1)
print(simplify_fraction(17, 5))    # (17, 5) — already in lowest terms
```

---

### Medium: Ugly Number II (LeetCode 264)

Find the n-th **ugly number** — positive numbers whose only prime factors are 2, 3, and 5.
The sequence is: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, ...

**Connection to LCM/GCD:** While this problem uses DP with three pointers rather than
LCM directly, the concept of "least common multiple" is related — we're merging three
sequences (multiples of 2, 3, 5) and need to handle overlaps (e.g., 6 appears in both
the x2 and x3 sequences, like an LCM collision).

```python
def nth_ugly_number(n: int) -> int:
    """
    Three-pointer merge of the x2, x3, x5 sequences.

    Key idea: Every ugly number is 2x, 3x, or 5x for some smaller ugly number x.
    We maintain three pointers, each tracking which ugly number to multiply next.

    Time:  O(n)
    Space: O(n)
    """
    ugly = [0] * n
    ugly[0] = 1

    # Pointers into the ugly array for each factor
    i2 = i3 = i5 = 0
    next2, next3, next5 = 2, 3, 5

    for i in range(1, n):
        ugly[i] = min(next2, next3, next5)

        # Advance ALL pointers that match (handles duplicates like 6 = 2*3 = 3*2)
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


print(nth_ugly_number(10))   # 12
print(nth_ugly_number(1))    # 1
print(nth_ugly_number(15))   # 24
```

---

### Medium: Count Primes using LCM/GCD (LeetCode 2197 — Replace Non-Coprime Numbers)

Given an array of integers, repeatedly find adjacent elements that are **not coprime**
(gcd > 1), replace them with their LCM, and repeat until no more replacements can be made.

```
Input:  [6,4,3,2,7,6,2]
Output: [12,7,6]
Explanation: (6,4)->12, (3,2)->6, (6,6)->6, result [12,7,6]
```

**Key insight:** Use a stack. Push elements and keep merging the top two if they
share a common factor.

```python
from math import gcd

def replace_non_coprimes(nums: list[int]) -> list[int]:
    """
    Stack-based greedy merge of non-coprime adjacent pairs.

    Time:  O(n * log(max_val)) — each element pushed/popped at most once,
           each gcd is O(log(max_val))
    Space: O(n)
    """
    stack = []
    for num in nums:
        stack.append(num)
        # Keep merging top two elements while they share a factor
        while len(stack) >= 2:
            top = stack[-1]
            second = stack[-2]
            g = gcd(top, second)
            if g == 1:
                break  # coprime, stop merging
            # Replace both with their LCM
            merged = top // g * second  # = lcm(top, second)
            stack.pop()
            stack.pop()
            stack.append(merged)
    return stack


print(replace_non_coprimes([6,4,3,2,7,6,2]))   # [12, 7, 6]
print(replace_non_coprimes([2,2,1,1,3,3,3]))    # [2, 1, 1, 3]
```

---

### Hard: Nth Magical Number (LeetCode 878)

A positive integer is **magical** if it is divisible by `a` or `b`. Given `n`, `a`,
and `b`, return the n-th magical number modulo 10^9 + 7.

**Key insight — Inclusion-Exclusion + Binary Search:**
- Count of magical numbers <= `x` is: `x//a + x//b - x//lcm(a,b)`
  (subtract the overlap — numbers divisible by both a and b)
- Binary search for the smallest `x` where this count >= n

```python
from math import gcd

def nth_magical_number(n: int, a: int, b: int) -> int:
    """
    Binary search on the answer using inclusion-exclusion.

    Time:  O(log(n * min(a, b)) * log(min(a, b))) — binary search * gcd
           Simplifies to O(log(n * min(a, b))) since gcd is computed once
    Space: O(1)
    """
    MOD = 10**9 + 7
    ab_lcm = a * b // gcd(a, b)  # lcm(a, b)

    lo, hi = 1, n * min(a, b)
    while lo < hi:
        mid = (lo + hi) // 2
        # Count of magical numbers <= mid (inclusion-exclusion)
        count = mid // a + mid // b - mid // ab_lcm
        if count < n:
            lo = mid + 1
        else:
            hi = mid

    return lo % MOD


print(nth_magical_number(1, 2, 3))    # 2
print(nth_magical_number(4, 2, 3))    # 6
print(nth_magical_number(5, 2, 4))    # 10 (sequence: 2,4,6,8,10)
```

---

### Hard: Mirror Reflection (LeetCode 858)

A square room has mirrors on all walls with side length `p`. A laser shoots from
the bottom-left corner toward the right wall, hitting it first at height `q`.
Three receptors exist: 0 (bottom-right), 1 (top-right), 2 (top-left).
Which receptor does the laser eventually reach?

**Key insight:** Instead of simulating reflections, "unfold" the room by stacking
copies vertically. The laser travels in a straight line through these copies.
It reaches a receptor when the total vertical distance is a multiple of `p`.
The first such point is at height `lcm(p, q)`.

- Let `m = lcm(p,q) / p` = number of rooms stacked vertically = `q / gcd(p,q)`
- Let `n = lcm(p,q) / q` = number of horizontal bounces = `p / gcd(p,q)`

After dividing by `gcd(p, q)`, `m` and `n` are coprime, so they can't both be even.

| m (vertical) | n (horizontal) | Receptor |
|---------------|----------------|----------|
| even          | odd            | 0        |
| odd           | odd            | 1        |
| odd           | even           | 2        |

```python
from math import gcd

def mirror_reflection(p: int, q: int) -> int:
    """
    Time:  O(log(min(p, q)))
    Space: O(1)
    """
    g = gcd(p, q)
    m = q // g  # vertical rooms (number of times we cross a horizontal boundary)
    n = p // g  # horizontal bounces (number of times we hit a side wall)

    if m % 2 == 0:
        return 0  # even vertical, odd horizontal -> bottom-right receptor
    elif n % 2 == 0:
        return 2  # odd vertical, even horizontal -> top-left receptor
    else:
        return 1  # odd vertical, odd horizontal -> top-right receptor


print(mirror_reflection(2, 1))  # 2
print(mirror_reflection(3, 1))  # 1
print(mirror_reflection(3, 2))  # 0
```

---

### Hard: Count Pairs of Similar Strings with GCD constraints (LeetCode 2543 variant)

Given `n` and two integers `a` and `b`, count how many integers in `[1, n]` are
divisible by `a`, by `b`, by both, or by neither. This is the fundamental
**inclusion-exclusion** pattern that underpins many harder problems.

```python
from math import gcd

def count_divisibility(n: int, a: int, b: int) -> dict:
    """
    Inclusion-exclusion counting of divisibility in [1, n].

    Time:  O(log(min(a, b)))
    Space: O(1)
    """
    ab_lcm = a * b // gcd(a, b)

    div_a = n // a                     # divisible by a
    div_b = n // b                     # divisible by b
    div_both = n // ab_lcm             # divisible by both (= lcm)
    div_either = div_a + div_b - div_both  # divisible by a or b
    div_neither = n - div_either       # divisible by neither

    return {
        "div_a": div_a,
        "div_b": div_b,
        "div_both": div_both,
        "div_either": div_either,
        "div_neither": div_neither,
    }


result = count_divisibility(30, 3, 5)
print(result)
# {'div_a': 10, 'div_b': 6, 'div_both': 2, 'div_either': 14, 'div_neither': 16}
# Numbers 1-30 divisible by 3: 10, by 5: 6, by both (15,30): 2, by 3 or 5: 14
```

---

## Problem Summary

| #   | Problem                              | LC#  | Difficulty | Key Concept                         |
| --- | ------------------------------------ | ---- | ---------- | ----------------------------------- |
| 1   | Greatest Common Divisor of Strings   | 1071 | Easy       | GCD on string lengths               |
| 2   | X of a Kind in a Deck of Cards       | 914  | Easy       | GCD of all frequency counts >= 2    |
| 3   | Euclidean Steps Counter              | —    | Easy       | Understanding algorithm behavior    |
| 4   | Water and Jug Problem                | 365  | Medium     | Bezout's identity                   |
| 5   | Fraction Simplification              | —    | Medium     | GCD to reduce fractions             |
| 6   | Ugly Number II                       | 264  | Medium     | Three-pointer merge (related to LCM)|
| 7   | Replace Non-Coprime Numbers          | 2197 | Medium     | Stack + repeated GCD/LCM merging    |
| 8   | Nth Magical Number                   | 878  | Hard       | Binary search + inclusion-exclusion  |
| 9   | Mirror Reflection                    | 858  | Hard       | LCM to find laser endpoint          |
| 10  | Inclusion-Exclusion Counting         | —    | Hard       | LCM for overlap, foundational pattern|

---

## Key Patterns Cheat Sheet

```
Pattern                          When to use
──────────────────────────────── ──────────────────────────────────────
gcd(all values) >= k             Can we partition into groups of size k?
target % gcd(a,b) == 0           Is target reachable via combinations of a,b?
x//a + x//b - x//lcm(a,b)       Count numbers <= x divisible by a or b
a // gcd(a,b) * b                Compute LCM without overflow
s1+s2 == s2+s1                   Do strings share a common repeating unit?
Stack + merge while gcd>1        Collapse adjacent non-coprime elements
Binary search + count function   Find the n-th number with some divisibility property
Extended GCD                     Find modular inverse, Bezout coefficients
```

---

## When NOT to Use GCD/LCM

1. **When Python has it built-in:** Use `math.gcd()` and `math.lcm()` — don't reimplement in production
2. **When you need prime factors anyway:** Prime factorization gives you GCD/LCM as a side effect
3. **When extended GCD isn't needed:** Don't over-complicate with Bezout coefficients
4. **When one number is always 1:** `gcd(1, n) = 1`, `lcm(1, n) = n` — trivial, no computation needed

**Common mistake:** Computing `a * b // gcd(a, b)` for LCM — the intermediate `a * b`
can overflow in languages like C++/Java. Always compute `a // gcd(a, b) * b` instead.
(This doesn't matter in Python due to arbitrary-precision integers, but it's good
practice and expected in interviews.)

---

## Related Sections

- [Prime Numbers](./02-prime-numbers.md) — GCD via prime factorization
- [Modular Arithmetic](./03-modular-arithmetic.md) — uses extended GCD for modular inverse
