# fn-2-knl.4 Implement Python Internals Module

## Description
Deep dive into Python's implementation details. Essential for interviews where "Mastery of Language" is assessed.

## Scope
1.  **Memory Model**:
    *   Everything is an object.
    *   Variables are references.
    *   Mutability vs Immutability.
2.  **Garbage Collection**:
    *   Reference Counting (primary mechanism).
    *   Generational GC (for cyclic references).
    *   `gc` module basics.
3.  **Optimization & Advanced Features**:
    *   `__slots__`: Reducing memory footprint.
    *   Iterators & Generators (`yield`): Lazy evaluation.
    *   Decorators: Closures and wrappers.
    *   Context Managers: `__enter__`, `__exit__`.

## Definition of Done
- [x] Directory `21-python-internals` created.
- [x] `01-memory-management.md` created.
- [x] `02-generators-and-iterators.md` created.
- [x] `03-decorators-and-managers.md` created.
- [x] `04-python-gotchas.md` (e.g., mutable default args).

## Done summary
# Task Summary: fn-2-knl.4

Implemented a comprehensive Python Internals module covering memory management, generators/iterators, decorators, context managers, and common language pitfalls.
## Evidence
- Commits:
- Tests:
- PRs: