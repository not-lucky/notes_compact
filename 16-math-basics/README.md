# Chapter 16: Math for Interviews

## Building Intuition

**The "Mathematical Shortcut" Mental Model**

Think of math in interviews as a tool that turns brute-force problems into direct calculations:

```
Without math:                      With math:
Sum 1 to n -> Loop n times O(n)     Use n*(n+1)//2 -> O(1)
Check power of 2 -> Divide loop     Use n > 0 and n & (n-1) == 0 -> O(1)
Count primes to n -> Check each     Use Sieve -> O(n log log n)
```

**Why Math Matters**

1. **Interview frequency**: Appears in ~8-12% of FAANG interviews
2. **Foundation**: Many algorithms rely on mathematical properties (hashing, graph weights, DP transitions)
3. **Edge cases**: Math problems test attention to overflow, zero, and negative numbers
4. **Elegant solutions**: Often reduces O(n) solutions to O(1) with a formula

**Pattern Recognition**

Interview math isn't about showing off -- it's about recognizing which tool fits:

- When you see "divisibility" -> think GCD/LCM
- When you see "overflow" or "large numbers" -> think modular arithmetic
- When you see "random selection from stream" -> think reservoir sampling

**Common Complexity Traps**

Watch for operations whose actual cost is worse than they appear:

- `x in list` is O(n), not O(1) -- use a `set` for O(1) lookup
- String concatenation in a loop is O(n^2) -- use `"".join(parts)` instead
- Naive primality check (dividing up to n) is O(n) -- checking up to sqrt(n) reduces it to O(sqrt(n))

---

## Core Mathematical Concepts for Interviews

| Concept            | Why It Matters                            | Example Problem                       |
| ------------------ | ----------------------------------------- | ------------------------------------- |
| GCD/LCM            | Array operations, fraction simplification | Simplify fractions, water jug problem |
| Prime Numbers      | Factorization, divisibility               | Count primes, ugly numbers            |
| Modular Arithmetic | Large number handling, hash functions     | Pow(x, n), string hashing             |
| Random Sampling    | Fair selection from streams               | Reservoir sampling, shuffle           |
| Square Root        | Search problems, number properties        | Valid perfect square, sqrt(x)         |
| Number Properties  | Digit manipulation                        | Palindrome number, reverse integer    |

---

## When to Use Math in Interviews

### Strong Indicators (Use Math)

1. **"Divisibility"**: GCD, LCM, or prime factorization
2. **"Large numbers"**: Modular arithmetic to prevent overflow
3. **"Random selection"**: Reservoir sampling or Fisher-Yates
4. **"Find if number is X"**: Number property checks
5. **"Simplify fraction"**: GCD to reduce to lowest terms
6. **"Count primes"**: Sieve of Eratosthenes

### Weak Indicators (Consider Alternatives)

1. **Complex expressions**: Sometimes DP or brute force is clearer
2. **Unknown constraints**: Verify if math approach handles all cases
3. **Floating point precision**: Use integer math when possible

---

## When NOT to Use Math Tricks

1. **When clarity matters more**: A simple loop is often better than a clever formula
2. **When constraints are small**: For n < 100, brute force is fine and more readable
3. **When you can't explain the formula**: Using math you can't derive or justify is risky in an interview
4. **When edge cases multiply**: Math formulas often break for 0, negatives, or boundary values
5. **When debugging is hard**: Loops are easier to step through than closed-form formulas

> **Golden rule**: If you use a math formula, be ready to explain *why* it works and *when* it breaks.

---

## Chapter Contents

| #  | Topic | What's Covered | Key Interview Problems |
| -- | ----- | -------------- | ---------------------- |
| 01 | [GCD and LCM](./01-gcd-lcm.md) | Euclidean algorithm (iterative & recursive), extended GCD and Bezout's identity, LCM via GCD, GCD/LCM of arrays. Why `gcd(a, b) = gcd(b, a % b)` works and why it runs in O(log min(a,b)). | GCD of Strings (LC 1071), Water Jug (LC 365), Nth Magical Number (LC 878) |
| 02 | [Prime Numbers](./02-prime-numbers.md) | Trial division with 6k+/-1 optimization, Sieve of Eratosthenes (why marking starts from i^2), prime factorization, smallest prime factor sieve for batch factorization, divisor counting. | Count Primes (LC 204), Ugly Number I/II (LC 263/264), Largest Component by Common Factor (LC 952) |
| 03 | [Modular Arithmetic](./03-modular-arithmetic.md) | Binary exponentiation, modular inverse via Fermat's little theorem and extended GCD, why 10^9+7, division under modulus, rolling hash (Rabin-Karp), precomputed factorials for nCr mod p. | Pow(x, n) (LC 50), Super Pow (LC 372), Count Good Numbers (LC 1922), Fancy Sequence (LC 1622) |
| 04 | [Random Sampling](./04-random-sampling.md) | Reservoir sampling (k=1 and general k) with telescoping probability proof, Fisher-Yates shuffle (why naive shuffle is biased), weighted random selection via prefix sum + binary search, blacklist remapping. | Linked List Random Node (LC 382), Shuffle Array (LC 384), Random Pick with Weight (LC 528), Random Pick with Blacklist (LC 710) |
| 05 | [Square Root Problems](./05-sqrt-problems.md) | Integer sqrt via binary search and Newton's method (quadratic convergence), perfect square checks, the sqrt-as-balance-point insight (why primality checks only go to sqrt(n)), sum of squares (two-pointer), and search-on-answer patterns. | Sqrt(x) (LC 69), Valid Perfect Square (LC 367), Perfect Squares (LC 279), Smallest Good Base (LC 483) |
| 06 | [Number Properties](./06-number-properties.md) | Digit extraction without string conversion (`n % 10`, `n // 10`), overflow-safe integer reversal, half-reversal palindrome check, digital root formula, power-of-2/3/4 bit tricks, bijective base-26 (Excel columns), carry propagation, Roman numeral conversion. | Palindrome Number (LC 9), Reverse Integer (LC 7), Integer to Roman (LC 12), Multiply Strings (LC 43) |

---

## Implementation Template: Common Math Operations

```python
import math
from typing import List

class MathOperations:
    """Common mathematical operations for coding interviews."""

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Greatest Common Divisor using the Euclidean algorithm.

        The key insight: gcd(a, b) == gcd(b, a % b), and gcd(a, 0) == a.
        We use abs() to handle negative inputs correctly.

        Time:  O(log(min(a, b)))
        Space: O(1)

        Note: In interviews, you can use math.gcd() from the stdlib.
        """
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def lcm(a: int, b: int) -> int:
        """
        Least Common Multiple.

        Uses the identity: lcm(a, b) = |a * b| / gcd(a, b).
        We divide before multiplying to reduce overflow risk in other languages,
        though Python handles big integers natively.

        Time:  O(log(min(a, b)))  -- dominated by the GCD call
        Space: O(1)

        Note: In Python 3.9+, you can use math.lcm().
        """
        if a == 0 or b == 0:
            return 0
        return abs(a // MathOperations.gcd(a, b) * b)

    @staticmethod
    def is_prime(n: int) -> bool:
        """
        Check if n is prime using optimized trial division.

        Optimization: after checking 2 and 3, all primes are of the form
        6k +/- 1. So we only test divisors of that form, stepping by 6.

        Time:  O(sqrt(n))
        Space: O(1)
        """
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    @staticmethod
    def mod_pow(base: int, exp: int, mod: int) -> int:
        """
        Modular exponentiation: (base^exp) % mod using binary exponentiation.

        Processes the exponent bit-by-bit from LSB to MSB:
        - If the current bit is 1, multiply result by current base.
        - Square the base each iteration.

        Time:  O(log exp)
        Space: O(1)

        Note: Python's built-in pow(base, exp, mod) does the same thing.
        """
        if mod == 1:
            return 0
        result = 1
        base %= mod
        while exp > 0:
            if exp & 1:  # current bit is set
                result = (result * base) % mod
            exp >>= 1
            base = (base * base) % mod
        return result

    @staticmethod
    def integer_sqrt(n: int) -> int:
        """
        Integer square root -- returns floor(sqrt(n)) using binary search.

        Time:  O(log n)
        Space: O(1)

        Note: In Python 3.8+, you can use math.isqrt(n) instead.
        """
        if n < 0:
            raise ValueError("Square root of negative number")
        if n < 2:
            return n
        # Upper bound: n // 2 is sufficient for n >= 4, tighter than n
        left, right = 1, n // 2
        while left <= right:
            mid = left + (right - left) // 2
            square = mid * mid
            if square == n:
                return mid
            elif square < n:
                left = mid + 1
            else:
                right = mid - 1
        return right


# --- Example usage ---
if __name__ == "__main__":
    print(MathOperations.gcd(48, 18))           # 6
    print(MathOperations.lcm(4, 6))             # 12
    print(MathOperations.is_prime(17))           # True
    print(MathOperations.mod_pow(2, 10, 1000))   # 24  (2^10 = 1024, 1024 % 1000 = 24)
    print(MathOperations.integer_sqrt(50))        # 7   (floor(sqrt(50)) = 7)
```

---

## Common Mistakes

1. **Integer overflow**: Not an issue in Python (arbitrary precision), but matters if porting to Java/C++. Use modular arithmetic when the problem requires it.
2. **Off-by-one in ranges**: `range(2, n+1)` includes `n`; `range(2, n)` excludes it. Know which you need.
3. **Forgetting zero/negative inputs**: Many formulas break for n <= 0. Always handle these explicitly.
4. **Floating point errors**: `int(math.sqrt(n))` can be off by 1 due to rounding. Use `math.isqrt(n)` (Python 3.8+) or verify with `result * result <= n`.
5. **Division by zero**: Always check the denominator before dividing.
6. **Power-of-2 check missing n > 0**: `n & (n-1) == 0` is `True` when `n == 0`. The correct check is `n > 0 and n & (n-1) == 0`.

---

## Time Complexity Reference

| Operation              | Time            | Space | Notes                              |
| ---------------------- | --------------- | ----- | ---------------------------------- |
| GCD (Euclidean)        | O(log min(a,b)) | O(1)  | Iterative version                  |
| Primality check        | O(sqrt(n))      | O(1)  | Trial division (6k+/-1 optimization) |
| Sieve of Eratosthenes  | O(n log log n)  | O(n)  | Generates all primes up to n       |
| Modular exponentiation | O(log exp)      | O(1)  | Binary exponentiation              |
| Integer square root    | O(log n)        | O(1)  | Binary search                      |
| Newton's method sqrt   | O(log log n)    | O(1)  | Quadratic convergence              |

---

## Interview Tips

1. **Start with brute force**: Show you understand the problem before optimizing
2. **Optimize with math**: Mention the formula, explain why it's correct, then use it
3. **Watch for edge cases**: 0, 1, negative numbers, very large inputs
4. **Know Python stdlib shortcuts**: `math.gcd()`, `math.lcm()` (3.9+), `math.isqrt()` (3.8+), `pow(a, b, mod)`
5. **Verify with examples**: Work through a small case by hand to confirm your formula

---

## Classic Interview Problems by Company

| Company   | Favorite Math Problems                             |
| --------- | -------------------------------------------------- |
| Google    | Pow(x, n), Happy Number, Count Primes              |
| Meta      | Reverse Integer, Palindrome Number, Add Digits     |
| Amazon    | Valid Perfect Square, Sqrt(x), Excel Column Number |
| Microsoft | GCD of Strings, Ugly Number, Power of Three        |
| Apple     | Plus One, Missing Number, Integer to Roman          |

> These are common patterns, not guarantees. Focus on understanding the underlying math, not memorizing company-specific lists.

---

## Math Problem Signals

Look for these keywords and patterns in problem statements:

| Signal in Problem          | Technique to Consider          |
| -------------------------- | ------------------------------ |
| "Divisible by"             | GCD/LCM or modulo              |
| "Simplify fraction"        | GCD                            |
| "Random selection"         | Reservoir sampling             |
| "Large numbers / overflow" | Modular arithmetic             |
| "Is it a perfect ___"      | Square root or divisibility    |
| "Reverse / palindrome"     | Digit manipulation             |
| "Count primes up to n"     | Sieve of Eratosthenes          |
| "Power of X"               | Logarithm or repeated division |
| "Return answer mod 10^9+7" | Modular arithmetic             |

---

## Comparison: Math vs Other Approaches

| Scenario             | Math Approach                             | Alternative                              |
| -------------------- | ----------------------------------------- | ---------------------------------------- |
| Sum 1 to n           | `n * (n + 1) // 2` -- O(1)               | Loop -- O(n)                             |
| Check power of 2     | `n > 0 and n & (n-1) == 0` -- O(1)       | Repeated division -- O(log n)            |
| Random k from stream | Reservoir sampling -- O(n)                | Store all, then sample -- O(n) memory    |
| Is n prime?          | Trial division -- O(sqrt(n))              | Sieve -- O(n log log n) setup, O(1) query |
| Integer sqrt         | Binary search -- O(log n)                 | `math.isqrt()` -- simpler, same complexity |
| nCr mod p            | Precomputed factorials -- O(n) setup, O(1) query | Naive computation -- O(n) per query |

---

## Next: [01-gcd-lcm.md](./01-gcd-lcm.md)

Begin with GCD and LCM -- the most frequently asked math concepts in interviews.
