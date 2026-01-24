from typing import List

def numIslands(board: List[List[str]]) -> int:
    if not board:
        return 0

    rows, cols = len(board), len(board[0])
    count = 0

    def dfs(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] == "0":
            return
        board[r][c] = "0"
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "1":
                count += 1
                dfs(r, c)
    return count

def test_num_islands():
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    assert numIslands(grid1) == 1

    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    assert numIslands(grid2) == 3
    print("Number of Islands tests passed!")

if __name__ == "__main__":
    test_num_islands()
