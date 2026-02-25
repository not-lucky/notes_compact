# Implement Queue Using Stacks

> **Prerequisites:** [01-stack-basics](./01-stack-basics.md), [02-queue-basics](./02-queue-basics.md)

## Overview

This problem asks you to implement a queue (FIFO) using only stack (LIFO) operations. Unlike stack-with-queues, this problem has an elegant $\mathcal{O}(1)$ amortized solution! The key insight is that two stacks can simulate a queue: reversing LIFO ordering twice gives FIFO ordering.

## Building Intuition

**Why two stacks work for a queue**:

The magic: LIFO + LIFO = FIFO

```
Push A, B, C to a stack:
  Stack: [A, B, C] (C on top)
  Pop order: C, B, A (LIFO)

Now push those to another stack:
  Stack2: [C, B, A] (A on top)
  Pop order: A, B, C (FIFO!)
```

Reversing the order twice gives us the original order. This is the foundation of the two-stack queue.

**The Key Insight**:

```
- Input stack: New elements go here (like a holding area)
- Output stack: Pop from here (elements are in FIFO order)
- Transfer: When output is empty, reverse input to output
```

**Worked Example**:

```
Operations: push(1), push(2), pop(), push(3), pop(), pop()

push(1): input=[1], output=[]
push(2): input=[1,2], output=[]
pop():   output empty → transfer!
         pop from input to output: input=[], output=[2,1]
         (1 is now on top - first in, first out!)
         return 1, output=[2]
push(3): input=[3], output=[2]
pop():   output not empty, return 2, output=[]
pop():   output empty → transfer!
         input=[], output=[3]
         return 3
```

**Why $\mathcal{O}(1)$ Amortized?**

The clever part: we only transfer when output is empty.

```text
Trace for n pushes followed by n pops:
- Push phase: n × $\mathcal{O}(1)$ = $\mathcal{O}(n)$
- First pop: Transfer n elements $\mathcal{O}(n)$ + pop $\mathcal{O}(1)$
- Next n-1 pops: (n-1) × $\mathcal{O}(1)$ = $\mathcal{O}(n-1)$

Total: $\mathcal{O}(n)$ + $\mathcal{O}(n)$ + $\mathcal{O}(n)$ = $\mathcal{O}(3n)$
Average per operation: $\mathcal{O}(3n)$ / 2n = $\mathcal{O}(1)$ amortized!
```

Each element moves at most 3 times total:

1. Push to input: $\mathcal{O}(1)$
2. Transfer to output: $\mathcal{O}(1)$ per element
3. Pop from output: $\mathcal{O}(1)$

**Mental Model**: Think of two buckets connected by a pipe. New balls go in the left bucket (input stack). When you need a ball from the right bucket (output stack) and it's empty, you flip the left bucket over into the right bucket. Now the balls are in FIFO order in the right bucket!

## When NOT to Use This Pattern

The two-stack queue is wrong when:

1. **You Have a Queue Available**: Like stack-with-queues, this is educational. Use `collections.deque` in production.

2. **Worst-Case $\mathcal{O}(1)$ is Required**: While amortized $\mathcal{O}(1)$, individual operations can be $\mathcal{O}(n)$ during transfer. For real-time systems, use a linked-list queue.

3. **Memory Locality Matters**: Two stacks = two arrays = poor cache performance compared to a single circular buffer.

4. **You Need Both Ends**: If you need a deque (double-ended queue), this approach doesn't extend well.

**Why This IS Useful**:

- Demonstrates amortized analysis beautifully
- Common interview problem
- Shows that LIFO + LIFO = FIFO

**Comparison with Stack-with-Queues**:
| Aspect | Queue with Stacks | Stack with Queues |
|--------|-------------------|-------------------|
| Best amortized | $\mathcal{O}(1)$ ✓ | $\mathcal{O}(n)$ ✗ |
| Key insight | Lazy transfer | Must rotate |
| Practicality | More elegant | Less elegant |

## Interview Context

This problem is a **classic design question** at FANG+ companies because:

1. **Amortized analysis**: The optimal solution has $\mathcal{O}(1)$ amortized operations
2. **Lazy evaluation**: Demonstrates deferred computation pattern
3. **Real-world relevance**: Many systems use this pattern (e.g., message queues)
4. **Follow-up rich**: Leads to discussions about worst-case vs amortized complexity

Interviewers use this to assess your understanding of amortized analysis and lazy data structures.

---

## The Problem

Implement a queue using only stack operations:

- `push(x)` — Push element x to the back of queue
- `pop()` — Remove and return the front element
- `peek()` — Get the front element
- `empty()` — Return whether the queue is empty

**Constraint**: Only use `push`, `pop`, `top`, `empty` operations on stacks.

---

## Approach Comparison

| Approach                 | push | pop    | peek   | Space |
| ------------------------ | ---- | ------ | ------ | ----- |
| Two stacks (push costly) | $\mathcal{O}(n)$ | $\mathcal{O}(1)$   | $\mathcal{O}(1)$   | $\mathcal{O}(n)$  |
| Two stacks (pop costly)  | $\mathcal{O}(1)$ | $\mathcal{O}(n)$   | $\mathcal{O}(n)$   | $\mathcal{O}(n)$  |
| Two stacks (amortized)   | $\mathcal{O}(1)$ | $\mathcal{O}(1)$* | $\mathcal{O}(1)$* | $\mathcal{O}(n)$  |

\*Amortized $\mathcal{O}(1)$

---

## Solution 1: Two Stacks Amortized (Optimal)

```python
class MyQueue:
    """
    Queue using two stacks with $\mathcal{O}(1)$ amortized operations.

    Idea: Use input stack for push, output stack for pop.
    Only transfer when output is empty.

    Time Complexity: push $\mathcal{O}(1)$, pop/peek $\mathcal{O}(1)$ amortized
    Space Complexity: $\mathcal{O}(n)$
    """
    def __init__(self):
        self.input_stack = []   # For push operations
        self.output_stack = []  # For pop/peek operations

    def push(self, x: int) -> None:
        self.input_stack.append(x)

    def pop(self) -> int:
        self._transfer_if_needed()
        return self.output_stack.pop()

    def peek(self) -> int:
        self._transfer_if_needed()
        return self.output_stack[-1]

    def empty(self) -> bool:
        return len(self.input_stack) == 0 and len(self.output_stack) == 0

    def _transfer_if_needed(self) -> None:
        """Transfer from input to output only when output is empty."""
        if not self.output_stack:
            while self.input_stack:
                self.output_stack.append(self.input_stack.pop())


# Walkthrough:
# push(1): input=[1], output=[]
# push(2): input=[1,2], output=[]
# peek():  output empty → transfer → input=[], output=[2,1]
#          return output[-1] = 1
# push(3): input=[3], output=[2,1]
# pop():   output not empty → return output.pop() = 1
#          input=[3], output=[2]
# pop():   return 2, output=[]
# pop():   output empty → transfer → input=[], output=[3]
#          return 3
```

### Visual Representation

```
push(1), push(2), push(3):

  input_stack     output_stack
  ┌───┐
  │ 3 │ ←top      (empty)
  ├───┤
  │ 2 │
  ├───┤
  │ 1 │
  └───┘

pop() - transfer first:

  input_stack     output_stack
                  ┌───┐
  (empty)         │ 1 │ ←top (front of queue)
                  ├───┤
                  │ 2 │
                  ├───┤
                  │ 3 │
                  └───┘

  return 1

push(4), then pop():

  input_stack     output_stack
  ┌───┐           ┌───┐
  │ 4 │           │ 2 │ ←top
  └───┘           ├───┤
                  │ 3 │
                  └───┘

  return 2 (no transfer needed, output not empty)
```

---

## Amortized Analysis

Why is pop/peek $\mathcal{O}(1)$ amortized?

```text
Consider n push operations followed by n pop operations:

Push phase (n operations):
- Each push is $\mathcal{O}(1)$
- Total: $\mathcal{O}(n)$

Pop phase (n operations):
- First pop: Transfer n elements $\mathcal{O}(n)$ + pop $\mathcal{O}(1)$
- Remaining n-1 pops: Each is $\mathcal{O}(1)$
- Total: $\mathcal{O}(n)$ + $\mathcal{O}(n-1)$ = $\mathcal{O}(n)$

Total for 2n operations: $\mathcal{O}(n)$ + $\mathcal{O}(n)$ = $\mathcal{O}(2n)$
Amortized per operation: $\mathcal{O}(1)$

Key insight: Each element is pushed to input_stack once ($\mathcal{O}(1)$),
transferred to output_stack once ($\mathcal{O}(1)$ per element),
and popped from output_stack once ($\mathcal{O}(1)$).
Total: $\mathcal{O}(3)$ per element = $\mathcal{O}(1)$ amortized.
```

---

## Solution 2: Push Costly

```python
class MyQueue:
    """
    Queue using two stacks, costly push.

    Time Complexity: push $\mathcal{O}(n)$, pop $\mathcal{O}(1)$, peek $\mathcal{O}(1)$
    Space Complexity: $\mathcal{O}(n)$
    """
    def __init__(self):
        self.s1 = []  # Main stack (newest at bottom)
        self.s2 = []  # Helper stack

    def push(self, x: int) -> None:
        # Move all to s2
        while self.s1:
            self.s2.append(self.s1.pop())

        # Push new element (will be at bottom of s1)
        self.s1.append(x)

        # Move all back
        while self.s2:
            self.s1.append(self.s2.pop())

    def pop(self) -> int:
        return self.s1.pop()

    def peek(self) -> int:
        return self.s1[-1]

    def empty(self) -> bool:
        return len(self.s1) == 0
```

---

## Solution 3: Pop Costly

```python
class MyQueue:
    """
    Queue using two stacks, costly pop/peek.

    Time Complexity: push $\mathcal{O}(1)$, pop $\mathcal{O}(n)$, peek $\mathcal{O}(n)$
    Space Complexity: $\mathcal{O}(n)$
    """
    def __init__(self):
        self.s1 = []  # For push
        self.s2 = []  # For pop/peek

    def push(self, x: int) -> None:
        self.s1.append(x)

    def pop(self) -> int:
        # Move all to s2
        while self.s1:
            self.s2.append(self.s1.pop())

        result = self.s2.pop()

        # Move all back
        while self.s2:
            self.s1.append(self.s2.pop())

        return result

    def peek(self) -> int:
        while self.s1:
            self.s2.append(self.s1.pop())

        result = self.s2[-1]

        while self.s2:
            self.s1.append(self.s2.pop())

        return result

    def empty(self) -> bool:
        return len(self.s1) == 0
```

---

## Why Amortized Solution is Best

```text
Scenario: n push, then n pop (interleaved or sequential)

Approach           | Total Operations | Amortized per op
-------------------|------------------|------------------
Push costly        | $\mathcal{O}(n^2)$    | $\mathcal{O}(n)$ push, $\mathcal{O}(1)$ pop
Pop costly         | $\mathcal{O}(n^2)$    | $\mathcal{O}(1)$ push, $\mathcal{O}(n)$ pop
Amortized (lazy)   | $\mathcal{O}(n)$      | $\mathcal{O}(1)$ push, $\mathcal{O}(1)$ pop*

*amortized

The lazy transfer approach wins because:
1. We only transfer when necessary (output empty)
2. Each element is transferred at most once
3. We exploit the fact that consecutive pops don't need transfer
```

---

## Real-World Applications

1. **Message Queue Implementations**: Some internal implementations use similar patterns
2. **Undo/Redo Stacks**: Browser history can use this pattern
3. **Task Scheduling**: Converting LIFO to FIFO processing
4. **Interview Question Foundation**: Understanding leads to harder problems

---

## Edge Cases

```python
# 1. Empty queue
q = MyQueue()
print(q.empty())  # True

# 2. Single element
q.push(1)
print(q.peek())   # 1
print(q.pop())    # 1
print(q.empty())  # True

# 3. Interleaved operations
q.push(1)
q.push(2)
q.pop()           # 1
q.push(3)
q.peek()          # 2
q.pop()           # 2
q.pop()           # 3

# 4. Multiple pops after pushes
for i in range(1000):
    q.push(i)
for i in range(1000):
    assert q.pop() == i  # FIFO order preserved
```

---

## Follow-up Questions

### Q: What's the worst-case for a single pop?

A: $\mathcal{O}(n)$ when output stack is empty and we need to transfer. But amortized is $\mathcal{O}(1)$.

### Q: Can we guarantee $\mathcal{O}(1)$ worst-case?

A: Not with two simple stacks. Would need more complex structures (e.g., reversing during idle time).

### Q: How does this compare to deque?

A: `collections.deque` is $\mathcal{O}(1)$ worst-case for both ends. This is useful when you only have stack primitives available.

---

## Comparison with Stack Using Queues

| Aspect                      | Queue using Stacks  | Stack using Queues |
| --------------------------- | ------------------- | ------------------ |
| Best solution               | Amortized $\mathcal{O}(1)$ both | $\mathcal{O}(n)$ push or pop   |
| Key insight                 | Lazy transfer       | Must rotate        |
| Can achieve $\mathcal{O}(1)$ amortized? | Yes                 | No                 |

The queue using stacks has a better solution because:

- Two stacks can naturally reverse order (LIFO + LIFO = FIFO)
- We can delay the reversal until needed (lazy evaluation)

---

## Practice Problems

| #   | Problem                      | Difficulty | Key Concept          |
| --- | ---------------------------- | ---------- | -------------------- |
| 1   | Implement Queue using Stacks | Easy       | Core problem         |
| 2   | Implement Stack using Queues | Easy       | Reverse direction    |
| 3   | Design Circular Deque        | Medium     | Both ends            |
| 4   | Design Hit Counter           | Medium     | Queue-like with time |

---

## Key Takeaways

1. **Amortized $\mathcal{O}(1)$**: The lazy transfer approach achieves optimal performance
2. **Two stacks reverse order**: LIFO + LIFO = FIFO (stack reversal)
3. **Lazy evaluation wins**: Only transfer when output is empty
4. **Each element moves 3 times**: Push to input (1), transfer to output (2), pop from output (3)
5. **Worst-case vs amortized**: Single pop can be $\mathcal{O}(n)$, but amortized is $\mathcal{O}(1)$

---

## Next: [09-expression-evaluation.md](./09-expression-evaluation.md)

Learn how to evaluate expressions using stacks.
