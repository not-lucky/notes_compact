# Accounts Merge

> **Prerequisites:** [Union-Find Basics](./01-union-find-basics.md), [Connected Components](./04-connected-components.md)

## Interview Context

"Accounts Merge" (LeetCode 721) is a classic Union-Find problem that combines the data structure with string mapping. It tests your ability to map non-integer elements to Union-Find indices and correctly group related elements. This section also covers dictionary-based Union-Find, which is useful whenever keys are strings (or other hashable types) instead of integers.

Note: The `find`/`union` helpers are intentionally repeated in each solution below so that every code block is self-contained and copy-pasteable for interview practice.

---

## Building Intuition

**The "Email Detective" Mental Model**

Imagine you're a detective trying to identify people based on their email addresses:

```
Evidence:
Account 1: "John" uses john@gmail.com, john@work.com
Account 2: "John" uses john@home.com
Account 3: "John" uses john@work.com, john@school.com

Deduction:
- Accounts 1 and 3 share john@work.com → SAME PERSON!
- Account 2 has no overlap → DIFFERENT PERSON

Result: Two distinct people named "John"
```

The key insight: **Emails are the fingerprints**, not names. Two accounts merge if they share ANY email.

**The Transitive Chain**

```
Account A: email1, email2
Account B: email2, email3
Account C: email3, email4

email1 ←→ email2 ←→ email3 ←→ email4
         (all connected transitively!)

All four emails belong to ONE person.
```

**Why Union-Find Fits Perfectly**

This is a connectivity problem in disguise:

- **Nodes**: Email addresses
- **Edges**: Emails appearing in the same account
- **Groups**: All emails of one real person

Union-Find excels because:

1. We union all emails within each account
2. Transitive connections happen automatically
3. Final grouping is efficient via find()

```
Traditional approach (graph + BFS/DFS):
- Build adjacency list of email connections
- BFS/DFS from each unvisited email
- Track visited to avoid duplicates
- More bookkeeping

Union-Find approach:
- Union emails in same account (single loop)
- Group by root (simple dict aggregation)
- Clean, efficient, no visited tracking needed
```

---

## When NOT to Use Union-Find for Merging

**1. When Merge Logic is Complex**

Union-Find assumes binary connectivity: either connected or not. For nuanced merging rules:

```python
# "Merge accounts if they share 2+ emails" → Can't use basic UF
# "Merge accounts if names match AND share email" → Needs preprocessing

# Union-Find assumes: share ANY email = same person
```

**2. When You Need to Preserve Original Groups**

If you need to track which original accounts contributed to each merged account, Union-Find loses that information:

```python
# Union-Find: Tells you "these 5 emails belong together"
# Doesn't tell you: "This came from accounts 1, 3, and 7"

# If you need provenance, track it separately
```

**3. When Un-Merging is Required**

If accounts can later be "split" (e.g., user requests separation), Union-Find can't undo merges efficiently:

```python
# Union is permanent in standard Union-Find
# For reversible merging, consider different data structures
```

**4. For Small Input Sizes**

If there are only a few accounts (< 100), a simpler approach might be clearer:

```python
# Build graph, run DFS, group by component
# More lines of code but easier to understand
# For interview: mention you'd use Union-Find for scale
```

---

## Warm-Up: Group People by Shared Interests

Before tackling Accounts Merge, try this simpler grouping problem to build intuition.

**Problem**: Given a list of people, each with a set of interests, group all people who share at least one common interest (transitively). Return the groups of people.

```
Input:
people = [
    ["Alice", "hiking", "chess"],
    ["Bob", "chess", "cooking"],
    ["Carol", "swimming"],
    ["Dave", "cooking", "painting"],
]

Output: [["Alice", "Bob", "Dave"], ["Carol"]]

Explanation:
- Alice & Bob share "chess" → same group
- Bob & Dave share "cooking" → same group (Alice joins transitively)
- Carol has no overlap → separate group
```

### Solution

```python
from collections import defaultdict


def group_by_shared_interests(people: list[list[str]]) -> list[list[str]]:
    """
    Group people who share at least one interest (transitively).

    Strategy: Use Union-Find on person indices. For each interest,
    union all people who list that interest.

    Time:  O(n × k × α(n)) where n = number of people, k = avg interests per person
    Space: O(n + total unique interests)
    """
    n = len(people)
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

    # Map each interest to the first person who listed it.
    # When another person lists the same interest, union them.
    interest_to_person: dict[str, int] = {}

    for i, person_info in enumerate(people):
        interests = person_info[1:]  # person_info[0] is the name
        for interest in interests:
            if interest in interest_to_person:
                union(i, interest_to_person[interest])
            else:
                interest_to_person[interest] = i

    # Group person indices by their root
    groups: dict[int, list[str]] = defaultdict(list)
    for i, person_info in enumerate(people):
        groups[find(i)].append(person_info[0])

    return [sorted(names) for names in groups.values()]
```

**Key takeaway**: The pattern — map shared elements to Union-Find unions, then group by root — is exactly the same pattern used in Accounts Merge below.

---

## Stepping Stone: Smallest String With Swaps

**LeetCode 1202**: You are given a string `s` and a list of index pairs. You can swap the characters at any pair of indices any number of times. Return the lexicographically smallest string you can produce.

This bridges the gap to Accounts Merge: you use Union-Find to group indices, then sort within each group — the same "group by root, then sort" pattern.

```
Input: s = "dcab", pairs = [[0,3],[1,2]]
Output: "bacd"

Explanation:
- Indices 0 and 3 are connected → can freely rearrange s[0], s[3]: 'd','b'
- Indices 1 and 2 are connected → can freely rearrange s[1], s[2]: 'c','a'
- Sort each group: group {0,3} → 'b','d'; group {1,2} → 'a','c'
- Place back: s = "bacd"
```

### Solution

```python
from collections import defaultdict


def smallestStringWithSwaps(s: str, pairs: list[list[int]]) -> str:
    """
    Use Union-Find to group connected indices, sort characters
    within each group, then rebuild the string.

    Time:  O(n log n) where n = len(s) (dominated by sorting)
    Space: O(n)
    """
    n = len(s)
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

    # Union connected indices
    for i, j in pairs:
        union(i, j)

    # Group indices by root
    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)

    # Sort characters within each group, place back
    result = list(s)
    for indices in groups.values():
        chars = sorted(result[i] for i in indices)
        for i, c in zip(sorted(indices), chars):
            result[i] = c

    return "".join(result)
```

**Key takeaway**: This is the "group by root, then sort within group" pattern in its simplest form. Accounts Merge adds the complication of string-keyed UF and name tracking, but the core flow is identical.

---

## Problem Statement

Given a list of accounts where each account contains a name followed by emails, merge accounts that share at least one email. Return the merged accounts with emails sorted.

### Example

```
Input:
accounts = [
    ["John", "john@gmail.com", "john@work.com"],
    ["John", "john@home.com"],
    ["Mary", "mary@gmail.com"],
    ["John", "john@work.com", "john@school.com"]
]

Output:
[
    ["John", "john@gmail.com", "john@school.com", "john@work.com"],
    ["John", "john@home.com"],
    ["Mary", "mary@gmail.com"]
]

Explanation:
- Accounts 0 and 3 share "john@work.com" → merge into one group
  Merged emails: john@gmail.com, john@work.com, john@school.com (sorted)
- Account 1 ("john@home.com") has NO overlap with any other account → stays separate
- Account 2 (Mary) has no overlap → stays separate
- Note: Same name does NOT cause a merge — only shared emails do
```

---

## Approach: Union-Find with Email Mapping

### Key Steps

1. **Map emails to indices**: Each unique email gets an index
2. **Union emails in same account**: All emails in one account belong together
3. **Group by root**: Find all emails with same root
4. **Build result**: Associate each group with account name

### Visualization

```
Account 0: john@gmail.com, john@work.com
Account 1: john@home.com
Account 2: mary@gmail.com
Account 3: john@work.com, john@school.com

Step 1: Assign indices
john@gmail.com  → 0
john@work.com   → 1
john@home.com   → 2
mary@gmail.com  → 3
john@school.com → 4

Step 2: Union within accounts
Account 0: union(0, 1)  → {0, 1}
Account 1: (single email, no union)
Account 2: (single email, no union)
Account 3: union(1, 4)  → {0, 1, 4}

Step 3: Final groups
Root 0: [0, 1, 4] → john@gmail.com, john@work.com, john@school.com
Root 2: [2] → john@home.com
Root 3: [3] → mary@gmail.com
```

---

## Implementation

```python
from collections import defaultdict


def accountsMerge(accounts: list[list[str]]) -> list[list[str]]:
    """
    Merge accounts with Union-Find (index-based approach).

    Time:  O(E log E) where E = total emails across all accounts
           (dominated by sorting emails within each merged group)
    Space: O(E)
    """
    # Map each email to an index
    email_to_idx: dict[str, int] = {}
    email_to_name: dict[str, str] = {}
    idx: int = 0

    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in email_to_idx:
                email_to_idx[email] = idx
                email_to_name[email] = name
                idx += 1

    # Union-Find on indices
    n = len(email_to_idx)
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

    # Union all emails in the same account
    for account in accounts:
        first_email = account[1]
        first_idx = email_to_idx[first_email]

        for email in account[2:]:
            union(first_idx, email_to_idx[email])

    # Group emails by root
    groups: defaultdict[int, list[str]] = defaultdict(list)
    for email, email_idx in email_to_idx.items():
        root = find(email_idx)
        groups[root].append(email)

    # Build result
    result: list[list[str]] = []
    for root, emails in groups.items():
        # Get name from any email in the group
        name = email_to_name[emails[0]]
        # Sort emails and prepend name
        result.append([name] + sorted(emails))

    return result
```

---

## Alternative: Direct Email-to-Email Union

Instead of mapping to indices, union emails directly using a dictionary-based Union-Find.

```python
from collections import defaultdict


def accountsMerge_v2(accounts: list[list[str]]) -> list[list[str]]:
    """
    Direct email-to-email Union-Find without index mapping.

    Uses a dict-based UF with path compression and union by rank.
    Cleaner code than index-based approach, same complexity.

    Time:  O(E log E) where E = total emails across all accounts
    Space: O(E)
    """
    parent: dict[str, str] = {}
    rank: dict[str, int] = {}

    def find(x: str) -> str:
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: str, y: str) -> None:
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

    # Map each email to its account name and union within each account
    email_to_name: dict[str, str] = {}

    for account in accounts:
        name = account[0]
        first_email = account[1]

        for email in account[1:]:
            email_to_name[email] = name
            union(first_email, email)

    # Group emails by root
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for email in email_to_name:
        groups[find(email)].append(email)

    # Build result
    result: list[list[str]] = []
    for root, emails in groups.items():
        name = email_to_name[root]
        result.append([name] + sorted(emails))

    return result
```

---

## Step-by-Step Trace (Direct Email Approach)

Tracing `accountsMerge_v2` with abbreviated emails (a = a@g.com, etc.):

```python
accounts = [
    ["John", "a@g.com", "b@g.com"],
    ["John", "c@g.com"],
    ["John", "b@g.com", "d@g.com"],
    ["Mary", "e@g.com"]
]

# Processing each account (first_email = account[1]):
#
# Account 0: first_email = a
#   union(a, a) → find initializes a as root, no-op (same root)
#   union(a, b) → find initializes b as root, then parent[b] = a
#   parent: {a: a, b: a}
#
# Account 1: first_email = c
#   union(c, c) → find initializes c as root, no-op (same root)
#   parent: {a: a, b: a, c: c}
#
# Account 2: first_email = b
#   union(b, b) → find(b) = a, no-op (same root)
#   union(b, d) → find(b) = a, find initializes d as root
#                → parent[d] = a  (a, b, d all connected)
#   parent: {a: a, b: a, c: c, d: a}
#
# Account 3: first_email = e
#   union(e, e) → find initializes e as root, no-op (same root)
#   parent: {a: a, b: a, c: c, d: a, e: e}

# Grouping by find():
#   find(a) = a  →  group a: [a, b, d]
#   find(b) = a
#   find(c) = c  →  group c: [c]
#   find(d) = a
#   find(e) = e  →  group e: [e]

# Result (emails sorted within each group):
# ["John", "a@g.com", "b@g.com", "d@g.com"]
# ["John", "c@g.com"]
# ["Mary", "e@g.com"]
```

---

## Problem Variation: Similar String Groups

**LeetCode 839**: Two strings are similar if you can swap exactly two letters in one to get the other (or they are identical). Group all similar strings (transitively). Return the number of groups.

```
Input: strs = ["tars","rats","arts","star"]
Output: 2
Explanation:
- "tars" and "rats" are similar (swap t,r) → same group
- "rats" and "arts" are similar (swap r,a) → same group
- "star" is not similar to any of the above → separate group
- Groups: {"tars","rats","arts"}, {"star"}
```

```python
def numSimilarGroups(strs: list[str]) -> int:
    """
    Count groups of similar strings.

    Two strings are similar if they differ in exactly 0 or 2 positions
    (with those 2 positions being a valid swap). All input strings are
    anagrams of each other (guaranteed by the problem).

    Time: O(n² × m) where n = len(strs), m = string length
    Space: O(n)
    """
    n = len(strs)
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

    def similar(s1: str, s2: str) -> bool:
        """Check if s1 and s2 differ in exactly 0 or 2 swapped positions."""
        diff: list[int] = []
        for i, (c1, c2) in enumerate(zip(s1, s2)):
            if c1 != c2:
                diff.append(i)
                if len(diff) > 2:
                    return False

        if len(diff) == 0:
            return True  # Identical strings are similar
        if len(diff) == 2:
            i, j = diff
            return s1[i] == s2[j] and s1[j] == s2[i]
        return False  # 1 difference → can't fix with a single swap

    # Check all pairs
    for i in range(n):
        for j in range(i + 1, n):
            if similar(strs[i], strs[j]):
                union(i, j)

    # Count unique roots
    return len(set(find(i) for i in range(n)))
```

---

## Problem Variation: Sentence Similarity II

**LeetCode 737**: Words are similar if they're in the same similarity group (transitive). Check if two sentences are similar word-by-word.

```
Input:
sentence1 = ["great","acting","skills"]
sentence2 = ["fine","drama","talent"]
similarPairs = [["great","fine"],["acting","drama"],["skills","talent"]]

Output: True
Explanation: Each word in sentence1 maps to the corresponding word
in sentence2 through the similarity pairs.
```

```python
def areSentencesSimilarTwo(
    sentence1: list[str],
    sentence2: list[str],
    similarPairs: list[list[str]]
) -> bool:
    """
    Check sentence similarity with transitive similar words.

    Time: O(p × α(w) + n × α(w)) where p = pairs, w = unique words, n = sentence length
    Space: O(w)
    """
    if len(sentence1) != len(sentence2):
        return False

    parent: dict[str, str] = {}
    rank: dict[str, int] = {}

    def find(x: str) -> str:
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: str, y: str) -> None:
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

    # Build similarity groups
    for w1, w2 in similarPairs:
        union(w1, w2)

    # Check each word pair
    for w1, w2 in zip(sentence1, sentence2):
        if w1 == w2:
            continue
        if find(w1) != find(w2):
            return False

    return True
```

---

## Problem Variation: Synonymous Sentences

**LeetCode 1258**: Given a list of synonym pairs and a sentence, generate all possible sentences where each word can be replaced by any of its synonyms (transitively). Return sentences sorted lexicographically.

This problem uses the same dict-based UF pattern as Accounts Merge, but adds the step of enumerating all combinations from each synonym group.

```
Input:
synonyms = [["happy","joy"],["sad","sorrow"],["joy","cheerful"]]
text = "I am happy today but sad"

Synonym groups (transitive):
  {happy, joy, cheerful}  ← "happy" and "cheerful" linked through "joy"
  {sad, sorrow}

Output:
[
  "I am cheerful today but sad",
  "I am cheerful today but sorrow",
  "I am happy today but sad",
  "I am happy today but sorrow",
  "I am joy today but sad",
  "I am joy today but sorrow"
]
```

```python
from collections import defaultdict
from itertools import product


def generateSentences(
    synonyms: list[list[str]], text: str
) -> list[str]:
    """
    Generate all sentences with synonyms substituted.

    Strategy: Union-Find to build synonym groups, then enumerate
    all combinations using itertools.product.

    Time:  O(p × α(w) + S) where p = synonym pairs, w = unique words in pairs,
           S = total output size (product of group sizes for each word)
    Space: O(w + S)
    """
    parent: dict[str, str] = {}
    rank: dict[str, int] = {}

    def find(x: str) -> str:
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: str, y: str) -> None:
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

    # Build synonym groups
    for w1, w2 in synonyms:
        union(w1, w2)

    # Collect all synonyms by root
    groups: dict[str, list[str]] = defaultdict(list)
    for word in parent:
        groups[find(word)].append(word)

    # For each word in the sentence, get its sorted synonym group
    # (or just [word] if it has no synonyms)
    words = text.split()
    options: list[list[str]] = []
    for word in words:
        if word in parent:
            options.append(sorted(groups[find(word)]))
        else:
            options.append([word])

    # Generate all combinations, join into sentences.
    # product() on sorted lists yields tuples in lexicographic order,
    # so the resulting sentences are automatically sorted.
    return [" ".join(combo) for combo in product(*options)]
```

---

## Common Patterns

### 1. String-to-Index Mapping

```python
# When Union-Find needs integer indices but input is strings
item_to_idx: dict[str, int] = {}
idx: int = 0

for item in items:
    if item not in item_to_idx:
        item_to_idx[item] = idx
        idx += 1

# Now use item_to_idx[item] as Union-Find index
```

### 2. Dictionary-Based Union-Find

```python
# When items are hashable but not integers
parent: dict[str, str] = {}
rank: dict[str, int] = {}

def find(x: str) -> str:
    if x not in parent:
        parent[x] = x  # Initialize on first access
        rank[x] = 0
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(x: str, y: str) -> None:
    px, py = find(x), find(y)
    if px == py:
        return
    if rank[px] < rank[py]:
        px, py = py, px
    parent[py] = px
    if rank[px] == rank[py]:
        rank[px] += 1
```

### 3. First Element as Representative

```python
# Union all items to the first item in each group
for group in groups:
    first = group[0]
    for item in group[1:]:
        union(first, item)
```

---

## Complexity Analysis

For Accounts Merge with n accounts, k emails per account, and E = n × k total emails:

| Operation        | Time                 | Space              |
| ---------------- | -------------------- | ------------------ |
| Build email map  | O(E)                 | O(E)               |
| Union operations | O(E × α(E))          | O(1) (amortized)   |
| Group by root    | O(E × α(E))          | O(E)               |
| Sort groups      | O(E log E)           | O(E)               |
| **Total**        | **O(E log E)**       | **O(E)**           |

The sorting step dominates since α(E) is effectively constant (≤ 5 for any practical input).

---

## Edge Cases

1. **Single account**: Return as-is with sorted emails
2. **No overlapping emails**: Each account stays separate
3. **All accounts share one email**: All accounts merge into one
4. **Same name, different people**: Name doesn't cause merging — only shared emails do
5. **Long transitive chains**: Account A shares email with B, B with C, etc. — all merge into one group

---

## Interview Tips

1. **Clarify transitivity**: "If account A shares an email with B, and B with C, do A and C merge?" (Yes)
2. **Ask about name conflicts**: "Can different people share a name?" (Yes — names don't affect merging)
3. **Output format**: "Should emails be sorted? Any specific order of accounts in the result?"
4. **String vs index UF**: Mention both approaches. Index-based has lower constant factors (array access vs hashing); dict-based is cleaner and shorter. Pick based on interviewer preference
5. **Explain the pattern**: "Map shared elements → union → group by root → format output"

---

## Practice Problems

| #   | Problem                               | Difficulty | Key Concept                |
| --- | ------------------------------------- | ---------- | -------------------------- |
| 1   | Smallest String With Swaps (LC 1202)  | Medium     | Group indices, sort within |
| 2   | Accounts Merge (LC 721)               | Medium     | Email grouping             |
| 3   | Sentence Similarity II (LC 737)       | Medium     | Transitive similarity      |
| 4   | Synonymous Sentences (LC 1258)        | Medium     | Word group enumeration     |
| 5   | Similar String Groups (LC 839)        | Hard       | Pair-wise similarity       |
| 6   | Evaluate Division (LC 399)            | Medium     | Weighted Union-Find        |

---

## Related Sections

- [Connected Components](./04-connected-components.md) - Basic grouping
- [Redundant Connection](./06-redundant-connection.md) - Cycle detection
- [Hash Tables](../03-hashmaps-sets/README.md) - String mapping
