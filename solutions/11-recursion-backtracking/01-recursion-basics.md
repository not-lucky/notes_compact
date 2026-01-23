# Solution: Recursion Basics Practice Problems

## Problem 1: Fibonacci Number
### Problem Statement
The Fibonacci numbers, commonly denoted `F(n)` form a sequence, called the Fibonacci sequence, such that each number is the sum of the two preceding ones, starting from 0 and 1. That is,
`F(0) = 0, F(1) = 1`
`F(n) = F(n - 1) + F(n - 2), for n > 1.`

Given `n`, calculate `F(n)`.

### Constraints
- `0 <= n <= 30`

### Example
Input: `n = 2`
Output: `1`
Explanation: `F(2) = F(1) + F(0) = 1 + 0 = 1.`

### Python Implementation
```python
def fib(n: int) -> int:
    """
    Time Complexity: O(2^n) - without memoization
    Space Complexity: O(n) - recursion stack depth
    """
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Memoized version for better performance
def fib_memo(n: int, memo=None) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

---

## Problem 2: Power of Two
### Problem Statement
Given an integer `n`, return `true` if it is a power of two. Otherwise, return `false`.

An integer `n` is a power of two, if there exists an integer `x` such that `n == 2^x`.

### Constraints
- `-2^31 <= n <= 2^31 - 1`

### Example
Input: `n = 1`
Output: `true`
Explanation: `2^0 = 1`

### Python Implementation
```python
def isPowerOfTwo(n: int) -> bool:
    """
    Recursive approach.
    Time Complexity: O(log n)
    Space Complexity: O(log n)
    """
    if n <= 0:
        return False
    if n == 1:
        return True
    if n % 2 != 0:
        return False
    return isPowerOfTwo(n // 2)
```

---

## Problem 3: Reverse String
### Problem Statement
Write a function that reverses a string. The input string is given as an array of characters `s`.

You must do this by modifying the input array in-place with O(1) extra memory.

### Constraints
- `1 <= s.length <= 10^5`
- `s[i]` is a printable ascii character.

### Example
Input: `s = ["h","e","l","l","o"]`
Output: `["o","l","l","e","h"]`

### Python Implementation
```python
def reverseString(s: list[str]) -> None:
    """
    Recursive approach.
    Time Complexity: O(n)
    Space Complexity: O(n) - recursion stack
    """
    def helper(left, right):
        if left >= right:
            return
        s[left], s[right] = s[right], s[left]
        helper(left + 1, right - 1)

    helper(0, len(s) - 1)
```

---

## Problem 4: Merge Two Sorted Lists
### Problem Statement
You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists in a one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

### Constraints
- The number of nodes in both lists is in the range `[0, 50]`.
- `-100 <= Node.val <= 100`
- Both `list1` and `list2` are sorted in non-decreasing order.

### Example
Input: `list1 = [1,2,4], list2 = [1,3,4]`
Output: `[1,1,2,3,4,4]`

### Python Implementation
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

def mergeTwoLists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Recursive approach.
    Time Complexity: O(n + m)
    Space Complexity: O(n + m) - recursion stack
    """
    if not list1:
        return list2
    if not list2:
        return list1

    if list1.val < list2.val:
        list1.next = mergeTwoLists(list1.next, list2)
        return list1
    else:
        list2.next = mergeTwoLists(list1, list2.next)
        return list2
```

---

## Problem 5: Maximum Depth of Binary Tree
### Problem Statement
Given the `root` of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

### Constraints
- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [3,9,20,null,null,15,7]`
Output: `3`

### Python Implementation
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

def maxDepth(root: Optional[TreeNode]) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(h) - height of tree
    """
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

---

## Problem 6: Climbing Stairs
### Problem Statement
You are climbing a staircase. It takes `n` steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

### Constraints
- `1 <= n <= 45`

### Example
Input: `n = 2`
Output: `2`
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

### Python Implementation
```python
def climbStairs(n: int) -> int:
    """
    Memoized recursion (same as Fibonacci).
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    memo = {1: 1, 2: 2}
    def helper(n):
        if n in memo:
            return memo[n]
        memo[n] = helper(n - 1) + helper(n - 2)
        return memo[n]
    return helper(n)
```

---

## Problem 7: Pow(x, n)
### Problem Statement
Implement `pow(x, n)`, which calculates `x` raised to the power `n` (i.e., `x^n`).

### Constraints
- `-100.0 < x < 100.0`
- `-2^31 <= n <= 2^31-1`
- `n` is an integer.
- Either `x` is not zero or `n > 0`.
- `-10^4 <= x^n <= 10^4`

### Example
Input: `x = 2.00000, n = 10`
Output: `1024.00000`

### Python Implementation
```python
def myPow(x: float, n: int) -> float:
    """
    Binary Exponentiation (Recursive).
    Time Complexity: O(log n)
    Space Complexity: O(log n)
    """
    if n == 0:
        return 1
    if n < 0:
        return 1 / myPow(x, -n)

    if n % 2 == 0:
        half = myPow(x, n // 2)
        return half * half
    else:
        return x * myPow(x, n - 1)
```
