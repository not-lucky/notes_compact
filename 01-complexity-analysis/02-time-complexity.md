# Time Complexity Analysis

> **Prerequisites:** [01-big-o-notation.md](./01-big-o-notation.md)

## Building Intuition

**The "Work Counter" Mental Model**

Imagine you have a clicker counter in your hand. Every time your code does a "unit of work" (comparison, addition, assignment), you click. Time complexity answers: "How many clicks for n items?"

```
Linear scan:     Click once per item → n clicks → O(n)
Nested scan:     Click once per pair → n² clicks → O(n²)
Binary search:   Click once per halving → log n clicks → O(log n)
```

**The "Doubling Test"**

A quick mental check for complexity:
1. Imagine doubling your input size
2. Ask: "How much more work?"

| If work... | Then complexity is... |
|------------|----------------------|
| Stays same | O(1) |
| Adds constant | O(log n) |
| Doubles | O(n) |
| Slightly more than doubles | O(n log n) |
| Quadruples | O(n²) |

**Why This Matters**

Understanding time complexity lets you predict performance:
- O(n) with n=1,000,000 → ~1 second on modern hardware
- O(n²) with n=1,000,000 → ~12 days (!!)

---

## Interview Context

Interviewers expect you to analyze code on the spot. The skill isn't just knowing Big-O—it's breaking down any algorithm and determining its complexity systematically.

Common interview moments:
- "What's the time complexity of your solution?"
- "How does this change if the array is sorted?"
- "Your solution is O(n²). Can you optimize it?"

---

## Analyzing Loops

### Single Loops

The most straightforward case: count how many times the loop runs.

```python
def linear_scan(arr: list[int]) -> int:
    """
    Time: O(n) - loop runs n times
    """
    total = 0
    for num in arr:        # n iterations
        total += num       # O(1) per iteration
    return total           # Total: O(n) × O(1) = O(n)
```

### Non-Standard Loop Increments

```python
def skip_by_two(arr: list[int]) -> int:
    """
    Time: O(n) - loop runs n/2 times = O(n)
    Constants don't matter!
    """
    total = 0
    for i in range(0, len(arr), 2):  # n/2 iterations
        total += arr[i]
    return total

def log_loop(n: int) -> int:
    """
    Time: O(log n) - doubling the counter
    """
    count = 0
    i = 1
    while i < n:
        count += 1
        i *= 2             # 1, 2, 4, 8, ... until >= n
    return count           # Takes log₂(n) iterations
```

---

## Analyzing Nested Loops

### Standard Nested Loops

```python
def nested_example(n: int) -> int:
    """
    Time: O(n²)
    """
    count = 0
    for i in range(n):          # n iterations
        for j in range(n):      # n iterations each
            count += 1          # Total: n × n = n²
    return count
```

### Dependent Nested Loops

When the inner loop depends on the outer loop's variable:

```python
def triangular(n: int) -> int:
    """
    Time: O(n²)
    Inner loop runs: 0 + 1 + 2 + ... + (n-1) = n(n-1)/2 = O(n²)
    """
    count = 0
    for i in range(n):
        for j in range(i):      # j goes from 0 to i-1
            count += 1
    return count

def decreasing_inner(n: int) -> int:
    """
    Time: O(n²)
    Inner loop runs: n + (n-1) + ... + 1 = n(n+1)/2 = O(n²)
    """
    count = 0
    for i in range(n):
        for j in range(n - i):  # j goes from 0 to n-i-1
            count += 1
    return count
```

### Tricky Nested Loops

```python
def log_nested(n: int) -> int:
    """
    Time: O(n log n)
    Outer: n iterations
    Inner: log n iterations (doubling each time)
    """
    count = 0
    for i in range(n):          # n iterations
        j = 1
        while j < n:
            count += 1
            j *= 2              # log n iterations
    return count                # Total: n × log n

def two_pointer_pattern(arr: list[int]) -> int:
    """
    Time: O(n), NOT O(n²)!

    Even though there are two nested constructs,
    left and right together traverse n elements total.
    """
    left, right = 0, len(arr) - 1
    count = 0
    while left < right:
        if some_condition(arr[left], arr[right]):
            left += 1
        else:
            right -= 1
        count += 1
    return count  # At most n iterations total
```

---

## Analyzing Multiple Loops

### Sequential Loops (Add)

```python
def sequential(arr: list[int]) -> int:
    """
    Time: O(n) + O(n) = O(2n) = O(n)
    """
    total = 0

    # First pass: O(n)
    for num in arr:
        total += num

    # Second pass: O(n)
    for num in arr:
        total += num * 2

    return total
```

### Different Input Sizes

```python
def process_two_arrays(a: list[int], b: list[int]) -> int:
    """
    Time: O(a + b) where a = len(a), b = len(b)

    Don't call both 'n'!
    """
    total = 0
    for x in a:    # O(a)
        total += x
    for y in b:    # O(b)
        total += y
    return total

def nested_two_arrays(a: list[int], b: list[int]) -> int:
    """
    Time: O(a × b)
    """
    count = 0
    for x in a:        # O(a)
        for y in b:    # O(b) each time
            count += 1
    return count       # Total: O(a × b)
```

---

## Analyzing Recursion

### Linear Recursion

```python
def factorial(n: int) -> int:
    """
    Time: O(n) - one recursive call per level, n levels

    Call tree:
    factorial(5)
        factorial(4)
            factorial(3)
                factorial(2)
                    factorial(1)
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def sum_array(arr: list[int], i: int = 0) -> int:
    """
    Time: O(n) - one call per element
    """
    if i >= len(arr):
        return 0
    return arr[i] + sum_array(arr, i + 1)
```

### Binary Recursion (Exponential)

```python
def fibonacci_naive(n: int) -> int:
    """
    Time: O(2^n) - each call spawns two more

    Call tree for n=5:
              fib(5)
            /        \
        fib(4)      fib(3)
        /    \      /    \
    fib(3)  fib(2) fib(2) fib(1)
       ...

    Tree has 2^n nodes in worst case.
    """
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)
```

### Divide and Conquer (Logarithmic Recursion)

```python
def binary_search_recursive(arr: list[int], target: int,
                             left: int = 0, right: int = None) -> int:
    """
    Time: O(log n) - problem halves each level

    Call tree for n=16:
        search(16 elements)
            search(8 elements)
                search(4 elements)
                    search(2 elements)
                        search(1 element)

    Only log₂(n) = 4 levels.
    """
    if right is None:
        right = len(arr) - 1

    if left > right:
        return -1

    mid = (left + right) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)
```

### Divide and Conquer (Linear Work per Level)

```python
def merge_sort(arr: list[int]) -> list[int]:
    """
    Time: O(n log n)

    Recurrence: T(n) = 2T(n/2) + O(n)

    - log n levels (halving)
    - O(n) work at each level (merging)
    - Total: O(n log n)

    Visual:
    Level 0: [          n          ] → n work
    Level 1: [    n/2    ][   n/2   ] → n work
    Level 2: [n/4][n/4][n/4][n/4]     → n work
    ...
    log n levels × n work = O(n log n)
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])      # T(n/2)
    right = merge_sort(arr[mid:])     # T(n/2)

    return merge(left, right)         # O(n) to merge
```

---

## The Master Theorem (Simplified)

For recurrences of the form: T(n) = aT(n/b) + O(n^d)

| Condition | Complexity |
|-----------|------------|
| d > log_b(a) | O(n^d) |
| d = log_b(a) | O(n^d log n) |
| d < log_b(a) | O(n^(log_b(a))) |

### Common Examples

| Algorithm | Recurrence | Complexity |
|-----------|------------|------------|
| Binary search | T(n) = T(n/2) + O(1) | O(log n) |
| Merge sort | T(n) = 2T(n/2) + O(n) | O(n log n) |
| Linear scan | T(n) = T(n/2) + O(n) | O(n) |

---

## Amortized Analysis

Sometimes individual operations vary, but average over many operations is better.

### Dynamic Array Append

```python
class DynamicArray:
    """
    Append: O(1) amortized

    Most appends: O(1) - just add to end
    Occasional resize: O(n) - copy everything

    But resizing doubles capacity, so resize is rare.
    Over n appends: total work = n + n/2 + n/4 + ... ≈ 2n
    Average per append: 2n/n = O(1) amortized
    """
    def __init__(self):
        self.data = [None] * 4
        self.size = 0
        self.capacity = 4

    def append(self, val):
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = val
        self.size += 1

    def _resize(self):
        self.capacity *= 2
        new_data = [None] * self.capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
```

---

## Common Complexity Patterns

| Pattern | Complexity | Example |
|---------|------------|---------|
| Single loop | O(n) | Linear search |
| Two nested loops (same array) | O(n²) | Bubble sort |
| Loop with halving | O(log n) | Binary search |
| Divide & conquer + merge | O(n log n) | Merge sort |
| All subsets | O(2^n) | Subset generation |
| All permutations | O(n!) | Permutation generation |
| Two pointers (converging) | O(n) | Container with most water |

---

## Practice: Analyze These

```python
# Problem 1: What's the complexity?
def mystery1(n):
    i = 1
    while i < n:
        for j in range(n):
            pass
        i *= 2
```

<details>
<summary>Answer 1</summary>

O(n log n). Outer loop runs log n times (i doubles), inner loop runs n times each.
</details>

```python
# Problem 2: What's the complexity?
def mystery2(arr):
    n = len(arr)
    for i in range(n):
        for j in range(i, n):
            for k in range(j, n):
                pass
```

<details>
<summary>Answer 2</summary>

O(n³). Three nested loops. More precisely, it's n(n+1)(n+2)/6 ≈ n³/6, but constants drop.
</details>

```python
# Problem 3: What's the complexity?
def mystery3(arr):
    n = len(arr)
    result = []
    for i in range(n):
        result = result + [arr[i]]  # Note: not .append()
    return result
```

<details>
<summary>Answer 3</summary>

O(n²). The `+` creates a new list each time, copying all previous elements. Total: 1 + 2 + 3 + ... + n = O(n²).
</details>

---

## Practice Problems

| # | Problem | Difficulty | Focus |
|---|---------|------------|-------|
| 1 | Analyze a given code snippet | Easy | Loop analysis |
| 2 | Compare recursive vs iterative | Easy | Recursion basics |
| 3 | Identify amortized operations | Medium | Dynamic array |
| 4 | Solve recurrence relations | Medium | Master theorem |
| 5 | Two pointer complexity proof | Medium | Non-obvious O(n) |

---

## Key Takeaways

1. **Single loop over n elements** → O(n)
2. **Nested loops** → multiply their counts
3. **Loop variable doubles/halves** → O(log n)
4. **Recursion branching factor matters** → draw the tree
5. **Divide & conquer with linear merge** → typically O(n log n)
6. **Watch for hidden operations** → list concatenation, membership tests

---

## When NOT to Over-Analyze

1. **Don't count every operation**: Focus on the dominant term
2. **Don't analyze obvious O(1)**: Single variable assignments, comparisons
3. **Don't forget amortization**: Some expensive operations are rare (array resize)
4. **Don't assume worst case always matters**: Average case often more relevant
5. **Don't over-complicate**: If it looks like O(n), it probably is O(n)

**Practical tip**: For interviews, get the complexity class right (O(n) vs O(n²)). Don't waste time proving whether it's O(2n) or O(3n).

---

## Next: [03-space-complexity.md](./03-space-complexity.md)

Learn to analyze memory usage, including the often-forgotten call stack.
