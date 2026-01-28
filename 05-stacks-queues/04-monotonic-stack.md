# Monotonic Stack

> **Prerequisites:** [01-stack-basics](./01-stack-basics.md)

## Overview

A monotonic stack is a stack that maintains elements in sorted order (all increasing or all decreasing) from bottom to top. When pushing a new element, we pop all elements that violate the monotonic property. This simple modification transforms a basic stack into a powerful tool for solving "next greater/smaller element" problems in O(n) time.

## Building Intuition

**Why does maintaining sorted order help?**

The key insight is what information we gain from popping:

1. **When we pop an element**: We've found its "answer"—the first element that breaks its dominance. If we're maintaining a decreasing stack and pop element X because element Y is larger, then Y is X's "next greater element."

2. **Why we can pop confidently**: Once X is dominated by Y, X can never be the answer for any future element. If Z comes after Y and is looking for its next greater, Z will either be stopped by Y (if Y > Z) or go past Y. Either way, X is irrelevant.

**The Core Insight**:

```
In a monotonic stack, popping an element means we've found its answer.
The new element that caused the pop is the answer.
```

**Worked Example - Next Greater Element**:

```
Array: [2, 1, 5, 6, 2, 3]

i=0: push 2       stack: [2]        (start building)
i=1: push 1       stack: [2,1]      (1 < 2, still decreasing)
i=2: 5 > 1, pop   stack: [2]        → 1's answer is 5
     5 > 2, pop   stack: []         → 2's answer is 5
     push 5       stack: [5]
i=3: 6 > 5, pop   stack: []         → 5's answer is 6
     push 6       stack: [6]
i=4: push 2       stack: [6,2]      (2 < 6, still decreasing)
i=5: 3 > 2, pop   stack: [6]        → 2's answer is 3
     push 3       stack: [6,3]

Elements left (6, 3) have no next greater.
```

**Why O(n)?**: Each element is pushed exactly once and popped at most once. Even though we have nested loops, the total number of operations is bounded by 2n.

**Mental Model**: Think of people standing in a line by height (decreasing from left). When a tall person joins at the right, all shorter people in front of them "see" the tall person as their "next taller person to the right" and can leave the line. Only people taller than the new person stay.

## When NOT to Use Monotonic Stacks

Monotonic stacks are the wrong choice when:

1. **No "Next/Previous Boundary" Question**: If you're not looking for the first element that breaks a property (greater, smaller, etc.), you probably don't need this pattern.

2. **Need All Pairs, Not Just Next**: If you need to find all greater elements (not just the first one), you need a different approach like sorting or binary search.

3. **Non-Comparable Elements**: If elements can't be ordered (like strings without a custom comparison), monotonic stacks don't apply.

4. **Dynamic Data**: Monotonic stacks work best for single-pass problems. If elements are inserted/deleted dynamically, consider balanced BSTs or segment trees.

5. **2D Problems Without Reduction**: Monotonic stacks solve 1D problems. For 2D grids, you often need to reduce rows/columns to 1D first (like in maximal rectangle).

**Signs You Need a Different Approach**:

- "Find all elements greater than X" → Sorting or binary search
- "Count pairs with property" → Often two pointers or hashing
- "Queries on ranges with updates" → Segment tree or Fenwick tree

## Interview Context

Monotonic stacks are a **high-value interview pattern** at FANG+ companies because:

1. **Elegant O(n) solutions**: Solve "next greater/smaller" problems efficiently
2. **Common but tricky**: Tests algorithmic thinking beyond basic data structures
3. **Many variations**: Daily temperatures, stock spans, histogram problems
4. **Not obvious**: Candidates who know this pattern stand out

Interviewers use monotonic stacks to assess your ability to recognize non-obvious patterns and maintain invariants.

---

## Core Concept: What is a Monotonic Stack?

A monotonic stack maintains elements in sorted order (all increasing or all decreasing) from bottom to top. When we push a new element, we pop all elements that violate the monotonic property.

```
Monotonic Decreasing Stack (most common for "next greater"):

Array: [2, 1, 5, 6, 2, 3]

Step by step:
i=0: push 2      stack: [2]
i=1: push 1      stack: [2, 1]     (1 < 2, maintains decreasing)
i=2: 5 > 1, pop  stack: [2]        (1's next greater = 5)
     5 > 2, pop  stack: []         (2's next greater = 5)
     push 5      stack: [5]
i=3: 6 > 5, pop  stack: []         (5's next greater = 6)
     push 6      stack: [6]
i=4: push 2      stack: [6, 2]     (2 < 6, maintains decreasing)
i=5: 3 > 2, pop  stack: [6]        (2's next greater = 3)
     push 3      stack: [6, 3]

Elements left in stack (6, 3) have no next greater element.
```

---

## Two Types of Monotonic Stacks

| Type                 | Property        | Use Case                      |
| -------------------- | --------------- | ----------------------------- |
| Monotonic Decreasing | Top is smallest | Find **next greater** element |
| Monotonic Increasing | Top is largest  | Find **next smaller** element |

### Visual Comparison

```
Monotonic Decreasing (bottom to top: large → small)
┌───┐
│ 1 │ ← top (smallest)
├───┤
│ 3 │
├───┤
│ 7 │ ← bottom (largest)
└───┘

Monotonic Increasing (bottom to top: small → large)
┌───┐
│ 7 │ ← top (largest)
├───┤
│ 3 │
├───┤
│ 1 │ ← bottom (smallest)
└───┘
```

---

## Pattern 1: Next Greater Element

Find the next greater element for each position in the array.

```python
def next_greater_element(nums: list[int]) -> list[int]:
    """
    Find next greater element for each position.

    Time: O(n) - each element pushed and popped at most once
    Space: O(n) - for stack and result

    Example:
    nums = [2, 1, 2, 4, 3]
    result = [4, 2, 4, -1, -1]
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # Stack of indices, values are monotonic decreasing

    for i in range(n):
        # Pop all elements smaller than current
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)

    return result


# Example walkthrough
# nums = [2, 1, 2, 4, 3]
# i=0: stack=[0]
# i=1: stack=[0,1]         (nums[1]=1 < nums[0]=2)
# i=2: pop 1, result[1]=2  (nums[2]=2 > nums[1]=1)
#      stack=[0,2]
# i=3: pop 2, result[2]=4  (nums[3]=4 > nums[2]=2)
#      pop 0, result[0]=4  (nums[3]=4 > nums[0]=2)
#      stack=[3]
# i=4: stack=[3,4]         (nums[4]=3 < nums[3]=4)
# Result: [4, 2, 4, -1, -1]
```

---

## Pattern 2: Next Greater Element II (Circular Array)

```python
def next_greater_circular(nums: list[int]) -> list[int]:
    """
    Next greater element in circular array.

    LeetCode 503: Next Greater Element II

    Time: O(n)
    Space: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []

    # Iterate twice to handle circular nature
    for i in range(2 * n):
        idx = i % n
        while stack and nums[stack[-1]] < nums[idx]:
            result[stack.pop()] = nums[idx]

        # Only push in first pass
        if i < n:
            stack.append(i)

    return result


# Example
print(next_greater_circular([1, 2, 1]))  # [2, -1, 2]
```

---

## Pattern 3: Daily Temperatures

```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    """
    Find days until warmer temperature.

    LeetCode 739: Daily Temperatures

    Time: O(n)
    Space: O(n)
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # Stack of indices

    for i in range(n):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            prev_idx = stack.pop()
            result[prev_idx] = i - prev_idx  # Days difference
        stack.append(i)

    return result


# Example
temps = [73, 74, 75, 71, 69, 72, 76, 73]
print(daily_temperatures(temps))
# [1, 1, 4, 2, 1, 1, 0, 0]
```

---

## Pattern 4: Stock Span Problem

```python
def stock_span(prices: list[int]) -> list[int]:
    """
    Find span (consecutive days with price <= today's price).

    LeetCode 901: Online Stock Span

    Time: O(n)
    Space: O(n)
    """
    n = len(prices)
    result = []
    stack = []  # Stack of (index, price)

    for i in range(n):
        # Pop all prices <= current
        while stack and stack[-1][1] <= prices[i]:
            stack.pop()

        # Span = distance to previous greater element
        if stack:
            result.append(i - stack[-1][0])
        else:
            result.append(i + 1)  # No previous greater, span is entire left

        stack.append((i, prices[i]))

    return result


# Example
prices = [100, 80, 60, 70, 60, 75, 85]
print(stock_span(prices))
# [1, 1, 1, 2, 1, 4, 6]
```

### Online Version (Class-based)

```python
class StockSpanner:
    """
    Online stock span calculator.

    Each price() call is O(1) amortized.
    """
    def __init__(self):
        self.stack = []  # (price, span)

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span
```

---

## Pattern 5: Previous Smaller Element

```python
def previous_smaller_element(nums: list[int]) -> list[int]:
    """
    Find previous smaller element for each position.

    Uses monotonic INCREASING stack.

    Time: O(n)
    Space: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # Stack of indices, values are monotonic increasing

    for i in range(n):
        # Pop all elements >= current
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()

        if stack:
            result[i] = nums[stack[-1]]

        stack.append(i)

    return result


# Example
nums = [4, 5, 2, 10, 8]
print(previous_smaller_element(nums))
# [-1, 4, -1, 2, 2]
```

---

## Pattern 6: Sum of Subarray Minimums

```python
def sum_of_subarray_mins(arr: list[int]) -> int:
    """
    Sum of minimums of all subarrays.

    LeetCode 907: Sum of Subarray Minimums

    For each element, count subarrays where it's the minimum.
    Contribution = arr[i] * left_count * right_count

    Time: O(n)
    Space: O(n)
    """
    MOD = 10**9 + 7
    n = len(arr)

    # left[i] = distance to previous smaller element
    # right[i] = distance to next smaller or equal element
    left = [0] * n
    right = [0] * n
    stack = []

    # Find previous smaller
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)

    stack = []

    # Find next smaller (or equal to handle duplicates)
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)

    # Calculate sum
    result = 0
    for i in range(n):
        result = (result + arr[i] * left[i] * right[i]) % MOD

    return result


# Example
print(sum_of_subarray_mins([3, 1, 2, 4]))  # 17
# Subarrays: [3], [1], [2], [4], [3,1], [1,2], [2,4], [3,1,2], [1,2,4], [3,1,2,4]
# Mins:       3    1    2    4     1     1     2       1        1        1
# Sum: 3+1+2+4+1+1+2+1+1+1 = 17
```

---

## Choosing the Right Direction

### Monotonic Decreasing Stack

- **When**: Finding next/previous **greater** element
- **Property**: Stack values decrease from bottom to top
- **Pop condition**: `while stack and nums[stack[-1]] < nums[i]`

### Monotonic Increasing Stack

- **When**: Finding next/previous **smaller** element
- **Property**: Stack values increase from bottom to top
- **Pop condition**: `while stack and nums[stack[-1]] > nums[i]`

```
Problem                          | Stack Type          | Direction
---------------------------------|---------------------|----------
Next Greater Element             | Decreasing          | Left to Right
Previous Greater Element         | Decreasing          | Left to Right
Next Smaller Element             | Increasing          | Left to Right
Previous Smaller Element         | Increasing          | Left to Right
Daily Temperatures               | Decreasing          | Left to Right
Stock Span                       | Decreasing          | Left to Right
Largest Rectangle in Histogram   | Increasing          | Left to Right
```

---

## Template: Monotonic Stack

```python
def monotonic_stack_template(nums: list[int]) -> list[int]:
    """
    Generic monotonic stack template.

    Modify the comparison for different problems.
    """
    n = len(nums)
    result = [default_value] * n
    stack = []  # Stack of indices

    for i in range(n):
        # Adjust comparison based on problem:
        # < for next greater, > for next smaller
        # <= or >= to handle duplicates
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            result[idx] = some_computation(i, idx, nums)
        stack.append(i)

    return result
```

---

## Complexity Analysis

| Operation               | Time | Space |
| ----------------------- | ---- | ----- |
| Build monotonic stack   | O(n) | O(n)  |
| Per element (amortized) | O(1) | -     |

**Why O(n)?** Each element is pushed exactly once and popped at most once. Total operations = 2n = O(n).

---

## Common Mistakes

1. **Wrong direction**: Using decreasing when increasing is needed
2. **Duplicate handling**: `<` vs `<=` matters for equal elements
3. **Off-by-one**: Returning value vs index vs distance
4. **Empty stack check**: Always check before accessing `stack[-1]`
5. **Circular arrays**: Forgetting to iterate twice or use modulo

---

## Practice Problems

| #   | Problem                        | Difficulty | Key Concept            |
| --- | ------------------------------ | ---------- | ---------------------- |
| 1   | Next Greater Element I         | Easy       | Basic pattern          |
| 2   | Next Greater Element II        | Medium     | Circular array         |
| 3   | Daily Temperatures             | Medium     | Days until warmer      |
| 4   | Online Stock Span              | Medium     | Previous greater count |
| 5   | Sum of Subarray Minimums       | Medium     | Contribution counting  |
| 6   | Largest Rectangle in Histogram | Hard       | Height boundaries      |
| 7   | Maximal Rectangle              | Hard       | Histogram per row      |
| 8   | Remove K Digits                | Medium     | Build smallest number  |
| 9   | 132 Pattern                    | Medium     | Track min and pattern  |

---

## Key Takeaways

1. **O(n) magic**: Each element is pushed/popped at most once
2. **Decreasing for greater**: Monotonic decreasing finds next greater
3. **Increasing for smaller**: Monotonic increasing finds next smaller
4. **Store indices**: Usually more useful than values (can compute distances)
5. **Handle duplicates carefully**: `<` vs `<=` changes behavior
6. **Circular arrays**: Iterate 2n times with modulo

---

## Next: [05-monotonic-queue.md](./05-monotonic-queue.md)

Learn the sliding window maximum pattern using monotonic deque.
