# Chapter 05: Stacks & Queues

## Why This Matters for Interviews

Stacks and queues are **essential interview topics** at FANG+ companies because:

1. **Fundamental data structures**: Building blocks for many algorithms (DFS uses stack, BFS uses queue)
2. **LIFO/FIFO reasoning**: Tests your understanding of order-dependent processing
3. **Pattern versatility**: Monotonic stacks, expression parsing, sliding window max
4. **Design problems**: Min stack, implement queue using stacks, etc.
5. **Real-world relevance**: Browser history, undo/redo, task scheduling, rate limiting

At FANG+ companies, stack/queue problems range from easy warm-ups to tricky design questions.

**Interview frequency**: High. Expect stack or queue patterns in most interview loops.

---

## Core Patterns to Master

| Pattern | Frequency | Key Problems |
|---------|-----------|--------------|
| Valid Parentheses | Very High | Matching brackets, valid strings |
| Monotonic Stack | Very High | Next greater element, daily temperatures |
| Min/Max Stack | High | Stack with O(1) getMin/getMax |
| Queue with Stacks | High | Implement queue using two stacks |
| Stack with Queues | Medium | Implement stack using queues |
| Monotonic Deque | Medium | Sliding window maximum |
| Expression Evaluation | Medium | Calculator, reverse polish notation |

---

## Chapter Sections

| Section | Topic | Key Takeaway |
|---------|-------|--------------|
| [01-stack-basics](./01-stack-basics.md) | Stack Operations & Implementation | LIFO operations, use cases |
| [02-queue-basics](./02-queue-basics.md) | Queue Operations & Circular Queue | FIFO operations, circular implementation |
| [03-valid-parentheses](./03-valid-parentheses.md) | Matching Brackets | Stack for nested structure validation |
| [04-monotonic-stack](./04-monotonic-stack.md) | Monotonic Stack Pattern | Next greater element, daily temperatures |
| [05-monotonic-queue](./05-monotonic-queue.md) | Sliding Window Maximum | Deque for O(n) sliding window max |
| [06-min-stack](./06-min-stack.md) | Min Stack Design | O(1) push, pop, top, and getMin |
| [07-stack-with-queues](./07-stack-with-queues.md) | Implement Stack Using Queues | Design problem, tradeoffs |
| [08-queue-with-stacks](./08-queue-with-stacks.md) | Implement Queue Using Stacks | Amortized O(1) operations |
| [09-expression-evaluation](./09-expression-evaluation.md) | Expression Parsing | Calculator, RPN evaluation |
| [10-histogram-problems](./10-histogram-problems.md) | Largest Rectangle in Histogram | Classic monotonic stack application |

---

## Common Mistakes Interviewers Watch For

1. **Empty stack/queue access**: Popping from empty structure without checking
2. **Wrong direction**: Confusing LIFO vs FIFO in algorithm design
3. **Monotonic stack direction**: Using increasing when decreasing is needed (or vice versa)
4. **Off-by-one in sliding window**: Incorrect window boundary handling
5. **Not handling equal elements**: Monotonic stack behavior with duplicates
6. **Forgetting edge cases**: Empty input, single element, all same values

---

## Time Targets

| Difficulty | Target Time | Examples |
|------------|-------------|----------|
| Easy | 10-15 min | Valid Parentheses, Implement Queue using Stacks |
| Medium | 15-25 min | Daily Temperatures, Min Stack, Evaluate RPN |
| Hard | 25-40 min | Largest Rectangle in Histogram, Basic Calculator |

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

```python
stack = []
stack.append(1)      # Push
top = stack[-1]      # Peek
val = stack.pop()    # Pop
is_empty = len(stack) == 0
```

### Queue (using deque)

```python
from collections import deque

queue = deque()
queue.append(1)      # Enqueue (right)
val = queue.popleft() # Dequeue (left)
is_empty = len(queue) == 0
```

---

## Key Complexity Facts

| Operation | Stack (list) | Queue (deque) | Queue (list) |
|-----------|-------------|---------------|--------------|
| Push/Enqueue | O(1)* | O(1) | O(1)* |
| Pop/Dequeue | O(1) | O(1) | O(n) ⚠️ |
| Peek | O(1) | O(1) | O(1) |
| isEmpty | O(1) | O(1) | O(1) |

*Amortized, occasional O(n) for dynamic resizing

⚠️ **Never use `list.pop(0)` for queue operations** - it's O(n). Use `deque.popleft()`.

---

## Prerequisites

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

Understanding Big-O is essential. Arrays and linked lists knowledge helps understand implementation choices.

---

## Next Steps

Start with [01-stack-basics.md](./01-stack-basics.md) to understand stack operations and common use cases. Then progress through valid parentheses and monotonic stack patterns - these are the highest priority for interviews.
