# Letter Combinations of a Phone Number - Solutions

This document provides optimal solutions and detailed explanations for the practice problems related to Letter Combinations.

---

## 1. Letter Combinations of a Phone Number

### Problem Statement
Given a string containing digits from `2-9` inclusive, return all possible letter combinations that the number could represent. Return the answer in any order. A mapping of digit to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.

### Examples & Edge Cases
- **Input:** digits = "23" → **Output:** ["ad","ae","af","bd","be","bf","cd","ce","cf"]
- **Input:** digits = "" → **Output:** []
- **Edge Case:** Digit string containing '7' or '9' (which have 4 letters each).

### Optimal Python Solution (Backtracking)
```python
def letterCombinations(digits: str) -> list[str]:
    if not digits:
        return []

    mapping = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"
    }

    res = []

    def backtrack(index: int, current: list[str]):
        # Base case: we have picked a letter for every digit
        if index == len(digits):
            res.append("".join(current))
            return

        # Get the letters corresponding to the current digit
        letters = mapping[digits[index]]

        for char in letters:
            current.append(char)
            backtrack(index + 1, current)
            current.pop() # Backtrack

    backtrack(0, [])
    return res
```

### Detailed Explanation
1. **Mapping**: We use a hash map to store the fixed mapping of digits to letters.
2. **Backtracking**: We process the digits one by one. For each digit, we try all possible letters it can represent. For each choice, we move to the next digit.
3. **Cartesian Product**: This problem is essentially finding the Cartesian product of the letter sets for each digit.

### Complexity Analysis
- **Time Complexity:** $O(n \cdot 4^n)$ - In the worst case (digits 7 or 9), each digit has 4 choices. $n$ is the number of digits.
- **Space Complexity:** $O(n)$ - The recursion stack depth is equal to the number of digits.

---

## 2. Letter Case Permutation

### Problem Statement
Given a string `s`, we can transform every letter individually to be lowercase or uppercase to create another string. Return a list of all possible strings we could create.

### Optimal Python Solution (Backtracking)
```python
def letterCasePermutation(s: str) -> list[str]:
    res = []

    def backtrack(index: int, current: list[str]):
        if index == len(s):
            res.append("".join(current))
            return

        char = s[index]
        if char.isalpha():
            # Try lowercase
            current.append(char.lower())
            backtrack(index + 1, current)
            current.pop()

            # Try uppercase
            current.append(char.upper())
            backtrack(index + 1, current)
            current.pop()
        else:
            # If digit, just move on
            current.append(char)
            backtrack(index + 1, current)
            current.pop()

    backtrack(0, [])
    return res
```

---

## 3. Generate All Binary Strings

### Problem Statement
Given an integer `n`, generate all binary strings of length `n`.

### Optimal Python Solution (Backtracking)
```python
def generateBinaryStrings(n: int) -> list[str]:
    res = []

    def backtrack(current: list[str]):
        if len(current) == n:
            res.append("".join(current))
            return

        for bit in ["0", "1"]:
            current.append(bit)
            backtrack(current)
            current.pop()

    backtrack([])
    return res
```

---

## 4. All Paths from Source to Target

### Problem Statement
Given a directed acyclic graph (DAG) of `n` nodes labeled from `0` to `n - 1`, find all possible paths from node `0` to node `n - 1` and return them in any order.

### Optimal Python Solution (DFS Backtracking)
```python
def allPathsSourceTarget(graph: list[list[int]]) -> list[list[int]]:
    target = len(graph) - 1
    res = []

    def backtrack(curr_node: int, path: list[int]):
        if curr_node == target:
            res.append(path[:])
            return

        for neighbor in graph[curr_node]:
            path.append(neighbor)
            backtrack(neighbor, path)
            path.pop()

    backtrack(0, [0])
    return res
```

### Detailed Explanation
1. **DFS**: Since the graph is a DAG, we can use simple DFS without worrying about cycles.
2. **Backtracking**: We start at node 0, and for each neighbor, we add it to our path and recurse. After exploring all paths through a neighbor, we remove it from the path to explore other branches.
