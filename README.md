# Data Structures & Algorithms Interview Preparation

A comprehensive technical interview preparation repository covering data structures, algorithms, and system design for software engineering roles at top technology companies.

## Overview

This repository provides structured study materials designed for systematic interview preparation. Content emphasizes:

- **Pattern-based learning** over rote memorization
- **Rigorous complexity analysis** integrated throughout
- **Python idioms** leveraging the standard library
- **Clear communication** of technical trade-offs

## Repository Structure

### Core Topics (01–16)

| Chapter | Topic | Key Patterns |
| :--- | :--- | :--- |
| [01](./01-complexity-analysis/README.md) | Complexity Analysis | Big-O notation, amortized analysis, space-time trade-offs |
| [02](./02-arrays-strings/README.md) | Arrays & Strings | Two pointers, sliding window, prefix sums |
| [03](./03-hashmaps-sets/README.md) | Hash Maps & Sets | Frequency counting, O(1) lookups, collision handling |
| [04](./04-linked-lists/README.md) | Linked Lists | Pointer manipulation, fast/slow pointers |
| [05](./05-stacks-queues/README.md) | Stacks & Queues | Monotonic stacks, BFS templates, deque operations |
| [06](./06-trees/README.md) | Trees | DFS/BFS traversals, recursion, BST properties |
| [07](./07-heaps-priority-queues/README.md) | Heaps & Priority Queues | Top-K problems, median finding, heapify |
| [08](./08-graphs/README.md) | Graphs | Adjacency representations, traversal algorithms, shortest paths |
| [09](./09-dynamic-programming/README.md) | Dynamic Programming | Memoization, tabulation, state transitions |
| [10](./10-binary-search/README.md) | Binary Search | Search space reduction, bisect utilities |
| [11](./11-recursion-backtracking/README.md) | Recursion & Backtracking | Subsets, permutations, constraint satisfaction |
| [12](./12-greedy/README.md) | Greedy Algorithms | Local optimization, interval scheduling |
| [13](./13-tries/README.md) | Tries | Prefix operations, string autocomplete |
| [14](./14-union-find/README.md) | Union-Find | Disjoint sets, cycle detection, connected components |
| [15](./15-bit-manipulation/README.md) | Bit Manipulation | XOR patterns, bitmasks, set operations |
| [16](./16-math-basics/README.md) | Math Basics | GCD/LCM, prime factorization, modular arithmetic |

### System Design (17–19)

| Chapter | Topic | Focus Areas |
| :--- | :--- | :--- |
| [17](./17-system-design-basics/README.md) | System Design Basics | Scalability, availability, CAP theorem |
| [18](./18-low-level-design/README.md) | Low-Level Design | Class modeling, design patterns, API design |
| [19](./19-high-level-design/README.md) | High-Level Design | Distributed systems, load balancing, caching strategies |

### Reference Materials

| Appendix | Topic | Contents |
| :--- | :--- | :--- |
| [A](./A-python-cheatsheet/README.md) | Python Cheatsheet | `collections`, `heapq`, `bisect`, `itertools` |
| [B](./B-problem-patterns/README.md) | Problem Patterns | Solution templates by problem category |
| [C](./C-company-specific/README.md) | Company-Specific | Interview formats and question trends |

## Recommended Study Sequence

### Phase 1: Foundations (Weeks 1–6)
1. Complexity Analysis (Chapter 01)
2. Arrays & Strings (Chapter 02)
3. Hash Maps & Sets (Chapter 03)
4. Linked Lists (Chapter 04)
5. Stacks & Queues (Chapter 05)
6. Trees (Chapter 06)

### Phase 2: Core Algorithms (Weeks 7–12)
7. Heaps & Priority Queues (Chapter 07)
8. Graphs (Chapter 08)
9. Binary Search (Chapter 10)
10. Dynamic Programming (Chapter 09)
11. Recursion & Backtracking (Chapter 11)
12. Greedy Algorithms (Chapter 12)

### Phase 3: Advanced Topics (Weeks 13–16)
13. Tries (Chapter 13)
14. Union-Find (Chapter 14)
15. Bit Manipulation (Chapter 15)
16. Math Basics (Chapter 16)

### Phase 4: System Design (Weeks 17–20)
17. System Design Basics (Chapter 17)
18. Low-Level Design (Chapter 18)
19. High-Level Design (Chapter 19)

### Phase 5: Interview Preparation (Weeks 21+)
- Company-specific practice (Appendix C)
- Mock interviews
- Problem pattern review (Appendix B)

## Usage Guidelines

### For Each Topic

1. **Read the chapter overview** for conceptual foundations
2. **Study individual subtopics** with worked examples
3. **Attempt practice problems** independently before reviewing solutions
4. **Verify complexity analysis** by articulating time/space reasoning
5. **Cross-reference** related patterns in Appendix B

### Code Examples

All solutions use Python 3.10+ with type annotations:

```python
from collections import Counter, deque
from typing import List, Dict, Set


def two_sum(nums: List[int], target: int) -> List[int]:
    """Returns indices of two numbers that sum to target."""
    seen: Dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

### Complexity Documentation Standard

Every solution includes:

- **Time Complexity**: With justification (e.g., "O(n log n) due to sorting")
- **Space Complexity**: Including auxiliary structures and call stack
- **Trade-offs**: Discussion of alternative approaches when applicable

## Prerequisites

- Proficiency in at least one programming language
- Familiarity with basic programming constructs (loops, conditionals, functions)
- High school mathematics (algebra, logarithms, basic combinatorics)

## Development Environment

### Requirements

- Python 3.10 or higher
- Optional: `mypy` for type checking
- Optional: `ruff` for linting

### Verification

```bash
# Type checking
mypy .

# Linting
ruff check .

# Testing (where applicable)
pytest
```

## Readiness Indicators

Technical interview readiness is demonstrated by the ability to:

1. Analyze and state algorithm complexity within 30 seconds
2. Identify problem patterns and select appropriate data structures within 2–3 minutes
3. Implement correct solutions within 25–35 minutes
4. Articulate design decisions and trade-offs clearly during implementation
5. Handle follow-up questions on optimization and edge cases

## Supplementary Resources

### Textbooks
- *Cracking the Coding Interview*, Gayle Laakmann McDowell
- *Elements of Programming Interviews*, Adnan Aziz, Tsung-Hsien Lee, Amit Prakash
- *Introduction to Algorithms*, Cormen, Leiserson, Rivest, Stein (reference)

### System Design
- *Designing Data-Intensive Applications*, Martin Kleppmann
- *System Design Interview*, Alex Xu

### Practice Platforms
- LeetCode
- HackerRank
- Pramp (mock interviews)

## Repository Contents

```
.
├── 01-complexity-analysis/
├── 02-arrays-strings/
├── 03-hashmaps-sets/
├── 04-linked-lists/
├── 05-stacks-queues/
├── 06-trees/
├── 07-heaps-priority-queues/
├── 08-graphs/
├── 09-dynamic-programming/
├── 10-binary-search/
├── 11-recursion-backtracking/
├── 12-greedy/
├── 13-tries/
├── 14-union-find/
├── 15-bit-manipulation/
├── 16-math-basics/
├── 17-system-design-basics/
├── 18-low-level-design/
├── 19-high-level-design/
├── A-python-cheatsheet/
├── B-problem-patterns/
├── C-company-specific/
└── tasks/
```

---

**Getting Started**: Begin with [Chapter 01: Complexity Analysis](./01-complexity-analysis/README.md) to establish the analytical foundation for all subsequent topics.
