# fn-1.9 Create Chapter 07: Heaps & Priority Queues (8-10 files)

## Description
Create Chapter 07: Heaps & Priority Queues with 8-10 files:

## Files:
1. **README.md** - Heap interview patterns
2. **01-heap-basics.md** - Heap property, heapify, push/pop
3. **02-python-heapq.md** - Using Python's heapq module
4. **03-top-k-pattern.md** - Top K largest/smallest elements
5. **04-kth-largest-element.md** - Find kth largest, quick select
6. **05-merge-k-sorted.md** - Merge K sorted lists/arrays
7. **06-median-stream.md** - Find median from data stream
8. **07-task-scheduler.md** - Task scheduling with cooldown
9. **08-k-closest-points.md** - K closest points to origin
## Acceptance
- [ ] Heap fundamentals covered
- [ ] Python heapq usage explained
- [ ] Top-K pattern with variations
- [ ] Merge K sorted pattern
- [ ] Median from stream (two heaps)
- [ ] 8-10 markdown files created
## Done summary
## Done Summary

**What changed:**
- Created 9 markdown files for Chapter 07: Heaps & Priority Queues
- Covered heap fundamentals, Python heapq module, and 6 common interview patterns
- Included code examples, complexity analysis, and practice problems for each section

**Why:**
- Heaps are essential for efficiency-focused FANG+ interview questions
- Patterns like Top-K, merge K sorted, and two-heap median are frequently tested
- Content follows established chapter structure with interview context

**Verification:**
- 9 files created (README + 8 sections)
- Cross-chapter links validated
- Quick commands verified file structure
## Evidence
- Commits: 7641c4ad353b897bea4e5ef61ec65ae2cfd15ca0
- Tests: find . -name 'README.md' | wc -l, for dir in */; do echo "$dir: $(find "$dir" -name '*.md' | wc -l)"; done
- PRs: