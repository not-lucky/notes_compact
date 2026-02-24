# Chapter 16: Math for Interviews

## Building Intuition

**The "Mathematical Shortcut" Mental Model**

Think of math in interviews as a superpower that turns complex problems into simple calculations:

```
Without math:                     With math:
Sum 1 to n → Loop n times O(n)    Use n*(n+1)/2 → O(1)
Check power of 2 → Divide loop    Use n & (n-1) == 0 → O(1)
Count primes to n → Check each    Use Sieve → O(n log log n)
```

**Why Math Matters**

Interview math isn't about showing off—it's about recognizing patterns:

- When you see "divisibility," think GCD/LCM
- When you see "overflow," think modular arithmetic
- When you see "random selection from stream," think reservoir sampling

**The Hidden Costs**

Watch for operations that seem O(1) but aren't:

- `x in list` is O(n), not O(1)
- String concatenation in a loop is O(n²)
- Naive primality check is O(n), not O(√n)

---

## Why Math Matters for Interviews

1. **Interview frequency**: Appears in ~8-12% of FANG interviews
2. **Foundation**: Many algorithms rely on mathematical properties
3. **Edge cases**: Math problems test attention to overflow, zero, and negative numbers
4. **Elegant solutions**: Often allows O(1) or O(log n) solutions to seemingly complex problems

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
3. **When you don't understand the formula**: Using math you can't explain is risky
4. **When edge cases multiply**: Math formulas often break for 0, negatives, or boundaries
5. **When debugging is hard**: Loops are easier to trace than formulas

**The golden rule**: If you use a math formula, be ready to explain WHY it works.

---

## Chapter Contents

| #   | Topic                                            | Key Concepts                                    |
| --- | ------------------------------------------------ | ----------------------------------------------- |
| 01  | [GCD and LCM](./01-gcd-lcm.md)                   | Euclidean algorithm, applications               |
| 02  | [Prime Numbers](./02-prime-numbers.md)           | Primality check, Sieve of Eratosthenes          |
| 03  | [Modular Arithmetic](./03-modular-arithmetic.md) | Mod operations, overflow handling               |
| 04  | [Random Sampling](./04-random-sampling.md)       | Reservoir sampling, Fisher-Yates shuffle        |
| 05  | [Square Root Problems](./05-sqrt-problems.md)    | Integer sqrt, perfect square checks             |
| 06  | [Number Properties](./06-number-properties.md)   | Palindrome, reverse integer, digit manipulation |

---

## Implementation Template: Common Math Operations

```python
import math
from typing import List

class MathOperations:
    """
    Common mathematical operations for interviews.
    """

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Greatest Common Divisor using Euclidean algorithm.
        Time: O(log(min(a, b)))
        Space: O(1)
        """
        while b:
            a, b = b, a % b
        return abs(a)

    @staticmethod
    def lcm(a: int, b: int) -> int:
        """
        Least Common Multiple.
        Time: O(log(min(a, b)))
        Space: O(1)
        """
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // MathOperations.gcd(a, b)

    @staticmethod
    def is_prime(n: int) -> bool:
        """
        Check if n is prime.
        Time: O(sqrt(n))
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
        Modular exponentiation: (base^exp) % mod
        Time: O(log exp)
        Space: O(1)
        """
        if mod == 1:
            return 0
        result = 1
        base %= mod
        while exp > 0:
            if exp & 1:
                result = (result * base) % mod
            exp >>= 1
            base = (base * base) % mod
        return result

    @staticmethod
    def integer_sqrt(n: int) -> int:
        """
        Integer square root (floor of sqrt(n)).
        Time: O(log n)
        Space: O(1)
        """
        if n < 0:
            raise ValueError("Square root of negative number")
        if n < 2:
            return n
        left, right = 1, n
        while left <= right:
            mid = left + (right - left) // 2
            if mid * mid == n:
                return mid
            elif mid * mid < n:
                left = mid + 1
            else:
                right = mid - 1
        return right


# Example usage
print(MathOperations.gcd(48, 18))        # 6
print(MathOperations.lcm(4, 6))          # 12
print(MathOperations.is_prime(17))       # True
print(MathOperations.mod_pow(2, 10, 1000))  # 24
print(MathOperations.integer_sqrt(50))    # 7
```

---

## Common Mistakes

1. **Integer overflow**: Use modular arithmetic or Python's arbitrary precision
2. **Off-by-one in ranges**: `range(2, n+1)` vs `range(2, n)`
3. **Forgetting zero/negative**: Many formulas break for n ≤ 0
4. **Floating point errors**: `int(math.sqrt(n))` may be off by 1; verify!
5. **Division by zero**: Always check denominator before dividing

---

## Time Complexity Analysis

| Operation              | Time           | Space | Notes                   |
| ---------------------- | -------------- | ----- | ----------------------- |
| GCD (Euclidean)        | O(log n)       | O(1)  | Iterative version       |
| Primality check        | O(√n)          | O(1)  | Trial division          |
| Sieve of Eratosthenes  | O(n log log n) | O(n)  | Generate all primes ≤ n |
| Modular exponentiation | O(log exp)     | O(1)  | Binary exponentiation   |
| Integer square root    | O(log n)       | O(1)  | Binary search           |

---

## Interview Tips

1. **Start with brute force**: Show you understand the problem
2. **Optimize with math**: Many O(n) solutions become O(1) with formulas
3. **Watch for edge cases**: 0, 1, negative numbers, overflow
4. **Know Python shortcuts**: `math.gcd()`, `math.isqrt()`, `pow(a, b, mod)`
5. **Verify with examples**: Work through a small example to catch errors

---

## Classic Interview Problems by Company

| Company   | Favorite Math Problems                             |
| --------- | -------------------------------------------------- |
| Google    | Pow(x, n), Happy Number, Count Primes              |
| Meta      | Reverse Integer, Palindrome Number, Add Digits     |
| Amazon    | Valid Perfect Square, Sqrt(x), Excel Column Number |
| Microsoft | GCD of Strings, Ugly Number, Power of Three        |
| Apple     | Plus One, Missing Number, Integer to Roman         |

---

## Math Problem Signals

Look for these keywords/patterns:

```
- "Divisible by" → GCD/LCM or modulo
- "Simplify fraction" → GCD
- "Random selection" → Reservoir sampling
- "Large numbers/overflow" → Modular arithmetic
- "Is it a perfect ___" → Square root or divisibility
- "Reverse/palindrome" → Digit manipulation
- "Count primes up to n" → Sieve
- "Power of X" → Logarithm or repeated division
```

---

## Comparison: When to Use Math vs Other Approaches

| Scenario             | Use Math           | Use Alternative          |
| -------------------- | ------------------ | ------------------------ |
| Sum 1 to n           | `n*(n+1)//2`       | Loop (slower)            |
| Check power of 2     | `n & (n-1) == 0`   | Loop or log              |
| Random k from stream | Reservoir sampling | Store all (if memory ok) |
| Find if prime        | Trial division     | Sieve (if checking many) |
| Integer sqrt         | Binary search      | `math.isqrt()` (simpler) |

---

## Start: [01-gcd-lcm.md](./01-gcd-lcm.md)

Begin with GCD and LCM—the most frequently asked math concepts in interviews.
