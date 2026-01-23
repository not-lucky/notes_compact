# Shortest Path in Unweighted Graphs

## Practice Problems

### 1. Shortest Path in Binary Matrix
**Difficulty:** Medium
**Concept:** 8-directional

```python
from collections import deque
from typing import List

def shortest_path_binary_matrix(grid: List[List[int]]) -> int:
    """
    Given an n x n binary grid grid, return the length of the shortest clear path
    in the matrix. If there is no clear path, return -1.

    >>> shortest_path_binary_matrix([[0,1],[1,0]])
    2
    >>> shortest_path_binary_matrix([[0,0,0],[1,1,0],[1,1,0]])
    4

    Time: O(N^2)
    Space: O(N^2)
    """
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1

    queue = deque([(0, 0, 1)]) # r, c, dist
    visited = {(0, 0)}

    while queue:
        r, c, d = queue.popleft()
        if r == n - 1 and c == n - 1:
            return d

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, d + 1))

    return -1
```

### 2. Word Ladder
**Difficulty:** Hard
**Concept:** Implicit graph

```python
from collections import deque
from typing import List

def ladder_length(begin_word: str, end_word: str, word_list: List[str]) -> int:
    """
    Find the length of the shortest transformation sequence.

    >>> ladder_length("hit", "cog", ["hot","dot","dog","lot","log","cog"])
    5

    Time: O(M^2 * N)
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

### 3. Open the Lock
**Difficulty:** Medium
**Concept:** State graph

```python
from collections import deque
from typing import List

def open_lock(deadends: List[str], target: str) -> int:
    """
    Minimum number of turns to open the lock.

    >>> open_lock(["0201","0101","0102","1212","2002"], "0202")
    6

    Time: O(10^4 * 4 * 2)
    Space: O(10^4)
    """
    dead = set(deadends)
    if "0000" in dead:
        return -1

    queue = deque([("0000", 0)])
    visited = {"0000"}

    while queue:
        s, d = queue.popleft()
        if s == target:
            return d

        for i in range(4):
            digit = int(s[i])
            for move in [-1, 1]:
                new_digit = (digit + move) % 10
                new_s = s[:i] + str(new_digit) + s[i+1:]
                if new_s not in dead and new_s not in visited:
                    visited.add(new_s)
                    queue.append((new_s, d + 1))

    return -1
```
