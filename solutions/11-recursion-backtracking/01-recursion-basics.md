# Recursion Basics - Solutions

This document provides optimal solutions and detailed explanations for the practice problems in Recursion Basics.

---

## 1. Fibonacci Number

### Problem Statement
The Fibonacci numbers, commonly denoted `F(n)` form a sequence, called the Fibonacci sequence, such that each number is the sum of the two preceding ones, starting from 0 and 1.
Given `n`, calculate `F(n)`.

### Examples & Edge Cases
- **Input:** n = 2 → **Output:** 1 (F(2) = F(1) + F(0) = 1 + 0 = 1)
- **Input:** n = 4 → **Output:** 3 (F(4) = F(3) + F(2) = 2 + 1 = 3)
- **Edge Case:** n = 0 → Output: 0
- **Edge Case:** n = 1 → Output: 1

### Optimal Python Solution (Iterative/DP)
While the problem is classic for recursion, the recursive approach is $O(2^n)$. The optimal approach uses iteration or memoization.

```python
def fib(n: int) -> int:
    # Base cases
    if n <= 1:
        return n

    # Iterative approach (Space optimized)
    # F(n) = F(n-1) + F(n-2)
    prev2, prev1 = 0, 1

    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current

    return prev1
```

### Detailed Explanation
1. **Recursive Definition**: $F(n) = F(n-1) + F(n-2)$.
2. **Problem with Pure Recursion**: A naive recursive solution recalculates the same subproblems many times (e.g., `fib(2)` is calculated multiple times when finding `fib(4)`).
3. **Optimized Approach**: We use two variables `prev1` and `prev2` to keep track of the last two Fibonacci numbers. As we iterate from 2 up to `n`, we update these variables, effectively building the sequence from the bottom up.

### Complexity Analysis
- **Time Complexity:** $O(n)$ - We iterate from 2 to $n$ once.
- **Space Complexity:** $O(1)$ - We only use a constant amount of extra space for variables.

---

## 2. Power of Two

### Problem Statement
Given an integer `n`, return `true` if it is a power of two. Otherwise, return `false`.
An integer `n` is a power of two if there exists an integer `x` such that $n = 2^x$.

### Examples & Edge Cases
- **Input:** n = 1 → **Output:** true ($2^0$)
- **Input:** n = 16 → **Output:** true ($2^4$)
- **Input:** n = 3 → **Output:** false
- **Edge Case:** n <= 0 → Output: false

### Optimal Python Solution (Bit Manipulation)
```python
def isPowerOfTwo(n: int) -> bool:
    # A power of two in binary has exactly one bit set: 100...0
    # n-1 would be 011...1
    # n & (n-1) will be 0 if n is a power of two
    return n > 0 and (n & (n - 1)) == 0
```

### Detailed Explanation
1. **Binary Representation**: A power of two (like 8: `1000`) has exactly one bit set.
2. **The Trick**: Subtracting 1 from a power of two flips all bits from the rightmost set bit (e.g., $8-1=7$: `0111`).
3. **Bitwise AND**: Performing a bitwise AND between `n` and `n-1` will result in 0 if and only if `n` had exactly one bit set.
4. **Base Case**: We must ensure $n > 0$ because 0 and negative numbers are not powers of two.

### Complexity Analysis
- **Time Complexity:** $O(1)$ - Constant time bitwise operation.
- **Space Complexity:** $O(1)$ - No extra space used.

---

## 3. Reverse String

### Problem Statement
Write a function that reverses a string. The input string is given as an array of characters `s`.
You must do this by modifying the input array in-place with $O(1)$ extra memory.

### Examples & Edge Cases
- **Input:** s = ["h","e","l","l","o"] → **Output:** ["o","l","l","e","h"]
- **Edge Case:** Empty array or single character.

### Optimal Python Solution (Two Pointers)
```python
def reverseString(s: list[str]) -> None:
    # Use two pointers moving towards the center
    left, right = 0, len(s) - 1

    while left < right:
        # Swap characters
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
```

### Detailed Explanation
1. **Two Pointers**: Place one pointer at the start and one at the end of the list.
2. **Swap**: Exchange the elements at the pointers.
3. **Move Pointers**: Increment the left pointer and decrement the right pointer.
4. **Termination**: Stop when the pointers meet or cross in the middle.

### Complexity Analysis
- **Time Complexity:** $O(n)$ - We visit each element once (performing $n/2$ swaps).
- **Space Complexity:** $O(1)$ - In-place modification with constant extra space.

---

## 4. Merge Two Sorted Lists

### Problem Statement
You are given the heads of two sorted linked lists `list1` and `list2`.
Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.
Return the head of the merged linked list.

### Examples & Edge Cases
- **Input:** l1 = [1,2,4], l2 = [1,3,4] → **Output:** [1,1,2,3,4,4]
- **Edge Case:** One or both lists are empty.

### Optimal Python Solution (Iterative)
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeTwoLists(list1: ListNode, list2: ListNode) -> ListNode:
    # Create a dummy node to simplify the head of the result
    dummy = ListNode(-1)
    current = dummy

    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next

    # Attach the remaining part of the non-empty list
    current.next = list1 if list1 else list2

    return dummy.next
```

### Detailed Explanation
1. **Dummy Node**: Using a dummy node avoids special handling for the head of the merged list.
2. **Comparison**: While both lists have nodes, compare the values and attach the smaller one to the result list.
3. **Advance**: Move the pointer of the list we took a node from and the `current` pointer of our result list.
4. **Cleanup**: After the loop, one list might still have nodes. Since they are already sorted, we just attach them to the end of our merged list.

### Complexity Analysis
- **Time Complexity:** $O(n + m)$ - Where $n$ and $m$ are lengths of the two lists.
- **Space Complexity:** $O(1)$ - We only use a constant amount of extra space (reusing existing nodes).

---

## 5. Maximum Depth of Binary Tree

### Problem Statement
Given the `root` of a binary tree, return its maximum depth.
A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

### Examples & Edge Cases
- **Input:** root = [3,9,20,null,null,15,7] → **Output:** 3
- **Edge Case:** Root is `None` (depth 0).

### Optimal Python Solution (Recursive DFS)
```python
def maxDepth(root: TreeNode) -> int:
    # Base case: empty tree has depth 0
    if not root:
        return 0

    # Recursive step: 1 (current level) + max depth of subtrees
    left_depth = maxDepth(root.left)
    right_depth = maxDepth(root.right)

    return 1 + max(left_depth, right_depth)
```

### Detailed Explanation
1. **Decomposition**: The depth of a tree is $1 + \max(\text{depth of left child}, \text{depth of right child})$.
2. **Base Case**: If the current node is `None`, it contributes 0 to the depth.
3. **Recursion**: We recursively call the function for both children and return the maximum of their results plus 1 for the current node.

### Complexity Analysis
- **Time Complexity:** $O(n)$ - We visit every node in the tree exactly once.
- **Space Complexity:** $O(h)$ - Where $h$ is the height of the tree, representing the recursion stack depth. In the worst case (skewed tree), $O(n)$.

---

## 6. Climbing Stairs

### Problem Statement
You are climbing a staircase. It takes `n` steps to reach the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

### Examples & Edge Cases
- **Input:** n = 2 → **Output:** 2 (1+1, 2)
- **Input:** n = 3 → **Output:** 3 (1+1+1, 1+2, 2+1)
- **Edge Case:** n = 1 → Output: 1

### Optimal Python Solution (DP)
This is exactly the Fibonacci sequence problem disguised.

```python
def climbStairs(n: int) -> int:
    if n <= 2:
        return n

    # To reach step n, you can come from step n-1 or n-2
    # Ways(n) = Ways(n-1) + Ways(n-2)
    prev2, prev1 = 1, 2 # Ways for step 1 and step 2

    for _ in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current

    return prev1
```

### Detailed Explanation
1. **Recurrence Relation**: To reach the $n$-th step, you could have come from the $(n-1)$-th step (by taking 1 step) or the $(n-2)$-th step (by taking 2 steps).
2. **Formula**: Total ways $W(n) = W(n-1) + W(n-2)$.
3. **Implementation**: Similar to Fibonacci, we only need the last two values, allowing for $O(1)$ space optimization.

### Complexity Analysis
- **Time Complexity:** $O(n)$ - Linear scan up to $n$.
- **Space Complexity:** $O(1)$ - Constant space for variables.

---

## 7. Pow(x, n)

### Problem Statement
Implement `pow(x, n)`, which calculates $x$ raised to the power $n$ ($x^n$).

### Examples & Edge Cases
- **Input:** x = 2.0, n = 10 → **Output:** 1024.0
- **Input:** x = 2.1, n = 3 → **Output:** 9.261
- **Edge Case:** $n=0 \rightarrow 1$
- **Edge Case:** $n < 0 \rightarrow 1 / x^{-n}$

### Optimal Python Solution (Binary Exponentiation)
```python
def myPow(x: float, n: int) -> float:
    # Base case: x^0 is 1
    if n == 0:
        return 1.0

    # Handle negative exponent
    if n < 0:
        x = 1 / x
        n = -n

    # Recursive Binary Exponentiation
    def fastPow(base, exp):
        if exp == 0:
            return 1.0

        half = fastPow(base, exp // 2)

        if exp % 2 == 0:
            return half * half
        else:
            return base * half * half

    return fastPow(x, n)
```

### Detailed Explanation
1. **Binary Exponentiation (Divide and Conquer)**: Instead of multiplying $x$ by itself $n$ times ($O(n)$), we use the property $x^n = (x^{n/2})^2$ for even $n$, and $x^n = x \cdot (x^{n/2})^2$ for odd $n$.
2. **Efficiency**: Each step halves the exponent, leading to logarithmic time complexity.
3. **Negative $n$**: If $n$ is negative, $x^n = (1/x)^{-n}$.

### Complexity Analysis
- **Time Complexity:** $O(\log n)$ - The exponent is halved in each recursive call.
- **Space Complexity:** $O(\log n)$ - Recursion stack depth.
