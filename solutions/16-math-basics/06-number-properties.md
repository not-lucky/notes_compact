# Number Properties

## Practice Problems

### 1. Palindrome Number
**Difficulty:** Easy
**Concept:** Reverse half

```python
def isPalindrome(x: int) -> bool:
    """
    Check if integer is a palindrome without string conversion.
    Time: O(log x)
    Space: O(1)
    """
    if x < 0 or (x % 10 == 0 and x != 0):
        return False

    rev = 0
    while x > rev:
        rev = rev * 10 + x % 10
        x //= 10

    return x == rev or x == rev // 10
```

### 2. Reverse Integer
**Difficulty:** Medium
**Concept:** Overflow handling

```python
def reverse(x: int) -> int:
    """
    Reverse digits of a 32-bit signed integer.
    Time: O(log x)
    Space: O(1)
    """
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31

    res = 0
    sign = 1 if x >= 0 else -1
    x = abs(x)

    while x:
        digit = x % 10
        x //= 10

        if res > (INT_MAX - digit) // 10:
            return 0

        res = res * 10 + digit

    res *= sign
    if res < INT_MIN or res > INT_MAX:
        return 0
    return res
```
