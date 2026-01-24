# Solutions: Binary Basics

## 1. Add Binary

**Problem Statement:**
Given two binary strings `a` and `b`, return their sum as a binary string.

**Constraints:**
- `1 <= a.length, b.length <= 10^4`
- `a` and `b` consist only of '0' or '1' characters.
- Each string does not contain leading zeros except for the zero itself.

**Example:**
- Input: `a = "11", b = "1"`
- Output: `"100"`

**Python Implementation:**
```python
def addBinary(a: str, b: str) -> str:
    result = []
    carry = 0
    i, j = len(a) - 1, len(b) - 1

    while i >= 0 or j >= 0 or carry:
        digit_a = int(a[i]) if i >= 0 else 0
        digit_b = int(b[j]) if j >= 0 else 0

        total = digit_a + digit_b + carry
        result.append(str(total % 2))
        carry = total // 2

        i -= 1
        j -= 1

    return ''.join(reversed(result))
```

## 2. Number Complement

**Problem Statement:**
The complement of an integer is the integer you get when you flip all the 0's to 1's and all the 1's to 0's in its binary representation. Given a positive integer `num`, return its complement.

**Constraints:**
- `1 <= num < 2^31`

**Example:**
- Input: `num = 5` (101 in binary)
- Output: `2` (010 in binary)

**Python Implementation:**
```python
def findComplement(num: int) -> int:
    if num == 0:
        return 1
    # Create a mask with all 1s of the same length as num
    mask = (1 << num.bit_length()) - 1
    # XOR with mask flips all significant bits
    return num ^ mask
```

## 3. Reverse Bits

**Problem Statement:**
Reverse bits of a given 32 bits unsigned integer.

**Constraints:**
- The input must be a binary string of length 32.

**Example:**
- Input: `00000010100101000001111010011100`
- Output: `00111001011110000010100101000000`

**Python Implementation:**
```python
def reverseBits(n: int) -> int:
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```

## 4. Convert Binary Number in Linked List to Integer

**Problem Statement:**
Given `head` which is a reference node to a singly-linked list. The value of each node in the linked list is either 0 or 1. The linked list holds the binary representation of a number. Return the decimal value of the number in the linked list.

**Constraints:**
- The Linked List is not empty.
- Number of nodes will not exceed 30.
- Each node's value is either 0 or 1.

**Example:**
- Input: `head = [1,0,1]`
- Output: `5`

**Python Implementation:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def getDecimalValue(head: ListNode) -> int:
    result = 0
    while head:
        result = (result << 1) | head.val
        head = head.next
    return result
```

## 5. Concatenation of Consecutive Binary Numbers

**Problem Statement:**
Given an integer `n`, return the decimal value of the binary string formed by concatenating the binary representations of 1 to `n` in order, modulo 10^9 + 7.

**Constraints:**
- `1 <= n <= 10^5`

**Example:**
- Input: `n = 3`
- Output: `27` (Binary: "1" + "10" + "11" = "11011" = 27)

**Python Implementation:**
```python
def concatenatedBinary(n: int) -> int:
    MOD = 10**9 + 7
    result = 0
    for i in range(1, n + 1):
        # i.bit_length() tells us how many bits to shift
        result = ((result << i.bit_length()) + i) % MOD
    return result
```
