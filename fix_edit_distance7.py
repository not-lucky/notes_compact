import re

with open('/home/lucky/stuff/notes_fang/09-dynamic-programming/09-edit-distance.md', 'r') as f:
    content = f.read()

memo_str = """def min_distance_memo(word1: str, word2: str) -> int:
    \"\"\"
    Top-Down Memoization approach for Edit Distance.

    Time: O(m * n)
    Space: O(m * n) for memoization dictionary and recursion stack
    \"\"\"
    m, n = len(word1), len(word2)
    memo = {}

    def dfs(i: int, j: int) -> int:
        # Base cases: if one string is empty, operation count is the length of the other
        if i == 0: return j  # Need j insertions
        if j == 0: return i  # Need i deletions

        if (i, j) in memo:
            return memo[(i, j)]

        # If characters match, no operations needed for this position
        if word1[i - 1] == word2[j - 1]:
            memo[(i, j)] = dfs(i - 1, j - 1)
        else:
            # If they don't match, try all 3 operations and find the minimum
            memo[(i, j)] = 1 + min(
                dfs(i - 1, j),      # Delete from word1
                dfs(i, j - 1),      # Insert into word1
                dfs(i - 1, j - 1)   # Replace in word1
            )

        return memo[(i, j)]

    return dfs(m, n)"""

new_memo_str = """from functools import lru_cache

def min_distance_memo(word1: str, word2: str) -> int:
    \"\"\"
    Top-Down Memoization approach for Edit Distance.

    Time: O(m * n)
    Space: O(m * n) for memoization and recursion stack
    \"\"\"
    m, n = len(word1), len(word2)

    @lru_cache(None)
    def dfs(i: int, j: int) -> int:
        # Base cases: if one string is empty, operation count is the length of the other
        if i == 0: return j  # Need j insertions
        if j == 0: return i  # Need i deletions

        # If characters match, no operations needed for this position
        if word1[i - 1] == word2[j - 1]:
            return dfs(i - 1, j - 1)
        
        # If they don't match, try all 3 operations and find the minimum
        return 1 + min(
            dfs(i - 1, j),      # Delete from word1
            dfs(i, j - 1),      # Insert into word1
            dfs(i - 1, j - 1)   # Replace in word1
        )

    return dfs(m, n)"""

if memo_str in content:
    content = content.replace(memo_str, new_memo_str)
    print("Replaced min_distance_memo")

with open('/home/lucky/stuff/notes_fang/09-dynamic-programming/09-edit-distance.md', 'w') as f:
    f.write(content)

