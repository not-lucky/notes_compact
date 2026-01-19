# Prime Numbers

> **Prerequisites:** [GCD and LCM](./01-gcd-lcm.md) (helpful for understanding coprimality)

## Interview Context

Prime number problems test mathematical reasoning and optimization skills. Common interview scenarios include:
- Counting primes up to n
- Checking if a number is prime
- Finding prime factors
- Ugly number variants (numbers with limited prime factors)

The Sieve of Eratosthenes is the most important algorithm to know—it's efficient and appears frequently.

---

## Pattern: Trial Division (Primality Check)

To check if `n` is prime, we only need to test divisibility up to √n.

### Why √n is Sufficient

```
If n = a × b where a ≤ b, then:
  a × b = n
  a × a ≤ a × b = n
  a ≤ √n

So if n has a factor > 1, at least one factor is ≤ √n.
We only need to check up to √n.
```

### Visual Example

```
Is 29 prime?

√29 ≈ 5.4, so check 2, 3, 5:
  29 % 2 = 1 ✗
  29 % 3 = 2 ✗
  29 % 5 = 4 ✗

No divisors found → 29 is prime
```

---

## Implementation

### Basic Primality Check

```python
def is_prime(n: int) -> bool:
    """
    Check if n is prime using trial division.

    Time: O(√n)
    Space: O(1)
    """
    if n < 2:
        return False
    if n < 4:
        return True  # 2 and 3 are prime
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Check 6k ± 1 pattern (all primes > 3 are of this form)
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
```

### Why 6k ± 1 Optimization Works

```
All integers can be written as 6k, 6k+1, 6k+2, 6k+3, 6k+4, or 6k+5

6k     = divisible by 6 (not prime if > 6)
6k + 2 = divisible by 2
6k + 3 = divisible by 3
6k + 4 = divisible by 2

Only 6k + 1 and 6k + 5 (= 6k - 1) can be prime.

So we check i and i+2, then increment i by 6.
```

---

## Pattern: Sieve of Eratosthenes

The sieve efficiently finds ALL primes up to n. Essential for "count primes" problems.

### Algorithm Visualization

```
Find all primes ≤ 30:

Initial: [F F T T T T T T T T T T T T T T T T T T T T T T T T T T T T T]
Index:    0 1 2 3 4 5 6 7 8 9 ...

Mark multiples of 2:
[F F T T F T F T F T F T F T F T F T F T F T F T F T F T F T F]

Mark multiples of 3:
[F F T T F T F T F F F T F T F F F T F T F F F T F T F F F T F]

Mark multiples of 5:
[F F T T F T F T F F F T F T F F F T F T F F F T F F F F F T F]

Primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
```

### Implementation

```python
def sieve_of_eratosthenes(n: int) -> list[int]:
    """
    Find all primes up to n using Sieve of Eratosthenes.

    Time: O(n log log n)
    Space: O(n)
    """
    if n < 2:
        return []

    # is_prime[i] = True means i is prime
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    # Mark multiples of each prime
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            # Start from i*i (smaller multiples already marked)
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return [i for i in range(n + 1) if is_prime[i]]


# Test
print(sieve_of_eratosthenes(30))
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

### Count Primes (LeetCode 204)

```python
def countPrimes(n: int) -> int:
    """
    Count primes less than n.

    Time: O(n log log n)
    Space: O(n)
    """
    if n < 2:
        return 0

    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            # Mark all multiples starting from i*i
            for j in range(i * i, n, i):
                is_prime[j] = False

    return sum(is_prime)


# Test
print(countPrimes(10))   # 4 (primes: 2, 3, 5, 7)
print(countPrimes(100))  # 25
```

---

## Problem: Ugly Number

**LeetCode 263**: An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5.

```python
def isUgly(n: int) -> bool:
    """
    Check if n is an ugly number.

    Time: O(log n)
    Space: O(1)
    """
    if n <= 0:
        return False

    for prime in [2, 3, 5]:
        while n % prime == 0:
            n //= prime

    return n == 1


# Test
print(isUgly(6))    # True (2 × 3)
print(isUgly(8))    # True (2³)
print(isUgly(14))   # False (2 × 7)
print(isUgly(1))    # True
```

---

## Problem: Prime Factorization

```python
def prime_factors(n: int) -> list[int]:
    """
    Return all prime factors of n (with repetition).

    Time: O(√n)
    Space: O(log n) - number of prime factors
    """
    factors = []

    # Handle 2 separately
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Check odd numbers up to √n
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2

    # If n > 1, then it's a prime factor
    if n > 1:
        factors.append(n)

    return factors


# Test
print(prime_factors(12))    # [2, 2, 3]
print(prime_factors(100))   # [2, 2, 5, 5]
print(prime_factors(17))    # [17]
print(prime_factors(1))     # []
```

### Unique Prime Factors with Counts

```python
from collections import Counter

def prime_factor_counts(n: int) -> dict[int, int]:
    """
    Return prime factors with their counts.

    Time: O(√n)
    Space: O(log n)
    """
    return Counter(prime_factors(n))


print(prime_factor_counts(360))  # {2: 3, 3: 2, 5: 1}
# 360 = 2³ × 3² × 5
```

---

## Problem: Super Ugly Number

**LeetCode 313**: Find the nth super ugly number. Super ugly numbers are positive integers whose all prime factors are in the given list.

```python
def nthSuperUglyNumber(n: int, primes: list[int]) -> int:
    """
    Find nth super ugly number.

    Time: O(n * k) where k = len(primes)
    Space: O(n + k)
    """
    ugly = [0] * n
    ugly[0] = 1

    # Track index for each prime
    indices = [0] * len(primes)
    # Next values for each prime
    next_values = list(primes)

    for i in range(1, n):
        # Choose minimum
        ugly[i] = min(next_values)

        # Update all primes that produced this minimum
        for j in range(len(primes)):
            if next_values[j] == ugly[i]:
                indices[j] += 1
                next_values[j] = ugly[indices[j]] * primes[j]

    return ugly[n - 1]


# Test
print(nthSuperUglyNumber(12, [2, 7, 13, 19]))
# 32 (1,2,4,7,8,13,14,16,19,26,28,32)
```

---

## Problem: Happy Number

**LeetCode 202**: A happy number is defined by repeatedly replacing it with the sum of the squares of its digits until it equals 1 or loops endlessly.

```python
def isHappy(n: int) -> bool:
    """
    Check if n is a happy number.

    Time: O(log n) - proven to converge
    Space: O(log n) for seen set, or O(1) with Floyd's cycle detection
    """
    def get_next(num: int) -> int:
        total = 0
        while num > 0:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total

    # Use Floyd's cycle detection (O(1) space)
    slow = n
    fast = get_next(n)

    while fast != 1 and slow != fast:
        slow = get_next(slow)
        fast = get_next(get_next(fast))

    return fast == 1


# Test
print(isHappy(19))  # True: 1²+9²=82 → 8²+2²=68 → ... → 1
print(isHappy(2))   # False (cycles)
```

---

## Complexity Analysis

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| Trial division | O(√n) | O(1) | Single primality check |
| Sieve of Eratosthenes | O(n log log n) | O(n) | All primes up to n |
| Prime factorization | O(√n) | O(log n) | Factor decomposition |

### When to Use Each

```
Single check: n < 10^12 → Trial division
Multiple checks: Use sieve up to √(max_n)
Count primes ≤ n: Sieve
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
            # Keep dividing by p
            while n % p == 0:
                n //= p
            return n == 1

    # n itself is prime (p^1)
    return True


print(is_power_of_prime(8))   # True (2³)
print(is_power_of_prime(12))  # False (2² × 3)
print(is_power_of_prime(17))  # True (17¹)
```

### 2. Count Divisors

```python
def count_divisors(n: int) -> int:
    """
    Count total divisors using prime factorization.
    If n = p1^a1 * p2^a2 * ..., count = (a1+1)(a2+1)...

    Time: O(√n)
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1

    count = 1

    # Handle 2
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

    # Remaining prime factor
    if n > 1:
        count *= 2  # (1 + 1) for this prime

    return count


print(count_divisors(12))  # 6 (divisors: 1,2,3,4,6,12)
print(count_divisors(36))  # 9 (divisors: 1,2,3,4,6,9,12,18,36)
```

### 3. Smallest Prime Factor (SPF) Sieve

```python
def smallest_prime_factor_sieve(n: int) -> list[int]:
    """
    Build SPF array where spf[i] = smallest prime factor of i.
    Useful for O(log n) factorization of many numbers.

    Time: O(n log log n)
    Space: O(n)
    """
    spf = list(range(n + 1))  # spf[i] = i initially

    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:  # i is prime
            for j in range(i * i, n + 1, i):
                if spf[j] == j:  # Not yet marked
                    spf[j] = i

    return spf


# Usage: Factorize any number ≤ n in O(log n)
def factorize_with_spf(n: int, spf: list[int]) -> list[int]:
    factors = []
    while n > 1:
        factors.append(spf[n])
        n //= spf[n]
    return factors


spf = smallest_prime_factor_sieve(100)
print(factorize_with_spf(60, spf))  # [2, 2, 3, 5]
```

---

## Edge Cases

1. **0 and 1**: Not prime
2. **2**: The only even prime
3. **Negative numbers**: Primes are positive by definition
4. **Large primes**: May need Miller-Rabin for n > 10^12
5. **1 as factor**: Not a prime factor

---

## Interview Tips

1. **Memorize the 6k±1 optimization**: Shows sophistication
2. **Know the sieve complexity**: O(n log log n), not O(n²)
3. **Start marking from i²**: Common optimization question
4. **Mention space-time tradeoff**: Sieve uses O(n) space
5. **Python's built-in**: No `is_prime()`, but `sympy.isprime()` exists

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Count Primes | Medium | Sieve of Eratosthenes |
| 2 | Ugly Number | Easy | Limited prime factors |
| 3 | Ugly Number II | Medium | DP with multiple pointers |
| 4 | Super Ugly Number | Medium | Generalized ugly number |
| 5 | Happy Number | Easy | Digit sum cycle detection |
| 6 | Perfect Number | Easy | Divisor sum |

---

## Related Sections

- [GCD and LCM](./01-gcd-lcm.md) - Coprimality relates to primes
- [Modular Arithmetic](./03-modular-arithmetic.md) - Prime modulus properties
