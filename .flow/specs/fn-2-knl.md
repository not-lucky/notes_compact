# fn-2-knl The Elite FANG 2026 Upgrade

## Description
This epic upgrades the `notes_fang` repository from a standard DSA resource to an **Elite Preparation Suite** for Senior/Staff Engineer (L5+) interviews at Google, Meta, Netflix, and High-Frequency Trading (HFT) firms. It shifts focus from "knowing algorithms" to "mastering systems, concurrency, and deep language internals" alongside advanced algorithmic techniques.

## Scope

### 1. Advanced Algorithmic Patterns
*   **Bitmask DP**: State representation, optimization techniques.
*   **Digit DP**: Counting numbers with properties in ranges.
*   **DP on Trees**: Rerooting technique, diameter, interacting with subtrees.
*   **Range Queries**: Segment Trees (Lazy Propagation), Fenwick Trees (BIT), Sparse Tables (RMQ).
*   **Graph Algorithms**: Tarjan's (SCC, Bridges), Binary Lifting (LCA), Euler Tours.

### 2. Concurrency & Parallelism (The "Meta/Netflix" Layer)
*   **Core Concepts**: Process vs Thread, Deadlocks, Livelocks, Race Conditions.
*   **Python Specifics**: The GIL (Global Interpreter Lock), `threading` vs `multiprocessing`, `asyncio` basics.
*   **Implementation Patterns**: 
    *   Thread-safe Queue / Blocking Queue.
    *   Producer-Consumer with `Condition` variables.
    *   Read-Write Locks.
    *   Token Bucket / Leaky Bucket (Rate Limiter) logic.

### 3. Python Language Internals (The "Google" Layer)
*   **Memory Management**: Reference counting, Garbage Collection, Generations.
*   **Advanced Features**: Decorators, Generators (`yield`), Context Managers (`with`), Metaclasses (brief), `__slots__`.
*   **Performance**: List vs Tuple, Set vs List lookups, time complexity of internal operations.

### 4. The "Strategy Layer" & Visualization
*   **Meta-Cognition**: Add "Intuition", "Trade-offs", and "Evolution" sections to key patterns.
*   **Visuals**: Upgrade to Mermaid.js sequence diagrams for concurrency and state machines for DP.

### 5. System Design Connector
*   Link DSA problems to System Design concepts (e.g., "Consistent Hashing" from HashMaps, "QuadTrees" from Spatial Indexing).

## Acceptance Criteria
- [ ] New Directory `18-advanced-dp` created with Bitmask, Digit, Tree DP guides.
- [ ] New Directory `19-range-queries` created with Segment Tree and Fenwick Tree guides.
- [ ] New Directory `20-concurrency` created with 5+ deeply explained patterns and runnable code.
- [ ] New Directory `21-python-internals` created.
- [ ] `task.md` created to track detailed progress.
- [ ] All new code examples are PEP8 compliant and include complexity analysis.

## Work Phases
1.  **Phase 1: Advanced Algorithms** (DP & Range Queries)
2.  **Phase 2: Concurrency & OS Concepts**
3.  **Phase 3: Python Internals & Deep Dives**
4.  **Phase 4: Visuals & System Design Links**
