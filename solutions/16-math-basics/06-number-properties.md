# Practice Problems: Number Properties

This file contains optimal Python solutions for the practice problems listed in the Number Properties notes.

---

## 1. Palindrome Number

**Problem Statement:**
Given an integer `x`, return `true` if `x` is a palindrome, and `false` otherwise. An integer is a palindrome when it reads the same backward as forward.

**Examples & Edge Cases:**

- **Example 1:** `x = 121` -> Output: `True`
- **Example 2:** `x = -121` -> Output: `False` (From left to right: -121. From right to left: 121-)
- **Example 3:** `x = 10` -> Output: `False`
- **Edge Case:** `x = 0` -> Output: `True`

**Optimal Python Solution:**

```python
def isPalindrome(x: int) -> bool:
    """
    Checks if x is a palindrome without converting to string.
    Reverses the second half of the number and compares it with the first half.
    """
    # Negative numbers and numbers ending in 0 (except 0 itself) are not palindromes.
    if x < 0 or (x % 10 == 0 and x != 0):
        return False

    reversed_half = 0
    while x > reversed_half:
        # Move the last digit of x to reversed_half
        reversed_half = reversed_half * 10 + x % 10
        x //= 10

    # For even number of digits: x == reversed_half
    # For odd number of digits: x == reversed_half // 10 (middle digit doesn't matter)
    return x == reversed_half or x == reversed_half // 10
```

**Explanation:**

1. **Half-Reversal**: To avoid reversing the whole number (which could overflow a 32-bit integer), we only reverse the last half.
2. **Stopping Condition**: When `reversed_half >= x`, we have reached or passed the middle of the number.
3. **Comparison**:
   - If the number has an even count of digits, `x` should equal `reversed_half`.
   - If the count is odd, `x` should equal `reversed_half // 10` (the middle digit is ignored).

**Complexity Analysis:**

- **Time Complexity:** $O(\log_{10} x)$ because we process half of the digits.
- **Space Complexity:** $O(1)$.

---

## 2. Reverse Integer

**Problem Statement:**
Given a signed 32-bit integer `x`, return `x` with its digits reversed. If reversing `x` causes the value to go outside the signed 32-bit integer range $[-2^{31}, 2^{31} - 1]$, then return 0.

**Examples & Edge Cases:**

- **Example 1:** `x = 123` -> Output: `321`
- **Example 2:** `x = -123` -> Output: `-321`
- **Example 3:** `x = 120` -> Output: `21`
- **Edge Case:** Reversing leads to overflow (e.g., `1534236469` -> 0).

**Optimal Python Solution:**

```python
def reverse(x: int) -> int:
    """
    Reverses the digits of a 32-bit signed integer.
    Handles overflow explicitly.
    """
    INT_MIN, INT_MAX = -2147483648, 2147483647

    res = 0
    # Use absolute value for processing, handle sign at the end
    sign = -1 if x < 0 else 1
    x = abs(x)

    while x != 0:
        digit = x % 10
        x //= 10

        # Check for potential overflow before updating result
        # Python handles large ints, but we must return 0 per constraints
        if res > (INT_MAX - digit) // 10:
            return 0

        res = res * 10 + digit

    return res * sign
```

**Explanation:**

1. **Digit Extraction**: Use `% 10` and `// 10` to extract and remove the last digit.
2. **Overflow Check**: In each step, we check if `res * 10 + digit > INT_MAX`. Rearranged, this is `res > (INT_MAX - digit) // 10`.
3. **Sign Handling**: We process the magnitude and apply the sign at the very end.

**Complexity Analysis:**

- **Time Complexity:** $O(\log_{10} x)$ as we iterate through each digit.
- **Space Complexity:** $O(1)$.

---

## 3. Add Digits

**Problem Statement:**
Given an integer `num`, repeatedly add all its digits until the result has only one digit, and return it.

**Examples & Edge Cases:**

- **Example 1:** `num = 38` -> Output: `2` ($3+8=11, 1+1=2$)
- **Example 2:** `num = 0` -> Output: `0`
- **Edge Case:** Multiples of 9 (e.g., 18 -> 9).

**Optimal Python Solution:**

```python
def addDigits(num: int) -> int:
    """
    Calculates the digital root of a number in O(1).
    """
    if num == 0:
        return 0
    # Property of digital root: num % 9, but 9 if multiple of 9
    return 1 + (num - 1) % 9
```

**Explanation:**

1. **Mathematical Pattern**: The sum of digits of a number $n$ is congruent to $n \pmod 9$. This is because $10^k \equiv 1^k \equiv 1 \pmod 9$.
2. **Congruence**: Repeatedly summing digits eventually reaches the "digital root", which is essentially the number modulo 9 (where 0 is represented as 9 for positive multiples).
3. **Formula**: `1 + (num - 1) % 9` maps 1-9 to 1-9 and 10 to 1, etc., correctly handling the "multiples of 9" edge case.

**Complexity Analysis:**

- **Time Complexity:** $O(1)$.
- **Space Complexity:** $O(1)$.

---

## 4. Power of Two / Three / Four

**Problem Statement:**
Given an integer `n`, return `true` if it is a power of 2, 3, or 4 respectively.

**Optimal Python Solutions:**

```python
def isPowerOfTwo(n: int) -> bool:
    """
    Checks if n is a power of two using bitwise operations.
    A power of two has exactly one bit set.
    """
    return n > 0 and (n & (n - 1)) == 0

def isPowerOfThree(n: int) -> bool:
    """
    Checks if n is a power of three.
    1162261467 is the largest 32-bit power of three (3^19).
    """
    return n > 0 and 1162261467 % n == 0

def isPowerOfFour(n: int) -> bool:
    """
    Checks if n is a power of four.
    Properties: 1. Power of two. 2. Set bit is at an even position.
    """
    # 0x55555555 is a mask with 1s at positions 0, 2, 4, ...
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0
```

**Explanation:**

- **Power of Two**: $n \& (n-1)$ clears the only set bit in a power of two.
- **Power of Three**: Since 3 is prime, any power of 3 will only have 3 as a prime factor. We divide the largest possible power of 3 by $n$.
- **Power of Four**: Powers of four are a subset of powers of two where the set bit is at an even index ($4^0=1$ at index 0, $4^1=4$ at index 2, $4^2=16$ at index 4).

**Complexity Analysis:**

- **Time Complexity:** $O(1)$ for all three checks.
- **Space Complexity:** $O(1)$.

---

## 5. Plus One

**Problem Statement:**
You are given a large integer represented as an integer array `digits`, where each `digits[i]` is the $i$-th digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading 0's, except the number 0 itself. Increment the large integer by one and return the resulting array of digits.

**Examples & Edge Cases:**

- **Example 1:** `digits = [1,2,3]` -> Output: `[1,2,4]`
- **Example 2:** `digits = [9,9]` -> Output: `[1,0,0]`
- **Edge Case:** All digits are 9.

**Optimal Python Solution:**

```python
def plusOne(digits: list[int]) -> list[int]:
    """
    Increments the number represented by the digits array by one.
    """
    n = len(digits)
    # Start from the last digit
    for i in range(n - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        # If digit is 9, it becomes 0 and we carry over to the left
        digits[i] = 0

    # If we are here, it means all digits were 9 (e.g., 999 -> 1000)
    return [1] + digits
```

**Explanation:**

1. **Right-to-Left Traversal**: We add 1 to the last digit.
2. **Carry Logic**: If the digit is less than 9, we just increment it and return. If it's 9, it becomes 0 and the carry moves to the next digit.
3. **Corner Case**: If the loop finishes, it means we had a carry from the most significant digit (e.g., 999 becomes 000). We prepend 1 to the array.

**Complexity Analysis:**

- **Time Complexity:** $O(N)$ where $N$ is the number of digits.
- **Space Complexity:** $O(1)$ (or $O(N)$ if we count the space for the new array in the all-9s case).

---

## 6. Integer to Roman

**Problem Statement:**
Convert an integer to a Roman numeral string.

**Examples & Edge Cases:**

- **Example 1:** `3` -> `"III"`
- **Example 2:** `58` -> `"LVIII"`
- **Example 3:** `1994` -> `"MCMXCIV"`

**Optimal Python Solution:**

```python
def intToRoman(num: int) -> str:
    """
    Converts an integer to its Roman numeral representation.
    """
    # Mapping of values to symbols including subtractive combinations
    mapping = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    res = []
    for value, symbol in mapping:
        if num == 0: break
        count, num = divmod(num, value)
        res.append(symbol * count)

    return "".join(res)
```

**Explanation:**

1. **Greedy Strategy**: We start with the largest possible Roman numeral values.
2. **Subtractive Combinations**: We include cases like 4 (IV) and 900 (CM) directly in our mapping to simplify the logic.
3. **Iteration**: For each symbol, we see how many times it fits into the current number using `divmod`.

**Complexity Analysis:**

- **Time Complexity:** $O(1)$ because the number of symbols is fixed and the maximum value is 3999.
- **Space Complexity:** $O(1)$.

---

## 7. Excel Sheet Column Number

**Problem Statement:**
Given a string `columnTitle` that represents the column title as appears in an Excel sheet, return its corresponding column number.

**Examples & Edge Cases:**

- **Example 1:** `A` -> `1`
- **Example 2:** `AB` -> `28`
- **Example 3:** `ZY` -> `701`

**Optimal Python Solution:**

```python
def titleToNumber(columnTitle: str) -> int:
    """
    Converts Excel title to number (Base-26 with 1-indexing).
    """
    res = 0
    for char in columnTitle:
        # Each position represents a power of 26
        # A=1, B=2 ... Z=26
        val = ord(char) - ord('A') + 1
        res = res * 26 + val
    return res
```

**Explanation:**

1. **Base-26 Conversion**: This is essentially converting a number from base-26 to base-10.
2. **Calculation**: As we move from left to right, we multiply the existing result by 26 and add the value of the current character ($A=1, B=2, \dots$).

**Complexity Analysis:**

- **Time Complexity:** $O(N)$ where $N$ is the length of the string.
- **Space Complexity:** $O(1)$.

---

## 8. Self Dividing Numbers

**Problem Statement:**
A self-dividing number is a number that is divisible by every digit it contains. For example, 128 is a self-dividing number because $128 \% 1 = 0$, $128 \% 2 = 0$, and $128 \% 8 = 0$. A self-dividing number is not allowed to contain the digit zero.

Given two integers `left` and `right`, return a list of all the self-dividing numbers in the range `[left, right]`.

**Examples & Edge Cases:**

- **Example:** `left = 1, right = 22` -> `[1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 22]`
- **Edge Case:** Numbers containing 0 are excluded.

**Optimal Python Solution:**

```python
def selfDividingNumbers(left: int, right: int) -> list[int]:
    """
    Finds all self-dividing numbers in range [left, right].
    """
    def is_self_dividing(n):
        temp = n
        while temp > 0:
            digit = temp % 10
            if digit == 0 or n % digit != 0:
                return False
            temp //= 10
        return True

    res = []
    for num in range(left, right + 1):
        if is_self_dividing(num):
            res.append(num)
    return res
```

**Explanation:**

1. **Iteration**: Loop through every number in the range.
2. **Digit Checking**: For each number, extract its digits one by one. Check if the digit is zero or if the number is not divisible by that digit.
3. **Short-circuit**: As soon as we find an invalid digit, we return `False`.

**Complexity Analysis:**

- **Time Complexity:** $O(D \cdot \log_{10}(\text{right}))$, where $D$ is the number of integers in the range. We check $\log_{10} n$ digits for each number.
- **Space Complexity:** $O(1)$ excluding the output list.

---

## 9. Happy Number

**Problem Statement:**
A happy number is a number defined by the following process: Starting with any positive integer, replace the number by the sum of the squares of its digits. Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy.

**Examples & Edge Cases:**

- **Example 1:** `n = 19` -> `True`
- **Example 2:** `n = 2` -> `False`

**Optimal Python Solution:**

```python
def isHappy(n: int) -> bool:
    """
    Determines if a number is happy using Floyd's Cycle-finding Algorithm.
    """
    def get_next(number):
        total_sum = 0
        while number > 0:
            number, digit = divmod(number, 10)
            total_sum += digit ** 2
        return total_sum

    slow = n
    fast = get_next(n)
    while fast != 1 and slow != fast:
        slow = get_next(slow)
        fast = get_next(get_next(fast))

    return fast == 1
```

**Explanation:**

1. **Mathematical Property**: The sequence will either reach 1 or enter a known cycle (like the one starting with 4).
2. **Cycle Detection**: Using `slow` and `fast` pointers (Tortoise and Hare), we can detect if we have entered a loop without needing extra space for a hash set.

**Complexity Analysis:**

- **Time Complexity:** $O(\log n)$. The number of steps to converge or cycle is small.
- **Space Complexity:** $O(1)$.
