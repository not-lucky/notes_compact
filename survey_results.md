# Diagram Audit Survey Results (fn-1-202.1)

This document maps all existing diagrams in the repository and identifies standardization/alignment issues.

## Legacy ASCII Diagrams
These use `+`, `-`, `|` and should be converted to Unicode (`┌`, `─`, `┐`, `│`).

| File Path | Lines | Type | Notes |
| :--- | :--- | :--- | :--- |
| `08-graphs/03-dfs-basics.md` | 15-21 | Maze/Grid | High priority: uses `+---` style. |
| `solutions/02-arrays-strings/06-container-with-most-water.md` | 170-179 | Histogram | Uses `|` for bars; could use Unicode block elements or standard box lines. |
| `08-graphs/01-graph-representations.md` | 71-76, 327-332 | Graph | Simple ASCII arrows and nodes. |
| `14-union-find/01-union-find-basics.md` | 42-59 | Tree | Uses `/`, `\`, `|` for tree edges. |

## Existing Unicode Diagrams (Style Reference)
These already use Unicode box-drawing characters.

| File Path | Lines | Type | Alignment/Quality Check |
| :--- | :--- | :--- | :--- |
| `B-problem-patterns/01-pattern-flowchart.md` | 71-84, 91-121, 166-196, 238-267, 305-329 | Flowcharts | **Reference Standard**. Generally well-aligned. |
| `02-arrays-strings/03-two-pointers-opposite.md` | 74-81 | Array | Uses `┌───┐`. |
| `02-arrays-strings/06-prefix-sum.md` | 302-318 | Geometry | Uses Unicode for 2D area. |
| `05-stacks-queues/01-stack-basics.md` | 75-84 | Data Structure | Stack visualization. |
| `05-stacks-queues/04-monotonic-stack.md` | 116-131 | Data Structure | Stack visualization. |
| `08-graphs/03-dfs-basics.md` | 458-500 | Call Stack | Complex tree-like stack trace. |
| `17-system-design-basics/02-lru-cache.md` | 39-46, 110-120 | System/DS | Node and List visualization. |

## Identified Alignment Issues
- `B-problem-patterns/01-pattern-flowchart.md`: Large boxes like the "ARRAY PROBLEM" (Lines 91-121) have deep nested branches that need careful grid verification in subsequent tasks.
- `08-graphs/03-dfs-basics.md`: The maze diagram at line 15 is slightly uneven due to the way `+` and `-` are spaced.

## Summary for Implementation Phase
1.  **Standardize**: Target `08-graphs/03-dfs-basics.md`, `08-graphs/01-graph-representations.md`, and `14-union-find/01-union-find-basics.md` for Unicode conversion.
2.  **Align**: All diagrams in `B-problem-patterns/` need a final grid alignment pass.
3.  **Enrich**: Add Big-O and state labels as per epic requirements.
