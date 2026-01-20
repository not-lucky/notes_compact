# fn-1.11 Enhance 10-greedy chapter (6 files)

## Description
TBD

## Acceptance
- [ ] TBD

## Done summary
## Done Summary

### What changed
- Added "Building Intuition" section to all 8 files in 12-greedy chapter
- Added "When NOT to Use" section with anti-patterns and red flags to all 8 files
- Included mental models, visual examples, and counter-examples throughout

### Why
- Epic requires deep explanations before code
- Files were missing intuition-building content and anti-pattern guidance
- Consistent with the enhanced structure used in other chapters (07-heaps, 10-binary-search, etc.)

### Verification
- All 8 content files now contain "Building Intuition" section (verified with grep)
- All 8 content files now contain "When NOT to Use" section (verified with grep)
- Changes reviewed manually for quality and consistency

### Files modified
1. 01-greedy-basics.md
2. 02-interval-scheduling.md
3. 03-merge-intervals.md
4. 04-meeting-rooms.md
5. 05-jump-game.md
6. 06-gas-station.md
7. 07-candy-distribution.md
8. 08-partition-labels.md
## Evidence
- Commits: bb2f8d91d116dfe5dd07cd5b200099e94157d215
- Tests: grep 'Building Intuition' verified all 8 files, grep 'When NOT to Use' verified all 8 files
- PRs: