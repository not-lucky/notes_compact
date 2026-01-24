from collections import deque

def shortest_path_binary_maze(grid: list[list[int]]) -> int:
    """
    Find the shortest path in a binary maze (0 is open, 1 is blocked).
    From top-left to bottom-right.
    Pattern: BFS
    Time: O(R * C)
    Space: O(R * C)
    """
    if not grid or not grid[0] or grid[0][0] == 1:
        return -1

    rows, cols = len(grid), len(grid[0])
    if rows == 1 and cols == 1:
        return 0

    queue = deque([(0, 0, 0)])  # (row, col, distance)
    visited = {(0, 0)}

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        r, c, dist = queue.popleft()

        if r == rows - 1 and c == cols - 1:
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))

    return -1

if __name__ == "__main__":
    # Test cases
    grid1 = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    assert shortest_path_binary_maze(grid1) == 4

    grid2 = [
        [0, 1],
        [1, 0]
    ]
    assert shortest_path_binary_maze(grid2) == -1
    print("All tests passed!")
