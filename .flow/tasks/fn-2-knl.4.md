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
- [ ] Directory `21-python-internals` created.
- [ ] `01-memory-management.md` created.
- [ ] `02-generators-and-iterators.md` created.
- [ ] `03-decorators-and-managers.md` created.
- [ ] `04-python-gotchas.md` (e.g., mutable default args).
