# Overall 12-Greedy Refactoring Task Plan
- [x] Refactor README.md
- [x] Refactor 03-merge-intervals.md
- [x] Refactor 02-interval-scheduling.md
- [x] Refactor 08-partition-labels.md
- [x] Refactor 05-jump-game.md
- [ ] Refactor 01-greedy-basics.md
- [x] Refactor 04-meeting-rooms.md
- [x] Refactor 06-gas-station.md
- [x] Refactor 07-candy-distribution.md

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