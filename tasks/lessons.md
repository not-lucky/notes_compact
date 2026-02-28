# Lessons Learned

- Emphasize the separation between auxiliary space (call stack) and total space (storing result array).
- Highlight Python anti-patterns like O(n) slicing `arr[1:]` and recommend index pointers `start_idx`.
- Always ensure `path.pop()` is explicitly stated when using shared mutable lists for backtracking.
- Mention `"".join(path)` or `path[:]` to prevent appending empty lists into results.
- **Mental Models**: Consistently use defined frameworks like "Binary Include/Exclude" vs. "Loop-based Suffix Selection" instead of ad-hoc explanations for backtracking.
- **Visualizations**: Use explicit ASCII trees with clearly marked pruned branches (e.g., `✗ (overspent)`) to communicate constraints and dead ends visually rather than just textually.
- **Mutation & Reference Warnings**: When building a path incrementally, explicitly warn against `result.append(path)` explaining *why* reference types mutate. Always advocate for explicitly copying via `result.append(path[:])` and mathematically document the $O(N)$ operation inside complexity calculations.
- **Grid State Management**: Clearly document the 3 steps of grid backtracking: `1. Mutate State`, `2. Recurse`, and `3. Restore State (Backtrack)`. Call out implicit backtracking anti-patterns like deep copying a Sudoku board.