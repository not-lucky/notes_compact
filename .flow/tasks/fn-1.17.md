# fn-1.17 Enhance 17-system-design chapter (5 files)

## Description
TBD

## Acceptance
- [ ] TBD

## Done summary
## What changed
- Added "Building Intuition" sections to all 5 files with mental models, visual traces, and deep explanations of why each pattern works
- Added "When NOT to Use" sections with anti-patterns, decision matrices, and guidance on when simpler approaches are better
- Added "Complexity Derivation" sections with step-by-step proofs for LRU, LFU, and Rate Limiter
- Expanded eviction strategy explanations in README with detailed breakdowns for each policy

## Why
- The original files jumped directly into implementation without building intuition
- Missing guidance on when NOT to use each pattern led to potential over-engineering
- Complexity claims lacked step-by-step derivations that help learners understand *why* operations are O(1)

## Verification
- Verified all 5 files have "Building Intuition" sections: `grep -rl 'Building Intuition' 17-system-design-basics/` returns 5 files
- Verified all 5 files have "When NOT to Use" sections: `grep -rl 'When NOT to Use' 17-system-design-basics/` returns 5 files
- File sizes increased significantly (from ~5-14KB to 10-20KB) indicating substantial content addition
## Evidence
- Commits: 61360d6312f4f6306048a1dc2292841c422fc11f
- Tests: grep -rl 'Building Intuition' 17-system-design-basics/ | wc -l returns 5, grep -rl 'When NOT to Use' 17-system-design-basics/ | wc -l returns 5
- PRs: