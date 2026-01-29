# Binary Basics Solutions

## 1. Add Binary

**Problem Statement**: Given two binary strings `a` and `b`, return their sum as a binary string.

### Examples & Edge Cases

- **Example 1**: `a = "11"`, `b = "1"` → `100` (3 + 1 = 4)
- **Example 2**: `a = "1010"`, `b = "1011"` → `10101` (10 + 11 = 21)
- **Edge Cases**:
  - Empty strings: Not applicable per constraints (usually non-empty).
  - Different lengths: `a = "1"`, `b = "111"`.
  - Carrying over to a new bit: `a = "1"`, `b = "1"`.

### Optimal Python Solution

```python
def addBinary(a: str, b: str) -> str:
    """
    Adds two binary strings and returns the result as a binary string.

    Logic: Iterate from right to left, adding digits and maintaining a carry.
    """
    result = []
    carry = 0
    i, j = len(a) - 1, len(b) - 1

    while i >= 0 or j >= 0 or carry:
        # Get bits from each string, or 0 if we've reached the beginning
        digit_a = int(a[i]) if i >= 0 else 0
        digit_b = int(b[j]) if j >= 0 else 0

        # Sum digits and carry
        total = digit_a + digit_b + carry

        # Current bit is total % 2
        result.append(str(total % 2))

        # Carry is total // 2
        carry = total // 2

        i -= 1
        j -= 1

    # Result is built in reverse order
    return "".join(reversed(result))
```

### Explanation

The algorithm simulates manual addition (column by column from right to left). We use two pointers starting at the end of each string and a `carry` variable. At each step, we sum the bits and the carry. The bit for the current position is `sum % 2`, and the new carry is `sum // 2`. We continue until both strings are exhausted and there is no remaining carry.

### Complexity Analysis

- **Time Complexity**: O(max(N, M)) where N and M are the lengths of strings `a` and `b`. We traverse each string at most once.
- **Space Complexity**: O(max(N, M)) to store the result string.

---

## 2. Number Complement

**Problem Statement**: Given a positive integer, return its complement number. The complement flips all bits in the binary representation.

### Examples & Edge Cases

- **Example 1**: `5` (101) → `2` (010)
- **Example 2**: `1` (1) → `0` (0)
- **Edge Cases**:
  - `0`: Usually handled as 1 (depending on constraints).
  - Powers of 2: `4` (100) → `3` (011).

### Optimal Python Solution

```python
def findComplement(num: int) -> int:
    """
    Finds the bitwise complement by XORing with a mask of all 1s.
    """
    if num == 0:
        return 1

    # Create a mask with all 1s of the same length as num
    # num.bit_length() gives the number of bits required to represent num
    mask = (1 << num.bit_length()) - 1

    # XORing num with a mask of 1s flips all bits
    return num ^ mask
```

### Explanation

To flip all bits of a number within its significant bit range, we XOR it with a mask consisting of all ones. For example, if `num = 5` (binary `101`), we need a mask `111` (decimal `7`). `101 ^ 111 = 010` (decimal `2`). We calculate the mask by left-shifting `1` by the number of bits in `num` and subtracting `1`.

### Complexity Analysis

- **Time Complexity**: O(1) or O(bit_length), which is effectively O(1) for fixed-width integers (32 or 64 bit).
- **Space Complexity**: O(1) as we only use a few variables.

---

## 3. Reverse Bits

**Problem Statement**: Reverse bits of a given 32 bits unsigned integer.

### Examples & Edge Cases

- **Example**: `00000010100101000001111010011100` → `00111001011110000010100101000000`
- **Edge Cases**:
  - `0`: Reverses to `0`.
  - `0xFFFFFFFF`: Reverses to `0xFFFFFFFF`.

### Optimal Python Solution

```python
def reverseBits(n: int) -> int:
    """
    Reverses the bits of a 32-bit integer.
    """
    result = 0
    # Process all 32 bits
    for _ in range(32):
        # Shift result left to make room for the next bit
        result <<= 1
        # Add the rightmost bit of n to result
        result |= (n & 1)
        # Shift n right to process the next bit
        n >>= 1
    return result
```

### Explanation

We iterate 32 times (for each bit). In each iteration, we shift our `result` to the left to "make room", extract the least significant bit (LSB) of `n` using `n & 1`, and add it to our `result` using OR. Then we shift `n` to the right to bring the next bit to the LSB position.

### Complexity Analysis

- **Time Complexity**: O(1) because we always perform exactly 32 iterations.
- **Space Complexity**: O(1) as we use a single variable for the result.

---

## 4. Convert Binary Number in Linked List to Integer

**Problem Statement**: Given the head of a singly linked list where each node contains either a 0 or a 1, return the decimal value of the number represented by the list.

### Examples & Edge Cases

- **Example**: `head = [1, 0, 1]` → `5`
- **Edge Cases**:
  - Single node: `[1]` → `1`.
  - All zeros: `[0, 0, 0]` → `0`.

### Optimal Python Solution

```python
def getDecimalValue(head) -> int:
    """
    Converts a binary linked list to a decimal integer.
    """
    num = 0
    curr = head
    while curr:
        # Shift current number left (multiply by 2) and add the new bit
        num = (num << 1) | curr.val
        curr = curr.next
    return num
```

### Explanation

We traverse the linked list from head to tail. For each node, we shift the accumulated number `num` to the left by 1 (equivalent to multiplying by 2) and then add the node's value (0 or 1). This is the standard way to convert binary to decimal while reading from most significant bit to least significant bit.

### Complexity Analysis

- **Time Complexity**: O(N) where N is the number of nodes in the linked list. We visit each node once.
- **Space Complexity**: O(1) as we only store the resulting integer.

---

## 5. Concatenation of Consecutive Binary Numbers

**Problem Statement**: Given an integer `n`, return the decimal value of the binary string formed by concatenating the binary representations of 1 to `n` in order, modulo 10^9 + 7.

### Examples & Edge Cases

- **Example 1**: `n = 1` → `1`
- **Example 2**: `n = 3` → `11011` (binary 1, 10, 11) → `27`
- **Edge Cases**:
  - Large `n`: Requires modulo at each step.

### Optimal Python Solution

```python
def concatenatedBinary(n: int) -> int:
    """
    Concatenates binary representations from 1 to n and returns the decimal value.
    """
    MOD = 10**9 + 7
    result = 0

    for i in range(1, n + 1):
        # bit_length() tells us how many bits i occupies
        # Shift result left by that length and add i
        result = ((result << i.bit_length()) | i) % MOD

    return result
```

### Explanation

As we iterate from 1 to `n`, for each number `i`, we need to append its binary representation to our existing `result`. Appending bits means shifting the `result` to the left by the number of bits in `i` and then ORing/adding `i`. The number of bits in `i` is given by `i.bit_length()`. We apply the modulo operation at each step to keep the number within range.

### Complexity Analysis

- **Time Complexity**: O(N) where N is the input integer `n`. We loop from 1 to `n` and perform constant time bitwise operations in each iteration.
- **Space Complexity**: O(1) as we only maintain the `result` variable.
