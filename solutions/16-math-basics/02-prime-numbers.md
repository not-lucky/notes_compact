# Prime Numbers

## Practice Problems

### 1. Count Primes
**Difficulty:** Medium
**Concept:** Sieve of Eratosthenes

```python
def countPrimes(n: int) -> int:
    """
    Count the number of prime numbers less than n.
    Time: O(n log log n)
    Space: O(n)
    """
    if n < 2:
        return 0

    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n, i):
                is_prime[j] = False

    return sum(is_prime)
```

### 2. Ugly Number
**Difficulty:** Easy
**Concept:** Limited prime factors

```python
def isUgly(n: int) -> bool:
    """
    Check if a positive integer's prime factors are limited to 2, 3, and 5.
    Time: O(log n)
    Space: O(1)
    """
    if n <= 0:
        return False

    for p in [2, 3, 5]:
        while n % p == 0:
            n //= p

    return n == 1
```
