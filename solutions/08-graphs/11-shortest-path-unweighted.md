# Solutions: Shortest Path in Unweighted Graphs

## Practice Problems

| #   | Problem                        | Difficulty | Key Variation   |
| --- | ------------------------------ | ---------- | --------------- |
| 1   | Shortest Path in Binary Matrix | Medium     | 8-directional   |
| 2   | Word Ladder                    | Hard       | Implicit graph  |
| 3   | Minimum Knight Moves           | Medium     | Chess moves     |
| 4   | Open the Lock                  | Medium     | State graph     |
| 5   | Jump Game III                  | Medium     | Can reach index |
| 6   | Nearest Exit from Entrance     | Medium     | Grid BFS        |

---

## 1. Shortest Path in Binary Matrix

### Problem Statement

Find the shortest path from top-left to bottom-right in an `n x n` binary matrix with 8-directional movement.

### Optimal Python Solution

```python
from collections import deque

def shortestPathBinaryMatrix(grid: list[list[int]]) -> int:
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1: return -1
    if n == 1: return 1

    queue = deque([(0, 0, 1)]) # (r, c, dist)
    grid[0][0] = 1 # Mark visited

    while queue:
        r, c, d = queue.popleft()
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    if nr == n - 1 and nc == n - 1: return d + 1
                    grid[nr][nc] = 1
                    queue.append((nr, nc, d + 1))
    return -1
```

### Explanation

- **Algorithm**: BFS is optimal for unweighted graphs.
- **Variation**: Includes diagonals (8 directions).
- **Complexity**: Time O(N²), Space O(N²).

---

## 2. Word Ladder

### Problem Statement

Shortest transformation sequence from `beginWord` to `endWord`.

### Optimal Python Solution

```python
from collections import deque, defaultdict

def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
    word_set = set(wordList)
    if endWord not in word_set: return 0

    adj = defaultdict(list)
    L = len(beginWord)
    for word in wordList:
        for i in range(L):
            adj[word[:i] + "*" + word[i+1:]].append(word)

    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, dist = queue.popleft()
        if word == endWord: return dist

        for i in range(L):
            pattern = word[:i] + "*" + word[i+1:]
            for neighbor in adj[pattern]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
            adj[pattern] = [] # Optimization: prevent re-scanning
    return 0
```

### Explanation

- **Implicit Graph**: Nodes are words, edges exist if words differ by one char.
- **Complexity**: Time O(M²N), Space O(M²N).

---

## 3. Minimum Knight Moves

### Problem Statement

Minimum moves for a knight to reach `(x, y)` from `(0, 0)`.

### Optimal Python Solution

```python
from collections import deque

def minKnightMoves(x: int, y: int) -> int:
    x, y = abs(x), abs(y)
    queue = deque([(0, 0, 0)])
    visited = {(0, 0)}

    while queue:
        r, c, d = queue.popleft()
        if r == x and c == y: return d

        for dr, dc in [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in visited and nr >= -2 and nc >= -2:
                visited.add((nr, nc))
                queue.append((nr, nc, d + 1))
    return -1
```

---

## 4. Open the Lock

### Problem Statement

Minimum turns to unlock from "0000" to `target` avoiding `deadends`.

### Optimal Python Solution

```python
from collections import deque

def openLock(deadends: list[str], target: str) -> int:
    dead = set(deadends)
    if "0000" in dead: return -1
    queue = deque([("0000", 0)])
    visited = {"0000"}

    while queue:
        node, dist = queue.popleft()
        if node == target: return dist

        for i in range(4):
            for d in [-1, 1]:
                digit = (int(node[i]) + d) % 10
                neighbor = node[:i] + str(digit) + node[i+1:]
                if neighbor not in visited and neighbor not in dead:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
    return -1
```

---

## 5. Jump Game III

### Problem Statement

Check if you can reach any index with value 0 starting from `start`.

### Optimal Python Solution

```python
from collections import deque

def canReach(arr: list[int], start: int) -> bool:
    queue = deque([start])
    visited = {start}

    while queue:
        idx = queue.popleft()
        if arr[idx] == 0: return True

        for next_idx in [idx + arr[idx], idx - arr[idx]]:
            if 0 <= next_idx < len(arr) and next_idx not in visited:
                visited.add(next_idx)
                queue.append(next_idx)
    return False
```

---

## 6. Nearest Exit from Entrance

### Problem Statement

Find the shortest path from `entrance` to any exit at the border of a maze.

### Optimal Python Solution

```python
from collections import deque

def nearestExit(maze: list[list[str]], entrance: list[int]) -> int:
    rows, cols = len(maze), len(maze[0])
    queue = deque([(entrance[0], entrance[1], 0)])
    maze[entrance[0]][entrance[1]] = "+" # Mark visited

    while queue:
        r, c, d = queue.popleft()

        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == ".":
                if nr == 0 or nr == rows - 1 or nc == 0 or nc == cols - 1:
                    return d + 1
                maze[nr][nc] = "+"
                queue.append((nr, nc, d + 1))
    return -1
```
