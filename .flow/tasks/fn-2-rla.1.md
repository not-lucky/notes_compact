# fn-2-rla.1 Wipe and Mirror Directory Structure

## Description
Remove the existing `solutions/` folder and recreate the base directory structure mirroring the notes.

**Size:** S
**Files:** `solutions/` (root)

## Approach
- Delete `solutions/` directory if it exists.
- List all top-level directories (01-17, A, B, C).
- Create corresponding empty directories under `solutions/`.
## Acceptance
- [x] `solutions/` folder is fresh.
- [x] Subdirectories `01` through `17` and `A`, `B`, `C` exist in `solutions/`.
- [x] `ls solutions/` shows folders 01-17, A, B, C.
## Done summary
Wiped the old `solutions/` directory and recreated the base structure (01-17, A, B, C) as specified. Added `.gitkeep` files to ensure empty directories are tracked.

## Evidence
- Commits: `feat(solutions): reset directory structure to mirror notes hierarchy`
- Tests: Manual verification with `ls -F solutions/`
- PRs: N/A
