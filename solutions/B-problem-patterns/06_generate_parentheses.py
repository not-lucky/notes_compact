def generate_parentheses(n: int) -> list[str]:
    """
    Generate all valid combinations of n pairs of parentheses.
    Pattern: Backtracking
    Time: O(4^n / sqrt(n)) - Catalan number
    Space: O(n) for recursion stack
    """
    result = []

    def backtrack(current: str, open_count: int, close_count: int):
        if len(current) == 2 * n:
            result.append(current)
            return

        if open_count < n:
            backtrack(current + "(", open_count + 1, close_count)

        if close_count < open_count:
            backtrack(current + ")", open_count, close_count + 1)

    backtrack("", 0, 0)
    return result

if __name__ == "__main__":
    # Test cases
    assert sorted(generate_parentheses(3)) == sorted(["((()))","(()())","(())()","()(())","()()()"])
    assert generate_parentheses(1) == ["()"]
    print("All tests passed!")
