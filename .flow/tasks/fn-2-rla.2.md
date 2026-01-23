# fn-2-rla.2 Implement Mirroring for Folders 01-05

## Description
Process note files in folders `01` to `05`. For each file, parse the "Practice Problems" table and create a mirrored solution file.

**Size:** M
**Files:** `solutions/01-*` to `solutions/05-*`

## Approach
- Iterate through each `.md` file in the specified folders.
- Search for the `## Practice Problems` header.
- Extract problem names from the table.
- Generate a Python code block for each problem.
- Write a new `.md` file in `solutions/` with these blocks.
## Acceptance
- [ ] Solutions for Complexity Analysis, Arrays/Strings, Hashmaps/Sets, Linked Lists, and Stacks/Queues are created.
- [ ] Each file contains Python code blocks with type hints and docstrings.
- [ ] `solutions/02-arrays-strings/03-two-pointers-opposite.md` contains a Python solution for "Two Sum II".
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
