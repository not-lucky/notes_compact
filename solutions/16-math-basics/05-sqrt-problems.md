# Practice Problems: Square Root Problems

This file contains optimal Python solutions for the practice problems listed in the Square Root Problems notes.

---

## 1. Sqrt(x)

**Problem Statement:**
Given a non-negative integer `x`, compute and return the square root of `x`. Since the return type is an integer, the decimal digits are truncated, and only the integer part of the result is returned.

**Examples & Edge Cases:**
- **Example 1:** `x = 4` -> Output: `2`
- **Example 2:** `x = 8` -> Output: `2` (sqrt(8) = 2.82842..., which is truncated to 2)
- **Edge Case:** `x = 0` -> Output: `0`
- **Edge Case:** `x = 1` -> Output: `1`

**Optimal Python Solution:**
```python
def mySqrt(x: int) -> int:
    """
    Computes floor(sqrt(x)) using Binary Search.
    """
    if x < 2:
        return x

    left, right = 2, x // 2

    while left <= right:
        mid = left + (right - left) // 2
        num = mid * mid
        if num > x:
            right = mid - 1
        elif num < x:
            left = mid + 1
        else:
            return mid

    return right
```

**Explanation:**
1. **Search Space**: For $x \ge 2$, the square root is always between 2 and $x/2$.
2. **Binary Search**: We look for an integer $k$ such that $k^2 \le x < (k+1)^2$.
3. **Midpoint check**:
   - If `mid * mid > x`, the answer must be smaller, so we move `right`.
   - If `mid * mid < x`, the answer might be `mid` or larger, so we move `left`.
   - If `mid * mid == x`, we found the exact square root.
4. **Result**: If we don't find an exact match, the `right` pointer will end up at the floor value.

**Complexity Analysis:**
- **Time Complexity:** $O(\log x)$ because the search space is halved in each step.
- **Space Complexity:** $O(1)$.

---

## 2. Valid Perfect Square

**Problem Statement:**
Given a positive integer `num`, return `True` if `num` is a perfect square else `False`. Do not use any built-in library function such as `sqrt`.

**Examples & Edge Cases:**
- **Example 1:** `num = 16` -> Output: `True`
- **Example 2:** `num = 14` -> Output: `False`
- **Edge Case:** `num = 1` -> Output: `True`

**Optimal Python Solution:**
```python
def isPerfectSquare(num: int) -> bool:
    """
    Checks if num is a perfect square using Binary Search.
    """
    if num < 1:
        return False
    if num == 1:
        return True

    left, right = 1, num // 2

    while left <= right:
        mid = left + (right - left) // 2
        square = mid * mid
        if square == num:
            return True
        elif square < num:
            left = mid + 1
        else:
            right = mid - 1

    return False
```

**Explanation:**
1. **Binary Search**: Similar to `mySqrt`, but we specifically check for an exact match.
2. **Bounds**: We check integers from 1 up to `num // 2`.
3. **Newton's Method (Alternative)**: Newton's method $x_{n+1} = \frac{1}{2}(x_n + \frac{\text{num}}{x_n})$ also works very efficiently for this.

**Complexity Analysis:**
- **Time Complexity:** $O(\log \text{num})$.
- **Space Complexity:** $O(1)$.

---

## 3. Sum of Square Numbers

**Problem Statement:**
Given a non-negative integer `c`, decide whether there are two integers $a$ and $b$ such that $a^2 + b^2 = c$.

**Examples & Edge Cases:**
- **Example 1:** `c = 5` -> Output: `True` ($1^2 + 2^2 = 5$)
- **Example 2:** `c = 3` -> Output: `False`
- **Edge Case:** `c = 0` -> Output: `True` ($0^2 + 0^2 = 0$)

**Optimal Python Solution:**
```python
import math

def judgeSquareSum(c: int) -> bool:
    """
    Decides if c = a^2 + b^2 using Two Pointers.
    """
    # Start pointers at 0 and sqrt(c)
    left = 0
    right = int(math.sqrt(c))

    while left <= right:
        current_sum = left * left + right * right
        if current_sum == c:
            return True
        elif current_sum < c:
            left += 1
        else:
            right -= 1

    return False
```

**Explanation:**
1. **Search Bound**: The largest possible value for either $a$ or $b$ is $\sqrt{c}$.
2. **Two Pointers**: We start with the smallest possible $a$ (0) and the largest possible $b$ ($\lfloor\sqrt{c}\rfloor$).
3. **Logic**:
   - If $a^2 + b^2$ is too small, we need a larger value, so we increment $a$.
   - If $a^2 + b^2$ is too large, we need a smaller value, so we decrement $b$.
   - If they meet or pass without finding a sum, no solution exists.

**Complexity Analysis:**
- **Time Complexity:** $O(\sqrt{c})$. In the worst case, we traverse from 0 to $\sqrt{c}$.
- **Space Complexity:** $O(1)$.

---

## 4. Perfect Squares

**Problem Statement:**
Given an integer `n`, return the least number of perfect square numbers that sum to `n`.

**Examples & Edge Cases:**
- **Example 1:** `n = 12` -> Output: `3` ($4 + 4 + 4$)
- **Example 2:** `n = 13` -> Output: `2` ($4 + 9$)
- **Edge Case:** `n = 1` -> Output: `1`

**Optimal Python Solution:**
```python
def numSquares(n: int) -> int:
    """
    Finds the minimum number of perfect squares that sum to n using DP.
    """
    # dp[i] stores the minimum perfect squares for sum i
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    # Pre-calculate possible squares
    max_square_index = int(n**0.5) + 1
    squares = [i*i for i in range(1, max_square_index)]

    for i in range(1, n + 1):
        for square in squares:
            if i < square:
                break
            dp[i] = min(dp[i], dp[i - square] + 1)

    return dp[n]
```

**Explanation:**
1. **Dynamic Programming**: We build up the solution for all numbers from 1 to $n$.
2. **State Transition**: To find `dp[i]`, we try subtracting every perfect square $j^2 \le i$ and check `dp[i - j^2] + 1`. The minimum of these is our answer.
3. **Optimization**: BFS is also a very efficient way to solve this, as it finds the "shortest path" to sum 0.

**Complexity Analysis:**
- **Time Complexity:** $O(n\sqrt{n})$. For each $i$ from 1 to $n$, we check up to $\sqrt{i}$ squares.
- **Space Complexity:** $O(n)$ to store the DP table.

---

## 5. Arranging Coins

**Problem Statement:**
You have `n` coins and you want to build a staircase where the $k$-th row has exactly $k$ coins. Given `n`, return the number of complete rows of the staircase you can build.

**Examples & Edge Cases:**
- **Example 1:** `n = 5` -> Output: `2` (Row 1: 1 coin, Row 2: 2 coins, total 3. Row 3 needs 3, but only 2 left.)
- **Example 2:** `n = 8` -> Output: `3`
- **Edge Case:** `n = 0`.

**Optimal Python Solution:**
```python
import math

def arrangeCoins(n: int) -> int:
    """
    Finds the number of full staircase rows using the quadratic formula.
    Total coins for k rows is: S = k(k+1)/2
    We solve for k: k^2 + k - 2n = 0
    """
    # Using quadratic formula: k = (-1 + sqrt(1 + 8n)) / 2
    return int((math.sqrt(1 + 8 * n) - 1) / 2)
```

**Explanation:**
1. **Mathematical Approach**: The number of coins in $k$ complete rows is the sum of an arithmetic progression: $1 + 2 + \dots + k = \frac{k(k+1)}{2}$.
2. **Solving the Inequality**: We want the largest $k$ such that $\frac{k(k+1)}{2} \le n$.
3. **Quadratic Formula**: Solving $k^2 + k - 2n = 0$ gives $k = \frac{-1 \pm \sqrt{1 - 4(1)(-2n)}}{2}$. Since $k > 0$, we take the positive root.

**Complexity Analysis:**
- **Time Complexity:** $O(1)$ if we assume `sqrt` is $O(1)$ (or constant time for fixed precision).
- **Space Complexity:** $O(1)$.

---

## 6. Kth Smallest in Multiplication Table

**Problem Statement:**
Nearly every culture teaches multiplication tables between 1 and $n$, and 1 and $m$. For an $m \times n$ multiplication table, return the $k$-th smallest number in the table.

**Examples & Edge Cases:**
- **Example 1:** `m = 3, n = 3, k = 5` -> Output: `3` (Table: 1, 2, 2, 3, 3, 4, 6, 6, 9. Sorted: 1, 2, 2, 3, **3**, 4, 6, 6, 9)
- **Edge Case:** $k=1$ -> Output: `1`.
- **Edge Case:** $k=m \times n$ -> Output: $m \times n$.

**Optimal Python Solution:**
```python
def findKthNumber(m: int, n: int, k: int) -> int:
    """
    Finds kth smallest value using Binary Search on the value range.
    """
    def count(x):
        """Count how many numbers in the table are <= x."""
        res = 0
        for i in range(1, m + 1):
            # In row i, multiples are i, 2i, 3i... up to ni.
            # Count of j*i <= x is floor(x/i), but at most n.
            res += min(x // i, n)
        return res

    # Value range of the multiplication table
    left, right = 1, m * n

    while left < right:
        mid = left + (right - left) // 2
        if count(mid) < k:
            left = mid + 1
        else:
            right = mid

    return left
```

**Explanation:**
1. **Binary Search on Values**: The answer is between 1 and $m \cdot n$. We binary search for the smallest value $x$ such that there are at least $k$ numbers in the table $\le x$.
2. **Counting Function**: For a given value $x$, we can count how many numbers in each row are $\le x$ in $O(1)$ per row. In row $i$, the numbers are $i, 2i, 3i, \dots, ni$. The number of these $\le x$ is $\min(\lfloor x/i \rfloor, n)$.
3. **Efficiency**: This turns a difficult sorting problem into a binary search over values, which is much faster for large $m$ and $n$.

**Complexity Analysis:**
- **Time Complexity:** $O(m \cdot \log(m \cdot n))$. We do $O(\log(m \cdot n))$ steps of binary search, each taking $O(m)$ time for counting.
- **Space Complexity:** $O(1)$.
