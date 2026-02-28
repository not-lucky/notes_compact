# Recursion Basics

> **Prerequisites:** Basic understanding of function calls, stack data structure

## Core Concept

Recursion is a problem-solving technique where a function solves a problem by calling itself with a smaller or simpler input. It is one of the most fundamental concepts in computer science and forms the foundation for many advanced algorithms including tree traversals, divide-and-conquer, and backtracking.

## Intuition & Mental Models

**Why does recursion work?**

Think of recursion as a chain of delegation. Imagine you are in a long line and want to know your position:

1. **The Delegation Pattern**: You ask the person in front of you, "What is your position?" They ask the person in front of them, and so on until someone at the front says "I am #1." Then answers flow back: "I am #2", "I am #3", etc.

2. **The Key Mental Model**: Every recursive problem has two parts:
   - **Base case**: The simplest version you can solve directly (the person at the front).
   - **Recursive case**: A way to reduce the problem and combine results (asking the person ahead and adding 1).

3. **The "Leap of Faith"**: The most powerful recursive thinking technique is to **trust** that your recursive call correctly solves the smaller problem. Do not trace through every call—just assume it works and focus on: "If I had the answer to the smaller problem, how would I use it?"

4. **When Recursion "Clicks"**: Recursion is natural when the problem has self-similar structure—when a problem can be broken into smaller instances of itself. Trees, nested structures, and mathematical sequences all exhibit this property.

**Visual Intuition—The Nesting Dolls Model**:

```text
Problem(5) contains Problem(4) contains Problem(3) contains Problem(2) contains Problem(1)
    └── depends on ────└── depends on ────└── depends on ────└── depends on ────└── solved directly!
```

You cannot solve the outer doll without first solving the inner ones. The base case is the smallest doll that you can handle directly.

## Visualizations

### The Call Stack

When a function calls itself, each call is pushed onto the **call stack**. Each function call has its own scope (local variables).

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

**Trace of `factorial(4)`**:

```text
Stack: [factorial(4)]
Stack: [factorial(4), factorial(3)]
Stack: [factorial(4), factorial(3), factorial(2)]
Stack: [factorial(4), factorial(3), factorial(2), factorial(1)]
factorial(1) returns 1
Stack: [factorial(4), factorial(3), factorial(2)] → returns 2*1 = 2
Stack: [factorial(4), factorial(3)] → returns 3*2 = 6
Stack: [factorial(4)] → returns 4*6 = 24
Stack: [] → done
```

### The Recursion Tree

Many recursive problems form a **recursion tree**, especially when there are multiple recursive calls per function:

```text
                        fib(5)
                      /        \
               fib(4)            fib(3)
              /      \          /      \
          fib(3)    fib(2)  fib(2)    fib(1)
          /    \
      fib(2)  fib(1)
```

This visualization helps:

- Understand the total number of calls (time complexity).
- Identify overlapping subproblems (hint for Dynamic Programming).
- Debug recursive logic.

## Basic Implementation

### The Three Components

#### 1. Base Case

The condition where recursion stops. Without it, you get an infinite loop (Stack Overflow).

```python
def factorial(n: int) -> int:
    # Base case: stop when n is 0 or 1
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

#### 2. Recursive Case

The part where the function calls itself with a smaller/simpler input.

```python
def sum_list(nums: list[int], index: int = 0) -> int:
    # Base case
    if index == len(nums):
        return 0
    # Recursive case: current element + sum of rest
    # Note: We use an index pointer rather than nums[1:] to avoid \mathcal{O}(N) slicing
    return nums[index] + sum_list(nums, index + 1)
```

#### 3. Progress Toward Base Case

Each recursive call must move closer to the base case.

```python
# WRONG: No progress toward base case
def infinite(n: int) -> None:
    infinite(n)  # Never terminates!

# CORRECT: n decreases each call
def countdown(n: int) -> None:
    if n <= 0:
        return
    print(n)
    countdown(n - 1)  # Progress: n → n-1
```

## Complexity Analysis

When analyzing recursion, we must distinguish between:

1. **Auxiliary Space**: Memory used by the call stack.
2. **Total Space**: Auxiliary Space + Memory used to store the output/results.

| Pattern | Example | Time Complexity | Auxiliary Space (Call Stack) |
| ------- | ------- | --------------- | ---------------------------- |
| **Linear** | Factorial | $\mathcal{O}(N)$ - $N$ calls | $\mathcal{O}(N)$ depth |
| **Binary** | Fibonacci | $\mathcal{O}(2^N)$ - exponential nodes | $\mathcal{O}(N)$ max depth |
| **Divide & Conquer** | Merge Sort | $\mathcal{O}(N \log N)$ | $\mathcal{O}(\log N)$ depth |

**Note on Time Complexity:**
The time complexity of a recursive algorithm is generally:
`Total Recursive Calls * Time Complexity per Call`

For example, if you slice an array in your recursive call (`arr[1:]`), the slicing takes $\mathcal{O}(N)$ time. If you do this $N$ times, your time complexity becomes $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N)$. **Always use index pointers (`start_index`) to pass arrays $\mathcal{O}(1)$ instead of slicing.**

## Common Pitfalls

1. **Forgetting the Base Case**: Always write the base case first. Without it, you will get a `RecursionError: maximum recursion depth exceeded`.
2. **Passing Array Slices (`arr[1:]`)**: Slicing creates a new array, taking $\mathcal{O}(N)$ time and $\mathcal{O}(N)$ space. This turns an $\mathcal{O}(N)$ algorithm into an $\mathcal{O}(N^2)$ algorithm. Use an index parameter instead.
3. **Not Trusting the Recursion**: Trying to mentally trace every single call down to the base case for complex problems. Use the "Leap of Faith"—trace one level down and trust the rest.
4. **Returning the Wrong Type**: Ensure the recursive case returns the same type as the base case.
5. **Ignoring Stack Overflow Limits**: Python's default stack limit is ~1000. Problems with $N > 1000$ may crash. If the input can be large, convert to iteration.

## When NOT to Use Recursion

Recursion is elegant but not always the best choice. Avoid it when:

1. **Simple Loops Suffice**: If a problem can be solved with a straightforward `for` or `while` loop, prefer iteration. It is often clearer and more efficient.
2. **Deep Recursion Depth**: For inputs $N > 1000$, convert to iteration or increase the limit carefully (`sys.setrecursionlimit`).
3. **Heavy State Passing**: If you need to pass many variables through recursive calls, the overhead adds up. An iterative solution with explicit state may be cleaner.
4. **Performance-Critical Code**: Each function call has overhead (stack frame creation, parameter passing). For performance-critical inner loops, iteration is faster.

---

## Next: [02-subsets.md](./02-subsets.md)

Learn how to generate all subsets using recursion and backtracking.
