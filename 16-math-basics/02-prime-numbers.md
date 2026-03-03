# Prime Numbers

> **Prerequisites:** [GCD and LCM](./01-gcd-lcm.md) (helpful for understanding coprimality)

## Building Intuition

**The "Indivisible Atoms" Mental Model**

A **prime number** is an integer greater than 1 whose only divisors are 1 and itself. Primes are the "atoms" of numbers — they can't be broken down further:

- 12 = 2 × 2 × 3 (composite — built from prime atoms)
- 7 = 7 (prime — indivisible)
- 1 is **not** prime (by convention, to keep the Fundamental Theorem unique)

Every integer > 1 is either prime or a **unique** product of primes (ignoring order). This is the **Fundamental Theorem of Arithmetic**, and it's why primes matter — they're the building blocks of all numbers.

**Why Check Only Up to √n**

If n = a × b and both a, b > √n, then a × b > n — a contradiction. So at least one factor must be ≤ √n:

- 100 = 10 × 10 → √100 = 10
- 100 = 4 × 25 → one factor (4) is below √100

So if no factor exists in [2, √n], then n is prime.

**The 6k ± 1 Optimization**

All primes greater than 3 are of the form 6k ± 1. Here's why — every integer falls into one of six residue classes mod 6:

- 6k is divisible by 2 and 3 (not prime for k ≥ 1)
- 6k + 2 is divisible by 2
- 6k + 3 is divisible by 3
- 6k + 4 is divisible by 2
- Only **6k + 1** and **6k + 5** (equivalently 6k − 1) can be prime

This lets us skip 4 out of every 6 candidates, checking only 2 per group of 6.

---

## Interview Context

Prime number problems test mathematical reasoning and optimization skills. Common scenarios:

- **Primality testing**: Is a single number prime?
- **Counting/enumerating primes**: Find all primes up to n
- **Prime factorization**: Decompose a number into its prime factors
- **Constrained factor problems**: Ugly numbers, super ugly numbers
- **Number theory applications**: GCD, LCM, coprimality, divisor counting

The **Sieve of Eratosthenes** is the most important algorithm to know — it appears frequently and is far more efficient than checking each number individually.

---

## Pattern: Trial Division (Primality Check)

To check if `n` is prime, test divisibility by integers from 2 up to √n.

### Why √n is Sufficient (Proof)

```
If n = a × b where a ≤ b, then:
  a ≤ b
  a × a ≤ a × b = n
  a ≤ √n

So every composite n has at least one factor in [2, √n].
Checking only up to √n reduces O(n) checks to O(√n).
```

### Visual Example

```
Is 29 prime?

√29 ≈ 5.4, so check divisors 2, 3, 4, 5:
  29 % 2 = 1  ✗ (not divisible)
  29 % 3 = 2  ✗
  (skip 4 — if divisible by 4, already caught by 2)
  29 % 5 = 4  ✗

No divisors found → 29 is prime ✓
```

---

## Implementation

### Basic Primality Check

```python
def is_prime(n: int) -> bool:
    """
    Check if n is prime using trial division with 6k ± 1 optimization.

    Time: O(√n)
    Space: O(1)
    """
    if n < 2:
        return False
    if n < 4:
        return True  # 2 and 3 are prime
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Check 6k ± 1 pattern: all primes > 3 are of the form 6k ± 1.
    # Start at i = 5, check i (6k-1) and i+2 (6k+1), then jump by 6.
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


# Test
print(is_prime(2))    # True
print(is_prime(17))   # True
print(is_prime(1))    # False
print(is_prime(4))    # False
print(is_prime(97))   # True
print(is_prime(25))   # False (5 × 5)
```

### Why the 6k ± 1 Loop Works

```
All integers fall into one of six residue classes mod 6:

  6k     → divisible by 2 and 3 (never prime, k ≥ 1)
  6k + 1 → possible prime ✓
  6k + 2 → divisible by 2
  6k + 3 → divisible by 3
  6k + 4 → divisible by 2
  6k + 5 → possible prime ✓  (same as 6k − 1)

After handling 2 and 3 as special cases, we only check:
  i = 5, 11, 17, 23, ...  (6k − 1 values)
  i + 2 = 7, 13, 19, 25, ...  (6k + 1 values)

We start at i = 5 and increment by 6 each iteration,
checking both i and i + 2. This skips ~2/3 of candidates.
```

---

## Pattern: Sieve of Eratosthenes

The sieve efficiently finds **all** primes up to n. Instead of checking each number individually (O(n√n) total), it eliminates composites by marking multiples — much faster at O(n log log n).

**Key insight**: If p is prime, then 2p, 3p, 4p, ... are all composite. Mark them all in one pass. We can even start marking from p² because smaller multiples (2p, 3p, ..., (p-1)p) were already marked by smaller primes.

### Algorithm Visualization

```
Find all primes ≤ 30:

Initial: [F F T T T T T T T T T T T T T T T T T T T T T T T T T T T T T]
Index:    0 1 2 3 4 5 6 7 8 9 ...

Mark multiples of 2 (from 4):
[F F T T F T F T F T F T F T F T F T F T F T F T F T F T F T F]

Mark multiples of 3 (from 9):
[F F T T F T F T F F F T F T F F F T F T F F F T F T F F F T F]

Mark multiples of 5 (from 25):
[F F T T F T F T F F F T F T F F F T F T F F F T F F F F F T F]

√30 ≈ 5.5, so we stop here. Remaining T's are prime:
Primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
```

### Why Start Marking from i² (Not 2i)

When sieving with prime p, all multiples kp where k < p have already been handled:
- 2p was marked when we processed prime 2
- 3p was marked when we processed prime 3
- ...and so on up to (p-1)p

So the first unmarked multiple of p is p × p = p².

### Implementation

```python
def sieve_of_eratosthenes(n: int) -> list[int]:
    """
    Find all primes up to n (inclusive) using Sieve of Eratosthenes.

    Time: O(n log log n) — nearly linear
    Space: O(n)
    """
    if n < 2:
        return []

    # is_prime[i] = True means i is (potentially) prime
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    # Only need to sieve up to √n
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            # Mark multiples of i starting from i² (smaller multiples already marked)
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return [i for i in range(n + 1) if is_prime[i]]


# Test
print(sieve_of_eratosthenes(30))
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
print(sieve_of_eratosthenes(1))   # []
print(sieve_of_eratosthenes(2))   # [2]
```

---

## Pattern: Prime Factorization

Decompose n into its prime factors. The approach: divide out the smallest prime repeatedly, then move to the next candidate.

```python
def prime_factors(n: int) -> list[int]:
    """
    Return all prime factors of n (with repetition), in ascending order.

    Example: prime_factors(12) → [2, 2, 3]

    Time: O(√n) — we only check divisors up to √n
    Space: O(log n) — a number has at most log₂(n) prime factors
    """
    if n < 2:
        return []  # 0, 1, and negatives have no prime factorization

    factors = []

    # Extract all factors of 2 first
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Now n is odd — check odd candidates 3, 5, 7, ... up to √n
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2

    # If n > 1, whatever remains is a prime factor (the largest one)
    if n > 1:
        factors.append(n)

    return factors


# Test
print(prime_factors(12))    # [2, 2, 3]
print(prime_factors(100))   # [2, 2, 5, 5]
print(prime_factors(17))    # [17]
print(prime_factors(1))     # []
print(prime_factors(0))     # []
print(prime_factors(360))   # [2, 2, 2, 3, 3, 5]
```

### Unique Prime Factors with Counts

```python
from collections import Counter


def prime_factor_counts(n: int) -> dict[int, int]:
    """
    Return prime factors mapped to their exponents.

    Time: O(√n)
    Space: O(log n)
    """
    return dict(Counter(prime_factors(n)))


print(prime_factor_counts(360))  # {2: 3, 3: 2, 5: 1}
# 360 = 2³ × 3² × 5¹
```

---

## Complexity Analysis

| Algorithm             | Time           | Space    | Use Case                            |
| --------------------- | -------------- | -------- | ----------------------------------- |
| Trial division        | O(√n)          | O(1)     | Single primality check              |
| Trial division (6k±1) | O(√n / 3)      | O(1)     | Optimized single check              |
| Sieve of Eratosthenes | O(n log log n) | O(n)     | All primes up to n                  |
| Prime factorization   | O(√n)          | O(log n) | Decompose one number                |
| SPF sieve + factorize | O(n log log n) + O(log n) per query | O(n)     | Factor many numbers ≤ n |

### When to Use Each

```
Single primality check:
  n ≤ 10^12   → Trial division with 6k±1 (fast enough)
  n > 10^12   → Miller-Rabin probabilistic test

Many primality checks or "count primes ≤ n":
  → Sieve of Eratosthenes

Factor one number:
  → Trial division factorization O(√n)

Factor many numbers ≤ n:
  → Build SPF sieve once, then factorize each in O(log n)
```

---

## Common Variations

### 1. Check if Power of Prime

```python
def is_power_of_prime(n: int) -> bool:
    """Check if n = p^k for some prime p and k ≥ 1."""
    if n < 2:
        return False

    # Find smallest prime factor
    for p in range(2, int(n**0.5) + 1):
        if n % p == 0:
            # Keep dividing by p — if n reduces to 1, it was p^k
            while n % p == 0:
                n //= p
            return n == 1

    # n itself is prime (p^1)
    return True


print(is_power_of_prime(8))   # True (2³)
print(is_power_of_prime(12))  # False (2² × 3)
print(is_power_of_prime(17))  # True (17¹)
print(is_power_of_prime(1))   # False
```

### 2. Count Divisors

```python
def count_divisors(n: int) -> int:
    """
    Count total divisors using prime factorization.
    If n = p1^a1 * p2^a2 * ..., count = (a1+1)(a2+1)...

    Intuition: each divisor is formed by choosing an exponent for each
    prime factor (from 0 up to ai), so the count is the product of choices.

    Time: O(√n)
    Space: O(1)
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1

    count = 1

    # Handle factor of 2
    power = 0
    while n % 2 == 0:
        power += 1
        n //= 2
    count *= (power + 1)

    # Handle odd factors
    i = 3
    while i * i <= n:
        power = 0
        while n % i == 0:
            power += 1
            n //= i
        count *= (power + 1)
        i += 2

    # Remaining prime factor (exponent = 1)
    if n > 1:
        count *= 2  # (1 + 1) for this prime

    return count


print(count_divisors(12))  # 6 (divisors: 1, 2, 3, 4, 6, 12)
print(count_divisors(36))  # 9 (divisors: 1, 2, 3, 4, 6, 9, 12, 18, 36)
print(count_divisors(1))   # 1
print(count_divisors(7))   # 2 (1, 7)
```

### 3. Smallest Prime Factor (SPF) Sieve

When you need to factorize **many** numbers ≤ n, build an SPF table once, then factorize any number in O(log n) by repeatedly dividing by its smallest prime factor.

```python
def smallest_prime_factor_sieve(n: int) -> list[int]:
    """
    Build SPF array: spf[i] = smallest prime factor of i.

    Time: O(n log log n) to build
    Space: O(n)
    """
    spf = list(range(n + 1))  # spf[i] = i initially (assumes i is prime)

    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:  # i is prime (not yet marked by a smaller prime)
            for j in range(i * i, n + 1, i):
                if spf[j] == j:  # Only update if not already marked
                    spf[j] = i

    return spf


def factorize_with_spf(n: int, spf: list[int]) -> list[int]:
    """Factorize n in O(log n) using precomputed SPF table."""
    factors = []
    while n > 1:
        factors.append(spf[n])
        n //= spf[n]
    return factors


# Build once, factorize many
spf = smallest_prime_factor_sieve(100)
print(factorize_with_spf(60, spf))   # [2, 2, 3, 5]
print(factorize_with_spf(97, spf))   # [97]
print(factorize_with_spf(84, spf))   # [2, 2, 3, 7]
```

---

## Edge Cases

1. **0 and 1**: Not prime (primes must be > 1)
2. **2**: The only even prime — always handle before the odd-number loop
3. **Negative numbers**: Primes are positive by definition
4. **Large primes (n > 10¹²)**: Trial division becomes slow; use Miller-Rabin
5. **n = 0 or 1 in factorization**: Return empty list (no prime factors)
6. **n = 0 in factorization loops**: Guard against infinite loop (`while n % 2 == 0` never terminates for n = 0)
7. **Perfect squares**: √n is exact, so use `i * i <= n` (not `i <= sqrt(n)` which has float issues)

---

## Interview Tips

1. **Memorize the 6k±1 optimization**: Shows mathematical sophistication beyond basic trial division
2. **Know the sieve complexity**: O(n log log n) — nearly linear, not O(n√n) or O(n²)
3. **Explain why marking starts from i²**: Shows you understand the optimization, not just memorized code
4. **Mention space-time tradeoff**: Sieve uses O(n) space; for n = 10⁹ that's ~1 GB, so consider segmented sieve
5. **Use `i * i <= n` not `i <= math.sqrt(n)`**: Avoids floating-point precision issues
6. **Python has no built-in `is_prime()`**: `sympy.isprime()` exists but won't be available in interviews
7. **Guard edge cases first**: Always handle n < 2 at the top of prime functions to avoid infinite loops and wrong results

---

## Practice Problems (Progressive Difficulty)

### Easy: Count Primes (LeetCode 204)

Given an integer n, return the number of primes strictly less than n.

**Approach**: Sieve of Eratosthenes up to n-1. Note the problem asks for primes **strictly less than** n, so the sieve array size is `n` (indices 0 to n-1).

```python
def countPrimes(n: int) -> int:
    """
    Count primes strictly less than n using Sieve of Eratosthenes.

    Time: O(n log log n)
    Space: O(n)
    """
    if n < 3:
        return 0

    is_prime = [True] * n  # indices 0..n-1
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            # Mark multiples starting from i²
            for j in range(i * i, n, i):
                is_prime[j] = False

    return sum(is_prime)


# Test
print(countPrimes(10))   # 4 (primes: 2, 3, 5, 7)
print(countPrimes(0))    # 0
print(countPrimes(1))    # 0
print(countPrimes(2))    # 0 (no primes strictly less than 2)
print(countPrimes(3))    # 1 (prime 2)
print(countPrimes(100))  # 25
```

### Easy: Ugly Number (LeetCode 263)

An ugly number is a positive integer whose **only** prime factors are 2, 3, and 5. The idea: divide out all 2s, 3s, and 5s — if you're left with 1, no other primes were involved.

```python
def isUgly(n: int) -> bool:
    """
    Check if n is an ugly number.

    Time: O(log n) — each division at least halves n
    Space: O(1)
    """
    if n <= 0:
        return False

    for prime in [2, 3, 5]:
        while n % prime == 0:
            n //= prime

    # If n == 1, only 2/3/5 were factors. Otherwise some other prime remains.
    return n == 1


# Test
print(isUgly(6))    # True  (2 × 3)
print(isUgly(8))    # True  (2³)
print(isUgly(14))   # False (2 × 7 — 7 is not an allowed factor)
print(isUgly(1))    # True  (no prime factors at all — vacuously ugly)
print(isUgly(0))    # False (not positive)
```

### Easy: Perfect Number (LeetCode 507)

A perfect number equals the sum of its proper divisors (all positive divisors excluding the number itself). Check if n is perfect.

**Approach**: Iterate divisors up to √n. For each divisor `i`, both `i` and `n // i` are divisors. This avoids checking all numbers up to n.

```python
def checkPerfectNumber(num: int) -> bool:
    """
    Check if num is a perfect number.

    Time: O(√n)
    Space: O(1)
    """
    if num <= 1:
        return False

    divisor_sum = 1  # 1 is always a proper divisor (for num > 1)
    i = 2
    while i * i <= num:
        if num % i == 0:
            divisor_sum += i
            if i != num // i:  # Avoid counting √num twice
                divisor_sum += num // i
        i += 1

    return divisor_sum == num


# Test
print(checkPerfectNumber(28))   # True: 1 + 2 + 4 + 7 + 14 = 28
print(checkPerfectNumber(6))    # True: 1 + 2 + 3 = 6
print(checkPerfectNumber(496))  # True
print(checkPerfectNumber(12))   # False: 1 + 2 + 3 + 4 + 6 = 16 ≠ 12
print(checkPerfectNumber(1))    # False
```

### Easy: Happy Number (LeetCode 202)

A happy number is defined by repeatedly replacing it with the sum of squares of its digits. If the process reaches 1, it's happy; otherwise it loops forever.

**Connection to number theory**: This problem uses cycle detection (Floyd's algorithm) — the same technique used in Pollard's rho factorization algorithm. The digit-square-sum function maps integers to integers; if we never reach 1, we must enter a cycle (since the output is bounded).

```python
def isHappy(n: int) -> bool:
    """
    Check if n is a happy number using Floyd's cycle detection.

    Time: O(log n) — the digit square sum of a d-digit number is at most
          81d, which is much smaller than n, so the sequence quickly enters
          a small range and either reaches 1 or cycles.
    Space: O(1)
    """
    def digit_square_sum(num: int) -> int:
        total = 0
        while num > 0:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total

    # Floyd's tortoise and hare
    slow = n
    fast = digit_square_sum(n)

    while fast != 1 and slow != fast:
        slow = digit_square_sum(slow)                    # 1 step
        fast = digit_square_sum(digit_square_sum(fast))   # 2 steps

    return fast == 1


# Test
print(isHappy(19))  # True: 1²+9²=82 → 8²+2²=68 → 6²+8²=100 → 1²+0²+0²=1
print(isHappy(2))   # False (enters a cycle: 2→4→16→37→58→89→145→42→20→4→...)
print(isHappy(1))   # True
```

### Medium: Ugly Number II (LeetCode 264)

Find the nth ugly number (factors limited to 2, 3, 5).

**Approach**: Every ugly number is 2×, 3×, or 5× some smaller ugly number. We generate them in sorted order using three pointers — each pointer tracks which ugly number its prime should multiply next.

```python
def nthUglyNumber(n: int) -> int:
    """
    Three-pointer approach to generate ugly numbers in order.

    Time: O(n)
    Space: O(n)
    """
    ugly = [0] * n
    ugly[0] = 1

    # Pointers: index into ugly[] for each prime factor
    i2 = i3 = i5 = 0

    for i in range(1, n):
        next2 = ugly[i2] * 2
        next3 = ugly[i3] * 3
        next5 = ugly[i5] * 5

        ugly[i] = min(next2, next3, next5)

        # Advance ALL pointers that match (handles duplicates like 6 = 2×3 = 3×2)
        if ugly[i] == next2:
            i2 += 1
        if ugly[i] == next3:
            i3 += 1
        if ugly[i] == next5:
            i5 += 1

    return ugly[n - 1]


# Test
print(nthUglyNumber(10))   # 12 → sequence: [1, 2, 3, 4, 5, 6, 8, 9, 10, 12]
print(nthUglyNumber(1))    # 1
print(nthUglyNumber(15))   # 24
```

### Medium: Super Ugly Number (LeetCode 313)

Find the nth super ugly number. Super ugly numbers are positive integers whose **all** prime factors are in a given list of primes.

**Approach**: Generalization of Ugly Number II. Maintain a sorted sequence of ugly numbers. For each prime, track a pointer into the sequence — the next ugly number to multiply by that prime. At each step, pick the minimum candidate.

```python
def nthSuperUglyNumber(n: int, primes: list[int]) -> int:
    """
    Find the nth super ugly number.

    Time: O(n × k) where k = len(primes)
    Space: O(n + k)
    """
    ugly = [0] * n
    ugly[0] = 1

    # indices[j] = position in ugly[] that primes[j] should multiply next
    indices = [0] * len(primes)
    # next_vals[j] = ugly[indices[j]] * primes[j]
    next_vals = list(primes)

    for i in range(1, n):
        ugly[i] = min(next_vals)

        # Advance ALL primes that produced this minimum (avoids duplicates)
        for j in range(len(primes)):
            if next_vals[j] == ugly[i]:
                indices[j] += 1
                next_vals[j] = ugly[indices[j]] * primes[j]

    return ugly[n - 1]


# Test
print(nthSuperUglyNumber(12, [2, 7, 13, 19]))
# 32 → sequence: [1, 2, 4, 7, 8, 13, 14, 16, 19, 26, 28, 32]
```

### Medium: Four Divisors (LeetCode 1390)

Given an array of integers, return the sum of divisors of each element that has exactly 4 divisors. If no such element exists, return 0.

**Key insight**: A number with exactly 4 divisors is either:
- p × q (two distinct primes) → divisors: 1, p, q, pq
- p³ (prime cubed) → divisors: 1, p, p², p³

```python
def sumFourDivisors(nums: list[int]) -> int:
    """
    For each number, count its divisors by iterating up to √num.
    If exactly 4, add their sum to the result.

    Time: O(m × √max_val) where m = len(nums)
    Space: O(1)
    """
    total = 0

    for num in nums:
        divisor_sum = 0
        count = 0

        i = 1
        while i * i <= num:
            if num % i == 0:
                count += 1
                divisor_sum += i
                if i != num // i:
                    count += 1
                    divisor_sum += num // i
            if count > 4:  # Early exit: already too many divisors
                break
            i += 1

        if count == 4:
            total += divisor_sum

    return total


# Test
print(sumFourDivisors([21, 4, 7]))
# 32 → only 21 has 4 divisors (1, 3, 7, 21), sum = 32
#       4 has 3 divisors (1, 2, 4), 7 has 2 divisors (1, 7)
print(sumFourDivisors([1, 2, 3, 4, 5]))  # 0 (none have exactly 4 divisors)
print(sumFourDivisors([21, 21]))          # 64 (each 21 contributes 32)
```

### Medium: Closest Prime Numbers in Range (LeetCode 2523)

Given two integers left and right, find the two prime numbers num1 and num2 where left ≤ num1 < num2 ≤ right, and num2 - num1 is minimized. Return [-1, -1] if fewer than 2 primes exist in range.

**Approach**: Sieve all primes up to `right`, then scan for the closest consecutive pair in the range.

```python
def closestPrimes(left: int, right: int) -> list[int]:
    """
    Sieve to find all primes in [left, right], then find closest pair.

    Time: O(n log log n) where n = right
    Space: O(n)
    """
    if right < 2:
        return [-1, -1]

    # Build sieve up to right
    is_prime = [True] * (right + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(right**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, right + 1, i):
                is_prime[j] = False

    # Collect primes in range [left, right]
    primes = [i for i in range(max(left, 2), right + 1) if is_prime[i]]

    if len(primes) < 2:
        return [-1, -1]

    # Find closest consecutive pair
    best = [primes[0], primes[1]]
    for i in range(1, len(primes) - 1):
        if primes[i + 1] - primes[i] < best[1] - best[0]:
            best = [primes[i], primes[i + 1]]

    return best


# Test
print(closestPrimes(10, 19))  # [11, 13]
print(closestPrimes(4, 6))    # [-1, -1] (only 1 prime in range: 5)
print(closestPrimes(1, 1))    # [-1, -1]
```

### Medium: Count the Number of K-Big Indices (Euler's Totient — Related Pattern)

Euler's totient function φ(n) counts integers in [1, n] that are coprime with n. It's computed from the prime factorization:

φ(n) = n × ∏(1 - 1/p) for each distinct prime factor p of n.

This pattern appears in problems involving coprimality and modular inverses.

```python
def euler_totient(n: int) -> int:
    """
    Compute Euler's totient function φ(n).

    φ(n) = count of integers in [1, n] coprime to n.
    Uses the product formula: φ(n) = n × ∏(1 - 1/p) for prime factors p.

    Time: O(√n)
    Space: O(1)
    """
    if n <= 0:
        return 0

    result = n

    # For each prime factor p, multiply result by (1 - 1/p) = (p-1)/p
    d = 2
    while d * d <= n:
        if n % d == 0:
            # Remove all factors of d
            while n % d == 0:
                n //= d
            result -= result // d  # Equivalent to result *= (1 - 1/d)
        d += 1

    # If n > 1, then it's a remaining prime factor
    if n > 1:
        result -= result // n

    return result


# Test
print(euler_totient(12))  # 4 → {1, 5, 7, 11} are coprime to 12
print(euler_totient(1))   # 1
print(euler_totient(7))   # 6 (all of 1..6 are coprime to prime 7)
print(euler_totient(10))  # 4 → {1, 3, 7, 9}
```

### Hard: Largest Component Size by Common Factor (LeetCode 952)

Given an array of unique positive integers, group numbers that share a common factor > 1. Return the size of the largest connected component.

**Approach**: For each number, find its prime factors and union the number with each prime factor in a Union-Find structure. Numbers sharing a prime factor end up in the same component.

**Why Union-Find works here**: Instead of comparing every pair of numbers (O(n²)), we use prime factors as "bridges" — if two numbers share a prime factor p, they both get unioned with p, putting them in the same component.

```python
def largestComponentSize(nums: list[int]) -> int:
    """
    Union-Find approach: union each number with its prime factors.

    Time: O(n × √max_val × α(n)) where α is inverse Ackermann (~constant)
    Space: O(n + max_val)
    """
    from collections import Counter

    # Union-Find with path compression and union by rank
    parent = {}
    rank = {}

    def find(x: int) -> int:
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> None:
        rx, ry = find(x), find(y)
        if rx == ry:
            return
        # Union by rank
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1

    # For each number, union it with its prime factors
    for num in nums:
        temp = num
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                union(num, d)  # Union number with prime factor
                while temp % d == 0:
                    temp //= d
            d += 1
        if temp > 1:
            union(num, temp)  # Remaining large prime factor

    # Count component sizes (only for numbers in the input array)
    component_sizes = Counter(find(num) for num in nums)
    return max(component_sizes.values())


# Test
print(largestComponentSize([4, 6, 15, 35]))
# 4 → all connected: 4-6 (share 2), 6-15 (share 3), 15-35 (share 5)
print(largestComponentSize([20, 50, 9, 63]))
# 2 → {20, 50} share factor 5 or 2; {9, 63} share factor 3
print(largestComponentSize([2, 3, 6, 7, 4, 12, 21, 39]))
# 8 → all connected through shared prime factors
```

### Hard: Prime Palindrome (LeetCode 866)

Given an integer n, return the smallest prime palindrome ≥ n.

**Key insight**: All even-length palindromes (except 11) are divisible by 11, so they can't be prime. This means we only need to check odd-length palindromes (plus 11 as a special case), which dramatically reduces the search space.

**Why even-length palindromes are divisible by 11**: A number is divisible by 11 if its alternating digit sum is 0 mod 11. For an even-length palindrome like `abba`, the alternating sum is a - b + b - a = 0.

```python
def primePalindrome(n: int) -> int:
    """
    Find the smallest prime palindrome >= n.

    Strategy:
    - Generate palindromes in increasing order
    - Check each for primality
    - All even-length palindromes > 11 are divisible by 11, so skip them

    Time: O(n^0.5) per primality check, with relatively few palindrome candidates
    Space: O(1)
    """
    def is_prime(x: int) -> bool:
        if x < 2:
            return False
        if x < 4:
            return True
        if x % 2 == 0 or x % 3 == 0:
            return False
        i = 5
        while i * i <= x:
            if x % i == 0 or x % (i + 2) == 0:
                return False
            i += 6
        return True

    def is_palindrome(x: int) -> bool:
        s = str(x)
        return s == s[::-1]

    # Special case: 11 is the only even-length prime palindrome
    if n <= 11 and 11 >= n:
        # Check small primes directly
        for candidate in [2, 3, 5, 7, 11]:
            if candidate >= n:
                return candidate

    # For n > 11, only check odd-length numbers (even-length palindromes
    # are all divisible by 11, except 11 itself)
    candidate = max(n, 12)
    while True:
        # Skip even-length numbers: jump from 999 to 1001, etc.
        length = len(str(candidate))
        if length % 2 == 0:
            # Jump to smallest odd-length number: 10^length + 1
            candidate = 10**length + 1

        if is_palindrome(candidate) and is_prime(candidate):
            return candidate
        candidate += 1


# Test
print(primePalindrome(6))    # 7
print(primePalindrome(8))    # 11
print(primePalindrome(13))   # 101
print(primePalindrome(1))    # 2
```

### Hard: Preimage Size of Factorial Zeroes Function (LeetCode 793)

Given an integer k, return the number of non-negative integers x such that x! has exactly k trailing zeroes.

**Connection to primes**: Trailing zeroes in n! come from factors of 10 = 2 × 5. Since factors of 2 are always more abundant, the count of trailing zeroes = count of factor 5 in n!.

**Count of factor 5 in n!** = ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + ...  (Legendre's formula)

**Key insight**: The trailing-zeroes function f(x) is non-decreasing and never increases by more than 1 at a time for consecutive multiples of 5. For any valid k, exactly 5 values of x produce k trailing zeroes. For invalid k (a value that f(x) skips over), the answer is 0. So the answer is always 0 or 5.

```python
def preimageSizeFZF(k: int) -> int:
    """
    Count how many x have exactly k trailing zeroes in x!.

    Use binary search to find the range of x values where
    trailing_zeroes(x) == k.

    The answer is always 0 or 5.

    Time: O(log²(k)) — binary search with O(log k) per trailing_zeroes call
    Space: O(1)
    """
    def trailing_zeroes(n: int) -> int:
        """Count trailing zeroes in n! using Legendre's formula for prime 5."""
        count = 0
        power_of_5 = 5
        while power_of_5 <= n:
            count += n // power_of_5
            power_of_5 *= 5
        return count

    def first_with_at_least_k_zeroes(k: int) -> int:
        """Binary search for smallest x where trailing_zeroes(x) >= k."""
        lo, hi = 0, 5 * k + 1  # Upper bound: f(5k) >= k always
        while lo < hi:
            mid = (lo + hi) // 2
            if trailing_zeroes(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo

    # If both "first with >= k" and "first with >= k+1" exist,
    # the count is their difference (always 0 or 5).
    return first_with_at_least_k_zeroes(k + 1) - first_with_at_least_k_zeroes(k)


# Test
print(preimageSizeFZF(0))   # 5 (x = 0, 1, 2, 3, 4 all give 0 trailing zeroes)
print(preimageSizeFZF(5))   # 0 (no x gives exactly 5 trailing zeroes — f jumps from 4 to 6)
print(preimageSizeFZF(3))   # 5
print(preimageSizeFZF(1))   # 5
```

---

## When NOT to Use Prime Algorithms

1. **Don't build a sieve for a single query**: Sieve is O(n) space — only worth it for multiple queries or "count all primes ≤ n"
2. **Don't factor when you only need primality**: Factorization finds all primes; primality check just needs one divisor
3. **Don't use Miller-Rabin for small n**: For n < 10¹², trial division with 6k±1 is simpler and fast enough
4. **Don't forget integer overflow in other languages**: In Python this isn't an issue (arbitrary precision), but `i * i` can overflow in C++/Java
5. **Don't use `math.sqrt(n)`** for the loop bound: floating-point imprecision can cause off-by-one errors — use `i * i <= n` instead

**Space consideration**: Sieve of Eratosthenes uses O(n) memory. For n = 10⁹, a boolean array needs ~1 GB. Consider a **segmented sieve** for very large ranges.

---

## Related Sections

- [GCD and LCM](./01-gcd-lcm.md) - Coprimality relates to primes
- [Modular Arithmetic](./03-modular-arithmetic.md) - Prime modulus properties
