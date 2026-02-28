# Word Search

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md), grid traversal concepts

## Core Concept

Word Search applies backtracking to **grid-based path finding**. Given a 2D grid of characters and a target word, you determine if the word can be formed by sequentially adjacent cells. This pattern is fundamental for any problem involving exploring paths through a grid, emphasizing **in-place matrix state mutation**, bounding box early termination, and recursive depth management.

## Intuition & Mental Models

**Why does DFS with visited-marking work?**

Think of it as exploring a maze where you need to find a specific sequence of checkpoints.

1. **The Trail-Blazing Model (Level)**: Imagine you're in a letter forest. You need to spell a word by stepping on letters in sequence. You can't step on the same spot twice in one path, and you can only move to adjacent tiles (up/down/left/right). The index of the character we're trying to match acts as our depth/level.

2. **Suffix Selection (Choices)**: At each cell, our choices are the four valid adjacent neighbors. We iterate through each neighbor and try to match the next character in the word.

3. **State Mutation & Restoration**: To prevent cycles in the current path, we temporarily mark the current cell as "visited" by mutating it to a non-letter (e.g., `#`). But after exploring one path, we restore it to its original character so other paths can use that cell. This is the essence of grid backtracking.

4. **Early Termination (Pruning)**: Check for character mismatch before recursing. If `board[r][c] != word[index]`, return `False` immediately—don't waste time exploring neighbors.

## Visualizations

### Decision Tree and Grid Path Exploration

```text
Grid:           Word: "ABCCED"
A B C E
S F C S
A D E E

Starting at A(0,0), looking for "ABCCED":
(0,0)A → mark as '#', need "BCCED"
  ↓
(0,1)B → mark as '#', need "CCED"
  ↓
(0,2)C → mark as '#', need "CED"
  ↓
(1,2)C → mark as '#', need "ED"
  ↓
(2,2)E → mark as '#', need "D"
  ↓
(2,1)D → mark as '#', need "" ← Empty! Found it!

Path: A(0,0) → B(0,1) → C(0,2) → C(1,2) → E(2,2) → D(2,1)
```

## Basic Implementation: State Mutation and Restoration

Instead of a separate `visited` set, we temporarily mutate the cell to `#`, then restore it. This saves $O(M \times N)$ space and is a common interview optimization.

```python
def exist(board: list[list[str]], word: str) -> bool:
    """
    Check if word exists in the 2D grid using DFS backtracking.
    """
    if not board or not board[0] or not word:
        return False

    rows, cols = len(board), len(board[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

    def dfs(row: int, col: int, index: int) -> bool:
        # Base case: Found all characters
        if index == len(word):
            return True

        # Boundary check and character mismatch pruning
        if (row < 0 or row >= rows or
            col < 0 or col >= cols or
            board[row][col] != word[index]):
            return False

        # 1. Mutate State (Mark as visited in-place)
        temp = board[row][col]
        board[row][col] = '#'

        # 2. Recurse (Explore all 4 directions)
        for dr, dc in directions:
            if dfs(row + dr, col + dc, index + 1):
                return True

        # 3. Restore State (Backtrack: Unmark cell)
        board[row][col] = temp

        return False

    # Try each cell as a starting point
    for r in range(rows):
        for c in range(cols):
            # Start DFS if the first character matches
            if board[r][c] == word[0] and dfs(r, c, 0):
                return True

    return False
```

## Optimized Implementation: Early Termination via Character Frequency

We can pre-check if the board contains all the required characters. If the word needs three 'A's and the board only has two, we can instantly return `False`. Furthermore, we can search the word backwards if its last character is rarer than its first character, dramatically pruning the search tree.

```python
def exist_optimized(board: list[list[str]], word: str) -> bool:
    """
    Optimized Word Search with character frequency checking and reversed search.
    """
    from collections import Counter

    # Count characters in board
    board_count = Counter()
    for row in board:
        board_count.update(row)

    # Fast failure: check if word characters exist in board
    word_count = Counter(word)
    for char, count in word_count.items():
        if board_count[char] < count:
            return False

    # Optimization: if last char is rarer than first, search backwards!
    # This prevents expanding a massive tree if the start of the word is extremely common.
    if board_count[word[0]] > board_count[word[-1]]:
        word = word[::-1]

    rows, cols = len(board), len(board[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def dfs(row: int, col: int, index: int) -> bool:
        if index == len(word):
            return True

        if (row < 0 or row >= rows or
            col < 0 or col >= cols or
            board[row][col] != word[index]):
            return False

        # 1. Mutate State
        temp = board[row][col]
        board[row][col] = '#'

        # 2. Recurse
        for dr, dc in directions:
            if dfs(row + dr, col + dc, index + 1):
                return True

        # 3. Restore State
        board[row][col] = temp
        return False

    # Search
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0] and dfs(r, c, 0):
                return True

    return False
```

## Complexity Analysis

- **Time Complexity:** $O(M \times N \times 3^L)$ where $M \times N$ is the size of the board and $L$ is the length of the word. We iterate through every cell on the board ($M \times N$). For each cell, we explore up to 3 directions (we don't go back where we came from, hence 3, not 4) for a maximum depth of $L$.
- **Auxiliary Space:** $O(L)$ for the recursion depth representing the call stack when the path hits the length of the word.
- **Total Space:** $O(1)$ modification space since the 2D grid is mutated **in-place** directly.

## Common Pitfalls

### 1. Forgetting to Restore State (Backtrack)

If you don't reset the grid cell back to its original character, subsequent searches starting from other cells will encounter the `#` marker and fail, leading to an incorrect `False` answer.

```python
# WRONG: forgetting to restore
board[row][col] = '#'
result = dfs(...)
return result

# CORRECT:
board[row][col] = '#'
result = dfs(...)
board[row][col] = temp
return result
```

### 2. Slicing the String (Anti-Pattern)

Many candidates slice the string as they traverse (`word[1:]`). This takes $O(L)$ time per recursive call, worsening the time complexity from $O(3^L)$ to $O(L \cdot 3^L)$. Use an `index` pointer instead.

```python
# WRONG: O(L) operation inside recursion
dfs(row + 1, col, word[1:])

# CORRECT: O(1) index increment
dfs(row + 1, col, index + 1)
```

### 3. Early Termination Short-Circuiting Error

Avoid assigning variables locally for each recursive call if they aren't short-circuited properly. Using `or` ensures we break out the moment `True` is returned.

```python
# WRONG: Continues to explore even if a path is already found
res1 = dfs(row + 1, col, index + 1)
res2 = dfs(row - 1, col, index + 1)
res3 = dfs(row, col + 1, index + 1)
res4 = dfs(row, col - 1, index + 1)
return res1 or res2 or res3 or res4

# CORRECT: Early termination with short-circuiting
for dr, dc in directions:
    if dfs(row + dr, col + dc, index + 1):
        return True
```
