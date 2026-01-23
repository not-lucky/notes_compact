# Solutions: Math Basics

## 1. GCD and LCM

### Greatest Common Divisor (GCD)
**Problem Statement:**
Compute the Greatest Common Divisor of two integers using the Euclidean algorithm.

**Python Implementation:**
```python
def gcd(a: int, b: int) -> int:
    """
    Greatest Common Divisor using Euclidean algorithm.
    Time: O(log(min(a, b)))
    Space: O(1)
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a
```

### Least Common Multiple (LCM)
**Problem Statement:**
Compute the Least Common Multiple of two integers.

**Python Implementation:**
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
```

## 2. Prime Numbers

### Primality Check
**Problem Statement:**
Check if a number `n` is prime efficiently.

**Python Implementation:**
```python
def is_prime(n: int) -> bool:
    """
    Check if n is prime using trial division up to √n with 6k ± 1 optimization.
    Time: O(√n)
    Space: O(1)
    """
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
```

### Sieve of Eratosthenes
**Problem Statement:**
Find all primes up to `n`.

**Python Implementation:**
```python
def sieve_of_eratosthenes(n: int) -> list[int]:
    """
    Find all primes up to n using Sieve of Eratosthenes.
    Time: O(n log log n)
    Space: O(n)
    """
    if n < 2: return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]
```

## 3. Modular Arithmetic

### Modular Exponentiation
**Problem Statement:**
Compute `(base^exp) % mod` efficiently.

**Python Implementation:**
```python
def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Compute (base^exp) mod m using binary exponentiation.
    Time: O(log exp)
    Space: O(1)
    """
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result
```

## 4. Random Sampling

### Reservoir Sampling (Pick 1)
**Problem Statement:**
Select one random element from a stream of unknown size.

**Python Implementation:**
```python
import random

def reservoir_sample_one(stream) -> any:
    """
    Select one random element from a stream using O(1) space.
    Time: O(n)
    Space: O(1)
    """
    result = None
    for i, item in enumerate(stream, 1):
        if random.randint(1, i) == 1:
            result = item
    return result
```

### Fisher-Yates Shuffle
**Problem Statement:**
Shuffle an array in-place uniformly.

**Python Implementation:**
```python
import random

def shuffle(arr: list) -> list:
    """
    Shuffle array in-place using Fisher-Yates algorithm.
    Time: O(n)
    Space: O(1)
    """
    n = len(arr)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr
```

## 5. Square Root Problems

### Integer Square Root
**Problem Statement:**
Compute `floor(sqrt(x))` using binary search.

**Python Implementation:**
```python
def mySqrt(x: int) -> int:
    """
    Compute floor(sqrt(x)) using binary search.
    Time: O(log x)
    Space: O(1)
    """
    if x < 2: return x
    left, right = 1, x // 2
    result = 0
    while left <= right:
        mid = (left + right) // 2
        if mid * mid <= x:
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    return result
```

## 6. Number Properties

### Palindrome Number
**Problem Statement:**
Check if an integer is a palindrome without string conversion.

**Python Implementation:**
```python
def isPalindrome(x: int) -> bool:
    """
    Check if x is a palindrome by reversing half.
    Time: O(log x)
    Space: O(1)
    """
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    reversed_half = 0
    while x > reversed_half:
        reversed_half = reversed_half * 10 + x % 10
        x //= 10
    return x == reversed_half or x == reversed_half // 10
```

### Reverse Integer
**Problem Statement:**
Reverse digits of a 32-bit signed integer, return 0 on overflow.

**Python Implementation:**
```python
def reverse(x: int) -> int:
    """
    Reverse digits of x with overflow check.
    Time: O(log x)
    Space: O(1)
    """
    INT_MAX = 2**31 - 1
    sign = 1 if x >= 0 else -1
    x, result = abs(x), 0
    while x:
        digit = x % 10
        x //= 10
        if result > (INT_MAX - digit) // 10:
            return 0
        result = result * 10 + digit
    return result * sign
```
