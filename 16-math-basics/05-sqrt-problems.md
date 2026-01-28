# Square Root Problems

> **Prerequisites:** [Binary Search](../10-binary-search/README.md) (for integer sqrt)

## Building Intuition

**The "Goldilocks Search" Mental Model**

Finding √n is like finding the perfect temperature:

- If guess² < n: too cold, go higher
- If guess² > n: too hot, go lower
- If guess² = n: just right!

Binary search naturally fits this pattern.

**Why √n Appears Everywhere**

Square root is special because it's the "balance point":

- If n = a × b, at least one of a or b is ≤ √n
- This is why primality checking only goes to √n
- This is why some algorithms have O(√n) complexity (checking divisors)

**Newton's Method: Faster Than Binary Search**

Instead of halving the search range, Newton's method uses calculus:

- If x is too big, n/x is too small
- Average them: (x + n/x) / 2 is a better guess
- Converges quadratically (doubles correct digits each iteration)

For integers, this means ~log(log(n)) iterations vs log(n) for binary search.

---

## Interview Context

Square root problems test:

- Binary search implementation skills
- Edge case handling (0, 1, large numbers)
- Understanding of mathematical properties
- Newton's method (advanced)

Common patterns: integer square root, perfect square checks, and problems where √n appears in complexity analysis.

---

## Pattern: Binary Search for Integer Square Root

Find the largest integer `x` such that `x² ≤ n`.

### Key Insight

```
For n = 50:
  7² = 49 ≤ 50 ✓
  8² = 64 > 50  ✗

Answer: 7

Binary search in range [0, n] to find largest x where x² ≤ n.
```

### Visualization

```
Find isqrt(50):

Range: [0, 50]
  mid = 25, 25² = 625 > 50  → right = 24
Range: [0, 24]
  mid = 12, 12² = 144 > 50  → right = 11
Range: [0, 11]
  mid = 5, 5² = 25 ≤ 50     → left = 6, ans = 5
Range: [6, 11]
  mid = 8, 8² = 64 > 50     → right = 7
Range: [6, 7]
  mid = 6, 6² = 36 ≤ 50     → left = 7, ans = 6
Range: [7, 7]
  mid = 7, 7² = 49 ≤ 50     → left = 8, ans = 7
Range: [8, 7] → done

Answer: 7
```

---

## Implementation

### Integer Square Root (LeetCode 69)

```python
def mySqrt(x: int) -> int:
    """
    Compute floor(sqrt(x)) using binary search.

    Time: O(log x)
    Space: O(1)
    """
    if x < 2:
        return x

    left, right = 1, x // 2  # sqrt(x) ≤ x/2 for x ≥ 4
    result = 0

    while left <= right:
        mid = (left + right) // 2
        square = mid * mid

        if square == x:
            return mid
        elif square < x:
            result = mid  # Could be the answer
            left = mid + 1
        else:
            right = mid - 1

    return result


# Test
print(mySqrt(4))    # 2
print(mySqrt(8))    # 2 (floor of 2.83...)
print(mySqrt(0))    # 0
print(mySqrt(1))    # 1
print(mySqrt(100))  # 10
```

### Using Python Built-in

```python
import math

# Python 3.8+ has math.isqrt for integer square root
print(math.isqrt(50))  # 7

# For older Python, be careful with float sqrt
print(int(math.sqrt(50)))  # 7 (works here)
print(int(math.sqrt(2**50)))  # May be off by 1 due to float precision!
```

---

## Problem: Valid Perfect Square (LeetCode 367)

Check if a number is a perfect square without using sqrt.

```python
def isPerfectSquare(num: int) -> bool:
    """
    Check if num is a perfect square using binary search.

    Time: O(log num)
    Space: O(1)
    """
    if num < 1:
        return False

    left, right = 1, num

    while left <= right:
        mid = (left + right) // 2
        square = mid * mid

        if square == num:
            return True
        elif square < num:
            left = mid + 1
        else:
            right = mid - 1

    return False


# Test
print(isPerfectSquare(16))  # True (4²)
print(isPerfectSquare(14))  # False
print(isPerfectSquare(1))   # True (1²)
print(isPerfectSquare(0))   # False (by definition, or True depending on interpretation)
```

### Bit Manipulation Trick

```python
def isPerfectSquare_bit(num: int) -> bool:
    """
    Perfect squares in binary have specific patterns.
    Alternative: Use Newton's method or 1+3+5+... = n² trick.
    """
    # Perfect square property: 1 + 3 + 5 + ... + (2n-1) = n²
    i = 1
    while num > 0:
        num -= i
        i += 2

    return num == 0
```

---

## Pattern: Newton's Method (Heron's Method)

Iteratively improve an estimate of √n using:

```
x_next = (x + n/x) / 2
```

### Why It Works

```
If x is an overestimate of √n, then n/x is an underestimate.
The average (x + n/x)/2 is a better estimate.

Example: √50
  x = 25 → next = (25 + 50/25) / 2 = (25 + 2) / 2 = 13.5
  x = 13.5 → next = (13.5 + 50/13.5) / 2 ≈ 8.6
  x = 8.6 → next = (8.6 + 50/8.6) / 2 ≈ 7.2
  x = 7.2 → next ≈ 7.07
  ...converges to 7.071...
```

### Implementation

```python
def sqrt_newton(n: int) -> int:
    """
    Integer square root using Newton's method.

    Time: O(log n) iterations, each O(1)
    Space: O(1)
    """
    if n < 2:
        return n

    x = n
    while x * x > n:
        x = (x + n // x) // 2

    return x


# Test
print(sqrt_newton(50))   # 7
print(sqrt_newton(100))  # 10
print(sqrt_newton(2))    # 1
```

---

## Problem: Sum of Square Numbers (LeetCode 633)

Given a non-negative integer c, decide whether there're two integers a and b such that a² + b² = c.

```python
def judgeSquareSum(c: int) -> bool:
    """
    Check if c = a² + b² for some integers a, b.

    Approach: Two pointers
    - a starts at 0
    - b starts at floor(√c)
    - Adjust based on sum

    Time: O(√c)
    Space: O(1)
    """
    import math

    a = 0
    b = int(math.isqrt(c))

    while a <= b:
        total = a * a + b * b
        if total == c:
            return True
        elif total < c:
            a += 1
        else:
            b -= 1

    return False


# Test
print(judgeSquareSum(5))    # True (1² + 2² = 5)
print(judgeSquareSum(3))    # False
print(judgeSquareSum(4))    # True (0² + 2² = 4)
print(judgeSquareSum(2))    # True (1² + 1² = 2)
```

---

## Problem: Perfect Squares (LeetCode 279)

Find the least number of perfect square numbers that sum to n.

```python
def numSquares(n: int) -> int:
    """
    Minimum perfect squares that sum to n.

    DP approach: dp[i] = min squares to sum to i
    dp[i] = min(dp[i - j²]) + 1 for all valid j

    Time: O(n√n)
    Space: O(n)
    """
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1

    return dp[n]


# Test
print(numSquares(12))  # 3 (4 + 4 + 4)
print(numSquares(13))  # 2 (4 + 9)
print(numSquares(1))   # 1
```

### BFS Approach (Often Faster in Practice)

```python
from collections import deque

def numSquares_bfs(n: int) -> int:
    """
    BFS approach - find shortest path to 0.

    Time: O(n√n) worst case
    Space: O(n)
    """
    if n == 0:
        return 0

    squares = []
    i = 1
    while i * i <= n:
        squares.append(i * i)
        i += 1

    queue = deque([n])
    level = 0
    visited = {n}

    while queue:
        level += 1
        for _ in range(len(queue)):
            curr = queue.popleft()
            for sq in squares:
                remainder = curr - sq
                if remainder == 0:
                    return level
                if remainder > 0 and remainder not in visited:
                    visited.add(remainder)
                    queue.append(remainder)

    return -1  # Should never reach here for valid input
```

---

## Problem: Arranging Coins (LeetCode 441)

You have n coins to form a staircase. The k-th row has k coins. Find the number of complete rows.

```python
def arrangeCoins(n: int) -> int:
    """
    Find max k where 1+2+...+k ≤ n
    i.e., k(k+1)/2 ≤ n
    i.e., k² + k - 2n ≤ 0

    Using quadratic formula: k = (-1 + √(1 + 8n)) / 2

    Time: O(1)
    Space: O(1)
    """
    # Math solution
    import math
    return int((-1 + math.sqrt(1 + 8 * n)) / 2)


def arrangeCoins_binary(n: int) -> int:
    """
    Binary search approach.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, n
    result = 0

    while left <= right:
        mid = (left + right) // 2
        coins_needed = mid * (mid + 1) // 2

        if coins_needed <= n:
            result = mid
            left = mid + 1
        else:
            right = mid - 1

    return result


# Test
print(arrangeCoins(5))   # 2 (1+2=3 ≤ 5, but 1+2+3=6 > 5)
print(arrangeCoins(8))   # 3 (1+2+3=6 ≤ 8, but 1+2+3+4=10 > 8)
```

---

## Complexity Analysis

| Algorithm                    | Time     | Space | Notes              |
| ---------------------------- | -------- | ----- | ------------------ |
| Binary search sqrt           | O(log n) | O(1)  | Most common        |
| Newton's method              | O(log n) | O(1)  | Faster convergence |
| Perfect square check         | O(log n) | O(1)  | Binary search      |
| Sum of squares (two pointer) | O(√n)    | O(1)  | a² + b² = c        |
| numSquares (DP)              | O(n√n)   | O(n)  | Lagrange's theorem |

---

## Common Variations

### 1. Kth Smallest in Multiplication Table

Uses binary search where sqrt appears in analysis.

```python
def findKthNumber(m: int, n: int, k: int) -> int:
    """
    Find kth smallest in m×n multiplication table.

    Time: O(m log(m*n))
    Space: O(1)
    """
    def count_le(x: int) -> int:
        """Count numbers ≤ x in the table."""
        count = 0
        for i in range(1, m + 1):
            count += min(x // i, n)
        return count

    left, right = 1, m * n

    while left < right:
        mid = (left + right) // 2
        if count_le(mid) >= k:
            right = mid
        else:
            left = mid + 1

    return left
```

### 2. Power of N Check

```python
def is_power_of_n(num: int, n: int) -> bool:
    """Check if num = n^k for some k ≥ 0."""
    if num <= 0:
        return False
    if num == 1:
        return True  # n^0 = 1

    while num % n == 0:
        num //= n

    return num == 1


print(is_power_of_n(27, 3))  # True (3³)
print(is_power_of_n(16, 4))  # True (4²)
```

### 3. Count Perfect Squares in Range

```python
def count_perfect_squares(low: int, high: int) -> int:
    """Count perfect squares in [low, high]."""
    import math

    # First perfect square ≥ low
    sqrt_low = math.ceil(math.sqrt(low))
    # Last perfect square ≤ high
    sqrt_high = int(math.sqrt(high))

    if sqrt_low > sqrt_high:
        return 0
    return sqrt_high - sqrt_low + 1


print(count_perfect_squares(1, 100))   # 10 (1,4,9,16,25,36,49,64,81,100)
print(count_perfect_squares(10, 20))   # 1 (16)
```

---

## Edge Cases

1. **n = 0**: sqrt(0) = 0
2. **n = 1**: sqrt(1) = 1
3. **Large n**: Avoid overflow in mid \* mid (use mid <= n // mid)
4. **Perfect squares**: Should return exact value
5. **Negative input**: Undefined for real sqrt, return error or 0

---

## Interview Tips

1. **Start with binary search**: Most interviewers expect this
2. **Mention Newton's method**: Shows mathematical sophistication
3. **Handle edge cases explicitly**: 0, 1, and large numbers
4. **Watch for overflow**: `mid * mid` can overflow in some languages
5. **Know math.isqrt**: Python 3.8+ has it built-in

### Avoiding Overflow

```python
def mySqrt_safe(x: int) -> int:
    """Overflow-safe version."""
    if x < 2:
        return x

    left, right = 1, x // 2

    while left <= right:
        mid = (left + right) // 2

        # Instead of mid * mid, use mid <= x // mid
        if mid <= x // mid:
            if (mid + 1) > x // (mid + 1):
                return mid
            left = mid + 1
        else:
            right = mid - 1

    return right
```

---

## Practice Problems

| #   | Problem                              | Difficulty | Key Concept                        |
| --- | ------------------------------------ | ---------- | ---------------------------------- |
| 1   | Sqrt(x)                              | Easy       | Binary search                      |
| 2   | Valid Perfect Square                 | Easy       | Binary search or math              |
| 3   | Sum of Square Numbers                | Medium     | Two pointers                       |
| 4   | Perfect Squares                      | Medium     | DP or BFS                          |
| 5   | Arranging Coins                      | Easy       | Binary search or quadratic formula |
| 6   | Kth Smallest in Multiplication Table | Hard       | Binary search with counting        |

---

## When NOT to Roll Your Own Sqrt

1. **Python 3.8+ exists**: Use `math.isqrt()` for integer sqrt—it's correct and fast
2. **Floating point is fine**: Use `math.sqrt()` for approximate answers
3. **Small numbers**: For n < 1000, even a loop works fine
4. **Precision concerns**: `int(math.sqrt(n))` can be off by 1 for large n—verify with multiplication

### Common Pitfalls

```python
# WRONG: Can be off by 1 due to float precision
result = int(math.sqrt(n))

# RIGHT: Verify the result
result = int(math.sqrt(n))
if (result + 1) ** 2 == n:
    result += 1

# BEST: Use math.isqrt (Python 3.8+)
result = math.isqrt(n)
```

---

## Related Sections

- [Binary Search](../10-binary-search/README.md) - Foundation technique
- [Number Properties](./06-number-properties.md) - Related math patterns
