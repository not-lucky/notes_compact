- Added "Building Intuition" section to all 7 union-find files with mental models and visual examples
- Added "When NOT to Use" section to all 7 files documenting anti-patterns and when simpler approaches work
- Enhanced README.md with chapter-level intuition for the "Friendship Groups" mental model
- Total: 694 lines added across 7 files

Why:
- Files were compact and jumped to implementation without explaining WHY the technique works
- Missing guidance on when NOT to use Union-Find (e.g., directed graphs, actual path needed)
- No mental models to help build intuition before code

Verification:
- Ran grep to confirm all 7 files have both new sections
- Verified with git diff: 694 lines added
- All files follow consistent enhanced structure matching other completed chapters
