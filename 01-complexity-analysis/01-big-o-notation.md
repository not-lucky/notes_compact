# Big-O Notation Fundamentals

> **Prerequisites:** None - this is where it all begins

## Building Intuition

**The "Scaling Story" Mental Model**

Imagine you're comparing two pizza delivery services:

- **Service A**: Takes 5 minutes per pizza, regardless of order size
- **Service B**: Takes 1 minute setup + 2 minutes per pizza

For 1 pizza: A = 5 min, B = 3 min → B wins
For 10 pizzas: A = 50 min, B = 21 min → B wins
For 100 pizzas: A = 500 min, B = 201 min → B still wins, but the gap is proportionally smaller

At scale, both services are "linear in the number of pizzas"—the constants (5 vs 2) don't change the fundamental scaling behavior. If you double the order, the time roughly doubles for both.

**Why We Drop Constants**

```text
O(2n) vs O(n)
  ↓      ↓
Both double when n doubles → Same growth pattern → Both O(n)

O(n²) vs O(n)
  ↓       ↓
Quadruples   Doubles → Different patterns → Different classes
```

**The Key Insight**

Big-O answers: "If I double my input size, how much more work do I do?"

- **O(1)**: Exactly the same work
- **O(log n)**: A tiny bit more work (one extra step)
- **O(n)**: Double the work
- **O(n²)**: Quadruple the work
- **O(2ⁿ)**: Work squares or explodes exponentially

---

## Interview Context

Big-O notation is the language of algorithm efficiency. In every FANG+ interview, you'll use it to:

- Describe your solution's time and space efficiency before coding
- Compare different approaches and trade-offs
- Respond to "Can you do better?" prompts

Interviewers don't expect formal mathematical proofs. They want you to quickly, correctly, and confidently identify complexity classes and understand the *tightest upper bound* (technically Big-Theta $\Theta$, but colloquially called Big-O in interviews).

---

## What is Big-O?

Big-O describes the **upper bound** of an algorithm's growth rate as input size ($n$) increases. It answers: "In the worst-case scenario, how does the runtime or memory usage grow as $n$ approaches infinity?"

### The "Worst Case" Caveat

While Big-O formally describes the worst-case upper bound, interviewers often ask for the **average case** or **amortized worst case** depending on the data structure:

- Hash Table insertion is $O(1)$ on *average* (amortized), but $O(n)$ in the *worst case* (hash collisions).
- Quicksort is $O(n \log n)$ on *average*, but $O(n^2)$ in the *worst case*.

**Tip:** Always clarify which case you are describing if there is a difference. "This hash map lookup is $O(1)$ on average, though $O(n)$ worst-case if there are massive collisions."

### Dropping the Noise

Big-O ignores constants and lower-order terms because they become irrelevant at immense scales:

```text
O(2n + 5) → O(n)
O(n² + n) → O(n²)
O(100) → O(1)
```

We care about the **dominant term**—the part of the equation that grows the fastest.

---

## Time Complexity vs. Space Complexity

Interviews evaluate two dimensions of efficiency:

1.  **Time Complexity**: How many operations does the algorithm perform relative to the input size?
2.  **Space (Memory) Complexity**: How much *extra* or *auxiliary* memory does the algorithm use relative to the input size?

**Crucial Space Complexity Rules:**
- Do not count the space taken by the input itself (unless explicitly asked).
- Do not count the space taken by the output (the array you return), *unless* the output size is the core metric of the algorithm (e.g., generating all subsets).
- **Always count the Call Stack!** Recursive algorithms use $O(\text{max recursion depth})$ auxiliary space.

---

## Common Complexity Classes

### O(1) - Constant Time/Space

The cost doesn't change as the input size changes.

```python
def get_first(arr: list[int]) -> int | None:
    """
    Time: O(1) - single operation regardless of array size
    Space: O(1) - no extra memory allocated
    """
    return arr[0] if arr else None

def hash_lookup(d: dict[str, int], key: str) -> int | None:
    """
    Time: O(1) average, O(n) worst case (hash collisions)
    Space: O(1)
    """
    return d.get(key)
```

**Examples**: Array indexing, hash table access, stack push/pop, math formulas.

---

### O(log n) - Logarithmic Time

Runtime grows logarithmically—doubling the input only adds a *constant* amount of work (usually 1 extra step).

```python
def binary_search(arr: list[int], target: int) -> int:
    """
    Time: O(log n) - halving search space each iteration
    Space: O(1) - iterative approach uses constant pointers
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

**Why log n?** Each step eliminates half the remaining elements. For $n=1,000,000$ elements, binary search takes at most ~20 steps ($\log_2 1,000,000 \approx 20$). If you double it to 2,000,000, it takes ~21 steps.

**Examples**: Binary search, balanced BST operations, finding digits in a number.

---

### O(n) - Linear Time

Cost grows linearly and proportionally with the input size.

```python
def find_max(arr: list[int]) -> int | None:
    """
    Time: O(n) - must check every single element once
    Space: O(1) - only storing a single `max_val` integer
    """
    if not arr:
        return None

    max_val = arr[0]
    for num in arr:
        max_val = max(max_val, num)
    return max_val
```

**Examples**: Linear search, traversing an array or linked list, counting elements, two-pointer traversals.

---

### O(n log n) - Linearithmic Time

Common in efficient sorting algorithms. It's essentially doing $O(n)$ work $\log n$ times.

```python
def merge_sort(arr: list[int]) -> list[int]:
    """
    Time: O(n log n)
    - log n levels of recursion (halving each time)
    - n work at each level (merging the sub-arrays)

    Space: O(n)
    - O(n) extra space to hold the merged arrays
    - O(log n) call stack space
    - Total: O(n + log n) -> O(n)
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)  # Assume merge takes O(len(left) + len(right)) time
```

**Examples**: Merge sort, heap sort, quicksort (average case), many divide-and-conquer algorithms.

---

### O(n²) - Quadratic Time

Runtime grows with the square of input size. Usually indicates nested loops iterating over the same data.

```python
def has_duplicate_naive(arr: list[int]) -> bool:
    """
    Time: O(n²) - comparing roughly n*(n-1)/2 pairs
    Space: O(1) - no extra memory
    """
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] == arr[j]:
                return True
    return False
```

**Examples**: Nested loops over same input, bubble/insertion/selection sort, brute force pair checking.

---

### O(2ⁿ) - Exponential Time

Runtime doubles with each additional input element. Usually seen in recursion where each call spawns two more calls.

```python
def fibonacci_naive(n: int) -> int:
    """
    Time: O(2ⁿ) - each call spawns two more calls (actually closer to O(1.618ⁿ))
    Space: O(n) - maximum depth of the recursion tree is n
    """
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)
```

**Examples**: Recursive Fibonacci (without memoization), brute-force subset sum.

---

### O(n!) - Factorial Time

The worst common complexity. Grows astronomically fast. You are generating every possible arrangement.

```python
def all_permutations(nums: list[int]) -> list[list[int]]:
    """
    Time: O(n * n!) - n! permutations, each takes O(n) to copy to the result
    Space: O(n * n!) - storing all permutations
    """
    if len(nums) <= 1:
        return [nums[:]]

    result = []
    for i in range(len(nums)):
        rest = nums[:i] + nums[i+1:]
        for perm in all_permutations(rest):
            result.append([nums[i]] + perm)
    return result
```

**Examples**: Generating all permutations, brute force Traveling Salesperson Problem (TSP).

---

## Complexity Comparison Chart

For $n = 1,000$:

| Complexity | Operations | Practical?   |
| ---------- | ---------- | ------------ |
| O(1)       | 1          | ✓ Instant    |
| O(log n)   | ~10        | ✓ Instant    |
| O(n)       | 1,000      | ✓ Fast       |
| O(n log n) | ~10,000    | ✓ Fast       |
| O(n²)      | 1,000,000  | ✓ Acceptable |
| O(2ⁿ)      | $10^{301}$ | ✗ Impossible |
| O(n!)      | $10^{2567}$| ✗ Impossible |

For $n = 1,000,000$:

| Complexity | Operations | Practical?   |
| ---------- | ---------- | ------------ |
| O(1)       | 1          | ✓ Instant    |
| O(log n)   | ~20        | ✓ Instant    |
| O(n)       | $10^6$     | ✓ Fast       |
| O(n log n) | $2 \times 10^7$ | ✓ Acceptable |
| O(n²)      | $10^{12}$  | ⚠ Very slow  |
| O(2ⁿ)      | $\infty$   | ✗ Impossible |

---

## Rules for Determining Big-O

### Rule 1: Drop Constants

```python
# Both are O(n) Time
for i in range(n):       # O(n)
    pass

for i in range(2 * n):   # O(2n) → O(n)
    pass
```

### Rule 2: Drop Lower-Order Terms

```python
# This is O(n²), not O(n² + n)
for i in range(n):           # O(n)
    for j in range(n):       # × O(n) = O(n²)
        pass

for i in range(n):           # + O(n)
    pass
# Total: O(n² + n) → O(n²)
```

### Rule 3: Different Inputs, Different Variables

If an algorithm takes two distinct arrays, use two variables (e.g., $N$ and $M$).

```python
def process(arr1: list[int], arr2: list[int]) -> None:
    """
    Time: O(N + M) where N = len(arr1), M = len(arr2)
    Do NOT say O(N) unless you know len(arr1) == len(arr2).
    """
    for x in arr1:    # O(N)
        pass
    for y in arr2:    # O(M)
        pass
```

### Rule 4: Add Sequential Steps, Multiply Nested Steps

```python
# Sequential = ADD
for x in arr:    # O(n)
    pass
for y in arr:    # O(n)
    pass
# Total: O(n) + O(n) = O(2n) → O(n)

# Nested = MULTIPLY
for x in arr:          # O(n)
    for y in arr:      #   × O(n)
        pass
# Total: O(n) × O(n) = O(n²)
```

---

## Common Interview Traps

### Trap 1: "Nested Loop = Always O(n²)"

Just because you see a `while` loop inside a `for` loop doesn't make it $O(n^2)$. Look at the **total number of operations** across all iterations.

```python
def sliding_window(arr: list[int]) -> int:
    """
    Time: O(n), NOT O(n²)
    """
    left = 0
    # Outer loop runs n times
    for right in range(len(arr)):
        # Inner loop advances 'left'.
        # Across the ENTIRE execution of the function, 'left'
        # can only be advanced n times total.
        while left < right and arr[left] < 0:
            left += 1

    # Total operations: `right` moves n times, `left` moves at most n times.
    # Total time = O(n + n) = O(n).
    return left
```

### Trap 2: Ignoring Hidden Loops (Built-in functions)

Python hides loops in clean syntax. You must know the complexity of built-ins.

```python
# This is O(n²), not O(n)
for i in range(n):
    if target in arr:  # 'in' on a list is an O(n) linear search!
        pass
# Total: O(n) × O(n) = O(n²)
```

### Trap 3: String Concatenation

Strings are immutable in Python, Java, and many other languages. Creating a new string requires allocating memory and copying the old string.

```python
# Historically O(n²), not O(n)
s = ""
for char in chars:     # O(n) iterations
    s += char          # Each += creates new string: O(current length)
# Total time: 1 + 2 + 3 + ... + n = O(n²)

# Note: Modern CPython optimizes `+=` in specific cases, but you should
# ALWAYS use the O(n) join method in interviews to show you understand immutability.

# The correct, guaranteed O(n) way:
s = "".join(chars)  # Join pre-calculates length, allocates once, copies once: O(n)
```

### Trap 4: Amortized Time (Dynamic Arrays)

When you `append()` to a Python list or Java ArrayList, it's usually $O(1)$. But when the underlying fixed-size array gets full, it has to allocate a new, larger array and copy all $N$ elements over ($O(n)$ time).

Because this $O(n)$ resize happens rarely (usually doubling the size each time), the cost "spreads out" over many $O(1)$ operations.
**Result**: Appending is **$O(1)$ amortized time**, but $O(n)$ worst-case.

---

## Practice: Identify the Complexity

Try to identify the time and space complexity before expanding the answers.

```python
# Problem 1
def mystery1(n: int) -> None:
    for i in range(n):
        for j in range(i):
            pass
```

<details>
<summary>Answer 1</summary>

**Time: $O(n^2)$**. The inner loop runs 0 times, then 1 time, then 2 times, up to $n-1$ times.
$0 + 1 + 2 + ... + (n-1) = \frac{n(n-1)}{2}$, which drops to $O(n^2)$.
**Space: $O(1)$**.

</details>

```python
# Problem 2
def mystery2(n: int) -> None:
    i = n
    while i > 0:
        i //= 2
```

<details>
<summary>Answer 2</summary>

**Time: $O(\log n)$**. We are halving $i$ each iteration.
**Space: $O(1)$**.

</details>

```python
# Problem 3
def mystery3(arr: list[int]) -> list[int]:
    result = []
    for x in arr:
        if x not in result:
            result.append(x)
    return result
```

<details>
<summary>Answer 3</summary>

**Time: $O(n^2)$**. The `in` check on a list is $O(\text{len}(\text{result}))$, and we do it $n$ times.
**Space: $O(n)$** to store the result array (worst case: all unique elements).

*Fix: Use a `set` for $O(1)$ lookups to make time $O(n)$!*

</details>

---

## Key Takeaways

1. **Big-O describes upper bound growth rate**, not exact milliseconds or operations.
2. **Space complexity is just as important as Time complexity.** Don't forget the recursion call stack!
3. **Drop constants and lower-order terms**.
4. **Use different variables for different inputs** (e.g., $O(N + M)$).
5. **Watch for hidden $O(n)$ operations** (list `in`, `min()`, `max()`, `sum()`, string concatenation).
6. **Not all nested loops are $O(n^2)$**; trace the variables (like in sliding windows).

---

## Next: [02-time-complexity.md](./02-time-complexity.md)

Deep dive into analyzing loops, recursion trees, and master theorem basics.
