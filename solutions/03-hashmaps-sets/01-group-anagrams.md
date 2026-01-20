# Group Anagrams

## Problem Statement

Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

An anagram is a word formed by rearranging the letters of another word.

**Example:**
```
Input: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
```

## Building Intuition

### Why This Works

The fundamental insight is that anagrams are strings with identical character compositions - they contain exactly the same letters in exactly the same quantities, just arranged differently. This means if we can find a way to represent this "character composition" in a canonical form, all anagrams will map to the same representation.

Sorting provides one such canonical form: when you sort the characters of any anagram, you get the same result. "eat", "tea", and "ate" all become "aet" when sorted. This sorted string acts as a fingerprint that uniquely identifies the anagram group. Similarly, a character frequency count (how many a's, b's, c's, etc.) provides another canonical representation - all anagrams have identical frequency distributions.

The hash map then becomes our grouping mechanism. We use the canonical form as a key, and as we iterate through strings, we simply append each one to the list associated with its key. Strings that are anagrams will naturally end up in the same list because they share the same key.

### How to Discover This

When you see a grouping problem, immediately think: "What property do items in the same group share?" For anagrams, the shared property is character composition. Once you identify this, the next question is: "How can I represent this shared property as a hash map key?" This leads to either sorting (simple but slower) or character counting (slightly more complex but faster for long strings).

### Pattern Recognition

This is the **Canonical Form Hashing** pattern. Whenever you need to group items by some equivalence relationship (anagrams, rotations, permutations), find a canonical representation that's identical for all equivalent items and use it as a hash map key.

## When NOT to Use

- **When order matters**: If you need to preserve the relative ordering between anagram groups or need the first occurrence to define the group, you may need additional tracking.
- **When memory is extremely constrained**: Hash maps require O(n*k) space; if you can't afford this, consider sorting the entire array with a custom comparator (though this changes time complexity).
- **When strings contain Unicode or mixed character sets**: The character-count approach using a 26-element array only works for lowercase ASCII; for general Unicode, use a Counter/dictionary instead.
- **When you need streaming/online processing**: This approach requires all strings upfront; for streaming, you'd need a different data structure like a trie or database.

## Approach

### Key Insight
Anagrams have the same characters with the same frequencies. We need a canonical form to identify them.

### Method 1: Sorted String as Key
Sort each string and use as dictionary key.

### Method 2: Character Count as Key
Use character frequency tuple as key (faster for long strings).

## Implementation

```python
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Group anagrams using sorted string as key.

    Time: O(n × k log k) - n strings, k is max length
    Space: O(n × k) - storing all strings
    """
    from collections import defaultdict

    groups = defaultdict(list)

    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)

    return list(groups.values())


def group_anagrams_count(strs: list[str]) -> list[list[str]]:
    """
    Group anagrams using character count as key.
    Better for long strings (O(k) vs O(k log k)).

    Time: O(n × k)
    Space: O(n × k)
    """
    from collections import defaultdict

    groups = defaultdict(list)

    for s in strs:
        # Create count tuple as key
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(s)

    return list(groups.values())


def group_anagrams_prime(strs: list[str]) -> list[list[str]]:
    """
    Using prime number products as key.
    Each letter maps to a prime; product is unique for anagrams.

    Time: O(n × k)
    Space: O(n)

    Note: May overflow for very long strings.
    """
    from collections import defaultdict

    # First 26 primes
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
              43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]

    groups = defaultdict(list)

    for s in strs:
        product = 1
        for c in s:
            product *= primes[ord(c) - ord('a')]
        groups[product].append(s)

    return list(groups.values())
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Sorted Key | O(n × k log k) | O(n × k) | Simple, widely used |
| Count Key | O(n × k) | O(n × k) | Better for long strings |
| Prime Product | O(n × k) | O(n) | Risk of overflow |

Where n = number of strings, k = maximum string length

## Edge Cases

1. **Empty input**: `[]` → `[]`
2. **Single string**: `["a"]` → `[["a"]]`
3. **Empty strings**: `["", ""]` → `[["", ""]]`
4. **All same**: `["a", "a"]` → `[["a", "a"]]`
5. **No anagrams**: `["abc", "def"]` → `[["abc"], ["def"]]`
6. **Unicode**: Use hash map, not array indexing

## Common Mistakes

1. **Using list as dict key**: Lists aren't hashable; use tuple
2. **Wrong character indexing**: `ord(c) - ord('a')` for lowercase
3. **Not handling empty strings**: Empty string is its own anagram group
4. **Modifying input strings**: Don't sort in-place if not allowed

## Visual Walkthrough

```
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

Using sorted key:
  "eat" → "aet" → groups["aet"] = ["eat"]
  "tea" → "aet" → groups["aet"] = ["eat", "tea"]
  "tan" → "ant" → groups["ant"] = ["tan"]
  "ate" → "aet" → groups["aet"] = ["eat", "tea", "ate"]
  "nat" → "ant" → groups["ant"] = ["tan", "nat"]
  "bat" → "abt" → groups["abt"] = ["bat"]

Result: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

## Variations

### Find All Anagrams in String
Find all starting indices where anagram of pattern exists.

### Valid Anagram
Check if two strings are anagrams.

### Anagram Difference
Find minimum characters to change to make two strings anagrams.

```python
def min_steps_anagram(s: str, t: str) -> int:
    """
    Minimum steps to make t an anagram of s.
    Each step: replace one character in t.
    """
    from collections import Counter

    s_count = Counter(s)
    t_count = Counter(t)

    # Count excess characters in t
    excess = 0
    for char, count in t_count.items():
        if count > s_count.get(char, 0):
            excess += count - s_count.get(char, 0)

    return excess
```

### Largest Anagram Group
Return the group with most anagrams.

```python
def largest_anagram_group(strs: list[str]) -> list[str]:
    """Find the anagram group with most members."""
    groups = group_anagrams(strs)
    return max(groups, key=len) if groups else []
```

## Interview Tips

1. **Clarify constraints**: Case sensitivity? Only lowercase letters?
2. **Discuss trade-offs**: Sorted key is simpler, count key is faster
3. **Handle edge cases**: Empty input, empty strings
4. **Space optimization**: If memory is tight, discuss streaming approaches

## Related Problems

- **Valid Anagram** - Check if two strings are anagrams
- **Find All Anagrams in a String** - Sliding window approach
- **Permutation in String** - Check if permutation exists
- **Minimum Window Substring** - Related character counting
- **Sort Characters By Frequency** - Related frequency problem
