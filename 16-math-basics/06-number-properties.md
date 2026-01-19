# Number Properties

> **Prerequisites:** None (standalone topic)

## Interview Context

Number property problems test:
- Digit manipulation without converting to string
- Integer overflow awareness
- Edge case handling (negative numbers, zero, boundaries)
- Mathematical reasoning

Common problems: palindrome number, reverse integer, happy number, and power-of-X checks.

---

## Pattern: Digit Extraction

Extract digits from a number without converting to string.

```
123 → digits 1, 2, 3

Extract from right (easiest):
  123 % 10 = 3 (last digit)
  123 // 10 = 12 (remove last digit)

  12 % 10 = 2
  12 // 10 = 1

  1 % 10 = 1
  1 // 10 = 0 (done)

Digits from right: 3, 2, 1
```

### Implementation

```python
def extract_digits(n: int) -> list[int]:
    """
    Extract digits from right to left.

    Time: O(log n) - number of digits
    Space: O(log n) - to store digits
    """
    if n == 0:
        return [0]

    n = abs(n)
    digits = []

    while n:
        digits.append(n % 10)
        n //= 10

    return digits  # Reversed order (right to left)


def digit_count(n: int) -> int:
    """Count number of digits in n."""
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
print(digit_count(12345))    # 5
```

---

## Problem: Palindrome Number (LeetCode 9)

Check if an integer is a palindrome without converting to string.

### Approach 1: Reverse Half the Number

```python
def isPalindrome(x: int) -> bool:
    """
    Check if x is a palindrome by reversing half and comparing.

    Time: O(log x) - half the digits
    Space: O(1)
    """
    # Negative numbers and numbers ending in 0 (except 0 itself) aren't palindromes
    if x < 0 or (x % 10 == 0 and x != 0):
        return False

    reversed_half = 0

    # Build reversed half until it's >= remaining half
    while x > reversed_half:
        reversed_half = reversed_half * 10 + x % 10
        x //= 10

    # For even digits: x == reversed_half
    # For odd digits: x == reversed_half // 10 (middle digit doesn't matter)
    return x == reversed_half or x == reversed_half // 10


# Test
print(isPalindrome(121))    # True
print(isPalindrome(-121))   # False
print(isPalindrome(10))     # False
print(isPalindrome(12321))  # True
print(isPalindrome(0))      # True
```

### Why Reverse Only Half?

```
For 12321:
  x = 12321, reversed = 0
  x = 1232,  reversed = 1
  x = 123,   reversed = 12
  x = 12,    reversed = 123  ← reversed > x, stop

  Check: 12 == 123 // 10 = 12 ✓

This avoids potential overflow from full reversal.
```

---

## Problem: Reverse Integer (LeetCode 7)

Reverse digits of a 32-bit signed integer.

```python
def reverse(x: int) -> int:
    """
    Reverse digits of x, return 0 if overflow.

    32-bit signed range: [-2^31, 2^31 - 1] = [-2147483648, 2147483647]

    Time: O(log x)
    Space: O(1)
    """
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31

    sign = 1 if x >= 0 else -1
    x = abs(x)
    result = 0

    while x:
        digit = x % 10
        x //= 10

        # Check for overflow before multiplying
        if result > (INT_MAX - digit) // 10:
            return 0

        result = result * 10 + digit

    result *= sign

    # Final bounds check
    if result < INT_MIN or result > INT_MAX:
        return 0

    return result


# Test
print(reverse(123))       # 321
print(reverse(-123))      # -321
print(reverse(120))       # 21
print(reverse(1534236469))  # 0 (overflow)
```

### Overflow Check Explained

```
Before: result = result * 10 + digit

To avoid overflow, check:
  result * 10 + digit ≤ INT_MAX
  result ≤ (INT_MAX - digit) / 10

If this check fails, return 0.
```

---

## Problem: Add Digits (LeetCode 258)

Repeatedly add all digits until the result has only one digit.

```python
def addDigits(num: int) -> int:
    """
    Digital root of num.

    Naive: Keep summing digits until < 10.
    Math: Digital root = num mod 9 (with adjustment for 0 and multiples of 9)

    Time: O(1) with math formula
    Space: O(1)
    """
    if num == 0:
        return 0
    if num % 9 == 0:
        return 9
    return num % 9


def addDigits_iterative(num: int) -> int:
    """Iterative approach - O(log n) per iteration."""
    while num >= 10:
        total = 0
        while num:
            total += num % 10
            num //= 10
        num = total
    return num


# Test
print(addDigits(38))   # 2 (3+8=11, 1+1=2)
print(addDigits(0))    # 0
print(addDigits(18))   # 9
```

### Why num % 9 Works (Digital Root)

```
Key insight: 10 ≡ 1 (mod 9)

So any number like 123 = 1×100 + 2×10 + 3
                       ≡ 1×1 + 2×1 + 3 = 6 (mod 9)

The digit sum preserves the value mod 9.
Repeatedly summing converges to the remainder.

Special case: multiples of 9 have digital root 9, not 0.
```

---

## Problem: Power of Two/Three/Four

Check if n is a power of a base.

### Power of Two (LeetCode 231)

```python
def isPowerOfTwo(n: int) -> bool:
    """
    Check if n is power of 2.

    Key insight: Powers of 2 have exactly one bit set.
    n & (n-1) clears the lowest set bit.
    If result is 0, only one bit was set.

    Time: O(1)
    Space: O(1)
    """
    return n > 0 and (n & (n - 1)) == 0


# Test
print(isPowerOfTwo(1))    # True (2^0)
print(isPowerOfTwo(16))   # True (2^4)
print(isPowerOfTwo(3))    # False
print(isPowerOfTwo(0))    # False
```

### Power of Three (LeetCode 326)

```python
def isPowerOfThree(n: int) -> bool:
    """
    Check if n is power of 3.

    Method 1: Repeated division by 3
    Method 2: Largest power of 3 in int range is 3^19 = 1162261467
              If it's divisible by n, n is a power of 3.

    Time: O(1) for method 2
    Space: O(1)
    """
    # Method 2: 3^19 is largest power of 3 in 32-bit signed int
    return n > 0 and 1162261467 % n == 0


def isPowerOfThree_loop(n: int) -> bool:
    """Loop method - O(log n)."""
    if n <= 0:
        return False
    while n % 3 == 0:
        n //= 3
    return n == 1


# Test
print(isPowerOfThree(27))   # True (3^3)
print(isPowerOfThree(9))    # True (3^2)
print(isPowerOfThree(45))   # False
```

### Power of Four (LeetCode 342)

```python
def isPowerOfFour(n: int) -> bool:
    """
    Check if n is power of 4.

    Power of 4 properties:
    1. Must be power of 2: n & (n-1) == 0
    2. The single bit must be at even position (0, 2, 4, ...)
       Mask: 0x55555555 = ...01010101 in binary

    Time: O(1)
    Space: O(1)
    """
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0


def isPowerOfFour_math(n: int) -> bool:
    """Math approach: n = 4^k means n = 2^(2k), so log2(n) is even."""
    import math
    if n <= 0:
        return False
    log = math.log2(n)
    return log == int(log) and int(log) % 2 == 0


# Test
print(isPowerOfFour(16))   # True (4^2)
print(isPowerOfFour(8))    # False (2^3, not power of 4)
print(isPowerOfFour(1))    # True (4^0)
```

---

## Problem: Self Dividing Numbers (LeetCode 728)

A self-dividing number is divisible by every digit it contains.

```python
def selfDividingNumbers(left: int, right: int) -> list[int]:
    """
    Find all self-dividing numbers in [left, right].

    Time: O((right - left) × log(right))
    Space: O(1) excluding output
    """
    def is_self_dividing(n: int) -> bool:
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

## Problem: Integer to Roman (LeetCode 12)

```python
def intToRoman(num: int) -> str:
    """
    Convert integer to Roman numeral.

    Time: O(1) - bounded by max value
    Space: O(1)
    """
    values = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]

    result = []

    for value, symbol in values:
        while num >= value:
            result.append(symbol)
            num -= value

    return ''.join(result)


# Test
print(intToRoman(3))     # "III"
print(intToRoman(58))    # "LVIII"
print(intToRoman(1994))  # "MCMXCIV"
```

---

## Problem: Roman to Integer (LeetCode 13)

```python
def romanToInt(s: str) -> int:
    """
    Convert Roman numeral to integer.

    Key insight: If a smaller value appears before a larger,
    subtract it; otherwise add it.

    Time: O(n)
    Space: O(1)
    """
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
              'C': 100, 'D': 500, 'M': 1000}

    result = 0
    prev = 0

    for char in reversed(s):
        curr = values[char]
        if curr < prev:
            result -= curr
        else:
            result += curr
        prev = curr

    return result


# Test
print(romanToInt("III"))      # 3
print(romanToInt("LVIII"))    # 58
print(romanToInt("MCMXCIV"))  # 1994
```

---

## Problem: Excel Sheet Column Number/Title

```python
def titleToNumber(columnTitle: str) -> int:
    """
    Convert Excel column title to number (LeetCode 171).
    A=1, B=2, ..., Z=26, AA=27, AB=28, ...

    It's base-26, but with 1-indexing (no zero).

    Time: O(n)
    Space: O(1)
    """
    result = 0
    for char in columnTitle:
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result


def convertToTitle(columnNumber: int) -> str:
    """
    Convert number to Excel column title (LeetCode 168).

    Time: O(log n)
    Space: O(log n)
    """
    result = []

    while columnNumber > 0:
        columnNumber -= 1  # Adjust for 1-indexing
        result.append(chr(columnNumber % 26 + ord('A')))
        columnNumber //= 26

    return ''.join(reversed(result))


# Test
print(titleToNumber("A"))    # 1
print(titleToNumber("AB"))   # 28
print(titleToNumber("ZY"))   # 701

print(convertToTitle(1))     # "A"
print(convertToTitle(28))    # "AB"
print(convertToTitle(701))   # "ZY"
```

---

## Problem: Plus One (LeetCode 66)

Add one to a number represented as an array of digits.

```python
def plusOne(digits: list[int]) -> list[int]:
    """
    Add 1 to the number represented by digits array.

    Time: O(n)
    Space: O(1) or O(n) if new array needed
    """
    n = len(digits)

    for i in range(n - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0

    # All 9s case: 999 + 1 = 1000
    return [1] + digits


# Test
print(plusOne([1, 2, 3]))  # [1, 2, 4]
print(plusOne([9, 9, 9]))  # [1, 0, 0, 0]
print(plusOne([0]))        # [1]
```

---

## Complexity Analysis

| Problem | Time | Space | Key Technique |
|---------|------|-------|---------------|
| Palindrome number | O(log n) | O(1) | Reverse half |
| Reverse integer | O(log n) | O(1) | Digit extraction |
| Add digits | O(1) | O(1) | Digital root formula |
| Power of 2/3/4 | O(1) | O(1) | Bit manipulation or math |
| Integer ↔ Roman | O(1) | O(1) | Greedy or lookup |

---

## Edge Cases

1. **Zero**: Often a special case
2. **Negative numbers**: Palindrome check, power checks
3. **Single digit**: 0-9 are palindromes
4. **32-bit overflow**: Critical for reverse integer
5. **Trailing zeros**: 10 is not a palindrome
6. **Maximum values**: INT_MAX, INT_MIN

---

## Interview Tips

1. **Avoid string conversion unless asked**: Shows mathematical sophistication
2. **Handle overflow explicitly**: Especially for reverse integer
3. **Know digit formulas**: `n % 10` and `n // 10`
4. **Memorize bit tricks**: Power of 2: `n & (n-1) == 0`
5. **Test edge cases**: 0, negative, single digit, all 9s

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Palindrome Number | Easy | Reverse half |
| 2 | Reverse Integer | Medium | Overflow handling |
| 3 | Add Digits | Easy | Digital root |
| 4 | Power of Two/Three/Four | Easy | Bit manipulation |
| 5 | Plus One | Easy | Carry propagation |
| 6 | Integer to Roman | Medium | Greedy subtraction |
| 7 | Excel Sheet Column Number | Easy | Base-26 conversion |
| 8 | Self Dividing Numbers | Easy | Digit extraction |
| 9 | Happy Number | Easy | Cycle detection |

---

## Related Sections

- [Bit Manipulation](../15-bit-manipulation/README.md) - Power of 2 checks
- [GCD and LCM](./01-gcd-lcm.md) - Divisibility concepts
