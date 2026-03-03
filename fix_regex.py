import re

def test_memo_regex(s, p):
    memo = {}

    def dfs(i: int, j: int) -> bool:
        """Returns True if suffix s[i:] matches suffix p[j:]"""
        if (i, j) in memo:
            return memo[(i, j)]

        # Base Cases
        if j == len(p):
            return i == len(s) # True if both exhausted

        # Check if the current characters match
        first_match = i < len(s) and (s[i] == p[j] or p[j] == '.')

        # If the NEXT character in the pattern is a '*'
        if j + 1 < len(p) and p[j+1] == '*':
            # Branch 1: Match 0 times (skip the 'x*' in pattern, move j+2)
            # Branch 2: Match 1+ times (first_match must be true, consume s[i], keep pattern at j)
            ans = dfs(i, j + 2) or (first_match and dfs(i + 1, j))
        else:
            # Normal character match
            ans = first_match and dfs(i + 1, j + 1)

        memo[(i, j)] = ans
        return ans

    return dfs(0, 0)

print(test_memo_regex("aa", "a"))
print(test_memo_regex("aa", "a*"))
print(test_memo_regex("ab", ".*"))

def test_memo_wildcard(s, p):
    memo = {}

    def dfs(i: int, j: int) -> bool:
        if (i, j) in memo:
            return memo[(i, j)]

        # Base Cases
        if j == len(p):
            return i == len(s)
        if i == len(s):
            # If string is empty, pattern can only match if it's all '*'
            return all(char == '*' for char in p[j:])

        # Transitions
        match = s[i] == p[j] or p[j] == '?'

        if p[j] == '*':
            # Branch 1: Match zero characters (move pattern pointer j + 1)
            # Branch 2: Match one character (move string pointer i + 1, keep *)
            ans = dfs(i, j + 1) or dfs(i + 1, j)
        else:
            ans = match and dfs(i + 1, j + 1)

        memo[(i, j)] = ans
        return ans

    return dfs(0, 0)

print(test_memo_wildcard("aa", "a"))
print(test_memo_wildcard("aa", "*"))
print(test_memo_wildcard("cb", "?a"))
