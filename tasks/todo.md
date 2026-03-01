# Overall 12-Greedy Refactoring Task Plan
- [x] Refactor README.md
- [x] Refactor 03-merge-intervals.md
- [x] Refactor 02-interval-scheduling.md
- [x] Refactor 08-partition-labels.md
- [x] Refactor 05-jump-game.md
- [x] Refactor 01-greedy-basics.md
- [x] Refactor 04-meeting-rooms.md
- [x] Refactor 06-gas-station.md
- [x] Refactor 07-candy-distribution.md

## Completed 02-interval-scheduling.md
1. Wrote a Python test script (`test_intervals.py`) to systematically execute and verify all the code blocks in the file.
2. Verified the behavior of `max_activities`, `count_max_activities`, `erase_overlap_intervals` (LC 435), `find_min_arrows` (LC 452), `find_longest_chain` (LC 646), and both versions of `job_scheduling` (LC 1235).
3. Validated the logic of the dynamic programming backtracking function `job_scheduling_with_selection`, ensuring it properly rebuilds the optimal non-overlapping interval sequence.
4. Standardized the Python syntax (e.g. `list[tuple[int, int]]`).
5. Replaced some verbose comments inside functions with clear, descriptive docstrings explaining the algorithmic intent, touching conventions, and time/space complexities.
6. Improved the introductory context to explain why we focus on mapping the end time (e.g. "always pick the request that ends earliest and doesn't conflict with what you already accepted").
7. Significantly clarified the nuance between overlapping and touching intervals (`>` vs `>=`). The provided table ("Overlapping vs Touching: The Critical Detail") clearly maps common LeetCode problems to their respective convention (e.g., LC 452 Min Arrows requires `>` because balloons that touch can be shot with the same arrow).
8. Refined the DP recurrence logic for Weighted Interval Scheduling to explicitly document the `exclude` vs `include` states and why greedy falls short.
9. Updated the space complexity of `job_scheduling` to correctly state `O(n) -- DP array + sorted copy` to explicitly account for the memory overhead of doing `sorted(zip(...))` in Python.
10. Added specific takeaways to `tasks/lessons.md` covering python sorting space complexity and the importance of checking backtracking algorithms.

## Completed 01-greedy-basics.md
- Fixed sorting side effects by using `sorted()` instead of `.sort()` to prevent destructive mutations on input arrays. Space complexity updated accordingly.
- Added missing progressive problem: LC 2160 (Minimum Sum of Four Digit Number After Splitting Digits) as a great introductory problem.
- Added inline comments and fixed visual traces.
- Validated all code snippets locally.

## Completed 05-jump-game.md
1. Analyzed `12-greedy/05-jump-game.md` for errors, improvements in explanations, correctness, and code readability
2. Extracted all Python 3 code blocks and thoroughly tested them in `test_jump_game.py`.
3. Fixed a logical flaw in `can_cross` (Frog Jump LC 403). Added the explicit requirement check for the first jump (`if stones[1] != 1: return False`) and adjusted the initial DP state properly, iterating from index 1.
4. Refined the Python code snippets (typing, edge cases, removed trailing whitespace).
5. Addressed edge case definitions and handling. For LC 1696 (Jump Game VI), checked array initialization logic to clearly reflect DP principles.
6. Improved formatting and style of explanations.
7. Expanded clarification in `can_reach` on array modification requirements vs. utilizing a standard `visited` set for strict interview rules.

## Completed 08-partition-labels.md
1. Analyzed `12-greedy/08-partition-labels.md` for errors, improvements in explanations, correctness, and code readability
2. Refined the Python code snippets (typing, edge cases, naming)
3. Verified complexity analysis and visual trace
4. Enhanced explanation of why "Merge Intervals" is not explicitly needed
5. Expanded and reviewed the practice problems (maybe add related array/interval problems)
6. Reviewed chapter summary as this is the last file in the chapter
7. Documented results in this file
8. Updated `tasks/lessons.md` if any lessons are learned

### Review Results:
- Fixed a bug in `partition_labels_via_merge`: the overlap condition was `<` instead of `<=`, which technically works but in standard intervals `[0,2]` and `[2,4]` do overlap at `2`. Wait, in indices, index 2 overlaps with index 2, so `<=` is the strictly correct merge interval logic for this problem.
- Added type hints and standard empty string handling in code snippets.
- Reworded constraints to specify that string `s` consists of lowercase English letters.
- Clarified "Merge Intervals" explanation (string itself is the pre-sorted list of start times).
- Expanded practice problems with `Divide Intervals Into Minimum Number of Groups` (LC 2406).
- Checked the visual trace and complexity analysis; they are correct.
- Added minor micro-optimization clarifications in Common Mistakes.

## Completed 06-gas-station.md
1. Improved `can_complete_circuit_v2` with a comment clarifying baseline tank logic.
2. Fixed a logical error in `min_refuel_stops` where `if fuel >= target: break` was missing, which could lead to an unnecessary `-1` return when the heap was empty but the target was already reached.
3. Added the "Destroying Asteroids (LC 2126)" problem to the Practice Problems to show a greedy accumulation problem.
4. Expanded readability and clarified the implicit boundaries assumption (`n >= 1`).

## Completed 07-candy-distribution.md
1. Improved code correctness for Circular arrangement by refactoring the O(n^2) approach to an O(n) version using circular array unrolling.
2. Verified and updated table for the time/space complexities respectively.
3. Added another progressive practice problem Minimum Deletions to Make Character Frequencies Unique.
4. Ensured markdown logic formatting was sound and readable.