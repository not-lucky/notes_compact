# Practice Problems: Modular Arithmetic

This file contains optimal Python solutions for the practice problems listed in the Modular Arithmetic notes.

---

## 1. Pow(x, n)

**Problem Statement:**
Implement `pow(x, n)`, which calculates $x$ raised to the power $n$ (i.e., $x^n$).

**Examples & Edge Cases:**

- **Example 1:** `x = 2.0, n = 10` -> Output: `1024.0`
- **Example 2:** `x = 2.1, n = 3` -> Output: `9.261`
- **Example 3:** `x = 2.0, n = -2` -> Output: `0.25` ($2^{-2} = 1/4 = 0.25$)
- **Edge Case:** `n = 0` -> Output: `1.0`
- **Edge Case:** `n` is the minimum possible 32-bit integer (handled naturally in Python).

**Optimal Python Solution:**

```python
def myPow(x: float, n: int) -> float:
    """
    Computes x^n using binary exponentiation (Square and Multiply).
    """
    # Base case
    if n == 0:
        return 1.0

    # Handle negative power
    if n < 0:
        x = 1 / x
        n = -n

    res = 1.0
    current_product = x

    while n > 0:
        # If n is odd, multiply the result by current_product
        if n % 2 == 1:
            res *= current_product

        # Square the product and halve n
        current_product *= current_product
        n //= 2

    return res
```

**Explanation:**

1. **Binary Exponentiation**: Instead of multiplying $x$ by itself $n$ times, we use the binary representation of $n$. For example, $x^{13} = x^8 \cdot x^4 \cdot x^1$.
2. **Efficiency**: In each step, we either square the current value or multiply the result. This reduces the number of operations from $O(n)$ to $O(\log n)$.
3. **Negative Exponents**: If $n$ is negative, $x^n$ is equivalent to $(1/x)^{-n}$.

**Complexity Analysis:**

- **Time Complexity:** $O(\log n)$ because $n$ is halved in each iteration.
- **Space Complexity:** $O(1)$ as we use a constant amount of extra space.

---

## 2. Super Pow

**Problem Statement:**
Your task is to calculate $a^b \pmod{1337}$ where $a$ is a positive integer and $b$ is an extremely large positive integer given in the form of an array.

**Examples & Edge Cases:**

- **Example 1:** `a = 2, b = [3]` -> Output: `8`
- **Example 2:** `a = 2, b = [1,0]` -> Output: `1024`
- **Example 3:** `a = 1, b = [4,3,3,8,5,2]` -> Output: `1`
- **Edge Case:** `a` is large -> Use `a % 1337`.

**Optimal Python Solution:**

```python
def superPow(a: int, b: list[int]) -> int:
    """
    Computes a^b % 1337 using properties of modular exponentiation.
    a^1234 % m = (a^1230 % m * a^4 % m) % m
               = ((a^123 % m)^10 % m * a^4 % m) % m
    """
    MOD = 1337

    def quick_pow(base, power):
        res = 1
        base %= MOD
        while power > 0:
            if power % 2 == 1:
                res = (res * base) % MOD
            base = (base * base) % MOD
            power //= 2
        return res

    if not b:
        return 1

    last_digit = b.pop()
    # Recursive step: a^b = (a^(b//10))^10 * a^(b%10)
    return (quick_pow(superPow(a, b), 10) * quick_pow(a, last_digit)) % MOD
```

**Explanation:**

1. **Mathematical Property**: We use the property $a^{1234} = (a^{123})^{10} \cdot a^4$.
2. **Recursion**: We process the array `b` from the last element. The result of the rest of the array is raised to the 10th power, then multiplied by $a$ raised to the last digit.
3. **Modular Arithmetic**: Apply `% 1337` at every multiplication to prevent overflow and keep numbers small.

**Complexity Analysis:**

- **Time Complexity:** $O(L \cdot \log 10)$, where $L$ is the length of array $b$. We perform a constant number of modular exponentiations for each digit.
- **Space Complexity:** $O(L)$ due to the recursion stack.

---

## 3. Count Good Numbers

**Problem Statement:**
A digit string is good if the digits at even indices are even (0, 2, 4, 6, 8) and the digits at odd indices are prime (2, 3, 5, 7). Given an integer `n`, return the total number of good digit strings of length `n`. Since the answer may be large, return it modulo $10^9 + 7$.

**Examples & Edge Cases:**

- **Example 1:** `n = 1` -> Output: `5` (Strings: "0", "2", "4", "6", "8")
- **Example 2:** `n = 4` -> Output: `400`
- **Example 3:** `n = 50` -> Output: `564908303`
- **Edge Case:** Large $n$ (up to $10^{15}$) -> Requires $O(\log n)$ modular exponentiation.

**Optimal Python Solution:**

```python
def countGoodNumbers(n: int) -> int:
    """
    Counts good numbers using modular exponentiation.
    Even positions (0, 2, ...): 5 choices (0, 2, 4, 6, 8)
    Odd positions (1, 3, ...): 4 choices (2, 3, 5, 7)
    """
    MOD = 10**9 + 7

    # Number of even and odd positions
    even_pos = (n + 1) // 2
    odd_pos = n // 2

    # Total combinations = (5^even_pos * 4^odd_pos) % MOD
    # Use Python's built-in pow(base, exp, mod) for O(log n)
    return (pow(5, even_pos, MOD) * pow(4, odd_pos, MOD)) % MOD
```

**Explanation:**

1. **Combinatorics**: For each even index, there are 5 choices. For each odd index, there are 4 choices.
2. **Total Product**: The result is $5^{\text{even\_count}} \cdot 4^{\text{odd\_count}}$.
3. **Efficiency**: Since $n$ can be extremely large, we must use modular exponentiation ($O(\log n)$) instead of a simple loop. Python's `pow(a, b, m)` is highly optimized for this.

**Complexity Analysis:**

- **Time Complexity:** $O(\log n)$ for the two calls to `pow`.
- **Space Complexity:** $O(1)$.

---

## 4. String Hashing (Substring Search)

**Problem Statement:**
Implement a function to find the index of the first occurrence of `pattern` in `text` using the Rabin-Karp rolling hash algorithm.

**Examples & Edge Cases:**

- **Example 1:** `text = "sadbutsad", pattern = "sad"` -> Output: `0`
- **Example 2:** `text = "leetcode", pattern = "leeto"` -> Output: `-1`
- **Edge Case:** `pattern` is longer than `text`.
- **Edge Case:** Empty strings.

**Optimal Python Solution:**

```python
def strStr(text: str, pattern: str) -> int:
    """
    Rabin-Karp algorithm for string matching using rolling hash.
    """
    n, m = len(text), len(pattern)
    if m == 0: return 0
    if m > n: return -1

    # Constants for hashing
    BASE = 31
    MOD = 10**9 + 7

    # Precompute BASE^m % MOD
    max_pow = pow(BASE, m, MOD)

    # Initial hashes
    pattern_hash = 0
    window_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * BASE + ord(pattern[i])) % MOD
        window_hash = (window_hash * BASE + ord(text[i])) % MOD

    # Slide the window
    for i in range(n - m + 1):
        # Check if hashes match (verify strings to handle collisions)
        if window_hash == pattern_hash:
            if text[i : i + m] == pattern:
                return i

        # Roll the hash to the next window
        if i < n - m:
            window_hash = (window_hash * BASE - ord(text[i]) * max_pow + ord(text[i + m])) % MOD
            # Ensure window_hash is positive
            if window_hash < 0:
                window_hash += MOD

    return -1
```

**Explanation:**

1. **Rolling Hash**: Instead of recomputing the hash of the substring from scratch, we "roll" it by removing the contribution of the leftmost character and adding the new character on the right.
2. **Mathematical Formula**: `new_hash = (old_hash * BASE - leftmost_char * BASE^m + rightmost_char) % MOD`.
3. **Collision Handling**: Since different strings can have the same hash, we perform a direct string comparison if the hashes match.

**Complexity Analysis:**

- **Time Complexity:** $O(n + m)$ average case. $O(n \cdot m)$ in the worst case (many collisions), but extremely rare with a good prime modulus.
- **Space Complexity:** $O(1)$ additional space beyond input.

---

## 5. Unique Paths (Large Grid)

**Problem Statement:**
A robot is located at the top-left corner of a $m \times n$ grid. The robot can only move either down or right. Find the number of possible unique paths to the bottom-right corner. Since $m$ and $n$ can be large, return the result modulo $10^9 + 7$.

**Examples & Edge Cases:**

- **Example 1:** `m = 3, n = 7` -> Output: `28`
- **Example 2:** `m = 3, n = 2` -> Output: `3`
- **Edge Case:** `m = 1` or `n = 1` -> Output: `1`.

**Optimal Python Solution:**

```python
def uniquePaths(m: int, n: int) -> int:
    """
    Computes (m+n-2) choose (m-1) mod 10^9 + 7.
    Uses modular inverse for division.
    """
    MOD = 10**9 + 7

    # We need to compute (N) choose (K)
    N = m + n - 2
    K = min(m - 1, n - 1)

    if K == 0:
        return 1

    numerator = 1
    denominator = 1

    # Calculate N! / (K! * (N-K)!) -> (N * N-1 * ... * N-K+1) / K!
    for i in range(K):
        numerator = (numerator * (N - i)) % MOD
        denominator = (denominator * (i + 1)) % MOD

    # Division mod M: multiply by modular inverse
    # Since MOD is prime, we use Fermat's Little Theorem: a^(M-2) % M
    return (numerator * pow(denominator, MOD - 2, MOD)) % MOD
```

**Explanation:**

1. **Combinatorial Formula**: The total number of steps is $(m-1) + (n-1)$. We need to choose which $m-1$ steps are "down" (or $n-1$ are "right"). This is $\binom{m+n-2}{m-1}$.
2. **Modular Division**: To calculate $\frac{A}{B} \pmod M$, we calculate $A \cdot B^{-1} \pmod M$.
3. **Modular Inverse**: For a prime $M$, $B^{-1} \equiv B^{M-2} \pmod M$.

**Complexity Analysis:**

- **Time Complexity:** $O(\min(m, n) + \log \text{MOD})$.
- **Space Complexity:** $O(1)$.
