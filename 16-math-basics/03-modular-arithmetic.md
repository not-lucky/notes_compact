# Modular Arithmetic

> **Prerequisites:** [GCD and LCM](./01-gcd-lcm.md) (for modular inverse), [Prime Numbers](./02-prime-numbers.md) (for prime modulus)

## Building Intuition

**The "Clock" Mental Model**

Think of modular arithmetic like a clock:

- A 12-hour clock wraps around after 12: 13:00 → 1:00
- In mod 12: 13 % 12 = 1, 25 % 12 = 1, 37 % 12 = 1

```
For mod 5:      0 → 1 → 2 → 3 → 4 → 0 → 1 → ...
Number:         0   1   2   3   4   5   6   ...
Result mod 5:   0   1   2   3   4   0   1   ...
```

**Why 10^9 + 7?**

This magic number appears everywhere because:

1. It's prime (enables Fermat's little theorem for division)
2. It fits in 32-bit int with room for one multiplication: (10^9)² < 2^63
3. It's large enough that collision probability is tiny

**The Division Trap**

Addition, subtraction, and multiplication work naturally with mod:

- (a + b) % m = ((a % m) + (b % m)) % m ✓
- (a × b) % m = ((a % m) × (b % m)) % m ✓

But division is DIFFERENT:

- (a / b) % m ≠ ((a % m) / (b % m)) % m ✗
- You need the modular inverse: (a / b) % m = (a × b⁻¹) % m

---

## Interview Context

Modular arithmetic is essential for:

- Handling large numbers without overflow (Pow(x, n) mod m)
- Hash functions and rolling hashes (Rabin-Karp)
- Counting problems with "return answer mod 10^9+7"
- Cryptography-related problems

The key insight: `(a op b) mod m = ((a mod m) op (b mod m)) mod m` for +, -, ×

---

## Pattern: Basic Modular Operations

### Properties of Modulo

```
Key identities (for + , - , ×):

(a + b) mod m = ((a mod m) + (b mod m)) mod m
(a - b) mod m = ((a mod m) - (b mod m) + m) mod m
(a × b) mod m = ((a mod m) × (b mod m)) mod m

Division is DIFFERENT:
(a / b) mod m = (a × b⁻¹) mod m  (where b⁻¹ is modular inverse)
```

### Visualization

```
Think of numbers on a clock with m positions (0 to m-1):

For m = 5:
    0
  4   1
   3 2

7 mod 5 = 2  (go around once, land on 2)
-2 mod 5 = 3 (go backwards 2 from 0, land on 3)
```

---

## Implementation

### Modular Exponentiation (Binary Exponentiation)

The most common interview pattern. Compute `(base^exp) mod m` in O(log exp).

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
        if exp & 1:  # If exp is odd
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod

    return result


# Test
print(mod_pow(2, 10, 1000))     # 24 (1024 mod 1000)
print(mod_pow(3, 1000, 10**9+7))  # Large power, no overflow
```

### Python's Built-in

```python
# Python has a built-in pow with modulo!
print(pow(2, 10, 1000))  # 24

# This is optimized and handles edge cases
```

---

## Problem: Pow(x, n)

**LeetCode 50**: Implement `pow(x, n)`, which calculates x raised to the power n.

```python
def myPow(x: float, n: int) -> float:
    """
    Compute x^n using binary exponentiation.

    Time: O(log |n|)
    Space: O(1)
    """
    if n == 0:
        return 1.0

    # Handle negative exponent
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


# Test
print(myPow(2.0, 10))   # 1024.0
print(myPow(2.0, -2))   # 0.25
print(myPow(2.1, 3))    # 9.261
```

### Why Binary Exponentiation?

```
Naive: x^10 = x × x × x × x × x × x × x × x × x × x  (10 multiplications)

Binary: 10 = 1010 in binary
  x^10 = x^8 × x^2
       = (x^4)^2 × (x^2)
       = ((x^2)^2)^2 × (x^2)

Compute x^2, x^4, x^8 by repeated squaring (4 multiplications)
Multiply those where bit is set (1 more multiplication)

Total: ~log₂(10) = 4 multiplications vs 10
```

---

## Problem: Super Pow

**LeetCode 372**: Calculate `a^b mod 1337` where b is represented as an array.

```python
def superPow(a: int, b: list[int]) -> int:
    """
    Compute a^(large number) mod 1337.

    Key insight: a^1234 = a^(123*10 + 4) = (a^123)^10 × a^4

    Time: O(n) where n = len(b)
    Space: O(1)
    """
    MOD = 1337

    def pow_mod(base: int, exp: int) -> int:
        result = 1
        base %= MOD
        while exp > 0:
            if exp & 1:
                result = (result * base) % MOD
            base = (base * base) % MOD
            exp >>= 1
        return result

    result = 1
    for digit in b:
        # result = (previous result)^10 × a^digit
        result = pow_mod(result, 10) * pow_mod(a, digit) % MOD

    return result


# Test
print(superPow(2, [3]))        # 8
print(superPow(2, [1, 0]))     # 1024 mod 1337 = 1024
print(superPow(2, [2, 0, 0]))  # 2^200 mod 1337
```

---

## Pattern: Modular Inverse

Division in modular arithmetic requires the modular inverse.

```
a / b mod m = a × b⁻¹ mod m

where b⁻¹ is the modular inverse: b × b⁻¹ ≡ 1 (mod m)
```

### Modular Inverse Using Extended Euclidean Algorithm

```python
def mod_inverse_extended_gcd(a: int, m: int) -> int:
    """
    Find modular inverse of a under modulo m using extended GCD.
    Returns x such that (a * x) % m = 1

    Time: O(log m)
    Space: O(log m) for recursion

    Raises ValueError if inverse doesn't exist (gcd(a,m) != 1)
    """
    def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        if b == 0:
            return a, 1, 0
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (a // b) * y

    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"Modular inverse doesn't exist for {a} mod {m}")
    return (x % m + m) % m


# Test
print(mod_inverse_extended_gcd(3, 7))   # 5 (3×5 = 15 = 2×7 + 1)
print(mod_inverse_extended_gcd(2, 11))  # 6 (2×6 = 12 = 11 + 1)
```

### Modular Inverse Using Fermat's Little Theorem

When m is prime, `a^(m-1) ≡ 1 (mod m)`, so `a^(m-2) ≡ a⁻¹ (mod m)`.

```python
def mod_inverse_fermat(a: int, m: int) -> int:
    """
    Find modular inverse when m is PRIME using Fermat's little theorem.
    a^(-1) = a^(m-2) mod m

    Time: O(log m)
    Space: O(1)
    """
    return pow(a, m - 2, m)


# Test (MOD = 10^9 + 7 is prime)
MOD = 10**9 + 7
print(mod_inverse_fermat(2, MOD))  # 500000004 (2 × this ≡ 1 mod MOD)
```

---

## Problem: Division with Large Modulus

Many DP problems ask for "answer mod 10^9+7" and involve division.

```python
def compute_with_division(a: int, b: int) -> int:
    """
    Compute (a / b) mod (10^9 + 7)

    Example: Computing n choose k mod p
    """
    MOD = 10**9 + 7

    # a / b mod p = a × b^(-1) mod p
    return (a * pow(b, MOD - 2, MOD)) % MOD


# Example: Compute 10! / 3! mod (10^9 + 7)
from math import factorial
a = factorial(10)
b = factorial(3)
print(compute_with_division(a, b))  # 604800
print(a // b)  # Verify: 604800
```

---

## Pattern: Handling Negative Numbers

```python
def safe_mod(n: int, m: int) -> int:
    """
    Handle negative numbers correctly for modulo.
    Python's % handles this, but C++/Java don't!

    In Python: -7 % 5 = 3 (correct)
    In C++:    -7 % 5 = -2 (need to add m)
    """
    return ((n % m) + m) % m


# Python handles this correctly
print(-7 % 5)  # 3 in Python
print(safe_mod(-7, 5))  # 3
```

---

## Problem: Add Strings as Large Numbers

When dealing with very large numbers that don't fit in integers, use string arithmetic with modulo.

```python
def string_to_mod(s: str, mod: int) -> int:
    """
    Convert a large number string to its value mod m.

    Time: O(n)
    Space: O(1)
    """
    result = 0
    for char in s:
        result = (result * 10 + int(char)) % mod
    return result


# Test
large_number = "12345678901234567890"
MOD = 10**9 + 7
print(string_to_mod(large_number, MOD))
```

---

## Rolling Hash (Rabin-Karp Application)

Modular arithmetic enables efficient string hashing.

```python
def polynomial_hash(s: str, base: int = 31, mod: int = 10**9 + 9) -> int:
    """
    Compute polynomial hash: s[0]*base^(n-1) + s[1]*base^(n-2) + ... + s[n-1]

    Time: O(n)
    Space: O(1)
    """
    h = 0
    for char in s:
        h = (h * base + (ord(char) - ord('a') + 1)) % mod
    return h


# Rolling hash for substring matching
def rolling_hash_search(text: str, pattern: str) -> list[int]:
    """
    Find all occurrences of pattern in text using rolling hash.

    Time: O(n + m) average, O(n*m) worst case (hash collisions)
    Space: O(1)
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []

    BASE = 31
    MOD = 10**9 + 9

    # Precompute base^m
    base_pow = pow(BASE, m, MOD)

    # Compute pattern hash
    pattern_hash = polynomial_hash(pattern, BASE, MOD)

    # Compute initial window hash
    window_hash = polynomial_hash(text[:m], BASE, MOD)

    result = []
    if window_hash == pattern_hash and text[:m] == pattern:
        result.append(0)

    # Roll the window
    for i in range(1, n - m + 1):
        # Remove left char, add right char
        left_char = ord(text[i - 1]) - ord('a') + 1
        right_char = ord(text[i + m - 1]) - ord('a') + 1

        window_hash = (window_hash * BASE - left_char * base_pow + right_char) % MOD
        window_hash = (window_hash + MOD) % MOD  # Handle negative

        if window_hash == pattern_hash and text[i:i+m] == pattern:
            result.append(i)

    return result


# Test
print(rolling_hash_search("abcabcabc", "abc"))  # [0, 3, 6]
```

---

## Complexity Analysis

| Operation                      | Time       | Space    | Notes                 |
| ------------------------------ | ---------- | -------- | --------------------- |
| Modular add/sub/mul            | O(1)       | O(1)     | Direct operation      |
| Modular exponentiation         | O(log exp) | O(1)     | Binary exponentiation |
| Modular inverse (extended GCD) | O(log m)   | O(log m) | Stack space           |
| Modular inverse (Fermat)       | O(log m)   | O(1)     | Only for prime m      |
| Rolling hash                   | O(n)       | O(1)     | Per string            |

---

## Common Variations

### 1. Sum of Large Array Mod M

```python
def sum_mod(arr: list[int], mod: int) -> int:
    """Sum of array elements mod m."""
    return sum(x % mod for x in arr) % mod


print(sum_mod([10**18, 10**18, 10**18], 10**9 + 7))
```

### 2. Product of Large Array Mod M

```python
def product_mod(arr: list[int], mod: int) -> int:
    """Product of array elements mod m."""
    result = 1
    for x in arr:
        result = (result * (x % mod)) % mod
    return result


print(product_mod([1000, 2000, 3000], 10**9 + 7))
```

### 3. Factorial Mod M with Precomputation

```python
def precompute_factorials(n: int, mod: int) -> tuple[list[int], list[int]]:
    """
    Precompute factorials and inverse factorials mod m.
    Useful for computing many nCr values.

    Time: O(n + log m) for precomputation
    Space: O(n)
    """
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i-1] * i % mod

    # Inverse factorial: inv_fact[n] = (n!)^(-1) mod m
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], mod - 2, mod)
    for i in range(n - 1, -1, -1):
        inv_fact[i] = inv_fact[i + 1] * (i + 1) % mod

    return fact, inv_fact


def nCr_mod(n: int, r: int, fact: list[int], inv_fact: list[int], mod: int) -> int:
    """Compute nCr mod m using precomputed factorials."""
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % mod * inv_fact[n - r] % mod


# Test
MOD = 10**9 + 7
fact, inv_fact = precompute_factorials(1000, MOD)
print(nCr_mod(10, 3, fact, inv_fact, MOD))  # 120
print(nCr_mod(100, 50, fact, inv_fact, MOD))  # Large but computed efficiently
```

---

## Edge Cases

1. **Modulo by 0**: Undefined, check before operation
2. **Modulo by 1**: Always 0
3. **Negative numbers**: Use `((n % m) + m) % m`
4. **Overflow in multiplication**: In Python, no issue; in C++, use `long long`
5. **Zero to a power**: `0^n = 0` for n > 0, `0^0 = 1` by convention

---

## Interview Tips

1. **Know why 10^9+7**: It's prime (enables Fermat inverse) and fits in 32-bit with room for operations
2. **Use Python's `pow(a, b, mod)`**: It's optimized and handles edge cases
3. **Mention overflow prevention**: The interviewer wants to see you're aware
4. **Division requires inverse**: Never just divide when working mod m
5. **Verify with small examples**: Easy to make off-by-one errors

---

## Practice Problems

| #   | Problem                   | Difficulty | Key Concept                       |
| --- | ------------------------- | ---------- | --------------------------------- |
| 1   | Pow(x, n)                 | Medium     | Binary exponentiation             |
| 2   | Super Pow                 | Medium     | Modular exponentiation with array |
| 3   | Count Good Numbers        | Medium     | Modular arithmetic + counting     |
| 4   | String Hashing            | Medium     | Rolling hash (Rabin-Karp)         |
| 5   | Unique Paths (large grid) | Hard       | nCr with modular inverse          |

---

## When NOT to Use Modular Arithmetic

1. **When results fit in normal int**: Don't add complexity if overflow isn't a risk
2. **When you need actual values**: Mod loses information—can't recover original
3. **When precision matters**: Modular division requires inverse, which can be tricky
4. **When m isn't prime and you need division**: Modular inverse only exists when gcd(a, m) = 1
5. **When debugging**: Mod operations make debugging harder—test without mod first

**Common mistake**: Forgetting to handle negative numbers in languages like C++/Java.

---

## Related Sections

- [GCD and LCM](./01-gcd-lcm.md) - Extended GCD for modular inverse
- [Prime Numbers](./02-prime-numbers.md) - Prime modulus properties
