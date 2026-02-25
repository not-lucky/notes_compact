# Chapter 05: Stacks & Queues

Stacks and queues are fundamental linear data structures that impose specific constraints on how elements are added or removed. They are widely used both as standalone concepts and as the backbone for more complex algorithms. Mastering these patterns is critical for any technical interview.

### Why This Matters for Interviews
Stacks and queues frequently appear in FANG+ interviews because they elegantly encapsulate order-dependent processing. They test your fundamental computer science knowledge and ability to model state correctly.

1. **Algorithmic Building Blocks:** They power many graph and tree traversal algorithms (e.g., Depth-First Search naturally uses a stack and Breadth-First Search requires a queue).
2. **LIFO vs. FIFO Constraints:** They test your ability to correctly implement logic requiring either Last-In-First-Out (LIFO) or First-In-First-Out (FIFO) semantics.
3. **Versatile Patterns:** They form the basis of powerful problem-solving techniques, such as monotonic stacks for next-greater elements, expression parsing for calculators, and sliding window maximums using deques.
4. **Design Problems:** They are commonly featured in system design and data structure design rounds (e.g., implementing a `Min Stack` that retrieves the minimum element in $\mathcal{O}(1)$ time).
5. **Real-World Applications:** They simulate real-world systems like browser history (back/forward buttons), text editor undo/redo functionalities, CPU task scheduling, and network traffic rate limiting.

At FANG+ companies, stack and queue problems range from easy warm-ups to tricky design questions. Expect to encounter them frequently in your interview loops.

---

## Core Patterns to Master

| Pattern               | Frequency | Key Problems                             |
| --------------------- | --------- | ---------------------------------------- |
| Valid Parentheses     | Very High | Matching brackets, valid strings         |
| Monotonic Stack       | Very High | Next greater element, daily temperatures |
| Min/Max Stack         | High      | Stack with $\mathcal{O}(1)$ getMin/getMax|
| Queue with Stacks     | High      | Implement queue using two stacks         |
| Stack with Queues     | Medium    | Implement stack using queues             |
| Monotonic Deque       | Medium    | Sliding window maximum                   |
| Expression Evaluation | Medium    | Calculator, reverse polish notation      |

---

## Chapter Sections

| Section                                                   | Topic                             | Key Takeaway                             |
| --------------------------------------------------------- | --------------------------------- | ---------------------------------------- |
| [01-stack-basics](./01-stack-basics.md)                   | Stack Operations & Implementation | LIFO operations, use cases               |
| [02-queue-basics](./02-queue-basics.md)                   | Queue Operations & Circular Queue | FIFO operations, circular implementation |
| [03-valid-parentheses](./03-valid-parentheses.md)         | Matching Brackets                 | Stack for nested structure validation    |
| [04-monotonic-stack](./04-monotonic-stack.md)             | Monotonic Stack Pattern           | Next greater element, daily temperatures |
| [05-monotonic-queue](./05-monotonic-queue.md)             | Sliding Window Maximum            | Deque for $\mathcal{O}(N)$ sliding window max|
| [06-min-stack](./06-min-stack.md)                         | Min Stack Design                  | $\mathcal{O}(1)$ push, pop, top, and getMin      |
| [07-stack-with-queues](./07-stack-with-queues.md)         | Implement Stack Using Queues      | Design problem, tradeoffs                |
| [08-queue-with-stacks](./08-queue-with-stacks.md)         | Implement Queue Using Stacks      | Amortized $\mathcal{O}(1)$ operations            |
| [09-expression-evaluation](./09-expression-evaluation.md) | Expression Parsing                | Calculator, RPN evaluation               |
| [10-histogram-problems](./10-histogram-problems.md)       | Largest Rectangle in Histogram    | Classic monotonic stack application      |

---

## Common Mistakes Interviewers Watch For

1. **Empty Structure Access:** Always check `if stack` or `if queue` before attempting to `pop()`, `popleft()`, or access the `top()`/`peek()`. Doing so avoids an `IndexError`.
2. **Confusing LIFO vs. FIFO:** Choosing the wrong data structure for the problem. E.g., using a stack to traverse a tree by level (BFS) instead of a queue.
3. **Monotonic Pattern Directionality:** Incorrectly maintaining the monotonic invariant. E.g., maintaining an increasing stack when a strictly decreasing one was required to find the "next greater element".
4. **Incorrect Boundary Conditions:** Off-by-one errors in indices when using monotonic deques for sliding window problems, or incorrectly adding/removing from the window ends.
5. **Mishandling Duplicates:** Failing to consider if the monotonic stack should use strictly greater/less than (`>`) or greater/less than or equal to (`>=`) operators when elements are equal.
6. **Neglecting Edge Cases:** Not validating inputs such as empty strings, single-element arrays, strings with unbalanced characters, or arrays with all identical values.

---

## Time Targets

| Difficulty | Target Time | Examples                                         |
| ---------- | ----------- | ------------------------------------------------ |
| Easy       | 10-15 min   | Valid Parentheses, Implement Queue using Stacks  |
| Medium     | 15-25 min   | Daily Temperatures, Min Stack, Evaluate RPN      |
| Hard       | 25-40 min   | Largest Rectangle in Histogram, Basic Calculator |

---

## Pattern Recognition Guide

```
"Matching brackets..."           → Stack
"Next greater element..."        → Monotonic stack (decreasing)
"Previous smaller element..."    → Monotonic stack (increasing)
"Sliding window maximum..."      → Monotonic deque
"Implement queue using..."       → Two stacks
"Evaluate expression..."         → Stack(s) for operators/operands
"Largest rectangle..."           → Monotonic stack
"Min/max in constant time..."    → Auxiliary stack
```

---

## Python Stack & Queue Implementations

### Stack (using list)

Lists in Python are dynamic arrays and are naturally suited for use as stacks since `append()` and `pop()` operations occur at the end of the array, avoiding the need for element shifting.

```python
stack = []
stack.append(1)      # Push (Amortized \mathcal{O}(1))
top = stack[-1]      # Peek (\mathcal{O}(1))
val = stack.pop()    # Pop (\mathcal{O}(1))
is_empty = len(stack) == 0
```

### Queue (using deque)

Python's `collections.deque` is implemented as a doubly-linked list. This provides constant time append and pop operations from both ends, making it ideal for implementing queues.

```python
from collections import deque

queue = deque()
queue.append(1)       # Enqueue at right tail (\mathcal{O}(1))
val = queue.popleft() # Dequeue from left head (\mathcal{O}(1))
is_empty = len(queue) == 0
```

---

## Key Complexity Facts

| Operation    | Stack (list) | Queue (deque) | Queue (list) |
| ------------ | ------------ | ------------- | ------------ |
| Push/Enqueue | $\mathcal{O}(1)$*| $\mathcal{O}(1)$| $\mathcal{O}(1)$*|
| Pop/Dequeue  | $\mathcal{O}(1)$ | $\mathcal{O}(1)$| $\mathcal{O}(N)$ ⚠️|
| Peek         | $\mathcal{O}(1)$ | $\mathcal{O}(1)$| $\mathcal{O}(1)$ |
| isEmpty      | $\mathcal{O}(1)$ | $\mathcal{O}(1)$| $\mathcal{O}(1)$ |

*Amortized, occasional $\mathcal{O}(N)$ for dynamic resizing when using lists.

⚠️ **Performance Warning**: Never use `list.pop(0)` for queue operations in Python, as it takes $\mathcal{O}(N)$ time because all subsequent elements must be shifted. Always use `collections.deque` and `popleft()` for $\mathcal{O}(1)$ dequeue operations.

---

## Prerequisites

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

Understanding Big-O is essential. Arrays and linked lists knowledge helps understand implementation choices.

---

## Next Steps

Start with [01-stack-basics.md](./01-stack-basics.md) to understand stack operations and common use cases. Then progress through valid parentheses and monotonic stack patterns - these are the highest priority for interviews.
