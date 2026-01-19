# fn-1.16 Create Chapter 14: Union-Find / Disjoint Set (5-6 files)

## Description
Create Chapter 14: Union-Find with 5-6 files:

## Files:
1. **README.md** - Union-Find interview patterns
2. **01-union-find-basics.md** - Basic implementation, find and union
3. **02-path-compression.md** - Optimization with path compression
4. **03-union-by-rank.md** - Union by rank/size
5. **04-connected-components.md** - Count connected components
6. **05-accounts-merge.md** - Accounts merge problem
7. **06-redundant-connection.md** - Find redundant connection (cycle)
## Acceptance
- [ ] Union-Find implementation
- [ ] Path compression optimization
- [ ] Union by rank optimization
- [ ] Classic application problems
- [ ] 5-6 markdown files created
## Done summary
## What changed
- Created comprehensive README.md with Union-Find overview, patterns, and interview context
- Added 01-union-find-basics.md covering basic implementation and Number of Provinces problem
- Added 02-path-compression.md with recursive/iterative compression techniques
- Added 03-union-by-rank.md with rank and size-based union strategies
- Added 04-connected-components.md with dynamic connectivity patterns
- Added 05-accounts-merge.md with string-to-index mapping patterns
- Added 06-redundant-connection.md with cycle detection and MST applications

## Why
- Complete Union-Find / Disjoint Set chapter for interview preparation
- Follows established chapter format with interview context, visualizations, and problems

## Verification
- All 7 markdown files created in 14-union-find/
- Quick commands verified structure (file counts match expected)
- Cross-chapter links validated
## Evidence
- Commits: 288645eaff9e7341a12a33f68014acfe253ef4e8
- Tests: find . -name 'README.md' | wc -l, for dir in */; do echo "$dir: $(find "$dir" -name '*.md' | wc -l)"; done
- PRs: