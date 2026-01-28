# Solutions: BFS Basics

## Practice Problems

| #   | Problem                        | Difficulty | Key Pattern         |
| --- | ------------------------------ | ---------- | ------------------- |
| 1   | Flood Fill                     | Easy       | Basic grid BFS      |
| 2   | Number of Islands              | Medium     | Multi-component BFS |
| 3   | Shortest Path in Binary Matrix | Medium     | Shortest path       |
| 4   | Rotting Oranges                | Medium     | Multi-source BFS    |
| 5   | Word Ladder                    | Hard       | Implicit graph BFS  |
| 6   | 01 Matrix                      | Medium     | Multi-source BFS    |

---

## 1. Flood Fill

### Problem Statement

An image is represented by an `m x n` integer grid `image` where `image[i][j]` represents the pixel value of the image. You are also given three integers `sr`, `sc`, and `color`. You should perform a flood fill on the image starting from the pixel `image[sr][sc]`.

To perform a flood fill, consider the starting pixel, plus any pixels connected 4-directionally to the starting pixel of the same color as the starting pixel, plus any pixels connected 4-directionally to those pixels (also with the same color), and so on. Replace the color of all of the aforementioned pixels with `color`.

### Examples & Edge Cases

- **Example 1**: `image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2` -> `[[2,2,2],[2,2,0],[2,0,1]]`
- **Edge Cases**:
  - `newColor` is the same as the original color: Return the image as is to avoid infinite loops.
  - Grid with a single pixel.
  - Starting pixel at the boundary.

### Optimal Python Solution

```python
from collections import deque

def floodFill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    start_color = image[sr][sc]

    # If the starting pixel already has the target color, no fill needed
    if start_color == color:
        return image

    rows, cols = len(image), len(image[0])
    queue = deque([(sr, sc)])
    image[sr][sc] = color # Mark visited by changing color

    while queue:
        r, c = queue.popleft()

        # Check 4-directional neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # If neighbor is within bounds and has the original color
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == start_color:
                image[nr][nc] = color
                queue.append((nr, nc))

    return image
```

### Explanation

1. **Starting Point**: We identify the `start_color` at `(sr, sc)`.
2. **Avoid Redundancy**: If `start_color` is already the target `color`, we exit immediately.
3. **BFS Traversal**: We use a queue to explore all adjacent pixels of the same color.
4. **Marking Visited**: By updating the pixel to the new `color` as soon as it's added to the queue, we prevent it from being processed multiple times.

### Complexity Analysis

- **Time Complexity**: **O(M × N)**. In the worst case, we visit every pixel in the grid.
- **Space Complexity**: **O(M × N)**. The queue can store up to O(M × N) pixels in the worst case.

---

## 2. Number of Islands (BFS Focus)

### Problem Statement

Given an `m x n` 2D binary grid `grid` which represents a map of '1's (land) and '0's (water), return the number of islands.

### Examples & Edge Cases

- **Example 1**: `grid = [["1","1","0"],["1","1","0"],["0","0","1"]]` -> Output: 2
- **Edge Cases**: Empty grid, grid with no land, grid with no water.

### Optimal Python Solution

```python
from collections import deque

def numIslands(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    islands = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                islands += 1
                # BFS to sink the entire island
                queue = deque([(r, c)])
                grid[r][c] = "0" # Mark visited

                while queue:
                    curr_r, curr_c = queue.popleft()
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                            grid[nr][nc] = "0"
                            queue.append((nr, nc))

    return islands
```

### Explanation

1. **Iterate Grid**: We scan the grid cell by cell.
2. **Found Land**: When we find a "1", we increment our island count and start a BFS.
3. **BFS Sinking**: The BFS finds all connected land and "sinks" it by changing "1" to "0". This ensures we don't count the same island twice.
4. **BFS vs DFS**: For very large grids, BFS is often preferred in Python to avoid reaching the recursion depth limit.

### Complexity Analysis

- **Time Complexity**: **O(M × N)**. Each cell is visited at most twice (once by the main loop and once by BFS).
- **Space Complexity**: **O(min(M, N))**. The queue size is bounded by the perimeter of the largest island, which is at most O(min(M, N)).

---

## 3. Shortest Path in Binary Matrix

### Problem Statement

Given an `n x n` binary matrix `grid`, return the length of the shortest clear path from the top-left corner `(0, 0)` to the bottom-right corner `(n - 1, n - 1)`. If no such path exists, return -1. A clear path is a path where every visited cell is 0 and includes 8-directional connections.

### Examples & Edge Cases

- **Example 1**: `grid = [[0,1],[1,0]]` -> Output: 2
- **Example 2**: `grid = [[0,0,0],[1,1,0],[1,1,0]]` -> Output: 4
- **Edge Cases**:
  - Start or end cell is 1: Return -1.
  - `n = 1` and `grid[0][0] = 0`: Return 1.

### Optimal Python Solution

```python
from collections import deque

def shortestPathBinaryMatrix(grid: list[list[int]]) -> int:
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1

    if n == 1:
        return 1

    queue = deque([(0, 0, 1)]) # (row, col, distance)
    grid[0][0] = 1 # Mark visited by modifying the grid

    # 8 directions
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    while queue:
        r, c, dist = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                if nr == n - 1 and nc == n - 1:
                    return dist + 1
                grid[nr][nc] = 1 # Mark visited
                queue.append((nr, nc, dist + 1))

    return -1
```

### Explanation

1. **Shortest Path = BFS**: Since all edges have equal weight (1), BFS is guaranteed to find the shortest path.
2. **8-Directions**: We define all possible movements, including diagonals.
3. **Early Exit**: As soon as we reach the bottom-right corner, we return the current distance + 1.
4. **Visited Tracking**: We mark cells as `1` in the grid to avoid using extra space for a `visited` set.

### Complexity Analysis

- **Time Complexity**: **O(N²)**. We visit each cell at most once.
- **Space Complexity**: **O(N²)**. In the worst case, the queue can hold many cells.

---

## 4. Rotting Oranges

### Problem Statement

You are given an `m x n` grid where each cell can have one of three values:

- `0`: empty cell
- `1`: fresh orange
- `2`: rotten orange

Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten. Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.

### Examples & Edge Cases

- **Example 1**: `grid = [[2,1,1],[1,1,0],[0,1,1]]` -> Output: 4
- **Edge Cases**: No fresh oranges (return 0), no rotten oranges (return -1 if fresh exist), unreachable fresh oranges.

### Optimal Python Solution

```python
from collections import deque

def orangesRotting(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh_count = 0

    # 1. Initialize: Find all rotten oranges and count fresh ones
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh_count += 1

    if fresh_count == 0:
        return 0

    minutes = -1

    # 2. Multi-source BFS
    while queue:
        minutes += 1
        # Process oranges at the current "minute" level
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh_count -= 1
                    queue.append((nr, nc))

    return minutes if fresh_count == 0 else -1
```

### Explanation

1. **Multi-source BFS**: All rotten oranges start rotting their neighbors simultaneously. We add all initial rotten oranges to the queue at distance 0.
2. **Level Tracking**: We use `len(queue)` to process oranges minute by minute.
3. **Fresh Counter**: We keep track of the remaining fresh oranges to easily check if all oranges have rotted at the end.
4. **Impossible Scenario**: If the queue is empty but `fresh_count > 0`, some oranges are unreachable.

### Complexity Analysis

- **Time Complexity**: **O(M × N)**. Every cell is visited at most once.
- **Space Complexity**: **O(M × N)**. The queue size in the worst case.

---

## 5. Word Ladder

### Problem Statement

Given two words, `beginWord` and `endWord`, and a dictionary `wordList`, return the number of words in the shortest transformation sequence from `beginWord` to `endWord`. If no such sequence exists, return 0.

- Every adjacent word in the sequence must differ by exactly one letter.
- Every intermediate word must be in the `wordList`.

### Examples & Edge Cases

- **Example 1**: `beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]` -> Output: 5
- **Edge Cases**: `endWord` not in `wordList` (return 0), no path exists.

### Optimal Python Solution

```python
from collections import deque, defaultdict

def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
    if endWord not in wordList:
        return 0

    # Pre-process: Map patterns to words
    # e.g., "h*t" -> ["hit", "hot"]
    L = len(beginWord)
    all_combo_dict = defaultdict(list)
    for word in wordList:
        for i in range(L):
            all_combo_dict[word[:i] + "*" + word[i+1:]].append(word)

    # BFS
    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        current_word, level = queue.popleft()

        for i in range(L):
            # Intermediate pattern for current word
            pattern = current_word[:i] + "*" + current_word[i+1:]

            # Neighbors for this pattern
            for neighbor in all_combo_dict[pattern]:
                if neighbor == endWord:
                    return level + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, level + 1))

            # Optimization: Clear the pattern list to avoid redundant checks
            all_combo_dict[pattern] = []

    return 0
```

### Explanation

1. **Implicit Graph**: Words are nodes, and an edge exists between words that differ by one letter.
2. **Preprocessing Patterns**: Instead of comparing every word against every other word (O(N²)), we create patterns like `h*t`. This allows us to find neighbors in O(L) time.
3. **BFS**: Standard BFS to find the shortest path in an unweighted graph.
4. **Efficiency**: Clearing the `all_combo_dict[pattern]` after visiting neighbors is a common optimization to speed up the search.

### Complexity Analysis

- **Time Complexity**: **O(M² × N)**. M is the length of each word, N is the number of words. Preprocessing takes O(M²N) and BFS takes O(M²N).
- **Space Complexity**: **O(M² × N)**. To store the dictionary of patterns.

---

## 6. 01 Matrix

### Problem Statement

Given an `m x n` binary matrix `mat`, return the distance of the nearest `0` for each cell. The distance between two adjacent cells is 1.

### Examples & Edge Cases

- **Example 1**: `mat = [[0,0,0],[0,1,0],[0,0,0]]` -> Output: `[[0,0,0],[0,1,0],[0,0,0]]`
- **Example 2**: `mat = [[0,0,0],[0,1,0],[1,1,1]]` -> Output: `[[0,0,0],[0,1,0],[1,2,1]]`

### Optimal Python Solution

```python
from collections import deque

def updateMatrix(mat: list[list[int]]) -> list[list[int]]:
    rows, cols = len(mat), len(mat[0])
    queue = deque()

    # 1. Initialize: Add all 0s to queue and set 1s to infinity
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                queue.append((r, c))
            else:
                mat[r][c] = float('inf')

    # 2. Multi-source BFS
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # If neighbor is within bounds and can be updated with a shorter distance
            if 0 <= nr < rows and 0 <= nc < cols and mat[nr][nc] > mat[r][c] + 1:
                mat[nr][nc] = mat[r][c] + 1
                queue.append((nr, nc))

    return mat
```

### Explanation

1. **Multi-source BFS**: We treat all `0`s as starting sources.
2. **Distance Initialization**: We set the distance of `0`s to 0 and all `1`s to infinity.
3. **Propagation**: The BFS propagates from the `0`s outward. When we visit a neighbor, we check if the current path `mat[r][c] + 1` is shorter than its existing value.
4. **Efficiency**: By updating neighbors only if we find a shorter distance, we naturally explore only the necessary paths.

### Complexity Analysis

- **Time Complexity**: **O(M × N)**. Every cell is visited once.
- **Space Complexity**: **O(M × N)**. For the BFS queue.
