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

memo2_str = """def min_delete_distance_memo(word1: str, word2: str) -> int:
    \"\"\"
    Finds minimum deletions using Top-Down Memoization.
    Time: O(m * n), Space: O(m * n)
    \"\"\"
    m, n = len(word1), len(word2)
    memo = {}

    def lcs(i: int, j: int) -> int:
        if i == 0 or j == 0:
            return 0
        
        if (i, j) in memo:
            return memo[(i, j)]
            
        if word1[i - 1] == word2[j - 1]:
            memo[(i, j)] = 1 + lcs(i - 1, j - 1)
        else:
            memo[(i, j)] = max(lcs(i - 1, j), lcs(i, j - 1))
            
        return memo[(i, j)]

    return m + n - 2 * lcs(m, n)"""

new_memo2_str = """from functools import lru_cache

def min_delete_distance_memo(word1: str, word2: str) -> int:
    \"\"\"
    Finds minimum deletions using Top-Down Memoization.
    Time: O(m * n), Space: O(m * n)
    \"\"\"
    m, n = len(word1), len(word2)

    @lru_cache(None)
    def lcs(i: int, j: int) -> int:
        if i == 0 or j == 0:
            return 0
            
        if word1[i - 1] == word2[j - 1]:
            return 1 + lcs(i - 1, j - 1)
        else:
            return max(lcs(i - 1, j), lcs(i, j - 1))

    return m + n - 2 * lcs(m, n)"""

if memo2_str in content:
    content = content.replace(memo2_str, new_memo2_str)
    print("Replaced min_delete_distance_memo")

with open('/home/lucky/stuff/notes_fang/09-dynamic-programming/09-edit-distance.md', 'w') as f:
    f.write(content)

