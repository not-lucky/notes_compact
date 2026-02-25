# Chapter 04: Linked Lists

## Why This Matters for Interviews

Linked lists are a **fundamental interview topic** at FANG+ companies because:

1. **Pointer manipulation**: Tests your ability to handle references and memory
2. **In-place modifications**: Many problems require O(1) space solutions
3. **Edge case handling**: Empty lists, single nodes, cycles expose coding discipline
4. **Pattern versatility**: Fast-slow pointers, reversal, and merge patterns appear repeatedly
5. **Follow-up complexity**: "Can you do it in one pass?" or "with O(1) space?"

At FANG+ companies, linked list problems are often used as warm-up or to test fundamental CS knowledge.

**Interview frequency**: Medium-High. Expect at least 1 linked list problem in an interview loop.

---

## Core Patterns to Master

| Pattern                | Frequency | Key Problems                                   |
| ---------------------- | --------- | ---------------------------------------------- |
| Fast-Slow Pointers     | Very High | Cycle Detection, Find Middle, Nth from End     |
| Reversal Patterns      | Very High | Reverse List, Reverse Between, Reverse K-Group |
| Merge Operations       | High      | Merge Two Sorted, Merge K Sorted               |
| Dummy Node Technique   | High      | Most insert/delete operations                  |
| Intersection Detection | Medium    | Intersection of Two Lists                      |
| Deep Copy              | Medium    | Copy List with Random Pointer                  |

---

## Chapter Sections

| Section                                                     | Topic                       | Key Takeaway                               |
| ----------------------------------------------------------- | --------------------------- | ------------------------------------------ |
| [01-linked-list-basics](./01-linked-list-basics.md)         | Node Structure & Traversal  | Foundation for all linked list operations  |
| [02-fast-slow-pointers](./02-fast-slow-pointers.md)         | Fast-Slow Pointer Technique | Cycle detection, find middle, nth from end |
| [03-reversal-patterns](./03-reversal-patterns.md)           | Reversal Patterns           | Reverse entire, partial, and k-group       |
| [04-merge-lists](./04-merge-lists.md)                       | Merge Operations            | Merge sorted lists efficiently             |
| [05-intersection-detection](./05-intersection-detection.md) | Find Intersection           | Two-pointer technique for intersection     |
| [06-palindrome-list](./06-palindrome-list.md)               | Palindrome Check            | Combine fast-slow with reversal            |
| [07-dummy-node-technique](./07-dummy-node-technique.md)     | Dummy Node Pattern          | Simplify edge cases in list operations     |
| [08-copy-with-random](./08-copy-with-random.md)             | Deep Copy with Random       | Handle complex node relationships          |

---

## Common Mistakes Interviewers Watch For

1. **Losing the head**: Not saving reference to head before traversal
2. **Null pointer exceptions**: Forgetting to check `node is None` or `node.next is None`
3. **Off-by-one errors**: Wrong pointer in "nth from end" problems
4. **Cycle creation**: Accidentally creating cycles during reversal or modification
5. **Memory leaks**: Not properly handling node deletion (less critical in Python)
6. **Forgetting edge cases**: Empty list, single node, two nodes

---

## Time Targets

| Difficulty | Target Time | Examples                                           |
| ---------- | ----------- | -------------------------------------------------- |
| Easy       | 10-15 min   | Reverse List, Merge Two Sorted, Delete Node        |
| Medium     | 15-25 min   | Add Two Numbers, Remove Nth from End, Reorder List |
| Hard       | 25-40 min   | Merge K Sorted Lists, Reverse Nodes in K-Group     |

---

## Pattern Recognition Guide

```
"Detect cycle..."                 → Fast-slow pointers
"Find middle..."                  → Fast-slow pointers
"Nth from end..."                 → Two pointers, n apart
"Reverse list..."                 → Iterative or recursive reversal
"Merge sorted lists..."           → Two-pointer merge
"Insert/delete at position..."    → Dummy node
"Deep copy with random..."        → HashMap or interleaving
"Palindrome check..."             → Fast-slow + reversal
```

---

## Linked List Node Definition

```python
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next
```

This is the standard definition used in LeetCode and most interviews.

---

## Key Complexity Facts

| Operation          | Singly Linked | Doubly Linked | Array          |
| ------------------ | ------------- | ------------- | -------------- |
| Access by index    | O(n)          | O(n)          | O(1)           |
| Insert at head     | O(1)          | O(1)          | O(n)           |
| Insert at tail     | O(n)\*        | O(1)\*\*      | O(1) amortized |
| Insert at position | O(n)          | O(n)          | O(n)           |
| Delete at head     | O(1)          | O(1)          | O(n)           |
| Search             | O(n)          | O(n)          | O(n)           |

\*O(1) if tail pointer maintained
\*\*Requires tail pointer

---

## Prerequisites

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

Understanding Big-O notation is essential. Basic pointer/reference concepts help when visualizing node connections.

---

## Next Steps

Start with [01-linked-list-basics.md](./01-linked-list-basics.md) to understand how linked lists work and basic operations. Then progress through the patterns - fast-slow pointers and reversal patterns are the highest priority for interviews.
