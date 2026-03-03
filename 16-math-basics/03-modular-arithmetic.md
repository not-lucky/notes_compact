# Modular Arithmetic

> **Prerequisites:** [GCD and LCM](./01-gcd-lcm.md) (for modular inverse), [Prime Numbers](./02-prime-numbers.md) (for prime modulus)

## Building Intuition

**The "Clock" Mental Model**

Think of modular arithmetic like a clock — numbers "wrap around" after reaching the modulus:

- A 12-hour clock wraps around after 12: 13:00 → 1:00
- In mod 12: 13 % 12 = 1, 25 % 12 = 1, 37 % 12 = 1

```
For mod 5:      0 → 1 → 2 → 3 → 4 → 0 → 1 → ...
Number:         0   1   2   3   4   5   6   ...
Result mod 5:   0   1   2   3   4   0   1   ...
```

Two numbers are **congruent modulo m** if they have the same remainder when divided by m. We write `a ≡ b (mod m)`. For example, 13 ≡ 1 (mod 12).

**Why 10^9 + 7?**

This constant (1000000007) appears everywhere in competitive programming and interviews:

1. **It's prime** — enables modular inverse via Fermat's little theorem
2. **Fits in 64-bit multiplication** — if a, b < 10^9+7, then a * b < (10^9+7)^2 ≈ 10^18 < 2^63 ≈ 9.2 * 10^18, so the product fits in a 64-bit signed integer
3. **Large enough** — collision probability in hashing is ~1/10^9, which is tiny

**The Division Trap**

Addition, subtraction, and multiplication work naturally with mod:

- (a + b) % m = ((a % m) + (b % m)) % m
- (a - b) % m = ((a % m) - (b % m) + m) % m
- (a * b) % m = ((a % m) * (b % m)) % m

But division is DIFFERENT — you cannot just divide the remainders:

- (a / b) % m ≠ ((a % m) / (b % m)) % m
- Instead, multiply by the **modular inverse**: (a / b) % m = (a * b^(-1)) % m

**Why does this work for +, -, * but not /?** Because mod distributes over these operations (they preserve the congruence relation), but integer division can discard information via truncation. For example: 7 / 3 = 2 in integer math, but (7 mod 5) / (3 mod 5) = 2 / 3 = 0 — wrong.

---

## Interview Context

Modular arithmetic is essential for:

- **Handling large numbers without overflow** — Pow(x, n) mod m
- **Hash functions and rolling hashes** — Rabin-Karp string matching
- **Counting problems** — "return answer mod 10^9+7"
- **Combinatorics** — nCr mod p using precomputed factorials

The key identity: `(a op b) mod m = ((a mod m) op (b mod m)) mod m` for op in {+, -, *}

---

## Pattern: Basic Modular Operations

### Properties of Modulo

```
Key identities (for +, -, *):

(a + b) mod m = ((a mod m) + (b mod m)) mod m
(a - b) mod m = ((a mod m) - (b mod m) + m) mod m   <- the +m prevents negatives
(a * b) mod m = ((a mod m) * (b mod m)) mod m

Division requires the modular inverse:
(a / b) mod m = (a * b^(-1)) mod m    where b * b^(-1) ≡ 1 (mod m)
```

### Visualization

```
Think of numbers on a clock with m positions (0 to m-1):

For m = 5:
    0
  4   1
   3 2

 7 mod 5 = 2   (go around once, land on 2)
-2 mod 5 = 3   (go backwards 2 from 0, equivalently 5 - 2 = 3)
12 mod 5 = 2   (go around twice, land on 2)
```

---

## Implementation

### Modular Exponentiation (Binary Exponentiation)

The most common interview pattern. Compute `(base^exp) mod m` in O(log exp) time instead of O(exp) with naive multiplication.

**Core idea:** Decompose the exponent into powers of 2 using its binary representation, then combine results.

```python
def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Compute (base^exp) % mod using binary exponentiation.

    Key idea: exp in binary tells us which powers of base to multiply.
    Example: 2^13 = 2^(1101 in binary) = 2^8 * 2^4 * 2^1

    Time:  O(log exp)
    Space: O(1)
    """
    result = 1 % mod  # Handles mod=1 edge case (any number mod 1 = 0)
    base %= mod

    while exp > 0:
        if exp & 1:  # If current bit is set, multiply this power in
            result = result * base % mod
        exp >>= 1       # Move to next bit
        base = base * base % mod  # Square the base for the next power of 2

    return result


# Test
print(mod_pow(2, 10, 1000))        # 24  (1024 % 1000)
print(mod_pow(3, 1000, 10**9 + 7)) # Large power, no overflow
print(mod_pow(5, 0, 1))            # 0   (anything mod 1 = 0)
```

### Python's Built-in

```python
# Python has a built-in 3-argument pow that does modular exponentiation!
print(pow(2, 10, 1000))  # 24

# This is implemented in C and handles edge cases (exp=0, base=0, mod=1, etc.)
# Always prefer this in interviews -- it's cleaner and faster.
```

---

## Problem: Pow(x, n) -- LeetCode 50

Implement `pow(x, n)`, which calculates x raised to the power n.

**Note:** This problem uses floats, not modular arithmetic, but the same binary exponentiation technique applies.

```python
def myPow(x: float, n: int) -> float:
    """
    Compute x^n using binary exponentiation.

    Edge cases:
    - n = 0: return 1.0
    - n < 0: compute (1/x)^(-n)
    - n = -2^31: Python handles arbitrary precision ints, so -n is fine.
      In C++/Java, you'd need to handle this specially since -(-2^31)
      overflows a 32-bit int.

    Time:  O(log |n|)
    Space: O(1)
    """
    if n == 0:
        return 1.0

    # Handle negative exponent: x^(-n) = (1/x)^n
    if n < 0:
        x = 1.0 / x
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
print(myPow(2.1, 3))    # 9.261...
```

### Why Binary Exponentiation Works

```
Naive: x^10 = x * x * x * x * x * x * x * x * x * x   (9 multiplications)

Binary exponentiation: decompose exponent into binary
  10 = 1010 in binary = 8 + 2

  So x^10 = x^8 * x^2

  We compute successive squares:
    x^1  (given)
    x^2  = (x^1)^2     <- 1 multiplication
    x^4  = (x^2)^2     <- 1 multiplication
    x^8  = (x^4)^2     <- 1 multiplication

  Then multiply the ones where the bit is set:
    x^10 = x^8 * x^2   <- 1 multiplication

  Total: 4 multiplications instead of 9!
  In general: O(log n) instead of O(n)
```

---

## Problem: Super Pow -- LeetCode 372

Calculate `a^b mod 1337` where b is represented as an array of digits (can be huge).

```python
def superPow(a: int, b: list[int]) -> int:
    """
    Compute a^(large number represented as digit array) mod 1337.

    Key insight: process digits left to right.
    a^1234 = a^(123*10 + 4) = (a^123)^10 * a^4

    At each step, raise the running result to the 10th power (shifting
    the exponent left by one decimal digit), then multiply in a^digit.

    Time:  O(len(b) * log(10)) = O(len(b))
    Space: O(1)
    """
    MOD = 1337
    result = 1

    for digit in b:
        # Raise accumulated result to the 10th power, then multiply by a^digit
        result = pow(result, 10, MOD) * pow(a, digit, MOD) % MOD

    return result


# Test
print(superPow(2, [3]))        # 8
print(superPow(2, [1, 0]))     # 1024 (2^10 mod 1337 = 1024)
print(superPow(2, [2, 0, 0]))  # 1215 (2^200 mod 1337)
```

---

## Pattern: Modular Inverse

To "divide" in modular arithmetic, you multiply by the **modular inverse**.

```
a / b mod m  =  a * b^(-1) mod m

where b^(-1) is the modular inverse of b:  b * b^(-1) ≡ 1 (mod m)

The inverse exists if and only if gcd(b, m) = 1.
When m is prime, every non-zero b has an inverse (since gcd(b, m) = 1 for 0 < b < m).
```

### Method 1: Extended Euclidean Algorithm

Works for **any** modulus m (as long as gcd(a, m) = 1).

**Why it works:** The extended GCD finds integers x, y such that `a*x + m*y = gcd(a, m)`. If gcd(a, m) = 1, then `a*x + m*y = 1`, which means `a*x ≡ 1 (mod m)`, so x is the inverse.

```python
def mod_inverse_extended_gcd(a: int, m: int) -> int:
    """
    Find modular inverse of a under modulo m using extended GCD.
    Returns x such that (a * x) % m == 1.

    Time:  O(log m)
    Space: O(log m) due to recursion stack

    Raises ValueError if inverse doesn't exist (gcd(a, m) != 1).
    """
    def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        """Returns (gcd, x, y) such that a*x + b*y = gcd(a, b)."""
        if b == 0:
            return a, 1, 0
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (a // b) * y

    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"Modular inverse doesn't exist for {a} mod {m}")
    return x % m  # Python's % always returns non-negative for positive m


# Test
print(mod_inverse_extended_gcd(3, 7))   # 5  (because 3 * 5 = 15 = 2*7 + 1)
print(mod_inverse_extended_gcd(2, 11))  # 6  (because 2 * 6 = 12 = 11 + 1)
```

### Method 2: Fermat's Little Theorem (Prime Modulus Only)

When m is prime, **Fermat's little theorem** states: `a^(m-1) ≡ 1 (mod m)` for any a not divisible by m.

**Derivation of the inverse:**

```
a^(m-1) ≡ 1     (mod m)       <- Fermat's little theorem
a * a^(m-2) ≡ 1 (mod m)       <- factor out one a
Therefore: a^(-1) ≡ a^(m-2)   (mod m)
```

```python
def mod_inverse_fermat(a: int, m: int) -> int:
    """
    Find modular inverse when m is PRIME using Fermat's little theorem.
    a^(-1) ≡ a^(m-2) (mod m)

    Time:  O(log m)
    Space: O(1)
    """
    return pow(a, m - 2, m)


# Test (10^9 + 7 is prime)
MOD = 10**9 + 7
inv2 = mod_inverse_fermat(2, MOD)
print(inv2)              # 500000004
print(2 * inv2 % MOD)    # 1  <- confirms it's the inverse
```

### When to Use Which?

| Method | Requirement | Time | Space | Use when... |
| --- | --- | --- | --- | --- |
| Fermat's theorem | m must be prime | O(log m) | O(1) | m = 10^9+7 (most common) |
| Extended GCD | gcd(a, m) = 1 | O(log m) | O(log m) | m is not prime |

---

## Pattern: Division Under Modulus

Many DP/combinatorics problems ask for "answer mod 10^9+7" and involve division.

```python
def mod_divide(a: int, b: int, mod: int) -> int:
    """
    Compute (a / b) % mod where mod is prime.
    Uses Fermat's little theorem: a/b = a * b^(mod-2) mod mod.
    """
    return a % mod * pow(b, mod - 2, mod) % mod


# Example: Compute 10! / 3! mod (10^9 + 7)
from math import factorial

MOD = 10**9 + 7
a = factorial(10)
b = factorial(3)
print(mod_divide(a, b, MOD))  # 604800
print(a // b)                 # 604800 (verify)
```

---

## Pattern: Handling Negative Numbers

```python
def safe_mod(n: int, m: int) -> int:
    """
    Handle negative numbers correctly for modulo.

    Python's % already returns non-negative results for positive m:
        -7 % 5 = 3 in Python

    But C++/Java return negative remainders:
        -7 % 5 = -2 in C++/Java

    This formula works in ALL languages:
    """
    return ((n % m) + m) % m


# Python handles this correctly natively
print(-7 % 5)          # 3 in Python
print(safe_mod(-7, 5)) # 3 (portable formula)
```

---

## Pattern: Large Number String to Mod

When a number is given as a string (too large for even Python's arbitrary-precision to be practical in O(1)):

```python
def string_to_mod(s: str, mod: int) -> int:
    """
    Convert a number represented as a string to its value mod m.
    Processes digit by digit using Horner's method.

    Why it works: "1234" = ((1*10 + 2)*10 + 3)*10 + 4
    We take mod at each step to keep numbers small.

    Time:  O(n) where n = len(s)
    Space: O(1)
    """
    result = 0
    for ch in s:
        result = (result * 10 + int(ch)) % mod
    return result


# Test
large_number = "12345678901234567890"
MOD = 10**9 + 7
print(string_to_mod(large_number, MOD))  # 814816192
```

---

## Rolling Hash (Rabin-Karp Application)

Modular arithmetic enables efficient string hashing for substring matching.

**Idea:** Treat a string as a polynomial evaluated at some base, mod a large prime.

```python
def polynomial_hash(s: str, base: int = 31, mod: int = 10**9 + 9) -> int:
    """
    Compute polynomial hash of string s.
    hash = s[0]*base^(n-1) + s[1]*base^(n-2) + ... + s[n-1]

    Maps characters: 'a'->1, 'b'->2, ..., 'z'->26
    (We use 1-indexed to avoid 'a' mapping to 0, which would make
    "a", "aa", "aaa" all hash to 0.)

    Time:  O(n)
    Space: O(1)
    """
    h = 0
    for ch in s:
        h = (h * base + (ord(ch) - ord('a') + 1)) % mod
    return h


def rolling_hash_search(text: str, pattern: str) -> list[int]:
    """
    Find all occurrences of pattern in text using Rabin-Karp rolling hash.

    Key insight: when sliding the window one position right, we can update
    the hash in O(1) by removing the contribution of the leftmost character
    and adding the new rightmost character.

    Hash formula for window text[i..i+m-1]:
      h = text[i]*base^(m-1) + text[i+1]*base^(m-2) + ... + text[i+m-1]

    Sliding from position i to i+1:
      h_new = (h - text[i]*base^(m-1)) * base + text[i+m]

    Time:  O(n + m) average, O(n * m) worst case (hash collisions)
    Space: O(1) excluding output
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []

    BASE = 31
    MOD = 10**9 + 9

    # Precompute base^(m-1) mod MOD -- needed to remove the leftmost character
    base_pow = pow(BASE, m - 1, MOD)

    # Hash of the pattern
    pattern_hash = polynomial_hash(pattern, BASE, MOD)

    # Hash of the first window
    window_hash = polynomial_hash(text[:m], BASE, MOD)

    result = []
    if window_hash == pattern_hash and text[:m] == pattern:
        result.append(0)

    # Slide the window across the text
    for i in range(1, n - m + 1):
        # Remove leftmost character's contribution, add new rightmost character
        old_char = ord(text[i - 1]) - ord('a') + 1
        new_char = ord(text[i + m - 1]) - ord('a') + 1

        window_hash = ((window_hash - old_char * base_pow) * BASE + new_char) % MOD

        # Confirm match (hash collision is possible, so verify with string comparison)
        if window_hash == pattern_hash and text[i:i + m] == pattern:
            result.append(i)

    return result


# Test
print(rolling_hash_search("abcabcabc", "abc"))  # [0, 3, 6]
print(rolling_hash_search("aaaaa", "aa"))        # [0, 1, 2, 3]
```

---

## Common Variations

### 1. Sum of Large Array Mod M

```python
def sum_mod(arr: list[int], mod: int) -> int:
    """Sum of array elements mod m. Take mod at each step to prevent overflow in other languages."""
    total = 0
    for x in arr:
        total = (total + x) % mod
    return total


print(sum_mod([10**18, 10**18, 10**18], 10**9 + 7))
```

### 2. Product of Large Array Mod M

```python
def product_mod(arr: list[int], mod: int) -> int:
    """Product of array elements mod m."""
    result = 1
    for x in arr:
        result = result * x % mod
    return result


print(product_mod([1000, 2000, 3000], 10**9 + 7))
```

### 3. Factorial and nCr Mod M with Precomputation

Essential for combinatorics problems. Precompute once, then answer nCr queries in O(1).

```python
def precompute_factorials(n: int, mod: int) -> tuple[list[int], list[int]]:
    """
    Precompute factorials and inverse factorials mod m (m must be prime).
    Useful for answering many nCr queries efficiently.

    Time:  O(n) for precomputation (O(n) for factorials + O(log m) for one
           inverse + O(n) for the inverse factorial table)
    Space: O(n)
    """
    # Forward pass: compute fact[i] = i! mod m
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod

    # Compute inv_fact[n] = (n!)^(-1) mod m using Fermat's theorem
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], mod - 2, mod)

    # Backward pass: inv_fact[i] = inv_fact[i+1] * (i+1)
    # Because (i!)^(-1) = ((i+1)!)^(-1) * (i+1)
    for i in range(n - 1, -1, -1):
        inv_fact[i] = inv_fact[i + 1] * (i + 1) % mod

    return fact, inv_fact


def nCr_mod(n: int, r: int, fact: list[int], inv_fact: list[int], mod: int) -> int:
    """Compute C(n, r) mod m in O(1) using precomputed factorials."""
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % mod * inv_fact[n - r] % mod


# Test
MOD = 10**9 + 7
fact, inv_fact = precompute_factorials(1000, MOD)
print(nCr_mod(10, 3, fact, inv_fact, MOD))   # 120
print(nCr_mod(100, 50, fact, inv_fact, MOD)) # 538992043
```

### 4. Modular Arithmetic in DP

A common pattern: DP where the answer must be returned mod 10^9+7. The key is to apply mod at every step of the DP transition.

```python
def count_ways_to_climb(n: int) -> int:
    """
    Count ways to climb n stairs (1 or 2 steps at a time) mod 10^9+7.
    Classic Fibonacci-like DP with mod.
    """
    MOD = 10**9 + 7
    if n <= 2:
        return n

    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        curr = (prev1 + prev2) % MOD  # Mod at each step!
        prev2, prev1 = prev1, curr

    return prev1


print(count_ways_to_climb(100))  # 782204094
```

---

## Complexity Analysis

| Operation | Time | Space | Notes |
| --- | --- | --- | --- |
| Modular add/sub/mul | O(1) | O(1) | Direct operation |
| Modular exponentiation | O(log exp) | O(1) | Binary exponentiation |
| Modular inverse (Extended GCD) | O(log m) | O(log m) | Recursion stack; works for any m |
| Modular inverse (Fermat) | O(log m) | O(1) | Requires prime m |
| Precompute factorials | O(n) | O(n) | One-time setup for nCr queries |
| nCr query (with precomputation) | O(1) | O(1) | After precomputation |
| Rolling hash (build) | O(n) | O(1) | Per string |
| Rolling hash (slide) | O(1) | O(1) | Per position |

---

## Edge Cases

1. **Modulo by 0** — undefined; always validate the modulus
2. **Modulo by 1** — always 0 (every integer is divisible by 1). Note: `mod_pow` must initialize `result = 1 % mod` to handle this correctly.
3. **Negative numbers** — use `((n % m) + m) % m` (Python handles this natively, but C++/Java don't)
4. **Overflow in multiplication** — not an issue in Python (arbitrary precision), but critical in C++/Java (use `long long` or 128-bit)
5. **0^0** — 1 by convention (Python's `pow(0, 0)` returns 1)
6. **Inverse of 0** — doesn't exist; gcd(0, m) = m != 1
7. **Non-prime modulus with division** — modular inverse only exists when gcd(a, m) = 1; use extended GCD, not Fermat
8. **Exponent = 0 with mod = 1** — result should be 0 (since 1 % 1 = 0), not 1

---

## Interview Tips

1. **Know why 10^9+7** — it's prime (enables Fermat inverse) and products of two values < 10^9+7 fit in 64-bit integers
2. **Use Python's `pow(a, b, mod)`** — it's implemented in C, handles edge cases, and is the cleanest way to write modular exponentiation
3. **Always mod intermediate results** — don't wait until the end; mod after every operation to keep numbers small
4. **Division requires inverse** — never just divide when working mod m
5. **Verify with small examples** — compute by hand for small inputs to catch off-by-one errors
6. **Subtraction needs care** — `(a - b) % m` can go negative in C++/Java; add m before taking mod
7. **Initialize `result = 1 % mod`** — when implementing mod_pow manually, this handles the mod=1 edge case

---

## Practice Problems

### Easy: Count Good Numbers -- LeetCode 1922

A digit string of length n is **good** if digits at even indices are even (0,2,4,6,8 -> 5 choices) and digits at odd indices are prime (2,3,5,7 -> 4 choices). Return the count mod 10^9+7.

```python
def countGoodNumbers(n: int) -> int:
    """
    Even positions (0-indexed): 5 choices each -> ceil(n/2) positions
    Odd positions:  4 choices each -> floor(n/2) positions
    Total = 5^ceil(n/2) * 4^floor(n/2) mod MOD

    Time:  O(log n) -- two modular exponentiations
    Space: O(1)
    """
    MOD = 10**9 + 7
    even_positions = (n + 1) // 2  # ceil(n/2)
    odd_positions = n // 2         # floor(n/2)
    return pow(5, even_positions, MOD) * pow(4, odd_positions, MOD) % MOD


# Test
print(countGoodNumbers(1))    # 5
print(countGoodNumbers(4))    # 400
print(countGoodNumbers(50))   # 564908303
```

### Easy: Count Sorted Vowel Strings -- LeetCode 1641

Given an integer n, return the number of strings of length n that consist only of vowels (a, e, i, o, u) and are lexicographically sorted.

This is a **stars and bars** combinatorics problem: choosing n vowels with repetition from 5 types in non-decreasing order = C(n + 4, 4).

```python
def countVowelStrings(n: int) -> int:
    """
    Stars and bars: placing n identical items into 5 bins = C(n+4, 4).

    For this problem n <= 50 so no mod needed, but the technique
    generalizes to large n with modular arithmetic.

    Time:  O(1)
    Space: O(1)
    """
    from math import comb
    return comb(n + 4, 4)


def countVowelStringsMod(n: int, mod: int) -> int:
    """Modular version for large n."""
    # C(n+4, 4) = (n+4)! / (4! * n!)
    # = (n+1)(n+2)(n+3)(n+4) / 24
    numerator = 1
    for k in range(1, 5):
        numerator = numerator * (n + k) % mod
    return numerator * pow(24, mod - 2, mod) % mod


# Test
print(countVowelStrings(1))   # 5
print(countVowelStrings(2))   # 15
print(countVowelStrings(33))  # 66045
```

### Medium: Pow(x, n) -- LeetCode 50

See [implementation above](#problem-powx-n----leetcode-50).

### Medium: Super Pow -- LeetCode 372

See [implementation above](#problem-super-pow----leetcode-372).

### Medium: Count Unique Paths with Combinatorics -- LeetCode 62

Count paths in an m*n grid from top-left to bottom-right (only move right or down). Instead of DP, use combinatorics: we make exactly (m-1) down moves and (n-1) right moves, so the answer is C(m+n-2, m-1).

```python
def uniquePaths(m: int, n: int) -> int:
    """
    Answer = C(m+n-2, m-1) = (m+n-2)! / ((m-1)! * (n-1)!)

    For small grids this doesn't need modular arithmetic, but the
    technique extends to large grids where the answer must be mod p.

    Time:  O(min(m, n)) with math.comb
    Space: O(1)
    """
    from math import comb
    return comb(m + n - 2, m - 1)


def uniquePathsMod(m: int, n: int, mod: int) -> int:
    """Version for large grids where answer must be returned mod p (p prime)."""
    total = m + n - 2
    choose = m - 1

    # Precompute factorials up to total
    fact = [1] * (total + 1)
    for i in range(1, total + 1):
        fact[i] = fact[i - 1] * i % mod

    inv_fact = [1] * (total + 1)
    inv_fact[total] = pow(fact[total], mod - 2, mod)
    for i in range(total - 1, -1, -1):
        inv_fact[i] = inv_fact[i + 1] * (i + 1) % mod

    return fact[total] * inv_fact[choose] % mod * inv_fact[total - choose] % mod


# Test
print(uniquePaths(3, 7))      # 28
print(uniquePaths(3, 2))      # 3
MOD = 10**9 + 7
print(uniquePathsMod(3, 7, MOD))  # 28
```

### Medium: Count Number of Homogenous Substrings -- LeetCode 1759

A string is **homogenous** if all characters are the same. Given a string s, return the number of homogenous substrings of s, mod 10^9+7.

```python
def countHomogenous(s: str) -> int:
    """
    For a run of k identical characters, the number of homogenous
    substrings is k*(k+1)/2 (choose any contiguous subarray of the run).

    We group consecutive identical characters and sum k*(k+1)/2 for each group.
    Division by 2 uses modular inverse (or we can use the fact that
    one of k or k+1 is even, so integer division works here).

    Time:  O(n)
    Space: O(1)
    """
    MOD = 10**9 + 7
    total = 0
    count = 1  # Length of current run

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            # Add substrings from this run: count*(count+1)//2
            total = (total + count * (count + 1) // 2) % MOD
            count = 1

    # Don't forget the last run
    total = (total + count * (count + 1) // 2) % MOD
    return total


# Test
print(countHomogenous("abbcccaa"))  # 13
# "a"=1, "b","b","bb"=3, "c","c","c","cc","cc","ccc"=6, "a","a","aa"=3 -> 13
print(countHomogenous("xy"))        # 2
print(countHomogenous("zzzzz"))     # 15 (5*6//2)
```

### Medium: Number of Ways to Reorder Array to Get Same BST -- LeetCode 1569

Given an array of distinct integers, count the number of ways to reorder it such that the resulting BST is the same as the BST formed by the original array. Return the answer mod 10^9+7.

```python
def numOfWays(nums: list[int]) -> int:
    """
    Key insight: The root (first element) must stay. The left subtree
    elements must maintain their relative order, same for right subtree.
    But left and right elements can be interleaved in any valid way.

    The number of interleavings of two sequences of lengths L and R
    while preserving relative order = C(L+R, L).

    Recurse on left and right subtrees, multiply results.

    Time:  O(n^2) -- each element processed once per level
    Space: O(n^2) for recursion + combinations
    """
    from math import comb

    MOD = 10**9 + 7

    def count(nodes: list[int]) -> int:
        if len(nodes) <= 2:
            return 1

        root = nodes[0]
        left = [x for x in nodes if x < root]
        right = [x for x in nodes if x > root]

        # Ways to interleave left and right subsequences
        ways = comb(len(left) + len(right), len(left)) % MOD

        # Recurse into subtrees
        return ways * count(left) % MOD * count(right) % MOD

    # Subtract 1 because the problem asks for reorderings OTHER than the original
    return (count(nums) - 1) % MOD


# Test
print(numOfWays([2, 1, 3]))        # 1
print(numOfWays([3, 4, 5, 1, 2]))  # 5
print(numOfWays([1, 2, 3]))        # 0 (only one valid ordering)
```

### Hard: Fancy Sequence -- LeetCode 1622

Implement a data structure that supports `append`, `addAll`, `multAll`, and `getIndex` — all under mod 10^9+7. The tricky part is that `addAll` and `multAll` must be lazy (O(1) per operation), and `getIndex` must reconstruct the correct value using modular inverse.

```python
class Fancy:
    """
    Key insight: track a global affine transformation (multiply, then add).
    At any point, the actual value of every element is: val * M + A
    where M is the cumulative multiplier and A is the cumulative adder.

    When we append(v), we store a normalized value v' such that
    v' * M + A = v, i.e., v' = (v - A) * M^(-1) mod MOD.

    When we addAll(inc), we just do A += inc.
    When we multAll(m), we do M *= m and A *= m.
    When we getIndex(i), we return vals[i] * M + A.

    All operations: O(1) (using Fermat's inverse for append)
    Space: O(n) for stored values
    """
    def __init__(self):
        self.MOD = 10**9 + 7
        self.vals = []
        self.M = 1   # Cumulative multiplier
        self.A = 0   # Cumulative adder

    def append(self, val: int) -> None:
        # Store normalized: v' such that v' * M + A = val
        # v' = (val - A) * M^(-1) mod MOD
        inv_M = pow(self.M, self.MOD - 2, self.MOD)
        normalized = (val - self.A) % self.MOD * inv_M % self.MOD
        self.vals.append(normalized)

    def addAll(self, inc: int) -> None:
        self.A = (self.A + inc) % self.MOD

    def multAll(self, m: int) -> None:
        self.M = self.M * m % self.MOD
        self.A = self.A * m % self.MOD

    def getIndex(self, idx: int) -> int:
        if idx >= len(self.vals):
            return -1
        return (self.vals[idx] * self.M + self.A) % self.MOD


# Test
fancy = Fancy()
fancy.append(2)     # [2]
fancy.addAll(3)     # [5]
fancy.append(7)     # [5, 7]
fancy.multAll(2)    # [10, 14]
print(fancy.getIndex(0))  # 10
fancy.addAll(3)     # [13, 17]
fancy.append(10)    # [13, 17, 10]
fancy.multAll(2)    # [26, 34, 20]
print(fancy.getIndex(0))  # 26
print(fancy.getIndex(1))  # 34
print(fancy.getIndex(2))  # 20
```

### Hard: Count Anagrams -- LeetCode 2514

Given a string s of words separated by spaces, return the number of distinct anagrams of s, mod 10^9+7. An anagram rearranges letters within each word independently.

```python
def countAnagrams(s: str) -> int:
    """
    For each word, the number of distinct permutations is:
        len(word)! / (freq[c1]! * freq[c2]! * ...)

    Multiply across all words. Use modular inverse for division.

    Time:  O(n) where n = total characters
    Space: O(n) for factorial precomputation
    """
    from collections import Counter

    MOD = 10**9 + 7
    words = s.split()

    # Precompute factorials up to max word length
    max_len = max(len(w) for w in words)
    fact = [1] * (max_len + 1)
    for i in range(1, max_len + 1):
        fact[i] = fact[i - 1] * i % MOD

    # Precompute inverse factorials
    inv_fact = [1] * (max_len + 1)
    inv_fact[max_len] = pow(fact[max_len], MOD - 2, MOD)
    for i in range(max_len - 1, -1, -1):
        inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD

    result = 1
    for word in words:
        freq = Counter(word)
        # Numerator: len(word)!
        result = result * fact[len(word)] % MOD
        # Denominator: product of freq[c]! for each character
        for count in freq.values():
            result = result * inv_fact[count] % MOD

    return result


# Test
print(countAnagrams("too hot"))    # 18
print(countAnagrams("aa"))         # 1
print(countAnagrams("abcd efgh"))  # 576 (24 * 24)
```

### Hard: Matrix Exponentiation for Linear Recurrences

Not a single LeetCode problem, but a powerful technique that combines modular arithmetic with matrix multiplication. Any linear recurrence (Fibonacci, Tribonacci, etc.) can be computed in O(k^3 log n) where k is the order of the recurrence.

```python
def matrix_mult(A: list[list[int]], B: list[list[int]], mod: int) -> list[list[int]]:
    """Multiply two k*k matrices mod m."""
    k = len(A)
    C = [[0] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            for p in range(k):
                C[i][j] = (C[i][j] + A[i][p] * B[p][j]) % mod
    return C


def matrix_pow(M: list[list[int]], n: int, mod: int) -> list[list[int]]:
    """Compute M^n mod m using binary exponentiation on matrices."""
    k = len(M)
    # Identity matrix
    result = [[1 if i == j else 0 for j in range(k)] for i in range(k)]

    while n > 0:
        if n & 1:
            result = matrix_mult(result, M, mod)
        M = matrix_mult(M, M, mod)
        n >>= 1

    return result


def fibonacci_mod(n: int, mod: int) -> int:
    """
    Compute the n-th Fibonacci number mod m in O(log n) time.

    The recurrence F(n) = F(n-1) + F(n-2) can be expressed as:
    [F(n+1)]   [1 1]^n   [F(1)]
    [F(n)  ] = [1 0]   * [F(0)]

    Time:  O(k^3 * log n) where k=2 for Fibonacci -> O(log n)
    Space: O(k^2) -> O(1)
    """
    if n <= 1:
        return n % mod

    M = [[1, 1],
         [1, 0]]
    result = matrix_pow(M, n, mod)
    return result[0][1]  # F(n) is at position [0][1] (or equivalently [1][0])


# Test
MOD = 10**9 + 7
print(fibonacci_mod(10, MOD))       # 55
print(fibonacci_mod(100, MOD))      # 687995182
print(fibonacci_mod(10**18, MOD))   # Computes instantly!
```

---

## When NOT to Use Modular Arithmetic

1. **When results fit in normal integers** — don't add complexity if overflow isn't a risk
2. **When you need actual values** — mod loses information; you can't recover the original
3. **When m isn't prime and you need division** — modular inverse only exists when gcd(a, m) = 1; consider restructuring the computation
4. **When comparing magnitudes** — (a mod m) > (b mod m) does NOT imply a > b
5. **When debugging** — mod operations make debugging harder; test without mod first, then add it

---

## Related Sections

- [GCD and LCM](./01-gcd-lcm.md) — Extended GCD for modular inverse
- [Prime Numbers](./02-prime-numbers.md) — Prime modulus properties, Fermat's little theorem
