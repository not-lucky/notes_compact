def longest_substring_without_repeating_characters(s: str) -> int:
    """
    Find the longest substring without repeating characters.
    Pattern: Sliding Window (Variable)
    Time: O(n)
    Space: O(min(n, m)) where m is size of character set
    """
    seen = {}
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1

        seen[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len

if __name__ == "__main__":
    # Test cases
    assert longest_substring_without_repeating_characters("abcabcbb") == 3
    assert longest_substring_without_repeating_characters("bbbbb") == 1
    assert longest_substring_without_repeating_characters("pwwkew") == 3
    assert longest_substring_without_repeating_characters("") == 0
    print("All tests passed!")
