# BFS Basics

## Practice Problems

### 1. Flood Fill
**Difficulty:** Easy
**Concept:** Basic grid BFS

```python
from collections import deque
from typing import List

def flood_fill(image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
    """
    An image is represented by an m x n integer grid image where image[i][j]
    represents the pixel value of the image.
    Perform a flood fill on the image starting from the pixel (sr, sc).

    >>> flood_fill([[1,1,1],[1,1,0],[1,0,1]], 1, 1, 2)
    [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
    >>> flood_fill([[0,0,0],[0,0,0]], 0, 0, 0)
    [[0, 0, 0], [0, 0, 0]]

    Time: O(M * N)
    Space: O(M * N)
    """
    start_color = image[sr][sc]
    if start_color == color:
        return image

    rows, cols = len(image), len(image[0])
    queue = deque([(sr, sc)])
    image[sr][sc] = color

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == start_color:
                image[nr][nc] = color
                queue.append((nr, nc))

    return image
```

### 2. Shortest Path in Binary Matrix
**Difficulty:** Medium
**Concept:** Shortest path

```python
from collections import deque
from typing import List

def shortest_path_binary_matrix(grid: List[List[int]]) -> int:
    """
    Given an n x n binary grid grid, return the length of the shortest clear path
    in the matrix. If there is no clear path, return -1.
    A clear path in a binary matrix is a path from the top-left cell
    (i.e., (0, 0)) to the bottom-right cell (i.e., (n - 1, n - 1)).

    >>> shortest_path_binary_matrix([[0,1],[1,0]])
    2
    >>> shortest_path_binary_matrix([[0,0,0],[1,1,0],[1,1,0]])
    4
    >>> shortest_path_binary_matrix([[1,0,0],[1,1,0],[1,1,0]])
    -1

    Time: O(N^2)
    Space: O(N^2)
    """
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1

    queue = deque([(0, 0, 1)]) # r, c, length
    visited = {(0, 0)}

    while queue:
        r, c, length = queue.popleft()
        if r == n - 1 and c == n - 1:
            return length

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, length + 1))

    return -1
```

### 3. Rotting Oranges
**Difficulty:** Medium
**Concept:** Multi-source BFS

```python
from collections import deque
from typing import List

def oranges_rotting(grid: List[List[int]]) -> int:
    """
    You are given an m x n grid where each cell can have one of three values:
    0 representing an empty cell,
    1 representing a fresh orange, or
    2 representing a rotten orange.
    Every minute, any fresh orange that is 4-directionally adjacent to a
    rotten orange becomes rotten.
    Return the minimum number of minutes that must elapse until no cell
    has a fresh orange. If this is impossible, return -1.

    >>> oranges_rotting([[2,1,1],[1,1,0],[0,1,1]])
    4
    >>> oranges_rotting([[2,1,1],[0,1,1],[1,0,1]])
    -1
    >>> oranges_rotting([[0,2]])
    0

    Time: O(M * N)
    Space: O(M * N)
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0

    minutes = 0
    while queue:
        r, c, d = queue.popleft()
        minutes = max(minutes, d)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                queue.append((nr, nc, d + 1))

    return minutes if fresh == 0 else -1
```

### 4. Word Ladder
**Difficulty:** Hard
**Concept:** Implicit graph BFS

```python
from collections import deque
from typing import List, Set

def ladder_length(begin_word: str, end_word: str, word_list: List[str]) -> int:
    """
    A transformation sequence from word beginWord to word endWord using a
    dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk.
    Return the number of words in the shortest transformation sequence
    from beginWord to endWord, or 0 if no such sequence exists.

    >>> ladder_length("hit", "cog", ["hot","dot","dog","lot","log","cog"])
    5
    >>> ladder_length("hit", "cog", ["hot","dot","dog","lot","log"])
    0

    Time: O(M^2 * N) where M is word length and N is number of words
    Space: O(M^2 * N)
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    queue = deque([(begin_word, 1)])
    visited = {begin_word}

    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return length

        for i in range(len(word)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                next_word = word[:i] + c + word[i+1:]
                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, length + 1))

    return 0
```
