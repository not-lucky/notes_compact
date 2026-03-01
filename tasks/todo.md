# Tries: Chapter README Fixes
- [x] Review and fix `13-tries/README.md` structure and explanations
- [x] Correct and enhance Python 3 typing for Trie snippets
- [x] Merge scattered sections into cohesive blocks
- [x] Improve the visual model of Trie and memory representation
- [x] Consolidate comparisons and when to use Tries
- [x] Review `tasks/lessons.md`

# Tries: Word Dictionary Fixes
- [x] Review and fix `13-tries/04-word-dictionary.md`
- [x] Review MagicDictionary and WordFilter for correctness
- [x] Review and fix time complexities and space complexities
- [x] Add missing progressive problems

# Tries: Trie Implementation Fixes
- [x] Refactor Basic Trie: Update the `TrieNode` and `Trie` classes with modern Python 3 type hints (`dict[str, 'TrieNode']`, `bool`).
- [x] Refactor Array Trie: Add type hints.
- [x] Fix Extended Operations:
    - Wrap the floating methods in an `ExtendedTrie` class or explicitly note they belong inside `Trie`.
    - Fix the `delete` method to be more understandable.
- [x] Fix `TrieWithCount`: Define `count` on the `TrieNode` explicitly instead of using `hasattr`.
- [x] Fix `MapSum`: Use a `TrieNode` structure instead of raw dicts for consistency.