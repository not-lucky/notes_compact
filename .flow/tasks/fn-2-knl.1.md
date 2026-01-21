# fn-2-knl.1 Implement Advanced DP Modules

## Description
Create comprehensive guides and templates for advanced Dynamic Programming patterns that are standard in L5+ interviews.

## Scope
1.  **Bitmask DP**:
    *   Concept: Using integers to represent sets.
    *   Problem: "Traveling Salesperson", "Smallest Sufficient Team", or "Partition to K Equal Sum Subsets".
    *   Complexity: Time `O(2^N * N)`, Space `O(2^N)`.
2.  **Digit DP**:
    *   Concept: Constructing numbers digit by digit with constraints.
    *   Problem: "Number of Digit One", "Numbers with specific properties in range [L, R]".
    *   Technique: Memoization with `(index, tight, leading_zeros, ...)` state.
3.  **DP on Trees**:
    *   Concept: Processing subtrees and rerooting.
    *   Problem: "Maximum Path Sum", "Diameter of Tree", "Tree Distances".

## Definition of Done
- [x] Directory `18-advanced-dp` created.
- [x] `01-bitmask-dp.md` created with intuition, template, and 2 solved problems.
- [x] `02-digit-dp.md` created with intuition, template, and 2 solved problems.
- [x] `03-tree-dp.md` created with intuition, template, and 2 solved problems.
- [x] All code is Pythonic and commented.

## Done summary
Implemented comprehensive guides for Bitmask DP, Digit DP, and Tree DP (including Rerooting). Each guide includes intuition, templates, and 2-3 solved problems with Python implementations.
## Evidence
- Commits: aff57670a879b09d3e3e041c011f7d9b061cb229
- Tests: Manual verification of code snippets against standard implementations
- PRs: