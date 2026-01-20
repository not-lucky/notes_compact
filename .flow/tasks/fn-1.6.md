# fn-1.6 Enhance 12-binary-search chapter (7 files)

## Description
TBD

## Acceptance
- [ ] TBD

## Done summary
- Enhanced all 8 binary-search content files with "Building Intuition" sections explaining WHY each approach works (mental models, analogies, visual traces)
- Added "When NOT to Use" sections to all 8 files with anti-patterns and red flags
- Removed duplicate sections that were consolidated into the new structure
- Files enhanced: binary-search-template, first-last-occurrence, search-rotated-array, find-minimum-rotated, peak-element, search-space, matrix-search, median-two-arrays
- Verification: grep confirms 8 files with "Building Intuition" and 8 files with "When NOT to Use"
## Evidence
- Commits: bebc7e1966f3079cf3471ca013687299b4783bce
- Tests: grep -l 'Building Intuition' *.md | wc -l → 8, grep -l 'When NOT to Use' *.md | wc -l → 8
- PRs: