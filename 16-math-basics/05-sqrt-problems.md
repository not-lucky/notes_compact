# Square Root Problems

> **Prerequisites:** [Binary Search](../10-binary-search/README.md) (for integer sqrt)

## Building Intuition

**The "Goldilocks Search" Mental Model**

Finding `sqrt(n)` is like finding the perfect temperature:

- If `guess * guess < n`: too cold, go higher
- If `guess * guess > n`: too hot, go lower
- If `guess * guess == n`: just right!

Binary search naturally fits this pattern — we're searching for a value in a
sorted space `(1, 2, 3, ...)` where the predicate `x * x <= n` flips from True
to False at exactly one point.

**Why `sqrt(n)` Appears Everywhere**

Square root is the "balance point" of multiplication:

- If `n = a * b`, then at least one of `a` or `b` is `<= sqrt(n)`
  - *Proof:* If both `a > sqrt(n)` and `b > sqrt(n)`, then `a * b > n` — contradiction.
- This is why primality testing only checks divisors up to `sqrt(n)`
- This is why divisor enumeration runs in `O(sqrt(n))` time
- This is why the Sieve of Eratosthenes only sieves up to `sqrt(n)`

**Newton's Method: Faster Than Binary Search**

Instead of halving the search range each step, Newton's method uses calculus to
converge much faster:

- If `x` is an overestimate of `sqrt(n)`, then `n / x` is an underestimate (and vice versa)
- Their average `(x + n / x) / 2` is a tighter overestimate
- **Quadratic convergence**: the number of correct digits roughly *doubles* each
  iteration

For integers, this means ~`O(log log n)` iterations vs `O(log n)` for binary search.
In practice, Newton's method reaches the answer in very few steps even for huge `n`.

---

## Interview Context

Square root problems test:

- Binary search implementation skills (search on answer space)
- Edge case handling (0, 1, large numbers)
- Understanding of mathematical properties
- Divisor enumeration up to `sqrt(n)` (factorization, perfect numbers, primes)
- Newton's method (advanced — shows math sophistication)

Common patterns: integer square root, perfect square checks, divisor enumeration,
prime sieves, and problems where `sqrt(n)` appears in complexity analysis.

---

## Pattern 1: Binary Search for Integer Square Root

Find the largest integer `x` such that `x * x <= n`.

### Key Insight

```
For n = 50:
  7 * 7 = 49 <= 50  (valid)
  8 * 8 = 64 > 50   (too large)

Answer: 7

We binary search in range [1, n // 2] to find the largest x where x * x <= n.
This is a classic "last True" binary search pattern.
```

### Visualization

```
Find isqrt(50):

Range: [1, 25]   (n // 2 = 25)
  mid = 13, 13*13 = 169 > 50   -> right = 12
Range: [1, 12]
  mid = 6,  6*6   = 36  <= 50  -> left = 7, result = 6
Range: [7, 12]
  mid = 9,  9*9   = 81  > 50   -> right = 8
Range: [7, 8]
  mid = 7,  7*7   = 49  <= 50  -> left = 8, result = 7
Range: [8, 8]
  mid = 8,  8*8   = 64  > 50   -> right = 7
Range: [8, 7] -> left > right, done

Answer: 7
```

---

## Implementation

### Integer Square Root (LeetCode 69)

```python
def mySqrt(x: int) -> int:
    """
    Compute floor(sqrt(x)) using binary search.

    Time:  O(log x)
    Space: O(1)
    """
    if x < 2:
        return x  # sqrt(0) = 0, sqrt(1) = 1

    # For x >= 4, sqrt(x) <= x // 2.  For x in [2, 3], sqrt rounds to 1.
    left, right = 1, x // 2
    result = 1

    while left <= right:
        mid = (left + right) // 2
        square = mid * mid

        if square == x:
            return mid
        elif square < x:
            result = mid  # mid might be the answer; keep searching right
            left = mid + 1
        else:
            right = mid - 1

    return result


# Tests
assert mySqrt(0) == 0
assert mySqrt(1) == 1
assert mySqrt(2) == 1    # floor(1.41...) = 1
assert mySqrt(3) == 1    # floor(1.73...) = 1
assert mySqrt(4) == 2
assert mySqrt(8) == 2    # floor(2.83...) = 2
assert mySqrt(100) == 10
```

### Using Python Built-ins

```python
import math

# Python 3.8+ — math.isqrt gives exact integer square root (no float issues)
print(math.isqrt(50))       # 7
print(math.isqrt(2**50))    # 1048576 — always correct

# Caution with float-based sqrt for large numbers:
print(int(math.sqrt(50)))       # 7 (works here)
print(int(math.sqrt(2**50)))    # May be off by 1 due to float precision!

# If you must use math.sqrt, always verify:
def isqrt_safe(n: int) -> int:
    """Integer sqrt with float verification fallback."""
    r = int(math.sqrt(n))
    # Adjust for float imprecision
    if (r + 1) * (r + 1) <= n:
        r += 1
    elif r * r > n:
        r -= 1
    return r
```

> **Rule of thumb:** In interviews, use `math.isqrt()` only if the interviewer
> says built-ins are OK. Otherwise, implement binary search or Newton's method.

---

## Pattern 2: Newton's Method (Heron's Method)

Iteratively improve an estimate of `sqrt(n)` using:

```
x_next = (x + n / x) / 2
```

### Why It Works

```
We want to find r such that r*r = n, i.e., f(r) = r*r - n = 0.

Newton's method for root-finding: x_next = x - f(x) / f'(x)
  f(x) = x*x - n
  f'(x) = 2*x
  x_next = x - (x*x - n) / (2*x)
         = (2*x*x - x*x + n) / (2*x)
         = (x + n/x) / 2

Intuition: If x is an overestimate of sqrt(n), then n/x is an underestimate.
Their average is closer to the true value. Moreover, Newton's method always
converges from above when starting from an overestimate, so we can use the
simple stopping condition x*x <= n.

Example: sqrt(50)
  x = 50    -> next = (50 + 50/50) / 2     = 25.5
  x = 25.5  -> next = (25.5 + 50/25.5) / 2 ~ 13.73
  x = 13.73 -> next ~ 8.69
  x = 8.69  -> next ~ 7.22
  x = 7.22  -> next ~ 7.07
  ...converges to 7.071...

Convergence is quadratic: each step roughly doubles the number
of correct digits. So even for enormous n, very few steps suffice.
```

### Implementation

```python
def sqrt_newton(n: int) -> int:
    """
    Integer square root using Newton's method.

    Time:  O(log log n) iterations (quadratic convergence), each O(1)
    Space: O(1)
    """
    if n < 2:
        return n

    # Start with an overestimate. For n >= 2, n itself is always an overestimate
    # because n >= sqrt(n) when n >= 1.
    x = n
    while x * x > n:
        x = (x + n // x) // 2  # integer division keeps us in int domain

    return x


# Tests
assert sqrt_newton(0) == 0
assert sqrt_newton(1) == 1
assert sqrt_newton(2) == 1
assert sqrt_newton(50) == 7
assert sqrt_newton(100) == 10
assert sqrt_newton(10**18) == 10**9
```

> **Why start with `x = n`?** It guarantees we start with an overestimate
> (since `n >= sqrt(n)` for `n >= 1`). Newton's method for sqrt always converges
> from above when starting with an overestimate, which makes the loop condition
> simple: stop when `x * x <= n`.

---

## Pattern 3: Divisor Enumeration up to sqrt(n)

A fundamental pattern: to find all divisors of `n`, only iterate up to
`sqrt(n)`. For each divisor `d` found, `n // d` is also a divisor.

```python
import math

def get_divisors(n: int) -> list[int]:
    """
    Return all divisors of n in sorted order.

    Key insight: divisors come in pairs (d, n//d) where d <= sqrt(n).
    We only need to iterate up to sqrt(n) and collect both sides.

    Time:  O(sqrt(n))
    Space: O(number of divisors) — typically O(n^epsilon) which is very small
    """
    if n <= 0:
        return []

    small = []   # divisors <= sqrt(n)
    large = []   # divisors > sqrt(n)

    d = 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d != n // d:  # avoid duplicate when d*d == n
                large.append(n // d)
        d += 1

    # small is already sorted ascending; large is in descending order
    return small + large[::-1]


# Tests
assert get_divisors(12) == [1, 2, 3, 4, 6, 12]
assert get_divisors(16) == [1, 2, 4, 8, 16]
assert get_divisors(7) == [1, 7]       # prime
assert get_divisors(1) == [1]


def count_divisors(n: int) -> int:
    """
    Count the number of divisors of n.

    Time:  O(sqrt(n))
    Space: O(1)
    """
    if n <= 0:
        return 0

    count = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            count += 1
            if d != n // d:
                count += 1
        d += 1

    return count


assert count_divisors(12) == 6   # 1,2,3,4,6,12
assert count_divisors(1) == 1
assert count_divisors(7) == 2    # prime: 1 and 7
```

---

## Practice Problems (Easy -> Medium -> Hard)

### Easy: Valid Perfect Square (LeetCode 367)

Check if a number is a perfect square without using the sqrt function.

```python
def isPerfectSquare(num: int) -> bool:
    """
    Check if num is a perfect square using binary search.

    Time:  O(log num)
    Space: O(1)
    """
    if num < 1:
        return False

    left, right = 1, num

    while left <= right:
        mid = (left + right) // 2
        square = mid * mid

        if square == num:
            return True
        elif square < num:
            left = mid + 1
        else:
            right = mid - 1

    return False


# Tests
assert isPerfectSquare(16) is True   # 4*4
assert isPerfectSquare(14) is False
assert isPerfectSquare(1) is True    # 1*1
assert isPerfectSquare(0) is False   # 0 is not in [1, inf) per LeetCode constraint
```

**Alternative — Odd Numbers Summation Property:**

The sum of the first k odd numbers equals `k*k`: `1 + 3 + 5 + ... + (2k-1) = k*k`.

```python
def isPerfectSquare_sum(num: int) -> bool:
    """
    Uses the identity: 1 + 3 + 5 + ... + (2k-1) = k*k.
    Subtract consecutive odd numbers. If we hit exactly 0, it's a perfect square.

    Time:  O(sqrt(num))
    Space: O(1)
    """
    odd = 1
    while num > 0:
        num -= odd
        odd += 2

    return num == 0
```

---

### Easy: Perfect Number (LeetCode 507)

A **perfect number** is a positive integer that equals the sum of its proper
divisors (divisors excluding itself). Use `sqrt(n)` to enumerate divisors
efficiently.

```python
def checkPerfectNumber(num: int) -> bool:
    """
    Check if num is a perfect number.

    Enumerate divisors up to sqrt(num). For each divisor d, both d and
    num // d are proper divisors (exclude num itself).

    Known perfect numbers: 6, 28, 496, 8128, 33550336, ...

    Time:  O(sqrt(num))
    Space: O(1)
    """
    if num <= 1:
        return False

    divisor_sum = 1  # 1 is always a proper divisor for num > 1
    d = 2
    while d * d <= num:
        if num % d == 0:
            divisor_sum += d
            if d != num // d:
                divisor_sum += num // d
        d += 1

    return divisor_sum == num


# Tests
assert checkPerfectNumber(6) is True      # 1 + 2 + 3 = 6
assert checkPerfectNumber(28) is True     # 1 + 2 + 4 + 7 + 14 = 28
assert checkPerfectNumber(496) is True
assert checkPerfectNumber(12) is False    # 1 + 2 + 3 + 4 + 6 = 16 != 12
assert checkPerfectNumber(1) is False
```

---

### Easy: Arranging Coins (LeetCode 441)

You have `n` coins to form a staircase. The k-th row has exactly k coins. Find
the number of complete rows.

```python
def arrangeCoins(n: int) -> int:
    """
    Find max k where 1 + 2 + ... + k <= n, i.e., k*(k+1)/2 <= n.

    Math solution using the quadratic formula:
      k*k + k - 2n <= 0  ->  k <= (-1 + sqrt(1 + 8n)) / 2

    We use math.isqrt to avoid float precision issues.

    Time:  O(1)
    Space: O(1)
    """
    import math
    # Use isqrt for precision safety with large n
    return (math.isqrt(8 * n + 1) - 1) // 2


def arrangeCoins_binary(n: int) -> int:
    """
    Binary search approach: find largest k where k*(k+1)/2 <= n.

    Time:  O(log n)
    Space: O(1)
    """
    left, right = 0, n
    result = 0

    while left <= right:
        mid = (left + right) // 2
        coins_needed = mid * (mid + 1) // 2

        if coins_needed <= n:
            result = mid
            left = mid + 1
        else:
            right = mid - 1

    return result


# Tests
assert arrangeCoins(5) == 2   # rows: 1+2=3 <= 5, but 1+2+3=6 > 5
assert arrangeCoins(8) == 3   # rows: 1+2+3=6 <= 8, but 1+2+3+4=10 > 8
assert arrangeCoins(1) == 1
assert arrangeCoins(0) == 0
```

---

### Easy: Count Primes (LeetCode 204)

Count the number of primes strictly less than `n`. The Sieve of Eratosthenes
only needs to mark multiples for primes up to `sqrt(n)`.

```python
def countPrimes(n: int) -> int:
    """
    Sieve of Eratosthenes.

    Key sqrt insight: if a composite number c < n has a prime factor p,
    then p <= sqrt(c) < sqrt(n). So we only sieve primes up to sqrt(n).

    When marking multiples of prime p, we start from p*p (not 2*p)
    because smaller multiples like 2*p, 3*p, ... were already marked
    by smaller primes.

    Time:  O(n log log n)  — harmonic sum of primes
    Space: O(n)
    """
    if n < 3:
        return 0

    # is_prime[i] = True means i is prime (initially all True)
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    # Only sieve up to sqrt(n)
    p = 2
    while p * p < n:
        if is_prime[p]:
            # Mark multiples of p starting from p*p
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False
        p += 1

    return sum(is_prime)


# Tests
assert countPrimes(10) == 4    # primes: 2, 3, 5, 7
assert countPrimes(0) == 0
assert countPrimes(1) == 0
assert countPrimes(2) == 0     # strictly less than 2
assert countPrimes(3) == 1     # just 2
assert countPrimes(20) == 8    # 2,3,5,7,11,13,17,19
```

---

### Medium: Sum of Square Numbers (LeetCode 633)

Given a non-negative integer `c`, determine whether there exist two integers
`a` and `b` such that `a*a + b*b = c`.

```python
def judgeSquareSum(c: int) -> bool:
    """
    Two-pointer approach:
      - a starts at 0 (smallest possible)
      - b starts at floor(sqrt(c)) (largest possible)
      - If a*a + b*b == c -> found
      - If too small -> increase a
      - If too large -> decrease b

    Why two pointers work: for a fixed a, we need b*b = c - a*a.
    As a increases, the required b decreases. So a and b move toward
    each other monotonically — classic two-pointer pattern.

    Time:  O(sqrt(c))
    Space: O(1)
    """
    import math

    a = 0
    b = math.isqrt(c)

    while a <= b:
        total = a * a + b * b
        if total == c:
            return True
        elif total < c:
            a += 1
        else:
            b -= 1

    return False


# Tests
assert judgeSquareSum(5) is True    # 1*1 + 2*2 = 5
assert judgeSquareSum(3) is False
assert judgeSquareSum(4) is True    # 0*0 + 2*2 = 4
assert judgeSquareSum(2) is True    # 1*1 + 1*1 = 2
assert judgeSquareSum(0) is True    # 0*0 + 0*0 = 0
```

---

### Medium: Perfect Squares (LeetCode 279)

Find the **least** number of perfect square numbers that sum to `n`.

**Approach 1 — DP (Bottom-Up):**

```python
def numSquares(n: int) -> int:
    """
    dp[i] = minimum number of perfect squares that sum to i.

    Transition: dp[i] = min(dp[i - j*j] + 1) for all j where j*j <= i.

    Intuition: To form sum i, we pick one perfect square j*j and
    then need dp[i - j*j] more squares for the remainder.

    Time:  O(n * sqrt(n)) — for each i up to n, we try O(sqrt(i)) squares
    Space: O(n)
    """
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1

    return dp[n]


# Tests
assert numSquares(12) == 3  # 4 + 4 + 4
assert numSquares(13) == 2  # 4 + 9
assert numSquares(1) == 1   # 1
assert numSquares(7) == 4   # 4 + 1 + 1 + 1
```

**Approach 2 — BFS (Often Faster in Practice):**

Think of it as a shortest-path problem: start at `n`, subtract any perfect
square to get a neighbor, and find the fewest hops to reach 0.

```python
from collections import deque

def numSquares_bfs(n: int) -> int:
    """
    BFS approach — treat as shortest path from n to 0.

    Each "level" of BFS = one more perfect square added.
    First time we reach 0 = minimum count.

    Time:  O(n * sqrt(n)) worst case
    Space: O(n)
    """
    if n == 0:
        return 0

    # Precompute all perfect squares <= n
    squares = []
    i = 1
    while i * i <= n:
        squares.append(i * i)
        i += 1

    queue = deque([n])
    visited = {n}
    level = 0

    while queue:
        level += 1
        for _ in range(len(queue)):
            curr = queue.popleft()
            for sq in squares:
                remainder = curr - sq
                if remainder == 0:
                    return level
                if remainder > 0 and remainder not in visited:
                    visited.add(remainder)
                    queue.append(remainder)

    return -1  # Unreachable: by Lagrange's four-square theorem, answer <= 4
```

> **Lagrange's four-square theorem:** Every positive integer can be expressed
> as the sum of at most four perfect squares. So the answer is always 1-4.

---

### Medium: Bulb Switcher (LeetCode 319)

There are `n` bulbs, all off initially. You perform `n` rounds: in round `i`,
toggle every `i`-th bulb. After `n` rounds, how many bulbs are on?

**Key insight:** Bulb `k` is toggled once for each of its divisors. A bulb
ends up ON only if it's toggled an odd number of times, which happens only when
`k` has an odd number of divisors — i.e., `k` is a perfect square (because
divisors pair up except when `d = k // d`).

```python
import math

def bulbSwitch(n: int) -> int:
    """
    Count bulbs that are ON after n rounds.

    Bulb k is ON iff k has an odd number of divisors, which happens
    iff k is a perfect square. So the answer is floor(sqrt(n)).

    Time:  O(1)
    Space: O(1)
    """
    return math.isqrt(n)


# Tests
assert bulbSwitch(3) == 1    # only bulb 1 (1*1) is on
assert bulbSwitch(0) == 0
assert bulbSwitch(1) == 1
assert bulbSwitch(10) == 3   # bulbs 1, 4, 9 are on
assert bulbSwitch(16) == 4   # bulbs 1, 4, 9, 16
```

---

### Hard: Kth Smallest Number in Multiplication Table (LeetCode 668)

Given an `m x n` multiplication table, find the k-th smallest number.

The table entry at row `i`, column `j` is `i * j`. We binary search on the
answer value and use `sqrt` reasoning: the counting function uses division per
row, similar to how divisor enumeration works.

```python
def findKthNumber(m: int, n: int, k: int) -> int:
    """
    Binary search on the answer.

    For a candidate value x, count how many entries in the table are <= x.
    Row i has entries i, 2i, 3i, ..., ni.
    Numbers <= x in row i: min(x // i, n).

    Find the smallest x where count(x) >= k.

    Why binary search works: the count function is monotonically non-decreasing
    in x. We want the first x where count(x) >= k. This x is guaranteed to
    exist in the table because we search over [1, m*n].

    Time:  O(m * log(m*n))
    Space: O(1)
    """
    def count_le(x: int) -> int:
        """Count how many entries in the m x n table are <= x."""
        total = 0
        for i in range(1, m + 1):
            total += min(x // i, n)
        return total

    left, right = 1, m * n

    while left < right:
        mid = (left + right) // 2
        if count_le(mid) >= k:
            right = mid
        else:
            left = mid + 1

    return left


# Tests
# Table 3x3: 1,2,3,2,4,6,3,6,9 -> sorted: 1,2,2,3,3,4,6,6,9
assert findKthNumber(3, 3, 5) == 3
assert findKthNumber(2, 3, 6) == 6
```

---

### Hard: Smallest Good Base (LeetCode 483)

For a given integer `n` (as a string), find the smallest base `k` such that
all digits of `n` in base `k` are 1s. That is, `n = 1 + k + k*k + ... + k^(m-1)`
for some `m >= 2`.

The key sqrt insight: for a fixed length `m`, we need `k^(m-1) <= n`, so
`k <= n^(1/(m-1))`. We binary search for `k` at each candidate `m`, and `m`
ranges from `log2(n)` down to 2.

```python
def smallestGoodBase(n: str) -> str:
    """
    Find smallest k >= 2 such that n = 1 + k + k*k + ... + k^(m-1).

    Strategy:
      - For each possible length m (from longest to shortest),
        binary search for k such that (k^m - 1) / (k - 1) = n.
      - The longest possible repunit has m = floor(log2(n)) + 1 digits
        (all 1s in base 2).
      - For a fixed m, the sum 1 + k + ... + k^(m-1) is strictly
        increasing in k, so binary search finds k if it exists.

    Float precision note: we use int(num ** (1.0 / (m - 1))) + 2 as the
    upper bound to guard against float rounding errors. The binary search
    handles the rest exactly using integer arithmetic.

    Time:  O(log^2(n))
    Space: O(1)
    """
    num = int(n)

    # m ranges from max possible (base 2 gives most digits) down to 2
    max_m = num.bit_length()  # floor(log2(num)) + 1

    for m in range(max_m, 1, -1):
        # k^(m-1) <= num, so k <= num^(1/(m-1))
        # Use +2 to guard against float imprecision for large num
        lo = 2
        hi = int(num ** (1.0 / (m - 1))) + 2

        while lo <= hi:
            mid = (lo + hi) // 2

            # Compute 1 + mid + mid*mid + ... + mid^(m-1) using a loop
            # to avoid floating-point issues with the closed form
            total = 0
            power = 1
            for _ in range(m):
                total += power
                power *= mid

            if total == num:
                return str(mid)
            elif total < num:
                lo = mid + 1
            else:
                hi = mid - 1

    # m = 2: n = 1 + k -> k = n - 1 always works
    return str(num - 1)


# Tests
assert smallestGoodBase("13") == "3"   # 13 = 1 + 3 + 9 = 111 in base 3
assert smallestGoodBase("4681") == "8" # 4681 = 1+8+64+512+4096 = 11111 in base 8
assert smallestGoodBase("3") == "2"    # 3 = 1 + 2 = 11 in base 2
```

---

### Hard: Count Primes in Range Using Segmented Sieve

When you need primes in a large range `[lo, hi]` where `hi` can be up to `10^12`
but `hi - lo` is small (e.g., `<= 10^6`), use a **segmented sieve**. The key
insight is that any composite number `<= hi` has a prime factor `<= sqrt(hi)`.

```python
def count_primes_in_range(lo: int, hi: int) -> int:
    """
    Count primes in [lo, hi] using a segmented sieve.

    Step 1: Find all primes up to sqrt(hi) using a standard sieve.
    Step 2: Use those primes to mark composites in [lo, hi].

    This works for very large ranges (e.g., hi ~ 10^12) as long as
    hi - lo fits in memory.

    Time:  O(sqrt(hi) * log(log(hi)) + (hi - lo) * log(log(hi)))
    Space: O(sqrt(hi) + (hi - lo))
    """
    import math

    if hi < 2:
        return 0
    lo = max(lo, 2)
    if lo > hi:
        return 0

    # Step 1: small primes up to sqrt(hi)
    limit = math.isqrt(hi) + 1
    is_small_prime = [True] * (limit + 1)
    is_small_prime[0] = is_small_prime[1] = False
    p = 2
    while p * p <= limit:
        if is_small_prime[p]:
            for j in range(p * p, limit + 1, p):
                is_small_prime[j] = False
        p += 1
    small_primes = [p for p in range(2, limit + 1) if is_small_prime[p]]

    # Step 2: sieve the range [lo, hi]
    size = hi - lo + 1
    is_prime_seg = [True] * size  # is_prime_seg[i] represents lo + i

    for p in small_primes:
        # First multiple of p that is >= lo
        start = ((lo + p - 1) // p) * p
        if start == p:
            start += p  # don't mark p itself as composite
        for j in range(start, hi + 1, p):
            is_prime_seg[j - lo] = False

    return sum(is_prime_seg)


# Tests
assert count_primes_in_range(1, 10) == 4       # 2, 3, 5, 7
assert count_primes_in_range(10, 20) == 4      # 11, 13, 17, 19
assert count_primes_in_range(2, 2) == 1        # 2 is prime
assert count_primes_in_range(100, 110) == 4    # 101, 103, 107, 109
```

---

## Utility Patterns

### Count Perfect Squares in a Range

```python
import math

def count_perfect_squares(low: int, high: int) -> int:
    """
    Count perfect squares in [low, high].

    Uses math.isqrt for precision (avoids float rounding issues).

    The number of perfect squares in [1, n] is floor(sqrt(n)).
    For a range [low, high], it's floor(sqrt(high)) - floor(sqrt(low - 1)).

    Time:  O(1)
    Space: O(1)
    """
    if low > high or high < 0:
        return 0

    # Smallest integer whose square is >= low
    sqrt_low = math.isqrt(max(low, 0))
    if sqrt_low * sqrt_low < low:
        sqrt_low += 1

    # Largest integer whose square is <= high
    sqrt_high = math.isqrt(high)

    if sqrt_low > sqrt_high:
        return 0
    return sqrt_high - sqrt_low + 1


# Tests
assert count_perfect_squares(1, 100) == 10   # 1,4,9,16,25,36,49,64,81,100
assert count_perfect_squares(10, 20) == 1    # 16 only
assert count_perfect_squares(50, 50) == 0    # 50 is not a perfect square
assert count_perfect_squares(49, 49) == 1    # 49 = 7*7
assert count_perfect_squares(0, 0) == 1      # 0 = 0*0
```

### Power of N Check

```python
def is_power_of_n(num: int, n: int) -> bool:
    """
    Check if num = n^k for some integer k >= 0.

    Repeatedly divide by n. If we reach 1, it's a power of n.

    Edge cases:
      - num <= 0: False (we only consider positive powers)
      - n <= 1: special — n=1 means only num=1 works (1^k = 1 for all k)
      - num = 1: True for any valid n (n^0 = 1)

    Time:  O(log_n(num))
    Space: O(1)
    """
    if num <= 0:
        return False
    if num == 1:
        return True  # n^0 = 1 for any n >= 1
    if n <= 1:
        return False  # n=0 or n=1 can never produce num > 1

    while num % n == 0:
        num //= n

    return num == 1


assert is_power_of_n(27, 3) is True   # 3^3
assert is_power_of_n(16, 4) is True   # 4^2
assert is_power_of_n(10, 3) is False
assert is_power_of_n(1, 7) is True    # 7^0
assert is_power_of_n(1, 1) is True    # 1^k = 1
assert is_power_of_n(2, 1) is False   # 1^k is always 1, never 2
```

### Integer k-th Root

Useful when problems need roots other than square root (e.g., Smallest Good Base).

```python
def integer_kth_root(n: int, k: int) -> int:
    """
    Compute floor(n^(1/k)) using binary search.

    Avoids float precision issues that plague n ** (1.0 / k).

    Time:  O(k * log(n))  — k for the pow check at each binary search step
    Space: O(1)
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if k <= 0:
        raise ValueError("k must be positive")
    if n <= 1:
        return n

    # Upper bound: for k >= 2, n^(1/k) <= n.
    # Tighter bound: use float estimate + padding
    lo, hi = 1, int(n ** (1.0 / k)) + 2

    # Expand hi if our float estimate was too low
    while hi ** k < n:
        hi *= 2

    result = 1
    while lo <= hi:
        mid = (lo + hi) // 2
        power = mid ** k
        if power <= n:
            result = mid
            lo = mid + 1
        else:
            hi = mid - 1

    return result


# Tests
assert integer_kth_root(27, 3) == 3
assert integer_kth_root(26, 3) == 2
assert integer_kth_root(16, 4) == 2
assert integer_kth_root(10**18, 2) == 10**9
assert integer_kth_root(10**18, 3) == 10**6
assert integer_kth_root(0, 5) == 0
assert integer_kth_root(1, 10) == 1
```

---

## Complexity Summary

| Algorithm                    | Time             | Space | Notes                                    |
| ---------------------------- | ---------------- | ----- | ---------------------------------------- |
| Binary search sqrt           | O(log n)         | O(1)  | Most common in interviews                |
| Newton's method              | O(log log n)     | O(1)  | Quadratic convergence, very fast         |
| Perfect square check         | O(log n)         | O(1)  | Binary search variant                    |
| Odd-number summation check   | O(sqrt(n))       | O(1)  | 1+3+5+...+(2k-1) = k*k                  |
| Sum of squares (two-pointer) | O(sqrt(n))       | O(1)  | a*a + b*b = c                            |
| Divisor enumeration          | O(sqrt(n))       | O(1)  | Pair divisors: d and n//d                |
| Sieve of Eratosthenes        | O(n log log n)   | O(n)  | Only sieve up to sqrt(n)                 |
| numSquares (DP)              | O(n * sqrt(n))   | O(n)  | By Lagrange's theorem, answer is 1-4     |
| Kth in multiplication table  | O(m * log(m*n))  | O(1)  | Binary search on answer + linear count   |
| Segmented sieve              | O((hi-lo) loglog)| O(hi-lo) | Large ranges with small windows       |

---

## Edge Cases Checklist

1. **n = 0**: `sqrt(0) = 0`
2. **n = 1**: `sqrt(1) = 1`
3. **n = 2 or 3**: sqrt rounds down to 1
4. **Large n**: In Python, integers are arbitrary precision, so `mid * mid`
   never overflows. In C++/Java, use `mid <= n / mid` to avoid overflow.
5. **Perfect squares**: Must return the exact integer root
6. **Negative input**: Undefined for real sqrt — reject or return 0
7. **n between perfect squares** (e.g., `n = 8`): Must floor correctly to 2
8. **Float precision for large n**: `int(math.sqrt(n))` can be off by 1 for
   `n > 2^53` — always verify with integer multiplication or use `math.isqrt`

---

## Interview Tips

1. **Start with binary search** — most interviewers expect this approach
2. **Mention Newton's method** — shows mathematical maturity; ask if they want
   to see it
3. **Handle edge cases explicitly** — 0, 1, and very large numbers
4. **Watch for overflow in other languages** — `mid * mid` can overflow int32/int64
   in C++/Java. Use `mid <= n / mid` instead. (Not an issue in Python.)
5. **Know `math.isqrt`** — Python 3.8+ has it; mention it but don't rely on it
   unless told built-ins are OK
6. **Recognize divisor enumeration** — whenever a problem involves divisors,
   factors, or "pairs that multiply to n", think `sqrt(n)` immediately

### Overflow-Safe Pattern (for C++/Java, shown in Python for reference)

```python
def mySqrt_safe(x: int) -> int:
    """
    Overflow-safe version using division instead of multiplication.

    In C++/Java, mid * mid can overflow. Instead, compare mid with x // mid.

    Note: In Python, this is unnecessary (arbitrary precision ints),
    but good to know for interviews in other languages.

    Time:  O(log x)
    Space: O(1)
    """
    if x < 2:
        return x

    left, right = 1, x // 2
    result = 1

    while left <= right:
        mid = (left + right) // 2

        # Use division to avoid overflow: mid*mid <= x  <=>  mid <= x // mid
        # (when mid > 0 and we account for integer division rounding)
        if mid <= x // mid:
            result = mid
            left = mid + 1
        else:
            right = mid - 1

    return result
```

---

## Common Pitfalls

```python
import math

n = 10**18 + 7  # example large number

# WRONG: Can be off by 1 due to float precision for large n
result = int(math.sqrt(n))

# SAFER: Verify the result with integer arithmetic
result = int(math.sqrt(n))
if (result + 1) * (result + 1) <= n:
    result += 1
elif result * result > n:
    result -= 1

# BEST: Use math.isqrt (Python 3.8+) — always correct
result = math.isqrt(n)
```

---

## When NOT to Roll Your Own Sqrt

1. **Python 3.8+ exists**: Use `math.isqrt()` — it's exact and fast (C-level)
2. **Floating point is fine**: Use `math.sqrt()` when approximate answers suffice
3. **Small numbers**: For n < 1000, even a linear scan works fine
4. **Precision concerns**: `int(math.sqrt(n))` can be off by 1 for large n —
   always verify with multiplication if you go this route

---

## Practice Problems Summary

| #   | Problem                              | Difficulty | Key Concept                        | LeetCode |
| --- | ------------------------------------ | ---------- | ---------------------------------- | -------- |
| 1   | Sqrt(x)                              | Easy       | Binary search on answer            | 69       |
| 2   | Valid Perfect Square                 | Easy       | Binary search or odd-number sum    | 367      |
| 3   | Perfect Number                       | Easy       | Divisor enumeration up to sqrt     | 507      |
| 4   | Arranging Coins                      | Easy       | Binary search or quadratic formula | 441      |
| 5   | Count Primes                         | Medium     | Sieve of Eratosthenes, sqrt bound  | 204      |
| 6   | Sum of Square Numbers                | Medium     | Two pointers + sqrt bound          | 633      |
| 7   | Perfect Squares                      | Medium     | DP or BFS, Lagrange's theorem      | 279      |
| 8   | Bulb Switcher                        | Medium     | Divisor count parity = sqrt        | 319      |
| 9   | Kth Smallest in Multiplication Table | Hard       | Binary search + counting function  | 668      |
| 10  | Smallest Good Base                   | Hard       | Binary search + number theory      | 483      |

---

## Related Sections

- [Binary Search](../10-binary-search/README.md) — Foundation technique
- [Number Properties](./06-number-properties.md) — Related math patterns
