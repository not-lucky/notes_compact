# fn-1.12 Enhance 13-sorting chapter (6 files)

## Description
TBD

## Acceptance
- [ ] TBD

## Done summary
- Added "Building Intuition" sections to all 6 files in 13-tries chapter
- Added "When NOT to Use" sections with anti-patterns and red flags
- Enhanced README with core concepts (shared prefixes, O(L) guarantee, mental models)
- Each topic file explains WHY the approach works before diving into code

Why:
- Original files jumped into patterns too quickly without explaining intuition
- Missing guidance on when NOT to use tries (memory concerns, exact-match-only cases)

Verification:
- All 6 files confirmed to have "Building Intuition" and "When NOT to Use" sections
- grep -rl counts verified: 6/6 for both sections
## Evidence
- Commits: c0fe7db5da14c62876d72a73d715cac849d6b179
- Tests: grep verification
- PRs: