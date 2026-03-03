# Number Properties

> **Prerequisites:** None (standalone topic)

## Building Intuition

### The "Digit Surgery" Mental Model

Working with digits is like surgery on numbers -- three fundamental operations:

- **Extract** last digit: `n % 10` (scalpel)
- **Remove** last digit: `n // 10` (amputation)
- **Build** a number digit by digit: `result = result * 10 + digit` (reconstruction)

```
Extract digits from 123:
  123 % 10 = 3,  123 // 10 = 12
   12 % 10 = 2,   12 // 10 = 1
    1 % 10 = 1,    1 // 10 = 0  (done)

Digits extracted: 3, 2, 1 (right to left)
```

**Why this works:** The decimal system represents numbers as sums of powers of 10.
`123 = 1*100 + 2*10 + 3`. Modding by 10 isolates the ones place; integer-dividing
by 10 shifts every digit one position right, dropping the last one.

### The Overflow Trap

When reversing integers, the result can overflow:

- 32-bit signed int max: 2,147,483,647
- Reversing 1,000,000,009 gives 9,000,000,001 -- overflow!

**Critical rule:** Always check BEFORE the operation that would cause overflow,
not after. Once you've overflowed (in languages like C/Java), the damage is done.

> **Python note:** Python has arbitrary-precision integers, so overflow never
> actually happens. But interview problems (LeetCode 7) still require you to
> detect when the result *would* exceed 32-bit range and return 0.

### Bit Tricks for Powers

Powers of 2, 3, and 4 have elegant constant-time checks:

- **Power of 2:** Exactly one bit set in binary -> `n & (n - 1) == 0`
- **Power of 4:** Power of 2 AND the single bit is at an *even* position (0, 2, 4, ...) -> additionally check `n & 0x55555555 != 0`
- **Power of 3:** 3^19 = 1,162,261,467 is the largest power of 3 fitting in a 32-bit signed int. Since 3 is prime, any power of 3 divides 3^19 -> `1162261467 % n == 0`

---

## Interview Context

Number property problems test:

- Digit manipulation without converting to string
- Integer overflow awareness
- Edge case handling (negative numbers, zero, boundaries)
- Mathematical reasoning and pattern recognition

Common problems: palindrome number, reverse integer, happy number, and power-of-X checks.

---

## Pattern: Digit Extraction

Extract digits from a number without converting to string.

```
123 -> digits 1, 2, 3

Extract from right (easiest):
  123 % 10 = 3    (last digit)
  123 // 10 = 12  (remove last digit)

   12 % 10 = 2
   12 // 10 = 1

    1 % 10 = 1
    1 // 10 = 0   (done)

Digits from right: 3, 2, 1
```

### Implementation

```python
def extract_digits(n: int) -> list[int]:
    """
    Extract digits from right to left.

    Time:  O(d) where d = number of digits = O(log n)
    Space: O(d) to store digits
    """
    if n == 0:
        return [0]

    n = abs(n)  # Handle negatives by working with magnitude
    digits = []

    while n:
        digits.append(n % 10)
        n //= 10

    return digits  # Right-to-left order; reverse for left-to-right


def digit_count(n: int) -> int:
    """Count number of digits in n. O(log n) time, O(1) space."""
    if n == 0:
        return 1
    n = abs(n)
    count = 0
    while n:
        count += 1
        n //= 10
    return count


# Test
print(extract_digits(123))   # [3, 2, 1]
print(extract_digits(0))     # [0]
print(digit_count(12345))    # 5
print(digit_count(0))        # 1
```

---

## Problem: Palindrome Number (LeetCode 9) -- Easy

Check if an integer is a palindrome without converting to string.

### Approach: Reverse Half the Number

**Key idea:** Instead of reversing the entire number (which could overflow in some
languages), only reverse the second half. When the reversed half equals the
remaining first half, it's a palindrome.

```python
def isPalindrome(x: int) -> bool:
    """
    Check if x is a palindrome by reversing half and comparing.

    Time:  O(log x) -- processes half the digits
    Space: O(1)
    """
    # Negative numbers are never palindromes.
    # Numbers ending in 0 (except 0 itself) aren't palindromes
    # because no number starts with 0.
    if x < 0 or (x % 10 == 0 and x != 0):
        return False

    reversed_half = 0

    # Build reversed second half until it's >= remaining first half
    while x > reversed_half:
        reversed_half = reversed_half * 10 + x % 10
        x //= 10

    # Even digit count: x == reversed_half        (e.g., 1221 -> 12 == 12)
    # Odd digit count:  x == reversed_half // 10   (e.g., 12321 -> 12 == 123//10)
    # The middle digit doesn't affect palindrome-ness.
    return x == reversed_half or x == reversed_half // 10


# Test
print(isPalindrome(121))    # True
print(isPalindrome(-121))   # False
print(isPalindrome(10))     # False
print(isPalindrome(12321))  # True
print(isPalindrome(0))      # True
print(isPalindrome(1221))   # True
```

### Why Reverse Only Half?

```
For 12321 (odd digits):
  x = 12321, reversed_half = 0
  x = 1232,  reversed_half = 1
  x = 123,   reversed_half = 12
  x = 12,    reversed_half = 123   <- reversed_half > x, stop

  Check: x == reversed_half // 10  ->  12 == 123 // 10 = 12  ✓

For 1221 (even digits):
  x = 1221,  reversed_half = 0
  x = 122,   reversed_half = 1
  x = 12,    reversed_half = 12    <- reversed_half >= x, stop

  Check: x == reversed_half  ->  12 == 12  ✓

Benefits:
  1. Avoids potential overflow from full reversal (matters in C/Java)
  2. Only processes half the digits -- slightly faster
```

---

## Problem: Reverse Integer (LeetCode 7) -- Medium

Reverse digits of a 32-bit signed integer. Return 0 if the result overflows.

```python
def reverse(x: int) -> int:
    """
    Reverse digits of x, return 0 if result overflows 32-bit signed range.

    32-bit signed range: [-2^31, 2^31 - 1] = [-2147483648, 2147483647]

    Time:  O(log x) -- number of digits
    Space: O(1)
    """
    INT_MAX = 2**31 - 1   # 2147483647
    INT_MIN = -2**31      # -2147483648

    sign = 1 if x >= 0 else -1
    x = abs(x)
    result = 0

    while x:
        digit = x % 10
        x //= 10

        # Check overflow BEFORE the multiply+add that would cause it
        if result > (INT_MAX - digit) // 10:
            return 0

        result = result * 10 + digit

    result *= sign

    # Final bounds check (catches negative overflow edge case)
    if result < INT_MIN or result > INT_MAX:
        return 0

    return result


# Test
print(reverse(123))          # 321
print(reverse(-123))         # -321
print(reverse(120))          # 21
print(reverse(0))            # 0
print(reverse(1534236469))   # 0 (reversed = 9646324351 > INT_MAX)
```

### Overflow Check Explained

```
We want:  result * 10 + digit <= INT_MAX

Rearrange: result <= (INT_MAX - digit) / 10

We check: result > (INT_MAX - digit) // 10
  If true -> the next step would overflow, return 0.

Example with INT_MAX = 2147483647:
  result = 214748364, digit = 8
  (2147483647 - 8) // 10 = 214748363
  214748364 > 214748363  ->  True  ->  overflow!

  result = 214748364, digit = 7
  (2147483647 - 7) // 10 = 214748364
  214748364 > 214748364  ->  False  ->  safe (result = 2147483647 = INT_MAX)
```

---

## Problem: Add Digits / Digital Root (LeetCode 258) -- Easy

Repeatedly add all digits until the result has only one digit.

```python
def addDigits(num: int) -> int:
    """
    Compute the digital root of num using the O(1) formula.

    Time:  O(1)
    Space: O(1)
    """
    if num == 0:
        return 0
    return 1 + (num - 1) % 9  # Elegant one-liner for digital root


def addDigits_iterative(num: int) -> int:
    """Iterative approach -- keeps summing digits until single digit."""
    while num >= 10:
        digit_sum = 0
        while num:
            digit_sum += num % 10
            num //= 10
        num = digit_sum
    return num


# Test
print(addDigits(38))   # 2 (3+8=11, 1+1=2)
print(addDigits(0))    # 0
print(addDigits(18))   # 9
print(addDigits(1))    # 1
```

### Why the Digital Root Formula Works

```
Key insight: 10 ≡ 1 (mod 9), so 10^k ≡ 1 (mod 9) for all k.

Any number like 123 = 1×100 + 2×10 + 3
                     ≡ 1×1   + 2×1  + 3 = 6 (mod 9)

Summing digits preserves the value mod 9.
Repeating always converges to a single digit: the remainder mod 9.

Special case: multiples of 9 have digital root 9, not 0.

Formula: digital_root(n) = 1 + (n - 1) % 9   (for n > 0)

This handles the special case elegantly:
  n = 18: 1 + (17) % 9 = 1 + 8 = 9  ✓
  n = 38: 1 + (37) % 9 = 1 + 1 = 2  ✓
  n = 1:  1 + (0) % 9  = 1 + 0 = 1  ✓
```

---

## Problem: Power of Two/Three/Four

Check if n is a power of a given base.

### Power of Two (LeetCode 231) -- Easy

```python
def isPowerOfTwo(n: int) -> bool:
    """
    Check if n is a power of 2.

    Key insight: Powers of 2 in binary have exactly one bit set.
      1 = 0001,  2 = 0010,  4 = 0100,  8 = 1000

    n & (n - 1) clears the lowest set bit.
    If the result is 0, there was only one bit set -> power of 2.

    Example: n = 8 (1000), n-1 = 7 (0111) -> 1000 & 0111 = 0000 ✓
    Example: n = 6 (0110), n-1 = 5 (0101) -> 0110 & 0101 = 0100 ≠ 0 ✗

    Time:  O(1)
    Space: O(1)
    """
    return n > 0 and (n & (n - 1)) == 0


# Test
print(isPowerOfTwo(1))    # True  (2^0)
print(isPowerOfTwo(16))   # True  (2^4)
print(isPowerOfTwo(3))    # False
print(isPowerOfTwo(0))    # False
```

### Power of Three (LeetCode 326) -- Easy

```python
def isPowerOfThree(n: int) -> bool:
    """
    Check if n is a power of 3 (O(1) approach).

    Since 3 is prime, the only divisors of 3^19 are 3^0, 3^1, ..., 3^19.
    3^19 = 1162261467 is the largest power of 3 in 32-bit signed int range.
    So: n is a power of 3 iff n > 0 and 3^19 is divisible by n.

    Why this only works for primes: If the base were composite (e.g., 6),
    then 6^k's divisors would include non-powers of 6 (like 2, 3, 12, etc.).

    Time:  O(1)
    Space: O(1)
    """
    return n > 0 and 1162261467 % n == 0


def isPowerOfThree_loop(n: int) -> bool:
    """Loop method -- O(log_3 n) time. Works for any base."""
    if n <= 0:
        return False
    while n % 3 == 0:
        n //= 3
    return n == 1


# Test
print(isPowerOfThree(27))   # True  (3^3)
print(isPowerOfThree(9))    # True  (3^2)
print(isPowerOfThree(45))   # False (45 = 9 * 5, not a power of 3)
print(isPowerOfThree(1))    # True  (3^0)
```

### Power of Four (LeetCode 342) -- Easy

```python
def isPowerOfFour(n: int) -> bool:
    """
    Check if n is a power of 4.

    Two conditions:
    1. Must be a power of 2: n & (n-1) == 0
    2. The single set bit must be at an EVEN position (0-indexed: 0, 2, 4, ...)
       Powers of 4: 1(bit 0), 4(bit 2), 16(bit 4), 64(bit 6), ...
       Powers of 2 but NOT 4: 2(bit 1), 8(bit 3), 32(bit 5), ...

       Mask 0x55555555 = 0101 0101 ... in binary -- has 1s at even positions.
       ANDing with this mask checks if the set bit is at an even position.

    Time:  O(1)
    Space: O(1)
    """
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0


def isPowerOfFour_math(n: int) -> bool:
    """
    Math approach: 4^k = 2^(2k), so log2(n) must be a non-negative even integer.
    Uses bit_length for exact integer arithmetic (no floating-point issues).
    """
    if n <= 0:
        return False
    # Must be a power of 2 first
    if n & (n - 1) != 0:
        return False
    # For power of 2, log2(n) = bit_length - 1. Check if it's even.
    return (n.bit_length() - 1) % 2 == 0


# Test
print(isPowerOfFour(16))   # True  (4^2)
print(isPowerOfFour(8))    # False (2^3, not a power of 4)
print(isPowerOfFour(1))    # True  (4^0)
print(isPowerOfFour(64))   # True  (4^3)
```

---

## Problem: Happy Number (LeetCode 202) -- Easy

A happy number is one where repeatedly summing the squares of its digits eventually reaches 1. If it enters a cycle that never includes 1, it's not happy.

```python
def isHappy(n: int) -> bool:
    """
    Determine if n is a happy number using Floyd's cycle detection.

    Key insight: The sequence of digit-square sums either:
      (a) reaches 1 (happy), or
      (b) enters a cycle (not happy)
    This is the same structure as linked list cycle detection.

    Why a cycle must exist: For any number with d digits, the max
    digit-square sum is d * 81 (all 9s). For d >= 4, d * 81 < 10^d,
    so the values shrink and stay bounded. Bounded + infinite sequence
    = guaranteed repeated value = cycle.

    Time:  O(log n) -- the sequence values stay bounded
    Space: O(1) -- no set needed with Floyd's approach
    """
    def get_next(num: int) -> int:
        """Sum of squares of digits."""
        total = 0
        while num:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total

    slow = n
    fast = get_next(n)

    while fast != 1 and slow != fast:
        slow = get_next(slow)            # Move 1 step
        fast = get_next(get_next(fast))   # Move 2 steps

    return fast == 1


def isHappy_set(n: int) -> bool:
    """Set-based approach -- easier to understand, O(log n) space."""
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        total = 0
        while n:
            digit = n % 10
            total += digit * digit
            n //= 10
        n = total
    return n == 1


# Test
print(isHappy(19))   # True  (19 -> 82 -> 68 -> 100 -> 1)
print(isHappy(2))    # False (enters cycle: 2 -> 4 -> 16 -> 37 -> 58 -> 89 -> ...)
print(isHappy(1))    # True
print(isHappy(7))    # True  (7 -> 49 -> 97 -> 130 -> 10 -> 1)
```

---

## Problem: Ugly Number (LeetCode 263) -- Easy

An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5.
By convention, 1 is an ugly number.

**Approach:** Repeatedly divide by 2, 3, and 5. If the result is 1, it's ugly.

```python
def isUgly(n: int) -> bool:
    """
    Check if n is an ugly number (only prime factors 2, 3, 5).

    Time:  O(log n) -- each division at least halves n
    Space: O(1)
    """
    if n <= 0:
        return False

    for factor in (2, 3, 5):
        while n % factor == 0:
            n //= factor

    return n == 1


# Test
print(isUgly(6))    # True  (2 * 3)
print(isUgly(1))    # True
print(isUgly(14))   # False (2 * 7 -- 7 is not 2, 3, or 5)
print(isUgly(0))    # False
print(isUgly(-6))   # False
```

---

## Problem: Self Dividing Numbers (LeetCode 728) -- Easy

A self-dividing number is divisible by every digit it contains (and contains no zeros).

```python
def selfDividingNumbers(left: int, right: int) -> list[int]:
    """
    Find all self-dividing numbers in [left, right].

    Time:  O((right - left) * log(right)) -- check each number's digits
    Space: O(1) excluding output
    """
    def is_self_dividing(n: int) -> bool:
        if n <= 0:
            return False
        original = n
        while n:
            digit = n % 10
            if digit == 0 or original % digit != 0:
                return False
            n //= 10
        return True

    return [n for n in range(left, right + 1) if is_self_dividing(n)]


# Test
print(selfDividingNumbers(1, 22))
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 22]
```

---

## Problem: Count and Say (LeetCode 38) -- Medium

The count-and-say sequence starts with "1" and each subsequent term describes
the previous term using run-length encoding:

```
"1"      -> one 1       -> "11"
"11"     -> two 1s      -> "21"
"21"     -> one 2, one 1 -> "1211"
"1211"   -> one 1, one 2, two 1s -> "111221"
```

```python
def countAndSay(n: int) -> str:
    """
    Generate the nth term of the count-and-say sequence.

    Approach: Simulate the process n-1 times. For each term, walk through
    the string counting consecutive identical characters, then build the
    next term from those counts.

    Time:  O(n * L) where L is the length of the term (grows exponentially)
    Space: O(L) for building the next term
    """
    result = "1"

    for _ in range(n - 1):
        next_result = []
        i = 0

        while i < len(result):
            # Count consecutive identical digits
            char = result[i]
            count = 1
            while i + count < len(result) and result[i + count] == char:
                count += 1

            next_result.append(str(count))
            next_result.append(char)
            i += count

        result = "".join(next_result)

    return result


# Test
print(countAndSay(1))   # "1"
print(countAndSay(2))   # "11"
print(countAndSay(3))   # "21"
print(countAndSay(4))   # "1211"
print(countAndSay(5))   # "111221"
```

---

## Problem: Integer to Roman (LeetCode 12) -- Medium

Convert an integer (1 to 3999) to a Roman numeral string.

**Greedy approach:** Use the largest Roman value that fits, subtract, repeat.
Include the subtractive forms (like 4=IV, 9=IX) in the lookup table so the
greedy algorithm handles them naturally.

```python
def intToRoman(num: int) -> str:
    """
    Convert integer to Roman numeral using greedy subtraction.

    Time:  O(1) -- num is bounded at 3999; at most ~15 iterations
    Space: O(1)
    """
    values = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"),  (90, "XC"),  (50, "L"),  (40, "XL"),
        (10, "X"),   (9, "IX"),   (5, "V"),   (4, "IV"),  (1, "I"),
    ]

    result = []
    for value, symbol in values:
        while num >= value:
            result.append(symbol)
            num -= value

    return "".join(result)


# Test
print(intToRoman(3))     # "III"
print(intToRoman(58))    # "LVIII"
print(intToRoman(1994))  # "MCMXCIV"
print(intToRoman(4))     # "IV"
```

---

## Problem: Roman to Integer (LeetCode 13) -- Easy

```python
def romanToInt(s: str) -> int:
    """
    Convert Roman numeral string to integer.

    Key insight: Traverse right-to-left. If the current value is smaller
    than the previous one, subtract it (subtractive notation like IV=4).
    Otherwise, add it.

    Time:  O(n) where n = length of string
    Space: O(1)
    """
    values = {
        "I": 1, "V": 5, "X": 10, "L": 50,
        "C": 100, "D": 500, "M": 1000,
    }

    result = 0
    prev = 0

    for char in reversed(s):
        curr = values[char]
        if curr < prev:
            result -= curr  # Subtractive case (e.g., I before V)
        else:
            result += curr
        prev = curr

    return result


# Test
print(romanToInt("III"))      # 3
print(romanToInt("LVIII"))    # 58
print(romanToInt("MCMXCIV"))  # 1994
print(romanToInt("IV"))       # 4
```

---

## Problem: Excel Sheet Column Number/Title (LeetCode 171 & 168) -- Easy

Excel columns use a bijective base-26 system: A=1, B=2, ..., Z=26, AA=27, AB=28, ...

This is NOT standard base-26 (which would have a zero digit). The key difference
is the `columnNumber -= 1` adjustment when converting back.

```python
def titleToNumber(columnTitle: str) -> int:
    """
    Convert Excel column title to number (LeetCode 171).

    Treat as base-26 where A=1, B=2, ..., Z=26.
    Process left-to-right, accumulating: result = result * 26 + digit_value

    Time:  O(n) where n = length of title
    Space: O(1)
    """
    result = 0
    for char in columnTitle:
        result = result * 26 + (ord(char) - ord("A") + 1)
    return result


def convertToTitle(columnNumber: int) -> str:
    """
    Convert number to Excel column title (LeetCode 168).

    Key trick: subtract 1 before each mod to handle the 1-indexed system.
    Without this, Z (26) would produce a remainder of 0, which has no letter.

    Time:  O(log_26 n)
    Space: O(log_26 n)
    """
    result = []

    while columnNumber > 0:
        columnNumber -= 1  # Adjust from 1-indexed to 0-indexed
        result.append(chr(columnNumber % 26 + ord("A")))
        columnNumber //= 26

    return "".join(reversed(result))


# Test
print(titleToNumber("A"))    # 1
print(titleToNumber("AB"))   # 28
print(titleToNumber("ZY"))   # 701

print(convertToTitle(1))     # "A"
print(convertToTitle(28))    # "AB"
print(convertToTitle(701))   # "ZY"
print(convertToTitle(26))    # "Z"
```

---

## Problem: Plus One (LeetCode 66) -- Easy

Add one to a number represented as an array of digits.

```python
def plusOne(digits: list[int]) -> list[int]:
    """
    Add 1 to the number represented by digits array.

    Walk from the rightmost digit. If it's < 9, increment and return.
    If it's 9, set to 0 (carry) and continue left.
    If all digits were 9, prepend a 1.

    Time:  O(n)
    Space: O(1) in-place, or O(n) if all-9s case creates new array
    """
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0  # Carry

    # All digits were 9 (e.g., 999 -> 1000)
    return [1] + digits


# Test
print(plusOne([1, 2, 3]))  # [1, 2, 4]
print(plusOne([9, 9, 9]))  # [1, 0, 0, 0]
print(plusOne([0]))         # [1]
print(plusOne([9]))         # [1, 0]
```

---

## Problem: Count Primes (LeetCode 204) -- Medium

Count the number of prime numbers strictly less than n.

**The Sieve of Eratosthenes:** Start by assuming all numbers >= 2 are prime.
Then for each prime p, mark all its multiples (starting from p*p) as composite.
Numbers left unmarked are prime.

**Why start at p*p?** All smaller multiples of p (like 2p, 3p, ..., (p-1)p)
have already been marked by smaller primes.

```python
def countPrimes(n: int) -> int:
    """
    Count primes less than n using the Sieve of Eratosthenes.

    Time:  O(n log log n) -- classic sieve complexity
    Space: O(n)
    """
    if n <= 2:
        return 0

    # is_prime[i] = True means i is prime (initially assume all are prime)
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    # Only need to sieve up to sqrt(n)
    p = 2
    while p * p < n:
        if is_prime[p]:
            # Mark multiples of p starting from p*p
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False
        p += 1

    return sum(is_prime)


# Test
print(countPrimes(10))    # 4  (primes: 2, 3, 5, 7)
print(countPrimes(0))     # 0
print(countPrimes(1))     # 0
print(countPrimes(2))     # 0  (strictly less than 2)
print(countPrimes(20))    # 8  (primes: 2, 3, 5, 7, 11, 13, 17, 19)
```

### Sieve Walkthrough

```
n = 20, sieve for primes < 20:

Start: [F, F, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
              2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19

p=2: mark 4, 6, 8, 10, 12, 14, 16, 18
p=3: mark 9, 15   (6, 12, 18 already marked by p=2)
p=4: skip (already marked as composite)
p>=5: 5*5=25 >= 20, stop

Primes: 2, 3, 5, 7, 11, 13, 17, 19  -> count = 8
```

---

## Problem: Multiply Strings (LeetCode 43) -- Medium

Multiply two non-negative integers represented as strings. Cannot use built-in
big integer libraries or convert directly to integer.

**Why this problem matters:** It combines digit extraction, number building,
and carry propagation -- the core patterns of this chapter.

```python
def multiply(num1: str, num2: str) -> str:
    """
    Multiply two numbers represented as strings, digit by digit.

    Mimics the grade-school multiplication algorithm:
    Position i from num1 and position j from num2 contribute
    to position i+j and i+j+1 in the result.

    Time:  O(m * n) where m, n are lengths of inputs
    Space: O(m + n) for result array
    """
    m, n = len(num1), len(num2)
    # Result can have at most m + n digits (e.g., 99 * 99 = 9801, 4 digits)
    result = [0] * (m + n)

    # Multiply each digit pair (working right-to-left)
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            product = int(num1[i]) * int(num2[j])
            # Positions in result array
            p1, p2 = i + j, i + j + 1

            total = product + result[p2]
            result[p2] = total % 10        # Current digit
            result[p1] += total // 10      # Carry

    # Convert to string, skip leading zeros
    result_str = "".join(map(str, result)).lstrip("0")
    return result_str or "0"


# Test
print(multiply("2", "3"))       # "6"
print(multiply("123", "456"))   # "56088"
print(multiply("0", "12345"))   # "0"
print(multiply("99", "99"))     # "9801"
```

### Why Position i+j and i+j+1?

```
Think about multiplying 123 × 456 by hand:

         1  2  3     (indices 0, 1, 2)
      ×  4  5  6     (indices 0, 1, 2)
      ----------
         6 12 18     <- 3*6=18 goes to positions (2+2, 2+2+1) = (4, 5)
      5 10 15        <- shifted left by one
   4  8 12           <- shifted left by two

Result positions: 0  1  2  3  4  5

This is exactly: digit at index i (in num1) × digit at index j (in num2)
contributes to result position i+j (tens) and i+j+1 (ones).
```

---

## Problem: Add Binary (LeetCode 67) -- Easy

Add two binary strings and return the result as a binary string.

```python
def addBinary(a: str, b: str) -> str:
    """
    Add two binary strings without converting to int (to practice carry logic).

    Walk both strings right-to-left, adding digits + carry.

    Time:  O(max(m, n))
    Space: O(max(m, n)) for result
    """
    result = []
    carry = 0
    i, j = len(a) - 1, len(b) - 1

    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += int(a[i])
            i -= 1
        if j >= 0:
            total += int(b[j])
            j -= 1

        result.append(str(total % 2))
        carry = total // 2

    return "".join(reversed(result))


# Test
print(addBinary("11", "1"))      # "100"
print(addBinary("1010", "1011")) # "10101"
print(addBinary("0", "0"))       # "0"
```

---

## Problem: Integer to English Words (LeetCode 273) -- Hard

Convert a non-negative integer to its English words representation.

**Key insight:** English groups numbers in chunks of three digits (thousands,
millions, billions). Process the number in groups of 1000, handling each
three-digit chunk with a helper function.

```python
def numberToWords(num: int) -> str:
    """
    Convert integer to English words.

    Approach: Process in groups of 3 digits (the natural English grouping).
    For each group, convert the 3-digit number to words, then append
    the appropriate scale word (Thousand, Million, Billion).

    Time:  O(1) -- num is bounded (0 to 2^31 - 1, at most 10 digits)
    Space: O(1) -- output length is bounded
    """
    if num == 0:
        return "Zero"

    ones = [
        "", "One", "Two", "Three", "Four", "Five", "Six",
        "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve",
        "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen",
        "Eighteen", "Nineteen",
    ]
    tens = [
        "", "", "Twenty", "Thirty", "Forty", "Fifty",
        "Sixty", "Seventy", "Eighty", "Ninety",
    ]
    scales = ["", "Thousand", "Million", "Billion"]

    def three_digit_to_words(n: int) -> str:
        """Convert a number 0-999 to English words."""
        if n == 0:
            return ""

        parts = []
        if n >= 100:
            parts.append(ones[n // 100])
            parts.append("Hundred")
            n %= 100

        if n >= 20:
            parts.append(tens[n // 10])
            n %= 10

        if n > 0:
            parts.append(ones[n])

        return " ".join(parts)

    result = []
    scale_index = 0

    while num > 0:
        chunk = num % 1000
        if chunk != 0:
            words = three_digit_to_words(chunk)
            if scales[scale_index]:
                words += " " + scales[scale_index]
            result.append(words)

        num //= 1000
        scale_index += 1

    # Reverse because we processed from least significant group
    return " ".join(reversed(result))


# Test
print(numberToWords(123))
# "One Hundred Twenty Three"
print(numberToWords(12345))
# "Twelve Thousand Three Hundred Forty Five"
print(numberToWords(1234567))
# "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
print(numberToWords(0))
# "Zero"
print(numberToWords(1000000))
# "One Million"
print(numberToWords(20))
# "Twenty"
print(numberToWords(100))
# "One Hundred"
```

### Decomposition Pattern

```
1,234,567 breaks into groups of 3:

  1       -> "One"        + "Million"
  234     -> "Two Hundred Thirty Four" + "Thousand"
  567     -> "Five Hundred Sixty Seven"

Result: "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"

Edge cases to watch:
  - Groups of all zeros: 1,000,000 -> skip the "Thousand" group entirely
  - Numbers 11-19: special words (not "Ten One" but "Eleven")
  - Zero: special case, return "Zero" immediately
```

---

## Problem: Basic Calculator II (LeetCode 227) -- Medium

Evaluate a string expression with `+`, `-`, `*`, `/` (integer division truncating toward zero) and spaces. No parentheses.

**Approach:** Use a stack. Process `*` and `/` immediately (higher precedence),
defer `+` and `-` by pushing to stack, then sum the stack at the end.

```python
def calculate(s: str) -> int:
    """
    Evaluate arithmetic expression with +, -, *, / (no parentheses).

    Strategy: Maintain a stack. When we see * or /, apply immediately
    to the top of stack and current number. For + and -, push the
    (signed) number onto the stack. Final answer = sum(stack).

    Time:  O(n) -- single pass through the string
    Space: O(n) -- stack stores intermediate values
    """
    stack = []
    current_num = 0
    operator = "+"  # Initialize with '+' so the first number gets pushed

    for i, char in enumerate(s):
        if char.isdigit():
            current_num = current_num * 10 + int(char)

        # Process when we hit an operator or the end of the string
        if char in "+-*/" or i == len(s) - 1:
            if operator == "+":
                stack.append(current_num)
            elif operator == "-":
                stack.append(-current_num)
            elif operator == "*":
                stack.append(stack.pop() * current_num)
            elif operator == "/":
                # Truncate toward zero (Python's // truncates toward -inf)
                stack.append(int(stack.pop() / current_num))

            operator = char
            current_num = 0

    return sum(stack)


# Test
print(calculate("3+2*2"))       # 7
print(calculate(" 3/2 "))       # 1
print(calculate(" 3+5 / 2 "))   # 5
print(calculate("14-3/2"))      # 13
print(calculate("0-2147483647")) # -2147483647
```

### Why `int(a / b)` Instead of `a // b`?

```
Python's // operator does floor division (rounds toward negative infinity):
  -7 // 2 = -4   (floor of -3.5)

But the problem wants truncation toward zero:
  -7 truncated = -3

int(-7 / 2) = int(-3.5) = -3  ✓  (int() truncates toward zero)

Alternative: use math.trunc() or: -(abs(a) // abs(b)) when signs differ.
```

---

## Problem: Nth Digit (LeetCode 400) -- Medium

Find the nth digit in the infinite sequence 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...

**Key insight:** Group numbers by digit count:
- 1-digit: 1-9 (9 numbers, 9 digits total)
- 2-digit: 10-99 (90 numbers, 180 digits total)
- 3-digit: 100-999 (900 numbers, 2700 digits total)
- k-digit: 9 * 10^(k-1) numbers, each contributing k digits

```python
def findNthDigit(n: int) -> int:
    """
    Find the nth digit in the sequence 1, 2, 3, ..., 9, 10, 11, ...

    Step 1: Determine which digit-length group n falls into.
    Step 2: Find the exact number within that group.
    Step 3: Find the exact digit within that number.

    Time:  O(log n) -- the number of digit-length groups is O(log n)
    Space: O(1)
    """
    # Step 1: Skip past complete groups
    digit_len = 1      # Current group: 1-digit, 2-digit, etc.
    group_start = 1    # First number in this group
    group_count = 9    # How many numbers in this group

    while n > digit_len * group_count:
        n -= digit_len * group_count
        digit_len += 1
        group_start *= 10
        group_count *= 10

    # Step 2: Find which number in this group
    # n is now 1-indexed within this group
    number = group_start + (n - 1) // digit_len

    # Step 3: Find which digit within that number
    digit_index = (n - 1) % digit_len
    return int(str(number)[digit_index])


# Test
print(findNthDigit(3))    # 3  (sequence: 1, 2, [3])
print(findNthDigit(11))   # 0  (sequence: 1..9, 1, [0] -- 10th-11th digits are "10")
print(findNthDigit(15))   # 2  (sequence: 1..9(9 digits), 10=[1,0], 11=[1,1], 12=[1,[2]])
print(findNthDigit(1))    # 1
```

### Walkthrough

```
findNthDigit(15):

Group 1: 1-digit (1-9), 9 numbers × 1 digit = 9 digits total
  n = 15 > 9, so n -= 9  -> n = 6

Group 2: 2-digit (10-99), 90 numbers × 2 digits = 180 digits total
  n = 6 <= 180, so we're in this group.

Which number? group_start + (6-1) // 2 = 10 + 2 = 12
Which digit?  (6-1) % 2 = 1  -> second digit of "12" -> '2'

Answer: 2
```

---

## Complexity Summary

| Problem              | Time         | Space    | Key Technique                  |
| -------------------- | ------------ | -------- | ------------------------------ |
| Palindrome Number    | O(log n)     | O(1)     | Reverse half                   |
| Reverse Integer      | O(log n)     | O(1)     | Digit extraction + overflow    |
| Add Digits           | O(1)         | O(1)     | Digital root formula           |
| Power of 2/3/4       | O(1)         | O(1)     | Bit manipulation / divisor     |
| Happy Number         | O(log n)     | O(1)*    | Floyd's cycle detection        |
| Ugly Number          | O(log n)     | O(1)     | Divide out prime factors       |
| Integer <-> Roman    | O(1)         | O(1)     | Greedy / right-to-left scan    |
| Excel Column         | O(n)         | O(n)     | Bijective base-26 conversion   |
| Plus One             | O(n)         | O(1)*    | Carry propagation              |
| Count and Say        | O(n * L)     | O(L)     | Run-length encoding simulation |
| Count Primes         | O(n log log n) | O(n)   | Sieve of Eratosthenes          |
| Multiply Strings     | O(m * n)     | O(m + n) | Grade-school multiplication    |
| Add Binary           | O(max(m,n))  | O(max(m,n)) | Carry propagation          |
| Self Dividing        | O(k * d)     | O(1)*    | Digit extraction + divisible   |
| Nth Digit            | O(log n)     | O(1)     | Digit-group counting           |
| Basic Calculator II  | O(n)         | O(n)     | Stack + operator precedence    |
| Integer to English   | O(1)         | O(1)     | Recursive 3-digit grouping     |

\* Excluding output. Happy Number O(1) space with Floyd's, O(log n) with set.

---

## Edge Cases Checklist

1. **Zero:** Often needs special handling (is it a palindrome? power of X?)
2. **Negative numbers:** Never palindromes, never powers of X
3. **Single digit:** 0-9 are palindromes; 1 is a power of every base
4. **32-bit overflow:** Critical for reverse integer, check BEFORE the operation
5. **Trailing zeros:** 10 is not a palindrome (leading zeros aren't valid)
6. **Boundary values:** INT_MAX (2147483647), INT_MIN (-2147483648)
7. **All 9s:** Plus one on [9,9,9] needs array expansion
8. **Division toward zero:** Python `//` floors, but truncation toward zero may be required (use `int(a/b)`)
9. **Large inputs:** Sieve needs O(n) memory; digit problems need careful arithmetic to avoid TLE

---

## Interview Tips

1. **Avoid string conversion unless asked** -- shows mathematical sophistication
2. **Handle overflow explicitly** -- especially for reverse integer; check BEFORE the multiply
3. **Know the three digit formulas:** `n % 10` (extract), `n // 10` (remove), `result * 10 + digit` (build)
4. **Memorize bit tricks:** Power of 2 = `n & (n-1) == 0`; explain WHY it works
5. **Test edge cases systematically:** 0, negative, single digit, all 9s, max/min values
6. **Consider both approaches:** Know the math trick AND the loop fallback for power checks
7. **Know your division:** Python `//` floors toward -inf; use `int(a/b)` to truncate toward 0
8. **Sieve of Eratosthenes:** Memorize it; sieve up to sqrt(n), start marking from p*p

---

## Progressive Practice Problems

### Easy -- Foundation

| #   | Problem                        | LeetCode | Key Concept                  |
| --- | ------------------------------ | -------- | ---------------------------- |
| 1   | Palindrome Number              | 9        | Reverse half                 |
| 2   | Add Digits                     | 258      | Digital root formula         |
| 3   | Power of Two                   | 231      | Bit trick: `n & (n-1)`      |
| 4   | Power of Three                 | 326      | Prime divisor trick          |
| 5   | Power of Four                  | 342      | Bit position mask            |
| 6   | Plus One                       | 66       | Carry propagation            |
| 7   | Happy Number                   | 202      | Cycle detection on digits    |
| 8   | Ugly Number                    | 263      | Divide out prime factors     |
| 9   | Excel Sheet Column Number      | 171      | Bijective base-26 decode     |
| 10  | Roman to Integer               | 13       | Right-to-left scan           |
| 11  | Self Dividing Numbers          | 728      | Digit extraction + modulo    |
| 12  | Add Binary                     | 67       | Binary carry propagation     |

### Medium -- Application

| #   | Problem                        | LeetCode | Key Concept                  |
| --- | ------------------------------ | -------- | ---------------------------- |
| 13  | Reverse Integer                | 7        | Overflow-safe digit reversal |
| 14  | Integer to Roman               | 12       | Greedy with value table      |
| 15  | Excel Sheet Column Title       | 168      | Bijective base-26 encode     |
| 16  | Count Primes                   | 204      | Sieve of Eratosthenes        |
| 17  | Count and Say                  | 38       | Run-length encoding          |
| 18  | Multiply Strings               | 43       | Digit-by-digit multiplication|
| 19  | Nth Digit                      | 400      | Digit-group math             |
| 20  | Basic Calculator II            | 227      | Stack + operator precedence  |

### Hard -- Interview-Level Challenges

| #   | Problem                        | LeetCode | Key Concept                  |
| --- | ------------------------------ | -------- | ---------------------------- |
| 21  | Integer to English Words       | 273      | Recursive number decomposition|
| 22  | Basic Calculator               | 224      | Stack + recursion for parens |
| 23  | Strobogrammatic Number III     | 248      | Digit symmetry + counting    |
| 24  | Numbers At Most N Given Digit Set | 902   | Digit DP                     |

---

## When String Conversion is Acceptable

1. **When the interviewer allows it** -- always ask first
2. **When string is cleaner:** `str(n) == str(n)[::-1]` for palindrome check
3. **When you need individual digits:** Converting to string is O(log n) anyway
4. **When debugging:** String conversion helps verify your math-only logic

### String vs Math Trade-offs

| Approach        | Pros                                 | Cons                             |
| --------------- | ------------------------------------ | -------------------------------- |
| Math (% and //) | Shows sophistication, no allocations | Harder to read, easy to mess up  |
| String          | Clean, readable, easy to debug       | Extra memory, may seem "lazy"    |

**When to definitely use math:**

- When the interviewer explicitly requires it
- When overflow handling is the point of the problem
- When you need only half the digits (palindrome half-reversal)
- When the problem constraints forbid string conversion (Multiply Strings)

---

## Related Sections

- [Bit Manipulation](../15-bit-manipulation/README.md) -- Power of 2 checks, bit tricks
- [GCD and LCM](./01-gcd-lcm.md) -- Divisibility concepts
