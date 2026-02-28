# Implementation Plan: Recursion & Backtracking Standardization

## Objective
Upgrade all markdown files in the `11-recursion-backtracking` directory to meet senior-engineer standards. The refactoring will focus on correctness (eliminating Python anti-patterns), rigorous complexity analysis, and consistent pedagogical mental models.

## Context
The current notes have some suboptimal Python patterns (like $O(n)$ slicing in recursive calls, e.g., `s[1:]`), lack some precision in space complexity (not distinguishing between call stack vs output storage), and could use more unified mental models for backtracking (like explicitly comparing the "Binary Include/Exclude" tree vs the "Loop-based Suffix Selection" tree). This plan addresses these issues across all 15 files in the chapter to make them top-tier interview prep material.

## Pedagogical Structure Standards
Every file will be restructured to strictly follow this logical flow:
1. **Core Concept**: Brief definition of the problem class.
2. **Intuition & Mental Models**: Consistent use of frameworks:
   - *State vs. Level* for backtracking trees.
   - *Include/Exclude* (binary choice) vs. *Suffix Selection* (iterating through remaining choices via loops).
3. **Visualizations**:
   - Mandatory ASCII trees illustrating the recursive call stack.
   - Explicit visual indication of pruning (e.g., `✗ (overspent)` or `(pruned due to duplicate)`).
4. **Basic Implementation**: Clean, well-commented Python code avoiding anti-patterns.
5. **Optimized/Alternative Implementation**: (If applicable) In-place swapping, bit manipulation, or mathematical pruning.
6. **Complexity Analysis**:
   - Explicit distinction between **Auxiliary Space** (call stack depth) and **Total Space** (storing the resulting arrays).
   - Mathematical justification for Time Complexity (e.g., explaining that the $N$ in $O(N \cdot 2^N)$ comes from the $O(N)$ operation of explicitly copying the path).
7. **Common Pitfalls**: A dedicated section for frequent interview mistakes.

## Code Correctness & Performance Standards
- **Eradicate $O(n)$ Slicing**: Replace all instances of `arr[1:]` passed in recursive calls with $O(1)$ index-based pointers (e.g., `start_index`, `idx`).
- **Explicit Copying**: Highlight `result.append(path[:])` and explicitly warn against `result.append(path)`, explaining *why* reference types mutate.
- **State Management**: Clear differentiation between passing state implicitly via arguments vs. backtracking by explicitly mutating and restoring a shared list (`path.append()` -> `backtrack()` -> `path.pop()`).
- **Duplicate Handling & Pruning**: Standardize sorting requirements for duplicate handling (`if i > start and nums[i] == nums[i-1]: continue`) and visually explain the difference between input duplicates and same-level duplicates.

## Execution Batches
- [x] **Batch 1: The Foundations**
  - `01-recursion-basics.md`, `02-subsets.md`, `03-permutations.md`
  - *Focus*: Establish the *Include/Exclude* and *Suffix Selection* mental models. Replace any slicing with index pointers.
- [x] **Batch 2: Combinatorics & Sums**
  - `04-combinations.md`, `05-combination-sum.md`
  - *Focus*: Solidify pruning logic and ASCII trees demonstrating duplicate handling.
- [x] **Batch 3: Grid & State Backtracking**
  - `06-n-queens.md`, `07-sudoku-solver.md`, `08-word-search.md`
  - *Focus*: 2D matrix state mutation/restoration and bounding box optimizations.
- [x] **Batch 4: Strings & Trees**
  - `09-generate-parentheses.md`, `10-letter-combinations.md`, `README.md`
  - *Focus*: Path building, mapping logic, and strict string concatenation performance notes.

## Verification
- [x] Review the markdown files to ensure they render correctly and code syntax blocks are valid.
- [x] Ensure the complexity analysis is strictly differentiated (Auxiliary vs Total space).
- [x] Check that all slicing anti-patterns have been removed.

### Review Summary
- Replaced recursive array slicing `nums[1:]` with $O(1)$ `index` pointers in all files.
- Separated Auxiliary Space vs. Total Space in all complexity analyses across the 11 `recursion-backtracking` markdown files.
- Re-structured `README.md` to emphasize mental models like *Include/Exclude* vs *Suffix Selection*.
- Enhanced visualization using detailed ASCII trees indicating pruned states (e.g., `✗`).
- Addressed mutation anti-patterns, specifically focusing on path copies via `result.append(path[:])`.
- Checked all markdown headers and tables for syntax issues using `markdownlint`.
