# Practice Problems: Accounts Merge

## Problem 1: Accounts Merge
**LeetCode 721**

### Problem Statement
Given a list of `accounts` where each element `accounts[i]` is a list of strings, where the first element `accounts[i][0]` is a name, and the rest of the elements are emails representing emails of the account.

Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common email to both accounts. Note that even if two accounts have the same name, they may belong to different people as people could have the same name. A person can have any number of accounts initially, but all of their accounts definitely have the same name.

After merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails in **sorted order**. The accounts themselves can be returned in any order.

### Constraints
- `1 <= accounts.length <= 1000`
- `2 <= accounts[i].length <= 10`
- `1 <= accounts[i][j].length <= 30`
- `accounts[i][0]` consists of English letters.
- `accounts[i][j]` (for `j > 0`) is a valid email.

### Example
**Input:** `accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]`
**Output:** `[["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]`

### Python Implementation
```python
import collections

class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y

def accountsMerge(accounts: list[list[str]]) -> list[list[str]]:
    uf = UnionFind()
    email_to_name = {}

    for account in accounts:
        name = account[0]
        first_email = account[1]
        for email in account[1:]:
            email_to_name[email] = name
            uf.union(first_email, email)

    groups = collections.defaultdict(list)
    for email in email_to_name:
        groups[uf.find(email)].append(email)

    res = []
    for root in groups:
        res.append([email_to_name[root]] + sorted(groups[root]))

    return res
```

---

## Problem 2: Similar String Groups
**LeetCode 839**

### Problem Statement
Two strings `X` and `Y` are similar if we can swap two letters (in different positions) of `X`, so that it equals `Y`. Also two strings `X` and `Y` are similar if they are equal.

For example, `"tars"` and `"rats"` are similar (swapping at 0 and 2), and `"rats"` and `"arts"` are similar (swapping at 0 and 1), but `"star"` is not similar to `"tars"`, `"rats"`, or `"arts"`.

Together, these form a connected group of strings where a string is in the group if it is similar to at least one other string in the group. We are given a list `strs` of strings where every string in `strs` is an anagram of every other string in `strs`. How many groups are there?

### Constraints
- `1 <= strs.length <= 300`
- `1 <= strs[i].length <= 300`
- `strs[i]` consists of lowercase English letters only.
- All the strings in `strs` are anagrams of each other.

### Example
**Input:** `strs = ["tars","rats","arts","star"]`
**Output:** `2`

### Python Implementation
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.count = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y
            self.count -= 1

def numSimilarGroups(strs: list[str]) -> int:
    def is_similar(s1, s2):
        diff = 0
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                diff += 1
                if diff > 2:
                    return False
        return diff == 0 or diff == 2

    n = len(strs)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_similar(strs[i], strs[j]):
                uf.union(i, j)

    return uf.count
```

---

## Problem 3: Sentence Similarity II
**LeetCode 737**

### Problem Statement
We can represent a sentence as an array of words, for example, the sentence `"I am happy with leetcode"` can be represented as `["I","am","happy","with","leetcode"]`.

Given two sentences `sentence1` and `sentence2` each represented as a string array and given a list of similar word pairs `similarPairs`, determine if the two sentences are similar.

Two words `w1` and `w2` are similar if they are the same word or if they are in the same similarity group. Transitivity applies: if `w1` and `w2` are similar and `w2` and `w3` are similar, then `w1` and `w3` are similar.

Two sentences are similar if they have the same length and the word at the `ith` position of `sentence1` is similar to the word at the `ith` position of `sentence2`.

### Constraints
- `1 <= sentence1.length, sentence2.length <= 1000`
- `1 <= similarPairs.length <= 2000`
- `similarPairs[i].length == 2`
- `1 <= sentence1[i].length, sentence2[i].length, similarPairs[i][j].length <= 20`
- All the words consist of lower case English letters only.

### Example
**Input:** `sentence1 = ["great","acting","skills"], sentence2 = ["fine","drama","talent"], similarPairs = [["great","good"],["fine","good"],["drama","acting"],["skills","talent"]]`
**Output:** `true`

### Python Implementation
```python
class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y

def areSentencesSimilarTwo(sentence1: list[str], sentence2: list[str], similarPairs: list[list[str]]) -> bool:
    if len(sentence1) != len(sentence2):
        return False

    uf = UnionFind()
    for u, v in similarPairs:
        uf.union(u, v)

    for w1, w2 in zip(sentence1, sentence2):
        if w1 == w2:
            continue
        if uf.find(w1) != uf.find(w2):
            return False

    return True
```
