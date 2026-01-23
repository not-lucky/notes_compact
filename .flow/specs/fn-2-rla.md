# Mirror notes hierarchy to solutions with Python code blocks

## Overview
Recreate the `solutions/` directory as a mirror of the core notes hierarchy. Each markdown file in the notes that contains a "Practice Problems" section will have a corresponding file in the `solutions/` folder. These solution files will contain embedded Python code blocks with problem implementations, including type hints, complexity analysis, and `doctest` examples.

## Scope
- **Input**: Directories `01-17`, `A-C`.
- **Output**: A new `solutions/` directory with mirrored subfolders and `.md` files.
- **Cleanup**: Remove any existing `solutions/` folder before starting.

## Approach
1.  **Wipe & Rebuild**: Delete the existing `solutions/` directory and recreate the skeleton.
2.  **Parser**: Implement a script to parse `## Practice Problems` tables in note files.
3.  **Generator**: For each problem identified, generate a Python solution template using best practices (standard library imports, type hints, docstrings with Time/Space, `doctest`).
4.  **Mirroring**: For each note file `path/to/note.md`, create `solutions/path/to/note.md` containing the generated Python blocks.
5.  **Phased Rollout**: Process notes in batches by topic folder (e.g., Arrays/Strings, then Linked Lists, etc.).

## Quick commands
```bash
# Check mirroring status
find solutions -type f | wc -l

# Run syntax check on all solutions
grep -r "python" solutions | wc -l
```

## Acceptance
- [ ] Existing `solutions/` directory is removed.
- [ ] Folder structure of `solutions/` exactly matches the notes folders (`01-17`, `A-C`).
- [ ] Every note file with a "Practice Problems" table has a mirrored `.md` file in `solutions/`.
- [ ] Each mirrored file contains Python blocks for all problems listed in the source note.
- [ ] Python blocks follow best practices: type hints, Complexity (O-notation), and `doctest`.
- [ ] Valid Python syntax in all generated blocks.

## References
- `02-arrays-strings/03-two-pointers-opposite.md`: Reference for problem table format.
- `A-python-cheatsheet/`: Reference for standard library patterns.
- `SKILL.md`: Best practices for Python solution formatting.
